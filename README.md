## Hosted

https://shishaa.pythonanywhere.com/

## Screenshots



# fashion_web

**fashion_web** is a E-commerce system written in Python 3 and using Django framework.
The application allows users add to cart products and checkout. It allows admins to add different Categories and products in the backend. 


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See installing instructions for notes on how to deploy the project on a live system.


### In development features

* Payment intergration

### Prerequisites
You will find hereafter what I use to develop and to run the project
* Python 3.7
* Django 3.1
* pipenv (not mandatory but highly recommended)

### Installing
Get a local copy of the project directory by cloning "fashion_web" from github. `git clone https://github.com/BabGee/fashion_web.git` 
I use pipenv for developing this project so I recommend you to create a virtual environment and activate it, `pipenv shell`  and to install the requirements `pip install -r requirements.txt`.

Then follow these steps:
1. Move to root folder `cd django_angular`
2. Create a `.env` file in the root folder, provide the required database information  to the `.env` file (.env.example file is provided to help set this information)
3. Create the tables with the django command line `python manage.py makemigrations` then `python manage.py migrate`
4. Create your admin log in credentials to add Products in the backend `python manage.py createsuperuser`
5. Finally, run the django server `python manage.py runserver `


## Built With

* [Python 3](https://www.python.org/downloads/) - Programming language
* [Django](https://www.djangoproject.com/) - Web framework 


## Versioning
I use exclusively Github

## License

This is an open source project not under any particular license.
However framework, packages and libraries used are on their own licenses. Be aware of this if you intend to use part of this project for your own project.




