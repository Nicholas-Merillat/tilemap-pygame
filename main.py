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
        self.screen = pygame.display.set_mode(SCREEN_RESOLUTION, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont('Monospace', int(24 * SCREEN_SCALE_FACTOR), True)

        self.tilemap = TileMap()
        self.tilemap.generate_world()

        self.camera = Camera(0, 0, False)
        self.player = Player(0, 0, 7, 15, self.tilemap)

        self.delta = (self.clock.tick(MAX_FPS) / 1000) * PHYSICS_FPS

    def render(self):
        # Draw any pixel art on viewport to keep pixels
        self.viewport = pygame.Surface((VIEWPORT_RESOLUTION[0] - self.camera.zoom, VIEWPORT_RESOLUTION[1] - self.camera.zoom / ASPECT_SCALE_FACTOR))
        self.viewport.fill((95,125,245))

        # Iterates through the visible tiles on camera in the tilemap and draws the tile images
        for x in self.tilemap.visible_x:
            for y in self.tilemap.visible_y:
                tile_id = self.tilemap.grid[x][y]
                if tile_id >= 1:
                    block_image = self.tilemap.block_images[tile_id - 1]
                    block_image = pygame.transform.scale(block_image, (TILE_SIZE, TILE_SIZE))
                    self.viewport.blit(block_image, pygame.Rect(math.floor(x * TILE_SIZE - self.camera.x), math.floor(y * TILE_SIZE - self.camera.y), TILE_SIZE, TILE_SIZE))

        pygame.draw.rect(self.viewport, (0,0,0), self.tilemap.cursor)
        pygame.draw.rect(self.viewport, (0,0,0), self.player.rect)

        # Scale viewport up and blit onto screen for pixel art effect + good performance
        pygame.transform.scale(self.viewport, self.screen.get_size(), self.screen)

        # Anything to be rendered at full res (UI, etc) should be put below and drawn onto screen instead of viewport
        fps_text = self.font_big.render(f'{int(self.clock.get_fps())}', True, (255, 255, 0))
        self.screen.blit(fps_text, fps_text.get_rect(center=(25 * SCREEN_SCALE_FACTOR, 15 * SCREEN_SCALE_FACTOR)))
    
    def run(self):
        while True:
            self.delta = (self.clock.tick(MAX_FPS) / 1000) * PHYSICS_FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.mouse_position = pygame.math.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            self.mouse_position_tile = self.tilemap.screen_to_tile((self.mouse_position.x / SCREEN_SCALE_FACTOR) / self.camera.zoom_scale_factor, (self.mouse_position.y / SCREEN_SCALE_FACTOR) / self.camera.zoom_scale_factor)
            self.mouse_pressed = pygame.mouse.get_pressed()
            self.mouse_in_window = self.mouse_position.x > 0 and self.mouse_position.x < self.screen.get_size()[0] and self.mouse_position.y > 0 and self.mouse_position.y < self.screen.get_size()[1]
            if self.mouse_in_window:
                if self.mouse_pressed[0]:
                    self.tilemap.set_tile(int(self.mouse_position_tile.x), int(self.mouse_position_tile.y), 0)
                elif self.mouse_pressed[2]:
                    self.tilemap.set_tile(int(self.mouse_position_tile.x), int(self.mouse_position_tile.y), 2)

            self.tilemap.cursor.x = (self.mouse_position_tile.x * TILE_SIZE - self.camera.x)
            self.tilemap.cursor.y = (self.mouse_position_tile.y * TILE_SIZE - self.camera.y)

            self.keys = pygame.key.get_pressed()
            self.player.update(self.delta, self.keys)
            self.camera.update(self.delta, self.player, self.keys)
            self.tilemap.update(self.camera)

            self.render()
            pygame.display.flip()

if __name__ == '__main__':
    main = Main()
    main.run()