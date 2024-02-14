import logging

# Display requirements could change depending on vehicule thus creating a specific class with methods to display car information
class CarDisplay:
    def pre_sim_display(self, cars):
        # While the current logic of the code prevents the array from being empty when this method is called adding a check if usage changes in future
        if not cars:
            print("\nThere is currently no car saved.")
        else:
            print("\nYour current list of cars are:")
            for car in cars:
                print(f"- {car.name}, ({car.pos_x}, {car.pos_y}) {car.direction}, {car.commands}")

    def post_sim_display(self, cars):
        # While the current logic of the code prevents the array from being empty when this method is called adding a check if usage changes in future
        if not cars:
            print("\nThere is currently no car saved.")
        else:
            print("\nAfter simulation, the result is:")
            # Here I decided to report all collisions twice, once for each car as the requirement document showed the same
            for car in cars:
                if car.status == 'running':
                    print(f"- {car.name}, ({car.pos_x},{car.pos_y}) {car.direction}")
                    logging.info(f"- {car.name}, ({car.pos_x},{car.pos_y}) {car.direction}")
                elif car.status == 'collided':
                    for collision_detail in car.collision_details:
                        # The step counter start at 0 but for readability in the ouput incrementing one so that for user "step 1" is the first step
                        print(f"- {car.name}, collides with {collision_detail['with_car']} at ({car.pos_x},{car.pos_y}) at step {collision_detail['step']+1}")
                        logging.info(f"- {car.name}, collides with {collision_detail['with_car']} at ({car.pos_x},{car.pos_y}) at step {collision_detail['step']+1}")
                else:
                    # running and collided are the only two expected status in current version of code but just in case of
                    print(f"- {car.name} is currently in limbo and cannot be found!")
                    logging.error(f"- {car.name} is currently in limbo and cannot be found!")