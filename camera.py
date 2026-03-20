import pygame

class Camera():
    def __init__(self, x, y, smooth_position, limit_left, limit_top, limit_right, limit_bottom, viewport):
        self.x = x
        self.y = y
        self.smooth_position = smooth_position
        self.limit_left = limit_left
        self.limit_top = limit_top
        self.limit_right = limit_right
        self.limit_bottom = limit_bottom
        self.viewport = viewport

        self.dx = x + self.viewport[0]
        self.dy = y + self.viewport[1]

    def update(self, delta, entity):
        if self.smooth_position:
            self.x = pygame.math.lerp(self.x, (entity.x + entity.width / 2) - self.viewport[0] / 2, 0.1 * delta)
            self.y = pygame.math.lerp(self.y, (entity.y + entity.height / 2) - self.viewport[1] / 2, 0.1 * delta)
        else:
            self.x = (entity.x + entity.width / 2) - self.viewport[0] / 2
            self.y = (entity.y + entity.height / 2) - self.viewport[1] / 2
        self.dx = self.x + self.viewport[0]
        self.dy = self.y + self.viewport[1]

        if self.x < self.limit_left:
            self.x = self.limit_left
        if self.y < self.limit_top:
            self.y = self.limit_top
        if self.dx > self.limit_right:
            self.x = self.limit_right - self.viewport[0]
        if self.dy > self.limit_bottom:
            self.y = self.limit_bottom - self.viewport[1]

        entity.rect.x = entity.x - self.x
        entity.rect.y = entity.y - self.y