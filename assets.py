import pygame
from pygame.rect import Rect


class Spaceship:
    def __init__(self, screen):
        self.screen = screen
        self.space_img = pygame.image.load("bilder/ship.png")
        self.space_img = pygame.transform.scale(self.space_img, (50, 50))
        self.sc_width = screen.get_width()
        self.rect = self.space_img.get_rect()
        self.rect.x = int(self.sc_width / 2 - 25)
        self.rect.y = 525

    def draw(self):
        self.screen.blit(self.space_img, (int(self.rect.x), self.rect.y))

    def move_right(self):
        """This function decides how fast the spaceship can go to the right"""
        self.rect.x += 2

    def move_left(self):
        """This function decides how fast the spaceship can go to the left"""
        self.rect.x -= 2


class Enemy:
    def __init__(self, screen):
        """This is the settings for the enemy. If you want to configure the speed or
        how much the enemy drop as they reach the border of the screen"""
        self.screen = screen
        self.enemy_img = pygame.image.load("bilder/enemy.png")
        self.enemy_img = pygame.transform.scale(self.enemy_img, (32, 32))
        self.sc_width = screen.get_width()
        self.rect = self.enemy_img.get_rect()
        self.enemy_speed = 3
        self.enemy_drop = 32

    def enemy_move(self):
        """This function decides how fast and how far to the side the enemy should go"""
        self.rect.x += self.enemy_speed

        if self.rect.x <= 0:
            self.enemy_speed = 3
            self.rect.y += self.enemy_drop
        if self.rect.x >= 768:
            self.enemy_speed = -3
            self.rect.y += self.enemy_drop

    def draw(self):
        self.screen.blit(self.enemy_img, (int(self.rect.x), self.rect.y))


class Bullet:
    """This is the settings for the bullet. Here you can configure the speed, height, width and the color"""
    def __init__(self, screen, x, y):
        self.screen = screen

        self.bullet_speed = 5
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)

        self.rect = Rect(x + 30, y + 8, self.bullet_width, self.bullet_height)

    def draw(self):
        pygame.draw.rect(self.screen, self.bullet_color, self.rect)
        self.rect.y -= self.bullet_speed
