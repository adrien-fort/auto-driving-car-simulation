Simul Module
==============

This module defines a simulation framework for vehicule/car movements in a given field. It includes a base class for simulations and a specific class for car simulations. Additionally, there is a function to run the simulation.

Simulation Class
----------------

.. class:: Simulation

   The base class for simulations provides a method to check if a given position is within the boundaries of the field.

CarSimulation Class
-------------------

.. class:: CarSimulation

   This class extends the `Simulation` class and adds methods specific to car simulations. It includes functions to check for car collisions, update collided cars, and execute car commands.

Functions
---------

.. function:: run_simul
   :noindex:

   This function orchestrates the execution of the simulation. It takes a field object and an array of cars as input, displays the initial state of the cars, and iteratively executes their commands until all cars have collided or all commands are completed.

Module Usage
------------

This module provides a framework for simulating car movements. Users can use the `run_simul` function to execute the simulation by providing a field object and an array containing cars.

Example
-------

.. code-block:: python
   
   import logging
   from src.display import CarDisplay
   from simul import CarSimulation, Simulation, run_simul

   # Define the field and cars
   field = ...  # Define your field instance
   cars = [...]  # List of car instances

   # Run the simulation
   run_simul(field, cars)