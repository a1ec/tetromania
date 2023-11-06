from gfx import Color, fill_cell

def rotate_shape(shape):
    return list(zip(*shape[::-1]))

def text_to_list2D(text):
    'Create a 2D shape from a text string'
    return [[int(cell) for cell in row] for row in text.split('\n') if row]

def list2D_to_text(two_d_list):

    return '\n'.join(''.join(str(i) for i in row) for row in two_d_list)

def remove_duplicates_2d(original_list):
    no_duplicates = list(set(tuple(map(tuple, x)) for x in original_list))
    return [list(map(list, x)) for x in no_duplicates]

def generate_rotations(shape):
    rotations = [shape]
    for _ in range(3):
        rotations.append(rotate_shape(rotations[-1]))
    return rotations

color_to_index = {color: i for i, color in enumerate(Color)}

class Shape:
    def __init__(self, text, type_, color):
        shape = text_to_list2D(text)
        self.rotations = generate_rotations(shape)
        #self.rotations = remove_duplicates_2d(self.rotations)
        self.type = type_
        self.color = color
        self.grid_value = color_to_index[color]
        self._rotate_index = 0

    def __repr__(self):
        return f'{self.type}Shape'

    def debug(self):
        print(f'Printing shape: {self.type}')
        self.print_rotations()

    @property
    def shape(self):
        return self.rotations[self._rotate_index]

    @property
    def height(self):
        return len(self.shape)

    @property
    def width(self):
        return len(self.shape[0])

    def print_rotations(self):
        for shape in self.rotations:
            print(list2D_to_text(shape),'\n')

    def is_ok_to_plot(self, grid, x_offset, y_offset):
        # Check if any values are out of bounds or would overwrite existing grid values
        for row in range(self.height):
            for col in range(self.width):
                if self.shape[row][col] != 0:
                    y = y_offset + row
                    x = x_offset + col
                    if (y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]) or grid[y][x] != 0):
                        return False
        return True

    def iterate_shape_over_grid(self, grid, x_offset, y_offset, func):
        for row in range(self.height):
            for col in range(self.width):
                if self.shape[row][col] != 0:
                    y = y_offset + row
                    x = x_offset + col
                    if (y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]) or grid[y][x] != 0):
                        return False
        return True

    def is_cell_empty(self, grid, x, y):
        return grid[y][x] != 0

    def is_cell_outside_grid(self, grid, x, y):
        return y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0])

    def set_on_grid(self, grid, x_offset, y_offset):
        if self.is_ok_to_plot(grid, x_offset, y_offset):
            # Plot the values onto the grid
            for row in range(self.height):
                for col in range(self.width):
                    if self.shape[row][col] != 0:
                        y = y_offset + row
                        x = x_offset + col
                        grid[y][x] = self.grid_value

    def draw(self, x_offset, y_offset, surface):
        'Draws the shape to screen only, for play or next'
        # calculate the x, y offset of the shape on screen
        values = self.rotations[self._rotate_index]
        for shape_y in range(len(values)):
            for shape_x in range(len(values[shape_y])):
                if values[shape_y][shape_x] != 0:
                    x = x_offset + shape_x
                    y = y_offset + shape_y
                    fill_cell(x, y, self.grid_value, surface)

    def rotate(self):
        self._rotate_index += 1
        self._rotate_index %= len(self.rotations)

I_SHAPE_TEXT = "1111\n0000"
O_SHAPE_TEXT = "11\n11"
T_SHAPE_TEXT = "010\n111\n000"
J_SHAPE_TEXT = "100\n111\n000"
L_SHAPE_TEXT = "001\n111\n000"
S_SHAPE_TEXT = "011\n110\n000"
Z_SHAPE_TEXT = "110\n011\n000"

I_SHAPE_TEXT = "1111"
O_SHAPE_TEXT = "11\n11"
T_SHAPE_TEXT = "010\n111"
J_SHAPE_TEXT = "100\n111"
L_SHAPE_TEXT = "001\n111"
S_SHAPE_TEXT = "011\n110"
Z_SHAPE_TEXT = "110\n011"

IShape = Shape(I_SHAPE_TEXT, 'I', Color.RED)
OShape = Shape(O_SHAPE_TEXT, 'O', Color.BLUE)
TShape = Shape(T_SHAPE_TEXT, 'T', Color.YELLOW)
JShape = Shape(J_SHAPE_TEXT, 'J', Color.WHITE)
LShape = Shape(L_SHAPE_TEXT, 'L', Color.PURPLE)
SShape = Shape(S_SHAPE_TEXT, 'S', Color.GREEN)
ZShape = Shape(Z_SHAPE_TEXT, 'Z', Color.CYAN)

Shapes = [IShape, OShape, TShape, JShape, LShape, SShape, ZShape]