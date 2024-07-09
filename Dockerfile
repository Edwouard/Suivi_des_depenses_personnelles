FROM python:3.9-alpine3.15

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app .

EXPOSE 5000

ENTRYPOINT ["python3", "app.py"]
