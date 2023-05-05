#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
$HOME/.profile;
cd /root/microservices/sheetToTable 
git pull
export FLASK_DEBUG=0

ps -ef | grep flask | grep 0.0.0 | awk -F " " '{print $2}' | xargs kill -9
echo 'reinicie server'
 nohup flask run --host=0.0.0.0 --debugger --port 80 --cert=/etc/ssl/certs/conexion.crt --key=/etc/ssl/private/conexion.key  &

