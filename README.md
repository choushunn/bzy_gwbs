## 1.构建镜像

##### 1.1 依赖文件

> - Dockerfile
> - docker-compose.yml

##### 1.2 生成镜像文件并启动

```shell
docker-compose up --build
```

## 2. 初始配置

##### 2.1 生成数据库表结构

```shell
python manage.py migrate
```

##### 2.2 创建超级管理员

```shell
python namage.py createsuperuser
```

## 3. 启动运行

```shell
# 后台运行
docker-compose up -d

# 前台地址
# 默认暴露 9000 端口 
http://localhost:9000

# 后台地址
http://localhost:9000/admin/
```

## 4. 注意事项

- 测试数据库使用SQLite
- 正式数据库可使用MySQL, PostgreSQL
- 需要生成数据库表结构