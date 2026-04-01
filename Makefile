run:
	.venv/bin/python -m streamlit run app.py --server.port 9632

docker-build:
	docker build -t transcript-whisper .

docker-run:
	docker run --rm -p 9632:9632 transcript-whisper