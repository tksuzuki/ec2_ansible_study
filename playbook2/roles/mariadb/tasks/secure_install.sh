#!/bin/bash

#set -xeu

[ $(/usr/bin/whoami) = 'root' ] || {
    /bin/echo root only
    exit 1
}

init_file=/tmp/mysql-init

/bin/cat <<EOF > ${init_file}
-- Set the root password
UPDATE mysql.user SET Password=PASSWORD('${mysql_root_password}') WHERE User='root';
FLUSH PRIVILEGES;
-- Remove anonymous users
DELETE FROM mysql.user WHERE User='';
-- Disallow remote root login
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost',  '127.0.0.1',  '::1');
-- Remove test database
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
-- Reload privilege tables
FLUSH PRIVILEGES;
EOF

chmod 600 ${init_file}


/bin/sh /usr/bin/mysqld_safe \
    --datadir=/var/lib/mysql \
    --socket=/var/lib/mysql/mysql.sock \
    --pid-file=/var/lib/mysql/mysqld01.pid \
    --basedir=/usr \
    --user=mysql \
    --skip-grant-tables \
    --skip-networking &

while :
do
    [ -r /var/lib/mysql/mysqld01.pid ] || continue

    if ps -ef | grep -q $(cat /var/lib/mysql/mysqld01.pid) ; then
        break
    fi
    sleep 10
done

mysql -uroot < ${init_file} -v

/bin/mysqladmin shutdown

rm -f ${init_file}

exit
