# Моніторинг — Prometheus + Grafana

Система моніторингу для контейнеризованого проєкту, розгорнутого в Microsoft Azure.

---

## Як розгортається моніторинг

Моніторинг запускається на тій самій Azure VM що і основний застосунок, через окремий Docker Compose файл.

**Крок 1.** Підключитись до VM:
```bash
ssh azureuser@PUBLIC_IP
```

**Крок 2.** Перейти в каталог проєкту:
```bash
cd /opt/app
```

**Крок 3.** Запустити стек моніторингу:
```bash
docker compose -f docker-compose.monitoring.yml up -d
```

**Крок 4.** Відкрити порти в Azure NSG (якщо не відкриті):
```bash
az network nsg rule create \
  --resource-group open-data-ai-rg \
  --nsg-name open-data-ai-vm-nsg \
  --name AllowGrafana \
  --priority 120 \
  --protocol Tcp \
  --destination-port-range 3000 \
  --access Allow \
  --direction Inbound

az network nsg rule create \
  --resource-group open-data-ai-rg \
  --nsg-name open-data-ai-vm-nsg \
  --name AllowPrometheus \
  --priority 130 \
  --protocol Tcp \
  --destination-port-range 9090 \
  --access Allow \
  --direction Inbound
```

---

## Які сервіси збирають метрики

| Сервіс | Опис |
|--------|------|
| **node-exporter** | Збирає метрики Linux VM: CPU, RAM, диск, мережа |
| **cAdvisor** | Збирає метрики Docker-контейнерів: використання ресурсів кожним контейнером |
| **Prometheus** | Збирає метрики самого себе та опитує всі інші сервіси кожні 15 секунд |

Конфігурація знаходиться у `monitoring/prometheus/prometheus.yml`.

---

## Які порти відкриті

| Порт | Сервіс | Призначення |
|------|--------|-------------|
| 3000 | Grafana | Веб-інтерфейс для дашбордів |
| 9090 | Prometheus | Веб-інтерфейс та API метрик |
| 9100 | node-exporter | Endpoint метрик VM |
| 8080 | cAdvisor | Endpoint метрик контейнерів |
| 5001 | Web app | Веб-інтерфейс застосунку |
| 22 | SSH | Підключення до VM |

---

## Як відкрити Grafana

1. Відкрити у браузері: `http://PUBLIC_IP:3000`
2. Логін: `admin`
3. Пароль: `admin123`

### Підключення Prometheus як Data Source

1. **Connections → Data sources → Add data source**
2. Вибрати **Prometheus**
3. URL: `http://PUBLIC_IP:9090`
4. Натиснути **Save & Test**

---

## Які панелі створено

Дашборд **"Memory Usage %"** містить три панелі:

### CPU Usage %
```promql
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```
Показує відсоток завантаження CPU VM в реальному часі.

### Memory Usage %
```promql
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```
Показує відсоток використання оперативної пам'яті VM.

### Running Containers
```promql
count(container_last_seen{image!=""})
```
Показує кількість активних Docker-контейнерів.

---

## Структура файлів моніторингу

```
monitoring/
└── prometheus/
    └── prometheus.yml        # Конфігурація Prometheus
docker-compose.monitoring.yml # Docker Compose для стеку моніторингу
```
