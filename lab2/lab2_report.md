University: [ITMO University](https://itmo.ru/ru/)

Faculty: [FICT](https://fict.itmo.ru)

Course: [Введение в веб технологии](https://ex-itmo-ict-faculty.github.io/introduction-in-web-tech/)

Year: 2026/2027

Group: U4225

Author: Степанов Даниил Сергеевич

Lab: Lab2

Date of create: 12.09.2026

Date of finished: — (дата защиты)

# Лабораторная работа №2. Настройка CI/CD пайплайна

## Цель работы

Научиться настраивать автоматизированные пайплайны сборки Docker-образов, публикации в registry и запуска этапа деплоя при изменении кода.

## Задание

Перенести приложение из первой лабораторной в новый репозиторий; настроить GitHub Actions для push в main, сборки Buildx, входа в Docker Hub с помощью секретов, публикации `username/my-flask-app:latest` и имитации деплоя через echo. Проверить запуск в Actions и появление образа в Docker Hub.

## 1. Подготовка проекта

Создан отдельный репозиторий [2026_2027-introduction-in-web-tech-u4225-stepanov_d_s](https://github.com/dasestepanov/2026_2027-introduction-in-web-tech-u4225-stepanov_d_s) аккаунта `dasestepanov`. Название отражает учебный год, курс, группу и ФИО, как требуют правила оформления. Данные автора и учебный год перенесены из первой лабораторной; дата защиты пока не заполнена.

В корень скопированы без изменения [app.py](../app.py), [requirements.txt](../requirements.txt), [Dockerfile](../Dockerfile) и [.dockerignore](../.dockerignore). Исходники взяты из лабораторной №1, коммит `6a79338` репозитория `dasestepanov/devops-lab-stepanov`.

Приложение Flask отвечает `Hello from Docker!` на `/`, слушает `0.0.0.0:5000`. Dockerfile использует `python:3.9-slim`, устанавливает Flask 2.0.1 и совместимую версию Werkzeug 2.0.3, запускает приложение от `appuser` с UID 1000. Существующий учебный стек сохранён для соответствия первой работе.

```text
.github/workflows/docker-build.yml
app.py
requirements.txt
Dockerfile
.dockerignore
.gitignore
README.md
LICENSE
lab2/
  lab2_report.md
  logs/
```

Отчёт находится в `lab2`, а приложение — в корне нового репозитория. Поэтому контекст сборки в workflow указан как `.`. `.dockerignore` исключает отчёт и логи из контекста Docker. `.gitignore` исключает служебные файлы и локальные переменные окружения.

## 2. Настройка GitHub Actions

Создан файл [.github/workflows/docker-build.yml](../.github/workflows/docker-build.yml):

```yaml
name: Build, publish and deploy Docker image

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: docker-publish-${{ github.ref }}
  cancel-in-progress: false

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - name: Checkout code
        uses: actions/checkout@v6

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Check required secrets
        env:
          DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
          DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
        run: |
          test -n "$DOCKER_USERNAME" || { echo '::error::Set DOCKER_USERNAME in repository secrets'; exit 1; }
          test -n "$DOCKER_PASSWORD" || { echo '::error::Set DOCKER_PASSWORD in repository secrets'; exit 1; }

      - name: Login to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push Docker image
        id: build
        uses: docker/build-push-action@v7
        with:
          context: .
          file: ./Dockerfile
          platforms: linux/amd64
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/my-flask-app:latest

      - name: Deploy (simulation)
        env:
          IMAGE: ${{ secrets.DOCKER_USERNAME }}/my-flask-app:latest
          DIGEST: ${{ steps.build.outputs.digest }}
        run: |
          echo "Deployment simulation: image $IMAGE is ready ($DIGEST)."
          echo 'No remote server is changed; this is the echo deployment allowed by the lab.'
          {
            echo '### Lab 2 — Docker CI/CD'
            echo "Image: $IMAGE"
            echo "Digest: $DIGEST"
            echo 'Deployment: echo simulation completed.'
          } >> "$GITHUB_STEP_SUMMARY"
```

| Этап | Назначение |
|---|---|
| push → main | Автоматически запускает workflow после изменения основной ветки |
| workflow_dispatch | Позволяет повторить проверку вручную после настройки секретов |
| ubuntu-latest | Выполняет задачу на Linux runner GitHub |
| Checkout code | Получает файлы текущего коммита |
| Set up Docker Buildx | Подготавливает расширенный сборщик Docker |
| Check required secrets | Проверяет наличие учётных данных без вывода их значений |
| Login to Docker Hub | Авторизует Docker с помощью двух secrets репозитория |
| Build and push Docker image | Собирает linux/amd64 и публикует тег latest |
| Deploy (simulation) | Выводит сообщение об образе и его digest после успешной публикации |

Права `contents: read` достаточны для получения исходников. `concurrency` упорядочивает публикации одной ветки, чтобы одновременные запуски не перезаписывали latest в случайном порядке. Таймаут задачи — 20 минут. Ошибка любого шага останавливает последующие шаги.

Тег образа формируется из Docker ID в `DOCKER_USERNAME`, поэтому логины GitHub и Docker Hub могут различаться. `latest` — изменяемый тег, а digest идентифицирует конкретное содержимое образа. Значение digest добавляется в сводку Actions.

Деплой является **имитацией**, разрешённой условием: команда echo не запускает контейнер на внешнем сервере. Реальный автоматический деплой потребовал бы доступа к целевому серверу и команд обновления сервиса.

## 3. Подготовка Docker Hub и секретов

Для завершения внешней проверки нужен Docker Hub аккаунт Степанова Даниила. В нём следует создать репозиторий `my-flask-app` и access token с правами Read & Write. В GitHub нужно открыть Settings → Secrets and variables → Actions → New repository secret и добавить:

| Имя | Значение |
|---|---|
| DOCKER_USERNAME | Docker ID Степанова Даниила |
| DOCKER_PASSWORD | Docker Hub access token того же аккаунта |

Значения секретов не помещаются в исходники, отчёт или скриншоты. Вместо пароля аккаунта можно использовать отзываемый токен. Один лишь успешный локальный docker build не проверяет авторизацию в Docker Hub.

## 4. Фактически выполненные локальные проверки

Окружение: Docker Desktop, сервер Docker 29.6.1, Linux-контейнеры, архитектура aarch64. Выполнено:

```sh
docker build --progress=plain -t my-flask-app:lab2-20260912 .
docker run -d --name lab2-20260912-flask \
  -p 127.0.0.1:5002:5000 my-flask-app:lab2-20260912
curl --fail --retry 5 --retry-connrefused -i http://127.0.0.1:5002/
docker exec lab2-20260912-flask id
docker exec lab2-20260912-flask pip check
```

Сборка завершилась с кодом 0. Использован кэш слоёв первой лабораторной: исходники и Dockerfile не менялись. Контейнер успешно запущен; HTTP-запрос вернул статус 200 и `Hello from Docker!`. `id` подтвердил `uid=1000(appuser)`, `pip check` — `No broken requirements found.`

Порт 5002 выбран для отдельного экземпляра второй работы. Порт внутри контейнера остаётся 5000. Локально получен образ arm64, тогда как GitHub runner собирает linux/amd64: локальная проверка не является подтверждением выполнения сборки на runner.

Подтверждения: [полный лог сборки](logs/01-build.txt), [HTTP-ответ, UID, зависимости и логи приложения](logs/02-smoke-test.txt). Это текстовые протоколы фактически выполненных команд.

## 5. Проверка публикации и деплоя

После добавления секретов необходимо выполнить push в main или запустить workflow вручную. В Actions проверяются Checkout, Buildx, Login, Build and push и Deploy. В Docker Hub на странице репозитория проверяется тег latest и digest; digest должен совпасть со сводкой Actions.

Дополнительная проверка опубликованного образа после успешного CI (вместо DOCKER_ID подставить реальный логин):

```sh
docker pull --platform linux/amd64 DOCKER_ID/my-flask-app:latest
docker run --rm --platform linux/amd64 -p 127.0.0.1:5003:5000 DOCKER_ID/my-flask-app:latest
# В другом терминале:
curl -i http://127.0.0.1:5003/
```

Первый коммит `8399daa` отправлен в `main` от автора Степанова Даниила Сергеевича с SSH-аутентификацией аккаунта `dasestepanov`. Автоматически создан [запуск Actions №34689599720](https://github.com/dasestepanov/2026_2027-introduction-in-web-tech-u4225-stepanov_d_s/actions/runs/34689599720). GitHub подтвердил успешное выполнение Checkout и Set up Docker Buildx. Шаг Check required secrets завершился ошибкой: секреты ещё не настроены. Login, Build and push и Deploy были пропущены. [Протокол статусов шагов из GitHub API](logs/03-actions.txt).

**Статус внешней проверки:** автоматический запуск подтверждён; ожидается настройка Docker Hub и секретов. Успешная публикация и этап Deploy пока не подтверждены. Ссылку на успешный запуск и digest следует добавить после фактического выполнения; вымышленные результаты не приводятся.

## Вывод

Подготовлен CI/CD workflow с автоматическим запуском по push в main, Linux runner, Buildx, авторизацией через secrets, публикацией Docker-образа и разрешённой имитацией деплоя. Локально подтверждены сборка, запуск приложения, HTTP 200 и отсутствие конфликтов зависимостей. Для завершения лабораторной остаётся подтвердить публикацию и выполнение Deploy в GitHub Actions с Docker Hub аккаунтом автора.

## Источники

1. [Правила оформления отчёта](https://ex-itmo-ict-faculty.github.io/introduction-in-web-tech/education/labs2025-2026/reportdesign/).
2. [GitHub Actions](https://docs.github.com/en/actions).
3. [Docker Build and push action — официальный пример](https://github.com/docker/build-push-action).
4. [Docker Hub access tokens](https://docs.docker.com/docker-hub/access-tokens/).
5. [Docker Buildx](https://docs.docker.com/buildx/).
