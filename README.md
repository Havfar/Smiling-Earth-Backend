# Smiling-Earth-Backend
Smiling Earth is the backend application running the Django Rest API. For the frontend applicaiton see  **[Smiling Earth Frontend](https://github.com/Havfar/Smiling-Earth)**.

# Getting Started - Local setup
It's recommended to have a look at the Django REST guide: https://www.django-rest-framework.org/

1. Create a virtualenv https://docs.python-guide.org/dev/virtualenvs/
2. Clone the repo by running: 
`git clone https://github.com/Havfar/Smiling-Earth-Backend.git`
3. Setup and activation of virtualenv (env that prevents python packages from being installed globaly on the machine)
4. Naviagate into the project folder, and create your own virtual environment



### Install python requirements

5. `cd Smiling-Earth-Backend`
6. `pip install -r requirements.txt`

### Setup up local environment
7. Create a new file in root called .env
8. Add 'DATABASE_URL=sqlite:///db.sqlite3' to the file
9. Migrate database by running: `python manage.py migrate`

### Create superuser
10. Create a local admin user by entering the following command: `python manage.py createsuperuser`

### Start the app

11. Run `python manage.py runserver`

