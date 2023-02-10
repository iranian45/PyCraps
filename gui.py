"""
To Do:
Add Payout/Chip collection methods
update remove_bet method to remove full bet if selected chip is greater than the bet amount.
lock in contract bets when applicable
add more stats and UI items
add settings/menu pages
Add Audio
Add Multiplayer support
Add Dice input for physical rolls
"""

import pygame
from random import randint

# Screen 
screen_width = 1400
screen_height = 900

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

class Button:
    def __init__(self, x, y, width, height, text, text_color, button_color, size=20):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font('Assets/font/ALGER.TTF', size)

    def draw(self, display):
        pygame.draw.rect(display, self.button_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x + self.width/2, self.y + self.height/2)
        display.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
class Bet:
    def __init__(self, dice):
        self.bet_dict = {
            'pass_line': {'odds': 1/1},
            'do_not_pass': {'odds': 1/1}
        }
        self.dice = dice

    def check_results(self):
        if self.dice.point_on == False:
            pass

class GUI: 
    def __init__(self, display, width = screen_width, height = screen_height):
        self.display = display
        self.width = width
        self.height = height
        self.chips = []
        self.buttons = []
        self.point_rect_dict= {}
        self.dice = Dice(display)
        self.rolls_to_display = {}

    def add_button(self, button):
        self.buttons.append(button)

    def render_text_center(self, display, text, font, size, rect, color, x_offset=0, y_offset=0):
    # Render text function to apply text to rectangles
        font = pygame.font.Font("Assets/font/"+font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (rect.center[0] + x_offset, rect.center[1] + y_offset)
        self.display.blit(text_surface, text_rect)

    def display_board(self):
        self.display.fill(dark_grey)

        # Draw rectangles for box numbers
        x_offset = 0
        numbers = ['four', 'five', 'six', 'eight', 'nine', 'ten']
        for number in numbers:
            self.point_rect_dict[f"{number}_dont_come"] = pygame.Rect(10+x_offset, 235, 90, 55)
            self.point_rect_dict[f"{number}_dont_come_odds"] = pygame.Rect(100+x_offset, 235, 90, 55)
            self.point_rect_dict[f"{number}_blank"] = pygame.Rect(10+x_offset, 290, 90, 55)
            self.point_rect_dict[f"{number}_lay"] = pygame.Rect(100+x_offset, 290, 90, 55)
            self.point_rect_dict[f"{number}_center"] = pygame.Rect(10+x_offset, 345, 180, 55)
            self.point_rect_dict[f"{number}_come"] = pygame.Rect(10+x_offset, 400, 90, 55)
            self.point_rect_dict[f"{number}_come_odds"] = pygame.Rect(100+x_offset, 400, 90, 55)
            self.point_rect_dict[f"{number}_place"] = pygame.Rect(10+x_offset, 455, 90, 55)
            self.point_rect_dict[f"{number}_buy"] = pygame.Rect(100+x_offset, 455, 90, 55)
            x_offset += 190 # offet for next box set
        
        # set coordinates and sizes for other bet rectangles
        self.point_rect_dict['pass_line'] = pygame.Rect(670, 730, 545, 70)
        self.point_rect_dict['pass_line_odds'] = pygame.Rect(580, 730, 90, 70)
        self.point_rect_dict['dont_pass_line'] = pygame.Rect(670, 660, 545, 70)
        self.point_rect_dict['dont_pass_odds'] = pygame.Rect(580, 660, 90, 70)
        self.point_rect_dict['field'] = pygame.Rect(580, 590, 635, 70)
        self.point_rect_dict['come'] = pygame.Rect(580, 520, 635, 70)
        self.point_rect_dict['dont_come'] = pygame.Rect(1150, 235, 65, 275)
        self.point_rect_dict['any_seven'] = pygame.Rect(290, 520, 280, 55)
        self.point_rect_dict['horn_two'] = pygame.Rect(290, 575, 140, 85)
        self.point_rect_dict['horn_three'] = pygame.Rect(290, 660, 140, 85)
        self.point_rect_dict['horn_twelve'] = pygame.Rect(430, 575, 140, 85)
        self.point_rect_dict['horn_eleven'] = pygame.Rect(430, 660, 140, 85)          
        self.point_rect_dict['any_craps'] = pygame.Rect(290, 745, 280, 55)
        self.point_rect_dict['hard_four'] = pygame.Rect(10, 575, 130, 85)
        self.point_rect_dict['hard_six'] = pygame.Rect(10, 660, 130, 85)
        self.point_rect_dict['hard_eight'] = pygame.Rect(140, 660, 130, 85)
        self.point_rect_dict['hard_ten'] = pygame.Rect(140, 575, 130, 85)

        for point, rect in self.point_rect_dict.items():
            pygame.draw.rect(self.display, light_grey, rect, 2)

        for point in numbers:
        # Add text to the box numbers
            center = self.point_rect_dict[f'{point}_center']
            pygame.draw.rect(self.display, purple, center)
            
            text_values = [
                ("DONT", f"{point}_dont_come"),
                ("ODDS", f"{point}_dont_come_odds"),
                ("LAY", f"{point}_lay"),
                (point.upper(), f"{point}_center"),
                ("COME", f"{point}_come"),
                ("ODDS", f"{point}_come_odds"),
                ("PLACE", f"{point}_place"),
                ("BUY", f"{point}_buy"),
            ]
            for text, value in text_values:
                self.render_text_center(self.display, text, 'ALGER.TTF', 27, self.point_rect_dict[value], gold)

        # Text and dice for prop bets and other bets
        self.render_text_center(self.display, '30 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['horn_two'], white, y_offset=(self.point_rect_dict['horn_two'].bottom-self.point_rect_dict['horn_two'].centery)/2)
        self.display.blit(self.dice.dice_images[0], (self.point_rect_dict['horn_two'].centerx-34,self.point_rect_dict['horn_two'].centery-24))
        self.display.blit(self.dice.dice_images[0], (self.point_rect_dict['horn_two'].centerx ,self.point_rect_dict['horn_two'].centery-24))
        self.render_text_center(self.display, '15 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['horn_three'], white, y_offset=(self.point_rect_dict['horn_three'].bottom-self.point_rect_dict['horn_three'].centery)/2)
        self.display.blit(self.dice.dice_images[0], (self.point_rect_dict['horn_three'].centerx-34,self.point_rect_dict['horn_three'].centery-24))
        self.display.blit(self.dice.dice_images[1], (self.point_rect_dict['horn_three'].centerx ,self.point_rect_dict['horn_three'].centery-24))
        self.render_text_center(self.display, '7 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['hard_four'], white, y_offset=(self.point_rect_dict['hard_four'].bottom-self.point_rect_dict['hard_four'].centery)/2)
        self.display.blit(self.dice.dice_images[1], (self.point_rect_dict['hard_four'].centerx-34,self.point_rect_dict['hard_four'].centery-24))
        self.display.blit(self.dice.dice_images[1], (self.point_rect_dict['hard_four'].centerx ,self.point_rect_dict['hard_four'].centery-24))
        self.render_text_center(self.display, '9 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['hard_six'], white, y_offset=(self.point_rect_dict['hard_six'].bottom-self.point_rect_dict['hard_six'].centery)/2)
        self.display.blit(self.dice.dice_images[2], (self.point_rect_dict['hard_six'].centerx-34,self.point_rect_dict['hard_six'].centery-24))
        self.display.blit(self.dice.dice_images[2], (self.point_rect_dict['hard_six'].centerx ,self.point_rect_dict['hard_six'].centery-24))
        self.render_text_center(self.display, '9 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['hard_eight'], white, y_offset=(self.point_rect_dict['hard_eight'].bottom-self.point_rect_dict['hard_eight'].centery)/2)
        self.display.blit(self.dice.dice_images[3], (self.point_rect_dict['hard_eight'].centerx-34,self.point_rect_dict['hard_eight'].centery-24))
        self.display.blit(self.dice.dice_images[3], (self.point_rect_dict['hard_eight'].centerx ,self.point_rect_dict['hard_eight'].centery-24))
        self.render_text_center(self.display, '7 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['hard_ten'], white, y_offset=(self.point_rect_dict['hard_ten'].bottom-self.point_rect_dict['hard_ten'].centery)/2)
        self.display.blit(self.dice.dice_images[4], (self.point_rect_dict['hard_ten'].centerx-34,self.point_rect_dict['hard_ten'].centery-24))
        self.display.blit(self.dice.dice_images[4], (self.point_rect_dict['hard_ten'].centerx ,self.point_rect_dict['hard_ten'].centery-24))
        self.render_text_center(self.display, '15 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['horn_eleven'], white, y_offset=(self.point_rect_dict['horn_eleven'].bottom-self.point_rect_dict['horn_eleven'].centery)/2)
        self.display.blit(self.dice.dice_images[4], (self.point_rect_dict['horn_eleven'].centerx-34,self.point_rect_dict['horn_eleven'].centery-24))
        self.display.blit(self.dice.dice_images[5], (self.point_rect_dict['horn_eleven'].centerx ,self.point_rect_dict['horn_eleven'].centery-24))
        self.render_text_center(self.display, '30 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['horn_twelve'], white, y_offset=(self.point_rect_dict['horn_twelve'].bottom-self.point_rect_dict['horn_twelve'].centery)/2)
        self.display.blit(self.dice.dice_images[5], (self.point_rect_dict['horn_twelve'].centerx-34,self.point_rect_dict['horn_twelve'].centery-24))
        self.display.blit(self.dice.dice_images[5], (self.point_rect_dict['horn_twelve'].centerx ,self.point_rect_dict['horn_twelve'].centery-24))
        self.render_text_center(self.display, '4 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['any_seven'], white, x_offset=(self.point_rect_dict['any_seven'].right-self.point_rect_dict['any_seven'].centerx)/2+20)
        self.render_text_center(self.display, '4 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['any_seven'], white, x_offset=(self.point_rect_dict['any_seven'].left-self.point_rect_dict['any_seven'].centerx)/2-20)
        self.render_text_center(self.display, 'SEVEN', 'ALGER.TTF', 30, self.point_rect_dict['any_seven'], deep_red)
        self.render_text_center(self.display, "DON'T", 'ALGER.TTF', 20, self.point_rect_dict['dont_come'], deep_red,y_offset=-50)
        self.render_text_center(self.display, "COME", 'ALGER.TTF', 20, self.point_rect_dict['dont_come'], deep_red,y_offset=-30)
        self.render_text_center(self.display, "BAR", 'ALGER.TTF', 20, self.point_rect_dict['dont_come'], deep_red,y_offset=-10)
        self.display.blit(self.dice.dice_images[5], (self.point_rect_dict['dont_come'].left,self.point_rect_dict['dont_come'].centery))
        self.display.blit(self.dice.dice_images[5], (self.point_rect_dict['dont_come'].left+self.dice.dice_images[5].get_rect().width,self.point_rect_dict['dont_come'].centery))
        self.render_text_center(self.display, '7 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['any_craps'], white, x_offset=(self.point_rect_dict['any_craps'].right-self.point_rect_dict['any_craps'].centerx)/2+20)
        self.render_text_center(self.display, '7 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['any_craps'], white, x_offset=(self.point_rect_dict['any_craps'].left-self.point_rect_dict['any_craps'].centerx)/2-20)
        self.render_text_center(self.display, 'CRAPS', 'ALGER.TTF', 30, self.point_rect_dict['any_craps'], deep_red)
        self.render_text_center(self.display, 'COME', 'ALGER.TTF', 80, self.point_rect_dict['come'], deep_red)
        self.render_text_center(self.display, "DON'T PASS BAR", 'ALGER.TTF', 60, self.point_rect_dict['dont_pass_line'], deep_red, x_offset= -30)
        self.display.blit(self.dice.dice_images[5], (self.point_rect_dict['dont_pass_line'].right-self.dice.dice_images[5].get_rect().width*2-10,self.point_rect_dict['dont_pass_line'].centery-self.dice.dice_images[5].get_rect().height/2))
        self.display.blit(self.dice.dice_images[5], (self.point_rect_dict['dont_pass_line'].right-self.dice.dice_images[5].get_rect().width-5,self.point_rect_dict['dont_pass_line'].centery-self.dice.dice_images[5].get_rect().height/2))
        self.render_text_center(self.display, "PASS LINE", 'ALGER.TTF', 80, self.point_rect_dict['pass_line'], white)
        self.render_text_center(self.display, "2", 'ALGER.TTF', 30, self.point_rect_dict['field'], gold, x_offset=-250, y_offset= 5)
        pygame.draw.circle(self.display, light_grey,(self.point_rect_dict['field'].centerx-250, self.point_rect_dict['field'].centery+5),20,2)
        self.render_text_center(self.display, "PAYS DOUBLE", 'ALGER.TTF', 15, self.point_rect_dict['field'], gold, x_offset=-250, y_offset= -22)
        self.render_text_center(self.display, "3", 'ALGER.TTF', 30, self.point_rect_dict['field'], gold, x_offset=-150, y_offset= -15)
        self.render_text_center(self.display, "4", 'ALGER.TTF', 30, self.point_rect_dict['field'], gold, x_offset=-50, y_offset= -15)
        self.render_text_center(self.display, "9", 'ALGER.TTF', 30, self.point_rect_dict['field'], gold, y_offset= -15)
        self.render_text_center(self.display, "FIELD", 'ALGER.TTF', 30, self.point_rect_dict['field'], white, y_offset= 15)
        self.render_text_center(self.display, "10", 'ALGER.TTF', 30, self.point_rect_dict['field'], gold, x_offset=50, y_offset= -15)
        self.render_text_center(self.display, "11", 'ALGER.TTF', 30, self.point_rect_dict['field'], gold, x_offset=150, y_offset= -15)
        self.render_text_center(self.display, "12", 'ALGER.TTF', 30, self.point_rect_dict['field'], gold, x_offset=250, y_offset= 5)
        pygame.draw.circle(self.display, light_grey,(self.point_rect_dict['field'].centerx+250, self.point_rect_dict['field'].centery+5),20,2)
        self.render_text_center(self.display, "PAYS TRIPLE", 'ALGER.TTF', 15, self.point_rect_dict['field'], gold, x_offset=+250, y_offset= -22)

        # Roll Button
        for button in self.buttons:
            button.draw(self.display)
        
class Player:
    def __init__(self, name, balance, dice):
        self.name = name
        self.balance = balance
        self.chips = [Button(10, 830, 60, 60, '1', black, white, 30),
                      Button(80, 830, 60, 60, '5', black, red, 30),
                      Button(150, 830, 60, 60, '25', black, green, 30),
                      Button(220, 830, 60, 60, '100', black, light_grey, 30),
                      Button(290, 830, 60, 60, '500', black, light_purple, 30)]
        
        self.selected_chip = None
        self.bets = {}
        self.dice = dice

    def draw_chips(self, display):
        for chip in self.chips:
            chip.draw(display)

    def draw_bets(self, display, point_rect_dict):
        for point, bet in self.bets.items():
            if bet >= 500:
                color = light_purple
                pygame.draw.circle(display, black, (point_rect_dict[point].left+30,point_rect_dict[point].centery), 22, 2)
                pygame.draw.circle(display, color, (point_rect_dict[point].left+30,point_rect_dict[point].centery), 20)
                font = pygame.font.Font('Assets/font/ALGER.TTF',20)
                font_surf = font.render(str(bet), True, black)
                font_rect = font_surf.get_rect()
                font_rect.center = (point_rect_dict[point].left+30,point_rect_dict[point].centery)
                display.blit(font_surf, font_rect)
                return color
            elif bet >= 100:
                color = light_grey
                pygame.draw.circle(display, black, (point_rect_dict[point].left+30,point_rect_dict[point].centery), 22, 2)
                pygame.draw.circle(display, color, (point_rect_dict[point].left+30,point_rect_dict[point].centery), 20)
                font = pygame.font.Font('Assets/font/ALGER.TTF',20)
                font_surf = font.render(str(bet), True, black)
                font_rect = font_surf.get_rect()
                font_rect.center = (point_rect_dict[point].left+30,point_rect_dict[point].centery)
                display.blit(font_surf, font_rect)
            elif bet >= 25:
                color = green
                pygame.draw.circle(display, black, (point_rect_dict[point].left+30,point_rect_dict[point].centery), 22, 2)
                pygame.draw.circle(display, color, (point_rect_dict[point].left+30,point_rect_dict[point].centery), 20)
                font = pygame.font.Font('Assets/font/ALGER.TTF',20)
                font_surf = font.render(str(bet), True, black)
                font_rect = font_surf.get_rect()
                font_rect.center = (point_rect_dict[point].left+30,point_rect_dict[point].centery)
                display.blit(font_surf, font_rect)
            elif bet >= 5:
                color = red
                pygame.draw.circle(display, black, (point_rect_dict[point].left+30,point_rect_dict[point].centery), 22, 2)
                pygame.draw.circle(display, color, (point_rect_dict[point].left+30,point_rect_dict[point].centery), 20)
                font = pygame.font.Font('Assets/font/ALGER.TTF',20)
                font_surf = font.render(str(bet), True, black)
                font_rect = font_surf.get_rect()
                font_rect.center = (point_rect_dict[point].left+30,point_rect_dict[point].centery)
                display.blit(font_surf, font_rect)
            elif bet >=1:
                color = white
                pygame.draw.circle(display, black, (point_rect_dict[point].left+30,point_rect_dict[point].centery), 22, 2)
                pygame.draw.circle(display, color, (point_rect_dict[point].left+30,point_rect_dict[point].centery), 20)
                font = pygame.font.Font('Assets/font/ALGER.TTF',20)
                font_surf = font.render(str(bet), True, black)
                font_rect = font_surf.get_rect()
                font_rect.center = (point_rect_dict[point].left+30,point_rect_dict[point].centery)
                display.blit(font_surf, font_rect)

    def select_chip(self, pos):
        for button in self.chips:
            if button.is_clicked(pos):
                self.selected_chip = int(button.text)
                return self.selected_chip
            
    def place_bet(self, pos, point_rect_dict):
        if self.selected_chip is not None and self.balance >= self.selected_chip:
            for point, rect in point_rect_dict.items():
                if rect.collidepoint(pos):
                    if point not in ['four_dont_come', 'four_blank', 'four_center', 'four_come',
                        'five_dont_come', 'five_blank', 'five_center', 'five_come',
                        'six_dont_come', 'six_blank', 'six_center','six_come',
                        'eight_dont_come', 'eight_blank', 'eight_center', 'eight_come',
                        'nine_dont_come', 'nine_blank', 'nine_center', 'nine_come',
                        'ten_dont_come', 'ten_blank', 'ten_center', 'ten_come',]:

                        come_odds = [
                            ('four_come_odds', 'four_come'),
                            ('five_come_odds', 'five_come'),
                            ('six_come_odds', 'six_come'),
                            ('eight_come_odds', 'eight_come'),
                            ('nine_come_odds', 'nine_come'),
                            ('ten_come_odds', 'ten_come'),
                        ]

                        dont_come_odds = [
                            ('four_dont_come_odds', 'four_dont_come'),
                            ('five_dont_come_odds', 'five_dont_come'),
                            ('six_dont_come_odds', 'six_dont_come'),
                            ('eight_dont_come_odds', 'eight_dont_come'),
                            ('nine_dont_come_odds', 'nine_dont_come'),
                            ('ten_dont_come_odds', 'ten_dont_come'),
                        ]
                        line_odds = [
                            ('pass_line_odds', 'pass_line'),
                            ('dont_pass_odds', 'dont_pass_line')
                        ]

                        for odds, req in come_odds + dont_come_odds + line_odds:
                            if point == odds and req not in self.bets:
                                return self.bets

                        if self.dice.point_on == False:
                            if point not in ['come', 'dont_come', 'pass_line_odds', 'dont_pass_odds']:
                                self.balance -= self.selected_chip
                                if point in self.bets:
                                    self.bets[point] += self.selected_chip
                                else:
                                    self.bets[point] = self.selected_chip
                                # print(f"You placed a {self.selected_chip} bet on {point}. Your new balance is {self.balance},..{self.bets}")
                                return self.bets
                            
                        if self.dice.point_on:
                            if point not in ['dont_pass_line']:
                                self.balance -= self.selected_chip
                                if point in self.bets:
                                    self.bets[point] += self.selected_chip
                                else:
                                    self.bets[point] = self.selected_chip
                                # print(f"You placed a {self.selected_chip} bet on {point}. Your new balance is {self.balance},..{self.bets}")
                                return self.bets
         
    def remove_bet(self, pos, point_rect_dict):
        if self.selected_chip is not None:
            for point, rect in point_rect_dict.items():
                if rect.collidepoint(pos):
                    if point in self.bets and self.selected_chip <= self.bets[point]:
                        self.balance += self.selected_chip
                        self.bets[point] -= self.selected_chip
                        # print(f"You removed a {self.selected_chip} bet on {point}. Your new balance is {self.balance},..{self.bets}")
                    return self.bets
   
    def check_roll(self):
        self.roll_losses = 0
        self.roll_winnings = 0

        payouts = {}
        for bet, amount in self.bets.items():
            payouts[bet] = 0

            if bet == 'hard_four':
                # Win
                if self.dice.value1 == 2 and self.dice.value2 == 2:
                    payouts[bet] += amount * (7 / 1)
                # Loss
                elif self.dice.check_results() in [4, 7]:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'hard_six':
                # Win
                if self.dice.value1 == 3 and self.dice.value2 == 3:
                    payouts[bet] += amount * (9 / 1)
                # Loss
                elif self.dice.check_results() in [6, 7]:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'hard_eight':
                # Win
                if self.dice.value1 == 4 and self.dice.value2 == 4:
                    payouts[bet] += amount * (9 / 1)
                # Loss
                elif self.dice.check_results() in [8, 7]:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'hard_ten':
                # Win
                if self.dice.value1 == 5 and self.dice.value2 == 5:
                    payouts[bet] += amount * (7 / 1)
                # Loss
                elif self.dice.check_results() in [10, 7]:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'any_seven':
                # Win
                if self.dice.check_results() == 7:
                    payouts[bet] += amount * (4 / 1)
                # Loss
                else:
                    payouts[bet] -= amount
                    self.bets[bet] = 0
            
            if bet == 'any_craps':
                # Win
                if self.dice.check_results() in [2, 3, 12]:
                    payouts[bet] += amount * (7 / 1)
                # Loss
                else:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'horn_two':
                # Win
                if self.dice.check_results() == 2:
                    payouts[bet] += amount * (30 / 1)
                # Loss
                else:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'horn_three':
                # Win
                if self.dice.check_results() == 3:
                    payouts[bet] += amount * (15 / 1)
                # Loss
                else:
                    payouts[bet] -= amount
                    self.bets[bet] = 0
            
            if bet == 'horn_eleven':
                # Win
                if self.dice.check_results() == 11:
                    payouts[bet] += amount * (15 / 1)
                # Loss
                else:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'horn_twelve':
                # Win
                if self.dice.check_results() == 12:
                    payouts[bet] += amount * (30 / 1)
                # Loss
                else:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'field':
                # Win
                if self.dice.check_results() in [2, 3, 4, 9, 10, 11, 12]:
                    payouts[bet] += amount * (1 / 1)
                # Loss
                else:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'come':
                # Win
                if self.dice.check_results() in [7, 11]:
                    payouts[bet] += amount
                # Loss
                elif self.dice.check_results() in [2, 3, 12]:
                    payouts[bet] -= amount
                    self.bets[bet] = 0
            
            if bet == 'dont_come':
                # Win
                if self.dice.check_results() in [2, 3]:
                    payouts[bet] += amount
                # Loss
                elif self.dice.check_results() in [7, 11]:
                    payouts[bet] -= amount
                    self.bets[bet] = 0
            
            if bet == 'dont_pass_line':
                if self.dice.point_on == False:
                    if self.dice.check_results() in [2, 3]:
                        payouts[bet] += amount
                    elif self.dice.check_results() in [7, 11]:
                        payouts[bet] -= amount
                        self.bets[bet] = 0
                elif self.dice.point_on:
                    if self.dice.check_results == 7:
                        payouts[bet] += amount
                    elif self.dice.point_value == self.dice.check_results():
                        payouts[bet] -= amount
                        self.bets[bet] = 0
            
            if bet == 'dont_pass_odds':   
                if self.dice.check_results == 7:
                    if self.dice.point_value in [4, 10]:
                        payouts[bet] += amount * (1 / 2)
                    if self.dice.point_value in [5, 9]:
                        payouts[bet] += amount * (2 / 3)
                    if self.dice.point_value in [6, 8]:
                        payouts[bet] += amount * (5 / 6)
                elif self.dice.point_value == self.dice.check_results():
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'pass_line':
                if self.dice.point_on == False:
                    if self.dice.check_results() in [7, 1]:
                        payouts[bet] += amount
                    elif self.dice.check_results() in [2, 3, 12]:
                        payouts[bet] -= amount
                        self.bets[bet] = 0
                elif self.dice.point_on:
                    if self.dice.check_results == 7:
                        payouts[bet] -= amount
                        self.bets[bet] = 0
                    elif self.dice.point_value == self.dice.check_results():
                        payouts[bet] += amount
            
            if bet == 'pass_line_odds':   
                if self.dice.check_results == self.dice.check_results():
                    if self.dice.point_value in [4, 10]:
                        payouts[bet] += amount * (2 / 1)
                    if self.dice.point_value in [5, 9]:
                        payouts[bet] += amount * (3 / 2)
                    if self.dice.point_value in [6, 8]:
                        payouts[bet] += amount * (6 / 5)
                elif self.dice.point_value == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'four_dont':
                if self.dice.check_results() == 7:
                    payouts[bet] += amount
                elif self.dice.check_results() == 4:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'four_dont_odds':
                if self.dice.check_results() == 7:
                    payouts[bet] += amount * (1 / 2)
                elif self.dice.check_results() == 4:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'four_lay':
                if self.dice.check_results() == 7:
                    payouts[bet] += (amount * (1 / 2)) - (amount * .05)
                elif self.dice.check_results() == 4:
                    payouts[bet] -= amount
                    self.bets[bet] = 0
            
            if bet == 'four_come':
                if self.dice.check_results() == 4:
                    payouts[bet] += amount
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'four_come_odds':
                if self.dice.check_results() == 4:
                    payouts[bet] += amount * (2 / 1)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'four_buy':
                if self.dice.check_results() == 4:
                    payouts[bet] += (amount * (2 / 1)) - (amount * .05)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0
                
            if bet == 'four_place':
                if self.dice.check_results() == 4:
                    payouts[bet] += amount * (9 / 5)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'ten_dont':
                if self.dice.check_results() == 7:
                    payouts[bet] += amount
                elif self.dice.check_results() == 10:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'ten_dont_odds':
                if self.dice.check_results() == 7:
                    payouts[bet] += amount * (1 / 2)
                elif self.dice.check_results() == 10:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'ten_lay':
                if self.dice.check_results() == 7:
                    payouts[bet] += (amount * (1 / 2)) - (amount * .05)
                elif self.dice.check_results() == 10:
                    payouts[bet] -= amount
                    self.bets[bet] = 0
            
            if bet == 'ten_come':
                if self.dice.check_results() == 10:
                    payouts[bet] += amount
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'ten_come_odds':
                if self.dice.check_results() == 10:
                    payouts[bet] += amount * (2 / 1)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'ten_buy':
                if self.dice.check_results() == 10:
                    payouts[bet] += (amount * (2 / 1)) - (amount * .05)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0
                
            if bet == 'ten_place':
                if self.dice.check_results() == 10:
                    payouts[bet] += amount * (9 / 5)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'five_dont':
                if self.dice.check_results() == 7:
                    payouts[bet] += amount
                elif self.dice.check_results() == 5:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'five_dont_odds':
                if self.dice.check_results() == 7:
                    payouts[bet] += amount * (2 / 3)
                elif self.dice.check_results() == 5:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'five_lay':
                if self.dice.check_results() == 7:
                    payouts[bet] += (amount * (2 / 3)) - (amount * .05)
                elif self.dice.check_results() == 5:
                    payouts[bet] -= amount
                    self.bets[bet] = 0
            
            if bet == 'five_come':
                if self.dice.check_results() == 5:
                    payouts[bet] += amount
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'five_come_odds':
                if self.dice.check_results() == 5:
                    payouts[bet] += amount * (3 / 2)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'five_buy':
                if self.dice.check_results() == 5:
                    payouts[bet] += (amount * (3 / 2)) - (amount * .05)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0
                
            if bet == 'five_place':
                if self.dice.check_results() == 5:
                    payouts[bet] += amount * (7 / 5)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'nine_dont':
                if self.dice.check_results() == 7:
                    payouts[bet] += amount
                elif self.dice.check_results() == 9:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'nine_dont_odds':
                if self.dice.check_results() == 7:
                    payouts[bet] += amount * (2 / 3)
                elif self.dice.check_results() == 9:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'nine_lay':
                if self.dice.check_results() == 7:
                    payouts[bet] += (amount * (2 / 3)) - (amount * .05)
                elif self.dice.check_results() == 9:
                    payouts[bet] -= amount
                    self.bets[bet] = 0
            
            if bet == 'nine_come':
                if self.dice.check_results() == 9:
                    payouts[bet] += amount
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'nine_come_odds':
                if self.dice.check_results() == 9:
                    payouts[bet] += amount * (3 / 2)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'nine_buy':
                if self.dice.check_results() == 9:
                    payouts[bet] += (amount * (3 / 2)) - (amount * .05)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0
                
            if bet == 'nine_place':
                if self.dice.check_results() == 9:
                    payouts[bet] += amount * (7 / 5)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'six_dont':
                if self.dice.check_results() == 7:
                    payouts[bet] += amount
                elif self.dice.check_results() == 6:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'six_dont_odds':
                if self.dice.check_results() == 7:
                    payouts[bet] += amount * (5 / 6)
                elif self.dice.check_results() == 6:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'six_lay':
                if self.dice.check_results() == 7:
                    payouts[bet] += (amount * (5 / 6)) - (amount * .05)
                elif self.dice.check_results() == 6:
                    payouts[bet] -= amount
                    self.bets[bet] = 0
            
            if bet == 'six_come':
                if self.dice.check_results() == 6:
                    payouts[bet] += amount
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'six_come_odds':
                if self.dice.check_results() == 6:
                    payouts[bet] += amount * (6 / 5)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'six_buy':
                if self.dice.check_results() == 6:
                    payouts[bet] += (amount * (6 / 5)) - (amount * .05)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0
                
            if bet == 'six_place':
                if self.dice.check_results() == 6:
                    payouts[bet] += amount * (7 / 6)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0            

            if bet == 'eight_dont':
                if self.dice.check_results() == 7:
                    payouts[bet] += amount
                elif self.dice.check_results() == 8:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'eight_dont_odds':
                if self.dice.check_results() == 7:
                    payouts[bet] += amount * (5 / 6)
                elif self.dice.check_results() == 8:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'eight_lay':
                if self.dice.check_results() == 7:
                    payouts[bet] += (amount * (5 / 6)) - (amount * .05)
                elif self.dice.check_results() == 8:
                    payouts[bet] -= amount
                    self.bets[bet] = 0
            
            if bet == 'eight_come':
                if self.dice.check_results() == 8:
                    payouts[bet] += amount
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'eight_come_odds':
                if self.dice.check_results() == 8:
                    payouts[bet] += amount * (6 / 5)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount
                    self.bets[bet] = 0

            if bet == 'eight_buy':
                if self.dice.check_results() == 8:
                    payouts[bet] += (amount * (6 / 5)) - (amount * .05)
                elif self.dice.check_results() == 8:
                    payouts[bet] -= amount
                    self.bets[bet] = 0
                
            if bet == 'eight_place':
                if self.dice.check_results() == 8:
                    payouts[bet] += amount * (7 / 6)
                elif self.dice.check_results() == 7:
                    payouts[bet] -= amount 
                    self.bets[bet] = 0
        self.roll_losses = sum(value for value in payouts.values() if value < 0)
        self.roll_winnings = sum(value for value in payouts.values() if value > 0)
        payouts = {k: v for k, v in payouts.items() if v != 0}
        print(payouts)
        print(f'Winnings: {self.roll_winnings} - Losses: {abs(self.roll_losses)} = {self.roll_winnings+self.roll_losses}')
        return payouts,self.roll_losses, self.roll_winnings            
            
    def post_roll(self):
        # Move Come Bets
        if 'come' in self.bets:
            if self.dice.check_results() == 4:
                if 'four_come' in self.bets:
                    self.bets['four_come'] += self.bets['come']
                else:
                    self.bets['four_come'] = self.bets['come']
                del self.bets['come']
            elif self.dice.check_results() == 5:
                if 'five_come' in self.bets:
                    self.bets['five_come'] += self.bets['come']
                else:
                    self.bets['five_come'] = self.bets['come']
                del self.bets['come']
            elif self.dice.check_results() == 6:
                if 'six_come' in self.bets:
                    self.bets['six_come'] += self.bets['come']
                else:
                    self.bets['six_come'] = self.bets['come']
                del self.bets['come']
            elif self.dice.check_results() == 8:
                if 'eight_come' in self.bets:
                    self.bets['eight_come'] += self.bets['come']
                else:
                    self.bets['eight_come'] = self.bets['come']
                del self.bets['come']
            elif self.dice.check_results() == 9:
                if 'nine_come' in self.bets:
                    self.bets['nine_come'] += self.bets['come']
                else:
                    self.bets['nine_come'] = self.bets['come']
                del self.bets['come']
            elif self.dice.check_results() == 10:
                if 'ten_come' in self.bets:
                    self.bets['ten_come'] += self.bets['come']
                else:
                    self.bets['ten_come'] = self.bets['come']    
                del self.bets['come'] 
        # Move Dont Come Bets
        if 'dont_come' in self.bets:
            if self.dice.check_results() == 4:
                if 'four_dont_come' in self.bets:
                    self.bets['four_dont_come'] += self.bets['dont_come']
                else:
                    self.bets['four_dont_come'] = self.bets['dont_come']
                del self.bets['dont_come']
            elif self.dice.check_results() == 5:
                if 'five_dont_come' in self.bets:
                    self.bets['five_dont_come'] += self.bets['dont_come']
                else:
                    self.bets['five_dont_come'] = self.bets['dont_come']
                del self.bets['dont_come']
            elif self.dice.check_results() == 6:
                if 'six_dont_come' in self.bets:
                    self.bets['six_dont_come'] += self.bets['dont_come']
                else:
                    self.bets['six_dont_come'] = self.bets['dont_come']
                del self.bets['dont_come']
            elif self.dice.check_results() == 8:
                if 'eight_dont_come' in self.bets:
                    self.bets['eight_dont_come'] += self.bets['dont_come']
                else:
                    self.bets['eight_dont_come'] = self.bets['dont_come']
                del self.bets['dont_come']
            elif self.dice.check_results() == 9:
                if 'nine_dont_come' in self.bets:
                    self.bets['nine_dont_come'] += self.bets['dont_come']
                else:
                    self.bets['nine_dont_come'] = self.bets['dont_come']
                del self.bets['dont_come']
            elif self.dice.check_results() == 10:
                if 'ten_dont_come' in self.bets:
                    self.bets['ten_dont_come'] += self.bets['dont_come']
                else:
                    self.bets['ten_dont_come'] = self.bets['dont_come']    
                del self.bets['dont_come']
        # Clear losses
        self.bets = {k: v for k, v in self.bets.items() if v != 0}
        # Pay winners
        print(f'Previous Balance: {self.balance} + Wins/Losses {self.roll_winnings+self.roll_losses} = {self.balance+(self.roll_winnings+self.roll_losses)}')
        self.balance += (self.roll_winnings)
        
    def display_account(self, display):
        font = pygame.font.Font('Assets/font/ALGER.TTF', 30)

        bets_text = font.render(str(round(sum(self.bets.values()),2)), True, black)
        bets_text_rect = bets_text.get_rect()
        bets_text_rect.right = 1390
        bets_text_rect.top = 10
        display.blit(bets_text, bets_text_rect)

        bets_label = font.render('My Bets: ', True, black)
        bets_label_rect = bets_label.get_rect()
        bets_label_rect.top = bets_text_rect.top
        bets_label_rect.right = bets_text_rect.left
        display.blit(bets_label, bets_label_rect)
        
        balance_text = font.render(str(round(self.balance,2)),True, black)
        balance_text_rect = balance_text.get_rect()
        balance_text_rect.topright = bets_text_rect.bottomright
        display.blit(balance_text, balance_text_rect)
        
        balance_label = font.render('Balance: ', True, black)
        balance_label_rect = balance_label.get_rect()
        balance_label_rect.bottomright = balance_text_rect.bottomleft
        display.blit(balance_label, balance_label_rect)

        pygame.draw.line(display, white, balance_label_rect.topleft, bets_text_rect.bottomright, 1)
        

        



        
class Dice:
    def __init__(self, display):
        self.display = display
        self.dice_images = []
        self.rolling_images = []
        self.rolls_to_display = {}
        for i in range (1,9):
            self.rolling_image = pygame.image.load(f'Assets/animation/roll{i}.png')
            self.rolling_image = pygame.transform.scale(self.rolling_image, (screen_height*(1/7), screen_height*(1/7)))
            self.rolling_images.append(self.rolling_image)
        for i in range (1,7):
            self.dice_image = pygame.image.load(f'Assets/dice/{i}.png')
            self.dice_image = pygame.transform.scale(self.dice_image, (screen_height*(1/14)*.5, screen_height*(1/14)*.5))
            self.dice_images.append(self.dice_image)

        self.value1 = 0
        self.value2 = 0
        self.roll_data = {}
        self.roll_count = 0

        self.point_value = None
        self.point_on = False
        self.puck_on = pygame.image.load('Assets/puck/puck_on.png')
        self.puck_on = pygame.transform.scale(self.puck_on, (50,50))
        self.puck_off = pygame.image.load('Assets/puck/puck_off.png')
        self.puck_off = pygame.transform.scale(self.puck_off, (50,50))

    def check_point(self):
        if not self.point_on:
            if self.check_results() in [4, 5, 6, 8, 9, 10]:
                self.point_value = self.check_results()
                self.point_on = True
                # print(f'the point is {self.point_value}')
            else:
                pass
                # print('the point is off')
        else:
            if self.check_results() == 7 or self.check_results() == self.point_value:
                self.point_on = False
                self.point_value = None
                # print('Point is off')
            else:
                pass
                # print(f'point is {self.point_value}')

    def puck_movement(self, display):
        if self.point_on == False:
            display.blit(self.puck_off, (1158, 245))
        elif self.point_on == True and self.point_value == 4:
            display.blit(self.puck_on, (10, 345))
        elif self.point_on == True and self.point_value == 5:
            display.blit(self.puck_on, (200, 345))
        elif self.point_on == True and self.point_value == 6:
            display.blit(self.puck_on, (390, 345))
        elif self.point_on == True and self.point_value == 8:
            display.blit(self.puck_on, (580, 345))
        elif self.point_on == True and self.point_value == 9:
            display.blit(self.puck_on, (770, 345))
        elif self.point_on == True and self.point_value == 10:
            display.blit(self.puck_on, (960, 345))


    def roll_dice(self):
        self.roll_count += 1
        self.value1 = randint(1, 6)
        self.value2 = randint(1, 6)
        self.roll_history()
        self.roll_animation()
        if self.roll_count > 10:
            self.rolls_to_display = dict(list(self.roll_data.items())[-10:])
        else:
            self.rolls_to_display = self.roll_data
        print(self.value1+self.value2)

    def roll_history(self):
        self.roll_data[self.roll_count] = {"Dice 1":self.value1, "Dice 2":self.value2, "Total":self.check_results()}
        # print(self.roll_data)

    def check_results(self):
        total = self.value1 + self.value2
        return total
    
    def roll_animation(self):
        x, y = screen_width//3, screen_height//3
        for i in self.rolling_images:
            self.display.blit(i, (x, y))
            self.display.blit(i, (x-screen_height*(1/14),y))
            pygame.display.flip()
            pygame.time.wait(100)

    def last_ten_rolls(self):
        x, y = 10, 10
        for num, roll in self.rolls_to_display.items():
            dice1_index, dice2_index = None, None
            if roll["Dice 1"] in range(1, 7):
                dice1_index = int(roll["Dice 1"]) - 1
                self.display.blit(self.dice_images[dice1_index], (x, y))
            if roll["Dice 2"] in range (1, 7):
                dice2_index = int(roll["Dice 2"]) - 1
                self.display.blit(self.dice_images[dice2_index], (x, y+screen_height*(1/14)*.5))
            x += screen_height*(1/14)

    

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Craps')
        self.clock = pygame.time.Clock()

        self.gui = GUI(self.display)
        self.dice = Dice(self.display)

        self.roll_button = Button(1275, 775, 115, 115, "Roll", black, yellow, 40)
        self.gui.buttons.append(self.roll_button)

        self.running = True
        self.player = Player("Amir", 500, self.dice)   

        self.state = 'betting'
        self.time_status = 'start'
        self.start_time = 0

    def run(self):        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.state == 'betting':
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()               
                        self.player.select_chip(pos)
                        if event.button == 1:
                            self.player.place_bet(pos,self.gui.point_rect_dict)
                        elif event.button == 3:
                            self.player.remove_bet(pos, self.gui.point_rect_dict)
                    if self.time_status == 'start':
                        self.start_time = pygame.time.get_ticks()
                        self.time_status = 'stop'
                    if self.time_status == 'stop':
                        current_time = pygame.time.get_ticks()
                        elapsed_time = (current_time-self.start_time) /1000
                        # print(elapsed_time)
                        if elapsed_time >= 60:
                            print('shooting')
                            self.state = 'shooting'
                    
                elif self.state in 'shooting':                      
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()   
                        for button in self.gui.buttons:
                            if button.is_clicked(pygame.mouse.get_pos()):
                                if button.text == "Roll":
                                    self.state = 'betting'
                                    self.start_time = pygame.time.get_ticks()
                                    self.dice.roll_dice()
                                    self.player.check_roll()
                                    self.dice.check_point()
                                    self.player.post_roll()
                                    print('betting')
                                    

            # update display
            current_time = pygame.time.get_ticks()
            self.gui.display_board()
            self.dice.last_ten_rolls()
            self.player.draw_chips(self.display)
            self.player.draw_bets(self.display, self.gui.point_rect_dict)
            self.dice.puck_movement(self.display)
            self.player.display_account(self.display)

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()

