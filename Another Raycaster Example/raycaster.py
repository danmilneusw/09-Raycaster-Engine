import math
import pygame
from settings import *

# Closes the program 
def close(): 
    pygame.display.quit()
    pygame.quit()

def main():
    global positionX
    global positionY
    global directionX
    global directionY
    global showShadow

    pygame.init()

    clock = pygame.time.Clock()

    # Creates window 
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SCALED, vsync=1)
    pygame.display.set_caption("Raycast Engine")

    planeX = 0.0
    planeY = 0.5

    # Trigeometric tuples + variables for index
    TGM = (math.cos(ROTATIONSPEED), math.sin(ROTATIONSPEED))
    ITGM = (math.cos(-ROTATIONSPEED), math.sin(-ROTATIONSPEED))
    COS, SIN = (0,1)
    
    while True:
        keys=pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            close()

        if keys[pygame.K_a]:
            oldDirectionX = directionX
            directionX = directionX * ITGM[COS] - directionY * ITGM[SIN]
            directionY = oldDirectionX * ITGM[SIN] + directionY * ITGM[COS]
            oldPlaneX = planeX
            planeX = planeX * ITGM[COS] - planeY * ITGM[SIN]
            planeY = oldPlaneX * ITGM[SIN] + planeY * ITGM[COS]

        if keys[pygame.K_d]:
            oldDirectionX = directionX
            directionX = directionX * TGM[COS] - directionY * TGM[SIN]
            directionY = oldDirectionX * TGM[SIN] + directionY * TGM[COS]
            oldPlaneX = planeX
            planeX = planeX * TGM[COS] - planeY * TGM[SIN]
            planeY = oldPlaneX * TGM[SIN] + planeY * TGM[COS]    

        if keys[pygame.K_w]:
            if not map[int(positionX + directionX * MOVESPEED)][int(positionY)]:
                positionX += directionX * MOVESPEED
            if not map[int(positionX)][int(positionY + directionY * MOVESPEED)]:
                positionY += directionY * MOVESPEED
                
        if keys[pygame.K_s]:
            if not map[int(positionX - directionX * MOVESPEED)][int(positionY)]:
                positionX -= directionX * MOVESPEED
            if not map[int(positionX)][int(positionY - directionY * MOVESPEED)]:
                positionY -= directionY * MOVESPEED

        if keys[pygame.K_1]:
            showShadow = True
        if keys[pygame.K_2]:
            showShadow = False
            
        # Draws roof and floor
        screen.fill((200,200,200))
        pygame.draw.rect(screen, (70,70,70), (0, HEIGHT/2, WIDTH, HEIGHT/2)) 
                
        # Starts drawing level from 0 to < WIDTH 
        column = 0        
        while column < WIDTH:
            cameraX = 2.0 * column / WIDTH - 1.0
            rayPositionX = positionX
            rayPositionY = positionY
            rayDirectionX = directionX + planeX * cameraX
            rayDirectionY = directionY + planeY * cameraX + .000000000000001 # avoid zero division 

            # In what square is the ray?
            mapX = int(rayPositionX)
            mapY = int(rayPositionY)

            # Delta distance calculation
            # Delta = square ( raydir * raydir) / (raydir * raydir)
            deltaDistanceX = math.sqrt(1.0 + (rayDirectionY * rayDirectionY) / (rayDirectionX * rayDirectionX))
            deltaDistanceY = math.sqrt(1.0 + (rayDirectionX * rayDirectionX) / (rayDirectionY * rayDirectionY))

            # We need sideDistanceX and Y for distance calculation. Checks quadrant
            if (rayDirectionX < 0):
                stepX = -1
                sideDistanceX = (rayPositionX - mapX) * deltaDistanceX

            else:
                stepX = 1
                sideDistanceX = (mapX + 1.0 - rayPositionX) * deltaDistanceX

            if (rayDirectionY < 0):
                stepY = -1
                sideDistanceY = (rayPositionY - mapY) * deltaDistanceY

            else:
                stepY = 1
                sideDistanceY = (mapY + 1.0 - rayPositionY) * deltaDistanceY

            # Finding distance to a wall
            hit = 0
            while  (hit == 0):
                if (sideDistanceX < sideDistanceY):
                    sideDistanceX += deltaDistanceX
                    mapX += stepX
                    side = 0
                    
                else:
                    sideDistanceY += deltaDistanceY
                    mapY += stepY
                    side = 1
                    
                if (map[mapX][mapY] > 0):
                    hit = 1

            # Correction against fish eye effect
            if (side == 0):
                perpWallDistance = abs((mapX - rayPositionX + ( 1.0 - stepX ) / 2.0) / rayDirectionX)
            else:
                perpWallDistance = abs((mapY - rayPositionY + ( 1.0 - stepY ) / 2.0) / rayDirectionY)

            # Calculating HEIGHT of the line to draw
            lineHEIGHT = abs(int(HEIGHT / (perpWallDistance+.0000001)))
            drawStart = -lineHEIGHT / 2.0 + HEIGHT / 2.0

            # if drawStat < 0 it would draw outside the screen
            if (drawStart < 0): drawStart = 0

            drawEnd = lineHEIGHT / 2.0 + HEIGHT / 2.0

            if (drawEnd >= HEIGHT): drawEnd = HEIGHT - 1

            # Wall colors 0 to 3
            wallcolors = [ [], [20,20,20], [50,50,50], [120,120,120] ]
            color = wallcolors[ map[mapX][mapY] ]

            # Apply shadow
            # if side == 1 then tone the color down
            if showShadow:
                if side == 1:
                    for i,v in enumerate(color):
                        color[i] = int(v / 2)

            # Drawing the graphics
            pygame.draw.line(screen, color, (column,drawStart), (column, drawEnd), 2)
            column += 2

        # Updating display
        pygame.event.pump()
        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Amount of seconds between each loop
main()