import pygame
from game_board import enviroment as environment
from player import Player
from ghosts import Ghosts
# Initializes backend for pygame
pygame.init()

# Must be divisible by size of square on board 
WIDTH = 800
HEIGHT = 576

# Set some pygame static variables 
screen = pygame.display.set_mode([WIDTH, HEIGHT])

timer = pygame.time.Clock()
fps = 60 
font = pygame.font.SysFont(name='playbill', size=20)
level = environment()
run = True
color = 'blue'
player = Player(screen=screen)

eaten_ghosts = [False, False, False, False]

blinky = Ghosts(x=380, 
            y=100, 
            color='red', 
            player_x=player.player_x,
            player_y=player.player_y,
            power_up=False,
            id=0,
            screen=screen)

inky = Ghosts(x=400, 
            y=100, 
            color='powerup', 
            player_x=player.player_x,
            player_y=player.player_y,
            power_up=False,
            id=1,
            screen=screen)

pinky = Ghosts(x=450, 
            y=120, 
            color='pink', 
            player_x=player.player_x,
            player_y=player.player_y,
            power_up=False,
            id=2,
            screen=screen)

clyde = Ghosts(x=360, 
            y=110, 
            color='orange', 
            player_x=player.player_x,
            player_y=player.player_y,
            power_up=False,
            id=3,
            screen=screen)

score = 0
def draw_environment(screen, level): 
    no_dots = [4, 5, 0, 9, 6]
    for i, row in enumerate(level): 
        for j, item in enumerate(row): 
            # horizontal 
            if item == 1: 
                pygame.draw.line(screen, color, [j*32, i*32], [j*32 + 32, i*32], 3)
                pygame.draw.line(screen, color, [j*32, i*32+32], [j*32 + 32, i*32+32], 3)
            # vertical
            if item == 2: 
                pygame.draw.line(screen, color, [j*32, i*32], [j*32, i*32+32], 3)
                pygame.draw.line(screen, color, [j*32+32, i*32], [j*32 + 32, i*32+32], 3)

            # horizontal
            if item == 4: 
                pygame.draw.line(screen, color, [j*32, i*32], [j*32 + 32, i*32], 3)
                pygame.draw.line(screen, color, [j*32, i*32+32], [j*32 + 32, i*32+32], 3)

            # vertical
            if item == 5: 
                pygame.draw.line(screen, color, [j*32, i*32], [j*32, i*32+32], 3)
                pygame.draw.line(screen, color, [j*32+32, i*32], [j*32 + 32, i*32+32], 3)

    for i, row in enumerate(level): 
        for j, item in enumerate(row): 
            if item not in no_dots: 
                pygame.draw.circle(screen, 'white', ((j*32) + 16, (i*32) + 16), 4)
            if item == 3: 
                pygame.draw.circle(screen, 'white', ((j*32) + 16, (i*32) + 16), 8)
            if item == 9: 
                pygame.draw.line(screen, 'white', [j*32, i*32], [j*32 + 32, i*32], 3)
                pygame.draw.line(screen, color, [j*32, i*32+32], [j*32 + 32, i*32+32], 3)

def move_player(valid_turns, player):
    # R, L, U, D 
    if player.direction == 0 and valid_turns[0]: 
        player.player_x += player.player_speed
    elif player.direction == 1 and valid_turns[1]:
        player.player_x -= player.player_speed
    elif player.direction == 2 and valid_turns[2]: 
        player.player_y -= player.player_speed
    elif player.direction == 3 and valid_turns[3]: 
        player.player_y += player.player_speed


def check_position(center_x, center_y):
    # right, left, up, down 
    turns = [False, False, False, False]
    error_term = 30
    if center_x // 32 < 24 and center_x // 32 >= 0 and center_y // 32 < 17 and center_y // 32 >= 0: 
        upper_y_square = level[(center_y + error_term) // 32][center_x//32]
        lower_y_square = level[(center_y - error_term) //32][center_x//32]
        left_x_square = level[center_y //32][(center_x + error_term) //32]
        right_x_square = level[center_y//32][(center_x - error_term) //32]
        sideways_positions = [1,3,9, 4, 6]
        up_and_down_positions = [2,3,9, 5, 6]
        # print(f'upper y: {upper_y_square}, lowe y : {lower_y_square}, right {right_x_square}, left {left_x_square}')

        if player.direction_command == 0:
            if left_x_square in sideways_positions:
                turns[1] = True
        if player.direction_command == 1:
            if right_x_square in sideways_positions:
                turns[0] = True
        if player.direction_command == 2:
            if upper_y_square in up_and_down_positions:
                turns[3] = True
        if player.direction_command == 3:
            if lower_y_square in up_and_down_positions:
                turns[2] = True

        if player.direction_command == 2 or player.direction_command == 3 or player.direction_command == 1 or player.direction_command == 0:
            sideways_positions = [1,3,9, 4, 6]
            up_and_down_positions = [2,3,5, 6]
            if 14 <= center_x % 32 <= 18:
                if upper_y_square in up_and_down_positions:
                    turns[3] = True
                if lower_y_square in up_and_down_positions:
                    turns[2] = True
            if 14 <= center_y % 32 <= 18:
                if left_x_square in sideways_positions:
                    turns[1] = True
                if right_x_square in sideways_positions:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

def draw_misc(score, powerup, lives, player, game_over, game_won):
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player.player_images[0], (30, 30)), (650 + i * 40, 915))
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


def check_collisions(center_x, center_y, score): 
    print(level[center_y //32][center_x//32])
    if 0 < player.player_x < 800: 
        if level[center_y //32][center_x//32] == 1: 
            level[center_y //32][center_x//32] = 4
            score += 10
        if level[center_y //32][center_x//32] == 2: 
            print('HELLO')
            level[center_y //32][center_x//32] = 5
            score += 10
        if level[center_y //32][center_x//32] == 3: 
            level[center_y //32][center_x//32] = 6
            score += 50
    return score


# check whether or not a single pixel moves at every fps 
while run: 
    timer.tick(fps) # Frame Rate
    if player.counter < 19: 
        player.counter += 1
    else: 
        player.counter = 0 

    screen.fill('black')
    draw_environment(screen, level)
    player.draw_player()
    blinky.draw(eaten_ghosts=eaten_ghosts)
    pinky.draw(eaten_ghosts=eaten_ghosts)
    inky.draw(eaten_ghosts=eaten_ghosts)
    clyde.draw(eaten_ghosts=eaten_ghosts)

    center_x = player.player_x + 13
    center_y = player.player_y + 13 
    print(player.player_x, player.player_y)
    turns_allowed = check_position(center_x = center_x,
                                   center_y = center_y)
    move_player(valid_turns=turns_allowed, player=player)
    score = check_collisions(center_x=center_x, center_y=center_y, score=score)
    
    
    
    
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

    if player.direction_command == 0 and turns_allowed[0]:
        player.direction = 0
    if player.direction_command == 1 and turns_allowed[1]:
        player.direction = 1
    if player.direction_command == 2 and turns_allowed[2]:
        player.direction = 2
    if player.direction_command == 3 and turns_allowed[3]:
        player.direction = 3

    if player.player_x > 800:
        player.player_x = -47
    elif player.player_x < -50:
        player.player_x = 790

    if player.player_y > 500:
        player.player_y = -10
    elif player.player_y < -10:
        player.player_y = 500

    pygame.display.flip()

pygame.quit()