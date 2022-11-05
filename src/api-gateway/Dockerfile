FROM qa:base

COPY app /app
WORKDIR /app
ENV EMB_SERVING_PORT=8000

RUN pip install -r requirements.txt

CMD ["python", "app.py"]