FROM python:3.10.6-alpine
WORKDIR /app
COPY . .
RUN pip install "poetry==1.5.1"
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
ENV PYTHONPATH "${PYTHONPATH}:/"
RUN chmod +x start.sh
ENTRYPOINT ["./start.sh"]
CMD ["python", "main.py"]