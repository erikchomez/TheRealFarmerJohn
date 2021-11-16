---
layout: default
title: Status
---

# {{ page.title }}

## Video

[![Watch the video](https://img.youtube.com/vi/euE9zT-ezas/maxresdefault.jpg)](https://www.youtube.com/watch?v=euE9zT-ezas)


## Summary of the Project

The goal of this project is to train an agent to maximize the amount of crop produced using a combination of reinforcement learning and curriculum learning. The agent starts off with an easy task and gradually the difficulty of each task is increased. The following is a sample curriculum: 

 1. Task 1

The agent is placed in an enclosed environment with the necessary tools and resources to begin farming.
 
 2. Task 2

The agent is placed in an open environment without limited tools and resources.
 
 3. Task 3

The agent is placed in an open environment without any tools and resources.

We are still continuing with the original proposal. 

## Approach

Our approach uses the Proximal Policy Optimization that is implemented by RLlib. For our input, we use an observation space that contains the closest 3x3 region. Since our agent starts off in a closed environment of size 9x9, this observation space worked well. We are able to send the agent what blocks are in front of it, and act accordingly. For instance, if there is an empty farmland in front of it, the agent will switch to hotbar 2 and use the seeds. If there is a block of dirt, the agent will switch to hotbar 1 and use the diamond hoe. Otherwise, the agent will move around and try to find farmland to plant seeds in. Currently we are taking a skill based approach on training the agent. We are working on training its seed planting skill, and then placing the agent in a more challenging environment. 

Our inital agent starts of in a closed off environment with a diamond hoe and seeds. The environment is a closed off 9x9 grid with a 5x5 grid of farmland in the center, as well as a single water block that hydrates the farmland. As the agent improves the skill it is training to improve, we plan on changing this environment to make it harder for the agent.

We also decided to use continuous movements to give our agent more freedom in the moves it can make. Our action space is of size 4 and includes "move", "turn", "use" and "jump". We included "move" and "turn" for basic maneuverability. "Use" is included because we want our agent to be able to use the diamond hoe or plant seeds. Finally, we include "jump" because we have an initial environment with farmland already generated, with a single water block source in the middle. The jump action allows the agent the escape the water block if it falls into it. The agent's pitch is also fixed at 45 so it has a clear view of the ground, while still having a good field of view. 

As for rewards, we decided to give the agent positive rewards for using and planting seeds, and for hoeing dirt blocks, as well as a negative reward for falling into the water block. We are still playing around with the reward scheme, and have not decided how to handle the time needed to grow crops, but the following is the general idea we had:

| Action      | Reward |
| :---        |    :----:   |
| Use seeds      | +1       |
| Use hoe | + 1 |
| Touching water block   | -10        |

## Evaluation

### Quantitative

For our quantitative evalauation, we decided to use the reward returns from previous episodes to keep track of how our agent is performing. Currently, we have an agent that is able to grow crops on most of the farmland, but we still are seeing the agent fall into the water and recieve a negative reward. We think that playing with the reward scheme would help stabilize the agent. We also trained our agent for a long period of time, and saw similar results, which can be seen in the second image below.

![banner](https://i.imgur.com/g4p4vk7.png)

![banner2](https://i.imgur.com/av7MP2o.jpeg)

## Remaining Goals and Challenges

### Remaining Goals

So far we have only trained the agent on placing seeds in farmland, and also started working on training the agent to hoe dirt into farmland. However, we still need to train the agent to grow the crops and maximize the amount of wheat it can grow. Since we are using a curriculum to train our agent, these first two tasks are part of the easier tasks that we will train our agent on. We plan on fleshing out a curriculum that will allow our agent to train effectively. 

For the following weeks, we plan on stabilizing the training for placing seeds and hoeing dirt. We also plan on creating more complex challenges that will be part of the overall curriculum. Another goal we have in mind is changing the training environment that we place the agent in. Currently we have a closed off environment and give the agent the tools necessary to grow crop. However, we plan on training our agent to be able to grow crop effectively in more complex and unconstrained environments. 

### Challenges

We have ran into a few challenges so far. One being figuring out a reward scheme that works best. We have been unable to stabilize the training to consistently get high rewards for farming land or placing seeds. Either the agent does well, or doesn't move towards the farmland and places seeds. We plan on playing around with the enclosed area to figure out if there is a way we can help the agent avoid falling into the water. Either by changing the negative reward, or placing a block that can rest over the water and still allow the agent to move over it. Something like slab might work for us. 

Giving rewards to the agent is another challenge we have come across. For instance, Malmo has the ability to reward the agent for a few actions, however, there is no reward endpoint for using an item. So figuring out how to reward our agent for hoeing dirt has been difficult compared to placing seeds (which has an endpoint RewardForDiscardingItem). Additionally, if the agent does get stuck in the water block, there is no reward for jumping so although we can give a negative reward for touching a water block, we still have to penalize the agent for jumping out. We think that combining the two actions' rewards could work in this situation. 

## Resources Used

We used Assignment 2 and modified it for our project. We also used Malmo's XML schema documentation and project documentation. 

[XML Schema Documentation](https://microsoft.github.io/malmo/0.21.0/Schemas/MissionHandlers.html)

[Project Documentation](https://microsoft.github.io/malmo/0.30.0/Documentation/index.html)
