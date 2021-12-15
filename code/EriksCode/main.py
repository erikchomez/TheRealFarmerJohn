from Farmer import Farmer
import ray
from ray.rllib.agents import ppo
from pathlib import Path
import os

if __name__ == '__main__':
    ray.init()

    trainer = ppo.PPOTrainer(env=Farmer, config={
        'env_config': {},  # No environment parameters to configure
        'framework': 'torch',  # Use pyotrch instead of tensorflow
        'num_gpus': 0,  # We aren't using GPUs
        'num_workers': 0
    })

    user_input = input("Use last checkpoint [y/n]? ")

    if user_input.lower() == 'y':
        while True:
            dir_path = input("Training path data: ")

            if os.path.exists(dir_path):
                trainer.load_checkpoint(dir_path)
                break

            else:
                print("Invalid path: ", dir_path)

    current_directory = Path(__file__).parent.absolute()

    i = 0
    while True:
        print(trainer.train())

        i += 1
        if i % 2 == 0:
            checkpoint = trainer.save_checkpoint(current_directory)
            print("Checkpoint saved at ", checkpoint)

