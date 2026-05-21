# Звіт з лабораторної роботи №7
**Тема:** Моніторинг за допомогою Prometheus та Grafana  
**Студент:** Максим Грицишин | ШІ-2023

---

## Мета роботи

Організувати базовий моніторинг контейнеризованого застосунку, розгорнутого в Microsoft Azure, за допомогою Prometheus і Grafana.

---

## 1. Джерела метрик

У роботі використано три рівні спостереження:

| Сервіс | Порт | Що збирає |
|--------|------|-----------|
| **node-exporter** | 9100 | Метрики Linux VM: CPU, RAM, диск, мережа |
| **cAdvisor** | 8080 | Метрики Docker-контейнерів |
| **Prometheus** | 9090 | Метрики самого себе |

### Конфігурація Prometheus (prometheus.yml)

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
```

---

## 2. Метрики на дашборді

На дашборді **"Memory Usage %"** в Grafana створено три панелі:

### 2.1. CPU Usage %

**PromQL запит:**
```
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

Показує відсоток використання CPU VM. Під час роботи значення становило ~3.8% — VM працює з мінімальним навантаженням.

### 2.2. Memory Usage %

**PromQL запит:**
```
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```

Показує відсоток використаної оперативної пам'яті. Значення коливалось в діапазоні 18-21%.

### 2.3. Running Containers

**PromQL запит:**
```
count(container_last_seen{image!=""})
```

Показує кількість запущених контейнерів. Значення = 7.

---

## 3. Розгортання стеку моніторингу

### 3.1. Terraform apply — створення VM

![terraform apply](screenshots/terraform_apply.jpeg)

VM створена в Poland Central з public IP `74.248.148.77`.

### 3.2. Відкриття порту 3000 для Grafana

![nsg grafana port](screenshots/nsg_grafana_port.jpeg)

Через Azure CLI додано правило AllowGrafana (порт 3000) в Network Security Group.

### 3.3. Запущені контейнери

![docker ps](screenshots/docker_ps.jpeg)

Всі 7 контейнерів запущені: grafana, prometheus, cadvisor, node-exporter, web, data_load, postgres.

| Контейнер | Image | Порт |
|-----------|-------|------|
| prometheus | prom/prometheus:latest | 9090 |
| grafana | grafana/grafana:latest | 3000 |
| node-exporter | prom/node-exporter:latest | 9100 |
| cadvisor | gcr.io/cadvisor/cadvisor:latest | 8080 |

---

## 4. Налаштування Grafana

### 4.1. Головна сторінка Grafana

![grafana home](screenshots/grafana_home.jpeg)

Grafana доступна за адресою `http://74.248.148.77:3000`.

### 4.2. Підключення Prometheus як Data Source

![grafana datasource](screenshots/grafana_datasource.jpeg)

Prometheus підключено за адресою `http://74.248.148.77:9090` — **Successfully queried the Prometheus API**.

### 4.3. Перевірка метрик у Prometheus

![prometheus query](screenshots/prometheus_query.jpeg)

Запит `up` повертає значення 1 для всіх трьох targets:
- `node-exporter:9100` — UP
- `localhost:9090` — UP
- `cadvisor:8080` — UP

---

## 5. Дашборд

### 5.1. Готовий дашборд з трьома панелями

![grafana dashboard](screenshots/grafana_dashboard.jpeg)

Дашборд відображає в реальному часі:
- **Memory Usage %** — ~20%
- **CPU Usage %** — ~3.8%
- **Running Containers** — 7

### 5.2. Панель Running Containers

![grafana containers](screenshots/grafana_containers.jpeg)

Запит `count(container_last_seen{image!=""})` повертає 7 — всі контейнери активні.

---

## 6. Труднощі та їх вирішення

**Проблема 1:** Імпортований дашборд Node Exporter Full (ID: 1860) показував "No data" — змінні Job та Nodename не підтягувались автоматично.  
**Вирішення:** Створено власний дашборд вручну з конкретними PromQL запитами.

**Проблема 2:** Grafana не могла підключитись до Prometheus за адресою `http://prometheus:9090` (DNS не резолвиться між різними Docker networks).  
**Вирішення:** Використано публічну IP-адресу VM `http://74.248.148.77:9090` як URL для data source.

---

## 7. Спостереження за результатами моніторингу

- **CPU:** ~3.8% — VM майже не навантажена, Standard_B2s_v2 з надлишком для цього проєкту
- **RAM:** ~20% (~800 MB з 4 GB) — всі 7 контейнерів споживають помірну кількість пам'яті
- **Контейнери:** 7 активних — застосунок і моніторинг стабільно працюють
- Графіки оновлюються кожну хвилину, що дозволяє спостерігати динаміку в реальному часі

---

## Висновки

У ході лабораторної роботи успішно реалізовано систему моніторингу:

- Розгорнуто стек Prometheus + Grafana + Node Exporter + cAdvisor в Docker
- Prometheus збирає метрики з трьох джерел кожні 15 секунд
- Grafana підключена до Prometheus і відображає дашборд з реальними даними
- Створено три панелі моніторингу: CPU, RAM, кількість контейнерів
- Набуто практичний досвід роботи з системами спостереження в хмарному середовищі
