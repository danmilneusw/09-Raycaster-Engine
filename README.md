# 09-Raycaster-Engine
## Introduction
The Raycaster engine was first developed by John Carmack of id Software in 1991 and 1992 for Wolfenstein 3D. It also was used for:
- 1992: Wolfenstein 3D
- 1992: Spear of Destiny
- 1993: Blake Stone: Aliens of Gold
- 1993: Wolf VR
- 1993: Blake VR
- xxxx: Hellraiser (cancelled)
- 1994: Corridor 7: Alien Invasion
- 1994: Cybertag
- 1994: Spear Mission Packs (Lost Episodes)
- 1994: Super 3D Noah’s Ark
- 1994: Operation Body Count
- 1994: Blake Stone: Planet Strike
- 1994: Rise of the Triad

Raycasting allowed for a pseudo-3D effect. All logic is performed in a 2D grid where rays are cast from the position of the player to detect objects. If the ray detects an object, it will be rendered in a 3D view to the player. This is also why the player can move forwards, backwards, left, and right, but not up or down: the Wolfenstein map is all flat.

The raycaster engine was one of, if not the fastest 3D rendering engine at the time and allowed high-paced action games to be played on PCs intended for processing word documents.

[Play Wolfenstein 3D](https://playclassic.games/games/first-person-shooter-dos-games-online/play-wolfenstein-3d-online/play/)


<div align="center">
  <a href="Images\Wolf3d_pc.png" target="_blank">
    <img src="Images\Wolf3d_pc.png" style="height:400px;"/>
  </a>
</div>
<div align="center">
  <a href="https://en.wikipedia.org/wiki/Wolfenstein_3D">
  Source
  </a>
</div>
<br>

## Summary
- Get familiar with Pygame
- Create a Raycaster engine
- Profile using SnakeViz
- Attempt optimisation

## Tutorial
I recommend you use VS Code for this tutorial and for any time we use Python. You can use IDLE if you want, but you will miss out on the builtin terminal, which we'll use later when we profile, and in-editor error checking. On the University machines the program might just be called 'Code'. For today, create a python file and save it in the same location as the README.md file.

### Step 1 - Pygame Boilerplate
Start with the standard boilerplate for Pygame. Running this will shown a black screen with a height half its width. We define the standard Pygame code to create a window and create a main() function that resembles the Update() function of our Unity projects. We set the FPS to be locked at 60 (increase if you want). There's also code for terminating the script on pressing Esc or actually closing the window by pressing the X button.

```
import pygame

WIDTH = 1000
HEIGHT = WIDTH / 2

pygame.init()
clock = pygame.time.Clock()
# creates window 
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SCALED, vsync=1)
pygame.display.set_caption("Raycast Engine")

# closes the program 
def close(): 
    pygame.quit()

def main():
    running = True
    while running:
        # check for pressing Esc or closing the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Updating display
        pygame.display.flip()
        clock.tick(60) / 1000  # amount of seconds between each loop

    close()

main()
```

<div align="center">
  <a href="Images\01.png" target="_blank">
    <img src="Images\01.png" style="height:400px;"/>
  </a>
</div>

Notice how we also set the display to have VSYNC enabled. This is a setting that can also be set in Unity. VSYNC, short for Vertical Synchronization, ensures that the frame has completed rendering before displaying it to the user. Without this, parts of the frame can be rendered before the entire frame is ready, causing this effect: 

<div align="center">
  <a href="Images\screentearing.gif" target="_blank">
    <img src="Images\screentearing.gif" style="height:400px;"/>
  </a>
</div>

### Step 2 - Adding a 2D Map
Remember, for a raycaster engine, nearly all the logic is 2D! So we define a 2D map made of ones and zeroes (one = wall, zero = no wall). We'll use numpy to make an array of these values so its easy to make logic that can reference the map.

So add `import numpy as np` to the top of your code. And add a map to your global variables, use this one for now as its sufficient for testing and we'll implement a mapmaker right at the end of this so you can easily modify it:

```
WIDTH = 1000
HEIGHT = WIDTH / 2
MAP = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
TILE_SIZE = 50      # the size of a single tile
MAP_SIZE = len(MAP) # = 10
```

Next, we need a function that can actually draw this map as a 2D grid and display it to us. This is purely for development purposes. We can remove it at the end of this tutorial.

The first part will loop over the rows in MAP, returning the row each time, plus by using the enumerate function, the index of the row (y) also. This is useful as we'll need the index later.

```
# draw the 2d map
def draw_map():
    for y, row in enumerate(MAP):
...
```

We also need to loop over every cell in that row. Using enumerate we can, again, get the index value that we can use later:

```
# draw the 2d map
def draw_map():
    for y, row in enumerate(MAP):
            for x, cell in enumerate(row):
...
```

So far we have the code to loop over every row and every cell in each row. Let's actually do something with that info. If the cell is a 0, then set its colour to white (255, 255, 255), else it must be a 1, so set its colour to black (0, 0, 0):

```
# draw the 2d map
def draw_map():
    for y, row in enumerate(MAP):
            for x, cell in enumerate(row):
                colour = (255, 255, 255) if cell == 0 else (0, 0, 0)
...
```

Now we know what colour to make the cell, we'll draw it using pygame.draw.rect. See if you can figure out this logic yourself, please ask if you want clarification.

```
# draw the 2d map
def draw_map():
    for y, row in enumerate(MAP):
            for x, cell in enumerate(row):
                colour = (255, 255, 255) if cell == 0 else (0, 0, 0)
                pygame.draw.rect(screen, colour, pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
...
```

Finally, we'll add some rectanges of width 1 around each tile to create a gridlines effect.

```
# draw the 2d map
def draw_map():
    for y, row in enumerate(MAP):
            for x, cell in enumerate(row):
                colour = (255, 255, 255) if cell == 0 else (0, 0, 0)
                pygame.draw.rect(screen, colour, pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
```

The latest code above is our completed draw_map function. Add it just before your def `main()` function definition and run to see the results.

We defined the width of the window (WIDTH) as 1000 and defined the tile size (TILE_SIZE) as 50. The MAP_SIZE takes the number of values in a row, which is 10. This means the total size of the grid we will display is 50*10, which is 500 and exactly half of the total width. Therefore, our grid will take up one half of the window (like in the image below).

<div align="center">
  <a href="Images\02.png" target="_blank">
    <img src="Images\02.png" style="height:400px;"/>
  </a>
</div>

### Step 3 - Adding a Player
We must define some variables that will hold some information on the player. These are the coordinates of the player, the angle the player is facing, and the speed it travels at. The angle of our player will work in radians, not degrees. This means that `math.sin(pi)` will result in a starting angle of 0. Because we're using Python's 'math' functions, we need to add `import math` to the top of the code.

<div align="center">
  <a href="Images\radians.gif" target="_blank">
    <img src="Images\radians.gif" style="height:400PX;"/>
  </a>
</div>
<div align="center">
  Angle is on the left of each section, radians is on the right (180, Pi)
  <a href="https://www.math.csi.cuny.edu/~ikofman/Polking/drg_txt.html">
  (Source)
  </a>
</div>
<br>

```
player_x = 100
player_y = 100
player_angle = math.pi
player_speed = 4
```

Next we need some logic for drawing the player to the screen. We are still working on developing our grid (the left half of our window), so let's put this next code in our draw_map function:

```
# draw player on 2D board
pygame.draw.circle(screen, (255, 0, 0), (int(player_x), int(player_y)), 8)

# draw player direction
pygame.draw.line(screen, (0, 255, 0),   # draw line in green colour
                  (player_x, player_y),  # set its position to match the player
                  (player_x - math.sin(player_angle) * 50,       # calc the x position of the end of the line 
                  player_y + math.cos(player_angle) * 50), 4)   # calc the y position of the end of the line
```

The code above draws a red circle at the position we defined earlier with a size of 8. It also draws a green line that begins at the coordinates of the player and uses some theory on circles so we can calculate the end point of the line that all matches the player's angle (player_angle) with a width of 4.

<div align="center">
  <a href="Images\03_still.png" target="_blank">
    <img src="Images\03_still.png" style="height:400px;"/>
  </a>
</div>

We need to be able to move our player. We can get the user's input from the WASD or arrow keys and change the angle if they rotate the player or change the players position if they move the player forwards or backwards. Moving forward takes the current player position and then moves them in the direction of the current angle by calculating the correct x and y coordinates of the player. Put this code after calling the draw_map function in our main function.

```
# get user input
keys = pygame.key.get_pressed()
# handle user input
if keys[pygame.K_LEFT] or keys[pygame.K_a]: player_angle -= 0.1
if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player_angle += 0.1
if keys[pygame.K_UP] or keys[pygame.K_w]:
    player_x += -math.sin(player_angle) * player_speed
    player_y += math.cos(player_angle) * player_speed
if keys[pygame.K_DOWN] or keys[pygame.K_s]:
    player_x -= -math.sin(player_angle) * player_speed
    player_y -= math.cos(player_angle) * player_speed
```

You also need to remind Python that these are global variables, so add the following to the top of the main() function:

```
    global player_angle
    global player_x
    global player_y
```

We have no collision detection implemented yet, so we know it's possible to go through walls, but something unusual is that we can make some trippy patterns by moving outside of the 2D grid...

<div align="center">
  <a href="Images\03_no_fill.png" target="_blank">
    <img src="Images\03_no_fill.png" style="height:400px;"/>
  </a>
</div>

We can fix this by filling the screen with a colour before every frame, meaning we stop rendering on top of previous renders. Define a variable called BACKGROUND_COLOUR and set it to whatever you want (example: `BACKGROUND_COLOUR = (8,32,64)`). Add this next code before calling the draw_map function in the main function:

```
# clear the screen
screen.fill(BACKGROUND_COLOUR)  
```

### Part 4 - Adding FOV
We need to define the minimum and maxium angle that we'll shoot raycasts between. This will define our FOV.

Create a new variable called FOV and set it to `math.pi / 3`. PI/3 equals 1.047 radians. We can convert from radians to degrees like this:

$$1.047 \, \text{Rad} \times \frac{180}{\pi} = 60^\circ$$

Meaning we have an FOV of 60 degrees.

Also add `HALF_FOV = FOV / 2`, so we have a variable storing half of this value in radians too.

Add the next code into the draw_map function. This will draw two additional green lines to the left and right of the player with an angle of 60 degrees seperating them. This logic is very similar to the logic for drawing the green line in front of the player, except we just subtract or add the angle by HALF_FOV so that they're shifted from the forward/centre angle.

```
# draw player FOV
pygame.draw.line(screen, (0, 255, 0), (player_x, player_y),
                                    (player_x - math.sin(player_angle - HALF_FOV) * 50,
                                    player_y + math.cos(player_angle - HALF_FOV) * 50), 3)

pygame.draw.line(screen, (0, 255, 0), (player_x, player_y),
                                    (player_x - math.sin(player_angle + HALF_FOV) * 50,
                                    player_y + math.cos(player_angle + HALF_FOV) * 50), 3)
```

<div align="center">
  <a href="Images\04.png" target="_blank">
    <img src="Images\04.png" style="height:400px;"/>
  </a>
</div>

### Part 5 - Raycasting!
Now the part where we actually raycast to detect which planes should be drawn in our 3D render. This part is a little tricky; I had to go through it a few times to fully understand its logic, so have a read first then please ask for clarification and I'll do my best to help. 

First, let's define some new variables. We need a variable to hold the number of rays we want to cast (N_RAYS), a variable to hold the angle between each ray (STEP_ANGLE) so we know how much to shift the angle of each ray by each time to cover the full 60 degrees, and a variable to store the maximum distance we should draw our ray based on the length of the map (purely as an optimisation technique, more detail is coming up on this shortly).

```
N_RAYS = 100
STEP_ANGLE = FOV / N_RAYS
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
```

Next, a new function called cast_rays that will run our raycasting logic. Sorry this is a long one:

We start off by setting the start_angle to the leftmost angle of the player's FOV.

```
# raycasting algorithm
def cast_rays():
    # define left most angle of FOV
    start_angle = player_angle - HALF_FOV
...
```

Next, we loop over the total number of rays we want to cast. 

```
# raycasting algorithm
def cast_rays():
    # define left most angle of FOV
    start_angle = player_angle - HALF_FOV
    # loop over the number of rays
    for ray in range(N_RAYS):
...
```

Then use a nested loop to check the distance each ray travels until it hits a wall or until it reaches the value of `MAX_DEPTH`.

```
# raycasting algorithm
def cast_rays():
    # define left most angle of FOV
    start_angle = player_angle - HALF_FOV
    # loop over the number of rays
    for ray in range(N_RAYS):
        # cast ray step by step
        for depth in range(MAX_DEPTH):
...
```

`target_x` and `target_y` are then needed to hold the coordinates of the end point of the ray. Think of the ray extending a tiny amount each time this loop runs until it hits something or reaches `MAX_DEPTH`. We can round these two variables to give us the equivalent indeces of the column (`col`) and row (`row`) in our grid.

```
...
        # cast ray step by step
        for depth in range(MAX_DEPTH):
            # get ray target coordinates
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth

            # covert target X, Y coordinate to map col, row
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)
...
```

Then we can check if the end point in our ray is within the map boundaries. This is to check if the column and row actually exists in our map. It could be outside of our map, which would cause an error later when we check what is at those coordinates, because if it's not within our map then the coorindates won't exist and we won't be able to check if there is a zero or one at that coordinate.

```
...
        # cast ray step by step
        for depth in range(MAX_DEPTH):
            # get ray target coordinates
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth
            
            # covert target X, Y coordinate to map col, row
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)

            # check if ray is within map boundaries
            if 0 <= col < MAP_SIZE and 0 <= row < MAP_SIZE:
...
```

Next, we'll check the value in our 2D map at that position.

```
            # check if ray is within map boundaries
            if 0 <= col < MAP_SIZE and 0 <= row < MAP_SIZE:
                # calculate map square index
                square = MAP[row][col]
...
```

And if the value of `square` is a 1, then we know we have hit a wall and we can draw a green rectangle over that coordinate to highlight that we have hit it, draw the full ray as a yellow line to the display, and finally use `break` to break out from the nested loop (`for depth in range(MAX_DEPTH)`) and then, finally, `start_angle` is incrementing by the value of `STEP_ANGLE` and this whole process repeats until all the rays have been cast.

```
...
            # check if ray is within map boundaries
            if 0 <= col < MAP_SIZE and 0 <= row < MAP_SIZE:
                # calculate map square index
                square = MAP[row][col]

                # ray hits the condition
                if square == 1:
                    # highlight wall that has been hit by a casted ray
                    pygame.draw.rect(screen, (0, 255, 0), (col * TILE_SIZE,
                                                        row * TILE_SIZE,
                                                        TILE_SIZE - 2,
                                                        TILE_SIZE - 2))

                    # draw casted ray
                    pygame.draw.line(screen, (255, 255, 0), (player_x, player_y), (target_x, target_y))
                    break

        # increment angle by a single step
        start_angle += STEP_ANGLE
```

This is the raycasting algorithm completed. Be sure to call it by placing the following after `draw_map()`:

```
        # cast rays
        cast_rays()
```

Your game view should look like this:

<div align="center">
  <a href="Images\05.png" target="_blank">
    <img src="Images\05.png" style="height:400px;"/>
  </a>
</div>

If we reduce the number of N_RAYS, we reduce the amount of times the main loop in cast_rays runs for, optimising our loop. A number too low however, will result in walls being missed:

<div align="center">
  <a href="Images\05_12_rays_only.png" target="_blank">
    <img src="Images\05_12_rays_only.png" style="height:400px;"/>
  </a>
</div>

We can optimise by reducing MAX_DEPTH, which holds the value of the longest a ray should ever need to be cast at. This is equivalent to the width of the map. Technically, the longest distance that could be draw is between two diagonals of the map, you could work out the hypotenuse from the width and height of the map to find this, but our system is good enough for now. Our system means each ray checks if it is colliding with a wall but only up to the value of `MAX_depth`, so if it never hits a wall within this distance then it doesn't continue checking forever. Like in the image below, you can position the player at a distance greater than the length of the map to see rays stop being cast when their length is greater than `MAX_DEPTH`. Reducing the MAX_DEPTH to something quite short would be an example of frustum culling (like we discussed games like Silent Hill did but were able to hide this technique from the player by adding fog).

<div align="center">
  <a href="Images\05_max_depth.png" target="_blank">
    <img src="Images\05_max_depth.png" style="height:400px;"/>
  </a>
</div>

### Part 6 - 3D Rendering
All our 2D logic is done and we have identified the walls the player will be able to see using the raycastings algorith, so let's translate that information into a 3D render.

We first need a new variable called `SCALE`. Set its value to 5. This will provide the appropriate scaling our render to the screen.

After drawing the yellow rast cast line inside our `cast_rays` function and when a wall is hit, we can draw walls. Our code defines a new colour (0, black) for the wall, calculates the wall height (`wall_height`) by taking a value and dividing it by the current depth of the ray. A larger depth means the ray end point is further away and that we should draw a shorter rectangle compared to when we have a smaller depth value, for example:

If the wall is 20,000 pixels away, the wall with have a height of 1.

If the wall is 1 pixel away, the wall will have a height of 20,000.

You can change the number from 20,000 to change the height of the walls, but this value makes the walls quite realistically sized based on the player's speed (try a value of 2,000 or something higher to see what I mean). We also add `0.0001`, just to avoid a division by zero which can make the game crash.

We then ensure the height of the wall never exceeds the height of the screen by capping `wall_height` at `HEIGHT` (the window height) if it is greater than `HEIGHT`.

Finally, we draw the 3D projection by drawing a rectangle by taking the number of the current ray (`ray`) and multiplying it by the scale (+ the height so the 3D render is displayed on the right side of the screen) to get the x-coordinate of the top-left corner of the rectangle, halving the wall height then subtracting half the wall height to determine the y_coordinate of the top-left corner of the rectangle, then setting the width as the scale, and the height as the wall height.

```
                # ray hits the condition
                if square == 1:
                    # highlight wall that has been hit by a casted ray
                    pygame.draw.rect(screen, (0, 255, 0), (col * TILE_SIZE,
                                                        row * TILE_SIZE,
                                                        TILE_SIZE - 2,
                                                        TILE_SIZE - 2))

                    # draw casted ray
                    pygame.draw.line(screen, (255, 255, 0), (player_x, player_y), (target_x, target_y))
                    
                    colour = 0
                                    
                    # calculate wall height
                    wall_height = 20000 / (depth + 0.0001)
                    
                    # ensure height of the wall never exceeds the height of the screen
                    if wall_height > HEIGHT: wall_height = HEIGHT 
                    
                    # draw a rectangle at this ray's position
                    pygame.draw.rect(screen, (colour, colour, colour), (
                        HEIGHT + ray * SCALE, # x-coordinate of the top-left corner of the rectangle
                        (HEIGHT / 2) - wall_height / 2, # y_coordinate of the top-left corner of the rectangle
                        SCALE,  # width of the rectangle
                        wall_height))   # height of the rectangle
                    
                    break
```

If it wasn't already clear, we don't draw a rectangle the size of each wall, we draw sections of each wall as tall and thin rectangles. To see the rectangles drawn, you can add lines between each rectangle like this:

```
                    # draw a vertical line between each rectangle
                    pygame.draw.line(screen, (24, 128, 24), 
                                    (HEIGHT + ray * SCALE, 0), 
                                    (HEIGHT + ray * SCALE, HEIGHT), 
                                    1)
```

You might notice this fish-eye effect. This can be corrected by adjusting the depth based on the angle of the ray relative to the player’s direction. The fish-eye effect occurs because rays at the edge of the field of view travel a greater distance than rays in the center. We can remove it with a single line of code and we can make the walls more interesting, by changing the colour of them based on depth.

```
                    # auto colour
                    colour = 255 / (1 + depth * depth * 0.0001)
                
                    # fix fish eye effect
                    depth *= math.cos(player_angle - start_angle)
```

<details>
<summary>How does the fix fish eye effect code work?</summary>
In a raycasting engine, rays are cast from the player’s position in a fan-like pattern to sample the environment. The distance from the player to the wall hit by each ray is used to calculate the height of the wall slice in the 3D projection. However, this distance is not always the true perpendicular distance to the wall. For rays cast at an angle to the player’s direction (i.e., rays towards the edges of the field of view), the distance to the wall is greater than the perpendicular distance. This results in wall slices towards the edges of the screen being drawn taller than they should be, creating a distortion known as the “fish eye” effect.
<br><br>
The line `depth *= math.cos(player_angle - start_angle)` corrects this distortion. The expression `math.cos(player_angle - start_angle)` calculates the cosine of the difference between the angle of the ray and the player’s direction. This value is a scaling factor that decreases from 1 to 0 as the angle increases from 0 to 90 degrees. When this scaling factor is multiplied with the distance to the wall (depth), it effectively reduces the distance for rays cast at an angle, bringing it closer to the true perpendicular distance. This corrects the height of the wall slices towards the edges of the screen, removing the fish-eye effect.
</details>

<div align="center">
  <a href="Images\06.png" target="_blank">
    <img src="Images\06.png" style="height:400px;"/>
  </a>
</div>

### Part 7 - Collision Detection
We can set our player's coordinates to only update when we the coordinates of where we want to travel to is a cell that is a 0/not a wall:

```
        # get user input
        keys = pygame.key.get_pressed()
        # handle user input
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: player_angle -= 0.1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player_angle += 0.1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_player_x = player_x + -math.sin(player_angle) * player_speed
            new_player_y = player_y + math.cos(player_angle) * player_speed
            if MAP[int(new_player_y / TILE_SIZE)][int(new_player_x / TILE_SIZE)] == 0:
                player_x = new_player_x
                player_y = new_player_y
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_player_x = player_x - -math.sin(player_angle) * player_speed
            new_player_y = player_y - math.cos(player_angle) * player_speed
            if MAP[int(new_player_y / TILE_SIZE)][int(new_player_x / TILE_SIZE)] == 0:
                player_x = new_player_x
                player_y = new_player_y
```

Our player will not move at all though even if we're slightly facing a wall. An improved version would be to allow the player to slide along the wall. We can check if there's a wall  separately for both the x and y coordinates. This means that if the player’s new position is inside a wall in one direction but not the other, the player’s position will still be updated in the direction where there’s no wall. This allows the player to slide along walls instead of stopping completely:

```
        # get user input
        keys = pygame.key.get_pressed()
        # handle user input
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: player_angle -= 0.1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player_angle += 0.1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_player_x = player_x + -math.sin(player_angle) * player_speed
            new_player_y = player_y + math.cos(player_angle) * player_speed
            if MAP[int(player_y / TILE_SIZE)][int(new_player_x / TILE_SIZE)] == 0:
                player_x = new_player_x
            if MAP[int(new_player_y / TILE_SIZE)][int(player_x / TILE_SIZE)] == 0:
                player_y = new_player_y
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_player_x = player_x - -math.sin(player_angle) * player_speed
            new_player_y = player_y - math.cos(player_angle) * player_speed
            if MAP[int(player_y / TILE_SIZE)][int(new_player_x / TILE_SIZE)] == 0:
                player_x = new_player_x
            if MAP[int(new_player_y / TILE_SIZE)][int(player_x / TILE_SIZE)] == 0:
                player_y = new_player_y
```

### Part 8 - Removing the 2D View
To remove the 2D view and have the 3D render in full-screen, comment out the draw_map function call and comment out the code for highlighting hit walls and drawing the caster rays in the cast_rays function. Also remove the shift that moves the position of drawing the walls to the right side of the screen by removing the `HEIGHT` variable so your code now looks like this:

```
pygame.draw.rect(screen, (color, color, color), (
                        ray * SCALE,
                        (HEIGHT / 2) - wall_height / 2,
                        SCALE, wall_height))
```

<div align="center">
  <a href="Images\08.png" target="_blank">
    <img src="Images\08.png" style="height:400px;"/>
  </a>
</div>

### Part 9 - Adding a Map Editor
Our map is only 10 x 10. Wolfenstein 3D used a much larger map. I have made a map editor for you. Open map_editor.py and run the script. Save the default map for now and press save. Swap the `MAP` variable with `MAP = np.loadtxt("map.csv", dtype=int)` to load the csv. Test your game. This should run badly; the raycaster engine is specifically designed for corridors and small rooms. Define your own map and you will see performance is better in places where only a few walls have to be rendered as opposed to many like you'd get in an open space.

## Profiling
### FPS Counter
I have provided a script for an FPS counter called fps.py. Ensure it is in the same directory as your raycaster engine. Implementing the contents of fps.py to your script is fairly easy.

- At the top of your script add: `from fps import FPS`
- After defining the `clock` add an FPS object with: `fps = FPS(clock)`
- Just before updating the display in the main loop add: `fps.render(screen)`

<div align="center">
  <a href="Images\FPS.png" target="_blank">
    <img src="Images\FPS.png" style="height:400px;"/>
  </a>
</div>

### SnakeViz
SnakeViz is a Python profiler with handy visualisation tools. It's not as sophisticated as the Unity Profiler, but it's an ok equivalent.

Open the Terminal with "Ctrl" + "'" (typically the key with the @ symbol on or the key below the escape key) and paste in `pip install snakeviz` then press enter.

Alternatively, you can open the Anaconda Prompt program. Paste in `pip install snakeviz` and press enter to install SnakeViz.

Then, like in the screenshot below, ensure your terminal or Anaconda Prompt is in the current directory containing your Python file. Use `cd <full file path to the folder containing your python file>` to navigate the terminal there if it isn't already. And paste in `python -m cProfile -o raycaster.prof .\<name of your python file>`, make sure to replace `<name of your python file>` with your file (mine is called 10_no_2d.py). Pressing enter will use Python's inbuilt cProfile module and export the output to a file name `raycaster.prof`. Paste in `snakeviz .\raycaster.prof` and press enter. This will open the browser and display the results of the profile using SnakeViz.

If this is all a bit confusing at first, try profiling the file `profiling_example.py` first using SnakeViz to more easily understand what information you're shown.

<div align="center">
  <a href="Images\SnakeViz Terminal.png" target="_blank">
    <img src="Images\SnakeViz Terminal.png" style="height:200px;"/>
  </a>
</div>

Experiment with the options to understand what it is capable of.

<div align="center">
  <a href="Images\SnakeViz Icicle.png" target="_blank">
    <img src="Images\SnakeViz Icicle.png" style="height:400px;"/>
  </a>
</div>

<div align="center">
  <a href="Images\SnakeViz Sunburst.png" target="_blank">
    <img src="Images\SnakeViz Sunburst.png" style="height:400px;"/>
  </a>
</div>

### Optimization Task
For your assessment, you will be tasked with optimising a Pygame particles simulator. To get some practice for this, see about how you can optimise the raycasting algorithm (the ray_casts function). This doesn't mean optimising by using whatever quick Python hacks exists, but optimising by improving the logic so we get the same results but more efficiently. Try yourself and ask if you'd like me to tell you the solution (it will still be up to you to figure out how to implement it!).

## Extra Resources
### Cool Raycaster Examples
- [Pretty Raycaster Demo](https://www.reddit.com/r/pygame/comments/jjmb7f/i_have_been_working_on_a_ray_caster_engine_in/)
- [Super Mario Bros. in Python Pygame Raycaster](https://www.youtube.com/watch?v=NXhRi8UgzZk)


### Raycaster Tutorials
- [Pygame Raycaster with Textiles and Sprites](https://www.youtube.com/watch?v=ECqUrT7IdqQ&t=767s)
- [Killer Robotics Blog on Pygame Raycaster with Sprites and Textiles](https://killerrobotics.me/2021/08/13/raycasting-game-in-python-and-pygame-part-1/)
- [C++ OpenGL Raycaster Tutorial](https://www.youtube.com/watch?v=gYRrGTC7GtA&t=244s)
- [Code Monkey King/GitHub maksimKorzh Pygame Raycaster](https://github.com/maksimKorzh/raycasting-tutorials/tree/main/tutorial)
- [GitHub ChristianD376 Pygame Raycaster](https://github.com/ChristianD37/Pygame-Raycaster/tree/master)

### SnakeViz
- [SnakeViz Tutorial](https://www.youtube.com/watch?v=qhb7cehwChc)
