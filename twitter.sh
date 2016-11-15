cd
cd twitter-framework
source twitter-env/bin/activate
cd src/servicio/web-grafica/
google-chrome 127.0.0.1:8000/srvtwitter &
mongod --repair
mongod &
python manage.py runserver
