# Anthropic ProxyAPI CLI Utility

Утилита командной строки для взаимодействия с моделями Anthropic (Claude) через сервис ProxyAPI.ru

![CLI Demo](https://img.shields.io/badge/CLI-Demo-blueviolet)
![Python](https://img.shields.io/badge/Python-3.8%2B-success)
![License](https://img.shields.io/badge/License-MIT-green)

## Особенности

- Поддержка последних моделей Claude 3
- Работа с промптами из файла или командной строки
- Настройка параметров генерации (температура, токены)
- Кроссплатформенная работа (Windows/Linux/macOS)
- Безопасное хранение API-ключа
- Подробное логирование ошибок

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/lightclove/anthropic-proxy-cli.git
cd anthropic-proxy-cli
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Использование

### Базовые команды

```bash
python ai_client.py \
  --api-key YOUR_API_KEY \
  --model claude-3-5-haiku-20241022 \
  --prompt "Ваш текст запроса" \
  --max-tokens 500 \
  --temperature 0.7
```

### Примеры

### Запрос из файла:

```bash
python ai_client.py \
  --api-key sk-... \
  --model claude-3-7-sonnet-20250219 \
  --file input.txt \
  --max-tokens 1500
```
### Показать помощь:

```bash
python ai_client.py --help
```

### Параметры

- Аргумент	    Обязательный	  Описание

- --api-key	    Да	            API ключ от ProxyAPI

- --model	       Да	  Выбор модели   (см. список ниже)

- --prompt	    Нет*	          Текст запроса

- --file	      Нет*	          Файл с промптом

- --max-tokens	Нет	            Макс. токенов (по умолчанию 1024)

- --temperature	Нет	            Креативность (0.0-1.0)

- --timeout	    Нет	            Таймаут запроса (сек)

- *Обязательно указать либо --prompt, либо --file

### Поддерживаемые модели

- claude-3-5-haiku-20241022

- claude-3-5-sonnet-20241022

- claude-3-7-sonnet-20250219

## Настройка окружения
Для постоянного хранения API-ключа создайте файл .env:

```bash
ANTHROPIC_API_KEY=your_api_key_here
```

И используйте в коде:

```bash
import os
api_key = os.getenv("ANTHROPIC_API_KEY")
```

### Обработка ошибок
Утилита предоставляет детальную информацию об ошибках:

- HTTP статусы API

- Проблемы с сетью

- Ошибки формата ответа

- Проблемы с файлами ввода

### Лицензия
Данный проект распространяется под лицензией MIT.

### Документация
Официальная документация ProxyAPI: https://proxyapi.ru

Anthropic API Reference: https://docs.anthropic.com/
