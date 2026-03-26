from settings import *

from tilemap import TileMap
from player import Player
from camera import Camera

# Have to call this or else fetching monitor resolution doesn't work
ctypes.windll.user32.SetProcessDPIAware()

class Main():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(F'Tile Map {TILEMAP_SIZE[0]}x{TILEMAP_SIZE[1]}')
        pygame.display.set_icon(pygame.image.load('content/icon.png'))
        self.display_resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h)

        self.viewport = pygame.Surface(VIEWPORT_RESOLUTION)
        self.screen = pygame.display.set_mode(WINDOW_RESOLUTION)
        self.screen_scale_factor = pygame.math.Vector2(self.screen.size[0] / VIEWPORT_RESOLUTION[0], self.screen.size[1] / VIEWPORT_RESOLUTION[1])
        self.fullscreen = False

        self.clock = pygame.time.Clock()
        
        self.font_big = pygame.font.Font('content/bolds-pixels.ttf', int(24 * self.screen_scale_factor.x))
        self.font_medium = pygame.font.Font('content/bolds-pixels.ttf', int(16 * self.screen_scale_factor.x))
        self.font_small = pygame.font.Font('content/bolds-pixels.ttf', int(12 * self.screen_scale_factor.x))
        self.debug_text_color = (255,255,255)

        self.camera = Camera(0, 0, True)

        self.tilemap = TileMap(self.camera)
        self.tilemap.generate_world()
        self.lighting = False

        self.player = Player(0, 200, 7, 15, self.tilemap)

    def render(self):
        # Draw any pixel art on viewport to keep pixels
        self.viewport = pygame.Surface((VIEWPORT_RESOLUTION[0] - self.camera.zoom, VIEWPORT_RESOLUTION[1] - self.camera.zoom / ASPECT_SCALE_FACTOR))

        # Blit only the whats visible from the camera and tilemap to viewport
        self.viewport.blit(self.tilemap.surface, (0,0))
        if self.lighting:
            for rect in self.tilemap.rects:
                pygame.draw.rect(self.viewport, (0,0,0), (rect.left, rect.top, rect.width, rect.height))

        # Tilemap highlight on cursor
        self.viewport.blit(self.tilemap.cursor, (self.mouse_position_tile.x * TILE_SIZE - self.camera.x, self.mouse_position_tile.y * TILE_SIZE - self.camera.y), special_flags=pygame.BLEND_ADD)

        # Player
        pygame.draw.rect(self.viewport, (0,0,0), self.player.rect)

        # Scale viewport up and blit onto screen for pixel art effect + good performance
        pygame.transform.scale(self.viewport, self.screen.get_size(), self.screen)

        # Anything to be rendered at full res (UI, etc) should be put below and drawn onto screen instead of viewport
        fps_text = self.font_big.render(f'{int(self.clock.get_fps())}', True, self.debug_text_color)
        lighting_text = self.font_small.render(f'lighting: {self.lighting}', True, self.debug_text_color)
        player_pos_text = self.font_small.render(f'player pos: {int(self.player.x)}, {int(self.player.y)}', True, self.debug_text_color)
        camera_pos_text = self.font_small.render(f'camera pos: {int(self.camera.x)}, {int(self.camera.y)}', True, self.debug_text_color)
        visible_tiles_text = self.font_small.render(f'visible tiles: {self.tilemap.tile_count}', True, self.debug_text_color)
        self.screen.blit(fps_text, fps_text.get_rect(topleft=(25 * self.screen_scale_factor.x, 15 * self.screen_scale_factor.y)))
        self.screen.blit(player_pos_text, player_pos_text.get_rect(topleft=(25 * self.screen_scale_factor.x, 40 * self.screen_scale_factor.y)))
        self.screen.blit(camera_pos_text, camera_pos_text.get_rect(topleft=(25 * self.screen_scale_factor.x, 50 * self.screen_scale_factor.y)))
        self.screen.blit(visible_tiles_text, visible_tiles_text.get_rect(topleft=(25 * self.screen_scale_factor.x, 60 * self.screen_scale_factor.y)))
        self.screen.blit(lighting_text, lighting_text.get_rect(topleft=(25 * self.screen_scale_factor.x, 70 * self.screen_scale_factor.y)))

    def refresh(self):
        self.screen_scale_factor = pygame.math.Vector2(self.screen.size[0] / VIEWPORT_RESOLUTION[0], self.screen.size[1] / VIEWPORT_RESOLUTION[1])
        self.font_big = pygame.font.Font('content/bolds-pixels.ttf', int(24 * self.screen_scale_factor.x))
        self.font_medium = pygame.font.Font('content/bolds-pixels.ttf', int(16 * self.screen_scale_factor.x))
        self.font_small = pygame.font.Font('content/bolds-pixels.ttf', int(12 * self.screen_scale_factor.x))

    def run(self):
        self.delta = (self.clock.tick(MAX_FPS) / 1000) * PHYSICS_FPS
        while True:
            self.delta = (self.clock.tick(MAX_FPS) / 1000) * PHYSICS_FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LALT:
                        if self.fullscreen:
                            self.fullscreen = False
                            self.screen = pygame.display.set_mode(WINDOW_RESOLUTION)
                        else:
                            self.fullscreen = True
                            self.screen = pygame.display.set_mode(self.display_resolution, pygame.FULLSCREEN)

                        self.refresh()
                    elif event.key == pygame.K_LSHIFT:
                        self.lighting = not self.lighting

            self.mouse_position = pygame.math.Vector2(pygame.mouse.get_pos())
            self.mouse_position_tile = self.tilemap.screen_to_tile((self.mouse_position.x / self.screen_scale_factor.x) / self.camera.zoom_scale_factor, (self.mouse_position.y / self.screen_scale_factor.y) / self.camera.zoom_scale_factor)
            self.mouse_pressed = pygame.mouse.get_pressed()

            if self.mouse_pressed[0]:
                self.tilemap.set_tile(int(self.mouse_position_tile.x), int(self.mouse_position_tile.y), 0)
            elif self.mouse_pressed[2]:
                self.tilemap.set_tile(int(self.mouse_position_tile.x), int(self.mouse_position_tile.y), 3)

            self.keys = pygame.key.get_pressed()
            self.player.update(self.delta, self.keys)
            self.camera.update(self.delta, self.keys, self.player)
            self.tilemap.update()
            
            self.render()
            pygame.display.update()

if __name__ == '__main__':
    main = Main()
    main.run()