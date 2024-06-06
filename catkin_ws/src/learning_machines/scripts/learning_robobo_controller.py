#!/usr/bin/env python3
import sys
import matplotlib.pyplot as plt
from robobo_interface import SimulationRobobo, HardwareRobobo
from learning_machines import run_all_actions, task_zero
from data_files import FIGRURES_DIR, RESULT_DIR
import io
import cv2
import numpy as np



if __name__ == "__main__":
    # You can do better argument parsing than this!
    if len(sys.argv) < 2:
        raise ValueError(
            """To run, we need to know if we are running on hardware of simulation
            Pass `--hardware` or `--simulation` to specify."""
        )
    elif sys.argv[1] == "--hardware":
        rob = HardwareRobobo(camera=True)
    elif sys.argv[1] == "--simulation":
        rob = SimulationRobobo()
    else:
        raise ValueError(f"{sys.argv[1]} is not a valid argument.")

    def plot_list_of_values(my_list, name, experiment_nr):
        """"
        Takes in a list of values saves a plt plot to the figures_dir
        
        """
        plt.figure()
        plt.plot(my_list)
        plt.title('Sample Plot')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        # Convert the buffer to a NumPy array
        image = np.frombuffer(buf.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # Save the image using OpenCV
        cv2.imwrite(str(FIGRURES_DIR / f"{name}_experiment{experiment_nr}_{sys.argv[1]}.png"), image)
        plt.close()

    for experiment_nr in [1]:  
        frontlvals, frontrvals, frontcvals = task_zero(rob)
        values = {
            'frontlvals' : frontlvals,
            'frontrvals' : frontrvals,
            'frontcvals' : frontcvals
        }
        print("All frontL vals:", frontlvals)
        print("All frontR vals:", frontrvals)
        print("All frontC vals:", frontcvals)

        for key, value in values.items():
            plot_list_of_values(value, key, experiment_nr)
        """ # Open the file in write mode
        with open(filename, 'w') as file:
            # Iterate through the list and write each item to the file
            for item in frontlvals:
                file.write(str(FIGRURES_DIR / "test.txt"))"""
        


    



