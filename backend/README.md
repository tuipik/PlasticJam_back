Backend.

Steps to install on debian / Ubuntu:
should be installed MySQL and Docker.

- Copy or clone project.

- Install python3 environment

- Install mysqlclient:
    
    sudo apt-get install libssl-dev
    sudo apt-get install python3-dev
    pip install mysqlclient 

- Make database on Docker:

sudo docker run --name tzproject2 -v ~/tz_volume:/var/lib/mysql \
-p 3307:3306 -e MYSQL_USER=a -e MYSQL_PASSWORD=a -e MYSQL_ROOT_PASSWORD=a \
-e MYSQL_DATABASE=a mysql:latest

- Migrate to db:

./manage.py migrate

- fill up the db:

./manage.py fill_up_db

- start the server:

./manage.py runserver

- Get the API:

users list - http://127.0.0.1:8000/api/users/

user detail - http://127.0.0.1:8000/api/users/5/

user statistics - http://127.0.0.1:8000/api/stats/5/

Cause the data in db is for only october 2019, the previos url returns empty list,
and the api in standart shows the data for last 7 days, 
to see the data use next url:

http://127.0.0.1:8000/api/stats/5/?since=2019-10-01&until=2019-10-31

