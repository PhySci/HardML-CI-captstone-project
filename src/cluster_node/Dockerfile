FROM qa:base

COPY app /app
WORKDIR /app

RUN pip install -r requirements.txt && \
    mkdir "/model"

ENV MODEL_PATH=/model

CMD ["python", "app.py"]