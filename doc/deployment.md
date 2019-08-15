# Ubuntu 18.04 LTS

## package update
```
# apt-get update && apt-get dist-upgrade
# apt-get autoclean
# apt-get autoremove
```

## locale
```
# locale-gen --purge en_US.UTF-8 ko_KR.UTF-8 th_TH.UTF-8
# update-locale LANG=en_US.UTF-8
# apt-get install gettext
```

## timezone
```
# timedatectl set-timezone Asia/Bangkok
# timedatectl set-ntp 1
```

## hostname
```
# hostnamectl set-hostname windmill
# reboot
```

## users and groups
```
# groupadd devops
# useradd -g devops -G sudo,devops -b /home -m -s /bin/bash dev
# passwd dev
# useradd -g devops -b /home -m -s /bin/bash was
# dpkg-statoverride --update --add root sudo 4750 /bin/su
# dpkg-statoverride --update --add root sudo 4750 /usr/bin/sudo
# passwd -d -l root
# usermod -s /bin/false root
```

## vim
```
$ sudo update-alternatives --config editor
```

```
$ cat > ~/.vimrc
set nocompatible
set ruler
set wrap
set number

set tabstop=8
set softtabstop=4
set shiftwidth=4
set expandtab
set autoindent
set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class
set nocindent

set nobackup
set visualbell
set hlsearch
set background=dark
set termencoding=utf-8
set encoding=utf-8
set fileencoding=utf-8
set fileencodings=ucs-bom,utf-8,euc-kr,latin1

filetype indent plugin on
```

## ssh
`/etc/ssh/sshd_config`

```
Port 22111
AddressFamily inet
PermitRootLogin no
StrictModes yes
AllowGroups devops
```

```
$ sudo service ssh restart
```

# Python

## PyEnv

```
$ sudo su - was
$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
$ cp ~/.profile ~/.bash_profile
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
$ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
$ source ~/.bash_profile
$ pyenv install --list
```

## Build Python

```
$ sudo apt-get install build-essential zlib1g-dev libffi-dev libbz2-dev libreadline-dev libssl-dev libsqlite3-dev
$ sudo su - was
$ pyenv install 3.7.4
```

## VirtualEnv

```
$ git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
$ echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
$ pyenv virtualenv -p python3.7 3.7.4 django
$ pip install --upgrade pip
```

# Web
## Maria DB

```
$ sudo apt-get install mariadb-server libmysqlclient-dev
$ sudo mysql
> CREATE DATABASE windmill DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
> CREATE USER windmill@localhost IDENTIFIED BY 'pass';
> GRANT ALL PRIVILEGES ON windmill.* TO windmill@localhost;
> FLUSH PRIVILEGES;
```

## Django

```
$ sudo apt-get install nginx
$ sudo mkdir -p /var/www/windmill
$ sudo chown was /var/www/windmill/
```

```
$ sudo su - was
$ cd /var/www/windmill
$ git clone git@github.com:pincoin/windmill.git repo
$ mkdir run ssl logs repo/media
$ exit
```

```
$ sudo chown was:www-data /var/www/windmill/run/
```

```
$ sudo su - was
$ cd /var/www/windmill/
$ pyenv shell django
$ pip install -r repo/requirements.txt
$ pip install mysqlclient gunicorn
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py collectstatic
```

test

```
$ python manage.py runserver
$ gunicorn --bind 0.0.0.0:8000 conf.wsgi:application
```


## NGINX

### /etc/nginx/sites-available/default

```
server {
    listen 80 default_server;
    server_name _;
    return 444;
}
```

### /etc/nginx/sites-available/com.windmill.www-ssl

```
upstream app_server {
    server unix:/var/www/windmill/run/gunicorn.sock;
}

server {
    listen 443 ssl;
    server_name www.windmill.com;
    charset utf-8;
    client_max_body_size 16M;

    ssl on;
    ssl_certificate /var/www/windmill/ssl/windmill_com.pem;
    ssl_certificate_key /var/www/windmill/ssl/windmill_com.key;

    root /var/www/windmill/repo;

    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    location /assets/ {
        access_log off;
        log_not_found off;
    }

    location /media/ {
        access_log off;
        log_not_found off;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://app_server;
    }

    access_log /var/www/windmill/logs/access.log;
    error_log /var/www/windmill/logs/error.log;
}
```

```
$ sudo ln -s /etc/nginx/sites-available/com.windmill.www /etc/nginx/sites-enabled/
$ sudo nginx -t
$ sudo service nginx restart
```

### Gunicorn

/etc/systemd/system/gunicorn.service

```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=was
Group=www-data
WorkingDirectory=/var/www/windmill/repo
ExecStart=/home/was/.pyenv/versions/django/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/windmill/run/gunicorn.sock \
    --env DJANGO_SETTINGS_MODULE=conf.settings \
    --log-level info \
    --access-logfile /var/www/windmill/logs/gunicorn-access.log \
    --error-logfile /var/www/windmill/logs/gunicorn-errors.log \
    conf.wsgi:application

[Install]
WantedBy=multi-user.target
```

```
$ sudo systemctl enable gunicorn
$ sudo systemctl start gunicorn
$ sudo systemctl status gunicorn
```

### Redis

### Memcached

### RabbitMQ
