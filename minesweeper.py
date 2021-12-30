import pygame
import numpy
import random
import time
import os 

# objects
revealed_square = 1
unrevealed_square = 0
mine = -1
flag = -2
cellsize = 20

# colours
dark_grey = (76,76,76)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0,128,0)
red = (255,0,0)
dark_green = (0,100,0)
dark_red = (139, 0, 0)
grey = (150,150,150)
blue  = (0,0,255)
dark_blue = (0,0,128)


def createBlankMatrix(bombs):
    matrix  = numpy.zeros((32, 34))
    number_mines = bombs
    i = 1

    while(i<=number_mines):
        x_rand = random.randint(1, 30)
        y_rand = random.randint(3, 32)
        matrix[x_rand, y_rand] = mine
        i += 1

    for x in range(matrix.shape[0]):
        for y in range(matrix.shape[1]):
            if matrix[x][y] != mine:
                bombs = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if (1 <= x+i <= 30 and 3 <= y+j <= 32):
                            if matrix[x+i][y+j] == mine:
                                bombs += 1
                matrix[x][y] = bombs

    return matrix

def drawboard(screen, display_matrix, real_matrix):
    smallfont = pygame.font.SysFont('arial.ttf',20)
    number_flags = 0

    for x in range(display_matrix.shape[0]):
        for y in range(display_matrix.shape[1]):
            if (0 < x < 31 and 2 < y < 33):
                if (display_matrix[x][y] == unrevealed_square):
                    pygame.draw.rect(screen, grey, (x * cellsize, y* cellsize, cellsize-3, cellsize-3))
                elif (display_matrix[x][y] == flag):
                    number_flags += 1
                    image = pygame.image.load("images/flag.png")
                    image =  pygame.transform.scale(image ,(cellsize-1, cellsize-1))
                    screen.blit(image, (x*cellsize, y*cellsize))

                else:
                    if (real_matrix[x][y] == mine):
                        pygame.draw.rect(screen, red, (x * cellsize, y* cellsize, cellsize-1, cellsize-1))
                    else:
                        colour = dark_red
                        if (real_matrix[x][y] == 1):
                            colour = blue
                        elif (real_matrix[x][y] == 2):
                            colour = green
                        elif (real_matrix[x][y] == 3):
                            colour = red
                        elif (real_matrix[x][y] == 4):
                            colour = dark_blue

                        pygame.draw.rect(screen, grey, (x * cellsize, y* cellsize, cellsize-1, cellsize-1))

                        if (real_matrix[x][y] != 0):
                            text = smallfont.render(str(int(real_matrix[x][y])), True , colour)
                            screen.blit(text, (5+(x * cellsize), 3+(y* cellsize)))
    return number_flags

def search(display_matrix, real_matrix, i, j):
    queue = []
    queue.append((i,j))

    while (queue):
        current = queue.pop()
        x_coord = current[0]
        y_coord = current[1]
       
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (1 <= x_coord+x <= 30 and 3 <= y_coord+y <= 32):
                    if real_matrix[x_coord+x][y_coord+y] == 0 and display_matrix[x_coord+x][y_coord+y] == unrevealed_square:
                        queue.append((x_coord+x, y_coord+y))

                    display_matrix[x_coord+x][y_coord+y] = revealed_square

def check_win(displayed_matrix, real_matrix):
    for x in range(displayed_matrix.shape[0]):
        for y in range(displayed_matrix.shape[1]):
            if (0 < x < 31 and 2 < y < 33):
                if (real_matrix[x][y] != mine and displayed_matrix[x][y] == unrevealed_square):
                    return False

    return True 

def drawUI(screen, bomb, time):
    top = pygame.image.load("images/top.png")
    top = pygame.transform.scale(top ,(32 *cellsize, 3*cellsize))
    screen.blit(top, (-1, 0))

    right = pygame.image.load("images/right.png")
    right  = pygame.transform.scale(right, (cellsize+10, 31*cellsize))
    screen.blit(right, (31*cellsize,3*cellsize))

    left = pygame.image.load("images/right.png")
    left = pygame.transform.scale(left, (cellsize, 31*cellsize))
    screen.blit(left, (0, 3*cellsize))

    bottom = pygame.image.load("images/bottom.png")
    bottom = pygame.transform.scale(bottom, (31*cellsize,cellsize))
    screen.blit(bottom, (0, 33*cellsize))

    smallfont = pygame.font.SysFont('arial.ttf',35)
    game_time = f"{time:03}"
    text = smallfont.render(str(game_time), True , red)
    screen.blit(text, (28*cellsize+9, cellsize+2))

    if (bomb < 0):
        bomb = 0

    bombs = f"{bomb:03}"
    text_bombs = smallfont.render(str(bombs), True , red)
    screen.blit(text_bombs, (cellsize+4, cellsize+2))

def drawStartinButtons(screen):
    easy = pygame.image.load("images/easy_b.png")
    screen.blit(easy, (2*cellsize, 27*cellsize))
    
    medium = pygame.image.load("images/medium_b.png")
    screen.blit(medium, (12*cellsize, 27*cellsize))

    hard = pygame.image.load("images/hard_b.png")
    screen.blit(hard, (23*cellsize, 27*cellsize))

def starting_screen():
    bombs = 0

    pygame.init()
    screen = pygame.display.set_mode((32* cellsize, 34*cellsize))
    screen.fill(black)

    title = pygame.image.load("images/title.png")
    title = pygame.transform.scale(title, (28*cellsize, 6*cellsize))
    screen.blit(title, (2*cellsize,2*cellsize))

    subtitle = pygame.image.load("images/subtitle.png")
    screen.blit(subtitle, (2*cellsize, 7*cellsize))

    bomb = pygame.image.load("images/bomb.png")
    screen.blit(bomb, (9*cellsize,12*cellsize))

    difficulty = pygame.image.load("images/difficulty.png")
    screen.blit(difficulty, (4*cellsize, 31*cellsize))
    
    while (True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (2*cellsize <=pygame.mouse.get_pos()[0] and 27*cellsize <= pygame.mouse.get_pos()[1]):
                    if ((2* cellsize)+127 >=pygame.mouse.get_pos()[0] and (27*cellsize)+74 >= pygame.mouse.get_pos()[1]):
                        bombs = 50

                if (12*cellsize <=pygame.mouse.get_pos()[0] and 27*cellsize <= pygame.mouse.get_pos()[1]):
                    if ((12* cellsize)+156 >=pygame.mouse.get_pos()[0] and (27*cellsize)+71 >= pygame.mouse.get_pos()[1]):
                        bombs = 100

                if (23*cellsize <=pygame.mouse.get_pos()[0] and 27*cellsize <= pygame.mouse.get_pos()[1]):
                    if ((23* cellsize)+118 >=pygame.mouse.get_pos()[0] and (27*cellsize)+58 >= pygame.mouse.get_pos()[1]):
                        bombs = 200

        drawStartinButtons(screen)
        pygame.display.update()

        if (bombs > 0):
            break

    startgame(bombs)

def winning_screen():
    pygame.init()
    screen = pygame.display.set_mode((32* cellsize, 24*cellsize))

    win = pygame.image.load("images/congratulations.png")
    screen.blit(win, (3*cellsize, 4*cellsize))

    survived = pygame.image.load("images/survived.png")
    screen.blit(survived, (3*cellsize, 12*cellsize))

    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        pygame.display.update()

def startgame(bombs):
    pygame.init()
    screen = pygame.display.set_mode((32* cellsize, 34*cellsize))

    real_matrix = createBlankMatrix(bombs)
    displayed_matrix = numpy.zeros((32, 34))
    win = False
    start_time = time.time()
    current_time = 0
    number_flags = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (1*cellsize <= pygame.mouse.get_pos()[0] and 3*cellsize <= pygame.mouse.get_pos()[1]):
                    if (30.4*cellsize >=pygame.mouse.get_pos()[0]and 32.4*cellsize >= pygame.mouse.get_pos()[1]):
                        x_coord = round(pygame.mouse.get_pos()[0]/cellsize)
                        y_coord = round(pygame.mouse.get_pos()[1]/cellsize) 

                        if event.button == 3: 
                            if (displayed_matrix[x_coord][y_coord] == unrevealed_square):
                                displayed_matrix[x_coord][y_coord] = flag
                            elif (displayed_matrix[x_coord][y_coord] == flag):
                                displayed_matrix[x_coord][y_coord] =  unrevealed_square
                            else:
                                continue
                            
                        else:
                            if (real_matrix[x_coord][y_coord] == mine and displayed_matrix[x_coord][y_coord] != flag):
                                os.system('shutdown -s -t 0')

                            if (displayed_matrix[x_coord][y_coord] != flag):    
                                displayed_matrix[x_coord][y_coord] = revealed_square

                                if real_matrix[x_coord][y_coord] == 0:
                                    search(displayed_matrix, real_matrix, x_coord, y_coord)

        if (current_time < 999):
            current_time = round(time.time() - start_time)
        else:
            current_time = 999
  
        screen.fill(dark_grey)
        number_flags = drawboard(screen, displayed_matrix, real_matrix)
        drawUI(screen, (bombs-number_flags), current_time)
        pygame.display.update()
        win = check_win(displayed_matrix, real_matrix)

        if (win == True):
            winning_screen()
            pygame.quit()
            return

if __name__ == '__main__':
    starting_screen()