FROM python:alpine
ENV PYTHONUNBUFFERED 1

RUN apk add --update nodejs-npm
RUN pip install gunicorn

RUN mkdir /code
RUN mkdir /workdir
ENV PORFAVOR_WORKDIR /workdir
WORKDIR /code

ADD package.json /code/
RUN npm install

ADD . /code
RUN npm run build

RUN rm -rf node_modules/
RUN pip install .

ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:8000", "porfavor.server.main:app"]
EXPOSE 8000
