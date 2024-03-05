import numpy as np
map = np.loadtxt("map.csv", dtype=int)

# display
WIDTH = 1000
HEIGHT = 800

# Movement constants   
ROTATIONSPEED = 0.05
MOVESPEED = 0.08

# turn shadows on/off
showShadow = True

# Defines starting position and direction
positionX = 1.0
positionY = 1.0

directionX = 1.0
directionY = 0.0