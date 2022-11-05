FROM emb_serving:base

WORKDIR /app
COPY app /app
RUN chmod +x init_use.py && \
    python init_use.py

CMD ["python", "app.py"]

