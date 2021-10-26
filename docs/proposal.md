---
layout: default
title: Proposal
---
 
# {{ page.title }}

## Summary of the Project

The goal of this project is to train a Generative Adversarial Network (GAN) on real world Lidar point cloud terrain data and generate new point clouds visualized in Minecraft. 

Terrain generation is useful in world building. Generating terrains from real world data can be used in augmented reality, as well as world building in video games. Synthesizing Lidar point clouds can be used in developing systems that are capable of understanding their surroundings.

## AI/ML Algorithms

Our team anticipates using a GAN, employing two deep neural networks, a generator and a discriminator, that work against each other during model training. Each network will be trained using the Chamfer Loss.

## Evaluation Plan

The quantitative metrics we plan to evaluate are the reconstructed point clouds. We plan on using a combination Earth-Mover's Distance and Chamfer Distance. 

The qualitative metric we plan to evaluate is the visualized point clouds in Minecraft. We plan on producing voxels of the real world terrain data, and voxels of the generated point clouds to evaluate the quality of our generations. Then importing them to Minecraft and evaluating the macro features generated, such as overhanging clifss, etc. Our moonshot case would be to create a GAN capable of procedural generation of larger, more expansive models based on the training data.

## Appointment with the Instructor

We plan on meeting with the instructor on Thursday October 21 @ 2:15pm.
