## Get started
Computer with docker installed 
Install it via [Download](https://www.docker.com/):

## 1 
Build
```shell
docker-compose build
```
## 2 
Start docker
```shell
docker-compose up -d
or console debug
docker-compose up 
```
## 3 
Create Admin User for window
```shell
winpty docker-compose exec web python manage.py createsuperuser
```
Create Admin User for linux
```shell
sudo docker-compose exec web python manage.py createsuperuser
```

sync django model with db for window
```shell
winpty docker-compose exec web python manage.py migrate --run-syncdb
```

sync django model with db for linux
```shell
sudo docker-compose exec web python manage.py migrate --run-syncdb
```

django document [see more ](https://www.djangoproject.com/):


## wordpress

install custom_api plugin in your wordpress

## wp-config.php for developmet environment
```php
define( 'WP_ENVIRONMENT_TYPE', 'local' );
```

## create application password 

application password [see more ](https://www.paidmembershipspro.com/create-application-password-wordpress/):


## connect django to wordpress
fill your credentials  wordpress section in django admin
    - website name
    - url
    - username
    - password
    - api_password 