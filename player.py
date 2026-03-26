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

        self.speed_accel = 0.04
        self.speed_max = 1.25
        self.gravity = 0.15
        self.fall_speed_cap = 5
        self.jump_force = -3

    def update(self, delta, keys):
        self.direction = -int(keys[pygame.K_a]) + int(keys[pygame.K_d])
        self.want_to_jump = keys[pygame.K_w]
        
        self.velocity.x = pygame.math.lerp(self.velocity.x, self.speed_max * self.direction, easeOutQuad(self.speed_accel) * delta)
        self.velocity.y += self.gravity * delta
        if self.velocity.y > self.fall_speed_cap:
            self.velocity.y = self.fall_speed_cap

        self.prev_x = self.x
        self.prev_y = self.y
        self.x += self.velocity.x * delta
        self.y += self.velocity.y * delta

        # Prevents player from traveling a distance greater than a singular tile (This fixes the bug with window focus and delta)
        if abs(self.y - self.prev_y) > TILE_SIZE:
            self.y = self.prev_y
        if abs(self.x - self.prev_x) > TILE_SIZE:
            self.x = self.prev_x

        self.dx = self.x + self.width
        self.dy = self.y + self.height

        # Get the surrounding tiles around the player and if there are any tiles, do collision
        self.is_on_ground = False

        self.below_tile_left = self.tilemap.world_to_tile(self.x + 1, self.dy)
        self.below_tile_right = self.tilemap.world_to_tile(self.dx - 1, self.dy)

        self.above_tile_left = self.tilemap.world_to_tile(self.x + 1, self.y)
        self.above_tile_right = self.tilemap.world_to_tile(self.dx - 1, self.y)

        self.right_tile_top = self.tilemap.world_to_tile(self.dx, (self.y + self.height * 0.5) - 1)
        self.right_tile_bottom = self.tilemap.world_to_tile(self.dx, (self.y + self.height * 0.5) + 1)

        self.left_tile_top = self.tilemap.world_to_tile(self.x, (self.y + self.height * 0.5) - 1)
        self.left_tile_bottom = self.tilemap.world_to_tile(self.x, (self.y + self.height * 0.5) + 1)

        if self.tilemap.grid[int(self.below_tile_left.x)][int(self.below_tile_left.y)] != 0 and self.velocity.y >= 0:
            self.y = self.below_tile_left.y * TILE_SIZE - self.height
            self.velocity.y = 0
            self.is_on_ground = True
        elif self.tilemap.grid[int(self.below_tile_right.x)][int(self.below_tile_right.y)] != 0 and self.velocity.y >= 0:
            self.y = self.below_tile_right.y * TILE_SIZE - self.height
            self.velocity.y = 0
            self.is_on_ground = True

        if self.tilemap.grid[int(self.above_tile_left.x)][int(self.above_tile_left.y)] != 0 and self.velocity.y <= 0:
            self.y = (self.above_tile_left.y + 1) * TILE_SIZE
            self.velocity.y = 0
        elif self.tilemap.grid[int(self.above_tile_right.x)][int(self.above_tile_right.y)] != 0 and self.velocity.y <= 0:
            self.y = (self.above_tile_right.y + 1) * TILE_SIZE
            self.velocity.y = 0

        if self.tilemap.grid[int(self.right_tile_top.x)][int(self.right_tile_top.y)] != 0 and self.velocity.x >= 0:
            self.x = self.right_tile_top.x * TILE_SIZE - self.width
            self.velocity.x = 0
        elif self.tilemap.grid[int(self.right_tile_bottom.x)][int(self.right_tile_bottom.y)] != 0 and self.velocity.x >= 0:
            self.x = self.right_tile_bottom.x * TILE_SIZE - self.width
            self.velocity.x = 0

        if self.tilemap.grid[int(self.left_tile_top.x)][int(self.left_tile_top.y)] != 0 and self.velocity.x <= 0: 
            self.x = (self.left_tile_top.x + 1) * TILE_SIZE
            self.velocity.x = 0
        elif self.tilemap.grid[int(self.left_tile_bottom.x)][int(self.left_tile_bottom.y)] != 0 and self.velocity.x <= 0: 
            self.x = (self.left_tile_bottom.x + 1) * TILE_SIZE
            self.velocity.x = 0

        # Collision with world borders
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
        elif self.want_to_jump == False and self.velocity.y < 0:
            self.velocity.y *= 0.75

        self.rect.x = self.x
        self.rect.y = self.y