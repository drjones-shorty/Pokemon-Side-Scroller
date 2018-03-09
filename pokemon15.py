import pygame
import time
from random import randint
import sys, pygame.mixer
from pygame.locals import *

# Game Constants
black = (0,0,0)
white = (255,255,255)
surfaceWidth = 1000 
surfaceHeight = 700
    
pygame.init()
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

def score(count):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render("Score: "+str(count), True, black)
    surface.blit(text, [10,10])    


def lives(lcount):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render("Lives: "+str(lcount), True, black)
    surface.blit(text, [surfaceWidth-100,10])    

def die(explode, x,y):
    surface.blit(explode, (x,y))
    pygame.display.update()
    time.sleep(1)
    clock.tick()
    
def gameOver():
    msgSurface('Game Over')
    
def icon(x, y, image):
    surface.blit(image, (x,y))

def main():

	# Load Configs
    imgBackX = 0
    imgBackY = 0
    imageHeight = 192
    imageWidth = 192
    evolvedHeight = imageHeight+64
    evolvedWidth = imageWidth+64
    iconXreset = 50
    iconYreset = 200
    offscreenX = surfaceWidth + 100
    rightEdge = surfaceWidth - 100
    leftEdge = 10
    bottomEdge = surfaceHeight - 10
    topEdge = -50
    maxScreenBullets = 5
    moveRateFast = 30
    moveRateMed = 20
    moveRateSlow = 10
    evolveStage2Score = 30
    scoreIncr = 1
    scoreIncrMed = 5
    scoreIncrHigh = 10
    ememySpeedUpRate = 1
    

    # Load background   
    imgBack = pygame.image.load('sky.gif')
   
    # Load Player into memory
    hero = pygame.image.load('Bulbasaur.png')
    hero = pygame.transform.scale(hero,(imageWidth,imageHeight))
    
    # Load Evolved Player into memory
    img2 = pygame.image.load('Ivysaur.png')
    img2 = pygame.transform.scale(img2,(evolvedWidth,evolvedHeight))
    
    # Load Enemy into memory
    chal = pygame.image.load('Charmander.png')
    chal = pygame.transform.scale(chal,(imageWidth,imageHeight))

    # Load Evolved Enemy into memory
    evolvedChal = pygame.image.load('Charizard.png')
    evolvedChal = pygame.transform.scale(evolvedChal,(evolvedWidth,evolvedHeight))
    
    # Load bullet
    bulletpicture = pygame.image.load("topbullet.gif")
    bulletpicture = pygame.transform.scale(bulletpicture,(50,50))
    
    # Load apple
    apple = pygame.image.load("apple.png")
    apple = pygame.transform.scale(apple,(128,128))

    # Load dead Player into memory
    explode = pygame.image.load('boom.png')
    explode = pygame.transform.scale(explode,(evolvedWidth,evolvedHeight))    

    # Load mountains into memory
    mountaintop = pygame.image.load('mountaintop.png')    

        
    # Inital Game state
    current_score = 0
    current_lives = 3
    game_over = False
    apple_on = False     
    
    # Inital settings
    x = iconXreset
    y = iconYreset
    chalx = surfaceWidth
    chaly = randint(0,(surfaceHeight/2))
    applex = surfaceWidth
    appley = randint(0,(surfaceHeight/2))    
    y_move = 0
    x_move = 0
    bullets=[]
    pokespeed = 10
    mountx = offscreenX
    mounty = surfaceHeight - randint(200,(surfaceHeight/2))

    
    # Game Loop
    while not game_over:

        # End if done
        if current_lives <=0 or current_score < 0:
            game_over = True
            gameOver()
                       
        # Capture player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_move = moveRateMed * -1


                if event.key == pygame.K_SPACE:
                    if (len(bullets)) <= maxScreenBullets :
	                    bullets.append([x + imageWidth,y + (imageHeight/2)])                    
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    y_move = moveRateSlow

        # Add Background
        surface.blit(imgBack, (imgBackX,imgBackY))
        
        # Set new y coord based on user input
        y += y_move
        # Add player icon
        icon(x, y, hero)
        
        # Add enemy
        surface.blit(chal, (chalx,chaly))
        # Move enemy by adjusting x coordinates
        chalx -= pokespeed
        
        # Add mountains
        surface.blit(mountaintop, (mountx,mounty))
        # Move enemy by adjusting x coordinates
        mountx -= pokespeed        
        
        # Add apple
        if current_score%20==0 and apple_on == False:
            apple_on = True

        if apple_on:
            surface.blit(apple, (applex,appley))
            # Move enemy by adjusting x coordinates
            applex -= moveRateFast
            # Logic to respawn enemy when last enemy flys off screen
            if applex < (leftEdge):
                applex = offscreenX
                appley = randint(0,(surfaceHeight/2))
                apple_on = False

        # Set the Score
        score(current_score)
        
        # Set the lives
        lives(current_lives)
                
        # Set Upper & Lower boundaries
        if y > bottomEdge or y < topEdge:
            current_lives -= scoreIncr
            die(explode,x,y)
            x = iconXreset
            y = iconYreset
            
        if x < leftEdge:
            x = leftEdge
            
        if x > rightEdge:
            x = rightEdge
            
        # Logic to respawn enemy when last enemy flys off screen
        if chalx < (leftEdge):
            chalx = surfaceWidth
            chaly = randint(0,(surfaceHeight/2))
            current_score -= scoreIncrMed

        # Logic to respawn mountain when last one flys off screen
        if mountx < (-300):
            mountx = surfaceWidth
            mounty = randint(175,500)
            if pokespeed < moveRateFast:
                pokespeed += ememySpeedUpRate            
            
        # Move bullets
        for b in range(len(bullets)):
    	    bullets[b][0]+=moveRateSlow

        # If bullet gets to end of screen remove
        for bullet in bullets:
    	    if bullet[0]>surfaceWidth:
                bullets.remove(bullet)

        # Add bullets to screen
        for bullet in bullets:
            surface.blit(bulletpicture, pygame.Rect(bullet[0], bullet[1], 0, 0))
            
        # Logic for bullet + enemy collision
        for bullet in bullets:
    	    if bullet[0]>=chalx and (bullet[1] <= chaly + (imageHeight) and bullet[1] >= chaly) :
                #  Remove bullet
                bullets.remove(bullet)
                # Respawn 
                chalx = surfaceWidth
                chaly = randint(0,(surfaceHeight/2))
                # Incrment the score
                current_score += scoreIncr


        # Logic for player + enemy collision 
        if x >= chalx:
            if y >= chaly - (imageHeight/2) and y <= chaly + (imageHeight/2):
                current_lives -= scoreIncr
                die(explode,x,y)    
                # reset
                x = iconXreset
                y = iconYreset
                chalx = surfaceWidth
                chaly = randint(0,(surfaceHeight/2))


        # Logic for player + apple collision 
        if x >= applex:
            if y >= appley - (imageHeight/2) and y <= appley + (imageHeight/2):              
                # reset
                x = iconXreset
                current_score += scoreIncrMed
                applex = offscreenX
                appley = randint(0,(surfaceHeight/2))
                apple_on = False
                
        # Update the screen with new settings
        pygame.display.update()
        clock.tick(60)
                                        
        # Evolve
        if current_score >= evolveStage2Score:
            hero = evolvedHero
            imageHeight = evolvedHeight
            imageWidth = evolvedWidth
            chal = evolvedChal
     	
main()
pygame.quit()
quit()
