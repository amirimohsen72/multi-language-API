# multi-language-API
API for multi language app 



## Getting started
this project use pipenv .
for install pipenv :
``` 
pip install pipenv
```
for run pipenv :
``` 
pipenv shell
```

all packages list store in requirements.txt

this simple project use sqlite database for use simplest in database folder.

if you want create or use database read bellow note.
in .env file can write your setting .for example if DEBUG = True database is sqlite3 .
after connect database for migrate use:
```
python manage.py migrate
```
if use my database you can use bellow user and pass for login to admin panel.
```
nathion code : 1234567890
password : 1234
```
if you want create new db and user in first need load group data by this command :
```
python manage.py loaddata group.json
```

after load group table you can createsuperuser:
```
python manage.py createsuperuser
```
in this step you most set your nationalcode for username and set email and password.



## django apps 
we have 3 main model for django 
- [X] config (this is base application app)
- [X] support

- [ ] shop



runserver by this command
```
python manage.py runserver
```


for see swagger of web application use this address : 
```
http://127.0.0.1:8000/swagger/
```
