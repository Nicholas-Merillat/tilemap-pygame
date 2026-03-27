from settings import *

from tileset import TileSet

class TileMap():
    def __init__(self, camera):
        self.cursor = pygame.surface.Surface((TILE_SIZE, TILE_SIZE))
        self.cursor.fill((75,75,75))
        self.camera = camera

        self.tile_count = 0
        self.grid = numpy.full((TILEMAP_SIZE[0], TILEMAP_SIZE[1]), 0)
        self.light_grid = numpy.full((TILEMAP_SIZE[0], TILEMAP_SIZE[1]), 0)
        self.offsets = [(0, -1, 0), (-1, 0, 1), (1, 0, 2), (0, 1, 3)]

        self.surface = pygame.surface.Surface(VIEWPORT_RESOLUTION, pygame.SRCALPHA)
        self.rects = []

        # Load tilesets
        self.tilesets = []
        with open('content/blocks.txt', 'r') as file:
            file_content = file.read()
            tiles = file_content.splitlines()
            for tile in tiles:
                if tile != 'air':
                    image_path = f'content/sprites/{tile}-fast.png'
                    try:
                        surface = pygame.image.load(image_path)
                        surface = surface.convert_alpha()
                        self.tilesets.append(TileSet(tile, surface))
                    except pygame.error as e:
                        print(f'Error loading tileset {tile}: {e}')

    # Set tile ID at tile position
    def set_tile(self, tile_x, tile_y, tile_id):
        self.grid[tile_x][tile_y] = tile_id

    # Get tile ID at tile position
    def get_tile(self, tile_x, tile_y):
        return self.grid[tile_x][tile_y]

    # Get world coordinates of a tile with tile position
    def tile_to_world(self, tile_x, tile_y):
        return pygame.math.Vector2(tile_x * TILE_SIZE + self.camera.x, tile_y * TILE_SIZE + self.camera.y)
    
    # Convert screen coordinates to corresponding tile
    def screen_to_tile(self, x, y):
        tile_x = int(math.floor((x + self.camera.x) / TILE_SIZE))
        tile_y = int(math.floor((y + self.camera.y) / TILE_SIZE))
        return pygame.math.Vector2(tile_x, tile_y)
    
    # Convert world coordinates to corresponding tile
    def world_to_tile(self, x, y):
        tile_x = int(math.floor(x / TILE_SIZE))
        tile_y = int(math.floor(y / TILE_SIZE))
        tile_x = max(0, min(tile_x, TILEMAP_SIZE[0] - 1))
        tile_y = max(0, min(tile_y, TILEMAP_SIZE[1] - 1))
        return pygame.math.Vector2(tile_x, tile_y)
    
    def generate_world(self):
        # Generate surface grass with a sin function then fill below 10 layers with dirt, rest stone
        for x in range(TILEMAP_SIZE[0]):
            y = int(math.sin(x / 20) * 4) + 40
            self.set_tile(x, y, 1)
            self.set_tile(x, range(y + 1, y + 9), 2)
            self.set_tile(x, range(y + 9, TILEMAP_SIZE[1]), 3)
    
    def update(self, lighting):
        # Sky
        self.surface.fill((165,215,240))

        self.tile_count = 0
        self.tile_surfaces = []

        # Range used to see which tiles to render on screen based on what the camera can see
        self.camera_to_tile = self.screen_to_tile(self.camera.x % TILE_SIZE, self.camera.y % TILE_SIZE)
        self.visible_tiles_x = math.ceil((VIEWPORT_RESOLUTION[0] - self.camera.zoom) / TILE_SIZE)
        self.visible_tiles_y = math.ceil((VIEWPORT_RESOLUTION[1] - (self.camera.zoom / ASPECT_SCALE_FACTOR)) / TILE_SIZE)
        self.visible_x = range(max(0, int(self.camera_to_tile.x) - 1), min(int(self.camera_to_tile.x + self.visible_tiles_x) + 1, TILEMAP_SIZE[0]))
        self.visible_y = range(max(0, int(self.camera_to_tile.y) - 1), min(int(self.camera_to_tile.y + self.visible_tiles_y) + 1, TILEMAP_SIZE[1]))

        # Iterating column major is apparently more memory efficient
        for y in self.visible_y:
            for x in self.visible_x:
                tile_id = self.grid[x][y] # Accessing directly instead of using get_tile() is marginally faster
                if tile_id >= 1:
                    self.tile_count += 1
                    self.light_grid[x][y] = max(0, self.light_grid[x][y-1] - 1)

                    # Bit masking for auto tiling
                    bitmask = 0
                    for bit in self.offsets:
                        nx, ny = x + bit[0], y + bit[1]
                        if 0 <= nx < TILEMAP_SIZE[0] and 0 <= ny < TILEMAP_SIZE[1]:
                            if self.grid[nx][ny] == tile_id:
                                bitmask |= (1 << bit[2])
                    
                    tile = (self.tilesets[tile_id - 1].get_tile_surface(bitmask))
                    if lighting:
                        black = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                        if self.light_grid[x][y] != 0:
                            black.fill((0,0,0, self.light_grid[x][y] * -36 % 255))
                            self.tile_surfaces.append((tile, (math.floor((x * TILE_SIZE) - self.camera.x), math.floor((y * TILE_SIZE)  - self.camera.y), TILE_SIZE, TILE_SIZE)))
                            self.tile_surfaces.append((black, (math.floor((x * TILE_SIZE) - self.camera.x), math.floor((y * TILE_SIZE)  - self.camera.y), TILE_SIZE, TILE_SIZE)))
                        else:
                            black.fill((0,0,0, 255))
                            self.tile_surfaces.append((black, (math.floor((x * TILE_SIZE) - self.camera.x), math.floor((y * TILE_SIZE)  - self.camera.y), TILE_SIZE, TILE_SIZE)))
                    else:
                        self.tile_surfaces.append((tile, (math.floor((x * TILE_SIZE) - self.camera.x), math.floor((y * TILE_SIZE)  - self.camera.y), TILE_SIZE, TILE_SIZE)))
                else:
                    self.light_grid[x][y] = 8

        self.rects = self.surface.blits(self.tile_surfaces, True)