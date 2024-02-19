import os
import sys
import logging

# Add the project's root directory to sys.path (this failed to happen under certain conditions)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

from src.setup import configure_logging
from src.field import Field
from src.car import car_creation
from src.simul import run_simul


def main():
    configure_logging()
    exit_program = False

    while not exit_program:
        print("Welcome to Auto Driving Car Simulation!", end='\n')
        logging.info("New instance of the app starting...")
        # Get user to create the field
        field = Field(None, None)
        simulation_field = field.field_creation()
        cars = []

        # Note the below loop could be improved in the future so that in first iteration it doesn't offer to run simulation with no car, this was not in the initial requirement though
        while True:
            option = input("Please choose from the following options:\n[1] Add car to field\n[2] Run simulation\n")
            
            #calling the car creation, not adding a break to allow repetition
            if option == '1':
                logging.info("User has opted to create a new car.")
                car_creation(simulation_field, cars)

            #calling the simulation and breaking out of the nested loop, as per requirement a different prompt is expected after simulation has run
            elif option == '2':
                logging.info("User has opted to run the simulation.")
                run_simul(simulation_field, cars)

                break
            else:
                print("Invalid choice, please enter 1 or 2!")
                logging.warning("User made an invalid choice and was prompted to retry")
        
        while True:
            user_input = input("\nPlease choose from the following options:\n[1] Start over\n[2] Exit\n\n")

            if user_input == '1':
                #Not displaying anything as per requirement, next print is back at the beginning of parent loop
                logging.info("User has opted to start over.")
                break
            elif user_input == '2':
                print("Thank you for running the simulation. Goodbye!")
                logging.info("User has opted to exit the application, shutting done now...")
                exit_program = True
                break
            else:
                print("Invalid choice, please enter 1 or 2!")
                logging.warning("User made an invalid choice and was prompted to retry")

main()