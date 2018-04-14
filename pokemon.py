import os
import pygame
import time
from random import randint
import sys, pygame.mixer
from pygame.locals import *
from libs.settings import *

    
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.mixer.init()
pygame.mixer.music.load(os.path.join("Data",'dragons.mp3'))

surface = pygame.display.set_mode((surfaceWidth,surfaceHeight))
pygame.display.set_caption('Bulbasaur')
clock = pygame.time.Clock()    

'''
Restart or Quit Logic
'''
def replay_or_quit():
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    for event in pygame.event.get([pygame.JOYBUTTONDOWN, pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.JOYBUTTONDOWN:
            continue

        return event.key
    
    return None


'''
Load an image from the data directory with per pixel alpha transparency.
'''
def load_image(i):
    return pygame.image.load(os.path.join("Data", i)).convert_alpha()

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

def showBombs(bcount):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render("Bombs: "+str(bcount), True, black)
    surface.blit(text, [450,10])    

def die(explode, rect):
    surface.blit(explode, rect)
    pygame.display.update(rect)
    clock.tick(60)
    
def gameOver():
    msgSurface('Game Over')

def test(i, x, y):
    font = pygame.font.Font('freesansbold.ttf', 20)
    smfont = pygame.font.Font('freesansbold.ttf', 10)
    herotext = font.render("x:" + str(x) + " y:"+str(y), True, black)
    countertext = font.render("i:" + str(i) , True, black)
    one = smfont.render("100", True, black)
    three = smfont.render("300", True, black)
    five = smfont.render("500", True, black)
    seven = smfont.render("700", True, black)
    surface.blit(herotext, [400,30])
    surface.blit(countertext, [400,50])
    surface.blit(one, [100,5])
    surface.blit(one, [5,100])
    surface.blit(one, [970,100])
    surface.blit(one, [100,690])
    surface.blit(three, [300,5])
    surface.blit(three, [5,300])
    surface.blit(three, [970,300])
    surface.blit(three, [300,690])
    surface.blit(five, [500,5])
    surface.blit(five, [5,500])
    surface.blit(five, [970,500]) 
    surface.blit(five, [500,690])   
    surface.blit(seven, [700,5])
    surface.blit(seven, [700,690])


def main():

### Dynamic Variables
    # Inital Game state
    i=0
    current_score = 0
    current_lives = 3
    game_over = False
    apple_on = False 
    # Inital settings
    halfScreenY = randint(0,(surfaceHeight/2))
    y_move = 0
    x_move = 0
    bullets=[]
    bombs=[]
    enemies=[]
    bombCount = 2
    pokespeed = 15
    paused = 0
    dead = False

### Load images into memory
    # Load background   
    imgBack = pygame.image.load(os.path.join("Data", "sky.gif"))
   
    # Load Player into memory
    heroIco = load_image('Bulbasaur.png')
    heroIco = pygame.transform.scale(heroIco,(imageWidth,imageHeight))
    heroIcoMask = pygame.mask.from_surface(heroIco, 50)
    heroIcoRect = heroIco.get_rect()
    heroIcoRect.x = iconXreset
    heroIcoRect.y = iconYreset
    
    # Load Enemy into memory
    enemyIco = load_image('Charmander.png')
    enemyIco = pygame.transform.scale(enemyIco,(imageWidth,imageHeight))
    enemyIcoMask = pygame.mask.from_surface(enemyIco, 50)
    enemyIcoRect = enemyIco.get_rect()
    enemyIcoRect.x = surfaceWidth
    enemyIcoRect.y = halfScreenY
    
    # Load bullet
    bulletIco = load_image("topbullet.gif")
    bulletIco = pygame.transform.scale(bulletIco,(50,50))
    bulletIcoMask = pygame.mask.from_surface(bulletIco, 50)
    bulletIcoRect = bulletIco.get_rect()
    
    # Load apple
    appleIco = load_image("pokeball_sprite.png")
    appleIco = pygame.transform.scale(appleIco,(128,128))
    appleIcoMask = pygame.mask.from_surface(appleIco, 50)
    appleIcoRect = appleIco.get_rect()
    appleIcoRect.x = surfaceWidth
    appleIcoRect.y = halfScreenY
    
    # Load dead Player into memory
    explode = load_image('boom.png')
    explode = pygame.transform.scale(explode,(250,250))

    # Load bomb
    bombIco = load_image("topbullet.gif")
    bombIco = pygame.transform.scale(bombIco,(150,150))
    bombIcoMask = pygame.mask.from_surface(bombIco, 50)
    bombIcoRect = bombIco.get_rect()

    # Load mountains into memory
    mountain = load_image('mountaintop.png')    
    mountainMask = pygame.mask.from_surface(mountain, 50)
    mountainRect = mountain.get_rect()
    mountainRect.x = offscreenX
    mountainRect.y = surfaceHeight - randint(mountHeight,(surfaceHeight/2))
    
    pygame.joystick.init()

###############    
### Game Loop
###############
    while not game_over:

        # Counter
        i += 1
        
        # Pause before restarting
        if dead==True:
            enemies.clear()
            mountainRect.x = offscreenX
            mountainRect.y = surfaceHeight - randint(mountHeight,(surfaceHeight/2))
            heroIcoRect.x = iconXreset
            heroIcoRect.y = iconYreset
            dead = False
            
### Game Control
        # End if done
        if current_lives <=0 or current_score < 0:
            game_over = True
            gameOver()
### End Game Control

### Capture Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if paused == 1:
                        paused = 0
                    else:
                        paused = 1
        
        # Get count of joysticks
        joystick_count = pygame.joystick.get_count()
        
        if joystick_count > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            axes = joystick.get_numaxes()
            leftjoysticky = joystick.get_axis(1)
            leftjoystickx = joystick.get_axis(0)
            if leftjoysticky != 0:
                y_move = moveRateMed * leftjoysticky
            if leftjoystickx != 0:
                x_move = moveRateMed * leftjoystickx
            button = joystick.get_button( 0 )
            button2 = joystick.get_button( 1 )
            if button == 1 and i%5==0:
                if (len(bullets)) <= maxScreenBullets :
                    bullets.append([heroIcoRect.x + imageWidth, heroIcoRect.y + (imageHeight/2)])
            if button2 ==1 and i%7==0:
                if bombCount > 0:
                    bombs.append([heroIcoRect.x + imageWidth, heroIcoRect.y + (imageHeight/2)])
                    bombCount -= 1

### End Capture Input
### Display Images            

        # Add Background
        surface.blit(imgBack, (imgBackX,imgBackY))
        # Add player icon
        surface.blit(heroIco, (heroIcoRect.x, heroIcoRect.y))        
        # Add mountains
        surface.blit(mountain, (mountainRect.x,mountainRect.y))
        # Add bullets to screen
        for bullet in bullets:
            surface.blit(bulletIco, pygame.Rect(bullet[0], bullet[1], 0, 0))
        # Add bullets to screen
        for bomb in bombs:
            surface.blit(bombIco, pygame.Rect(bomb[0], bomb[1], 0, 0))
        # Add apple
        if current_score%10==0  and apple_on == False:
            apple_on = True
        if apple_on == True:
            surface.blit(appleIco, (appleIcoRect.x,appleIcoRect.y))
             # Logic to respawn enemy when last enemy flys off screen
            if appleIcoRect.x < (leftEdge):
                appleIcoRect.x = offscreenX
                appleIcoRect.y = halfScreenY
                apple_on = False

        if len(enemies) < maxEnemies:
            enemies.append([enemyIcoRect.x-randint(0,200),randint(0,surfaceHeight-150)])
                                
        # Add bullets to screen
        for enemy in enemies:
            surface.blit(enemyIco, pygame.Rect(enemy[0], enemy[1], 0, 0))
                
### End Display Images

### Movement
        if paused == 0:
            # Move mountain by adjusting x coordinates
            mountainRect.x -= pokespeed        

            if apple_on == True:
                # Move enemy by adjusting x coordinates
                appleIcoRect.x -= moveRateFast

            # Set new y coord based on user input
            heroIcoRect.y += y_move
            heroIcoRect.x += x_move

            # Move bullets
            for b in range(len(bullets)):
                bullets[b][0]+=moveRateSlow
            # Move bombs
            for B in range(len(bombs)):
                bombs[B][0]+=moveRateSlow

            # Move enemies
            for e in range(len(enemies)):
                if e%2==0:
                    enemies[e][0]-=moveRateMed
                elif e%3==0:
                    enemies[e][0]-=moveRateFast
                else:
                    enemies[e][0]-=pokespeed
                
        # Set Upper & Lower boundaries
        if heroIcoRect.y > bottomEdge or heroIcoRect.y < topEdge:
            current_lives -= scoreIncr
            die(explode,heroIcoRect)
            dead = True
            continue
        
        if heroIcoRect.x < leftEdge:
            heroIcoRect.x = leftEdge
            
        if heroIcoRect.x > rightEdge:
            heroIcoRect.x = rightEdge
### End Movement


### Start Collisions ###
        bx, by = (heroIcoRect[0], heroIcoRect[1])
        
        if apple_on == True:
            appleOffset_x = bx - appleIcoRect[0]
            appleOffset_y = by - appleIcoRect[1]
            appleCollide = appleIcoMask.overlap(heroIcoMask, (appleOffset_x, appleOffset_y))
            if appleCollide:
                bombCount += 1
                # reset
                current_score += scoreIncrMed
                appleIcoRect.x = offscreenX
                appleIcoRect.y = halfScreenY
                apple_on = False
            
        mountOffset_x = bx - mountainRect[0]
        mountOffset_y = by - mountainRect[1]
        mountCollide = mountainMask.overlap(heroIcoMask, (mountOffset_x, mountOffset_y))
        if mountCollide:
            current_lives -= scoreIncr
            die(explode,heroIcoRect)
            dead = True
            continue

        for bullet in bullets:
            bulletOffset_x = mountainRect[0] - bullet[0]
            bulletOffset_y = mountainRect[1] - bullet[1]
            bulletCollide = bulletIcoMask.overlap(mountainMask, (round(bulletOffset_x), round(bulletOffset_y)))
            if bulletCollide:
                #  Remove bullet
                try:
                    bullets.remove(bullet)
                except:
                    print("already gone")

        for bomb in bombs:
            bombOffset_x = mountainRect[0] - bomb[0]
            bombOffset_y = mountainRect[1] - bomb[1]
            bombCollide = bombIcoMask.overlap(mountainMask, (round(bombOffset_x), round(bombOffset_y)))
            if bombCollide:
                mountainRect.x = offscreenX
                mountainRect.y = surfaceHeight - randint(mountHeight,(surfaceHeight/2))
                    

        for enemy in enemies:
            enemyOffset_x = bx - enemy[0]
            enemyOffset_y = by - enemy[1]
            enemyCollide = enemyIcoMask.overlap(heroIcoMask, (enemyOffset_x, enemyOffset_y))
            if enemyCollide:
                current_lives -= scoreIncr
                die(explode,heroIcoRect)    
                dead = True
                continue
            
            for bullet in bullets:
                bulletOffset_x = enemy[0] - bullet[0]
                bulletOffset_y = enemy[1] - bullet[1]
                bulletCollide = bulletIcoMask.overlap(enemyIcoMask, (round(bulletOffset_x), round(bulletOffset_y)))
                if bulletCollide:
                    current_score += scoreIncr
                    #  Remove bullet
                    try:
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                    except:
                        print("already gone")

            for bomb in bombs:
                bombOffset_x = enemy[0] - bomb[0]
                bombOffset_y = enemy[1] - bomb[1]
                bombCollide = bombIcoMask.overlap(enemyIcoMask, (round(bombOffset_x), round(bombOffset_y)))
                if bombCollide:
                    current_score += scoreIncr
                    #  Remove bomb
                    try:
                        enemies.remove(enemy)
                    except:
                        print("already gone")                        
                        
        last_bx, last_by = bx, by


### End Collisions


### Spawning
        # Logic to respawn mountain when last one flys off screen
        if mountainRect.x < (-300):
            mountainRect.x = surfaceWidth
            mountainRect.y = randint(mountHeight,600)
            if pokespeed < moveRateFast:
                pokespeed += enemySpeedUpRate            
            
        # If enemy gets to end of screen remove
        for enemy in enemies:
            if enemy[0] < leftEdge:
                enemies.remove(enemy)

        # If bullet gets to end of screen remove
        for bullet in bullets:
            if bullet[0]>surfaceWidth:
                bullets.remove(bullet)

        # If bullet gets to end of screen remove
        for bomb in bombs:
            if bomb[0]>surfaceWidth:
                bombs.remove(bomb)

### End Spawning

###


        # Set the Score
        score(current_score)
        # Set the lives
        lives(current_lives)
        # Set the bombs
        showBombs(bombCount)
        # Used for debugging
        test(i,heroIcoRect.x,heroIcoRect.y)
                                                        

        # Update the screen with new settings
        pygame.display.update()
        clock.tick(60)

#pygame.mixer.music.play(-1)            
main()
pygame.quit()
quit()


