import pandas as pd
import pygame
from random import randint
from settings import *

pygame.init()

dice_images = []
dice_rolling_images = []

for num in range(1,7):
    dice_image = pygame.image.load('Assets/dice/'+str(num)+'.png')
    dice_image = pygame.transform.scale(dice_image, (32, 32))
    dice_images.append(dice_image)

die_image_1 = dice_images[0]
die_image_2 = dice_images[1]
die_image_3 = dice_images[2]
die_image_4 = dice_images[3]
die_image_5 = dice_images[4]
die_image_6 = dice_images[5]

class DiceButton:
    def __init__(self):
        self.rect = pygame.Rect(1275, 775, 115, 115)
        self.color = yellow
        self.text = "Roll Dice"
        self.dice1 = None
        self.dice2 = None
        self.dice_total = 0
        self.rolls = {}
        self.roll_num = 0
        self.dice_images = []
        self.rolling_images = []
        for i in range (1,9):
            self.rolling_image = pygame.image.load(f'Assets/animation/roll{i}.png')
            self.rolling_image = pygame.transform.scale(self.rolling_image, (screen_height*(1/7), screen_height*(1/7)))
            self.rolling_images.append(self.rolling_image)
        for i in range (1,7):
            self.dice_image = pygame.image.load(f'Assets/dice/{i}.png')
            self.dice_image = pygame.transform.scale(self.dice_image, (screen_height*(1/14)*.5, screen_height*(1/14)*.5))
            self.dice_images.append(self.dice_image)
        self.font = pygame.font.SysFont('Algerian', 20)
        self.rolls_to_display = {}
        self.point_val = None
        self.point_on = False
        self.puck_on = pygame.image.load('Assets/puck/puck_on.png')
        self.puck_on = pygame.transform.scale(self.puck_on, (50,50))
        self.puck_off = pygame.image.load('Assets/puck/puck_off.png')
        self.puck_off = pygame.transform.scale(self.puck_off, (50,50))
    
    def create(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, black)
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text_surface, text_rect)
        x, y = 10, 10
        for roll_num, roll in self.rolls_to_display.items():
            dice1_index, dice2_index = None, None
            if roll["Dice 1"] in range(1, 7):
                dice1_index = int(roll["Dice 1"]) - 1
                screen.blit(self.dice_images[dice1_index], (x, y))
            if roll["Dice 2"] in range(1, 7):
                dice2_index = int(roll["Dice 2"]) - 1
                screen.blit(self.dice_images[dice2_index], (x, y+screen_height*(1/14)*.5))
            x += screen_height*(1/14)

    def handle_clicks(self, pos):
        if self.rect.collidepoint(pos):
            self.roll_dice()
            self.game_progress()
    
    def roll_dice(self):
        x, y = screen_width//3, screen_height//3
        for i in self.rolling_images:
            screen.blit(i, (x, y))
            screen.blit(i, (x-screen_height*(1/14),y))
            pygame.display.flip()
            pygame.time.wait(100)
        self.roll1 = randint(1,6)
        self.roll2 = randint(1,6)
        self.roll_sum = self.roll1 + self.roll2
        self.roll_num += 1
        self.rolls[self.roll_num] = {"Dice 1": self.roll1, "Dice 2": self.roll2, "Sum": self.roll_sum}
        if len(self.rolls) > 10:
            self.rolls_to_display = dict(list(self.rolls.items())[-10:])
        else:
            self.rolls_to_display = self.rolls
        pygame.display.update()
    
    def game_progress(self):
        if self.point_on == False:  
            if self.roll_sum in [4, 5, 6, 8, 9, 10]:
                self.roll_audio()
                self.point_val = self.roll_sum
                self.point_on = True                
            elif self.roll_sum in [7, 11]:
                self.roll_audio()
            else:
                self.roll_audio()
        elif self.point_on == True:
            if self.roll_sum == self.point_val:
                self.roll_audio()
                self.point_on = False
                self.point_val = None
            elif self.roll_sum in [4, 5, 6, 8, 9, 10]:
                self.roll_audio()
            elif self.roll_sum in [2, 3, 11, 12]:
                self.roll_audio()
            else:
                self.roll_audio()
                self.point_on = False
                self.point_val = None
    
    def puck_movement(self):
        if self.point_on == False:
            screen.blit(self.puck_off, (1158, 245))
        elif self.point_on == True and self.point_val == 4:
            screen.blit(self.puck_on, (10, 345))
        elif self.point_on == True and self.point_val == 5:
            screen.blit(self.puck_on, (200, 345))
        elif self.point_on == True and self.point_val == 6:
            screen.blit(self.puck_on, (390, 345))
        elif self.point_on == True and self.point_val == 8:
            screen.blit(self.puck_on, (580, 345))
        elif self.point_on == True and self.point_val == 9:
            screen.blit(self.puck_on, (770, 345))
        elif self.point_on == True and self.point_val == 10:
            screen.blit(self.puck_on, (960, 345))

    def roll_audio(self):
        self.off_sounds = {
            2: "Assets/audio/2off.wav",
            3: "Assets/audio/3off.wav",
            4: "Assets/audio/4easyoff.wav" if self.roll1 in [1, 3] else "Assets/audio/4hardoff.wav",
            5: "Assets/audio/5off.wav",
            6: "Assets/audio/6easyoff.wav" if self.roll1 in [1, 2, 4] else "Assets/audio/6hardoff.wav",
            7: "Assets/audio/7off.wav",
            8: "Assets/audio/8easyoff.wav" if self.roll1 in [2, 3, 5, 6] else "Assets/audio/8hardoff.wav",
            9: "Assets/audio/9off.wav",
            10: "Assets/audio/10easyoff.wav" if self.roll1 != 5 else "Assets/audio/10hardoff.wav",
            11: "Assets/audio/11off.wav",
            12: "Assets/audio/12off.wav"
        }
        self.on_sounds = {
            2: "Assets/audio/2on.wav",
            3: "Assets/audio/3on.wav",
            4: "Assets/audio/4easywinner.wav" if self.point_val == 4 and self.roll1 in [1, 3] else "Assets/audio/4easyon.wav" if self.roll1 in [1, 3] else "Assets/audio/4hardwinner.wav" if self.point_val == 4 else "Assets/audio/4hardon.wav",
            5: "Assets/audio/5winner.wav" if self.point_val == 5 else "Assets/audio/5on.wav",
            6: "Assets/audio/6easywinner.wav" if self.point_val == 6 and self.roll1 in [1, 2, 4, 5] else "Assets/audio/6easyon.wav" if self.roll1 in [1, 2, 4] else "Assets/audio/6hardwinner.wav" if self.point_val == 6 else "Assets/audio/6hardon.wav",
            7: "Assets/audio/7out.wav",
            8: "Assets/audio/8easywinner.wav" if self.point_val == 8 and self.roll1 in [2, 3, 5, 6] else "Assets/audio/8easyon.wav" if self.roll1 in [2, 3, 5, 6] else "Assets/audio/8hardwinner.wav" if self.point_val == 8 else "Assets/audio/8hardon.wav",
            9: "Assets/audio/9winner.wav" if self.point_val == 9 else "Assets/audio/9on.wav",
            10: "Assets/audio/10easywinner.wav" if self.point_val == 10 and self.roll1 in [4, 6] else "Assets/audio/10easyon.wav" if self.roll1 in [4, 6] else "Assets/audio/10hardwinner.wav" if self.point_val == 10 else "Assets/audio/10hardon.wav",
            11: "Assets/audio/11on.wav",
            12: "Assets/audio/12on.wav",
        }
        if self.point_on:
            self.sound = pygame.mixer.Sound(self.on_sounds[self.roll_sum])
        else:
            self.sound = pygame.mixer.Sound(self.off_sounds[self.roll_sum])
        self.sound.play()