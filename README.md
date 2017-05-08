# Tutor LAB

We want to determine the effectiveness of our tutors and TAs (Teacher Assistants) in the Computer Science department at The University of Texas at San Antonio and analyze whether we need more or less, should promote or demote, or should certain classes even need a TA. The software will have three distinct interfaces: Professor, Student, and TA/Tutor. Each one will have its own set of tools and techniques for helping us collect information on our TA/Tutor program as well as allow one another to communicate about issues or comments on the program. You will be able to set up appointments with your tutors and TA, chat with them when you are off campus, and collabrate with other students via a student forum.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install for the software to run and how to install them.
The site is run using a python framework called [Django](https://www.djangoproject.com). 
Everything needed for this project is in the requirements.txt which can be installed by running the command 

```
pip install -U -r requirements.txt
```

### Running The Site

This will tell you how to get the site started as well as other impportant scripts to rum.

```
python manage.py runserver
```

### Database Updates

After making changes to any models.py, you must make migrations.

```
python manage.py makemigrations
```

This makes a python file telling the database what to update. Once this file is made we can migrate them to the database

```
python manage.py migrate
```

If any errors occur follow the instructions given by the error codes.

## Built With

* [Channels](https://channels.readthedocs.io/en/stable/) - A Django framework used for websockets
* [Django](https://www.djangoproject.com) - Python web framework
* [Django-Datetime-Widget](https://github.com/asaglimbeni/django-datetime-widget) - A add-on that makes using bootstrap datetime picker simpler
* [Django-Nested-Admin](https://github.com/theatlantic/django-nested-admin) - Add-on to Django admin
* [Django-Password-Reset](https://github.com/brutasse/django-password-reset) - Package made for Django for ease of use with password reset
* [MySQLclient](https://github.com/PyMySQL/mysqlclient-python) - A python client to interact with a MySQL Database
* [Pillow](https://github.com/python-pillow/Pillow) - Used by python and Django for images
* [Pusher](https://pusher.com/docs) - A live notification framework for websites
* [Service_Identity](https://github.com/pyca/service_identity) -  A tool for verifying whether a certificate is valid for the intended purposes

## Idea For Project
* **Larry Clark** - Professor at The University of Texas at San Antonio

## Code Authors

* [**Koby Huckabee**](https://github.com/AceTugboat) - Project Leader / Developer
* [**Joseph Martinez**](https://github.com/jsmart93) - Architect Liaison/ Developer / UX Designer

See also the list of [contributors](https://github.com/AceTugboat/TutorLab/graphs/contributors) who participated in this project.

## ChangeLog:

### **v 1.0**

*Website major updtes*
+ Admin can now upload all students, instructors, and courses through .xls spreadsheet
+ Admin can purge the database of past semester students, and courses
+ Admin can modify instructor statis as Tutor Admin
+ Tutor Admin can create/delete tutors
+ Tutor Admin can print out report of surveys by semester and tutor
+ Instructors can make custom issue sets per class for desktop app
+ see more in documents...

*Desktop major updates*
+ Pulls students enrolled classes based on admin import
+ Pulls custom issue set for class if created by instructor
+ Live updates via websockets
+ Gets and Sends survey information to site
+ see more in documents...

### **v 0.9**

*Website*
+ Updated APIs to work directly with the desktop application

*Desktop application*
+ Redesigned in python PyQt4 [Documentation](http://doc.qt.io/qt-4.8/index.html)
+ Works directly with the site APIs
+ Uses websockets to allow the site to communicate directly with the application

### **v 0.8**
+ All Calendar functions work
+ Added forum with most functionality

### **v 0.7**

*Website*
+ Student can make chat request
+ Tutor can accept chat request
+ Starts chat session
+ Student can make appointment request
+ Tutor receives appointment request
+ Tutor view renders FullCalendar
+ Updated tutor UI
+ Live notifications for appointments
+ Student register now checks if username is already used before creating account and logging student in

*Desktop application*
+ Sends information to database
+ Updated UI

### **v 0.6** 

*Website*
+ New logo
+ A student login
+ Register student form
+ Side navigation bar to student page
+ Student appointment request form
+ Calendar alternative “fullcalendar”
+ Migrated database to MySQL from SQLite 
+ ~~footer information~~
+ ~~Page background color~~

*Desktop application*
+ Grabs student abc123
+ Grabs computer number
+ Asks for class

*Web Services*
+ addQueue API
+ registered API

### **v 0.5**

Initial push and pick up from previous summer project
