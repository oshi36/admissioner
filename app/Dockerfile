FROM python:alpine3.14

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["main.py"]