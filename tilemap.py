from settings import *

class TileMap():
    def __init__(self, camera):
        self.cursor = pygame.surface.Surface((TILE_SIZE, TILE_SIZE))
        self.cursor.fill((75,75,75))
        self.camera = camera

        self.grid = numpy.full((TILEMAP_SIZE[0], TILEMAP_SIZE[1]), numpy.uint16(0))
        self.bitmask_grid = numpy.full((TILEMAP_SIZE[0], TILEMAP_SIZE[1]), numpy.uint8(0))
        self.bitmask_dict = {0:(0,0), 1:(0,8), 2:(0,16), 3:(0,24), 4:(8,0), 5:(8,8), 6:(8,16), 7:(8,24), 8:(16,0), 9:(16,8), 10:(16,16), 11:(16,24), 12:(24,0), 13:(24,8), 14:(24,16), 15:(24,24)}

        with open('content/blocks.txt', 'r') as file:
            file_content = file.read()
            blocks = file_content.splitlines()
            self.tile_images = []
            for block in blocks:
                if block != 'air':
                    image_path = f'content/sprites/{block}.png'
                    try:
                        image_surface = pygame.image.load(image_path).convert_alpha()
                        self.tile_images.append(image_surface)
                    except pygame.error as e:
                        print(f'Error loading image {block}: {e}')

        self.update()

    # Set tile ID at tile position
    def set_tile(self, tile_x, tile_y, tile_id):
        self.grid[tile_x][tile_y] = tile_id
        self.texture()

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
            y = int(math.sin(x / 14) * 4) + 40
            self.grid[x][y] = 1
            self.grid[x][range(y + 1, y + 9)] = 2
            self.grid[x][range(y + 9, TILEMAP_SIZE[1])] = 3
        self.texture()

    def bitmask(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                tile_id = self.grid[x][y]
                if tile_id >= 1:
                    bitmask_counter = numpy.uint8(0)

                    # In a try catch because edge tiles obv cant index past the edges so I just brute force it, this is why world border tiles autotile weird
                    try:
                        if self.grid[x][y-1] == tile_id: # North
                            bitmask_counter += 2**0
                        if self.grid[x-1][y] == tile_id: # West
                            bitmask_counter += 2**1
                        if self.grid[x+1][y] == tile_id: # East
                            bitmask_counter += 2**2
                        if self.grid[x][y+1] == tile_id: # South
                            bitmask_counter += 2**3
                    except:
                        pass

                    self.bitmask_grid[x][y] = bitmask_counter

    def texture(self):
        self.bitmask()
        self.texture_surface = pygame.surface.Surface((TILEMAP_SIZE[0] * TILE_SIZE, TILEMAP_SIZE[1] * TILE_SIZE), pygame.SRCALPHA)

        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                tile_id = self.grid[x][y]
                if tile_id >= 1:
                    tile_image = self.tile_images[tile_id - 1]

                    block_rect = pygame.Rect(self.bitmask_dict[self.bitmask_grid[x][y]][1], self.bitmask_dict[self.bitmask_grid[x][y]][0], TILE_SIZE, TILE_SIZE)
                    block_image = tile_image.subsurface(block_rect)
                    block_image = pygame.transform.scale(block_image, (TILE_SIZE, TILE_SIZE))
                    self.texture_surface.blit(block_image, pygame.Rect(math.floor(x * TILE_SIZE), math.floor(y * TILE_SIZE), TILE_SIZE, TILE_SIZE))

    def update_texture(self, x, y):
        pass
    
    def update(self):
        pass
        # Range used to see which tiles to render on screen based on what the camera can see
        # self.camera_to_tile = self.screen_to_tile(self.camera.x % TILE_SIZE, self.camera.y % TILE_SIZE)
        # self.visible_tiles_x = math.ceil((VIEWPORT_RESOLUTION[0] - self.camera.zoom) / TILE_SIZE)
        # self.visible_tiles_y = math.ceil((VIEWPORT_RESOLUTION[1] - (self.camera.zoom / ASPECT_SCALE_FACTOR)) / TILE_SIZE)
        # self.visible_x = range(max(0, int(self.camera_to_tile.x) - 1), min(int(self.camera_to_tile.x + self.visible_tiles_x) + 1, TILEMAP_SIZE[0]))
        # self.visible_y = range(max(0, int(self.camera_to_tile.y) - 1), min(int(self.camera_to_tile.y + self.visible_tiles_y) + 1, TILEMAP_SIZE[1]))