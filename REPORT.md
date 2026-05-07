# Звіт: Використання системи контролю версій Git


**Репозиторій:** https://github.com/maksym-hrytsyshyn/open-data-ai-analytics

## Що зроблено
- Створено структуру проєкту, налаштовано `.gitignore`.
- Реалізовано 4 модулі в окремих feature-гілках:
  `feature/data_load`, `feature/data_quality_analysis`,
  `feature/data_research`, `feature/visualization`.
- Усі гілки злиті в `main` через PR на GitHub з описом змін.
- Створено merge-конфлікт у README.md між гілками
  `feature/data_quality_analysis` і `feature/data_research`.
  Конфлікт розв'язано вручну — залишено версію гіпотез з data_quality_analysis.
- Додано CHANGELOG.md і поставлено тег `v0.1.0`.

## Як виник і вирішився merge-конфлікт
Обидві гілки (`feature/data_quality_analysis` і `feature/data_research`)
змінювали секцію "Питання та гіпотези" у README.md по-різному.
Після мерджу першої гілки, при спробі змерджити другу GitHub виявив конфлікт.
Конфлікт розв'язано через веб-редактор GitHub — залишено фінальну версію
гіпотез і зроблено merge commit.

## git log
(base) mcs@MacBook-Air-Maksim open-data-ai-analytics % git log --oneline --graph --decorate --all
* 017e771 (HEAD -> main, tag: v0.1.0, origin/main, origin/HEAD) docs: add CHANGELOG for v0.1.0
*   db794e9 Merge pull request #4 from maksym-hrytsyshyn/feature/visualization
|\  
| * 7c05808 (origin/feature/visualization, feature/visualization) feat(visualization): add scenario comparison, spread and YoY change plots
|/  
*   fcc6308 Merge pull request #2 from maksym-hrytsyshyn/feature/data_research
|\  
| *   d4b0567 Merge branch 'main' into feature/data_research
| |\  
| |/  
|/|   
* |   b2c0197 Merge pull request #3 from maksym-hrytsyshyn/feature/data_quality_analysis
|\ \  
:...skipping...
* 017e771 (HEAD -> main, tag: v0.1.0, origin/main, origin/HEAD) docs: add CHANGELOG for v0.1.0
*   db794e9 Merge pull request #4 from maksym-hrytsyshyn/feature/visualization
|\  
| * 7c05808 (origin/feature/visualization, feature/visualization) feat(visualization): add scenario comparison, spread and YoY change plots
|/  
*   fcc6308 Merge pull request #2 from maksym-hrytsyshyn/feature/data_research
|\  
| *   d4b0567 Merge branch 'main' into feature/data_research
| |\  
| |/  
|/|   
* |   b2c0197 Merge pull request #3 from maksym-hrytsyshyn/feature/data_quality_analysis
|\ \  
| * | 5e22e4f (origin/feature/data_quality_analysis, feature/data_quality_analysis) feat(quality): update hypotheses based on quality analysis findings
| * | d88441e fix(quality):  delete comments
| * | 1f19fe3 feat(quality): add quality report and numeric coercion for UA-formatted numbers
:...skipping...
* 017e771 (HEAD -> main, tag: v0.1.0, origin/main, origin/HEAD) docs: add CHANGELOG for v0.1.0
*   db794e9 Merge pull request #4 from maksym-hrytsyshyn/feature/visualization
|\  
| * 7c05808 (origin/feature/visualization, feature/visualization) feat(visualization): add scenario comparison, spread and YoY change plots
|/  
*   fcc6308 Merge pull request #2 from maksym-hrytsyshyn/feature/data_research
|\  
| *   d4b0567 Merge branch 'main' into feature/data_research
| |\  
| |/  
|/|   
* |   b2c0197 Merge pull request #3 from maksym-hrytsyshyn/feature/data_quality_analysis
|\ \  
| * | 5e22e4f (origin/feature/data_quality_analysis, feature/data_quality_analysis) feat(quality): update hypotheses based on quality analysis findings
| * | d88441e fix(quality):  delete comments
| * | 1f19fe3 feat(quality): add quality report and numeric coercion for UA-formatted numbers
|/ /  
:...skipping...
* 017e771 (HEAD -> main, tag: v0.1.0, origin/main, origin/HEAD) docs: add CHANGELOG for v0.1.0
*   db794e9 Merge pull request #4 from maksym-hrytsyshyn/feature/visualization
|\  
| * 7c05808 (origin/feature/visualization, feature/visualization) feat(visualization): add scenario comparison, spread and YoY change plots
|/  
*   fcc6308 Merge pull request #2 from maksym-hrytsyshyn/feature/data_research
|\  
| *   d4b0567 Merge branch 'main' into feature/data_research
| |\  
| |/  
|/|   
* |   b2c0197 Merge pull request #3 from maksym-hrytsyshyn/feature/data_quality_analysis
|\ \  
| * | 5e22e4f (origin/feature/data_quality_analysis, feature/data_quality_analysis) feat(quality): update hypotheses based on quality analysis findings
| * | d88441e fix(quality):  delete comments
| * | 1f19fe3 feat(quality): add quality report and numeric coercion for UA-formatted numbers
|/ /  
| * 7fdb809 (origin/feature/data_research, feature/data_research) feat(research): add EDA module and refine hypotheses
|/  
*   ca5bbca Merge pull request #1 from maksym-hrytsyshyn/feature/data_load
|\  
| * c348352 (origin/feature/data_load, feature/data_load) feat(data_load): add CSV downloader for macro indicators dataset
|/  
* c05d719 docs: add project goal, data source and hypotheses
* 13c9d15 chore: initial project structure and .gitignore
~
~
~
~
~
~
~
~
~
~
