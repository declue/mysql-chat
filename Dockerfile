FROM ubuntu:20.04

ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive
ENV DATABASE_ROOT_PASSWORD=testpassword
ENV DATABASE_NAME=chat

RUN apt update
RUN apt install -y sudo vim python3 python3-pip
RUN apt install -y mysql-server mysql-client pkg-config default-libmysqlclient-dev

COPY install_mysql.sh /root/
COPY app.py /root/
COPY index.html /root/
COPY requirements.txt /root/
COPY entry.sh /root/

WORKDIR /root

RUN pip install -r requirements.txt

RUN ./install_mysql.sh $DATABASE_ROOT_PASSWORD $DATABASE_NAME
RUN chmod +x /root/entry.sh

ENTRYPOINT /root/entry.sh
