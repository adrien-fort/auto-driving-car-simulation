Display Module
=================

The `display` module provides a class, `CarDisplay`, with methods for displaying information about cars in the Auto Driving Car Simulation. The idea is that when the code gets extended to other vehicule there might be a need for different display approach and keep the modularity of displaying through this approach.

CarDisplay Class
---------------------

.. class:: CarDisplay

   The `CarDisplay` class contains methods for displaying information about cars before and after the simulation.

Functions
---------------------

.. function:: pre_sim_display

   Displays information about cars before the simulation.

.. function:: post_sim_display

   Displays information about cars after the simulation, inclusive of details in case of collision.

Usage
----------

To use the `CarDisplay` class and related functions, import them into your script:

.. code-block:: python

    from src.display import CarDisplay

    # Example usage
    car_display = CarDisplay()
    car_display.pre_sim_display([car1, car2])
    car_display.post_sim_display([car1, car2])
