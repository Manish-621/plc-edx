We will be using tutor which is a third party provider for openedx a docker based solution.

https://docs.tutor.overhang.io/



**Prerequisits:**

Docker

 
Docker-compose

---------------------------------------------------------------

**Check if prerequisits are installed or not**

To check if prerequisits are installed or not run the following commands

for checking docker version:

`docker --version`

If the software is not installed try installing the docker using the following command 

`curl -sSL https://get.docker.com/ | sh `

the following command will install the docker edge version. once docker installed give the docker non-root user access.
Instructions in the link below
https://docs.docker.com/engine/install/linux-postinstall/

for checking docker-compose version:

`docker-compose --version`

if docker-compose is not installed try installing from the following link

https://docs.docker.com/compose/install/

--------------------------------

**Installing TUTOR**


```
sudo curl -L "https://github.com/overhangio/tutor/releases/download/v3.12.3/tutor-$(uname -s)_$(uname -m)" -o /usr/local/bin/tutor
sudo chmod 0755 /usr/local/bin/tutor
```

`tutor local quickstart`

*** Basic tutor installation is done ***


once you are done with tutor you need to create a superuser

To create a superuser follow the below steps
https://docs.tutor.overhang.io/local.html#creating-a-new-user-with-staff-and-admin-rights

`tutor local createuser --staff --superuser yourusername user@email.com`

----------------------

**Local Development**

docs : https://docs.tutor.overhang.io/dev.html

For running tutor in local point the repo to you local working directory

1. build the image openedx-dev

`tutor images build openedx-dev`

2.once images is build just run the following command inorder to start local development

https://docs.tutor.overhang.io/dev.html#prepare-the-edx-platform-repo


```
tutor dev run -v /path/to/edx-platform:/openedx/edx-platform lms bash
pip install --requirement requirements/edx/development.txt
python setup.py install
paver update_assets --settings=tutor.development
```


 3. Once running the above commnds just run the following command

For LMS : 
`tutor dev runserver /path/to/edx-platform:/openedx/edx-platform lms` 

For CMS : 
`tutor dev runserver /path/to/edx-platform:/openedx/edx-platform cms` 


Browse the following urls:

LMS: localhost:8000
CMS: localhost:8001









