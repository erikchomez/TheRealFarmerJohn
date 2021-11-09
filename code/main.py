from Farmer import Farmer
import ray
from ray.rllib.agents import ppo


if __name__ == '__main__':
    ray.init()

    trainer = ppo.PPOTrainer(env=Farmer, config={
        'env_config': {},  # No environment parameters to configure
        'framework': 'torch',  # Use pyotrch instead of tensorflow
        'num_gpus': 0,  # We aren't using GPUs
        'num_workers': 0
    })

    while True:
        print(trainer.train())
