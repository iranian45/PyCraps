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

# Game State
betting = 0 # to allow to players time to place bets
shooting = 1 # switch to activate the dice roll button
payouts = 2 # to animate chips being paid out

# set default state
state = betting

# Main game loop
running = True
while running:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False    

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                if state == betting:
                    chips.handle_clicks(event.pos)
                    player.handle_betting(event.pos)
                    # add timer for betting state to push to shooting state
                if state == shooting:
                    dice_button.handle_clicks(event.pos)
                    # add timer for shooting state then push to payouts state
                if state == payouts:
                    # Once bets are out and dice are rolled add animation for payouts
                    pass
                
    # Clear the screen
    screen.fill(dark_grey)
    
    # Draw the craps table
    table.table_background()
    table.draw_table()
    chips.create()
    dice_button.create()
    dice_button.puck_movement()
    
    # Update the screen
    pygame.display.update()

    #11

    