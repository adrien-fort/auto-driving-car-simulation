.. highlight:: python

========
Assumptions
========

The code is currently designed around several assumptions:
    | 1)Based on the requirement, cars that reach the edge of the field are still active but stop moving forward (over the edge) and might continue to move after being told to turn.
    | 2)Cars involved in a collision do not disappear until the end of the simulation, thus more cars could collide at the same coordinates in later steps.
    | 3)Fields with 0 width or height are not allowed.
    | 4)There is no point in running a simulation without car so the code will prompt user to start again

Snippet
--------

1) This is handled in the simul module in the execute_car_command method from the CarSimulation class as it calls the below check before letting car moving forward

.. code-block:: python

        def is_within_boundaries(field, pos_x, pos_y):
            # Returns true if coordinate provided are in boundary of the field
            return 0 <= pos_x < field.width and 0 <= pos_y < field.height

2) This is simply handled with the Vehicle.status attribute which Car inherits, cars in collided status stop executing commands but they remain in the cars array to check for collision

.. code-block:: python

    def execute_car_command(field, car, command, cars, step_counter):
        # Check if car isn't collided and then triggers the function associated with the command 
        if car.status == "running":
            if command == 'F':
                # Depending on direction, checking if the upcoming move is out of the field boundary before calling the move_forward method (if out of bound the move doesn't happen)
                # In a future iteration if we want the self-driving car/vehicule to avoid collision this would likely be handled here by adding more conditions 
                if car.direction == 'N' and CarSimulation.is_within_boundaries(field, car.pos_x, car.pos_y + 1):
                    car.move_forward()

3) This is a validation added in the field-creation method in the Field class:

.. code-block:: python

    # Check if at  both numbers are positive, making an assumption that a field without width or heights isn't allowed
    if width <= 0 or height <= 0:
        raise ValueError("Please enter positive integers for both width and height.")

4) This is a validation added at the start of the run_simul function:

.. code-block:: python

    def run_simul(field, cars):
        if not cars:
            print("You are trying to run a simulation without any car saved, please start over!")
            logging.warning(f"User was trying to run a simulation without any car saved and was prompted to start over.")
        else: