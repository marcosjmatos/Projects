import time

import pygame
import numpy as np

pygame.init()

width, height = int(600), int(600)
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25

screen.fill(bg)

nxC, nyC = int(50), int(50)

dimCW = int(width / nxC)
dimCH = int(height / nyC)

gameState = np.zeros((nxC, nyC))

# automata Pulsar Pequeño
gameState[5, 3] = 1
gameState[3, 3] = 1
gameState[4, 3] = 1
gameState[4, 2] = 1
gameState[3, 2] = 1
gameState[2, 2] = 1

# Control de ejecucion
Pausar_Ejecucion = False


while True:

    newGameState = np.copy(gameState)

    screen.fill(bg)
    time.sleep(0.1)

    # registramos eventos con el teclado y mouse
    ev = pygame.event.get()

    for event in ev:

        # detectamos si se presiona una tecla,
        if event.type == pygame.KEYDOWN:
            Pausar_Ejecucion = not Pausar_Ejecucion

        # detectamos si se presiona el mouse
        mouse_click = pygame.mouse.get_pressed()

        if sum(mouse_click) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouse_click[2]

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not Pausar_Ejecucion:

                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                          gameState[x % nxC, (y - 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x - 1) % nxC, y % nyC] + \
                          gameState[(x + 1) % nxC, y % nyC] + \
                          gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                          gameState[x % nxC, (y + 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y + 1) % nyC]
                # Regla 1 "Una celula muerta con 3 vecinas vivas, revive"
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                # Regla 2 "Una celula viva con 2 vecinos o mas 3 3 Muere"
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0
            # Poligono de cada celda de dibujo
            poly = [(x * dimCW, y * dimCH),
                        ((x + 1) * dimCW, y * dimCH),
                        ((x + 1) * dimCW, (y + 1) * dimCH),
                        (x * dimCW, (y + 1) * dimCH)]

            if newGameState[x, y] == 0:
                    pygame.draw.polygon(screen, (128, 128, 128), poly, int(1))
            else:
                    pygame.draw.polygon(screen, (255, 255, 255), poly, int(0))

    # Actualizamos el estado de Juego.
    gameState = np.copy(newGameState)

    # Actualizamos la Pantalla.
    pygame.display.flip()
