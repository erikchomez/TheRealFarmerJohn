---
layout: default
title: Final Report
---

# {{ page.title }}

## Video

## Project Summary
Our project goal is to train a Minecraft agent to plant, grow, and harvest
as much wheat as possible in a 10000000-tick Minecraft cycle. In doing so, we wanted
to see if our agent could optimize farming around different environments,
and create farms that maximized both wheat growth and harvesting yield. Eventually,
we want our agent to be able to farm in any naturally-generated environment, and
create farms that effectively utilize the environment (planting near water,
in direct sunlight, clustering crops, etc.)

To accomplish this goal, we decided to use reinforcement learning, similar to the
missions in Assignment 2. However, for our project, reinforcement learning by itself
wasn't effective, so we trained our agent using a curriculum learning process.
Reinforcement learning itself may produce effective results, but since farming
takes a lot of time, our group decided to split the learning into lessons to
speed up the process.

Farming in Minecraft is a multi-step process that can be optimized. Farming involves:
* Tilling land to turn it into soil
  * Soil can either be dry, or wet if it's near water
  * Dry soil will turn back into dirt if crops aren't planted in it within a few seconds
  * Wet soil will grow crops faster
  * Wet soil will not turn back into dirt
* Planting seeds
  * Right clicking on the soil once it's tilled
  * Clicking on any other block won't do anything
* Waiting for the crops to grow
  * During this time, crops will burst and turn back into dirt if jumped on
  * Hydrated crops take between 1-3 Minecraft days to grow into harvestable wheat
* Harvesting the crops
  * Harvesting requires the seeds to be fully grown
  * Harvesting crops early yields seeds, but no wheat
* Re-planting seeds
  * Land will still be tilled after harvesting
    
By defining the problem in terms of time, actions, environment, and optimization, it's clear that
there's not a trivial way to maximize the return of wheat without using "smart"
algorithms or machine learning. Even with smart algorithms, there may be bias
introduced with the methodology of each step, which is why we opted for pure
machine-learning. In other words, we didn't hard-code any behavior into our agent,
so our agent would learn how to optimize farming using its environment.

Our agent's action space includes:
* moving forward and backward
* turning
* using items in the inventory
* switching between items in the inventory
* jumping
* attacking (for harvesting)

And our agent's observation space includes:
* a 2x5x5 grid/array of blocks adjacent to the agent
* an array of items in the agent's inventory

We trained our agent in a variety of environments, with varying incentives and
playgrounds depending on the lesson being taught. In every lesson, our agent
spawned with a hoe (tool used for tilling grass/dirt into soil) and some seeds.
We tracked and graphed our agent's progress, and the specific lessons are covered
in the approaches section of this document.

## Approaches
Our team decided to train our agent using a Task-Specific Curriculum. Each
lesson involved training our agent by placing it in an environment and
rewarding it or punishing it based on its behavior, training the agent
until the returns converged, then using checkpoints to continue training
the agent on more difficult tasks.

That being said, the difficulty of the tasks, as well as the objectives,
varied in each curriculum. We took created two separate curriculums to evaluate
the effectiveness of our lessons and increase the chances of our agent learning.
### Many-Small-Life-Lessons Curriculum
The first approach we tested involved teaching the agent different, valuable
lessons for farming, and rewarding the agent for maximizing the yield in each lesson.
The last lesson would only reward the agent for harvesting wheat. 
The agent started with a diamond hoe and seeds in its inventory.
The lessons were as followed:
1. Plant as many seeds as possible
    * Environment: Flat grass plane
    * Rewards: +1 for discarding seeds
    * Punishments: -3 for obtaining seeds (either through harvesting early or jumping on them)
    * *The agent converged to ~125 seeds planted in about 1 million steps.
   Behavior included the agent jumping and moving diagonally backward while
   tilling the ground and planting seeds*
2. Plant as many seeds as possible, without getting stuck in walls
    * Environment: Flat grass plane enclosed with fences 50 blocks on any side
    * Rewards: +1 for discarding seeds
    * Punishments: -3 for obtaining seeds
    * *Agent was already good at planting, got stuck in walls in the beginning
   but eventually learned how to turn and plant along walls. Didn't stop on crops
   too often.*
3. Plant as many seeds as possible in an enclosed space, with water
    * Environment: Flat grass plane enclosed with fences, with water randomly generated inside
    * Rewards: +1 for discarding seeds
    * Punishments: -3 for obtaining seeds
    * *Agent struggled to learn how to utilize jumping effectively, but eventually converged to
   around 0, planting crops without jumping on them, but not
   planting as many as it did in previous trials.*
4. Harvest wheat
    * Environment: Same as trial 3
    * Rewards: +1 for harvesting wheat
    * Punishments: None
    * *Agent planted a lot of seeds and waited in water, but didn't know how to harvest wheat, even when
   standing next to fully grown wheat*

Looking at the graphs, it's clear that the first lesson was likely around a good
difficulty for our agent to master. Though graph 2 doesn't show the full training returns,
since the agent started off so well, it's likely that the lesson was too easy. Adjustments
could have been made to the environment size, or more obstacles could have been
generated to make the task more difficult.

Lesson 3 was too difficult for the agent to master, as the agent forgot most of
its previous training and instead opted to sit and do nothing as opposed to planting crops.
The agent still planted a full field of seeds sometimes, but othertimes sat still. This
may have been due to the random generation of water; if the agent spawned in a
body of water, its observation space would be filled with water and it would give up.

Lesson 4 may have been too much for our agent, due to the challenges presented
in the previous lesson. The agent was overfitted, and as a result didn't like planting anything
due to the punishments being weighted more than the rewards.
## Evaluation

## References

We used Assignment 2 and modified it for our project. We also used Malmo's XML schema documentation and project documentation. 

[Minecraft Wiki](https://minecraft.fandom.com/wiki/Minecraft_Wiki)

[Getting Started with Curriculum Learning](https://www.youtube.com/watch?v=zieklxM9LZE)

[Curriculum for Reinforcement Learning by Lilian Weng](https://lilianweng.github.io/lil-log/2020/01/29/curriculum-for-reinforcement-learning.html)

[XML Schema Documentation](https://microsoft.github.io/malmo/0.21.0/Schemas/MissionHandlers.html)

[Project Documentation](https://microsoft.github.io/malmo/0.30.0/Documentation/index.html)
