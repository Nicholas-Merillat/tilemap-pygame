import pygame
from settings import *

class Player():
    def __init__(self, x, y, width, height, tilemap):
        self.x = x
        self.y = y
        self.dx = x + width
        self.dy = y + height
        self.width = width
        self.height = height
        self.tilemap = tilemap

        self.velocity = pygame.math.Vector2(0, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.limit_right = TILE_SIZE * TILEMAP_SIZE[0]
        self.limit_bottom = TILE_SIZE * TILEMAP_SIZE[1]

        self.acceleration = 0.1
        self.max_speed = 1.5
        self.gravity = 0.2
        self.fall_speed_cap = 5
        self.jump_force = -3.5

    def update(self, delta, keys):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.direction = -int(keys[pygame.K_a]) + int(keys[pygame.K_d])
        self.want_to_jump = keys[pygame.K_w]

        self.velocity.x = pygame.math.lerp(self.velocity.x, self.max_speed * self.direction, self.acceleration * delta)
        self.velocity.y += self.gravity * delta
        if self.velocity.y > self.fall_speed_cap:
            self.velocity.y = self.fall_speed_cap

        self.x += self.velocity.x * delta
        self.y += self.velocity.y * delta
        self.dx = self.x + self.width
        self.dy = self.y + self.height

        # collision is based off tiles surrounding the player
        self.is_on_ground = False
        self.below_tile = self.tilemap.world_to_tile(self.x + self.width / 2, self.dy)
        self.above_tile = self.tilemap.world_to_tile(self.x + self.width / 2, self.y)
        self.right_tile = self.tilemap.world_to_tile(self.dx, self.y + self.height / 2)
        self.left_tile = self.tilemap.world_to_tile(self.x, self.y + self.height / 2)

        if self.tilemap.grid[int(self.below_tile.x)][int(self.below_tile.y)] != 0 and self.velocity.y >= 0:
            self.y = self.below_tile.y * TILE_SIZE - self.height
            self.velocity.y = 0
            self.is_on_ground = True
        elif self.tilemap.grid[int(self.above_tile.x)][int(self.above_tile.y)] != 0 and self.velocity.y <= 0:
            self.y = (self.above_tile.y + 1) * TILE_SIZE
            self.velocity.y = 0

        if self.tilemap.grid[int(self.right_tile.x)][int(self.right_tile.y)] != 0 and self.velocity.x >= 0:
            self.x = self.right_tile.x * TILE_SIZE - self.width
            self.velocity.x = 0
        elif self.tilemap.grid[int(self.left_tile.x)][int(self.left_tile.y)] != 0 and self.velocity.x <= 0: 
            self.x = (self.left_tile.x + 1) * TILE_SIZE
            self.velocity.x = 0

        # borders of world
        if self.x < 0:
            self.x = 0
            self.velocity.x = 0
        elif self.dx > self.limit_right:
            self.x = self.limit_right - self.width
            self.velocity.x = 0
        if self.y < 0:
            self.y = 0
            self.velocity.y = 0
        elif self.dy > self.limit_bottom:
            self.y = self.limit_bottom - self.height
            self.velocity.y = 0
            self.is_on_ground = True

        if self.want_to_jump and self.is_on_ground:
            self.want_to_jump = False
            self.velocity.y = self.jump_force
        elif self.want_to_jump == False and self.velocity.y <= 0:
            self.velocity.y /= 1.25

        self.rect.x = self.x
        self.rect.y = self.y