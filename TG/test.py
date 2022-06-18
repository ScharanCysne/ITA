import random
import pygame  
pygame.init()
  
# Window dimensions (width, height)
WIN_WIDTH  = 800
WIN_HEIGHT = 500
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
win.fill((232, 232, 232))

# set the pygame window name 
pygame.display.set_caption("UAVs Simulator")

# Number of Obstacles
n_obstacles = 20
# Number of Agents  
n_agents = 1
x = 100
y = 100

# Dimensions of the object 
radius = 10
# Obstacles
obstacles = []
obstacles_pos = []
for i in range(n_obstacles):
    x_obs = random.random() * WIN_WIDTH
    y_obs = random.random() * WIN_HEIGHT
    obstacles.append(pygame.draw.circle(win, (60,51,158), (x_obs,y_obs), radius))
    obstacles_pos.append((x_obs,y_obs))
    
# Agents
agents = []
for i in range(n_agents):
   x = random.random() * WIN_WIDTH
   y = random.random() * WIN_HEIGHT
   agent = pygame.draw.circle(win, (82,0,0), (x,y), radius)
   agents.append(agent)

# velocity / speed of movement
step_size = 2
max_time = 10 #seconds
# Indicates pygame is running
run = True
  
# infinite loop 
while run:
    # creates time delay of 10ms 
    pygame.time.delay(10)
      
    # iterate over the list of Event objects  
    # that was returned by pygame.event.get() method.  
    for event in pygame.event.get():
          
        # if event object type is QUIT  
        # then quitting the pygame  
        # and program both.  
        if event.type == pygame.QUIT:
            # it will make exit the while loop 
            run = False
    # stores keys pressed 
    keys = pygame.key.get_pressed()
      
    # if left arrow key is pressed
    if keys[pygame.K_LEFT] and x > radius:
        # decrement in x co-ordinate
        agents[0].move(-step_size,0)
        x -= step_size

    # if left arrow key is pressed
    if keys[pygame.K_RIGHT] and x < WIN_WIDTH-radius:
        # increment in x co-ordinate
        agents[0].move(step_size,0)
        x += step_size
         
    # if left arrow key is pressed   
    if keys[pygame.K_UP] and y > radius:
        # decrement in y co-ordinate
        agents[0].move(0,-step_size)
        y -= step_size
          
    # if left arrow key is pressed   
    if keys[pygame.K_DOWN] and y < 500-radius:
        # increment in y co-ordinate
        agents[0].move(0,step_size)
        y += step_size
              
    # it refreshes the window
    win.fill((232, 232, 232))
    pygame.draw.circle(win, (82,0,0), (x,y), radius)
    for obstacle_pos in obstacles_pos:
        pygame.draw.circle(win, (60,51,158), obstacle_pos, radius)
    pygame.display.flip() 
  
# closes the pygame window 
pygame.quit()