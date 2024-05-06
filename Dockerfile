FROM python:3.9
MAINTAINER Mikhail Ragulin 'mikhail.ragulin@gmail.com'
COPY . /app
WORKDIR /app
RUN pip3 install --upgrade pip -r requirements.txt
RUN pip3 install --no-binary pyuwsgi pyuwsgi
EXPOSE 5000
ENTRYPOINT ["uwsgi"]
CMD ["--http", "0.0.0.0:5000", "--master", "--callable", "app", "--process", "4", "--threads", "2", "--wsgi-file", "app.py"]



