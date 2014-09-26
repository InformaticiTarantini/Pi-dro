This is a simple python script to control 2 DC motors using Raspberrypi and TB6612FNG motor controller

control:

UP(arrow key) = clockwise(2 motor)
DOWN(arrow key) = counter clockwise(2 motor)
LEFT(arrow key) = clockwise(left motor) + counter clockwise(right motor)
RIGHT(arrow key) = counter clockwise(left motor) +  clockwise(right motor)


Note: I use and modify some script from "RemoteKeyborgC" from PicoBorg

*EDIT*

**<Walter's Update>**

The Keyboard controls are now managed by a simple js script that makes requests to a web service,
that exposes a web interface to the GPIO management script, written in Python.
The web service is based on Flask and Bootstrap3.

*USAGE*

To install the requirements, use the following command

> pip install -r requirements.txt

Then, to run the server, launch the `pidro.py` script

> python pidro.py

To edit Flask settings, use the file `settings.py`. Here you can change the default port (8000),
the host and logging settings.

Enjoy!

 
