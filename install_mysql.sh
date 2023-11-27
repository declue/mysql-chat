#!/bin/bash


if [ "$#" -ne 2 ]; then
    echo "usage: $0 [Root Password] [Database Name]"
    exit 1
fi

ROOT_PASSWORD=$1
DATABASE_NAME=$2

sudo apt update
sudo apt install -y mysql-server mysql-client pkg-config default-libmysqlclient-dev

sudo /etc/init.d/mysql start

sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$ROOT_PASSWORD'; FLUSH PRIVILEGES;"

sudo mysql -u root -p$ROOT_PASSWORD -e "CREATE DATABASE $DATABASE_NAME;"



