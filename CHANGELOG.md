# Changelog

## [0.1.0] — 2026-05-07
### Added
- Базова структура проєкту (`data/`, `src/`, `notebooks/`, `reports/figures/`).
- Модуль `data_load` — завантаження датасету з data.gov.ua (підтримка cp1251, auto-detect sep).
- Модуль `data_quality_analysis` — перевірка пропусків, дублікатів, типів, конвертація числових рядків.
- Модуль `data_research` — описова статистика, розкид між сценаріями, порівняння 2020 vs 2021.
- Модуль `visualization` — три графіки: порівняння сценаріїв, розкид, зміна YoY.
- README з метою, джерелом даних і гіпотезами.

## [0.2.0] — 2026-05-07
### Added
- GitHub Actions CI workflow (`ci.yml`) з matrix strategy для 4 модулів.
- Паралельний запуск модулів на GitHub-hosted runner (ubuntu-latest, Python 3.11).
- Ручний запуск pipeline через `workflow_dispatch` з вибором конкретного модуля.
- Збереження артефактів (логи, графіки) після кожного CI run.
- Self-hosted runner на локальному MacBook Air M4 (macOS ARM64).
- Окремий workflow `ci-selfhosted.yml` для запуску visualization на self-hosted runner.