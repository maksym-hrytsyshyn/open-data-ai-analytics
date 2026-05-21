# Лабораторна №6 — Terraform + Azure Cloud Shell + cloud-init

## Мета
Розгортання Docker-проєкту в Microsoft Azure засобами Terraform + Cloud Shell + cloud-init без локального середовища.

## Структура
```
infra/terraform/
├── main.tf          # Terraform ресурси Azure
├── variables.tf     # Змінні (регіон, розмір VM тощо)
├── outputs.tf       # Outputs (public IP, web URL, SSH)
└── cloud-init.yaml  # Автоматичне налаштування VM
```

## Розгортання

### 1. Відкрити Azure Cloud Shell
1. Увійдіть на [portal.azure.com](https://portal.azure.com)
2. Натисніть іконку **`>_`** у верхньому меню
3. Виберіть **Bash**

### 2. Клонувати репозиторій
```bash
git clone https://github.com/maksym-hrytsyshyn/open-data-ai-analytics
cd open-data-ai-analytics/infra/terraform
```

### 3. Ініціалізувати Terraform
```bash
terraform init
terraform fmt
terraform validate
terraform plan
```

### 4. Виконати terraform apply
```bash
terraform apply
```
Введіть `yes` для підтвердження. Створення інфраструктури займає ~3-5 хвилин.

### 5. Перевірити результат
Після завершення `terraform apply` у виводі з'явиться:
```
public_ip_address = "XX.XX.XX.XX"
web_url           = "http://XX.XX.XX.XX:5001"
ssh_command       = "ssh azureuser@XX.XX.XX.XX"
```

Зачекайте ~5 хвилин поки cloud-init завершить налаштування VM, потім:
```bash
curl http://XX.XX.XX.XX:5001
```

Або відкрийте у браузері: **http://XX.XX.XX.XX:5001**

### 6. Перевірка через SSH
```bash
ssh azureuser@XX.XX.XX.XX
# Пароль: P@ssw0rd1234!

# Перевірити контейнери
docker ps

# Переглянути логи cloud-init
sudo tail -f /var/log/cloud-init-output.log
```

### 7. Видалити ресурси після демонстрації
```bash
terraform destroy
```
Введіть `yes`. Це видалить усі створені ресурси Azure.

## Параметри VM
| Параметр | Значення |
|----------|----------|
| Регіон | Poland Central |
| Розмір | Standard_B2s_v2 (2 vCPU, 4 GB RAM) |
| ОС | Ubuntu 22.04 LTS |
| Порт SSH | 22 |
| Порт Web | 5001 |

## Примітки
- Azure for Students надає $100 кредит без банківської картки
- Файл `.env` не входить до репозиторію — потрібно створити вручну на VM
- Університетська підписка підтримує регіон Poland Central
