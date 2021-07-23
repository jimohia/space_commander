#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 14:47:08 2021

@author: jimmy

Pygame Project - "Space Command"
"""

    ### Imports and Initializations
# Import PyGame and Random libraries
import pygame 
import random
# Lets import some key bindings
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT    
    )
#Load pygame mixer for songs and sfx
pygame.mixer.init()
pygame.mixer.music.load('space_song.wav')
pygame.mixer.music.play(loops = -1)
# Initialize Pygame
pygame.init()

    ### Class Creation
# Define player class by extending Sprite
class Player(pygame.sprite.Sprite):
    """" This is the class for the player, there should
    only ever be one of these at a time... I think."""
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('tie_fighter.png').convert_alpha()
        self.surf.set_colorkey((255, 255, 254), RLEACCEL)
        self.rect = self.surf.get_rect()    
    # Def func() Move the Sprite based on player keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)
            # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
# Define Asteroid Class by extending Sprite
class Asteroid(pygame.sprite.Sprite):
    """ This is the class to create obstacles for the player to dodge.
    There may be many or few of these moving from right to left at 
    variable speeds and positions."""
    def __init__(self):
        super(Asteroid, self).__init__()
        self.surf = pygame.image.load('asteroid.png').convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0, screen_height))
                )
        self.speed = random.randint(1,3)        
    # Define the Asteroid's frame updates based on 'speed'
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
# Define Galaxy Class by extending Sprite
class Galaxy(pygame.sprite.Sprite):
    """ This is a class to implement background images that scroll
    past the player in game. The image should be a galaxy of some type
    hence the name of the class."""
    def __init__(self):
        super(Galaxy, self).__init__()
        self.surf = pygame.image.load('galaxy.png').convert_alpha()
        self.surf.set_colorkey((255, 255, 254), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(screen_width+20, screen_width + 100),
                random.randint(0, screen_height))
            )
        self.speed = random.randint(1,3)        
    # Define the Galaxy's frame updates based on 'speed'
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
# Define Enemy Class by extending Sprite
class Enemy(pygame.sprite.Sprite):
    """ This is a class to implement enemy ships. I hope to extend
    this class to encompass multiple types of enemy ships"""
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load('x_wing.png').convert_alpha()
        self.surf.set_colorkey((255, 255, 254), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0, screen_height))
            )
        self.speed = random.randint(3,6)
        self.last_shot = pygame.time.get_ticks()
        
        # Sprite Groups for Enemy Lasers
        self.sprites = all_sprites
        self.lasers = enemy_lasers
    # Define the enemy's frame updates based on speed
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        self.shoot()
    # Define shoot function to implement EnemyLaser
    def shoot(self):
        """ Fires enemy lasers"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > 1500:
            self.last_shot = current_time
            laser = EnemyLaser(self.rect.x, self.rect.y)
            self.sprites.add(laser)
            self.lasers.add(laser)
        
# Define EnemyLaser Class by extending Sprite
class EnemyLaser(pygame.sprite.Sprite):
    """"This is a class to implement laser blasts for the enemy
    X_wing fighter (rebel scum)."""
    def __init__(self, x, y):
        super(EnemyLaser, self).__init__()
        self.surf = pygame.image.load('laser_beam_red.png').convert_alpha()
        self.surf.set_colorkey((255, 255, 254), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.right = x
        self.rect.top = y
        self.speed = 10
    # Define the laser beam's frame updates
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        

    ### Clock and Screen    
# Set Screen Size with Width = 800 & Height = 600
screen_width = 800
screen_height = 600
# Create the screen object (surface) with screen width and height
screen = pygame.display.set_mode([screen_width,screen_height])
# Set up the game clock
clock = pygame.time.Clock()

    ### Instantiations and Instancing Events
# Create a custom event for adding a new asteroid
ADDASTEROID = pygame.USEREVENT + 1
pygame.time.set_timer(ADDASTEROID, 750)
# Create a custom event for adding a background galaxy
ADDGALAXY = pygame.USEREVENT + 2
pygame.time.set_timer(ADDGALAXY, 9000)
# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 3
pygame.time.set_timer(ADDENEMY, 4500)
#Instantiate the Player
player = Player()

    ### Sprite Groups
# Create groups to hold asteroid sprites and all sprites
# - asteroids is used for collision detection and position updates
# - all_sprites is used for rendering
asteroids = pygame.sprite.Group()
galaxies = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
enemy_lasers = pygame.sprite.Group()

    ### Game Loop
# Run variable for main loop
running = True
# Main loop
while running:
    # Run event handler
    for event in pygame.event.get():
        # Did the player depress a key?
        if event.type == KEYDOWN:
            # Was it the ESC key?
            if event.key == K_ESCAPE:
                running = False
        # Did the player click close?        
        elif event.type == pygame.QUIT:
            running = False            
        # Add a new asteroid?
        elif event.type == ADDASTEROID:
            # Create the new asteroid and add it to the sprites group
            new_asteroid = Asteroid()
            asteroids.add(new_asteroid)
            all_sprites.add(new_asteroid)
        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to the sprites group
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)     
        # Add a new background galaxy?
        elif event.type == ADDGALAXY:
            new_galaxy = Galaxy()
            galaxies.add(new_galaxy)
            all_sprites.add(new_galaxy)        
    # Get the set of pressed keys and store in dictionary
    pressed_keys = pygame.key.get_pressed()    
    # Update asteroid position
    asteroids.update()
    # Update enemies position
    enemies.update()    
    # Update Galaxy background images
    galaxies.update()
    # Update enemy lasers
    enemy_lasers.update()    
    #Update player sprite based on player keypresses
    player.update(pressed_keys)    
    # Fill the background color 
    screen.fill((0, 0, 0))    
    # Draw the player on the screen
    for entity in all_sprites:
        screen.blit(entity.surf, (entity.rect)) 
        
    # Check for player collisions
    if pygame.sprite.spritecollideany(player, asteroids):
        player.kill()
        running = False
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False
    if pygame.sprite.spritecollideany(player, enemy_lasers):
        player.kill()
        running = False
        
    # Check for NPO collisions
    collisions = pygame.sprite.groupcollide(
        asteroids, enemies, False, True)
    collisions = pygame.sprite.groupcollide(
        asteroids, enemy_lasers, False, True)
    collisions = pygame.sprite.groupcollide(
        enemies, enemy_lasers, True, True)
    
    # Flip (update) the display
    pygame.display.flip()    
    #Lock framerate
    clock.tick(30)

    ### End and Exit
# Stop the music
pygame.mixer.music.stop()
pygame.mixer.quit()    
#Done! Time to quit
pygame.quit()

