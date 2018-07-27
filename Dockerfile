FROM python:alpine
ENV PYTHONUNBUFFERED 1

RUN apk add --update nodejs-npm
RUN pip install gunicorn

RUN mkdir /code
WORKDIR /code

ADD package.json /code/
RUN npm install

ADD . /code
RUN npm run build

RUN rm -rf node_modules/
RUN pip install .
