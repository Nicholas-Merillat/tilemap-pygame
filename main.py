import pygame, math, sys
from settings import *
from tilemap import TileMap
from player import Player
from camera import Camera

class Main():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(F'Tile Map {TILEMAP_SIZE[0]}x{TILEMAP_SIZE[1]}')
        pygame.display.set_icon(pygame.image.load('content/icon.png'))

        self.viewport = pygame.Surface(VIEWPORT_RESOLUTION)
        self.screen = pygame.display.set_mode(SCREEN_RESOLUTION)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Monospace', int(24 * SCREEN_SCALE_FACTOR), True)

        self.tilemap = TileMap()
        self.camera = Camera(0, 0, True)
        self.player = Player(100, 100, 7, 15, self.tilemap)

    def render(self):
        self.viewport.fill((95,125,245))
        fps_text = self.font.render(f'{int(self.clock.get_fps())}', True, (255, 255, 0))

        for x in self.tilemap.visible_x:
            for y in self.tilemap.visible_y:
                tile_id = self.tilemap.grid[x][y]
                if tile_id >= 1:
                    block_image = self.tilemap.block_images[tile_id - 1]
                    block_image = pygame.transform.scale(block_image, (TILE_SIZE, TILE_SIZE))
                    self.viewport.blit(block_image, pygame.Rect(x * TILE_SIZE - self.camera.x, y * TILE_SIZE - self.camera.y, TILE_SIZE, TILE_SIZE))

        pygame.draw.rect(self.viewport, (0,0,0), self.tilemap.cursor)
        pygame.draw.rect(self.viewport, (0,0,0), self.player.rect)

        scaled_viewport = pygame.transform.scale(self.viewport, self.screen.get_size())

        self.screen.blit(scaled_viewport, (0,0))
        self.screen.blit(fps_text, fps_text.get_rect(center=(25 * SCREEN_SCALE_FACTOR, 15 * SCREEN_SCALE_FACTOR)))
    
    def run(self):
        while True:
            if MAX_FPS > 0: self.delta = (self.clock.tick(MAX_FPS) / 1000) * PHYSICS_FPS
            else: self.delta = (self.clock.tick() / 1000) * PHYSICS_FPS
            if self.delta > PHYSICS_FPS / MIN_FPS: self.delta = PHYSICS_FPS / MIN_FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.mouse_position = pygame.math.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            self.mouse_position_tile = pygame.math.Vector2(math.floor((self.mouse_position.x / SCREEN_SCALE_FACTOR + self.camera.x) / TILE_SIZE), math.floor((self.mouse_position.y / SCREEN_SCALE_FACTOR + self.camera.y) / TILE_SIZE))
            self.mouse_pressed = pygame.mouse.get_pressed()
            self.mouse_in_window = self.mouse_position.x > 0 and self.mouse_position.x < SCREEN_RESOLUTION[0] and self.mouse_position.y > 0 and self.mouse_position.y < SCREEN_RESOLUTION[1]
            if self.mouse_in_window:
                if self.mouse_pressed[0]:
                    self.tilemap.set_tile(int(self.mouse_position_tile.x), int(self.mouse_position_tile.y), 0)
                elif self.mouse_pressed[2]:
                    self.tilemap.set_tile(int(self.mouse_position_tile.x), int(self.mouse_position_tile.y), 2)

            self.tilemap.cursor.x = (self.mouse_position_tile.x * TILE_SIZE - self.camera.x)
            self.tilemap.cursor.y = (self.mouse_position_tile.y * TILE_SIZE - self.camera.y)

            self.keys = pygame.key.get_pressed()
            self.player.update(self.delta, self.keys)
            self.camera.update(self.delta, self.player)
            self.tilemap.update(self.camera)

            self.render()
            pygame.display.flip()

if __name__ == '__main__':
    main = Main()
    main.run()