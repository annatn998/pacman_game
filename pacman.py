import pygame 
from game_board import enviroment
from player import Player
from ghosts import Ghosts

# Time in Video: 1:38:08

pygame.init()

# Need to divide width & height by total number of tiles that you have 
# Is important that you have the screen size divisible by the tile size that you want
WIDTH = 800
HEIGHT = 630

# Setting pygame up to use the static variables that you created
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Set the speed that your game will run 
timer = pygame.time.Clock()
fps = 60 # Fastest speed that the game can run 
font = pygame.font.SysFont(name='playbill', size=20)
level = enviroment()
run = True 
color = 'blue'
player = Player(screen=screen)
score = 0
power_up = False 
power_counter = 0 
eaten_ghosts = [False, False, False, False]
startup_counter = 0
moving = False

eaten_ghosts = [False, False, False, False]

blinky = Ghosts(x=380, 
            y=100, 
            color='red', 
            player_x=player.player_x,
            player_y=player.player_y,
            power_up=False,
            id=0,
            screen=screen,
            level=level,
            eaten_ghosts=eaten_ghosts)

inky = Ghosts(x=400, 
            y=100, 
            color='powerup', 
            player_x=player.player_x,
            player_y=player.player_y,
            power_up=False,
            id=1,
            screen=screen,
            level=level,
            eaten_ghosts=eaten_ghosts)

pinky = Ghosts(x=450, 
            y=120, 
            color='pink', 
            player_x=player.player_x,
            player_y=player.player_y,
            power_up=False,
            id=2,
            screen=screen,
            level=level,
            eaten_ghosts=eaten_ghosts)

clyde_x = 35
clyde_y = 50
clyde_direction = 0 


def check_collisions(score, 
                     player_x, 
                     center_x, 
                     center_y, 
                     power_up, 
                     power_count, 
                     eaten_ghosts):
    
    # print('check collisions: ', center_x//32, center_y//32)
    if player_x > 0 and player_x < 780: 
        if level[center_y // 32][center_x // 32] == 1: 
            level[center_y // 32][center_x // 32] = 4
            score += 10
        if level[center_y // 32][center_x // 32] == 2: 
            level[center_y // 32][center_x // 32] = 5
            score += 10
        if level[center_y // 32][center_x // 32] == 3: 
            level[center_y // 32][center_x // 32] = 6
            score += 10
            power_up = True
            power_count = 0 
            eaten_ghosts = [False, False, False, False]
    return score, power_up, power_count, eaten_ghosts

def draw_enviroment(screen, level):

    for i,row in enumerate(level):
        for j,item in enumerate(row):
            if item == 1 or item == 4:
                pygame.draw.line(screen, color , [j*32, i*32], [j*32+32,i*32], 3)
                pygame.draw.line(screen, color , [j*32, i*32+32], [j*32+32,i*32+32], 3)
            elif item == 2 or item == 5:
                pygame.draw.line(screen, color , [j*32, i*32], [j*32,i*32+32], 3)
                pygame.draw.line(screen, color , [j*32+32, i*32], [j*32+32,i*32+32], 3)

    # TUTORING LESSON 3
    for i, row in enumerate(level):
            for j, item in enumerate(row):
                if item != 0 and item != 9 and item != 4 and item != 5 and item != 6:
                    pygame.draw.circle(screen,'white',((j*32) + 16, (i*32) + 16), 4 )
                if item == 3 and not player.flicker and item != 6: 
                    pygame.draw.circle(screen,'white',((j*32) + 16, (i*32) + 16), 8 )
                if item == 9: 
                    pygame.draw.line(screen, 'white', [j*32, i*32], [j*32+32,i*32], 3)
                    pygame.draw.line(screen, color , [j*32, i*32+32], [j*32+32,i*32+32], 3)

def check_position(center_x, center_y): 
    # Right, left, up, or down 
    turns = [False, False, False, False]
    error_term = 30

    # check collissions based on center x and center y +/- error_term
    if center_x // 32 < 24 and center_x // 32 >= 0 and center_y // 32 < 17 and center_y // 32 >= 0: 
        upper_y_square = level[(center_y + error_term) // 32][center_x//32]
        lower_y_square = level[(center_y - error_term) // 32][center_x//32]
        left_x_square = level[center_y // 32][(center_x - error_term)//32]
        right_x_square =  level[center_y // 32][(center_x + error_term)//32] 
        # print(f'x_position: {center_x // 32}, y_position: {center_y // 32}, right_square: {right_x_square}, left_square: {left_x_square}, bottom_square: {upper_y_square}, upper_square: {lower_y_square}')
        possible_squares_x = [1,3,9,4,6]
        possible_squares_y = [2,3,9,5,6]
        # if you hit the edge of the board all the way to the right you have to be turning to the right 
        if player.direction_command == 0: 
            # is the piece right behind me less than 1 because on the board anything over a 1 is a line 
            if left_x_square in possible_squares_x: 
                turns[1] = True
        # if you are facing left and the dot to your right is not a line you can turn right 
        if player.direction_command == 1: 
            if right_x_square in possible_squares_x: 
                turns[0] = True
        if player.direction_command == 2: 
            if upper_y_square in possible_squares_y: 
                turns[3] = True
        if player.direction_command == 3: 
            if lower_y_square in possible_squares_y: 
                turns[2] = True  
        # Turn up and down based on if you're facing up or down 
        if player.direction_command == 2 or player.direction_command == 3:
            possible_squares_x = [1,3,9,4,6]
            possible_squares_y = [2,3,5,6]
            # if center x position divided by how wide each tile is 
            # if the remainder is <= 16 then we're pretty much in the middle of the tile  
            # Can only turn if you're roughly at the mid-point of the square for visual effects
            # Want to check first if we should even allow the image to turn, because it would look weird if it turned at this point
            if 14 <= center_x % 32 <= 18: 
                if upper_y_square in possible_squares_y:
                    turns[3] = True
                if lower_y_square in possible_squares_y:
                    turns[2] = True       
            if 14 <= center_y % 32 <= 18:          
                if  left_x_square in possible_squares_x:
                    turns[1] = True
                if right_x_square in possible_squares_x:
                    turns[0] = True 

 
        if player.direction_command == 0 or player.direction_command == 1:
            possible_squares_x = [1,3,9,4,6]
            possible_squares_y = [2,3,5,6]
            # if center x position divided by how wide each tile is 
            # if the remainder is <= 16 then we're pretty much in the middle of the tile  
            # Can only turn if you're roughly at the mid-point of the square for visual effects
            # Want to check first if we should even allow the image to turn, because it would look weird if it turned at this point 
            if 14 <= center_x % 32 <= 18:
                if upper_y_square in possible_squares_y: 
                    turns[3] = True
                if lower_y_square in possible_squares_y:
                    turns[2] = True      
            if 14 <= center_y % 32 <= 18:             
                if possible_squares_x:
                    turns[1] = True
                if possible_squares_x:
                    turns[0] = True                            
    else:  
        # if you've gone past the limits of the board you have to be able to turn left or right 
        turns[0] = True 
        turns[1] = True

    
    return turns

def move_player(play_x, play_y, valid_turns, player): 
    # R, L, U, D
    # if we are pointed right and the players are allowed to move right then we can change the x-position 
    if player.direction == 0 and valid_turns[0]: 
        play_x += player.player_speed
    elif player.direction == 1 and valid_turns[1]: 
        play_x -= player.player_speed
    elif player.direction == 2 and valid_turns[2]: 
        play_y -= player.player_speed
    elif player.direction == 3 and valid_turns[3]: 
        play_y += player.player_speed      

    return play_x, play_y          

def get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y, powerup):
    if player.player_x < WIDTH//2:
        runaway_x = WIDTH
    else: 
        runaway_x = 0
    if player.player_y < HEIGHT//2:
        runaway_y = HEIGHT
    else: 
        runaway_y = 0

    return_target = (400, 100)


def draw_misc(score, powerup, lives, player, game_over, game_won):
    score_text = font.render(f'Score: {score}', True, 'white') # gets smooth edges
    screen.blit(score_text, (10, 600))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 600), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player.player_images[0], (15, 15)), (300 + i * 40, 590))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))


# What do we want to execute every single iteration 
while run: 
    timer.tick(fps) # Frame rate 
    if player.counter < 19: 
        player.counter += 1
        if player.counter > 5: 
            player.flicker = False
    else: 
        player.counter = 0
        player.flicker = True
    
    if power_up and power_counter < 600: # at 60 frames per second it means that after 10 seconds of the power showing we'll see a change
        power_counter += 1 

    elif power_up and power_counter >= 600: 
        power_counter = 0
        power_up = False 
        eaten_ghosts = [False, False, False, False]

    if startup_counter < 180: 
        moving = False 
        startup_counter += 1
    else: 
        moving = True

    screen.fill('black') # putting a solid color in the back 
    draw_enviroment(screen, level)
    player.draw_player()

    clyde = Ghosts(x=clyde_x, 
            y=clyde_y, 
            color='orange', 
            player_x=player.player_x,
            player_y=player.player_y,
            power_up=False,
            id=3,
            screen=screen,
            level=level,
            eaten_ghosts=eaten_ghosts,
            direction=clyde_direction)
    
    # What direction am I able to turn in 
    # Check position of the center of the character 
    center_x = player.player_x + 13
    center_y = player.player_y + 13

    blinky.draw(eaten_ghosts=eaten_ghosts)
    pinky.draw(eaten_ghosts=eaten_ghosts)
    inky.draw(eaten_ghosts=eaten_ghosts)

    # pygame.draw.circle(screen, 'red', (center_x, center_y), 2)
    valid_turns = check_position(center_x, center_y)
    if moving: 
        player.player_x, player.player_y = move_player(player.player_x, player.player_y, valid_turns, player)
        # blinky_x, blinky_y, blinky_direction = blinky.move_clyde(player_x=player.player_x, player_y=player.player_y)
        # inky_x, inky_y, inky_direction = inky.move_clyde(player_x=player.player_x, player_y=player.player_y)
        # pinky_x, pinky_y, pinky_direction = pinky.move_clyde(player_x=player.player_x, player_y=player.player_y)
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde(player_x=player.player_x, player_y=player.player_y)
    
    score, power_up, power_counter, eaten_ghosts = check_collisions(player_x=player.player_x, 
                                                                  center_x=center_x, 
                                                                  center_y=center_y, 
                                                                  score=score,
                                                                  power_up=power_up,
                                                                  power_count=power_counter,
                                                                  eaten_ghosts=eaten_ghosts)
    draw_misc(score=score, 
              powerup=power_up, 
              lives=3, 
              player=player, 
              game_over=False, 
              game_won=False)
    
    

    for event in pygame.event.get(): # gets everything happening in your computer (keyboard, mouse, buttons)
        # So you need to check what the even type is 
        if event.type == pygame.QUIT: # unique command tied to pygame window 
            run = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_RIGHT: 
                player.direction_command = 0
            if event.key == pygame.K_LEFT: 
                player.direction_command = 1
            if event.key == pygame.K_UP: 
                player.direction_command = 2 
            if event.key == pygame.K_DOWN: 
                player.direction_command = 3

        # If you let go of the key it should just go in the same direction
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and player.direction_command == 0:
                player.direction_command = player.direction
            if event.key == pygame.K_LEFT and player.direction_command == 1:
                player.direction_command = player.direction
            if event.key == pygame.K_UP and player.direction_command == 2:
                player.direction_command = player.direction
            if event.key == pygame.K_DOWN and player.direction_command == 3:
                player.direction_command = player.direction

    # print(player.direction_command, player.direction, valid_turns)
    if player.direction_command == 0 and valid_turns[0]:
        player.direction = 0
    if player.direction_command == 1 and valid_turns[1]:
        player.direction = 1
    if player.direction_command == 2 and valid_turns[2]:
        player.direction = 2
    if player.direction_command == 3 and valid_turns[3]:
        player.direction = 3

    if player.player_x > WIDTH: 
        player.player_x = -10
    elif player.player_x < -10: 
        player.player_x = WIDTH - 3

    if player.player_y >= 531: 
        player.player_y = -10 
    elif player.player_y <= -10: 
        player.player_y = 500

    # Re-draws on the screen every iteration 
    # Flip does the whole screen display does a specific section 
    # but if you don't put an argument into display it works like flip 
    pygame.display.flip()

pygame.quit()

