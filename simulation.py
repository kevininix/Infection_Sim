import sys
import pygame
import numpy as np

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 100, 255)
red = (255, 0, 0)
purple = (255,0,255)
grey = (230, 230, 230)
yellow = (255, 255, 0)

# Default background
background = white

# Dot population and enviroment
class Dot(pygame.sprite.Sprite):

  def __init__(self, x, y, width, height, color = black, 
  radius = 5, velocity = [0,0], randomize = False):
    
    # Call initializer in superclass
    super().__init__()

    # Width and height of dot people
    self.image = pygame.Surface(
        [radius * 2, radius * 2]
    )

    # Background
    self.image.fill(background)
    pygame.draw.circle(
        self.image, color, (radius, radius),
        radius
    )
    
    # virus inital parameters
    self.kill_switch_on = False
    self.recovered = False

    self.randomize = randomize

    # "Hitbox"
    self.rect = self.image.get_rect()
    self.pos = np.array([x, y], dtype = np.float64)
    self.vel = np.asarray(velocity, dtype = np.float64) 

    self.width = width
    self.height = height

  # Update attributes
  def update(self):

    self.pos += self.vel
    x, y = self.pos
    
    # Boundary conditions
    if x < 0 or x > self.width:
        self.vel *= -1
    if y < 0 or y > self.height:
        self.vel *= -1 

    self.rect.x = x
    self.rect.y = y

    # normalize velocity to slow down super fast dots
    vel_norm = np.linalg.norm(self.vel)
    if vel_norm > 5:
      self.vel /= vel_norm 

    # non-recovered dots have random velocity and thus direction
    if self.randomize:
      self.vel += np.random.rand(2) * 2 - 1
  
    # Every time a suceptible dot bumps into an infected 
    # dot it gets infected and either recovers or dies 
    # wheel_of_fortune handles how fast this happens 
    if self.kill_switch_on:
      self.wheel_of_fortune -= 1

      if self.wheel_of_fortune <= 0:
        self.kill_switch_on = False
        some_number = np.random.rand()

        if self.mortality_rate > some_number:
          self.kill() #<-- inherited from Sprite
        else:
          self.recovered = True
      
  # Change the color of the newly infected
  def respawn(self, color, radius = 5):

    return Dot(self.rect.x, self.rect.y, self.width,
    self.height, color = color, velocity = self.vel)
  
  # Whether an infected recovers or dies
  def killswitch(self, wheel_of_fortune = 20, 
  mortality_rate = 0.2):
    
    self.kill_switch_on = True
    self.wheel_of_fortune = wheel_of_fortune
    self.mortality_rate = mortality_rate


class Simulation:

  def __init__(self, width = 600, height = 480):

    self.width = width
    self.height = height

    # Containers
    self.susceptible_container = pygame.sprite.Group()
    self.infected_container = pygame.sprite.Group()
    self.recovered_container = pygame.sprite.Group()
    # entire population container
    self.all_containers = pygame.sprite.Group()
  
    # initial conditions
    self.n_susceptible = 20
    self.n_infected = 1
    self.n_quarantined = 0
    self.T = 1000
    self.wheel_of_fortune = 20
    self.mortality_rate = 0.2
  
  def start(self, randomize = False):
    
    # Total population
    self.N = self.n_susceptible + self.n_infected + self.n_quarantined

    # Initialize simulation
    pygame.init()
    screen = pygame.display.set_mode(
        (self.width, self.height)
    )
    
    # Susceptible dot people
    for i in range(self.n_susceptible):
      # Random start position
      x = np.random.randint(0, self.width + 1)
      y = np.random.randint(0, self.height + 1)
    
      # Random start velocity
      vel = np.random.rand(2) * 2 - 1
    
      # Dot person
      lil_guy = Dot(x, y, self.width, self.height, 
      color = blue, velocity = vel, randomize = randomize)
      self.susceptible_container.add(lil_guy)
      self.all_containers.add(lil_guy)

    # Susceptible dot people
    for i in range(self.n_quarantined):
      x = np.random.randint(0, self.width + 1)
      y = np.random.randint(0, self.height + 1)
    
      vel = [0, 0]
    
      lil_guy = Dot(x, y, self.width, self.height, 
      color = blue, velocity = vel, randomize = False)
      self.susceptible_container.add(lil_guy)
      self.all_containers.add(lil_guy)

    # Infected dot people
    for i in range(self.n_infected):
      x = np.random.randint(0, self.width + 1)
      y = np.random.randint(0, self.height + 1)
    
      vel = np.random.rand(2) * 2 - 1
    
      lil_guy = Dot(x, y, self.width, self.height, 
      color = red, velocity = vel, randomize = randomize)
      self.infected_container.add(lil_guy)
      self.all_containers.add(lil_guy)
    
    # Add a graph to display population stats
    stats = pygame.Surface(
      (self.width // 4, self.height // 4)
    )
    stats.fill(grey)
    stats.set_alpha(230)
    stats_pos = (self.width // 40, self.height // 40)

    # Define runtime of simulation
    clock = pygame.time.Clock()

    for i in range(self.T):
      # Check if game's closed
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()
      
      # Update all dot people
      self.all_containers.update()
      # Draw background
      screen.fill(background)    
      
      # Update stats
      stats_height = stats.get_height()
      stats_width = stats.get_width()
      n_inf_now = len(self.infected_container)
      n_rec_now = len(self.recovered_container)
      n_pop_now = len(self.all_containers)
      # x-axis position as function of time
      t = int((i / self.T) * stats_width)
      # plotting infected stats
      y_infect = int(
        stats_height - (n_inf_now / n_pop_now) * stats_height
      )
      # plotting deaths stats
      y_dead = int(
        ((self.N - n_pop_now) / self.N) * stats_height
      )
      # plotting recovered stats 
      y_recov = int(
        (n_rec_now / n_pop_now) * stats_height
      )

      stats_graph = pygame.PixelArray(stats)
      stats_graph[t, y_infect:] = pygame.Color(*red)
      stats_graph[t, :y_dead] = pygame.Color(*yellow)
      stats_graph[t, y_dead: y_dead + y_recov] = pygame.Color(*purple)

      # New infections 
      collision_group = pygame.sprite.groupcollide(
        self.susceptible_container,
        self.infected_container,
        True, #<-- remove from susceptible_container
        False #<-- infected stay the same
      )
      
      # Susceptible-to-infected conversion
      for lil_guy in collision_group:
        silly_guy = lil_guy.respawn(red)
        silly_guy.vel *= -1
        silly_guy.killswitch(
          self.wheel_of_fortune, self.mortality_rate
        )
        self.infected_container.add(silly_guy)
        self.all_containers.add(silly_guy)

      # Recoveries
      recovered = []
      for lil_guy in self.infected_container:
        if lil_guy.recovered:
          unsilly_guy = lil_guy.respawn(purple)
          self.recovered_container.add(unsilly_guy)
          self.all_containers.add(unsilly_guy)
          recovered.append(lil_guy)
      
      if len(recovered) > 0:
        self.infected_container.remove(*recovered)
        self.all_containers.remove(*recovered)

      self.all_containers.draw(screen)
      
      # delete the pixelarray object so it doesn't lock
      # the stat values and stop us from updating them
      del stats_graph
      stats.unlock()
      screen.blit(stats, stats_pos)
      pygame.display.flip()

      # Update display
      pygame.display.flip()
    
      # time before next loop round
      clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
  virus = Simulation()
  virus.n_susceptible = 30
  virus.mortality_rate = 0.2
  virus.n_quarantined = 70
  virus.n_infected = 2
  virus.wheel_of_fortune = 200
  virus.start(randomize = True)