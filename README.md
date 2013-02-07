bisp: Building Information Service Platform
===========================================

Discrete building simulator.

Introduction
-----------
In a time when people are starting to realize the impact of climate change, legislation has been introduced in order to limit the use of fossil fuels. A significant amount of the energy used today is spent in buildings. Still, little is known about how buildings are used and the tolerances of the factors influencing the experience of the occupants. With insights into these areas we can make informed decisions about the tradeoffs involved in running a building.

Buildings are complex systems with multiple layers of controllable services. Writing code for such a system requires a considerable amount of testing. It is paramount that the software controlling the building not turn off the electricity during normal operation. The same goes for water, ventilation, heating or cooling.

BISP provides a framework for working services it in a building. It acts as a repository for sensor data, and it export the measurement and building information using a coherent interface. 

Requirements
------------

* django: web framework
* django-tastypie: web service interface
* networkx: python graph library
* APScheduler: scheduling library http://packages.debian.org/sid/python-apscheduler
* MySQL: database management system

Installation
------------
We assume Ubuntu 12.10 LTS and django 1.41.

Make sure you have all dependencies:

	apt-get install mysql-server python-django python-mysqldb python-networkx python-tastypie python-setuptools git

The mysql-server package should ask you to select a root password. Remember this password, as it is needed later.

The package apscheduler is currently not in the ubuntu repository. Install the package using:

	easy_install apscheduler

Now it is time to fetch the code. You do this by using git and cloning the building simulator repository. Go into the directory where you would like to install the simulator and execute:

	git clone https://github.com/javigon/bisp.git

Now we have to setup the database access. Edit the bisp/bif/webconf/settings.py with your favorite editor.

At line 19, you see the line 'PASSWORD': 'password', change it to the password you entered when installing mysql.

Save and close the file.

Next we need to create the database. Run:

	mysql -u root -p

and enter your chosen database password.

Then write:

	create database bisp;

and after you may exit the mysql command line again by writing:

	exit

We are now ready to instantiate the database for bisp:

	cd into bisp/bif and write python manage.py syncdb

It will ask you to create a Django user.

	"You just installed Django's auth system, which means you don't have any superusers defined.
	Would you like to create one now? (yes/no): "

Write yes and create a user.

Now we have everything installed and ready to go. Start the bisp by executing:

	python manage.py runserver 127.0.0.1:8000

Before you can really use BISP, an building must be instantiated. To use the dummy building available in the source. You can either create it by accessing http://localhost:8000/admin/ (and insert a building) or write the following query into mysql:

	INSERT INTO repo_measurement (bid, description, bri, active) values(0, 'Building description', 0,1);


Source code structure
---------------------

* /doc/                Documentation
* /doc/manual.*        Manual
* /doc/sketches/       Ideas
* /doc/vocabulary.txt  List of terms
* /bif/                Source code
* /bif/sim/            Code for simulation
* /bif/webconf/        Django settings to connect the building model and sensor data repository
* /bif/building/       Building model and simulation instantiation
* /bif/examples/       Various examples on how to use the BISP framework
* /bif/userapi         Django app for exporting the building and sensor repository data
* /bif/repo            Django data definition for building and repository data.

* Please note that both the documentation and the presentation are written in LaTeX. Since we only provide the .tex file, it is necessary to build the documentation order to get a .pdf. The Makefile file provided can be used for this purpose (type make in /doc/). It is also possible to use a LaTeX compiler of choice (Mac users).
