
import pygame

class Player(): 
    def __init__(self, screen):
        self.player_images = []
        self.player_x = 450
        self.player_y = 450
        self.direction = 0
        self.screen = screen
        self.counter = 0
        self.flicker = False
        self.direction_command = 0
        self.player_speed = 1

    def draw_player(self):
        # counter will cycle through the images 
        # 5 is chosen because at 60fps it looks better 
        # basically do all 4 images in 20 clicks 
        # 0- Right, 1- Left, 2 - up, 3 - down 
        self.grab_images()
        if self.direction == 0: 
            self.screen.blit(self.player_images[self.counter // 5], (self.player_x, self.player_y))
        if self.direction == 1: 
            self.screen.blit(pygame.transform.flip(self.player_images[self.counter // 5], True, False), 
                        (self.player_x, self.player_y))
        if self.direction == 2: 
            self.screen.blit(pygame.transform.rotate(self.player_images[self.counter // 5], 90), 
                             (self.player_x, self.player_y))
        if self.direction == 3: 
            self.screen.blit(pygame.transform.rotate(self.player_images[self.counter // 5], 270), 
                             (self.player_x, self.player_y))

    def grab_images(self): 
        for i in range(1,5): 
            # Load and scale the image because the images might be larger than 
            # The size of our squares
            # sized down to 32 x 32 square 
            self.player_images.append(pygame.transform.scale(pygame.image.load(f"./images/pacman_sprites/pacman{i}.png"), (25,25)))
    