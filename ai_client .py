#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import requests
import json
import sys
import os
from typing import List, Dict, Optional

SUPPORTED_MODELS = [
    "claude-3-5-haiku-20241022",
    "claude-3-5-sonnet-20241022",
    "claude-3-7-sonnet-20250219"
]

class AnthropicClient:
    def __init__(self, api_key: str, base_url: str = "https://api.proxyapi.ru/anthropic/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "AnthropicProxyClient/3.0 (Cross-Platform)"
        })

    def create_completion(
        self,
        prompt: str,
        model: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        timeout: int = 30
    ) -> Optional[str]:
        """Основной метод для выполнения запроса"""
        messages = [{"role": "user", "content": prompt}]

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": "You are a helpful assistant"
        }

        try:
            response = self.session.post(
                f"{self.base_url}/messages",
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            return self._parse_response(response.json())

        except requests.exceptions.HTTPError as e:
            self._log_http_error(e)
        except requests.exceptions.RequestException as e:
            print(f"Network error: {str(e)}", file=sys.stderr)
        except Exception as e:
            print(f"Unexpected error: {str(e)}", file=sys.stderr)

        return None

    def _parse_response(self, response: Dict) -> str:
        """Парсинг ответа API с проверкой структуры"""
        try:
            if 'content' in response and isinstance(response['content'], list):
                return response['content'][0].get('text', '')
            return response.get('choices', [{}])[0].get('message', {}).get('content', '')
        except (KeyError, IndexError) as e:
            raise ValueError(f"Invalid API response format: {str(e)}") from e

    def _log_http_error(self, e: requests.exceptions.HTTPError):
        """Логирование HTTP ошибок"""
        error_info = {
            "status": e.response.status_code,
            "url": e.response.url,
            "response": e.response.text,
            "headers": dict(e.response.headers)
        }
        print("API Error:", json.dumps(error_info, indent=2), file=sys.stderr)

def read_file(file_path: str) -> str:
    """Кроссплатформенное чтение файла с проверкой ошибок"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"File error ({file_path}): {str(e)}", file=sys.stderr)
        sys.exit(1)

def validate_temperature(value: str) -> float:
    """Валидация параметра температуры"""
    try:
        temp = float(value)
        if 0.0 <= temp <= 1.0:
            return temp
        raise ValueError
    except:
        raise argparse.ArgumentTypeError("Must be between 0.0 and 1.0")

def main():
    # Настройка парсера аргументов
    parser = argparse.ArgumentParser(
        description="CLI for Anthropic AI via ProxyAPI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    required = parser.add_argument_group('Required arguments')
    required.add_argument("--api-key", required=True, help="ProxyAPI key (sk-...)")
    required.add_argument("--model", required=True, choices=SUPPORTED_MODELS, help="AI model")

    input_group = required.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--prompt", help="Input text")
    input_group.add_argument("--file", help="Input file")

    optional = parser.add_argument_group('Optional arguments')
    optional.add_argument("--max-tokens", type=int, default=1024,
                         help="Max tokens (100-4096)")
    optional.add_argument("--temperature", type=validate_temperature,
                         default=0.7, help="Creativity level")
    optional.add_argument("--timeout", type=int, default=30,
                         help="Request timeout")

    args = parser.parse_args()

    # Получение промпта
    try:
        prompt = args.prompt if args.prompt else read_file(args.file)
    except Exception as e:
        print(f"Input error: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # Инициализация клиента
    client = AnthropicClient(api_key=args.api_key)

    # Выполнение запроса
    response = client.create_completion(
        prompt=prompt,
        model=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        timeout=args.timeout
    )

    # Вывод результата
    if response:
        print("\n" + "═" * 80)
        print("AI Response:")
        print("═" * 80)
        print(response)
        print("═" * 80 + "\n")
        sys.exit(0)
    else:
        print("No response received", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
