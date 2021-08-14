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
# Set Colors 
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
#Load pygame mixer for songs and sfx
pygame.mixer.init()
pygame.mixer.music.load('space_song.wav')
pygame.mixer.music.play(loops = -1)
# Initialize Pygame
pygame.init()
pygame.font.init()
# Define Round Function
def Round():
    """This function is to be called to start a round of the game"""
    running = True
    for sprite in all_sprites:
        sprite.kill()
    for sprite in death_star_group:
        sprite.kill()
    for sprite in death_star_explode:
        sprite.kill()
    player = Player()
    all_sprites.add(player)    
    score = 0
    splash = 0
    Laser.count_laser = 0
        ### Game Loop
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
                # Create the new X-wing and add it to the sprites group
                new_enemy = X_wing()
                enemies.add(new_enemy)
                x_wings.add(new_enemy)
                all_sprites.add(new_enemy)
            # Add a Y-wing?
            elif event.type == ADDYWING:
                new_y_wing = Y_wing()
                enemies.add(new_y_wing)
                y_wings.add(new_y_wing)
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
        # Update Explostions
        y_explodes.update()
        x_explodes.update()
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
            Score_screen(splash)
        if pygame.sprite.spritecollideany(player, enemies):
            explosion_wav.play()
            player.kill()
            running = False
            Score_screen(splash)
        if pygame.sprite.spritecollideany(player, enemy_lasers):
            explosion_wav.play()
            player.kill()
            running = False
            Score_screen(splash)
        ### Need to parse out x and y wings
        player_shoot_y_wing = pygame.sprite.groupcollide(
            player_lasers, y_wings, True, True)
        for hit in player_shoot_y_wing:
            explosion_wav.play()
            splash = splash + 1
            y_exp = Y_wing_explode(hit.rect.centerx, hit.rect.centery)
            all_sprites.add(y_exp)
            y_explodes.add(y_exp)
        player_shoot_x_wing = pygame.sprite.groupcollide(
            player_lasers, x_wings, True, True)
        for hit in player_shoot_x_wing:
            explosion_wav.play()
            splash = splash + 1
            x_exp = X_wing_explode(hit.rect.centerx, hit.rect.centery)
            all_sprites.add(x_exp)
            x_explodes.add(x_exp)
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


def Score_screen(splash):
    """A function to call the score screen"""
    # Score Screen
    score_screen = True
    death_star = Death_star()
    death_star_group.add(death_star)
    screen.fill((0, 0, 0))
    if Laser.count_laser == 0:
        hit_ratio = 0
    else:
        hit_ratio = splash / (Laser.count_laser) * 100
    score = splash * 1000 * hit_ratio // 100
    while score_screen == True:
        font = pygame.font.SysFont(sysfont, 24)
        splash_img = font.render('You Destroyed ' + str(splash) + ' Rebel Scum', 
                                 True, YELLOW)
        ratio_img = font.render('Hit Ratio = ' + str(int(hit_ratio)) + '%', True, BLUE)
        score_img = font.render('Your Score: ' + str(int(score)), True, BLUE)
        end_img = font.render('Hit Escape to Exit, Space to Play Again', True, BLUE)
    
        ### Screen Blits
        screen.blit(splash_img, (screen_width/2 - splash_img.get_width()/2, 
                                 screen_height/2 - splash_img.get_height()/2)
                    )
        screen.blit(ratio_img, (screen_width/2 - ratio_img.get_width()/2, 
                                screen_height/2 - ratio_img.get_height()/2 + 
                                splash_img.get_height())
                    )    
        screen.blit(score_img, (screen_width/2 - score_img.get_width()/2,
                                screen_height/2 - score_img.get_height()/2 +
                                splash_img.get_height() +
                                ratio_img.get_height())
                    )    
        screen.blit(end_img, (screen_width/2-(end_img.get_width()/2),
                              screen_height/2 - end_img.get_height()/2 + 
                              splash_img.get_height() + 
                              ratio_img.get_height() + 
                              score_img.get_height())
                    )


        # Draw the player on the screen
    
        death_star_group.update()
        death_star_explode.update()
    
        for entity in death_star_explode:
            screen.blit(entity.surf, (entity.rect))
        for entity in death_star_group:
            screen.blit(entity.surf, (entity.rect))
        pygame.display.flip()
        # Update the Background
        background.update()
        background.render()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    score_screen = False
                    Round()
                elif event.key == K_ESCAPE:
                    running = False
                    score_screen = False
                elif event.type == pygame.QUIT:
                    running = False
                    score_screen = False

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
    count_laser = 0
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
        self.count_laser = Laser.count_laser
        Laser.count_laser += 1
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
        self.speed = 1        
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
# Define Y-Wing Explosion Class
class Y_wing_explode(pygame.sprite.Sprite):
    """ This class is to explode Y-wings when destroyed"""
    def __init__(self, x, y):
        super(Y_wing_explode, self).__init__()
        self.surf = pygame.image.load('y_wing_explosion_1.png').convert_alpha()
        self.anim_image = []
        for filename in ['y_wing_explosion_2.png',
                      'y_wing_explosion_3.png',
                      'y_wing_explosion_4.png']:
            self.anim_image.append(pygame.image.load(filename).convert_alpha())
        self.rect = self.surf.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.timer = pygame.time.get_ticks()
        self.img_ind = -1
    def update(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.timer > 200:
            self.timer = pygame.time.get_ticks()            
            self.img_ind = self.img_ind + 1
            if self.img_ind == len(self.anim_image):
                    self.kill()
            else:
                self.surf = self.anim_image[self.img_ind]                        
# Define X_wing_explode class
class X_wing_explode(pygame.sprite.Sprite):
    """ This class is to explode Y-wings when destroyed"""
    def __init__(self, x, y):
        super(X_wing_explode, self).__init__()
        self.surf = pygame.image.load('x_wing_explosion_1.png').convert_alpha()
        self.anim_image = []
        for filename in ['x_wing_explosion_2.png',
                      'x_wing_explosion_3.png',
                      'x_wing_explosion_4.png']:
            self.anim_image.append(pygame.image.load(filename).convert_alpha())
        self.rect = self.surf.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.timer = pygame.time.get_ticks()
        self.img_ind = -1
    def update(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.timer > 200:
            self.timer = pygame.time.get_ticks()            
            self.img_ind = self.img_ind + 1
            if self.img_ind == len(self.anim_image):
                    self.kill()
            else:
                self.surf = self.anim_image[self.img_ind]                        
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
class Death_star(pygame.sprite.Sprite):
    """ This is a class to implement Death Star."""
    def __init__(self):
        super(Death_star, self).__init__()
        self.surf = pygame.image.load('death_star.png').convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center = (175, 175))
        self.speed = 0
        self.timer = pygame.time.get_ticks()
        
    # Define the enemy's frame updates based on speed
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.timer > 2000:
            boom = Death_star_explode()
            death_star_explode.add(boom)
            self.kill()
        if self.rect.right < 0:
            self.kill()
        
            
class Death_star_explode(pygame.sprite.Sprite):
    """ This class is to explode Death Star at end screen"""
    def __init__(self):
        super(Death_star_explode, self).__init__()
        self.surf = pygame.image.load('death_star_explosion_1.png').convert_alpha()
        self.anim_image = []
        for filename in ['death_star_explosion_2.png',
                      'death_star_explosion_3.png',
                      'death_star_explosion_4.png',
                      'death_star_explosion_5.png',
                      'death_star_explosion_6.png',
                      'death_star_explosion_7.png']:
            self.anim_image.append(pygame.image.load(filename).convert_alpha())
        self.rect = self.surf.get_rect(center = (175, 175))
        self.timer = pygame.time.get_ticks()
        self.img_ind = -1
    def update(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.timer > 150:
            self.timer = pygame.time.get_ticks()            
            self.img_ind = self.img_ind + 1
            if self.img_ind == len(self.anim_image):
                    self.kill()
            else:
                self.surf = self.anim_image[self.img_ind]
            self.rect = self.surf.get_rect(center = (175, 175))

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
pygame.time.set_timer(ADDASTEROID, 1500)
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
y_explodes = pygame.sprite.Group()
x_explodes = pygame.sprite.Group()
x_wings = pygame.sprite.Group()
y_wings = pygame.sprite.Group()
death_star_explode = pygame.sprite.Group()
death_star_group = pygame.sprite.Group()

# Load sounds for the game here
enemy_laser_wav = pygame.mixer.Sound('fire_laser.wav')
explosion_wav = pygame.mixer.Sound('explosion.wav')
player_laser_wav = pygame.mixer.Sound('laser_fire_2.wav')

# Set Background
background = Background()

# Run variable for main loop
menu = True
running = True
score_screen = True

# Start Menu
sysfont = pygame.font.get_default_font()
while menu == True:
    font = pygame.font.SysFont(sysfont, 24)
    title = font.render('#EmpireDidNothingWrong', True, YELLOW)
    img = font.render('Hit Space to Start. Escape to Exit', True, BLUE)
    screen.blit(title, (screen_width/2 - (title.get_width()/2), 
                      screen_height/2 - (title.get_height()/2))
                )
   
    screen.blit(img, (screen_width/2-(img.get_width()/2), 
                      screen_height/2 - (img.get_height()/2)
                      + (title.get_height()))
                )
    pygame.display.update()
    # Update the Background
    background.update()
    background.render()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                menu = False
            elif event.key == K_ESCAPE:
                running = False
                menu = False
        elif event.type == pygame.QUIT:
            running = False
            menu = False


    ### Game Loop
Round()

### End and Exit
# Stop the music
pygame.mixer.music.stop()
pygame.mixer.quit()    
#Done! Time to quit
pygame.quit()

