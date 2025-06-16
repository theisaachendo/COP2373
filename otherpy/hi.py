#build a game where its like doom but you can move around and shoot enemies and collect items and upgrade your weapons and health and ammo and etc.

import pygame
import random
import math
import os
import numpy as np
from noise import pnoise2
from PIL import Image
from pygame import mixer

# Initialize Pygame and mixer
pygame.init()
mixer.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Horror FPS")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
BLOOD_RED = (139, 0, 0)

# Generate textures
def generate_wall_texture(size=256):
    texture = np.zeros((size, size, 3), dtype=np.uint8)
    for y in range(size):
        for x in range(size):
            # Generate noise-based texture
            noise = pnoise2(x/32, y/32, octaves=4, persistence=0.5)
            color = int((noise + 1) * 128)
            texture[y, x] = [color, color, color]
    return pygame.surfarray.make_surface(texture)

def generate_floor_texture(size=256):
    texture = np.zeros((size, size, 3), dtype=np.uint8)
    for y in range(size):
        for x in range(size):
            # Generate tile-like pattern
            tile_x = (x // 32) % 2
            tile_y = (y // 32) % 2
            color = 100 if (tile_x + tile_y) % 2 == 0 else 150
            texture[y, x] = [color, color, color]
    return pygame.surfarray.make_surface(texture)

# Generate sounds
def generate_gunshot_sound():
    sample_rate = 44100
    duration = 0.1
    t = np.linspace(0, duration, int(sample_rate * duration))
    # Generate white noise
    noise = np.random.uniform(-1, 1, len(t))
    # Add decay
    decay = np.exp(-t * 50)
    sound = noise * decay
    # Convert to 16-bit integer
    sound = (sound * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(sound)

def generate_enemy_sound():
    sample_rate = 44100
    duration = 0.5
    t = np.linspace(0, duration, int(sample_rate * duration))
    # Generate creepy sound
    freq = np.linspace(200, 100, len(t))
    sound = np.sin(2 * np.pi * freq * t)
    # Add some noise
    sound += np.random.uniform(-0.2, 0.2, len(t))
    # Add decay
    decay = np.exp(-t * 2)
    sound = sound * decay
    # Convert to 16-bit integer
    sound = (sound * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(sound)

# Generate textures and sounds
WALL_TEXTURE = generate_wall_texture()
FLOOR_TEXTURE = generate_floor_texture()
GUNSHOT_SOUND = generate_gunshot_sound()
ENEMY_SOUND = generate_enemy_sound()

# Map settings
MAP_SIZE = 15
CELL_SIZE = 50
WALL_HEIGHT = 200

# Enhanced map layout with more complex structure
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Player class
class Player:
    def __init__(self):
        self.x = 2 * CELL_SIZE
        self.y = 2 * CELL_SIZE
        self.angle = 0
        self.speed = 3
        self.health = 100
        self.ammo = 30
        self.shooting = False
        self.last_shot = 0
        self.shoot_delay = 250
        self.gun_offset = 0
        self.gun_recoil = 0
        self.weapons = {
            'pistol': {'damage': 25, 'ammo': 30, 'fire_rate': 250},
            'shotgun': {'damage': 50, 'ammo': 8, 'fire_rate': 1000}
        }
        self.current_weapon = 'pistol'

    def move(self, keys):
        dx = math.cos(math.radians(self.angle)) * self.speed
        dy = -math.sin(math.radians(self.angle)) * self.speed

        if keys[pygame.K_w]:
            new_x = self.x + dx
            new_y = self.y + dy
            if not self.check_collision(new_x, new_y):
                self.x = new_x
                self.y = new_y
        if keys[pygame.K_s]:
            new_x = self.x - dx
            new_y = self.y - dy
            if not self.check_collision(new_x, new_y):
                self.x = new_x
                self.y = new_y
        if keys[pygame.K_a]:
            new_x = self.x + math.cos(math.radians(self.angle - 90)) * self.speed
            new_y = self.y - math.sin(math.radians(self.angle - 90)) * self.speed
            if not self.check_collision(new_x, new_y):
                self.x = new_x
                self.y = new_y
        if keys[pygame.K_d]:
            new_x = self.x + math.cos(math.radians(self.angle + 90)) * self.speed
            new_y = self.y - math.sin(math.radians(self.angle + 90)) * self.speed
            if not self.check_collision(new_x, new_y):
                self.x = new_x
                self.y = new_y

    def check_collision(self, x, y):
        map_x = int(x / CELL_SIZE)
        map_y = int(y / CELL_SIZE)
        if 0 <= map_x < MAP_SIZE and 0 <= map_y < MAP_SIZE:
            return MAP[map_y][map_x] == 1
        return True

    def rotate(self, mouse_movement):
        self.angle += mouse_movement[0] * 0.1
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

    def shoot(self):
        current_time = pygame.time.get_ticks()
        weapon = self.weapons[self.current_weapon]
        if (current_time - self.last_shot > weapon['fire_rate'] and 
            self.ammo > 0):
            self.last_shot = current_time
            self.ammo -= 1
            self.gun_recoil = 10
            GUNSHOT_SOUND.play()
            return True
        return False

    def switch_weapon(self):
        if self.current_weapon == 'pistol':
            self.current_weapon = 'shotgun'
        else:
            self.current_weapon = 'pistol'

    def update(self):
        if self.gun_recoil > 0:
            self.gun_recoil -= 1

    def draw(self, screen):
        # Draw player body
        pygame.draw.circle(screen, BLUE, (self.x, self.y), 20)
        
        # Draw gun
        gun_x = self.x + math.cos(math.radians(self.angle)) * self.gun_offset
        gun_y = self.y - math.sin(math.radians(self.angle)) * self.gun_offset
        pygame.draw.rect(screen, GRAY, (gun_x - 5, gun_y - 5, 20, 10))
        
        # Draw direction indicator
        end_x = self.x + math.cos(math.radians(self.angle)) * 30
        end_y = self.y - math.sin(math.radians(self.angle)) * 30
        pygame.draw.line(screen, WHITE, (self.x, self.y), (end_x, end_y), 2)

# Bullet class
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10
        self.lifetime = 100

    def move(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed
        self.lifetime -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), 3)

# Enemy class
class Enemy:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = random.randint(2, MAP_SIZE - 2) * CELL_SIZE
        self.y = random.randint(2, MAP_SIZE - 2) * CELL_SIZE
        self.speed = 1.5
        self.health = 150
        self.color = BLOOD_RED
        self.attack_range = 50
        self.attack_damage = 10
        self.last_attack = 0
        self.attack_delay = 1000
        self.is_attacking = False
        self.last_sound = 0
        self.sound_delay = 2000

    def move_towards_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_sound > self.sound_delay:
            ENEMY_SOUND.play()
            self.last_sound = current_time
        
        if dist < self.attack_range:
            self.is_attacking = True
            if current_time - self.last_attack > self.attack_delay:
                player.health -= self.attack_damage
                self.last_attack = current_time
        else:
            self.is_attacking = False
            if dist != 0:
                new_x = self.x + (dx / dist) * self.speed
                new_y = self.y + (dy / dist) * self.speed
                if not self.check_collision(new_x, new_y):
                    self.x = new_x
                    self.y = new_y

    def check_collision(self, x, y):
        map_x = int(x / CELL_SIZE)
        map_y = int(y / CELL_SIZE)
        if 0 <= map_x < MAP_SIZE and 0 <= map_y < MAP_SIZE:
            return MAP[map_y][map_x] == 1
        return True

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 15)
        # Health bar
        health_width = 30 * (self.health / 100)
        pygame.draw.rect(screen, RED, (self.x - 15, self.y - 25, 30, 5))
        pygame.draw.rect(screen, GREEN, (self.x - 15, self.y - 25, health_width, 5))

def draw_3d_view(screen, player, enemies, bullets):
    # Draw ceiling
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT // 2))
    
    # Draw floor with texture
    floor_rect = pygame.Rect(0, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT // 2)
    screen.blit(FLOOR_TEXTURE, floor_rect)

    # Cast rays for walls
    for x in range(0, WINDOW_WIDTH, 2):
        ray_angle = (player.angle - 30) + (x / WINDOW_WIDTH) * 60
        ray_x = player.x
        ray_y = player.y
        distance = 0
        hit_wall = False

        while not hit_wall and distance < MAP_SIZE * CELL_SIZE:
            distance += 1
            ray_x = player.x + math.cos(math.radians(ray_angle)) * distance
            ray_y = player.y - math.sin(math.radians(ray_angle)) * distance

            map_x = int(ray_x / CELL_SIZE)
            map_y = int(ray_y / CELL_SIZE)

            if 0 <= map_x < MAP_SIZE and 0 <= map_y < MAP_SIZE:
                if MAP[map_y][map_x] == 1:
                    hit_wall = True
                    wall_height = min(WALL_HEIGHT * (CELL_SIZE / distance), WINDOW_HEIGHT)
                    # Calculate texture coordinates
                    texture_x = int((ray_x + ray_y) * 2) % WALL_TEXTURE.get_width()
                    wall_slice = WALL_TEXTURE.subsurface((texture_x, 0, 2, WALL_TEXTURE.get_height()))
                    wall_slice = pygame.transform.scale(wall_slice, (2, int(wall_height)))
                    screen.blit(wall_slice, (x, (WINDOW_HEIGHT - wall_height) // 2))

    # Draw enemies
    for enemy in enemies:
        dx = enemy.x - player.x
        dy = enemy.y - player.y
        enemy_angle = math.degrees(math.atan2(-dy, dx))
        angle_diff = (enemy_angle - player.angle) % 360
        if angle_diff > 180:
            angle_diff -= 360

        if abs(angle_diff) < 30:
            distance = math.sqrt(dx * dx + dy * dy)
            enemy_height = min(WALL_HEIGHT * (CELL_SIZE / distance), WINDOW_HEIGHT)
            enemy_width = enemy_height
            screen_x = (angle_diff + 30) * (WINDOW_WIDTH / 60)
            
            # Draw enemy with animation
            enemy_surface = pygame.Surface((int(enemy_width), int(enemy_height)))
            enemy_surface.fill(enemy.color)
            if enemy.is_attacking:
                # Draw attack animation
                pygame.draw.line(enemy_surface, WHITE, 
                               (0, 0), (enemy_width, enemy_height), 3)
                pygame.draw.line(enemy_surface, WHITE,
                               (enemy_width, 0), (0, enemy_height), 3)
            
            screen.blit(enemy_surface, 
                       (screen_x - enemy_width/2,
                        (WINDOW_HEIGHT - enemy_height) // 2))

def draw_gun(screen, player):
    # Draw gun based on current weapon
    gun_x = WINDOW_WIDTH // 2
    gun_y = WINDOW_HEIGHT - 100 - player.gun_recoil
    
    if player.current_weapon == 'pistol':
        pygame.draw.rect(screen, DARK_GRAY, (gun_x - 20, gun_y, 40, 80))
        pygame.draw.rect(screen, GRAY, (gun_x - 10, gun_y - 20, 20, 20))
    else:  # shotgun
        pygame.draw.rect(screen, DARK_GRAY, (gun_x - 30, gun_y, 60, 100))
        pygame.draw.rect(screen, GRAY, (gun_x - 20, gun_y - 30, 40, 30))

def draw_hud(screen, player):
    # Draw health bar
    pygame.draw.rect(screen, RED, (10, 10, 200, 20))
    pygame.draw.rect(screen, GREEN, (10, 10, 2 * player.health, 20))
    
    # Draw ammo and weapon info
    font = pygame.font.Font(None, 36)
    ammo_text = font.render(f"{player.current_weapon.upper()}: {player.ammo}", True, WHITE)
    screen.blit(ammo_text, (10, 40))

# Create game objects
player = Player()
enemies = [Enemy() for _ in range(5)]
bullets = []

# Game loop
running = True
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_TAB:
                player.switch_weapon()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if player.shoot():
                    bullets.append(Bullet(player.x, player.y, player.angle))
        elif event.type == pygame.MOUSEMOTION:
            player.rotate(event.rel)

    # Get keyboard input
    keys = pygame.key.get_pressed()
    player.move(keys)
    player.update()

    # Update bullets
    for bullet in bullets[:]:
        bullet.move()
        if bullet.lifetime <= 0:
            bullets.remove(bullet)
            continue

        # Check bullet collision with enemies
        for enemy in enemies[:]:
            dx = bullet.x - enemy.x
            dy = bullet.y - enemy.y
            if math.sqrt(dx * dx + dy * dy) < 20:
                enemy.health -= player.weapons[player.current_weapon]['damage']
                if enemy.health <= 0:
                    enemies.remove(enemy)
                if bullet in bullets:
                    bullets.remove(bullet)
                break

    # Update enemies
    for enemy in enemies:
        enemy.move_towards_player(player)

    # Clear screen
    screen.fill(BLACK)

    # Draw 3D view
    draw_3d_view(screen, player, enemies, bullets)
    
    # Draw gun
    draw_gun(screen, player)
    
    # Draw HUD
    draw_hud(screen, player)

    # Update display
    pygame.display.flip()

    # Control game speed
    clock.tick(60)

# Quit game
pygame.quit()  