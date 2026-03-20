import pygame, math, numpy

class TileMap():
    def __init__(self, tile_size, tilemap_size, viewport):
        self.tile_size = tile_size
        self.tilemap_size = tilemap_size
        self.viewport = viewport

        self.visible_tiles_x = math.ceil(self.viewport[0] / self.tile_size)
        self.visible_tiles_y = math.ceil(self.viewport[1] / self.tile_size)
        self.cursor = pygame.Rect(0, 0, self.tile_size, self.tile_size)
        self.camera = pygame.math.Vector2(0, 0)

        self.grid = numpy.full((self.tilemap_size[0], self.tilemap_size[1]), 0)
        for x in range(self.tilemap_size[0]):
            for y in range(self.tilemap_size[1]):
                if y == 40:
                    self.grid[x][y] = 1
                elif y > 40 and y <= 51:
                    self.grid[x][y] = 2
                elif y > 51:
                    self.grid[x][y] = 3

        with open('content/blocks.txt', 'r') as file:
            file_content = file.read()
            blocks = file_content.splitlines()
            self.block_images = []
            for block in blocks:
                if block != 'air':
                    image_path = f'content/sprites/{block}.png'
                    try:
                        image_surface = pygame.image.load(image_path).convert_alpha()
                        self.block_images.append(image_surface)
                    except pygame.error as e:
                        print(f'Error loading image {block}: {e}')
    def set_tile(self, tile_x, tile_y, tile_id):
        self.grid[tile_x][tile_y] = tile_id
    def tile_to_world(self, tile_x, tile_y):
        return pygame.math.Vector2(tile_x * self.tile_size + self.camera.x, tile_y * self.tile_size + self.camera.y)
    def screen_to_tile(self, x, y):
        tile_x = int(math.floor((x + self.camera.x) / self.tile_size))
        tile_y = int(math.floor((y + self.camera.y) / self.tile_size))
        return pygame.math.Vector2(tile_x, tile_y)
    def world_to_tile(self, x, y):
        tile_x = int(math.floor(x / self.tile_size))
        tile_y = int(math.floor(y / self.tile_size))
        tile_x = max(0, min(tile_x, self.tilemap_size[0] - 1))
        tile_y = max(0, min(tile_y, self.tilemap_size[1] - 1))
        return pygame.math.Vector2(tile_x, tile_y)
    def update(self, camera):
        self.camera = camera

        # range used to see which tiles to render on screen based on what camera can see
        camera_to_tile = self.screen_to_tile(self.camera.x % self.tile_size, self.camera.y % self.tile_size)
        self.visible_x = range(max(0, int(camera_to_tile.x) - 1), min(int(camera_to_tile.x + self.visible_tiles_x) + 1, self.tilemap_size[0]))
        self.visible_y = range(max(0, int(camera_to_tile.y) - 1), min(int(camera_to_tile.y + self.visible_tiles_y) + 1, self.tilemap_size[1]))