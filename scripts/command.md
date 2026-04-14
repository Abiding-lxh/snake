
sudo /etc/init.d/nginx start	//启动nginx
sudo nginx -s reload

sudo redis-server /etc/redis/redis.conf	//启动redis进程

uwsgi --ini scripts/uwsgi.ini	//启动uwsgi
daphne -b 0.0.0.0 -p 5016 snake.asgi:application	//启动daphne