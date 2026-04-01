# Whisper Transcriber

Минимальное веб-приложение на [Streamlit](https://streamlit.io): загрузка одного или нескольких аудиофайлов и последовательная транскрипция через [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text) (`whisper-1`).

## Возможности

- Форматы: MP3, WAV, M4A, MP4
- Несколько файлов за раз, обработка по очереди
- Для каждого файла: имя и текст; скачивание отдельного `.txt` или одного файла со всеми транскриптами
- Ключ API из переменной окружения или вводом в интерфейсе

## Требования

- Python 3.12+
- Аккаунт OpenAI и [API key](https://platform.openai.com/api-keys)

## Локальный запуск

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Создайте `.env` в корне проекта (опционально):

```env
OPENAI_API_KEY=sk-...
```

Запуск на порту **9632**:

```bash
make run
```

Откройте в браузере: <http://localhost:9632>.

## Docker

Сборка и запуск:

```bash
make docker-build
export OPENAI_API_KEY=sk-...
make docker-run
```

Или в одну команду:

```bash
docker run --rm -p 9632:9632 -e OPENAI_API_KEY="sk-..." transcript-whisper
```

Приложение слушает порт **9632** внутри контейнера; с хоста тот же порт: `http://localhost:9632`.

## Стек

- Streamlit, OpenAI Python SDK, python-dotenv

## Лицензия

Используйте и изменяйте по своему усмотрению для личных или рабочих задач.
