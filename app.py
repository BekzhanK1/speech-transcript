import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# .env рядом с app.py (не зависит от cwd, откуда вызвали streamlit run)
load_dotenv(Path(__file__).resolve().parent / ".env")

st.set_page_config(page_title="Whisper Transcriber", page_icon="🎙️")

st.title("🎙️ Whisper MP3 в Текст")

if "batch" not in st.session_state:
    st.session_state.batch = None

# Боковая панель для настроек
with st.sidebar:
    env_api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        autocomplete="off",
    )
    api_key = (api_key_input or "").strip() or env_api_key
    model = st.selectbox("Модель", ["whisper-1"])
    language = st.text_input("Язык (например, 'ru' или 'en')", value="ru")

uploaded_files = st.file_uploader(
    "Выберите один или несколько аудиофайлов",
    type=["mp3", "wav", "m4a", "mp4"],
    accept_multiple_files=True,
)


def transcribe_one(client: OpenAI, uploaded, model: str, language: str) -> str:
    file_bytes = uploaded.getvalue()
    file_ext = uploaded.name.rsplit(".", 1)[-1].lower() if "." in uploaded.name else ""
    if not file_ext:
        file_ext = "mp4"
    mime_type = uploaded.type or "application/octet-stream"
    clean_file = (f"audio.{file_ext}", file_bytes, mime_type)
    result = client.audio.transcriptions.create(
        model=model,
        file=clean_file,
        language=language,
        response_format="text",
    )
    if isinstance(result, str):
        return result
    return getattr(result, "text", str(result))


if uploaded_files and api_key:
    if st.button("Начать транскрибацию"):
        client = OpenAI(api_key=api_key)
        ok: list[dict[str, str]] = []
        errors: list[tuple[str, str]] = []

        for i, uploaded_file in enumerate(uploaded_files):
            name = uploaded_file.name
            with st.spinner(f"Файл {i + 1}/{len(uploaded_files)}: {name}…"):
                try:
                    text = transcribe_one(client, uploaded_file, model, language)
                    ok.append({"name": name, "text": text})
                except Exception as e:
                    errors.append((name, str(e)))

        st.session_state.batch = {"ok": ok, "errors": errors}

    batch = st.session_state.batch
    if batch:
        for name, err in batch["errors"]:
            st.error(f"{name}: {err}")

        for i, item in enumerate(batch["ok"]):
            name = item["name"]
            text = item["text"]
            st.subheader(f"📄 {name}")
            st.text_area(
                "Транскрипт",
                value=text,
                height=320,
                key=f"tr_{i}",
            )
            base = os.path.splitext(name)[0] or "transcript"
            st.download_button(
                f"Скачать {name}.txt",
                text,
                file_name=f"{base}.txt",
                key=f"dl_{i}",
            )

        if batch["ok"]:
            st.success("Готово: ниже каждый файл и его транскрипт.")
            combined = "\n".join(
                f"=== {x['name']} ===\n{x['text']}\n" for x in batch["ok"]
            )
            st.download_button(
                "Скачать все транскрипты одним .txt",
                combined,
                file_name="all_transcripts.txt",
                key="dl_all",
            )

elif not api_key:
    st.info("Пожалуйста, введите ваш API ключ в боковом меню.")
elif not uploaded_files:
    st.info("Загрузите один или несколько файлов.")
