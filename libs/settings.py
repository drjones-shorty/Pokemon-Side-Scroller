from random import randint

### Load Configs (Constants)
# Game Constants
black = (0,0,0)
white = (255,255,255)
surfaceWidth = 1000 
surfaceHeight = 700
imgBackX = 0
imgBackY = 0
imageHeight = 182
imageWidth = 192
iconXreset = 50
iconYreset = 200
offscreenX = surfaceWidth + 100
rightEdge = surfaceWidth - 100
leftEdge = 10
bottomEdge = surfaceHeight - 10
topEdge = -50
maxScreenBullets = 10
moveRateFast = 20
moveRateMed = 13
moveRateSlow = 8
scoreIncr = 1
scoreIncrMed = 5
scoreIncrHigh = 10
enemySpeedUpRate = .5
mountHeight = 210
maxEnemies = 1
last_bx = iconXreset
last_by = iconYreset

