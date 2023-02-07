"""
Class 1: Player
-Attributes: name, chips, bets
-Methods: place_bet(), increase_bet(), collect_winnings(), update_chips()

Class 2: Bet
-Attributes: amount, odds, payout, type
-Methods: calculate_payout()

Class 3: Chip
-Attributes: value, color, location
-Methods: place_chip(), remove_chip()

Class 4: Dice
-Attributes: value1, value2
-Methods: roll_dice(), check_result()

Class 5: Game
-Attributes: players, bets, dice, point
-Methods: start_round(), end_round(), bet_phase(), payout_phase(), check_bets(), clear_bets()

Class 6: GUI 
-Attributes: display, chips, buttons
-Methods: display_board(), display_chips(), display_bets(), display_dice(), display_message(), display_players()

To Do:

Add stages to game (Betting, Shooting, Payouts)
Add Payout/Chip collection methods and update self.bets in player class to remove chips from accurate locations

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
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.chips = [Button(10, 830, 60, 60, '1', black, white, 30),
                      Button(80, 830, 60, 60, '5', black, red, 30),
                      Button(150, 830, 60, 60, '25', black, green, 30),
                      Button(220, 830, 60, 60, '100', black, light_grey, 30),
                      Button(290, 830, 60, 60, '500', black, light_purple, 30)]
        
        self.selected_chip = None
        self.bets = {}

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
                    self.balance -= self.selected_chip
                    if point in self.bets:
                        self.bets[point] += self.selected_chip
                    else:
                        self.bets[point] = self.selected_chip
                    print(f"You placed a {self.selected_chip} bet on {point}. Your new balance is {self.balance},..{self.bets}")
                    return self.bets
    
    def remove_bet(self, pos, point_rect_dict):
        if self.selected_chip is not None:
            for point, rect in point_rect_dict.items():
                if rect.collidepoint(pos):
                    if point in self.bets and self.selected_chip <= self.bets[point]:
                        self.balance += self.selected_chip
                        self.bets[point] -= self.selected_chip
                        print(f"You removed a {self.selected_chip} bet on {point}. Your new balance is {self.balance},..{self.bets}")
                    return self.bets
   
    def check_roll(self):
        for point, bet in self.bet.items():
            print(point)

class Dice:
    def __init__(self, display):
        self.display = display
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

        self.value1 = 0
        self.value2 = 0
        self.roll_data = {}
        self.roll_count = 0

    def roll_dice(self):
        self.roll_count += 1
        self.value1 = randint(1, 6)
        self.value2 = randint(1, 6)
        self.roll_history()
        self.roll_animation()
        self.last_ten_rolls()

    def roll_history(self):
        self.roll_data[self.roll_count] = {"Dice 1":self.value1, "Dice 2":self.value2, "Total":self.check_results()}
        print(self.roll_data)

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
        for num, roll in self.roll_data.items():
            dice1_index, dice2_index = None, None
            if roll["Dice 1"] in range(1, 7):
                dice1_index = int(roll["Dice 1"]) - 1
                self.display.blit(self.dice_images[dice1_index], (x, y))
            if roll["Dice 2"] in range (1, 7):
                dice2_index = int(roll["Dice 2"]) - 1
                self.display.blit(self.dice_images[dice2_index], (x, y+screen_height*(1/14)*.5))
            x += screen_height*(1/14)

def main():
    
    pygame.init()
    display = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Craps')
    
    gui = GUI(display)
    dice = Dice(display)

    roll_button = Button(1275, 775, 115, 115, "Roll", black, yellow, 40)
    gui.buttons.append(roll_button)
    player = Player("Amir", 500)

    running = True
    betting = True
    shooting = False
    payouts = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                               
                if betting == True:
                    player.select_chip(pos)
                    if event.button == 1:
                        player.place_bet(pos,gui.point_rect_dict)
                    elif event.button == 3:
                        player.remove_bet(pos, gui.point_rect_dict)
            
                if shooting == True:
                    for button in gui.buttons:
                        if button.is_clicked(pygame.mouse.get_pos()):
                            if button.text == "Roll":
                                dice.roll_dice()
                                betting, shooting = True, False
                        
                if payouts == True:
                    pass





        # update display
        current_time = pygame.time.get_ticks()
        gui.display_board()
        dice.last_ten_rolls()
        player.draw_chips(display)
        player.draw_bets(display, gui.point_rect_dict)

        pygame.display.update()

if __name__ == "__main__":
    main()

