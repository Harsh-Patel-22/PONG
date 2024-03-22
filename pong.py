# Retro Style Pong Game 
#todo Make corrections in the winner logic to match it with the real thing
#todo Find and add suitable for winning
#todo Make classes for paddle and ball and refractor the entire code

import pygame
import random
import sys

WINTHRESHOLD = 2
WINNER = 1

def drawObjects():
    paddle1 = pygame.Rect(5,paddle1Y,10,100)
    paddle2 = pygame.Rect(785,paddle2Y,10,100)
    ball = pygame.Rect(ballX, ballY, 13, 13)

    pygame.draw.rect(SCREEN, (255,255,255), paddle1)
    pygame.draw.rect(SCREEN, (255,255,255), paddle2)
    pygame.draw.rect(SCREEN, (255,255,255), ball, border_radius=4)


    retroFont = pygame.font.Font('retrofont.ttf',25)
    p1ScoreText = retroFont.render(str(player1score), True, (255,255,255))
    p1ScoreHolder = p1ScoreText.get_rect()
    p1ScoreHolder.center = (200, 100)
    p2ScoreText = retroFont.render(str(player2score), True, (255,255,255))
    p2ScoreHolder = p2ScoreText.get_rect()
    p2ScoreHolder.center = (600, 100)

    SCREEN.blit(p1ScoreText, p1ScoreHolder)
    SCREEN.blit(p2ScoreText, p2ScoreHolder)

def configureState(activestate):
    global balldX, balldY, ballX, ballY, paddle1Y, paddle2Y, state

    if activestate == 'start':
        
        state = 'start'
        paddle1Y = 5
        paddle2Y = 495
        ballX = SCREEN.get_width() / 2
        ballY = SCREEN.get_height() / 2

    elif activestate == 'play':
        state = 'play'
        balldX = random.randint(-50,50) / 10
        balldY = random.randint(-50,50) / 5

        if balldX >= 0:
            balldX = max(balldX, 3)
        elif balldX < 0:
            balldX = min(balldX, -3)

        if balldY >= 0:
            balldY = max(balldY, 3)
        elif balldY < 0:
            balldY = min(balldY, -3)

    elif activestate == 'serve':
        state = 'serve'
        paddle1Y = 5
        paddle2Y = 495
        ballX = SCREEN.get_width() / 2
        ballY = SCREEN.get_height() / 2
        if servingplayer == 1: # paddle 1's serve
            print('paddle1 is serving')
            balldX = random.randint(0,100) / 10
            balldY = random.randint(-50,50) / 5
            if balldX >= 0:
                balldX = max(balldX, 3)
            if balldY >= 0:
                balldY = max(balldY, 3)

        elif servingplayer == 2: # paddle 2's serve
            print('paddle2 is serving')
            balldX = random.randint(-100,0) / 10
            balldY = random.randint(-50,50) / 5
            if balldX < 0:
                balldX = min(balldX, -3)
            if balldY < 0:
                balldY = min(balldY, -3)
    elif activestate == 'over':
        state = 'over'
        retroFont = pygame.font.Font('retrofont.ttf',50)
        winText = retroFont.render(f'Player {WINNER} wins!', True, (255,255,255))
        winTextHolder = winText.get_rect()
        winTextHolder.center = (400,300)
        SCREEN.blit(winText, winTextHolder)

def generateReflected_Y():
    global balldY
    if(balldY > 0):
        balldY = random.randint(0, 50) / 5
    else:
        balldY = random.randint(-50,0) / 5
        
    if balldY >= 0:
        balldY = max(balldY, 3)
    elif balldY < 0:
        balldY = min(balldY, -3)

def handleCollision():
    global balldX
    if (ballX < 15 and (ballY > paddle1Y and ballY < paddle1Y + 100)):
        GAME_SOUNDS['hit'].play()
        balldX = -balldX * 1.1
        generateReflected_Y()

    elif (ballX > 780 and (ballY > paddle2Y and ballY < paddle2Y + 100)):
        GAME_SOUNDS['hit'].play()
        balldX = -balldX * 1.1
        generateReflected_Y()

def handlePoints():
    global player1score, player2score, state, servingplayer, WINNER
    scoredPoint = False
    if ballX < 0:
        scoredPoint = True
        player2score += 1
        print(f'Player 2 score = {player2score}')
        WINNER = 2
        servingplayer = 1
    elif ballX > 799:
        scoredPoint = True
        player1score += 1
        print(f'Player 1 score = {player1score}')
        WINNER = 1
        servingplayer = 2
    
    if scoredPoint:
        GAME_SOUNDS['point'].play()
        if player1score == WINTHRESHOLD or player2score == WINTHRESHOLD:
            configureState('over')
        else:
            configureState('serve')

pygame.init()
fpsclock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((800, 600))
ICON = pygame.image.load('icon.png')
pygame.display.set_icon(ICON)
pygame.display.set_caption('Pong')
GAME_SOUNDS = {}


GAME_SOUNDS['hit'] = pygame.mixer.Sound('paddlehit.wav')
GAME_SOUNDS['point'] = pygame.mixer.Sound('point.wav')
GAME_SOUNDS['point'].set_volume(0.1)

player1score = 0
player2score = 0
servingplayer = 0

retroFont = pygame.font.Font('retrofont.ttf',32)
instructionFont = pygame.font.Font('display.otf', 30)

title = retroFont.render('PONG', True, (255,255,255))
titleHolder = title.get_rect()
titleHolder.center = (400, 50)

paddle1Y = 5
paddle2Y = 495
ballX = SCREEN.get_width() / 2
ballY = SCREEN.get_height() / 2

paddle1Speed = 0
paddle2Speed = 0

state = 'start'
configureState(state)
while True:
    SCREEN.fill((0,0,0))
    SCREEN.blit(title,titleHolder)
    if state == 'start':
        instruction1 = instructionFont.render("'w' and 's' to control left paddle", True, (255,255,255))
        instruction2 = instructionFont.render("'up' and 'down' arrow keys for right paddle", True, (255,255,255))
        instruction3 = instructionFont.render("Press 'space' to Start!", True, (255,255,255))

        instruction1Holder = instruction1.get_rect()
        instruction1Holder.center = (400, 250)
        instruction2Holder = instruction2.get_rect()
        instruction2Holder.center = (400, 375)
        instruction3Holder = instruction3.get_rect()
        instruction3Holder.center = (400, 500)
        SCREEN.blit(instruction1,instruction1Holder)
        SCREEN.blit(instruction2,instruction2Holder)
        SCREEN.blit(instruction3,instruction3Holder)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state == 'start':
                    configureState('play')
                elif state == 'serve':
                    state = 'play'
                print(state)

            if state == 'play' or state == 'serve':
                if event.key == pygame.K_w:
                    paddle1Speed = -7.5
                
                if event.key == pygame.K_s:
                    paddle1Speed = 7.5

                if event.key == pygame.K_UP:
                    paddle2Speed = -7.5
                    
                if event.key == pygame.K_DOWN:
                    paddle2Speed = 7.5
            
        if state == 'play' or state == 'serve':
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    paddle2Speed = 0 
                
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    paddle1Speed = 0

    if state == 'start':
        drawObjects()
        pygame.display.update()
        fpsclock.tick(24)

    if state == 'play':
        paddle1Y += paddle1Speed
        paddle2Y += paddle2Speed
        ballX += balldX
        ballY += balldY

        if(ballY <= 0 or ballY >= 600):
            balldY = -balldY

        if(paddle1Y <= 0):
            paddle1Y = 0 

        if(paddle1Y >= 500):
            paddle1Y = 500 

        if(paddle2Y <= 0):
            paddle2Y = 0 

        if(paddle2Y >= 500):
            paddle2Y = 500 
        handleCollision()
        handlePoints()
        drawObjects()
        pygame.display.update()
        fpsclock.tick(24)