import pygame
import gfx
from gfx import CELL_SIZE_PIXELS, GRID_OPACITY, COLORS, FG_COLOR, GRID_ROWS_HIDDEN
from config import SCREEN_RESOLUTION, ORIGIN

class Grid:
    def __init__(self, width, height, lines_opacity=GRID_OPACITY):
        self.width = width
        self.height = height
        self.cells = None
        SURFACE_RESOLUTION = CELL_SIZE_PIXELS * self.width, CELL_SIZE_PIXELS * self.height
        self.surface = pygame.Surface(SURFACE_RESOLUTION)
        self.overlay = pygame.Surface(SURFACE_RESOLUTION, pygame.SRCALPHA)
        self.lines_opacity = lines_opacity
        self.init_gridlines()
        self.clear_cells()
        self.lines_made = 0

    def init_gridlines(self, grid_size=CELL_SIZE_PIXELS, color=FG_COLOR, opacity=GRID_OPACITY):
        'Draws a translucent grid onto a surface'
        opacity = (opacity, )
        # Draw the grid lines on the grid surface
        for y in range(0, self.height * grid_size + grid_size, grid_size):
            if y != 0:
                y -= 1
            pygame.draw.line(self.overlay, color + opacity, (0, y), (self.width * grid_size, y), 1)
        for x in range(0, self.width * grid_size + grid_size, grid_size):
            if x != 0:
                x -= 1
            pygame.draw.line(self.overlay, color + opacity, (x, 0), (x, self.height * grid_size), 1)

    def set_cell(self, x, y, color):
        'Sets grid value to a color (non-zero)'
        self.cells[y][x] = color

    def clear_cells(self):
        'Clears all grid elements to zero'
        self.cells = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def clear_full_lines(self):
        l = self.cells
        # Create a new list to store the rows we want to keep
        new_l = [row for row in l if 0 in row]
        # Calculate the number of full rows that were removed
        num_full_rows = len(l) - len(new_l)
        self.lines_made += num_full_rows

        # Add the same number of empty rows at the top
        for _ in range(num_full_rows):
            new_l.insert(0, [0]*len(l[0]))
        self.cells = new_l

    def draw_cells(self):
        'Draw all the cells in the grid'
        y = 0
        for line in self.cells:
            x = 0
            for color in line:
                self.fill_cell(x, y, color)
                x += 1
            y += 1

    def fill_cell(self, x, y, color):
        'Draw a filled block on the surface'
        pygame.draw.rect(self.surface,
                         COLORS[color] + (255, ),
                         pygame.Rect(x*CELL_SIZE_PIXELS, (y+GRID_ROWS_HIDDEN)*CELL_SIZE_PIXELS, CELL_SIZE_PIXELS, CELL_SIZE_PIXELS))

    def outline_cell(self, x, y, color):
        'Draw an unfilled block on the surface'
        pygame.draw.rect(self.surface,
                         COLORS[color] + (255, ),
                         pygame.Rect(x*CELL_SIZE_PIXELS, (y+GRID_ROWS_HIDDEN)*CELL_SIZE_PIXELS, CELL_SIZE_PIXELS, CELL_SIZE_PIXELS), 1)

    @property
    def centre(self):
        return int(self.width/2), int(self.height/2)

    def draw_gridlines(self):
        self.surface.blit(self.overlay, ORIGIN)

    def update_gfx(self):
        self.draw_cells()
        self.draw_gridlines()
