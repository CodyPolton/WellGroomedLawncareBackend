### Install and Run the Backend Mac

```bash
#Go to front end directory
cd backend

#install backend dependences
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

#go into django framework folder
cd backend-framework

#Start django dev server
django manage.py runserver

```

### Install and Run the Backend Windows

```bash
#Go to front end directory
cd backend

#install backend dependences
python -m venv venv
cd venv
cd Scripts
activate
cd ../..
pip install -r requirements.txt

#go into django framework folder
cd backend-framework
cd vueapi

#Start django dev server
python manage.py runserver

```