import subprocess
import pytest

# This is meant as the end to end test cases by running the main program through various input secenarios
def run_command_with_inputs(inputs):
    command = ['python', '..\src\Simulator.py'] 

    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    output, error = process.communicate(input=inputs)
    return process.returncode, output, error

def test_simulator_end_to_end():
    # Test case 1: Simulating an initial bad input in field - not integer
    inputs = "a 10\n" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1
    assert "Error: invalid literal for int() with base 10: 'a'. Please try again." in output

    # Test case 2: Simulating an initial bad input in field - not two numbers
    inputs = "10 10 10\n" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1
    assert "Error: Please enter exactly two integers.. Please try again." in output

    # Test case 3: Simulating an initial bad input in field - 0 width/height field
    inputs = "0 0\n" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1
    assert "Error: Please enter positive integers for both width and height.. Please try again." in output

    # Test case 4: Simulating an initial good input in field
    inputs = "10 10\n" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1 
    assert "You have created a field of 10 x 10." in output

    # Test case 5: Simulating a good input in field but unavailable choice
    inputs = "10 10\n3\n" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Invalid choice, please enter 1 or 2!" in output

    # Test case 6: Simulating a good input in field but starting a simulation without car loaded
    inputs = "10 10\n2\n" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "You are trying to run a simulation without any car saved, please start over!" in output

    # Test case 7: Simulating a good input in field and starting a car creation
    inputs = "10 10\n1\n" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Please enter the name of the car:" in output

    # Test case 8: Simulating a good input in field and starting a car creation - name entered
    inputs = "10 10\n1\nA\n" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Please enter initial position of car 'A' in x y Direction format:" in output

    # Test case 9: Simulating a good input in field and starting a car creation - bad input in position
    inputs = "10 10\n1\nA\na 1 W" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Error: invalid literal for int() with base 10: 'a'" in output

    # Test case 10: Simulating a good input in field and starting a car creation - bad input in position
    inputs = "10 10\n1\nA\n3 f W" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Error: invalid literal for int() with base 10: 'f'" in output

    # Test case 11: Simulating a good input in field and starting a car creation - bad input in position
    inputs = "10 10\n1\nA\n4 4 4 4" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Error: Please enter information in the requested format. Please try again." in output

    # Test case 12: Simulating a good input in field and starting a car creation - bad input in position
    inputs = "10 10\n1\nA\n4 4 L" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Error: Please enter a valid direction! Please try again." in output

    # Test case 13: Simulating a good input in field and starting a car creation - bad input in position
    inputs = "10 10\n1\nA\n10 10 N" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Error: Please enter position within the field of 10 x 10, meaning the max numbers are 9 x 9 as the field start at 0 x 0. Please try again." in output

    # Test case 14: Simulating a good input in field and starting a car creation - good input in position
    inputs = "10 10\n1\nA\n4 4 N" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Please enter the commands for car 'A':" in output

    # Test case 15: Simulating a good input in field and starting a car creation - bad commands input
    inputs = "10 10\n1\nA\n4 4 N\nFFULLR" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Error: Commands invalid, please follow expected format. Please try again." in output

    # Test case 16: Simulating a good input in field and starting a car creation - good commands input
    inputs = "10 10\n1\nA\n4 4 N\nFFLFLFR" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Your current list of cars are:\n- A, (4, 4) N, FFLFLFR" in output

    # Test case 17: Simulating a good input in field and car creation and starting smulation
    inputs = "10 10\n1\nA\n4 4 N\nFFLFLFR\n2" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Your current list of cars are:\n- A, (4, 4) N, FFLFLFR\n\nAfter simulation, the result is:\n- A, (3,5) W" in output

    # Test case 18: Two car simulation - attempt to create both car with same name
    inputs = "10 10\n1\nA\n4 4 N\nFFLFLFR\n1\nA" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Error: A car with the name 'A' already exists. Please choose a different name." in output

    # Test case 19: Two car simulation - attempt to create both car with same position
    inputs = "10 10\n1\nA\n4 4 N\nFFLFLFR\n1\nB\n4 4 S" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Error: Another car already exists at this position. Please choose a different position. Please try again." in output

    # Test case 20: Two car simulation - no collision case
    inputs = "10 10\n1\nA\n4 4 N\nFFLFLFR\n1\nB\n3 3 S\nFFLFLFR\n2" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Your current list of cars are:\n- A, (4, 4) N, FFLFLFR\n- B, (3, 3) S, FFLFLFR\n\nAfter simulation, the result is:\n- A, (3,5) W\n- B, (4,2) E" in output

    # Test case 21: Two car simulation - collision case
    inputs = "10 10\n1\nA\n4 4 E\nFFFFFF\n1\nB\n8 4 W\nFFFF\n2" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Your current list of cars are:\n- A, (4, 4) E, FFFFFF\n- B, (8, 4) W, FFFF\n\nAfter simulation, the result is:\n- A, collides with B at (6,4) at step 2\n- B, collides with A at (6,4) at step 2" in output

    # Test case 22: Three car simulation collision case with collision at different steps
    inputs = "10 10\n1\nA\n2 4 E\nFFFFFF\n1\nB\n6 4 W\nFFFF\n1\nC\n8 4 W\nFFFFFFF\n2" 
    returncode, output, error = run_command_with_inputs(inputs)
    assert returncode == 1  
    assert "Your current list of cars are:\n- A, (2, 4) E, FFFFFF\n- B, (6, 4) W, FFFF\n- C, (8, 4) W, FFFFFFF\n\nAfter simulation, the result is:\n- A, collides with B at (4,4) at step 2\n- A, collides with C at (4,4) at step 4\n- B, collides with A at (4,4) at step 2\n- B, collides with C at (4,4) at step 4\n- C, collides with A at (4,4) at step 4" in output