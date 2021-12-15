---
layout: default
title: Final Report
---

# {{ page.title }}

## Video

[![Watch the video](https://img.youtube.com/vi/DX2mueYg7qM/maxresdefault.jpg)](https://www.youtube.com/watch?v=DX2mueYg7qM)

## Project Summary
Our project goal is to train a Minecraft agent to plant, grow, and harvest
as much wheat as possible in a 1000000-tick Minecraft cycle. In doing so, we wanted
to see if our agent could optimize farming around different environments,
and create farms that maximized both wheat growth and harvesting yield. Eventually,
we want our agent to be able to farm in any naturally-generated environment, and
create farms that effectively utilize the environment (planting near water,
in direct sunlight, clustering crops, etc.)

To accomplish this goal, we decided to use reinforcement learning, similar to the
mission in Assignment 2. However, for our project, reinforcement learning by itself
was unable to establish the connection between sowing and proper harvesting due to the time necessary for wheat growth.
Therefore, we opted to train our agent using a curriculum learning process in which we could specify individual skills necessary for the process and allow the agent to link these learned behaviors together to successfully optimize the end goal of harvesting wheat.
Curriculum learning also allowed us to split the complex task into smaller segments for easier debugging and analysis, and due to the prolonged time necessary for crop growth in Minecraft without the use of artificial lights or bone meal, was pivotal in producing reasonable test durations. It was both convenient and necessary in order to attempt this multi-stage, randomized time-delay task.

In regards to the process itself, farming in Minecraft is a multi-step process that can be optimized with various factors:
* Tilling land to turn it into soil
  * Soil can either be dry, or wet if it's within 4 blocks of water
  * Dry soil will turn back into dirt if crops aren't planted in it within a few ticks
  * Wet soil will grow crops faster
  * Wet soil will not turn back into dirt
* Planting seeds
  * Right clicking on the soil once it's tilled with a hoe tool
* Waiting for the crops to grow
  * Wheat grows in 7 stages, only advancing if exposed to high levels of light (daytime in our case)
  * Crop growth is nonlinear, and the growth ticks are randomized.
  * During this time, crops will break and farmland turn back into dirt if jumped on
  * Hydrated crops take between 1-3 Minecraft days to grow into harvestable wheat
* Harvesting the crops
  * Harvesting requires the wheat to be fully grown, otherwise returns one seed
  * Harvesting crops yields 1 wheat, and 0-3 seeds.
* Re-planting seeds
  * Dirt will remain tilled after harvesting
    
By defining the problem in terms of time, actions, environment, and optimization, it's clear that
there is no trivial way to maximize the return of wheat without using "smart"
algorithms or machine learning in application on varying environments. An agent must plant the seed, abstain from breaking the growing crop, and only harvest the wheat when fully grown. Given Malmo's limited observation space, the agent is unable to tell if the farmland is watered or not and what stage of growth the crop is in. Given that the growth time for crops can vary up to a factor of 3 times the minimum ticks required, the agent must maintain efficiency by balancing the line between overwaiting and premature harvesting. 
Even with smart algorithms, there may be bias
introduced with the methodology of each step, which is why we opted for pure
machine-learning. In other words, we didn't hard-code any behavior into our agent
so our agent would learn how to optimize farming using only its environment and reward system.

Our agent's action space includes:
* moving forward and backward
* turning
* using items in the hotbar
* switching between items in the hotbar
* jumping
* attacking (for harvesting)

And our agent's observation space includes:
* a 2x5x5 grid/array of blocks centered on the agent
* an array of items in the agent's inventory

The observation space was extended to a width of 5 due to water blocks hydrating 4 blocks outwards in all directions.

We trained our agent in a variety of environments, with varying rewards and
training environments depending on the lesson being taught. In every lesson, our agent
spawned with a diamond hoe (tool used for tilling grass/dirt into soil) and stacks of seeds. The number of hoes and seeds were altered in later lessons to focus training on efficiency and working within time and resource constraints.
We tracked and graphed our agent's progress with our reward system and manual observation, and the specific lessons attempted are covered
in the approaches section of this document.

## Approaches
Our team decided to train our agent using a Task-Specific Curriculum. Each
lesson involved training our agent by placing it in an environment and
rewarding it or penalizing it based on its behavior, training the agent
until the returns converged, then using checkpoints to continue training
the agent on more difficult tasks.

That being said, the difficulty of the tasks, as well as the core objectives,
varied in each curriculum. We created two separate curriculums to evaluate
the effectiveness of our lessons and increase the chances of our agent learning.
### Many-Small-Life-Lessons Curriculum
The first approach we tested involved teaching the agent different, valuable
lessons for farming, and rewarding the agent for maximizing the yield in each lesson.
The last lesson would only reward the agent for harvesting wheat.
The lessons were as followed:
1. Plant as many seeds as possible
    * Environment: Flat grass plane
    * Rewards: +1 for discarding seeds
    * Punishments: -3 for obtaining seeds (either through harvesting early or jumping on them)
    * *The agent converged to ~125 seeds planted in about 1 million steps.
   Behavior included the agent jumping and moving diagonally backward while
   tilling the ground and planting seeds*
    ![](https://raw.githubusercontent.com/erikchomez/TheRealFarmerJohn/jskwon2/docs/images/m_returns_seeds.png)
      
2. Plant as many seeds as possible, without getting stuck in walls
    * Environment: Flat grass plane enclosed with fences 50 blocks on any side
    * Rewards: +1 for discarding seeds
    * Punishments: -3 for obtaining seeds
    * *Agent was already good at planting, got stuck in walls in the beginning
   but eventually learned how to turn and plant along walls. Didn't stop on crops
   too often.*
      ![](https://raw.githubusercontent.com/erikchomez/TheRealFarmerJohn/jskwon2/docs/images/m_returns_walls.png)

3. Plant as many seeds as possible in an enclosed space, with water
    * Environment: Flat grass plane enclosed with fences, with water randomly generated inside
    * Rewards: +1 for discarding seeds
    * Punishments: -3 for obtaining seeds
    * *Agent struggled to learn how to utilize jumping effectively, but eventually converged to
   around 0, planting crops without jumping on them, but not
   planting as many as it did in previous trials.*
      ![](https://raw.githubusercontent.com/erikchomez/TheRealFarmerJohn/jskwon2/docs/images/m_returns_water.png)
4. Harvest wheat
    * Environment: Same as trial 3
    * Rewards: +1 for harvesting wheat
    * Punishments: None
    * *Agent planted a lot of seeds and waited in water, but didn't know how to harvest wheat, even when
   standing next to fully grown wheat*
      ![](https://raw.githubusercontent.com/erikchomez/TheRealFarmerJohn/jskwon2/docs/images/m_returns_wheat.png)

Looking at the graphs, it's clear that the first lesson was likely around a good
difficulty for our agent to master. Though graph 2 doesn't show the full training returns,
since the agent started off so well, it's likely that the lesson was too easy. Adjustments
could have been made to the environment size, or more obstacles could have been
generated to make the task more difficult.

Lesson 3 was too difficult for the agent to master, as the agent forgot most of
its previous training and instead opted to sit and do nothing as opposed to planting crops.
The agent still planted a full field of seeds sometimes, but at other times sat still. This
may have been due to the random generation of water; if the agent spawned in a
body of water, its observation space would be filled with water and it would give up.

Lesson 4 may have been too much for our agent, due to the challenges presented
in the previous lesson. The agent was overfitted, and as a result didn't like planting anything
due to the punishments being weighted more than the rewards.

Building off of Lesson 3, in a different environment consisting of a 9x9 enclosed space with a single water block in the center, the agent was able to harvest wheat with a few supervisiations. Since the space is so compact, and there is no room for the agent to walk around and take actions while it waits for the crop to grow, instead it goes into a hibernation, waiting a certain amount of time to allow the crops to grow. To speed up the process as well, torches were placed around the farmland to allow the crops to grow overnight. With these modifications, the agent was able to successfully harvest wheat. 

4.1 Harvesting wheat in smaller enclosed space
* Environment: Flat grass plane enclosed with fences 9 blocks on any side, as well as a 5x5 farmland grid in the center.
    
* Rewards: +1 for harvesting wheat
    
* Punishments: -1 for collecting torches
    
* *Agent was able to plant seeds, and wait for the crop to grow. Then was able to harvest crop.*
    
![banner2](https://i.imgur.com/8pb3aie.png)

Although this approach worked, and the agent was able to harvest crop at the end. It wouldn't translate well to the actual gameplay mechanics. If the agent were to stand still and wait for crops to grow, it exposes itself to potential mob attacks if it does so during the night. Also, staying still prevents the agent from learning and collecting rewards by hoeing dirt and planting seeds. 

### Converging Skills Curriculum
As our first approach was unable to establish the connection between sowing seeds and harvesting fully grown wheat in separated and specified lessons, we attempted a new approach focusing on consistently pushing the agent towards proper harvesting within segmented lessons. 

We trained the agent in the following steps:

Sowing Seeds -> Harvesting Wheat -> Efficiency Within Constraints -> Application in Simulated Environment

The key objective of wheat collection was maintained by outsizing it's reward, while penalties and rewards for other behaviors was adjusted as necessary between each lesson to better train the targeted behavior for that stage.

The first two stages were 50x50 blocks, bordered by a 1 block high fence with cobblestone beyond it that would penalize the agent and end the current mission, and 10% of the land available were water blocks distributed near the central spawn area.

1. Prioritizing  Seeds:
    * The first lesson was focused on re-teaching the agent to plant seeds without having the agent be stuck in water or escape by randomly placing dirt blocks by the fence.
    * The reward / penalty schema was:
      * PLANTING SEED +2 (ENCOURAGE PLANTING)
      * COLLECTING WHEAT +100 (PRIMARY GOAL)
      * STEPPING ON WATER -10 (PENALIZE GETTING STUCK IN WATER)
      * COLLECTING DIRT -1 (PENALIZE UNNECESSARY BLOCK BREAKAGE)
      * COLLECTING SEED -5 (MAJORITY FROM TRAMPLING, SMALL AMOUNT FROM HARVESTING)
    * The alloted time was lengthy to allow for growth, but we soon found that the agent learned to optimalize its rewards by randomly planting as many seeds as possible around the map as fast as possible until its hoe broke, then wandering until the time ran out or he escaped by accident instead of harvesting.

    ![banner2](https://i.imgur.com/5FTXr6r.png)
    * While the agent was successful in learning to sow seeds as quickly as possible, we adjusted the reward weights and items available to the agent to account for the "sow not harvest" strategy the agent acquired. Manual observation revealed no more than 10 wheat harvested in most sessions.

    ![banner2](https://i.imgur.com/LNHZm2e.png)
    * This was due to the same roadblock we were facing in our first approach: myopic reward optimalization. This core challenge will be expanded on our evaluation section.

2. Prioritizing  Wheat:
    * After analysing the issues we faced in the first lesson, we attempted to account for them by shifting the reward weights to prioritize wheat collection and giving the agent an additional diamond hoe in place of a seed stack.
    * The new reward / penalty schema was:
      * PLANTING SEED +1 (LOWERED TO AVOID SOW NOT HARVEST STRATEGY)
      * COLLECTING WHEAT +100
      * STEPPING ON WATER -2 (TO AVOID HYDROPHOBIA)
      * COLLECTING DIRT -5 (INCREASED PENALTY)
      * PLACING DIRT -10 (PENALIZE POTENTIAL ESCAPE)
      * STEPPING ON COBBLESTONE -1000 (HEAVILY PENALIZE ESCAPES)
      * COLLECTING SEED -2 (LOWERED TO ENCOURAGE BREAKING WHEAT EVEN IF PREMATURE)
   *  This stage was left running for the longest time, as we believed it was the most critical component of the agent's learning to reach the final goal.
   *  Only two escapes were recorded, and although a restart was necessary due to a crash caused by server lag, this lesson was extremely successful.
   *  The agent went from accidentally breaking wheat to developing a set pattern, and even though penalties were increased on average, maintained a fairly high reward outcome.

   ![banner2](https://i.imgur.com/kICC8JE.png)

   ![banner2](https://i.imgur.com/sjQN2B4.png)

   *  Although at first glance it may seem the agent scored much lower, but this is where we found a huge issue within Malmo's reward system. We found that not all wheat collections were being rewarded properly, likely due to the high tick per second we were employing in order to have these extremely long trials complete in reasonable time.
   *  In reality, manual observation showed the agent was consistently almost tripling the average wheat collected averaging above 30 per session, now employing a tactic of "wetland, dryland, wetland," where the agent plants as many seeds as possible around the spawn area with water blocks, walk off into the dry corners of the map to plant seeds gaining additional rewards and seemingly wait out time, then returns once it has broken both the diamond hoes given which coincided with the growth of the wheat.

   ![banner2](https://i.imgur.com/b7QsDYJ.png)

   *  The seed planting optimization was carried through into this lesson, showing the fruits of our curriculum learning - in this example, the agent has planted nearly 6 stacks of seeds within 28% of the allotted time.

   ![banner2](https://i.imgur.com/XoF1EBv.png)

   *  The agent also began to show a loose understanding of planting in hydrated farmland and in bunches rather than sparse patches. The agent would till and sow a small circle, then move on to a new location, and repeat.

3. Prioritizing Efficiency
   * This is by the most difficult step, as we now constrained our agent to a much smaller field with only 25% of the land and water availble, half the time previously alloted, and half the resources previously given (1 diamond hoe, 3 stacks of seeds).
   * The new reward / penalty schema was:
      * COLLECTING WHEAT +100
      * STEPPING ON WATER +1 (TO PUSH FOR HYDROPHILIA AND PLANTING IN HYDRATED FARMLAND)
      * COLLECTING DIRT -10 (INCREASED PENALTY)
      * PLACING DIRT -10
      * STEPPING ON COBBLESTONE -100 (REDUCED PENALTY TO KEEP GRAPHS NEATER)
      * COLLECTING SEED -2
   * Rewards for planting seeds were now completely removed, as we wanted our agent to not rely on any kind of tactic where they prioritized seed planting for rewards. Besides a small reward for water, the only reward source was from the wheat. We wanted to force our agent to become efficient in resource and time management, further penalize unnecessary dirt block breakage, heavily prioritize hydrated farmland, and focus purely on wheat harvesting rather than seed planting.
   * As expected, this step was largely in the negatives for our agent, and escapes were somewhat frequent.

   ![banner2](https://i.imgur.com/RYxlCUq.png)

   ![banner2](https://i.imgur.com/ptsYTTg.png)

   * The agent struggled the most against the space constraint, and was unable to properly harvest the few crops that successfully grew in time.

   ![banner2](https://i.imgur.com/1Dq5yjc.png)

   * It still maintained ideal planting speed, quickly using up both the hoe and seeds. The issue was that in a small map, the agent frequently ended up escaping or waiting too long, with the mission ending right as it began to harvest.
   * This was largely in line with our goal, as the agent was to return to its normal constraints but with the curriculum of efficiency embedded in its behavior.

4. Application in Island Environment
   * The agent, now armed with a definite understanding of where and how quickly to till and sow, a grasp on when to harvest, and the bias for task efficiency, is put to the test against a completely untrained baseline in a foreign environment.
   * If successful, the segmented skills should converge through curriculum learning into a behavior that vastly outperforms an agent without the aforementioned lessons.
   * All of the agent's resources and time were reset to the first lesson's. (1 diamond hoe, 6 stacks of seeds)
   * The new environment was a 30x30 simulated island, with a small 6x6 lake in the center and an outer 1 block ring of water. Borders were kept in place for the sake of the untrained agent and consistency. There were 4 outer rings and 4 inner rings of hydratable farmland, and 15 middle rings of dry farmland between them to allow selectivity of crop placement.
   * The new reward / penalty schema was:
      * COLLECTING WHEAT +1 (THE END GOAL, THE ONLY MEASUREMENT THAT MATTERS IN OUR AGENTS LEARNING)
      * NOTHING ELSE IS COUNTED, AS WE ONLY WANT TO SEE HOW MUCH WHEAT OUR AGENT CAN SUCCESSFULLY GATHER
   * At this point, we successfully debugged and implemented our own reward system for wheat. Unlike previous lessons when some wheats were uncounted for due to missed ticks, we verified that our system is accurate in every observed mission.

   ![banner2](https://i.imgur.com/gZ4XA83.png)

   * As we can see in our baseline, the untrained agent was still able to successfully gather a few wheats from assumably random behavior, albeit inconsistent and often returning back to 0.

   ![banner2](https://i.imgur.com/LBoA7K7.png)

   * As shown above, our trained agent completely outperformed the untrained agent, consistently reaching above 15 crops to a maximum of 38 crops. Due to the limited size of the environment, it still struggled with escaping borders occasionally.


## Evaluation
### Quantitative
From a quantitative standpoint, our agent was able to harvest over 40 wheats on average
as it progressed in its last lesson in the second
curriculum, and 30 on average in the last curriculum. 
Our baseline agent was only able to harvest a few wheats in random
intervals, so it's clear that our trained agent was able to learn through its 
curriculum. Our rewards charts, albeit flawed due to Malmo's reward system, still shows a massive gap between
untrained and trained agents, and a continual progress towards efficiently gathering wheat.
### Qualitative
There are several improvements that our agent could use.

One of the most wasteful behaviors of our agent is that it doesn't optimize
for tool durability. As a result, it sometimes breaks the hoe, despite the
fact that the hoe has enough durability to plant all of the seeds. If we were to
deploy our agent in any useful capacity, we would have to find a way to reward/punish
the agent for tool usage.

Another inherent aspect to farming is time; the agent needs to take care of itself
during the farming process. Since farming takes days, the agent almost starves to
death on every mission, especially if it's jumping a lot. To improve this, we could
start the agent off with some food, and reward it for eating if its hungry. Or, if we
decided to implement AI, we could just tell it to eat when its hungry.

Despite these areas that could be improved, our agent did start to produce higher quality
results.

We have observed that as our agent progresses, it has
started to learn to cluster food closer together (as opposed to randomly scattering it
across the map). We expect that as the agent continues to learn, it will start to
produce higher quality farmland, which more closely resembles that of a real
player.

Surprisingly, the agent also taught us something. It's more efficient to harvest
wheat by jumping on it than breaking it. Our agent, in its last lesson, learned that 
breaking wheat, then walking over to pick it up, takes too much time. Jumping on wheat
directly below the agent allows it to take the wheat immediately, which is faster. Most of us would not think to do so, as it returns the farmland beneath into regular dirt, but the agent does not care as there was never a point where the agent had enough time to plant, harvest, replant, and harvest the same block, and therefore never optimized for it. Our agent was able to discover something most of us would not consider, as it only looks at the task in hand rather than conventional reasoning.

### Malmo's Limits
Malmo was not easy to work with. Teaching an agent to farm took a lot of time, and
with millions of steps, it was necessary for us to speed up the ticks in order to
get any usable results in 10 weeks.

Speeding up the ticks to anything besides 20ms (the default) caused the Malmo/Minecraft
server to fall behind updating, which led to most of the reward signals
not functioning. Additionally, Malmo's reward system is bugged: a reward
of 1 for collecting seeds triggers a reward of 64, if the agent has at least 64
seeds in its inventory.

To get past this, we had to implement many of our own changes that either
normalize Malmo's rewards, or bypassed them entirely. The only problem with normalizing
rewards are that we couldn't distinguish between the agent collecting seeds, or wheat.
This effectively killed the agent's learning chances in the first curriculum, and made
all subsequent missions more difficult.

For the second curriculum, we implemented our own rewards system that added the
hotbar as an observation space, and programmatically rewarded the agent if it
harvested wheat. Many of the challenges we faced outside of designing the environment
were caused by Malmo, but we were able to successfully finish training our agent
anyway.
## References

We used Assignment 2 and modified it for our project. We also used Malmo's XML schema documentation and project documentation. 

[Minecraft Wiki](https://minecraft.fandom.com/wiki/Minecraft_Wiki)

[Getting Started with Curriculum Learning](https://www.youtube.com/watch?v=zieklxM9LZE)

[Curriculum for Reinforcement Learning by Lilian Weng](https://lilianweng.github.io/lil-log/2020/01/29/curriculum-for-reinforcement-learning.html)

[XML Schema Documentation](https://microsoft.github.io/malmo/0.21.0/Schemas/MissionHandlers.html)

[Project Documentation](https://microsoft.github.io/malmo/0.30.0/Documentation/index.html)
