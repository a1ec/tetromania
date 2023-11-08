from copy import copy
import random
import pygame
from shape import Shape, Tetrominoes, color_to_index
from gfx import Color, fill_cell, GRID_ROWS_HIDDEN
from event import Event

def is_copy_cells_ok(src, dest, x_offset, y_offset):
    # Get the dimensions of the source and destination grids
    src_height, src_width = len(src), len(src[0])
    dest_height, dest_width = len(dest), len(dest[0])

    # Check if the source grid fits within the destination grid with the given offsets
    if x_offset < 0: 
        #print("x_offset < 0")
        return False

    if x_offset + src_width > dest_width:
        #print("x_offset + src_width > dest_width")
        return False

    if y_offset < 0:
        #print("y_offset < 0")
        return False
    
    if y_offset + src_height > dest_height:
        #print("y_offset + src_height > dest_height")
        return False

    # Check if any non-zero part of the source grid would write over a non-zero part of the destination grid
    for i in range(src_height):
        for j in range(src_width):
            if src[i][j] != 0 and dest[i + y_offset][j + x_offset] != 0:
                #print(f"Overlap: at x, y: {j + x_offset}, {i + y_offset}")
                return False
    return True


class Position:
    def __init(self, x, y, rotation_index):
        self.x = None
        self.y = None
        self.rotation_index = None

class Piece:
    def __init__(self, grid):
        self.shapes = None
        self.shape = None
        self.next_shape = None
        self.grid = grid
        self.count = 0

        self.new_x = 0
        self.new_y = 0
        self._new_rotation_index = 0
        self.new_cells = None

        self._rotation_index = 0
        self.get_next_shape()
        self.x = self.grid.centre[0] - int(self.width / 2)
        self.y = 0

    def refill_shapes(self):
        if not self.shapes:
            self.shapes = copy(Tetrominoes)
            random.shuffle(self.shapes)

    def get_next_shape(self):
        if self.next_shape:
            self.shape = self.next_shape
            self.refill_shapes()
            self.next_shape = self.shapes.pop() 
        else: # first time loading
            self.refill_shapes()
            self.shape = self.shapes.pop()
            self.refill_shapes()
            self.next_shape = self.shapes.pop()

        self.cell_value = color_to_index[self.shape.color]
        self.count += 1

    @property
    def cells(self):
        return self.shape.rotations[self._rotation_index]

    @property
    def height(self):
        return len(self.cells)

    @property
    def width(self):
        return len(self.cells[0])

    def place(self, x, y):
        self.x = x
        self.y = y

    def gameover(self):
        pygame.event.post(Event.game_over)

    def spawn_new(self):
        'New piece at top'
        self.get_next_shape()
        self.place(self.grid.centre[0] - int(self.width/2), GRID_ROWS_HIDDEN)
        if not is_copy_cells_ok(self.new_cells, self.grid.cells, self.new_x, self.new_y):
            self.gameover()

    def update_position(self, dx=0, dy=0, drotate=0):
        self.new_x = self.x + dx
        self.new_y = self.y + dy
        self._new_rotation_index = self.get_safe_rotation_index(self._rotation_index + drotate)
        self.new_cells = self.shape.rotations[self._new_rotation_index]
        if is_copy_cells_ok(self.new_cells, self.grid.cells, self.new_x, self.new_y):
            # within grid bounds and no overlapping blocks 👍
            self.new_position_to_current()
        elif dy != 0 and dx == 0:
            # maybe can be gamed but good enough
            self.set_on_grid()

    def new_position_to_current(self):
        self.x = self.new_x
        self.y = self.new_y
        self._rotation_index = self._new_rotation_index

    def __repr__(self):
        return f'{self.type}Piece'

    def debug(self):
        print(f'Printing shape: {self.type}')
        self.print_rotations()

    def print_rotations(self):
        for shape in self.shape.rotations:
            print(list2D_to_text(shape),'\n')

    def set_on_grid(self):
        if is_copy_cells_ok(self.new_cells, self.grid.cells, self.new_x, self.new_y):
            # Plot the values onto the grid_cells
            for row in range(self.height):
                for col in range(self.width):
                    if self.cells[row][col] != 0:
                        y = self.x + row
                        x = self.y + col
                        self.grid.cells[y][x] = self.cell_value
            self.spawn_new()

    def set_on_grid(self):
        # Write the source grid onto the destination grid
        for i in range(self.height):
            for j in range(self.width):
                if self.cells[i][j] != 0:
                    self.grid.cells[i + self.y][j + self.x] = self.cell_value
        self.spawn_new()
        self.grid.clear_full_lines()

    def draw_to_surface(self, surface, x_offset=0, y_offset=0, shape_cells=None, color=None, x=None, y=None):
        'Draws the shape to screen only, for play or next'
        # Use instance variables if no argument is provided
        if shape_cells is None:
            shape_cells = self.cells
        if color is None:
            color = self.cell_value
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        for row in range(len(shape_cells)):
            for col in range(len(shape_cells[row])):
                if shape_cells[row][col] != 0:
                    fill_cell(x + col, y + row, color, surface, x_offset, y_offset)

    def draw_next(self, surface, x_offset, y_offset):
        color = color_to_index[self.next_shape.color]
        self.draw_to_surface(surface, x_offset, y_offset, shape_cells=self.next_shape.cells, color=color, x=0, y=0)

    def get_safe_rotation_index(self, index):
        index %= len(self.shape.rotations)
        return index

    def rotate(self, index):
        index -= 1
        return get_safe_rotation_index(index)