from settings import *

class TileSet():
    def __init__(self, name, image):
        self.name = name
        self.image = image

        self.size = (int(self.image.size[0] / TILE_SIZE), int(self.image.size[1] / TILE_SIZE))

        # Stores the tiles in a dictionary with an ID corresponding to a tile coordinate in the tileset
        self.index_dict = {}
        x = 0
        y = 0
        for i in range(self.size[0] * self.size[1]):
            x = i % self.size[0]
            self.index_dict.update({str(i):(x * TILE_SIZE, y * TILE_SIZE)})

            if (x + 1) / self.size[0] >= 1:
                y += 1

        print(self.index_dict)

    def get_tile_surface(self, tile_index):
        pass