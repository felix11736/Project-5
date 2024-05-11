FROM python:3.7

COPY requirements.txt /requirements.txt

COPY ./app /app

WORKDIR /

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["app/main.py", "--reload"]