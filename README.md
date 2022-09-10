# Infection_Sim
A simple NumPy + Pygame simulation of disease spreading, following the SIR model's classification of the population as **S**usceptible, **I**nfected and **R**ecovered, with a real-time graph of the evolution of the disease in terms of the infected, recovered and diseased. 

Other settings include a mortality rate, a velocity randomizer (for random walk), number of quarantined individuals, number of initial infections, and a function to control the speed of recovery/death.

<p align="center">
<img src="/images/settings.png" alt="Image of the settings with susceptible people set to 100, mortality rate to 20 percent, quarantined to zero, infected to 2, speed of recovery/death to 200 and randomizer set to True." title="">
</p>

**Simulation in action with the above settings** (graphical errors from the screen recorder used to make the gifs):

<p align="center">
<img src="/images/sim1.gif" alt="Animated gif of the simulation." width="300" height="250"/>
</p>

**Same simulation with randomize = False**

<p align="center">
<img src="/images/sim1_1.gif" alt="Animated gif of the simulation." width="300" height="250"/>
</p>

**With 70% of the population in quarantine**

<p align="center">
<img src="/images/sim2.gif" alt="Animated gif of the simulation." width="300" height="250"/>
</p>
