# MySQL on Host with Docker

1. install mysql on ubuntu
2. bind to the docker address. Change `/etc/mysql/mysql.conf.d/mysqld.cnf`. Bind address -> `127.0.0.1,host.docker.internal`
3. add `172.17.0.1 host.docker.internal` to `/etc/hosts`
4. `systemctl restart mysql`
5. now `host.docker.internal` can be used in django configuration as DB address
6. Enter mysql and execute `CREATE USER 'owm' IDENTIFIED WITH mysql_native_password BY 'xxx';` to create the owm user

# Configure Database `openwastemap`

1. `CREATE DATABASE openwastemap;`
2. `GRANT ALL PRIVILEGES ON openwastemap.* TO 'owm';`