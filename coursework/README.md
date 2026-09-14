# Курсовая работа: персональный сайт Даниила Степанова

**[Открыть сайт курсовой](https://dasestepanov.github.io/devops-lab-stepanov/)**

[Отчёт о курсовой работе](COURSEWORK.md) · [Конфигурация MkDocs](mkdocs.yml) · [Исходники страниц](docs/) · [Готовая сборка](site/)

Готовый персональный сайт на MkDocs 1.6.1 и Material 9.7.7. Семь страниц, русский поиск, адаптивная навигация, портрет в рамке и галерея мемов.

## Запуск

Нужен Python 3.9 или новее. Откройте терминал в папке проекта.

macOS / Linux:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs --version
mkdocs serve -a 127.0.0.1:8010
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m mkdocs serve -a 127.0.0.1:8010
```

Откройте http://127.0.0.1:8010/. Для остановки нажмите Ctrl+C.

На macOS можно также запустить `./start.command` или открыть этот файл двойным щелчком в Finder. При первом запуске скрипт создаст окружение и установит зависимости.

## Сборка

```sh
python -m mkdocs build --strict
```

Результат находится в `site/`. Эта папка включена в репозиторий и архив. Чтобы просмотреть готовую сборку без установки MkDocs:

```sh
python3 -m http.server 8010 --directory site
```

В Windows вместо `python3` используйте `py`. Просматривайте через HTTP-сервер: поиск использует JavaScript и не рассчитан на прямое открытие HTML через `file://`.

## Структура

- `mkdocs.yml` — конфигурация, тема, поиск, навигация, палитра и футер.
- `docs/*.md` — семь страниц сайта.
- `docs/images/` — оригинальное фото, пять мемов и SVG-логотип «ДС».
- `docs/stylesheets/extra.css` — индивидуальное оформление и мобильная адаптация.
- `requirements.txt` — зафиксированные версии зависимостей.
- `site/` — готовая статическая сборка.
- `COURSEWORK.md` — описание реализации и результатов проверки.

## Редактирование

Содержимое меняется в Markdown-файлах папки `docs/`, затем сайт пересобирается. Базовые цвета: Powder Blue `#9DB3D3` и Vintage Wine `#3F1521`. Шрифты системные, изображения локальные; загрузка шрифтов из Google не требуется.

Личные контакты автор не предоставил. В `docs/contacts.md` оставлено явное уведомление; ссылки Сбера и ИТМО подписаны как ссылки организаций. Когда будут известны личные адреса, добавьте email и социальные сети на страницу и в `extra.social` конфигурации. Сайт опубликован на GitHub Pages, адрес указан в `site_url`.

## При желании: GitHub Pages

После создания собственного GitHub-репозитория, настройки Git remote и добавления фактического `site_url` можно выполнить `mkdocs gh-deploy`. В настройках Pages выберите ветку `gh-pages`. Команда публикует сайт в настроенный репозиторий, поэтому перед запуском проверьте `git remote -v`.

## Документация

- [MkDocs: конфигурация](https://www.mkdocs.org/user-guide/configuration/)
- [Material: навигация](https://squidfunk.github.io/mkdocs-material/setup/setting-up-navigation/)
- [Markdown Guide](https://www.markdownguide.org/)
