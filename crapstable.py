import pygame
from settings import *
from dice import *

class CrapsTable:
    def __init__(self, screen):
        self.screen = screen
        self.table_rect = pygame.Rect(0, 0, screen_width, screen_height)

        numbers = ['four', 'five', 'six', 'eight', 'nine', 'ten']

        x_offset = 0
        self.point_rect_dict = {}

        # Set box numbers rectangles coordinates and sizes
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
        
    def draw_table(self):
    # draw the table using the rectangles        
        for point, rect in self.point_rect_dict.items():
            pygame.draw.rect(self.screen, light_grey, rect, 2)      
    
    def render_text_center(self, screen, text, font, size, rect, color, x_offset=0, y_offset=0):
    # Render text function to apply text to rectangles
        font = pygame.font.Font("Assets/font/"+font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (rect.center[0] + x_offset, rect.center[1] + y_offset)
        self.screen.blit(text_surface, text_rect)
    
    
    def table_background(self):
    # Draw some background images
        points = ['four', 'five', 'six', 'eight', 'nine', 'ten'] 
        hardways_and_horns = ['horn_two', 'horn_three', 'hard_four', 'hard_six', 'hard_eight', 'hard_ten', 'horn_eleven', 'horn_twelve']
        for point in points:
        # Add text to the box numbers
            center = self.point_rect_dict[f'{point}_center']
            pygame.draw.rect(screen, purple, center)
            
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
                self.render_text_center(screen, text, 'ALGER.TTF', 27, self.point_rect_dict[value], gold)
        
        # Text and dice for prop bets and other bets
        self.render_text_center(screen, '30 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['horn_two'], white, y_offset=(self.point_rect_dict['horn_two'].bottom-self.point_rect_dict['horn_two'].centery)/2)
        screen.blit(die_image_1, (self.point_rect_dict['horn_two'].centerx-34,self.point_rect_dict['horn_two'].centery-24))
        screen.blit(die_image_1, (self.point_rect_dict['horn_two'].centerx ,self.point_rect_dict['horn_two'].centery-24))
        self.render_text_center(screen, '15 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['horn_three'], white, y_offset=(self.point_rect_dict['horn_three'].bottom-self.point_rect_dict['horn_three'].centery)/2)
        screen.blit(die_image_1, (self.point_rect_dict['horn_three'].centerx-34,self.point_rect_dict['horn_three'].centery-24))
        screen.blit(die_image_2, (self.point_rect_dict['horn_three'].centerx ,self.point_rect_dict['horn_three'].centery-24))
        self.render_text_center(screen, '7 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['hard_four'], white, y_offset=(self.point_rect_dict['hard_four'].bottom-self.point_rect_dict['hard_four'].centery)/2)
        screen.blit(die_image_2, (self.point_rect_dict['hard_four'].centerx-34,self.point_rect_dict['hard_four'].centery-24))
        screen.blit(die_image_2, (self.point_rect_dict['hard_four'].centerx ,self.point_rect_dict['hard_four'].centery-24))
        self.render_text_center(screen, '9 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['hard_six'], white, y_offset=(self.point_rect_dict['hard_six'].bottom-self.point_rect_dict['hard_six'].centery)/2)
        screen.blit(die_image_3, (self.point_rect_dict['hard_six'].centerx-34,self.point_rect_dict['hard_six'].centery-24))
        screen.blit(die_image_3, (self.point_rect_dict['hard_six'].centerx ,self.point_rect_dict['hard_six'].centery-24))
        self.render_text_center(screen, '9 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['hard_eight'], white, y_offset=(self.point_rect_dict['hard_eight'].bottom-self.point_rect_dict['hard_eight'].centery)/2)
        screen.blit(die_image_4, (self.point_rect_dict['hard_eight'].centerx-34,self.point_rect_dict['hard_eight'].centery-24))
        screen.blit(die_image_4, (self.point_rect_dict['hard_eight'].centerx ,self.point_rect_dict['hard_eight'].centery-24))
        self.render_text_center(screen, '7 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['hard_ten'], white, y_offset=(self.point_rect_dict['hard_ten'].bottom-self.point_rect_dict['hard_ten'].centery)/2)
        screen.blit(die_image_5, (self.point_rect_dict['hard_ten'].centerx-34,self.point_rect_dict['hard_ten'].centery-24))
        screen.blit(die_image_5, (self.point_rect_dict['hard_ten'].centerx ,self.point_rect_dict['hard_ten'].centery-24))
        self.render_text_center(screen, '15 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['horn_eleven'], white, y_offset=(self.point_rect_dict['horn_eleven'].bottom-self.point_rect_dict['horn_eleven'].centery)/2)
        screen.blit(die_image_5, (self.point_rect_dict['horn_eleven'].centerx-34,self.point_rect_dict['horn_eleven'].centery-24))
        screen.blit(die_image_6, (self.point_rect_dict['horn_eleven'].centerx ,self.point_rect_dict['horn_eleven'].centery-24))
        self.render_text_center(screen, '30 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['horn_twelve'], white, y_offset=(self.point_rect_dict['horn_twelve'].bottom-self.point_rect_dict['horn_twelve'].centery)/2)
        screen.blit(die_image_6, (self.point_rect_dict['horn_twelve'].centerx-34,self.point_rect_dict['horn_twelve'].centery-24))
        screen.blit(die_image_6, (self.point_rect_dict['horn_twelve'].centerx ,self.point_rect_dict['horn_twelve'].centery-24))
        self.render_text_center(screen, '4 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['any_seven'], white, x_offset=(self.point_rect_dict['any_seven'].right-self.point_rect_dict['any_seven'].centerx)/2+20)
        self.render_text_center(screen, '4 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['any_seven'], white, x_offset=(self.point_rect_dict['any_seven'].left-self.point_rect_dict['any_seven'].centerx)/2-20)
        self.render_text_center(screen, 'SEVEN', 'ALGER.TTF', 30, self.point_rect_dict['any_seven'], deep_red)
        self.render_text_center(screen, "DON'T", 'ALGER.TTF', 20, self.point_rect_dict['dont_come'], deep_red,y_offset=-50)
        self.render_text_center(screen, "COME", 'ALGER.TTF', 20, self.point_rect_dict['dont_come'], deep_red,y_offset=-30)
        self.render_text_center(screen, "BAR", 'ALGER.TTF', 20, self.point_rect_dict['dont_come'], deep_red,y_offset=-10)
        screen.blit(die_image_6, (self.point_rect_dict['dont_come'].left,self.point_rect_dict['dont_come'].centery))
        screen.blit(die_image_6, (self.point_rect_dict['dont_come'].left+die_image_6.get_rect().width,self.point_rect_dict['dont_come'].centery))
        self.render_text_center(screen, '7 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['any_craps'], white, x_offset=(self.point_rect_dict['any_craps'].right-self.point_rect_dict['any_craps'].centerx)/2+20)
        self.render_text_center(screen, '7 TO 1', 'ALGER.TTF', 20, self.point_rect_dict['any_craps'], white, x_offset=(self.point_rect_dict['any_craps'].left-self.point_rect_dict['any_craps'].centerx)/2-20)
        self.render_text_center(screen, 'CRAPS', 'ALGER.TTF', 30, self.point_rect_dict['any_craps'], deep_red)
        self.render_text_center(screen, 'COME', 'ALGER.TTF', 80, self.point_rect_dict['come'], deep_red)
        self.render_text_center(screen, "DON'T PASS BAR", 'ALGER.TTF', 60, self.point_rect_dict['dont_pass_line'], deep_red, x_offset= -30)
        screen.blit(die_image_6, (self.point_rect_dict['dont_pass_line'].right-die_image_6.get_rect().width*2-10,self.point_rect_dict['dont_pass_line'].centery-die_image_6.get_rect().height/2))
        screen.blit(die_image_6, (self.point_rect_dict['dont_pass_line'].right-die_image_6.get_rect().width-5,self.point_rect_dict['dont_pass_line'].centery-die_image_6.get_rect().height/2))
        self.render_text_center(screen, "PASS LINE", 'ALGER.TTF', 80, self.point_rect_dict['pass_line'], white)
        self.render_text_center(screen, "2", 'ALGER.TTF', 30, self.point_rect_dict['field'], gold, x_offset=-250, y_offset= 5)
        pygame.draw.circle(screen, light_grey,(self.point_rect_dict['field'].centerx-250, self.point_rect_dict['field'].centery+5),20,2)
        self.render_text_center(screen, "PAYS DOUBLE", 'ALGER.TTF', 15, self.point_rect_dict['field'], gold, x_offset=-250, y_offset= -22)
        self.render_text_center(screen, "3", 'ALGER.TTF', 30, self.point_rect_dict['field'], gold, x_offset=-150, y_offset= -15)
        self.render_text_center(screen, "4", 'ALGER.TTF', 30, self.point_rect_dict['field'], gold, x_offset=-50, y_offset= -15)
        self.render_text_center(screen, "9", 'ALGER.TTF', 30, self.point_rect_dict['field'], gold, y_offset= -15)
        self.render_text_center(screen, "FIELD", 'ALGER.TTF', 30, self.point_rect_dict['field'], white, y_offset= 15)
        self.render_text_center(screen, "10", 'ALGER.TTF', 30, self.point_rect_dict['field'], gold, x_offset=50, y_offset= -15)
        self.render_text_center(screen, "11", 'ALGER.TTF', 30, self.point_rect_dict['field'], gold, x_offset=150, y_offset= -15)
        self.render_text_center(screen, "12", 'ALGER.TTF', 30, self.point_rect_dict['field'], gold, x_offset=250, y_offset= 5)
        pygame.draw.circle(screen, light_grey,(self.point_rect_dict['field'].centerx+250, self.point_rect_dict['field'].centery+5),20,2)
        self.render_text_center(screen, "PAYS TRIPLE", 'ALGER.TTF', 15, self.point_rect_dict['field'], gold, x_offset=+250, y_offset= -22)
        

