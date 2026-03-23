from settings import *

class TileMap():
    def __init__(self):
        self.cursor = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
        self.camera = pygame.math.Vector2(0, 0)

        self.grid = numpy.full((TILEMAP_SIZE[0], TILEMAP_SIZE[1]), 0)

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

    def get_tile(self, tile_x, tile_y):
        return self.grid[tile_x][tile_y]

    def tile_to_world(self, tile_x, tile_y):
        return pygame.math.Vector2(tile_x * TILE_SIZE + self.camera.x, tile_y * TILE_SIZE + self.camera.y)
    
    def screen_to_tile(self, x, y):
        tile_x = int(math.floor((x + self.camera.x) / TILE_SIZE))
        tile_y = int(math.floor((y + self.camera.y) / TILE_SIZE))
        return pygame.math.Vector2(tile_x, tile_y)
    
    def world_to_tile(self, x, y):
        tile_x = int(math.floor(x / TILE_SIZE))
        tile_y = int(math.floor(y / TILE_SIZE))
        tile_x = max(0, min(tile_x, TILEMAP_SIZE[0] - 1))
        tile_y = max(0, min(tile_y, TILEMAP_SIZE[1] - 1))
        return pygame.math.Vector2(tile_x, tile_y)
    
    def generate_world(self):
        # Generate surface grass and then fill below with dirt
        for x in range(TILEMAP_SIZE[0]):
            y = int(math.sin(x / 14) * 4) + 40
            self.grid[x][y] = 1
            self.grid[x][range(y + 1, y + 9)] = 2
            self.grid[x][range(y + 9, TILEMAP_SIZE[1])] = 3
    
    def update(self, camera):
        self.camera = camera

        # Range used to see which tiles to render on screen based on what the camera can see
        self.camera_to_tile = self.screen_to_tile(self.camera.x % TILE_SIZE, self.camera.y % TILE_SIZE)
        self.visible_tiles_x = math.ceil((VIEWPORT_RESOLUTION[0] - self.camera.zoom) / TILE_SIZE)
        self.visible_tiles_y = math.ceil((VIEWPORT_RESOLUTION[1] - (self.camera.zoom / ASPECT_SCALE_FACTOR)) / TILE_SIZE)
        self.visible_x = range(max(0, int(self.camera_to_tile.x) - 1), min(int(self.camera_to_tile.x + self.visible_tiles_x) + 1, TILEMAP_SIZE[0]))
        self.visible_y = range(max(0, int(self.camera_to_tile.y) - 1), min(int(self.camera_to_tile.y + self.visible_tiles_y) + 1, TILEMAP_SIZE[1]))

    def calculate_lighting(self) -> pygame.Surface:
        lightmap = numpy.full((len(self.visible_x), len(self.visible_y), 3), numpy.uint8(150))

        for x in self.visible_x:
            for y in self.visible_y:
                if self.grid[x][y] == 0:
                    lightmap[int(x - self.camera_to_tile.x)][int(y - self.camera_to_tile.y)] = (255,255,255)

        lightmap_surface = pygame.surfarray.make_surface(lightmap)
        return lightmap_surface