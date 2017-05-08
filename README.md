# Barkly Observation Recording tool
=========================================

This is a tool for recording observations of teachers in the NT, Australia. It was developed with the [wq framework].

It implements a number of observation templates in use in the NT education department, as well as the possibility to create some new types of templates. 

It was developed with the [wq framework]: http://wq.io/ which allows for use in schools with unreliable internet connections.

## Installation

There isn't currently a public URL available to try it out. To install your own copy, I suggest you first follow the [install instructions] for wq on your system up to creating a "hello world" page. Not all steps are strictly necessary, but if you are not already familiar with wq then this will help you to install obstool.

The following assumes you have installed the necessary system-wide dependencies for running Django and wq.

To install obstool in a Linux environment, create a python 3 virtual environment (see the above linked docs for how to do this if you are unsure), activate it, and clone this repository:
```
https://github.com/davidoj/obstool.git
```
Install required packages:
```
cd obstool
pip install -r requirements.txt
```

Edit `conf/obstool.conf` with appropriate settings. See the wq [install instructions] for what is appropriate here.

Create a `db/obstool/local_settings.py` file with database details and a secret key. One way to do this would be to copy the `local_settings.py` from your "hello world" site. Otherwise, you can use this skeleton and fill it in with the details relevant to your system:

```
#local_settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '<database_name>',
        'USER': '<database_user>',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '<secret_key>'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
```

After this, you can migrate the database and create an admin account:

```
cd db/
./manage.py migrate
./manage.py createsuperuser
```

Configure and restard Apache 
```
sudo ln -s $PROJECTSDIR/obstool/conf/obstool.conf /etc/apache2/sites-available/
sudo a2ensite obstool
```

Finally, you will need to generate teh htdocs folder for your site:

```
./deploy.sh
```

Answer 'n' to overwriting any html templates.


[wq framework]: http://wq.io/
[install instructions]: (https://wq.io/1.0/docs/setup)
