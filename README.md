# Лабораторные работы — введение в веб-технологии

Степанов Даниил Сергеевич, U4225, 2026/2027. GitHub: [dasestepanov](https://github.com/dasestepanov).

Автоматическая сборка и публикация Flask-приложения из лабораторной №1 через GitHub Actions. Деплой реализован сообщением `echo`, как разрешено заданием.

- [Лабораторная №2 — CI/CD](lab2/lab2_report.md)
- [Лабораторная №3 — мониторинг и безопасность](lab3/lab3_report.md)
- [Конфигурация стенда №3](lab3/compose.yaml)
- [Пайплайн](.github/workflows/docker-build.yml)
- [Протоколы локальных проверок](lab2/logs/)
- [Исходная лабораторная №1](https://github.com/dasestepanov/devops-lab-stepanov/tree/main/lab1)

## Запуск CI/CD

1. В Docker Hub аккаунта Даниила создать репозиторий `my-flask-app`.
2. В GitHub: Settings → Secrets and variables → Actions добавить `DOCKER_USERNAME` (Docker ID Даниила) и `DOCKER_PASSWORD` (его Docker Hub access token с правами Read & Write).
3. Отправить коммит в `main` или выбрать Actions → Build, publish and deploy Docker image → Run workflow.
4. Проверить успешный запуск и тег `latest` в Docker Hub.

Секреты в файлы проекта не записываются. Пока они не добавлены, шаг Check required secrets завершит запуск с понятной ошибкой.

## Локальная проверка

```sh
docker build -t my-flask-app:local .
docker run --rm -p 127.0.0.1:5002:5000 my-flask-app:local
# В другом терминале:
curl -i http://127.0.0.1:5002/
```

Ожидается HTTP 200 и `Hello from Docker!`. CI собирает `linux/amd64`; на Apple Silicon локальная сборка без указания платформы создаёт `arm64`.
