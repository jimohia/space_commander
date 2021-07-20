#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 14:47:08 2021

@author: jimmy

Pygame Project - "Space Command"
"""

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

#
pygame.mixer.music.load('space_song.wav')
pygame.mixer.music.play(loops = -1)

# Initialize Pygame
pygame.init()

# Define player class by extending Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('tie_fighter.png').convert()
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
    def __init__(self):
        super(Asteroid, self).__init__()
        self.surf = pygame.image.load('asteroid.png').convert()
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
    def __init__(self):
        super(Galaxy, self).__init__()
        self.surf = pygame.image.load('galaxy.png').convert()
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
    
# Set Screen Size with Width = 800 & Height = 600
screen_width = 800
screen_height = 600

# Create the screen object (surface) with screen width and height
screen = pygame.display.set_mode([screen_width,screen_height])



# Run variable for main loop
running = True

# Set up the game clock
clock = pygame.time.Clock()

# Create a custom event for adding a new enemy
ADDASTEROID = pygame.USEREVENT + 1
pygame.time.set_timer(ADDASTEROID, 250)

# Create a custom event for adding a background galaxy
ADDGALAXY = pygame.USEREVENT + 2
pygame.time.set_timer(ADDGALAXY, 4500)

#Instantiate the Player
player = Player()

# Create groups to hold asteroid sprites and all sprites
# - asteroids is used for collision detection and position updates
# - all_sprites is used for rendering
asteroids = pygame.sprite.Group()
galaxies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

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
            
        # Add a new enemy?
        elif event.type == ADDASTEROID:
            # Create the new enemy and add it to the sprites group
            new_asteroid = Asteroid()
            asteroids.add(new_asteroid)
            all_sprites.add(new_asteroid)
            
        # Add a new background galaxy?
        elif event.type == ADDGALAXY:
            new_galaxy = Galaxy()
            galaxies.add(new_galaxy)
            all_sprites.add(new_galaxy)
        
    # Get the set of pressed keys and store in dictionary
    pressed_keys = pygame.key.get_pressed()
    
    # Update asteroid position
    asteroids.update()
    
    # Update Galaxy background images
    galaxies.update()
    
    #Update player sprite based on player keypresses
    player.update(pressed_keys)
    
    # Fill the background color 
    screen.fill((0, 0, 0))
    
    
    # Draw the player on the screen
    for entity in all_sprites:
        screen.blit(entity.surf, (entity.rect))
    
    # Check for collisions
    if pygame.sprite.spritecollideany(player, asteroids):
        player.kill()
        running = False
    
    # Flip (update) the display
    pygame.display.flip()
    
    #Lock framerate
    clock.tick(30)

# Stop the music
pygame.mixer.music.stop()
pygame.mixer.quit()
    
#Done! Time to quit
pygame.quit()

