# Rock Contacts

*This application provides a simple SMS interface to commonly used Rock tasks.*

## Installation

Use `pip install -r requirements.txt` to install necessary libraries

## Development

Use [ngrok]() to create a secure tunnel to a public URL with:

    ./ngrok http -subdomain=rocksms 5000

## Deployment

### Install webserver

    $ sudo apt-get update
    $ sudo apt-get install apache2
    $ sudo apt-get install libapache2-mod-wsgi

### Point to Flask app

    $ mkdir ~/rocksms
    $ sudo ln -sT ~/rocksms /var/www/html/rocksms

### Create WSGI File
Put the following content in a file named `rocksms.wsgi`:

    import sys
    sys.path.insert(0, '/var/www/html/rocksms')
    
    from rocksms import app as application

### Enable `mod_wsgi`

The apache server displays html pages by default but to serve dynamic
content from a Flask app we'll have to make a few changes. In the apache
configuration file located at `/etc/apache2/sites-enabled/000-default.conf`,
add the following block just after the `DocumentRoot /var/www/html` line:

    WSGIDaemonProcess rocksms threads=5
    WSGIScriptAlias / /var/www/html/flaskapp/rocksms.wsgi
    
    <Directory rocksms>
        WSGIProcessGroup rocksms
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>

### Restart webserver

    $ sudo apachectl restart
