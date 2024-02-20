import logging
import json
from pprint import pprint
from src.display import CarDisplay

#Creating a parent class for simulations with methods that are likely to be re-usable in all sub-classes
class Simulation:
    def is_within_boundaries(self, field, pos_x, pos_y):
        # Returns true if coordinate provided are in boundary of the field
        return 0 <= pos_x < field.width and 0 <= pos_y < field.height

# Creating a specific simulation class for car as simulation with other vehicules could require different behaviours
class CarSimulation(Simulation):
    def is_car_collision(self, cars, car, pos_x, pos_y):
        # Check if there is another car at the specified position
        for other_car in cars:
            if other_car != car and other_car.pos_x == pos_x and other_car.pos_y == pos_y:
                logging.info(f"There was a collision between {car.name} and {other_car.name} at coordinate ({pos_x},{pos_y})")
                return True
        return False

    def get_collided_car_name(self, cars, car):
        # Simple function to fetch the other car name involved in the collision
        for other_car in cars:
            if other_car != car and other_car.pos_x == car.pos_x and other_car.pos_y == car.pos_y:
                return other_car.name
        
    def update_collided_cars(self, cars, colliding_car, step_counter):
        # Update the other car involved in the collision to receive details
        for other_car in cars:
            if other_car != colliding_car and other_car.pos_x == colliding_car.pos_x and other_car.pos_y == colliding_car.pos_y:
                other_car.status = "collided"
                colliding_car.status = "collided"

                col_details_other = {
                    'with_car': other_car.name,
                    'step': step_counter
                }

                col_details_colliding = {
                    'with_car': colliding_car.name,
                    'step': step_counter
                }
                if col_details_other not in colliding_car.collision_details:
                    colliding_car.collision_details.append(col_details_other)

                if col_details_colliding not in other_car.collision_details:
                    other_car.collision_details.append(col_details_colliding)


    def execute_car_command(self, field, car, command, cars, step_counter):
        # Check if car isn't collided and then triggers the function associated with the command 
        if car.status != "running":
            return
        car_simulation = CarSimulation()
        def move_within_boundaries(dx, dy):
            if car_simulation.is_within_boundaries(field, car.pos_x + dx, car.pos_y + dy):
                car.move_forward()

        # Depending on direction, checking if the upcoming move is out of the field boundary before calling the move_forward method (if out of bound the move doesn't happen)
        # In a future iteration if we want the self-driving car/vehicule to avoid collision this would likely be handled here by adding more conditions 
        if command == 'F':
            if car.direction == 'N': move_within_boundaries(0, 1)
            elif car.direction == 'S': move_within_boundaries(0, -1)
            elif car.direction == 'E': move_within_boundaries(1, 0)
            elif car.direction == 'W': move_within_boundaries(-1, 0)

        #Once the move is done we are checking if the move has caused a collision
            if car_simulation.is_car_collision(cars, car, car.pos_x, car.pos_y):
                car_simulation.update_collided_cars(cars, car, step_counter)
        elif command == 'L':
            car.turn_left()
        elif command == 'R':
            car.turn_right()
        else:
            # This shouldn't happen as we have validition when commands are inserted but putting a check nonetheless
            print(f"Unknown command '{command}' for car '{car.name}'")

# This function is really specific to the car run currently, if other simulations are added this would require some refactoring
def run_simul(field, cars):
    if not cars:
        print("You are trying to run a simulation without any car saved, please start over!")
        logging.warning("User was trying to run a simulation without any car saved and was prompted to start over.")
        return

    car_display = CarDisplay()
    car_simulation = CarSimulation()
    car_display.pre_sim_display(cars)

    num_commands = max(len(car.commands) for car in cars)
    step_counter = 0

    while step_counter < num_commands:
        all_cars_collided = all(car.status != "running" or step_counter >= len(car.commands) for car in cars)

        if all_cars_collided:
            break

        for car in cars:
            if car.status == "running" and step_counter < len(car.commands):
                logging.info(f"Executing step {step_counter} of the simulation for {car.name}.")
                car_simulation.execute_car_command(field, car, car.commands[step_counter], cars, step_counter)

        step_counter += 1

    logging.info("The simulation has completed successfully.")
    car_display.post_sim_display(cars)