import pygame
import numpy as np

from random import randint


pygame.init()


unitsInLength = 80
unitsInHeight = 50

unitSize = 20

canvasLength = unitsInLength * unitSize
canvasHeight = unitsInHeight * unitSize



infinityGrid = True

renderDelay = 5
lifeDelay = 400

run = True
runLife = False

draw = False
mousePressed = False


win = pygame.display.set_mode((canvasLength, canvasHeight))

pygame.display.set_caption("Game of Life")

lifeGrid = np.zeros((unitsInHeight, unitsInLength), dtype=int)

print(lifeGrid.shape)


def draw_lifeGrid():
    for row in range(len(lifeGrid)):
        for col in range(len(lifeGrid[row])):
            if lifeGrid[row, col] == 0:
                pygame.draw.rect(win, (255, 255, 255), (col * 20, row * 20, unitSize, unitSize), 1)
            else:
                pygame.draw.rect(win, (255, 255, 255), (col * 20, row * 20, unitSize, unitSize))


def mouse_controlls():

    xpos, ypos = pygame.mouse.get_pos()

    xi = int(xpos / unitSize)
    yi = int(ypos / unitSize)

    if draw:
        lifeGrid[yi, xi] = 0
    else:
        lifeGrid[yi, xi] = 1
    

def key_controlls(keys):
    global draw, lifeGrid, runLife, renderDelay, lifeDelay


    if not runLife:
        if keys[pygame.K_d]:
            draw = not draw
        if keys[pygame.K_c]:
            lifeGrid = np.zeros((unitsInHeight, unitsInLength), dtype=int)
        if keys[pygame.K_SPACE]:
            runLife = True
            renderDelay = lifeDelay
        if keys[pygame.K_r]:
            randomize_life()
        return

    if runLife:
        if keys[pygame.K_SPACE]:
            runLife = False
            renderDelay = 5


def event_handler():
    global run, mousePressed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mousePressed = False

        if event.type == pygame.KEYDOWN:
            key_controlls(pygame.key.get_pressed())


def randomize_life():
    global lifeGrid

    for row in range(len(lifeGrid)):
        for col in range(len(lifeGrid[row])):
            lifeGrid[row, col] = randint(0, 1)

    print("randomized")


def count_living_cells_neighbours(row, col):
    global lifeGrid

    count = 0

    c_row = row - 1
    c_col = col - 1

    for i_row in range(c_row, c_row+3):
        for i_col in range(c_col, c_col+3):
            try:

                if i_row == row and i_col == col:
                    continue

                if lifeGrid[i_row, i_col]:
                    count += 1
            except IndexError:
                errRow = i_row
                errCol = i_col

                if i_row == unitsInHeight and i_col == unitsInLength:
                    errRow = 0
                    errCol = 0
                elif i_row == unitsInHeight:
                    errRow = 0
                elif i_col == unitsInLength:
                    errCol = 0

                if lifeGrid[errRow, errCol]:
                    count += 1

    return count


def iterate_life():
    global lifeGrid

    newLifeGrid = np.zeros((unitsInHeight, unitsInLength), dtype=int)

    for row in range(len(lifeGrid)):
        for col in range(len(lifeGrid[row])):
            live_cell_neighbours = count_living_cells_neighbours(row, col)

            # if cell alive
            if lifeGrid[row, col]:
                print("Cell alive with", live_cell_neighbours, "neighbours")
                if live_cell_neighbours == 2 or live_cell_neighbours == 3:
                    print("celle overlever")
                    newLifeGrid[row, col] = 1
            # if cell dead
            else:
                print("Cell dead with", live_cell_neighbours, "neighbours")
                if live_cell_neighbours == 3:
                    print("celle fødes")
                    newLifeGrid[row, col] = 1


    print()

    lifeGrid = newLifeGrid

    print(newLifeGrid)
    print(lifeGrid)





while run:
    pygame.time.delay(renderDelay)

    event_handler()
    
    if not runLife and mousePressed:
        mouse_controlls()

    if runLife:
        iterate_life()
        
    win.fill((0, 0, 0))

    draw_lifeGrid()

    pygame.display.update()