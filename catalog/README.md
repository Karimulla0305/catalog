## Item Catalog Tablet Store Web App.

By Shaik Karimulla
This web app is a project for the Udacity Full stack Nano Degree.


## About

This project is mainly aimed to provide knowledge on the authorisation and authentication of a project.
It is a Web Application which provides a list of items within many categories as well as provide a user registration and authentication system. The Registered users will have the ability to post, update and delete their own items.


## In This Project

This Project contains Data_Setup python file in which the database as well as the tables and columns are created.
The db_init python file is used to enter the data into the columns of the table in the database.
The project python file gives the internal configuration of the project such as adding, updating and deleting of categories as well as items in the categories.


## Features

1. Checking the Proper authentication and authorisation.
2. Full CRUD support using Flask and SQLAlchemy.
3. Using the JSON endpoints.
4. Implements oAuth using with Google Sign-in API.


## Skills & Tools Required

1. Python
2. HTML
3. CSS
4. OAuth2client
5. Flask Framework
6. DataBaseModels
7. Vagrant
8. VirtualBox


## Tips to Run Project

1. Set up a Google Plus auth application.
2. go to google and login with Google.
3. Create a new project
4. Select "API's and Auth-> Credentials-> Create a new OAuth client ID" from the project menu
5. Select Web Application
6. follow the tips given by google


## How to Run

1. In First Step we have to Install Vagrant.
2. Now We have to Install VirtualBox.
3. Then Open CommandPrompt in your Folder's Path.
4. First initialize the Vagrant using the command:
	$ vagrant init ubunti/xenial64
5. Launch Vagrant Using the Command
	$ vagrant up
6. Log into Vagrant using Command
	$ vagrant ssh
7. Change the directory to vagrant using command
	$ cd vagrant
8. The app imports requests which is not on this vm. Run pip install requests
9. Now we have to activate the Virtual Environment in our Folder by Using the Command
	$ venv\scripts\activate
10. Run the Data_Setup.py using the command
	$ python Data_Setup.py
	 Execution of this file leads to creation of a database file(tablets.db) 
11. Run the db_init.py using the command
	$ python db_init.py
	Execution of this file leads to insertion of data into the database file
12. And then Run the project.py using the command 
	$ python project.py
	This File Executes the entire Project including Templates and remaining files
13. Access the application locally using http://localhost:8000	
	By running running project.py file in command prompt the server of our project will activates and we have to type the above url in browser.This displays basic version of our project.
14. Here we cannot be able to edit,add,delete our items.To enable edit,add,delete options we have to login to our 
	account.

	
## Using Google Login
   To Work in our Project we need to follow these steps:

1. Go to [Google Developers Console]
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'Tablet Store'
7. Authorized JavaScript origins = 'http://localhost:8000'
8. Authorized redirect URIs = 'http://localhost:8000/login' && 'http://localhost:8000/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Finally Run The Project using the steps mentioned in How to Run.
14. Now you can add,update and delete the Items in our Project.


### JSON Codes

The following are open to the public:

1.Tablet Catalog JSON: `/tabletStore/JSON`
    - Displays the whole tablets catalog.

2.Tablet Categories JSON: `/tabletStore/tabletCategories/JSON`
    - Displays all Tablets categories
	
3.All Tablets: `/tabletStore/tablets/JSON`
	- Displays all Tablets

4.Tablet Names JSON: `/tabletStore/<path:tablet_name>/tablets/JSON`
    - Displays all Tablet details of a specific Tablet Company

5.Tablet Category Names JSON: `/tabletStore/<path:tabname>/<path:medtablet_name>/JSON`
    - Displays a specific Tablet details of a specific Tablet Category.
