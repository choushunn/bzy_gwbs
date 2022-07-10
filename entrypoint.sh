#启动 supervisord
supervisord -c /etc/supervisor/supervisord.conf
#迁移数据库
python manage.py makemigrations
python manage.py migrate
#加载默认SQL文件
