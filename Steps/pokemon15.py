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
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.mixer.init()
pygame.mixer.music.load('dragons.mp3')

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

def showBombs(bcount):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render("Bombs: "+str(bcount), True, black)
    surface.blit(text, [450,10])    

def die(explode, x,y):
    surface.blit(explode, (x,y))
    #pygame.display.update()
    time.sleep(1)
    #clock.tick()
    
def gameOver():
    msgSurface('Game Over')
    
def getSlope(x1, y1, x2, y2):
    slope = (y2-y1)/(x2-x1)
    return slope

def getMountX(x,y,y1,m):
    x1 = ((y-y1)/m)+x
    return x1

def test(x,y,mx,my):
    font = pygame.font.Font('freesansbold.ttf', 20)
    smfont = pygame.font.Font('freesansbold.ttf', 10)
    slope = getSlope(mx+400,my,mx,my-500)
    slopetext = font.render("slope(m):" + str(slope), True, black)
    newX = font.render("newx:" + str(getMountX(mx+400,my,y+182,slope)), True, black)
    herotext = font.render("x:" + str(x) + " y:"+str(y), True, black)
    mounttext = font.render("mntx:"+str(mx)+" mnty:"+str(my), True, black)
    star = smfont.render("*", True, black)
    one = smfont.render("100", True, black)
    three = smfont.render("300", True, black)
    five = smfont.render("500", True, black)
    seven = smfont.render("700", True, black)
    surface.blit(herotext, [400,30])
    surface.blit(mounttext, [400,50])
    surface.blit(slopetext, [400,70])
    surface.blit(newX, [400,90])
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
    surface.blit(star, [x,y])
    surface.blit(star, [x+192,y+182])


def main():

### Load Configs (Constants)
    imgBackX = 0
    imgBackY = 0
    imageHeight = 182
    imageWidth = 192
    evolvedHeight = 207
    evolvedWidth = 238
    iconXreset = 50
    iconYreset = 200
    offscreenX = surfaceWidth + 100
    rightEdge = surfaceWidth - 100
    leftEdge = 10
    bottomEdge = surfaceHeight - 10
    topEdge = -50
    maxScreenBullets = 10
    moveRateFast = 20
    moveRateMed = 10
    moveRateSlow = 5
    evolveStage2Score = 30
    scoreIncr = 1
    scoreIncrMed = 5
    scoreIncrHigh = 10
    ememySpeedUpRate = .5
    mountHeight = 210
    
### Load images into memory
    # Load background   
    imgBack = pygame.image.load('sky.gif')
   
    # Load Player into memory
    hero = pygame.image.load('Bulbasaur.png')
    hero = pygame.transform.scale(hero,(imageWidth,imageHeight))
    
    # Load Evolved Player into memory
    evolvedHero = pygame.image.load('Ivysaur.png')
    evolvedHero = pygame.transform.scale(evolvedHero,(evolvedWidth,evolvedHeight))
    
    # Load Enemy into memory
    enemy = pygame.image.load('Charmander.png')
    enemy = pygame.transform.scale(enemy,(imageWidth,imageHeight))

    # Load Evolved Enemy into memory
    evolvedEnemy = pygame.image.load('Charizard.png')
    evolvedEnemy = pygame.transform.scale(evolvedEnemy,(evolvedWidth,evolvedHeight))
    
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

### Dynamic Variables        
    # Inital Game state
    current_score = 0
    current_lives = 3
    game_over = False
    apple_on = False     
    # Inital settings
    x = iconXreset
    y = iconYreset
    enemyx = surfaceWidth
    enemyy = randint(0,(surfaceHeight/2))
    applex = surfaceWidth
    appley = randint(0,(surfaceHeight/2))    
    y_move = 0
    x_move = 0
    bullets=[]
    bombs=[]
    bombCount = 2
    pokespeed = 10
    mountx = offscreenX
    mounty = surfaceHeight - randint(mountHeight,(surfaceHeight/2))
    paused = 0
    
    
    pygame.joystick.init()

###############    
### Game Loop
###############
    while not game_over:

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
            if button == 1:
                if (len(bullets)) <= maxScreenBullets :
                    bullets.append([x + imageWidth,y + (imageHeight/2)])
            if button2 ==1:
                if bombCount > 0:
                    bombs.append([x + imageWidth,y + (imageHeight/2)])
                    bombCount -= 1

### End Capture Input

### Display Images            
        # Add Background
        surface.blit(imgBack, (imgBackX,imgBackY))
        # Add player icon
        surface.blit(hero, (x, y))        
        # Add enemy
        surface.blit(enemy, (enemyx,enemyy))
        # Add mountains
        surface.blit(mountaintop, (mountx,mounty))
        # Add bullets to screen
        for bullet in bullets:
            surface.blit(bulletpicture, pygame.Rect(bullet[0], bullet[1], 0, 0))
        # Add bullets to screen
        for bomb in bombs:
            surface.blit(explode, pygame.Rect(bomb[0], bomb[1], 0, 0))
        # Add apple
        if current_score%20==0 and current_score > 0 and apple_on == False:
            apple_on = True
        if apple_on:
            surface.blit(apple, (applex,appley))
             # Logic to respawn enemy when last enemy flys off screen
            if applex < (leftEdge):
                applex = offscreenX
                appley = randint(0,(surfaceHeight/2))
                apple_on = False

        # Evolution
#        if current_score >= evolveStage2Score:
#            hero = evolvedHero
#            imageHeight = evolvedHeight
#            imageWidth = evolvedWidth
#            enemy = evolvedEnemy

### End Display Images

### Movement
        if paused == 0:
            # Move enemy by adjusting x coordinates
            enemyx -= pokespeed
            # Move mountain by adjusting x coordinates
            mountx -= pokespeed        
            # Move enemy by adjusting x coordinates
            applex -= moveRateFast
            # Set new y coord based on user input
            y += y_move
            x += x_move
            # Move bullets
            for b in range(len(bullets)):
                bullets[b][0]+=moveRateSlow
            # Move bullets
            for B in range(len(bombs)):
                bombs[B][0]+=moveRateSlow

                
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
### End Movement

### Spawning
        # Logic to respawn enemy when last enemy flys off screen
        if enemyx < (leftEdge):
            enemyx = surfaceWidth
            enemyy = randint(0,(surfaceHeight/2))
            #current_score -= scoreIncrMed

        # Logic to respawn mountain when last one flys off screen
        if mountx < (-300):
            mountx = surfaceWidth
            mounty = randint(mountHeight,600)
            if pokespeed < moveRateFast:
                pokespeed += ememySpeedUpRate            
            
        # If bullet gets to end of screen remove
        for bullet in bullets:
            if bullet[0]>surfaceWidth:
                bullets.remove(bullet)

        # If bullet gets to end of screen remove
        for bomb in bombs:
            if bomb[0]>surfaceWidth:
                bombs.remove(bomb)

### End Spawning

### Start Collisions

        # Logic for bullet + enemy collision
        for bullet in bullets:
            if bullet[0]>=enemyx and (bullet[1] <= enemyy + (imageHeight) and bullet[1] >= enemyy) :
                #  Remove bullet
                try:
                    bullets.remove(bullet)
                except:
                    print("already gone")
                # Respawn 
                enemyx = surfaceWidth
                enemyy = randint(0,(surfaceHeight/2))
                # Incrment the score
                current_score += scoreIncr
            if bullet[1]>=mounty and (bullet[1] <= surfaceHeight):
                if bullet[0] > getMountX(mountx+400,mounty,bullet[1],getSlope(mountx+400,mounty,mountx,mounty-500)):                      
                    try:
                        bullets.remove(bullet)
                    except:
                        print("alredy gone")

        # Logic for bomb + enemy collision
        for bomb in bombs:
            if bomb[0] + imageWidth >=enemyx and (bomb[1] <= enemyy + (imageHeight) and bomb[1] >= enemyy) :
                #  Remove bomb
                bombs.remove(bomb)
                # Respawn 
                enemyx = surfaceWidth
                enemyy = randint(0,(surfaceHeight/2))
                # Incrment the score
                current_score += scoreIncr
            if bomb[1]+imageHeight>=mounty and (bomb[1] <= surfaceHeight):
                if bomb[0] + imageWidth> getMountX(mountx+400,mounty,bomb[1],getSlope(mountx+400,mounty,mountx,mounty-500)):                      
                    bombs.remove(bomb)
                    # Respawn 
                    mountx = surfaceWidth
                    mounty = randint(mountHeight,(surfaceHeight/2))
                    # Incrment the score
                    current_score += scoreIncr

        # Logic for player + apple collision 
        if x >= applex:
            if y >= appley - (imageHeight/2) and y <= appley + (imageHeight/2):              
#                bombCount += 1
                # reset
                x = iconXreset
#                current_score += scoreIncrMed
                applex = offscreenX
                appley = randint(0,(surfaceHeight/2))
                apple_on = False

        # Logic for player + terrain collision
        if y + (imageHeight) >= mounty and y + (imageHeight/2) <= surfaceHeight:
            if x + imageWidth > getMountX(mountx+400,mounty,y+(imageWidth/2),getSlope(mountx+400,mounty,mountx,mounty-500)):
                current_lives -= scoreIncr
                die(explode,x,y)    
                # reset
                x = iconXreset
                y = iconYreset
                mountx = surfaceWidth
                mounty = randint(mountHeight,(surfaceHeight/2))


        # Logic for player + enemy collision 
        if x >= enemyx:
            if y >= enemyy - (imageHeight/2) and y <= enemyy + (imageHeight/2):
                current_lives -= scoreIncr
                die(explode,x,y)    
                # reset
                x = iconXreset
                y = iconYreset
                enemyx = surfaceWidth
                enemyy = randint(0,(surfaceHeight/2))
### End Collisions


        # Set the Score
        score(current_score)
        # Set the lives
        lives(current_lives)
        # Set the bombs
        showBombs(bombCount)
        # Used for debugging
        #test(x,y,mountx,mounty)
                                                        

        # Update the screen with new settings
        pygame.display.update()
        clock.tick(60)

#pygame.mixer.music.play(-1)            
main()
pygame.quit()
quit()


