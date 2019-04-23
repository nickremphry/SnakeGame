#Basic Snake Game
#Written by: Michael Remphry

import pygame, random, sys
from pygame.locals import *

pygame.init()

f = pygame.font.SysFont('Arial', 20)
display = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

diff = 0 
black = (0, 0, 0)
white = (255, 255, 255)

#Main menu screen with selective difficulties
def main_menu():
    
    global diff
    global black
    global white
    menu = True
    
    display.fill(white)
    
    easy_rect = pygame.draw.rect(display, (0, 255, 0), (35, 270, 100, 100))
    medium_rect = pygame.draw.rect(display, (255, 140, 0), (200, 270, 170, 100))
    hard_rect = pygame.draw.rect(display, (255, 0, 0), (435, 270, 100, 100))
    
    f1 = pygame.font.SysFont('Arial', 50)
    t1 = f1.render('Snake Game', True, black)
    display.blit(t1, (170, 10))
    
    f2 = pygame.font.SysFont('Arial', 30)
    t2 = f2.render('What Difficulty Would You Like?', True, black)
    display.blit(t2, (100, 150))
    
    e = f2.render('Easy', True, black)
    i = f2.render('Intermediate', True, black)
    h = f2.render('Hard', True, black)  
    display.blit(e, (50, 300))
    display.blit(i, (203, 300))
    display.blit(h, (450, 300))
    
    f3 = pygame.font.SysFont('Arial', 20)
    instr = f3.render('Instructions: Use arrow keys to move your snake! Good luck!', True, (black))
    display.blit(instr, (30, 450))
    
    while menu:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if easy_rect.collidepoint(pos):
                    diff = 10
                    menu = False
                if medium_rect.collidepoint(pos):
                    diff = 20
                    menu = False
                if hard_rect.collidepoint(pos):
                    diff = 25
                    menu = False
            
        pygame.display.update()

#Waiting screen in between menu and the game      
def start():
    
    global black
    global white
    
    f = pygame.font.SysFont('Arial', 50)
    r = f.render('Ready', True, black)
    s = f.render('Set', True, black)
    g = f.render('GO', True, black)
    
    display.fill(white)
    display.blit(r, (260, 260))
    pygame.display.flip()
    pygame.time.wait(1500)
    display.fill(white)
    display.blit(s, (260, 260))
    pygame.display.flip()
    pygame.time.wait(1500)
    display.fill(white)
    display.blit(g, (260, 260))
    pygame.display.flip()
    pygame.time.wait(1500)
    display.fill(white)
    pygame.display.flip()
    
#Displays a screen when the player wins
def win():
    
    global black
    
    f = pygame.font.SysFont('Arial', 50)
    t = f.render('Congratulations, You Won!')
    display.blit(t, (200, 270))
    pygame.display.update()
    pygame.time.wait(3000)

#Displays a screen whenever the snake dies        
def die(display, score):
    
    global black
    
    f = pygame.font.SysFont('Arial', 30)
    t = f.render('Your score was: ' + str(score), True, black)
    display.blit(t, (10, 270))
    pygame.display.update()
    pygame.time.wait(3000)

#Method for in game functionalities
def in_game():

    global diff
    global white
    global black
    
    move = 0
    score = 0
    
    #Creating the snake/blob
    snake = pygame.Surface((20, 20))
    snake.fill((0, 255, 0))
    snake_x = [290, 290, 290, 290, 290]
    snake_y = [290, 270, 250, 230, 210]
    blob = pygame.Surface((10, 10))
    blob.fill((random.randint(0, 150), random.randint(0, 255), random.randint(0, 255)))
    blob_posx = (random.randint(10, 580))
    blob_posy = (random.randint(10, 580))
    
    while True:
        clock.tick(diff)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_UP and move != 0:move = 2
                elif event.key == K_DOWN and move != 2:move = 0
                elif event.key == K_LEFT and move != 1:move = 3
                elif event.key == K_RIGHT and move != 3:move = 1
            
        #Adjusts to snake array according to movement
        if move == 0:
            snake_y[0] += 20
        elif move == 1:
            snake_x[0] += 20
        elif move == 2:
            snake_y[0] -= 20
        elif move == 3:
            snake_x[0] -= 20

        #Keeps the snake together when moving
        i = len(snake_y)-1
        while i >= 1:
            snake_x[i] = snake_x[i-1]
            snake_y[i] = snake_y[i-1]
            i -= 1
        
        #Turn the snake head into a rectangle object
        snake_rect = pygame.Rect((snake_x[0], snake_y[0], 20, 20))
    
        #Events for collecting blobs
        if snake_rect.colliderect((blob_posx, blob_posy, 10, 10)):
            score += 1
            snake_x.append(700)
            snake_y.append(700)
            blob_posx = random.randint(10, 580)
            blob_posy = random.randint(10, 580)
            blob.fill((random.randint(0, 75), random.randint(0, 255), random.randint(0, 255)))
    
        #Colliding with self event
        i = len(snake_x)-1
        while i >= 2:
            if snake_rect.colliderect((snake_x[i], snake_y[i], 20, 20)):
                die(display, score)
                return False
            i -= 1
             
        #Colliding with screen event
        if snake_x[0] < 0 or snake_x[0] > 590 or snake_y[0] < 0 or snake_y[0] > 590:
            die(display, score)
            break
        
        #if player collects 300 blobs event
        if score == 300:
            win()
            break
        
        #Placing snake/blob/score on screen
        display.fill(white)
        for i in range(0, len(snake_x)):
            display.blit(snake, (snake_x[i], snake_y[i]))
        display.blit(blob, (blob_posx, blob_posy))
        t = f.render(str(score), True, black)
        display.blit(t, (10, 10))
        pygame.display.update()

#Restart screen used after death or if won        
def restart():
    
    global white
    global black
    
    display.fill(white)
    
    invis_rect1 = pygame.draw.rect(display, white, (60, 200, 160, 65))
    invis_rect2 = pygame.draw.rect(display, white, (290, 200, 250, 70))
    invis_rect3 = pygame.draw.rect(display, white, (250, 380, 75, 75))
    
    f = pygame.font.SysFont('Arial', 30)
    t2 = f.render('Play Again', True, (black))
    t3 = f.render('Change Difficulty', True, (black))
    t4 = f.render('Quit', True, (black))

    display.blit(t2, (75, 210))
    display.blit(t3, (300, 210))
    display.blit(t4, (260, 400))
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if invis_rect1.collidepoint(pos):
                    start()
                    in_game()
                    restart()
                if invis_rect2.collidepoint(pos):
                    main_menu()
                    start()
                    in_game()
                    restart()
                if invis_rect3.collidepoint(pos):
                    sys.exit(0)
        
        pygame.display.update()
 
def snake_game():
    main_menu()
    start()
    in_game()
    restart()
    
snake_game()
    


