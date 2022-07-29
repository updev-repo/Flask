# Flask



# Setting up

## Initialize a virtualenv

```
$ pip install virtualenv
$ virtualenv -p /path/to/python3.x/installation env
$ source env/bin/activate
```

For mac users it will most likely be
```
$ pip install virtualenv
$ virtualenv -p python3 env
$ source env/bin/activate
```
Note: if you are using a python2.x version, point the -p value towards your python2.x path

## (If you're on a mac) Make sure xcode tools are installed

```
$ xcode-select --install
```

## Add Environment Variables

Create a file called `config.env` that contains environment variables in the following syntax: `ENVIRONMENT_VARIABLE=value`.
You may also wrap values in double quotes like `ENVIRONMENT_VARIABLE="value with spaces"`.
For example, the mailing environment variables can be set as the following.
We recommend using Sendgrid for a mailing SMTP server, but anything else will work as well.
```
MAIL_USERNAME=example@domain.com
MAIL_PASSWORD=SuperSecretPassword
SECRET_KEY=SuperRandomStringToBeUsedForEncryption
```

Other Key value pairs:

* `ADMIN_EMAIL`: set to the default email for your first admin account (default is `updev@gmail.com`)
* `ADMIN_PASSWORD`: set to the default password for your first admin account (default is `password`)
* `DATABASE_URL`: set to a postgresql database url (default is `data-dev.sqlite`)
* `REDISTOGO_URL`: set to Redis To Go URL or any redis server url (default is `http://localhost:6379`)
* `RAYGUN_APIKEY`: api key for raygun (default is `None`)
* `DEV_DATABASE_URL`: set to a postgresql database url
* `MAIL_SENDER`: this parameter will appear as the default mail sender
* `MAILGUN_DOMAIN`: this parameter comes from mailgun
* `MAILGUN_USERNAME`: this parameter comes from username
for other keys see, append to env file

* `FLASK_CONFIG`: can be `development`, `production`, `default`, `heroku`, `unix`, or `testing`. Most of the time you will use `development` or `production`.

**Note: do not include the `.env` file in any commits. This should remain private.**

## Install the dependencies

```
$ pip install -r requirements.txt
```

## Other dependencies for running locally

You need [Redis](http://redis.io/), and [Sass](http://sass-lang.com/). Chances are, these commands will work:


**Sass:**

```
$ gem install sass
```

**Redis:**

_Mac (using [homebrew](http://brew.sh/)):_

```
$ brew install redis
```

_Linux:_

```
$ sudo apt-get install redis-server
```

You will also need to install **PostgresQL**

_Mac (using homebrew):_

```
brew install postgresql
```

_Linux (based on this [issue](https://github.com/hack4impact/flask-base/issues/96)):_

```
sudo apt-get install libpq-dev
```

## Create the database

```
$ python manage.py recreate_db
```

## Other setup (e.g. creating roles in database)

```
$ python manage.py setup_dev
```

Note that this will create an admin user with email and password specified by the `ADMIN_EMAIL` and `ADMIN_PASSWORD` config variables. If not specified, they are both `findnex328@gmail.com` and `password` respectively.

```

## Running the app

```
$ source env/bin/activate
$ honcho start -f Local
```


## Known issues for linux and windows users

1. flask script:  If you get and error, that tells you no module named flask._compat or related. Open your
environment folder e,g

for windows and linux users
venv/lib/sites-packages/flask_scripts

locate the flask_script init file ( __init__.py) and change the line that imports 
from flask._compat import ... (possibly line 3)
 to from  ._compat import ...


2. flask upload:  If you get and error, that tells you no module named secure filename or related. Open your
environment folder e,g

for windows and linux users
venv/lib/sites-packages/flask_uploads.py

locate the flask_uploads.py file and change the line that imports 
from werkzeug import secure_filename, Filestorage 
 to from  werkzeug.utils import secure_filename
and from werkzeug.datastructures import Filestorage




## This issue may not show up but if it does here is the fix
3. flask wtf:  If you get and error, that tells you no module named url_encode or related. Open your
environment folder e,g

for windows and linux users
venv/lib/sites-packages/flask_wtf

note you will search this entire project(flask_wtf folder) , wherever you find an import exactly like this

from werkzeug import url_encode

change it to 

from werkzeug.urls import url_encode



## Finally, the mail feature will not work if you dont provide the mailgun domain , username and api key on the .env file. The one used to test this project is a product of a company and hence cannot be placed here as it posses a security risk, see mailgun's documentation on how to create yours.

## AWS DEPLOYMENT
Currently this app is already running on an ec2 instance, see AWS ec2 image snapshot documentation on how to take a snapshot of the current project and redeploy.

# Requirements for production use
1. Web server(nginx, apache2, tomcat etc):   An nginx configuration will be included by default, it currently serves the app but not suitable for production use case. see docs for more use on how to deploy nginx(load balancer) and gunicorn flask 

2. Letsencrypt or openssl: letsencrypt for creating ssl (server secure layer) certificates for protection.

commands are 
sudo apt-get install python3-certbot ( see docs for better clarification)
sudo certbot --nginx -d example.com, to generate a certificate for an existing domain
sudo certbot --renew to renew certifcates

# note if apache is used, the command changes to sudo certbot --apache -d example.com
and if you permit it to make changes and redirects on the server config found at
/etc/nginx/sites-available/plotty.conf

all request will be routed to https automatically for you.


3. Redis : currently redis is not supported on windows, but it allows the use of asynchronous programming by creating task queues etc. Currently email sending is done synchronously, but production use case has been taken care of. The project comes with a flask rabbit queue which acts as a worker for redis to execute each task on a different thread hence providing asynchronous use case. All you need is to call the qet_queue().enqueue() function on any task you which to make asynchronous

Example

for emails
redis_q.enqueue(
    send_email, templates="a template", recipients = "something here", body={
        'a dictionary here'
    }
)
The first parameter it takes is the funcion, then followed by the function parameters, you will need to do this on all instance by which the send_email is called to enable this functionality.

then run python manage.py run_worker to execute task available on the queue.

## Upon first deployment, the app will contain this by default. further deployment will not need to do this.

4. Database/Pooler: Currently in development an sqlite3 database is used as a default, but postgresql database and other databases can be used by specifying the DATABASE_URL parameter for production and DEV_DATABASE_URL for development. The database you decide to use may vary on it configuration, do well to visit it docs for details on how to install drivers etc. The sqlite3 database is  development use only database.

recommended option are

1. Postgresql with pooler for handling connectons e.g(pgpool2, pgbouncer see docs on either)
2. MySQL ( driver needed, mysql-client)
3. MariaDB
4. Microsoft Azure
5. MongoDB
6. Firebase
etc all this except postgresql will need extra changes to the project..


# HAPPY CODING / HACKING  !!!!!!


