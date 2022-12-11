![Briefing RSS Dashboard](https://raw.githubusercontent.com/jared252016/Briefing/master/image.png)

# Briefing
An iGoogle alternative that supports caching of RSS feeds with hourly updates.

Briefing uses Docker and Docker-Compose as the primary method of installation. If you want to install it locally (not recommended) you can read the Dockerfile to figure out what needs to be installed.

# Instructions

## Obtaining A Copy

### Docker Hub
I do not have a copy in the Docker Hub yet, so you will need to build it locally. When version 1.0 is released I will upload it to Docker so that it is easier to install.

### Git Pull
First create a directory to pull the project into. I will be using "briefing". I recommend putting this somewhere else besides the home directory, like in /srv, but it's up to you. After you create the directory, execute the pull on this repository.
```
mkdir ~/briefing/
git pull https://github.com/jared252016/Briefing.git
```

## Prerequisites 

### Docker
This project requires that you use Docker and should work on any linux distribution (or Windows via Subsystem)

To install Docker on Debian/Ubuntu, run the following:
```
sudo apt install docker.io
```

### Docker-Compose
You will also need docker-compose. Docker compose is a tool that allows you to script the deployment of Docker containers. To install it, run:

```
sudo apt install docker-compose
```

## Database Connection

### Docker Compose
The first step is to modify the password and root password in the docker-compose.yml file. The root password doesn't really matter since the user should have full permissions.
```
environment:
      - MYSQL_DATABASE=briefing
      - MYSQL_USER=b_user
      - MYSQL_PASSWORD=
      - MYSQL_ROOT_PASSWORD=
```
      
### Django Configs
Next you will need to navigate to Briefing/ and find the file settings.default.py. Move this file or copy it to settings.py

```
cp settings.default.py settings.py
```

Next you will need to set the password that you use above in the settings.py file. 
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'briefing',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
```

Look for what you see above and enter the user, password, and host. The host is "briefing_db" because the docker-compose.yml file calls that container briefing_db and it utilizes Docker's dns. You can either use "root" for the user and the root password, or the user/pass you set above.

## First run

### Building With Docker Compose
First you will need to build the Docker image. To do this, navigate to the folder where the docker-compose.yml file is and run:
```
sudo docker-compose build
```

### Starting With Docker Compose
Once the config files are modified you can go ahead and start the application using docker-compose. There are some additional steps to configure the database though once the project is started, but for now just run the following in the folder where the docker-compose.yml file is located.

```
sudo docker-compose up
```

I'm ommitting the "-d" to daemonize it so that we can see the log output for now. Go ahead and make a new console/terminal and run the following:
```
sudo docker exec -it briefing_web_1 /bin/sh
```
This will launch a terminal inside of the Django Docker container. Next we need to create the database schema and then create a super user for the admin. To create the database schema, in the /app folder run:

```
python3 manage.py makemigrations
python3 manage.py migrate
```

Then to create the super user run:

```
python3 manage.py createsuperuser
```

Once done, open your web browser and navigate to Briefing at 127.0.0.1:8000 or whatever your IP is + the port you set. You can access the admin at http://127.0.0.1:8000/admin/

### Creating a feed
[ Coming Soon ]
