FROM python:3.9
RUN mkdir /wwwroot  && mkdir -p /etc/supervisor/conf.d
WORKDIR /wwwroot

COPY . .
# supervisor
COPY ./config/supervisor/uwsgi_gwbs.conf /etc/supervisor/conf.d/uwsgi_gwbs.conf

#安装 requirements
RUN pip config set global.index-url https://pypi.douban.com/simple \
    && /usr/local/bin/python -m pip install --upgrade pip \
    && pip install -r ./requirements/production.txt --no-cache-dir\
    && echo_supervisord_conf > /etc/supervisor/supervisord.conf \
    &&  sed -i 's/nodaemon=false/nodaemon=true/g' /etc/supervisor/supervisord.conf \
    && sed -i '$a[include]' /etc/supervisor/supervisord.conf \
    && sed -i '$afiles=/etc/supervisor/conf.d/*.conf' /etc/supervisor/supervisord.conf \
    && sed -i 's/deb.debian.org/mirrors.bfsu.edu.cn/g' /etc/apt/sources.list


# 安装Nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/* && apt-get clean && apt-get autoremove

COPY ./config/nginx/nginx.conf /etc/nginx/nginx.conf

#暴露端口
EXPOSE 80

#启动
#ENTRYPOINT ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
ENTRYPOINT ["sh","./entrypoint.sh"]