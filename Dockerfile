FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=9632 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 9632

CMD ["streamlit", "run", "app.py", "--server.port=9632", "--server.address=0.0.0.0"]
