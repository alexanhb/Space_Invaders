import json
import pygame_menu
  
from assets import *

sc_width = 800
sc_height = 600

pygame.init()
menu_surface = pygame.display.set_mode((800, 800))


def start_the_game():
    screen = pygame.display.set_mode((sc_width, sc_height))
    pygame.display.set_caption("Space Invaders")
    background = pygame.image.load("bilder/background.png")

    # Enter your name text
    font = pygame.font.Font('freesansbold.ttf', 32)
    enter_name_text = font.render(f'Enter your name', True, (255, 0, 0))
    enter_name_rect = enter_name_text.get_rect()
    enter_name_rect.x = 250
    enter_name_rect.y = 350

    # Player input
    player_text = ""
    input_box = pygame.Rect(285, 400, 140, 32)

    # Lives text
    lives = 3
    font = pygame.font.Font('freesansbold.ttf', 32)
    lives_text = font.render(f'Lives: {lives}', True, (255, 0, 0))
    lives_text_rect = lives_text.get_rect()
    lives_text_rect.x = 0
    lives_text_rect.y = 535

    # You won text
    font = pygame.font.Font('freesansbold.ttf', 32)
    win_text = font.render(f'You won!', True, (255, 0, 0))
    win_text_rect = win_text.get_rect()
    win_text_rect.x = 310
    win_text_rect.y = 250

    # You lost text
    font = pygame.font.Font('freesansbold.ttf', 32)
    lost_text = font.render(f'You lost', True, (255, 0, 0))
    lost_text_rect = lost_text.get_rect()
    lost_text_rect.x = 315
    lost_text_rect.y = 250

    # Score text
    score = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    score_text = font.render(f'Score: {score}', True, (255, 0, 0))
    score_text_rect = score_text.get_rect()
    score_text_rect.x = 0
    score_text_rect.y = 570

    # Spaceship
    spaceship = Spaceship(screen)

    # Creating a list to store enemies
    enemies = []

    # Creating an enemy and calculating on how many enemies it should be on one row
    enemy = Enemy(screen)
    space_x = sc_width - 2 * enemy.rect.width
    number_of_enemies = space_x // (2 * enemy.rect.width)

    # Creating multiple rows of enemies. The higher height of the screen is more rows of enemies will be created.
    # Higher width of the game screen will spawn more enemies in each row
    space_y = (screen.get_height() - (5 * enemy.rect.height) - spaceship.rect.height)
    rows_of_enemies = space_y // (2 * enemy.rect.height)

    for rows in range(rows_of_enemies):
        for enemy_x in range(number_of_enemies):
            enemy = Enemy(screen)
            enemy_width, enemy_height = enemy.rect.size
            enemy.x = enemy_width + 2 * enemy_width * enemy_x
            enemy.rect.x = enemy.x
            enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * rows
            enemies.append(enemy)

    # Creating a list to store bullets
    bullets = []

    running = True
    clock = pygame.time.Clock()

    while running:
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # When you reached 0 lives or have killed all of the enemies this event will be used.
            # When you have lost you can type in your name and you score will be sent to the json file
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(player_text)
                    score_json = {
                        'name': player_text,
                        'score': score
                    }
                    with open('score.json', 'a') as file:
                        json.dump(score_json, file, ensure_ascii=False, indent=2)

                    running = False
                if event.key == pygame.K_BACKSPACE:
                    player_text = player_text[:-1]
                else:
                    player_text += event.unicode
            # Bullet mechanic using Space button to shoot
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(screen, spaceship.rect.x, spaceship.rect.y))

        # Player mechanic where left and right arrow keys moves the player and
        # forbids the player moving out of the screen
        if pressed[pygame.K_RIGHT] and spaceship.rect.x < sc_width - 60:
            spaceship.move_right()
        if pressed[pygame.K_LEFT] and spaceship.rect.x > 5:
            spaceship.move_left()

        for enemy in enemies:
            # Enemy Movement
            enemy.enemy_move()

            # Collision for spaceship and enemy and
            # if a enemy hits the spaceship it will be removed and lives will decrease by 1
            if enemy.rect.colliderect(spaceship.rect):
                enemies.remove(enemy)
                lives -= 1
                lives_text = font.render(f'Lives: {lives}', True, (255, 0, 0))
                if lives <= 0:
                    lives = 0
                    lives_text = font.render(f'Lives: {lives}', True, (255, 0, 0))
                    enemies.clear()

            # Collision for bullet and
            # enemy and if you hit an enemy add 10 to score and remove the enemy and bullet
            for bullet in bullets:
                if enemy.rect.colliderect(bullet.rect):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 10
                    score_text = font.render(f'Score: {score}', True, (255, 0, 0))

        # Draw
        screen.blit(background, (0, 0))
        screen.blit(lives_text, lives_text_rect)
        screen.blit(score_text, score_text_rect)

        # If lives reaches 0 you have lost. A text block will tell you "You lost"
        if lives == 0:
            screen.blit(lost_text, lost_text_rect)
            screen.blit(score_text, (310, 300))
            screen.blit(enter_name_text, enter_name_rect)
            txt_surface = font.render(player_text, True, (255, 0, 0))
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, (255, 0, 0), input_box, 2)

        # If you have killed all of the enemies and you are still above 0 lives, you have won.
        # When you are at the victory screen
        # you are able to type in your name and your score will be sent to the json file
        if enemies == [] and lives >= 1:
            screen.blit(win_text, win_text_rect)
            screen.blit(score_text, (300, 300))
            screen.blit(enter_name_text, enter_name_rect)
            txt_surface = font.render(player_text, True, (255, 0, 0))
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, (255, 0, 0), input_box, 2)

        spaceship.draw()
        for bullet in bullets:
            bullet.draw()

        for enemy in enemies:
            enemy.draw()
        pygame.display.update()

        clock.tick(60)


def leaderboard():
    with open("score.json", "r") as file:
        data = file.read()
        new_data = data.replace('}{', '},{')
        json_data = json.loads(f'[{new_data}]')

    leaderboard_menu = pygame_menu.Menu(800, 800, "Leaderboard", theme=pygame_menu.themes.THEME_BLUE)
    for line in json_data:
        leaderboard_menu.add_label(line['name'])
        leaderboard_menu.add_label(line['score'])
        leaderboard_menu.add_vertical_margin(20)

    leaderboard_menu.add_button("Back", menu)
    leaderboard_menu.mainloop(menu_surface)


def controls():
    controls_menu = pygame_menu.Menu(800, 800, "Leaderboard", theme=pygame_menu.themes.THEME_BLUE)
    controls_menu.add_label("Left and right arrow keys to move")
    controls_menu.add_vertical_margin(20)
    controls_menu.add_label("Space - Fire lasers from the spaceship")
    controls_menu.add_button("Back", menu)
    controls_menu.mainloop(menu_surface)


menu = pygame_menu.Menu(800, 800, "Space Invaders", theme=pygame_menu.themes.THEME_BLUE)
menu.add_button("Play", start_the_game)
menu.add_button("Leaderboard", leaderboard)
menu.add_button("Controls", controls)
menu.add_button("Quit", pygame_menu.events.EXIT)

menu.mainloop(menu_surface)
