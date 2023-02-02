import pygame

from crapstable import *
from settings import *
from chips import *
from dice import *
from player import *


# Create an instance of the CrapsTable class
table = CrapsTable(screen)  
dice_button = DiceButton()
player = Player()
chips = Chips(player)

# Main game loop
running = True
while running:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False    

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                player.select_chip(pos)
                chips.handle_clicks(event.pos)

            player.select_chip(event.pos)            
            dice_button.handle_clicks(event.pos)
    
    # Clear the screen
    screen.fill(dark_grey)
    
    # Draw the craps table
    table.table_background()
    table.draw_table()
    chips.create()
    dice_button.create()
    
    

    # Update the screen
    pygame.display.update()

    