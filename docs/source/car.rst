.. highlight:: python

==========
Car Module
==========

The `car` module provides classes and functions for creating and managing cars in the Auto Driving Car Simulation.

Vehicle Class
---------------

.. class:: Vehicle

      The `Vehicle` class is a generic class representing a vehicle. It mostly holds attributes that would be common to all vehicules and leave the  methods for moving forward, turning left, and turning right to the subclasses.

Car Class
--------------

.. class:: Car

      The `Car` class is a subclass of `Vehicle` with specific implementations for moving forward, turning left, and turning right.

Functions
-------------

.. function:: is_valid_integer

   Checks if a given value is a valid integer.

.. function:: car_naming

   Prompts the user to enter a unique name for a car.

.. function:: car_position

   Prompts the user to enter the initial position and direction of a car.

.. function:: car_commands

   Prompts the user to enter commands for the car to follow in simulation.

.. function:: car_creation

   Creates a new car instance based on user inputs from above functions.

Dependencies
------------

- display.py


Usage
--------

To use the `Car` class and related functions, import them into your script:

.. code-block:: python

    from src.car import Car, is_valid_integer, car_naming, car_position, car_commands, car_creation

    # Example usage
    car = Car("MyCar", 0, 0, "N", "FFR")
    car.move_forward()
    car.turn_left()
    car.turn_right()

    is_int = is_valid_integer("42")
    name = car_naming([])
    pos_x, pos_y, direction = car_position(Field(), [], "MyCar")
    commands = car_commands("MyCar")
    new_cars = car_creation(Field(), [])
