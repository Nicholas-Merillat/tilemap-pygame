from settings import *

class Camera():
    def __init__(self, x, y, smooth_position):
        self.x = x
        self.y = y
        self.dx = x + VIEWPORT_RESOLUTION[0]
        self.dy = y + VIEWPORT_RESOLUTION[1]
        self.smooth_position = smooth_position
        self.zoom = 0
        self.zoom_scale_factor = VIEWPORT_RESOLUTION[0] / (VIEWPORT_RESOLUTION[0] - self.zoom)

        self.smoothing_speed = 0.1
        self.limit_left = 0
        self.limit_top = 0
        self.limit_right = TILEMAP_SIZE[0] * TILE_SIZE
        self.limit_bottom = TILEMAP_SIZE[1] * TILE_SIZE

    def update(self, delta, entity, keys):
        if keys[pygame.K_EQUALS]:
            self.zoom += 4 * delta
        if keys[pygame.K_MINUS]:
            self.zoom -= 4 * delta
        if self.zoom < 0:
            self.zoom = 0
        elif self.zoom > 480:
            self.zoom = 480
        self.zoom_scale_factor = VIEWPORT_RESOLUTION[0] / (VIEWPORT_RESOLUTION[0] - self.zoom)

        if self.smooth_position:
            self.x = pygame.math.lerp(self.x, (entity.x + entity.width / 2) - VIEWPORT_RESOLUTION[0] / 2, self.smoothing_speed * delta)
            self.y = pygame.math.lerp(self.y, (entity.y + entity.height / 2) - VIEWPORT_RESOLUTION[1] / 2, self.smoothing_speed * delta)
        else:
            self.x = ((entity.x + entity.width / 2) - VIEWPORT_RESOLUTION[0] / 2) + self.zoom / 2
            self.y = ((entity.y + entity.height / 2) - VIEWPORT_RESOLUTION[1] / 2) + (self.zoom / 2) / ASPECT_SCALE_FACTOR
        self.dx = self.x + VIEWPORT_RESOLUTION[0]
        self.dy = self.y + VIEWPORT_RESOLUTION[1]

        if self.x < self.limit_left:
            self.x = self.limit_left
        if self.y < self.limit_top:
            self.y = self.limit_top
        if self.dx - self.zoom > self.limit_right:
            self.x = self.limit_right - VIEWPORT_RESOLUTION[0] + self.zoom
        if self.dy - self.zoom / ASPECT_SCALE_FACTOR > self.limit_bottom:
            self.y = self.limit_bottom - VIEWPORT_RESOLUTION[1] + self.zoom / ASPECT_SCALE_FACTOR

        entity.rect.x = entity.x - self.x
        entity.rect.y = entity.y - self.y