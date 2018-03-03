import pygame
import time
from random import randint

pygame.init()

black = (0,0,0)
white = (255,255,255)
surfaceWidth = 1000 
surfaceHeight = 700
imgback = pygame.image.load('grass.jpg')
imgx = 0
imgy = 0


surface = pygame.display.set_mode((surfaceWidth,surfaceHeight))
pygame.display.set_caption('Bulbasaur')
clock = pygame.time.Clock()

'''
Restart or Quit Logic
'''
def replay_or_quit():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            continue

        return event.key
    
    return None

''' 
Return Text Area
'''
def makeTextObjs(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

'''
Add Game Over Message and restart logic
'''
def msgSurface(text):
    smallText = pygame.font.Font('freesansbold.ttf', 20)
    largeText = pygame.font.Font('freesansbold.ttf', 150)

    titleTextSurf, titleTextRect = makeTextObjs(text, largeText)
    titleTextRect.center = surfaceWidth / 2, surfaceHeight / 2
    surface.blit(titleTextSurf, titleTextRect)

    typTextSurf, typTextRect = makeTextObjs('Press any key to continue', smallText)
    typTextRect.center =  surfaceWidth / 2, ((surfaceHeight / 2) + 100)
    surface.blit(typTextSurf, typTextRect)

    pygame.display.update()
    time.sleep(1)

    while replay_or_quit() == None:
        clock.tick()

    main()


def gameOver():
    msgSurface('Kaboom!')
    
def icon(x, y, image):
    surface.blit(image, (x,y))

def main():

    imageHeight = 192
    imageWidth = 192
    
    # Load Player into memory
    img = pygame.image.load('Bulbasaur.png')
    img = pygame.transform.scale(img,(imageHeight,imageWidth))
    
    # Load Evolved Player into memory
    img2 = pygame.image.load('Ivysaur.png')
    img2 = pygame.transform.scale(img2,(imageHeight+64,imageWidth+64))
    
    # Load Enemy into memory
    chal = pygame.image.load('Charmander.png')
    chal = pygame.transform.scale(chal,(imageHeight,imageWidth))
    
    # Load bullet
    bulletpicture = pygame.image.load("topbullet.gif")
        
    # Inital Game state
    current_score = 0
    game_over = False     
    
    # Inital settings
    x = 150
    y = 200
    y_move = 0
    chalx = surfaceWidth
    chaly = randint(0,(surfaceHeight/2))
    pokespeed = 10

    # Game Loop
    while not game_over:
                       
        # Capture player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_move = -20
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    y_move = 10
                    

        # Add Background
        surface.blit(imgback, (imgx,imgy))
        
        # Set new y coord based on user input
        y += y_move
        # Add player icon
        icon(x ,y, img)
        
        # Add enemy
        surface.blit(chal, (chalx,chaly))
        # Move enemy by adjusting x coordinates
        chalx -= pokespeed
        
        # Set Upper & Lower boundaries
        if y > surfaceHeight or y < 0:
            gameOver()
            
        # Debugging Logging
        print('y=' + str(y))     
        print('chaly=' + str(chaly))    
        
        # Logic to respawn enemy when last enemy flys off screen
        if chalx < (10):
            chalx = surfaceWidth
            chaly = randint(0, (surfaceHeight-imageHeight))
        	
        # Logic for player + enemy collision                                                                                                                                                                        if x >= chalx:
            print('x crossover')
            if y >= chaly - (imageHeight/2) and y <= chaly + (imageHeight/2):
                print('boom!')
                gameOver()

        # Update the screen with new settings
        pygame.display.update()
        clock.tick(60)

main()
pygame.quit()
quit()















    
