import pygame
import math
from sys import exit

from tilemap import TileMap
from player import Player
from camera import Camera

FPS_CAP = 60
VIEWPORT_RESOLUTION = (640, 360)
SCREEN_RESOLUTION = (1280, 720)
SCREEN_SCALE_FACTOR = (SCREEN_RESOLUTION[0] / VIEWPORT_RESOLUTION[0], SCREEN_RESOLUTION[1] / VIEWPORT_RESOLUTION[1])

TILE_SIZE = 8
TILEMAP_SIZE = (4200, 1200)

pygame.init()
pygame.display.set_caption(F'Tile Map {TILEMAP_SIZE[0]}x{TILEMAP_SIZE[1]}')
pygame.display.set_icon(pygame.image.load('content/icon.png'))

viewport = pygame.Surface(VIEWPORT_RESOLUTION)
screen = pygame.display.set_mode(SCREEN_RESOLUTION)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 64)

tilemap = TileMap(TILE_SIZE, TILEMAP_SIZE, VIEWPORT_RESOLUTION)
camera = Camera(0, 0, False, 0, 0, TILEMAP_SIZE[0] * TILE_SIZE, TILEMAP_SIZE[1] * TILE_SIZE, VIEWPORT_RESOLUTION)
player = Player(100, 100, 7, 15, tilemap)

def draw():
    viewport.fill((95,125,245))
    fps_text = font.render(f'{int(clock.get_fps())}', True, (255, 255, 0))

    last_tile_id = 0
    for x in tilemap.visible_x:
        for y in tilemap.visible_y:
            tile_id = tilemap.grid[x][y]
            if tile_id >= 1:
                if last_tile_id != tile_id:
                    last_tile_id = tile_id
                    block_image = tilemap.block_images[tile_id - 1]
                    block_image = pygame.transform.scale(block_image, (TILE_SIZE, TILE_SIZE))
                viewport.blit(block_image, pygame.Rect(x * TILE_SIZE - camera.x, y * TILE_SIZE - camera.y, TILE_SIZE, TILE_SIZE))

    pygame.draw.rect(viewport, (0,0,0), tilemap.cursor)
    pygame.draw.rect(viewport, (0,0,0), player.rect)

    scaled_viewport = pygame.transform.scale(viewport, screen.get_size())

    screen.blit(scaled_viewport, (0,0))
    screen.blit(fps_text, fps_text.get_rect(center=(45,40)))

def loop():
    mouse_position = pygame.math.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    mouse_position_tile = pygame.math.Vector2(math.floor((mouse_position.x / SCREEN_SCALE_FACTOR[0] + camera.x) / TILE_SIZE), math.floor((mouse_position.y / SCREEN_SCALE_FACTOR[1] + camera.y) / TILE_SIZE))
    mouse_pressed = pygame.mouse.get_pressed()
    mouse_in_window = mouse_position.x > 0 and mouse_position.x < SCREEN_RESOLUTION[0] and mouse_position.y > 0 and mouse_position.y < SCREEN_RESOLUTION[1]
    if mouse_in_window:
        if mouse_pressed[0]:
            tilemap.set_tile(int(mouse_position_tile.x), int(mouse_position_tile.y), 0)
        elif mouse_pressed[2]:
            tilemap.set_tile(int(mouse_position_tile.x), int(mouse_position_tile.y), 2)

    tilemap.cursor.x = (mouse_position_tile.x * TILE_SIZE - camera.x)
    tilemap.cursor.y = (mouse_position_tile.y * TILE_SIZE - camera.y)

    keys = pygame.key.get_pressed()
    player.update(keys)
    camera.update(player)
    tilemap.update(camera)

    draw()
    pygame.display.flip()
    delta = clock.tick(FPS_CAP) / 1000

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
    loop()