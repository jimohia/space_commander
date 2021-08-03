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
    K_SPACE,
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
# Define a background Class
class Background():
    """"This class is to implement horizontal scrolling backgrounds."""
    def __init__(self):
        self.surf = pygame.image.load('star_field.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.x_1 = 0
        self.y_1 = 0
        self.x_2 = screen_width
        self.y_2 = 0
        self.speed = 0.5
    def update(self):
        self.x_1 -= self.speed
        self.x_2 -= self.speed
        if self.x_1 <= -screen_width:
            self.x_1 = 0
            self.x_2 = screen_width
    def render(self):
        screen.blit(self.surf, (self.x_1, self.y_1))
        screen.blit(self.surf, (self.x_2, self.y_2))
# Define player class by extending Sprite
class Player(pygame.sprite.Sprite):
    """" This is the class for the player, there should
    only ever be one of these at a time... I think."""
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('tie_fighter.png').convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.last_shot = pygame.time.get_ticks()
        # Sprite Groups for Player Lasers
        self.sprites = all_sprites
        self.lasers = player_lasers
        self.rect.centerx = 10
        self.rect.centery = screen_height / 2
    # Def func() Move the Sprite based on player keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -4)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 4)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-4, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(4 , 0)
        if pressed_keys[K_SPACE]:
            self.player_shoot()
            # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
    def player_shoot(self):
        """ Fires player (TIE) lasers"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > 250:
            self.last_shot = current_time
            laser = Laser(self.rect.right, self.rect.centery)
            player_laser_wav.play()
            player_laser_wav.set_volume(0.5)
            self.sprites.add(laser)
            self.lasers.add(laser)    
# Define Laser Class by extending Sprite
class Laser(pygame.sprite.Sprite):
    """"This is a class to implement laser blasts for the player
    TIE fighter (#EmpireDidNothingWrong)."""
    def __init__(self, x, y):
        super(Laser, self).__init__()
        self.surf = pygame.image.load('laser_beam_green.png').convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.speed = 8
    # Define the laser beam's frame updates
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > screen_width:
            self.kill()
# Define Asteroid Class by extending Sprite
class Asteroid(pygame.sprite.Sprite):
    """ This is the class to create obstacles for the player to dodge.
    There may be many or few of these moving from right to left at 
    variable speeds and positions."""
    def __init__(self):
        super(Asteroid, self).__init__()
        self.surf = pygame.image.load('asteroid.png').convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.x = random.randint(10, screen_width + 300)
        if self.x < screen_width:
            self.y = -10
        else:
            self.y = random.randint(0, 0.5 * screen_height)
        self.rect = self.surf.get_rect(
            center = (self.x, self.y))
        self.speed = random.randint(1,2)
        self.orig_image = self.surf
        self.angle = 0        
    # Define the Asteroid's frame updates based on 'speed'
    def update(self):
        self.rect.move_ip(-self.speed, self.speed)
        self.angle += 8
        self.rotate()
        if self.rect.right < 0:
            self.kill()
        elif self.rect.top > screen_height:
            self.kill()
    def rotate(self):
        """Rotate the image of the sprite around its center."""
        # `rotozoom` usually looks nicer than `rotate`. Pygame's rotation
        # functions return new images and don't modify the originals.
        self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center=self.rect.center)
        self.surf = self.image
# Define Galaxy Class by extending Sprite
class Galaxy(pygame.sprite.Sprite):
    """ This is a class to implement background images that scroll
    past the player in game. The image should be a galaxy of some type
    hence the name of the class."""
    def __init__(self):
        super(Galaxy, self).__init__()
        self.surf = pygame.image.load('galaxy.png').convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(screen_width+20, screen_width + 100),
                random.randint(0, screen_height))
            )
        self.speed = random.randint(1,2)        
    # Define the Galaxy's frame updates based on 'speed'
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
# Define Enemy Class by extending Sprite
class Enemy(pygame.sprite.Sprite):
    """ This is a class to implement enemy ships. This class is 
    extended to encompass multiple types of enemy ships"""
    def __init__(self):
        super(Enemy, self).__init__()
        # Class attributes
        self.last_shot = pygame.time.get_ticks()        
        # Sprite Groups for Enemy Lasers
        self.sprites = all_sprites
        self.lasers = enemy_lasers
        
# this is the X-wing subclass
class X_wing(Enemy):
    """Implements a class for X-wings, a subclass of Enemy"""
    def __init__(self):
        super(X_wing, self).__init__()
        self.surf = pygame.image.load('x_wing.png').convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0 + 10, screen_height - 10))
            )
        self.speed = random.randint(2,3)
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
        if current_time - self.last_shot > 2500:
            self.last_shot = current_time
            laser = EnemyLaser(self.rect.x, self.rect.y)
            enemy_laser_wav.play()
            enemy_laser_wav.set_volume(0.5)
            self.sprites.add(laser)
            self.lasers.add(laser)
            
class Y_wing(Enemy):
    """ This is a class to implement Y-wings."""
    def __init__(self):
        super(Y_wing, self).__init__()
        self.surf = pygame.image.load('y_wing.png').convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0 + 10, screen_height - 10))
            )
        self.speed = random.randint(1,2)
        self.last_shot = pygame.time.get_ticks()
        
    # Define the enemy's frame updates based on speed
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
    
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
        self.speed = 5
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
pygame.time.set_timer(ADDASTEROID, 500)
# Create a custom event for adding a background galaxy
ADDGALAXY = pygame.USEREVENT + 2
pygame.time.set_timer(ADDGALAXY, 9000)
# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 3
pygame.time.set_timer(ADDENEMY, 4500)
# Create Y_wings
ADDYWING = pygame.USEREVENT + 4
pygame.time.set_timer(ADDYWING, 5500)

    ### Sprite Groups
# Create groups to hold asteroid sprites and all sprites
# - asteroids is used for collision detection and position updates
# - all_sprites is used for rendering
asteroids = pygame.sprite.Group()
galaxies = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
enemy_lasers = pygame.sprite.Group()
player_lasers = pygame.sprite.Group()

# Load sounds for the game here
enemy_laser_wav = pygame.mixer.Sound('fire_laser.wav')
explosion_wav = pygame.mixer.Sound('explosion.wav')
player_laser_wav = pygame.mixer.Sound('laser_fire_2.wav')

#Instantiate the Player
player = Player()
all_sprites.add(player)

# Set Background
background = Background()

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
            new_enemy = X_wing()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        # Add a Y-wing?
        elif event.type == ADDYWING:
            new_y_wing = Y_wing()
            enemies.add(new_y_wing)
            all_sprites.add(new_y_wing)
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
    # Update player_lasers
    player_lasers.update() 
    #Update player sprite based on player keypresses
    player.update(pressed_keys)   
    # Fill the background color 
    screen.fill((0, 0, 0))
    #Blitting
    # Update the Background
    background.update()
    background.render()
    # Draw the player on the screen
    for entity in all_sprites:
        screen.blit(entity.surf, (entity.rect)) 
    # Check for player collisions
    if pygame.sprite.spritecollideany(player, asteroids):
        explosion_wav.play()
        player.kill()
        running = False
    if pygame.sprite.spritecollideany(player, enemies):
        explosion_wav.play()
        player.kill()
        running = False
    if pygame.sprite.spritecollideany(player, enemy_lasers):
        explosion_wav.play()
        player.kill()
        running = False
    player_shoot_enemy = pygame.sprite.groupcollide(
        player_lasers, enemies, True, True)
    for hit in player_shoot_enemy:
        explosion_wav.play()
    collisions = pygame.sprite.groupcollide(
        player_lasers, asteroids, True, False)
        
    # Check for NPO collisions
    enemy_hit_asteroid = pygame.sprite.groupcollide(
        asteroids, enemies, False, True)
    for hit in enemy_hit_asteroid:
        explosion_wav.play()
    collisions = pygame.sprite.groupcollide(
        asteroids, enemy_lasers, False, True)
    enemy_hit_enemy = pygame.sprite.groupcollide(
        enemies, enemy_lasers, True, True)
    for hit in enemy_hit_enemy:
        explosion_wav.play()
    
    # Flip (update) the display
    pygame.display.flip()    
    #Lock framerate
    clock.tick(60)

    ### End and Exit
# Stop the music
pygame.mixer.music.stop()
pygame.mixer.quit()    
#Done! Time to quit
pygame.quit()

