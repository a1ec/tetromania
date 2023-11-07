from gfx import Color, fill_cell
import pygame

def text_to_list2D(text):
    'Create cells (a 2D list) from a text string'
    return [[int(cell) for cell in row] for row in text.split('\n') if row]

def list2D_to_text(two_d_list):
    'Create a text string from cells (a 2D list)'
    return '\n'.join(''.join(str(i) for i in row) for row in two_d_list)

def remove_duplicates_2d(original_list):
    no_duplicates = list(set(tuple(map(tuple, x)) for x in original_list))
    return [list(map(list, x)) for x in no_duplicates]

def generate_rotations(cells):
    rotations = [cells]
    for _ in range(3):
        rotations.append(rotate_shape(rotations[-1]))
    return rotations

def rotate_shape(cells):
    return list(zip(*cells[::-1]))

color_to_index = {color: i for i, color in enumerate(Color)}

class Shape:
    def __init__(self, text, type_, color):
        cells = text_to_list2D(text)
        self.rotations = generate_rotations(cells)
        self.type = type_
        self.color = color
        self._rotation_index = 0

    @property
    def cells(self):
        return self.rotations[self._rotation_index]

    @property
    def height(self):
        return len(self.cells)

    @property
    def width(self):
        return len(self.cells[0])
        
I_SHAPE_TEXT = "1111"
O_SHAPE_TEXT = "11\n11"
T_SHAPE_TEXT = "010\n111"
J_SHAPE_TEXT = "100\n111"
L_SHAPE_TEXT = "001\n111"
S_SHAPE_TEXT = "011\n110"
Z_SHAPE_TEXT = "110\n011"

IShape = Shape(I_SHAPE_TEXT, 'I', Color.LIGHT_BLUE)
OShape = Shape(O_SHAPE_TEXT, 'O', Color.YELLOW)
TShape = Shape(T_SHAPE_TEXT, 'T', Color.MAGENTA)
JShape = Shape(J_SHAPE_TEXT, 'J', Color.BLUE)
LShape = Shape(L_SHAPE_TEXT, 'L', Color.ORANGE)
SShape = Shape(S_SHAPE_TEXT, 'S', Color.GREEN)
ZShape = Shape(Z_SHAPE_TEXT, 'Z', Color.RED)

Tetrominoes = [IShape, OShape, TShape, JShape, LShape, SShape, ZShape]