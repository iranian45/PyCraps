import pygame

# Initizlize Pygame and set Screen info
pygame.init()
pygame.display.set_caption('')
info = pygame.display.Info()
screen_width = 1400
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

# Set Colors 
light_grey = (100,100,100)
dark_grey = (50,50,50)
deep_red = (175,0,0)
purple = (40,2,60)
gold = (212,175,55)
red = (133, 41, 40)
white = (255, 255, 255)
black = (0, 0, 0)
green = (53, 101, 77)
orange = (206, 75, 41)
light_purple = (123, 90, 148)
yellow = (238, 195, 93)

bets_dict = {
    "horn_two": {
        "rect":(290, 575, 140, 85), 
        "odds": (30/1),
        "win_condition": {
            (1,1)
        },
    },
    "horn_three":{
        "rect": (290, 660, 140, 85),
        "odds": (15/1),
        "win_condition":{
            (1,2),
            (2,1)
        }
    },
    "horn_eleven": {
        "rect":(430, 660, 140, 85),
        "odds":(15/1),
        "win_condition": {
            (5,6),
            (6,5)
        }
    },
    "horn_twelve":{
        "rect": (430, 575, 140, 85),
        "odds":(15/1),
        "win_condition":{
            (6,6)
        }
    },
    "any_craps":{
        "rect": (),
        "odds": (7/1),
        "win_condition":{
            (1,1),
            (1,2),
            (2,1),
            (6,6),
        }
    },
    "any_seven": {
        "rect": (),
        "odds":(4/1),
        "win_condition": {
            (1,6),
            (2,5),
            (3,4),
            (4,3),
            (5,2),
            (6,1)
        }
    },
    "field": {
        "rect": (),
        "odds": (1/1),
        "win_condition":{
            (1,1)
        }
    }
}

