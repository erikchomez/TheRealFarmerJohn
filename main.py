from agents.farmer import Farmer
import ray
from ray.rllib.agents import ppo
from pathlib import Path
import threading
import os


def train(trainer: ppo.PPOTrainer):
    while True:
        trainer.train()


if __name__ == '__main__':
    ray.init()

    trainer = ppo.PPOTrainer(env=Farmer, config={
        'env_config': {},  # No environment parameters to configure
        'framework': 'torch',  # Use pyotrch instead of tensorflow
        'num_gpus': 0,  # We aren't using GPUs
        'num_workers': 0
    })

    user_input = 'n'

    if user_input.lower() == 'y':
        while True:
            dir_path = input("Training path data: ")

            if os.path.exists(dir_path):
                trainer.load_checkpoint(dir_path)
                break

            else:
                print("Invalid path: ", dir_path)

    current_directory = Path(__file__).parent.absolute()

    training_thread = threading.Thread(target=lambda: train(trainer), daemon=False)
    training_thread.start()
    while True:
        cmd = input("ml_console > ")
        if cmd == "save":
            checkpoint = trainer.save_checkpoint(current_directory)
            print(f"Checkpoint saved as {checkpoint}")
        elif cmd == "exit":
            print("Ending main.py...")
            training_thread.join()
            break
