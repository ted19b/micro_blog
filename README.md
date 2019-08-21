# micro_blog

This application is a mini blog, in which you must authenticate before you can post a message. 
You can also see messages posted by other users. You can also communicate with other blog users.

The application is developed with the python flask framework and serves as a tutorial for this framework.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Install python (Version >= 3.6)

* Install Pycharm, Visual Basic Code (or use Terminal)

### Installing

Clone the project and install all the necessary dependencies for the project.

> git clone https://github.com/ted19b/micro_blog.git

> pip install -r requirements.txt

### Configuration of the Application

#### Mail Config
to activate the sending of mails in the application it is necessary to configure certain environment variables 
 here is an example to use a google email account for sending and receiving emails  

> export MAIL_SERVER=smtp.googlemail.com

> export MAIL_PORT=587

> export MAIL_USE_TLS=1

>export MAIL_USERNAME=<your-gmail-username>

>export MAIL_PASSWORD=<your-gmail-password>

you can use the same configuration to use another mail account or even a local mail server.

just create an ".env" file and declare these variables in the file... they will be automatically loaded when the application is started.

example of the ".env" file
    
    SECRET_KEY=your-secret-key
    MAIL_SERVER=smtp.googlemail.com
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME=your-gmail-username
    MAIL_PASSWORD=your-gmail-password
    MS_TRANSLATOR_KEY=<your-translator-key-here>
    ELASTICSEARCH_URL=http://localhost:9200

#### Translation Config
Extracting Text to Translate...
you can use the pybabel command to extract them to a .pot file, which stands for portable object template. This is a text file that includes all the texts that were marked as needing translation. The purpose of this file is 
to serve as a template to create translation files for each language.

+ extraction of all texts

To extract all the texts to the .pot file, you can use the following command:

> pybabel extract -F babel.cfg -k _l -o messages.pot .

+ create translation file for each language

The next step in the process is to create a translation for each language that will be supported in addition to the base one, which in this case is English.

start by adding german (language code de), so this is the command that does that

> pybabel init -i messages.pot -d blog_app/translations -l de

If you want to support other languages, just repeat the above command with each of the language codes you want, so that each language gets its own repository with a messages.po file.


+ Updating the Translations

In this situation you'll want to add the _() or _l() wrappers when you detect texts that don't have them, and then do an update procedure, which involves two steps

> pybabel extract -F babel.cfg -k _l -o messages.pot .

> pybabel update -i messages.pot -d app/translations

### Start the application

Open a terminal 

> export FLASK_APP=run_blog.py

> flask run

Run the application in debug mode 
> export FLASK_DEBUG=1

> export FLASK_APP=run_blog.py

> flask run



