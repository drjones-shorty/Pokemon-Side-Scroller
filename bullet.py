'''
There are several steps you have to go through to do this. You will need a picture of the bullet, a way to store the locations of the bullets, a way to create the bullets, a way to render the bullets, and a way to update the bullets. You appear to know how to import pictures already, so I'll skip that part.

There are several ways that you can store pieces of information. I will be using a list of the top left corner of the bullets. Create the list anywhere before the final loop with bullets=[].

To create the bullets, you will want to use the location of the mouse. Add in bullets.append([event.pos[0]-32, 500]) after shot.play(), indented the same amount.

To render the bullets, you will be adding a for loop into your game loop. After the line screen.blit(background, (0, 0)), add the following code:

for bullet in bullets:
  screen.blit(bulletpicture, pygame.Rect(bullet[0], bullet[1], 0, 0)
To update the bullets, you need to put something somewhere in your game loop that looks like this:

for b in range(len(bullets)):
  bullets[b][0]-=10
Finally, you need to remove the bullets when they reach the top of the screen. Add this after the for loop you just created:

for bullet in bullets:
  if bullet[0]<0:
    bullets.remove(bullet)
After putting this all into your code, it should look something like this:
'''

import sys, pygame, pygame.mixer
from pygame.locals import *

pygame.init()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

bullets=[]

background = pygame.image.load("grass.jpg")
ship = pygame.image.load("Bulbasaur.png")
ship = pygame.transform.scale(ship,(64,64))
bulletpicture = pygame.image.load("topbullet.gif")

shot = pygame.mixer.Sound("shot.wav")
soundin = pygame.mixer.Sound("sound.wav")

soundin.play()

while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()

    elif event.type == MOUSEBUTTONDOWN:
      shot.play()
      bullets.append([event.pos[0]-32, 500])

  clock.tick(60)

  mx,my = pygame.mouse.get_pos()

  for b in range(len(bullets)):
    bullets[b][0]-=10

  for bullet in bullets:
    if bullet[0]<0:
      bullets.remove(bullet)

  screen.blit(background,(0,0))

  for bullet in bullets:
    screen.blit(bulletpicture, pygame.Rect(bullet[0], bullet[1], 0, 0))

  screen.blit(ship,(mx-32,500))
  pygame.display.flip()
  
