# auto-driving-car-simulation

Simulation program to let cars move in a rectangular field with handling of potential collision between cars.

# Starting the program

just run src/Simulation.py in the src folder, this is where the main is and the programm starts, no other installation required other than Python. The code can run on both Windows and Linux.

# Assumptions made

The code is currently designed around several assumptions:
    -Based on the requirement, cars that reach the edge of the field are still active but stop moving forward (over the edge) and might continue to move after being told to turn.
    -Cars involved in a collision do not disappear until the end of the simulation, thus more cars could collide at the same coordinates in later steps.
    -Fields with 0 width or height are not allowed.
    -There is no point in running a simulation without car so the code will prompt user to start again


# BoW/Improvements

Below is a list of improvements that could be made but weren't in the initial requirements:
    -Car could stop themselves before entering a collision
    -Fields could be improved to include forbidden areas/coordinates (tree/wall/etc...)
    -Car/Vehicules could be given more commands (idle/parked/U turn) and diagonal directions (NE, NW, etc...)

# Tests

Unit tests have been written in pytest and thus pytest should be used to run them, they are all stored in the "tests" directory and follow usual naming convention thus can all be run at once if the "pytest" command is used.

# Observability

As this is a very basic application which doesn't even have API, no advanced telemetry except for logging has been put in place. The code will automatically create a logs directory under the project root and one log file per day will be created. 

# Documentation

Documentation was generated using Sphinx and is available in the docs directory. Simply run ".\make.bat html" (windows) or "make html" (linux) to regeneate the documentation.

# Pipeline

A very basic Github Action pipeline is in place which is triggered after a push, it will run the unit test against latest Ubuntu and will eventually let the code run on my Azure VM (stretch goal in progress).

# License

MIT License

Copyright (c) [2024] [Adrien Fort]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.