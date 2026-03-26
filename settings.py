import pygame, math, numpy, sys, ctypes, tkinter

# User settings
WINDOW_RESOLUTION = (1280, 720)
MAX_FPS = 0 # If 0, framerate is uncapped

# ENGINE SETTINGS BELOW DO NOT EDIT!

# Game settings
VIEWPORT_RESOLUTION = (640, 360) # 960, 540
ASPECT_SCALE_FACTOR = VIEWPORT_RESOLUTION[0] / VIEWPORT_RESOLUTION[1]
PHYSICS_FPS = 60

# Tilemap settings
TILE_SIZE = 8
TILEMAP_SIZE = (8400, 2400) # (8400, 2400) (4200, 1200)

def easeInQuad(t):
    return t * t

def easeOutQuad(t):
    return -t * (t - 2)