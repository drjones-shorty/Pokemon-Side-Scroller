import pygame
import time

black = (0,0,0)
white = (255,255,255)

pygame.init()

surfaceWidth = 1000 
surfaceHeight = 700

surface = pygame.display.set_mode((surfaceWidth,surfaceHeight))
pygame.display.set_caption('Bulbasaur')
clock = pygame.time.Clock()


def replay_or_quit():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            continue

        return event.key
    
    return None

def makeTextObjs(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

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
    img = pygame.image.load('Bulbasaur.png')
    x = 150
    y = 200
    img2 = pygame.image.load('Ivysaur.png')
    chal = pygame.image.load('Charmander.png')
    chalx = 650
    chaly = 200
    imgback = pygame.image.load('grass.jpg')
    imgx = 0
    imgy = 0
    
 
    y_move = 0
    
    game_over = False

    while not game_over:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_move = -20
                if event.key == pygame.K_SPACE:
                    img = img2
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    y_move = 10

        y += y_move

        surface.blit(imgback, (imgx,imgy))
        icon(x ,y, img)
        surface.blit(chal, (chalx,chaly))

        if y > surfaceHeight-40 or y < 0:
            gameOver()

        pygame.display.update()
        clock.tick(60)

main()
pygame.quit()
quit()















    
