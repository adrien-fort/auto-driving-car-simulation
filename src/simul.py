import logging
from src.display import CarDisplay

def is_collision(cars, car, pos_x, pos_y):
    # Check if there is another car at the specified position
    for other_car in cars:
        if other_car != car and other_car.pos_x == pos_x and other_car.pos_y == pos_y:
            logging.info(f"There was a collision between {car.name} and {other_car.name} at coordinate ({pos_x},{pos_y})")
            return True
    return False

def get_collided_car_name(cars, car):
    # Simple function to fetch the other car name involved in the collision
    for other_car in cars:
        if other_car != car and other_car.pos_x == car.pos_x and other_car.pos_y == car.pos_y:
            return other_car.name
        
def update_collided_cars(cars, colliding_car):
    # Update the other car involved in the collision to receive details
    for other_car in cars:
        if other_car != colliding_car and other_car.pos_x == colliding_car.pos_x and other_car.pos_y == colliding_car.pos_y:
            other_car.status = "collided"
            
            # Check if collision_details is empty
            if colliding_car.collision_details:
                last_step = colliding_car.collision_details[-1]['step']
            else:
                last_step = 0
            
            other_car.collision_details.append({
                'with_car': colliding_car.name,
                'step': last_step
            })

def is_within_boundaries(field, pos_x, pos_y):
    # Returns true if coordinate provided are in boundary 
    return 0 <= pos_x < field.width and 0 <= pos_y < field.height

def execute_command(field, car, command, cars, step_counter):
    # Check if car isn't collided and then triggers the function associated with the command 
    if car.status == "running":
        if command == 'F':
            # Depending on direction, checking if the upcoming move is out of the field boundary before calling the move_forward method (if out of bound the move doesn't happen)
            if car.direction == 'N' and is_within_boundaries(field, car.pos_x, car.pos_y + 1):
                car.move_forward()
            elif car.direction == 'S' and is_within_boundaries(field, car.pos_x, car.pos_y - 1):
                car.move_forward()
            elif car.direction == 'E'and is_within_boundaries(field, car.pos_x + 1, car.pos_y):
                car.move_forward()
            elif car.direction == 'W' and is_within_boundaries(field, car.pos_x - 1, car.pos_y) :
                car.move_forward()
            #Once the move is done we are checking if the move has caused a collision
            if is_collision(cars, car, car.pos_x, car.pos_y):
                car.status = "collided"
                car.collision_details.append({
                    'with_car': get_collided_car_name(cars, car),
                    'step': step_counter
                })
                update_collided_cars(cars, car)
        elif command == 'L':
            car.turn_left()
        elif command == 'R':
            car.turn_right()
        else:
            # This shouldn't happen as we have validition when commands are inserted
            print(f"Unknown command '{command}' for car '{car.name}'")

def run_simul(field, cars):
    CarDisplay.pre_sim_display(cars)
    num_commands = max(len(car.commands) for car in cars)
    step_counter = 0

    while True:
        # The all car collided flag is set to True as the loop will update it to false as long as one car at least is in running status thus not allowing the loop to break until all cars have collided or all commands are run
        all_cars_collided = True

        for car in cars:
            if car.status == "running" and step_counter < len(car.commands):
                logging.info(f"Executing step {step_counter} of the simulation.")
                execute_command(field, car, car.commands[step_counter], cars, step_counter)
                if car.status == "running":
                    all_cars_collided = False

        if all_cars_collided or step_counter >= num_commands - 1:
            break

        step_counter += 1
    
    logging.info(f"The simulation has completed successfully.")
    CarDisplay.post_sim_display(cars)