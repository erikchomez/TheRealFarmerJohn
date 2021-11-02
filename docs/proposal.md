---
layout: default
title: Proposal
---
 

# {{ page.title }}

## Summary of the Project

The goal of this project is to train an agent to maximize the amount of crop produced using a combination of tabular Q-learning and curriculum learning. The agent starts off with an easy task and gradually the difficulty of each task is increased. The following is a sample curriculum: 

 1. Task 1

The agent is placed in an enclosed environment with the necessary tools and resources to begin farming.
 
 2. Task 2

The agent is placed in an open environment without limited tools and resources.
 
 3. Task 3

The agent is placed in an open environment without any tools and resources.

## AI/ML Algorithms

Our team anticipates using curriculum learning and reinforcement learning. For the type of curriculum, we are thinking of using a Task-Specific Curriculum. This type of curriculum trains the model through gradually increasing level of complexity. Another approach we thought of was Skill-Based Curriculum. This approach decomposes what the agent is able to compete into a variety of skills, which are then mapped to a task.

## Evaluation Plan

We plan on evaluating the agent on how much crop it was able to maximize over a certain time frame. We also plan on using a Q-Table to visualize the results at each state.

## Appointment with the Instructor

We plan on meeting with the instructor on Thursday October 21 @ 2:15pm.
