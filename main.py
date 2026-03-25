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
        self.screen = pygame.display.set_mode(SCREEN_RESOLUTION, pygame.DOUBLEBUF)
        self.screen_scale_factor = pygame.math.Vector2(self.screen.size[0] / VIEWPORT_RESOLUTION[0], self.screen.size[1] / VIEWPORT_RESOLUTION[1])

        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont('Monospace', int(24 * self.screen_scale_factor.x), True)

        self.camera = Camera(0, 0, True)

        self.tilemap = TileMap(self.camera)
        self.tilemap.generate_world()

        self.player = Player((TILEMAP_SIZE[0] * TILE_SIZE) / 2, 150, 7, 15, self.tilemap)

    def render(self):
        # Draw any pixel art on viewport to keep pixels
        self.viewport = pygame.Surface((VIEWPORT_RESOLUTION[0] - self.camera.zoom, VIEWPORT_RESOLUTION[1] - self.camera.zoom / ASPECT_SCALE_FACTOR))
        self.viewport.fill((165,215,240))

        # Blit only the whats visible to the camera from the tilemap to viewport
        self.viewport.blit(self.tilemap.texture_surface, (0,0))

        #if self.tilemap.grid[int(self.mouse_position_tile.x)][int(self.mouse_position_tile.y)] != 0:
        self.viewport.blit(self.tilemap.cursor, (self.mouse_position_tile.x * TILE_SIZE - self.camera.x, self.mouse_position_tile.y * TILE_SIZE - self.camera.y), special_flags=pygame.BLEND_ADD)

        pygame.draw.rect(self.viewport, (0,0,0), self.player.rect)

        # Scale viewport up and blit onto screen for pixel art effect + good performance
        pygame.transform.scale(self.viewport, self.screen.get_size(), self.screen)

        # Anything to be rendered at full res (UI, etc) should be put below and drawn onto screen instead of viewport
        fps_text = self.font_big.render(f'{int(self.clock.get_fps())}', True, (255, 255, 0))
        self.screen.blit(fps_text, fps_text.get_rect(center=(25 * self.screen_scale_factor.x, 15 * self.screen_scale_factor.y)))

    def run(self):
        self.delta = (self.clock.tick(MAX_FPS) / 1000) * PHYSICS_FPS
        while True:
            self.delta = (self.clock.tick(MAX_FPS) / 1000) * PHYSICS_FPS
            self.screen_scale_factor = pygame.math.Vector2(self.screen.size[0] / VIEWPORT_RESOLUTION[0], self.screen.size[1] / VIEWPORT_RESOLUTION[1])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            self.mouse_position = pygame.math.Vector2(pygame.mouse.get_pos())
            self.mouse_position_tile = self.tilemap.screen_to_tile((self.mouse_position.x / self.screen_scale_factor.x) / self.camera.zoom_scale_factor, (self.mouse_position.y / self.screen_scale_factor.y) / self.camera.zoom_scale_factor)
            self.mouse_pressed = pygame.mouse.get_pressed()

            if pygame.mouse.get_focused():
                if self.mouse_pressed[0]:
                    self.tilemap.set_tile(int(self.mouse_position_tile.x), int(self.mouse_position_tile.y), 0)
                elif self.mouse_pressed[2]:
                    self.tilemap.set_tile(int(self.mouse_position_tile.x), int(self.mouse_position_tile.y), 1)

            self.keys = pygame.key.get_pressed()
            self.player.update(self.delta, self.keys)
            self.camera.update(self.delta, self.keys, self.player)
            self.tilemap.update()
            
            self.render()
            pygame.display.flip()

if __name__ == '__main__':
    main = Main()
    main.run()