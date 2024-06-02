from ghosts import Ghosts
import pygame
from game_board import enviroment
from player import Player

# Initializes backend for pygame

pygame.init()

# Must be divisible by size of square on board
WIDTH = 800
HEIGHT = 630

# Set some pygame static variables
screen = pygame.display.set_mode([WIDTH, HEIGHT])

timer = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont(name='playbill', size=20)
level = enviroment()
run = True
color = 'blue'
player = Player(screen=screen)
blinky = Ghosts(
    x=380,
    y=100,
    color = 'red',
    player_x = player.player_x,
    player_y= player.player_y,
    power_up= False,
    id= 0,
    screen=screen,
)
powerup = False
game_over = False
game_won= False
powerup_actevated = False
score = 0
startup_counter = 0
power_counter=0
eaten_ghosts= [False,False,False,False]




def draw_misc(score, powerup,lives, player, game_over, game_won):
    score_text = font.render(f'Score: {score}', True,'white')
    screen.blit(score_text, (10, 750))

    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 600), 15)

    for i in range(lives):
        screen.blit(pygame.transform.scale(player.player_images[0],(30,30)), (300 + i * 40, 590))

    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 600,300],0, 10)
        pygame.draw.rect(screen, 'dark grey', [70, 220, 550, 260], 0, 10)
        gameover_text = font.render('GAME OVER!!!!!!! Space bar to restart', True, 'green')
        screen.blit(gameover_text, (100,300))

    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 600, 300], 0, 10)
        pygame.draw.rect(screen, 'dark grey', [70, 220, 550, 260], 0, 10)
        gamewon_text = font.render('VICTORY!!!!!!! Space bar to restart', True, 'green')
        screen.blit(gamewon_text, (100, 300))

def draw_environment(screen, level):
    no_dots= [0,9,4,5,6]
    for i, row in enumerate(level):
        for j, item in enumerate(row):
            if item == 1:
                pygame.draw.line(screen, color, [j*32, i*32], [j*32 + 32, i*32], 3)
                pygame.draw.line(screen, color, [j*32, i*32+32], [j*32 + 32, i*32+32], 3)
            if item == 2:
                pygame.draw.line(screen, color, [j*32, i*32], [j*32, i*32+32], 3)
                pygame.draw.line(screen, color, [j*32+32, i*32], [j*32 + 32, i*32+32], 3)

            if item == 4:
                pygame.draw.line(screen, color, [j*32, i*32], [j*32 + 32, i*32], 3)
                pygame.draw.line(screen, color, [j * 32, i * 32 + 32], [j * 32 + 32, i * 32 + 32], 3)

            if item == 5:
                pygame.draw.line(screen, color, [j * 32, i * 32], [j * 32, i * 32 + 32], 3)
                pygame.draw.line(screen, color, [j * 32 + 32, i * 32], [j * 32 + 32, i * 32 + 32], 3)

    for i, row in enumerate(level):
        for j, item in enumerate(row):
            if item not in no_dots:
                pygame.draw.circle(screen, "white", ((j*32) + 16, (i*32) + 16),4)
            if item == 3:
                pygame.draw.circle(screen, "white", ((j * 32) + 16, (i * 32) + 16), 8)
            if item == 9:
                pygame.draw.line(screen, "white", [j*32, i*32], [j*32 + 32, i*32], 3)
                pygame.draw.line(screen, color,[j * 32, i * 32+32], [j * 32 + 32, i * 32+32], 3)

def check_collisions (center_x, center_y, score,powerup, power_count, eaten_ghost):
    if 0< player.player_x <800: # change to 800
        if level[center_y// 32] [center_x//32] == 1:
            level[center_y// 32] [center_x//32] = 4
            score += 10
        if level[center_y// 32] [center_x//32] == 2:
            level[center_y// 32] [center_x//32] = 5
            score += 10
        if level[center_y// 32] [center_x//32] == 3:
            level[center_y// 32] [center_x//32] = 6
            score += 50
            powerup = True
            power_count= 0
            eaten_ghost = [False,False,False,False]
    return score, powerup,power_count,eaten_ghost



def move_player(player_x, player_y, valid_turns, player):
    # R, L, U, D
    if player.direction == 0 and valid_turns[0]:
        player_x += player.player_speed
    elif player.direction == 1 and valid_turns[1]:
        player_x -= player.player_speed
    elif player.direction == 2 and valid_turns[2]:
        player_y -= player.player_speed
    elif player.direction == 3 and valid_turns[3]:
        player_y += player.player_speed

    return player_x,player_y

def check_position(center_x, center_y):
    #right, left, up, down
    turns = [ False,False,False,False]
    error_term= 30

    if center_x // 32 < 24 and center_x // 32 >= 0 and center_y// 32 < 17 and center_y// 32 >= 0 :
        upper_y_square = level[(center_y + error_term) // 32][center_x//32]
        lower_y_square = level[(center_y - error_term) // 32][center_x//32]
        left_x_square = level[center_y // 32][(center_x + error_term) // 32]
        right_x_square = level[center_y // 32][(center_x - error_term) // 32]
        play_curent_square = level [center_y // 32][center_x // 32]

        sidways_positions = [1,3,9,4,6]
        horizontel_positions =[2,3,5,6,9]
        if player.direction_command == 1:
            if right_x_square in sidways_positions:
                turns[0] = True
                '''if right_x_square == 3:
                    maybe inport time for time delay to actvait power up
                    would look something like:
                    wait(30)
                    powerup_actevated = True'''




        if player.direction_command == 0:
            if left_x_square in sidways_positions:
                turns[1] = True

        if player.direction_command == 3:
            if lower_y_square in horizontel_positions:
                turns[2] = True

        if player.direction_command == 2:
            if upper_y_square in horizontel_positions:
                turns[3] = True


        if player.direction_command == 2 or player.direction_command == 3:
          sidways_positions = [1, 3, 9, 4, 6]
          horizontel_positions = [2, 3, 5, 6] # delete 9 from these 
          if 14 <= center_x % 32 <= 18:
              if upper_y_square in horizontel_positions:
                turns[3] = True
              if lower_y_square in horizontel_positions:
                turns[2] = True

          if 14 <= center_y % 32 <= 18: # change these to 1 & 0 
              if left_x_square in sidways_positions:
                turns[1] = True
              if right_x_square in sidways_positions:
                turns[0] = True

        if player.direction_command == 0 or player.direction_command == 1:
            sidways_positions = [1, 3, 9, 4, 6]
            horizontel_positions = [2, 3, 5, 6] # need to delete 9 from these
            if 14 <= center_x % 32 <= 18:
                if upper_y_square in horizontel_positions:
                    turns[3] = True

                if lower_y_square in horizontel_positions:
                    turns[2] = True

            if 14 <= center_y % 32 <= 18:
                if left_x_square in sidways_positions:
                    turns[1] = True

                if right_x_square in sidways_positions:
                    turns[0] = True



    else:
        turns[0] = True
        turns[1] = True
    return turns


while run:
    timer.tick(fps) # Frame Rate
    if player.counter < 19:
        player.counter += 1
        if player.counter > 5:
            player.flicker=False
    else:
        player.counter = 0
        player.flicker = True

    if powerup and power_counter < 600:
         power_counter += 1


    if powerup and power_counter >= 600:
        power_counter =0
        powerup = False
        eaten_ghosts =[False,False,False,False]

    if startup_counter < 180:
        moving = False
        startup_counter += 1
    else:
        moving = True




    screen.fill('black')
    draw_environment(screen, level)
    player.draw_player()
    center_x = player.player_x + 13
    center_y = player.player_y + 13
    
    turns = check_position(center_x, center_y)

    if moving:
        player.player_x, player.player_y = move_player(player.player_x,player.player_y,turns,player)

    score,powerup,power_counter,eaten_ghosts  = check_collisions(center_x=center_x,
                                                                 center_y = center_y,
                                                                 score= score,
                                                                 powerup=powerup,
                                                                 power_count= power_counter,
                                                                 eaten_ghost = eaten_ghosts)


    draw_misc(
        score = score,
        lives = 3,
        player = player,
        game_over= False,
        game_won = False,
        powerup= powerup

    )




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and player.direction_command == 0:
                player.direction_command = player.direction
            if event.key == pygame.K_LEFT and player.direction_command == 1:
                player.direction_command = player.direction
            if event.key == pygame.K_UP and player.direction_command == 2:
                player.direction_command = player.direction
            if event.key == pygame.K_DOWN and player.direction_command == 3:
                player.direction_command = player.direction

        if player.direction_command == 0 and turns[0]:
            player.direction = 0
        if player.direction_command == 1 and turns[1]:
            player.direction = 1
        if player.direction_command == 2 and turns[2]:
            player.direction = 2
        if player.direction_command == 3 and turns[3]:
            player.direction = 3

        if player.player_x > 800:
            player.player_x = -47
        elif player.player_x < -47:
            player.player_x = 800

        if player.player_y > 500:
            player.player_y = -10
        elif player.player_y < -10:
            player.player_y = 500
    pygame.display.flip()



pygame.quit()
