FROM python:3.8.2-alpine3.11

ENV FLASK_APP=flaskr
ENV FLASK_ENV=development

COPY . /app

WORKDIR /app

RUN pip install --editable .

RUN pip install flask-talisman

RUN pip install flask-marshmallow

RUN pip install flask-wtf

RUN flask init-db

ENV FLASK_ENV=testing

ENV TESTING=True

RUN pip install pytest

RUN pytest

ENV TESTING=False

ENV FLASK_ENV=development

EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0" "--cert", "adhoc"]