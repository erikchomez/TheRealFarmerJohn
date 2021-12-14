---
layout: default
title: Final Report
---

# {{ page.title }}

## Video

## Project Summary
Our project goal is to train a Minecraft agent to plant, grow, and harvest
as much wheat as possible in a 3-day Minecraft cycle. In doing so, we wanted
to see if our agent could optimize farming around different environments,
and create farms that maximized both wheat growth and harvesting yield.

To accomplish this goal, we decided to use reinforcement learning, similar to the missions in Assignment 2.
However, for our project, reinforcement learning by itself wasn't effective, so
we trained our agent using a curriculum learning process.

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
    
By defining the problem in terms time, actions, environment, and optimization, it's clear that
there's not a trivial way to maximize the return of wheat without using "smart"
algorithms or machine learning. Even with smart algorithms, there may be bias
introduced with the methodology of each step, which is why we opted for pure
machine-learning. In other words, we didn't hard-code any behavior into our agent,
so our agent would learn how to optimize farming by itself.

Our agent's action space includes:
* moving
* turning
* using items in the inventory
* switching between items in the inventory
* jumping
* attacking (for harvesting)

And our agent's observation space includes:
* a 3x3 grid/array of blocks adjacent to the agent
* an array of items in the agent's inventory

We trained our agent in a variety of environments, with varying incentives and
playgrounds depending on the lesson being taught. In every lesson, our agent
spawned with a hoe (tool used for tilling grass/dirt into soil) and some seeds.
We tracked and graphed our agent's progress, and the specific lessons are covered
in the approaches section of this document.

## Approaches
Our team decided to take two approaches for training our agent through curriculum learning.
### Sequential Learning
One of the approaches involved teaching our agent the 

## Evaluation

## References

We used Assignment 2 and modified it for our project. We also used Malmo's XML schema documentation and project documentation. 

[XML Schema Documentation](https://microsoft.github.io/malmo/0.21.0/Schemas/MissionHandlers.html)

[Project Documentation](https://microsoft.github.io/malmo/0.30.0/Documentation/index.html)
