# flask

## Description
this is a simple flask application that incorporates user login and authentication

this application has a userlist page which authenticated users can use to see all usernames on the database

this application has a rest api to get the list of users


## preview
file:///home/david/Pictures/Screenshots/Screenshot%20from%202022-08-20%2009-37-18.png![image](https://user-images.githubusercontent.com/111660735/185769603-f721bdce-2152-4a90-9666-94acf6212bf2.png)
file:///home/david/Pictures/Screenshots/Screenshot%20from%202022-08-20%2009-37-27.png![image](https://user-images.githubusercontent.com/111660735/185769618-18be5d8a-daea-4f84-b27d-cb0cddd72b5d.png)
file:///home/david/Pictures/Screenshots/Screenshot%20from%202022-08-20%2009-37-48.png![image](https://user-images.githubusercontent.com/111660735/185769622-769ea315-53e5-488a-808e-fb98958f7860.png)
file:///home/david/Pictures/Screenshots/Screenshot%20from%202022-08-20%2009-41-59.png![image](https://user-images.githubusercontent.com/111660735/185769627-4729fb93-956f-4ab1-9677-4244b9f72351.png)
file:///home/david/Pictures/Screenshots/Screenshot%20from%202022-08-20%2010-01-51.png![image](https://user-images.githubusercontent.com/111660735/185769666-4fad65dd-4c63-431f-a16a-a316acd9311c.png)



# Setting the application
this application requires a database to run. the database required is mysql.

in the app config settings in apps.py, set the SQLALCHEMY_DATABASE_URI to match the user, password and host of the mysql serer to be used.

the name of the database should remain flask

## setting up database
open create_db.py and set the host, user and passord to the setting of the mysql server to be used.
the name of the database should remain flask.


## Running the application

1  Change directory to the backend folder cd backend

2  Create virtualenv virtualenv -p python3 env

3  Activate virtualenv source bundle_env/bin/activate

4  Install required python modules pip install -r requirements.txt

5  Only during the initial launch create database schema for your application python create_db.py. this would create the flask database

6  Run the application python app.py

That's it! Now your application is running at port 5000 and you can access it by typing http://localhost:5000/ in your browser.
