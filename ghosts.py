import pygame

class Ghosts(): 
    def __init__(self, x, 
                       y, 
                       color, 
                       player_x, 
                       player_y,
                       id,
                       screen, 
                       power_up,
                       level,
                       eaten_ghosts,
                       direction=0) -> None:
        
        self.x = x 
        self.y = y 
        self.center_x = self.x + 13
        self.center_y = self.y + 13
        self.direction = direction
        self.img = self.grab_images(color)
        self.eyes = False 
        self.target = (player_x, player_y)
        self.moving = False
        self.speed = 1
        self.id = id
        # outline of ghosts collision box 
        # define a circle that outlines pacman 
        # then we define a rectangle over the ghosts 
        # then we check it using pygame.check collisions
        self.screen = screen
        self.power_up_img = self.grab_images('powerup')
        self.eyes_img  = self.grab_images('eyes')
        self.power_up = power_up
        self.level = level
        self.box = False
        self.turns, self.box = self.check_collisions(self.level)
        self.rect = self.draw(eaten_ghosts=eaten_ghosts)


    def grab_images(self, filename): 
        img = pygame.transform.scale(pygame.image.load(f"./images/ghost_sprites/{filename}.png"), (50, 50))
        return img
    
    def draw(self, eaten_ghosts):
        # checking if the ghosts is still alive 
        # or if it was eaten during the power up  which if that's the case we will return it to the box 
        # once the eyes have been done floating around the screen 
        # so it's slightly different eyes vs being eaten 
        if (not self.power_up and not self.eyes) or (eaten_ghosts[self.id] and self.power_up and not self.eyes): 
            self.screen.blit(self.img, (self.x, self.y))
        # pacman has powered up, but not eaten the ghosts yet 
        elif self.power_up and not self.eyes and not eaten_ghosts[self.id]:
            self.screen.blit(self.power_up_img, (self.x, self.y))
        else:  # only other condition is if the ghost has been eaten 
            self.screen.blit(self.eyes_img, (self.x, self.y))

        # building the rectangles around the image 
        # and then show what you can hit 
        # where to start and then how wide and how tall 
        ghost_rect = pygame.rect.Rect((self.center_x - 13, self.center_y - 13), (25, 25))
        self.rect = ghost_rect
        return ghost_rect


    def check_collisions(self, level): 
        self.turns = [False, False, False, False]
        error_term = 30
        upper_y_square = level[(self.center_y + error_term) // 32][self.center_x//32]
        lower_y_square = level[(self.center_y - error_term) //32][self.center_x//32]
        left_x_square = level[self.center_y //32][(self.center_x + error_term) //32]
        right_x_square = level[self.center_y//32][(self.center_x - error_term) //32]

        if self.center_x // 32 < 24: 
            sideways_positions = [1,3,9,4,6]
            up_and_down_positions = [2,3,5,6,9]

            if left_x_square in sideways_positions or (left_x_square == 0 and self.box or self.eyes): 
                self.turns[1] = True 

            if right_x_square in sideways_positions or (right_x_square == 0 and self.box or self.eyes): 
                self.turns[0] = True 

            if upper_y_square in up_and_down_positions or (upper_y_square == 0 and self.box or self.eyes): 
                self.turns[3] = True 

            if lower_y_square in up_and_down_positions or (lower_y_square == 9 or lower_y_square == 0 and self.box or self.eyes): 
                self.turns[2] = True

            
            sideways_positions = [1,3,9,4,6]
            up_and_down_positions = [2,3,4,6,9]
            if 14 <= self.center_x % 32 <= 18: 
                if upper_y_square in up_and_down_positions or (upper_y_square == 0 and self.box or self.eyes): 
                    self.turns[3] = True 
                if lower_y_square in up_and_down_positions or (lower_y_square == 0 or lower_y_square == 9 and self.box or self.eyes): 
                    self.turns[2] = True

            if 14 <= self.center_y % 32 <= 18: 
                if left_x_square in sideways_positions or (left_x_square == 0 and self.box or self.eyes): 
                    self.turns[3] = True 
                if right_x_square in sideways_positions or (right_x_square == 0 and self.box or self.eyes): 
                    self.turns[2] = True 

        else: 
            self.turns[0] = True
            self.turns[1] = True 

        if 350 < self.x < 450 and 100 < self.y < 200: 
            self.box = True 
        else: 
            self.box = False 
        

        return self.turns, self.box

    def custom_movement(self, player_direction, ghost_direction, turns):
        if self.target[player_direction] > ghost_direction and self.turns[turns]:
            ghost_direction += self.speed 
            self.direction = turns
        if self.target[player_direction] < ghost_direction and self.turns[turns]: 
            ghost_direction -= self.speed 
            self.direction = turns
        
    def move_clyde(self, player_x, player_y):
        self.target = (player_x, player_y)
        # print('x & y: ', self.x, self.y, self.direction, self.target[0], self.turns[0])
        # r, l, u, d
        # clyde is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            if self.target[0] > self.x and self.turns[0]:
                self.x += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                else:
                    self.x += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x and self.turns[1]:
                self.x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                if self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                else:
                    self.x -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x and self.turns[1]:
                self.direction = 1
                self.x -= self.speed
            elif self.target[1] < self.y and self.turns[2]:
                self.direction = 2
                self.y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                else:
                    self.y -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y and self.turns[3]:
                self.y += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                #  start here 
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                else:
                    self.y += self.speed
        if self.x < -30:
            self.x = 700
        elif self.x > 700:
            self.x - 30
        return self.x, self.y, self.direction