class Tile(object):
    def __init__(self, number, left_environment, right_environment, crown_position, crown_count):
        self.number = number
        self.left_environment = left_environment
        self.right_environment = right_environment
        self.crown_position = crown_position
        self.crown_count = crown_count

class Field(object):
    def __init__(self):
        self.environment = 'E'
        self.tile = 0
        self.side = 'N'

    def add_left(self, tile):
        self.environment = tile.left_environment
        self.tile = tile.number
        self.side = 'L'

    def add_right(self, tile):
        self.environment = tile.right_environment
        self.tile = tile.number
        self.side = 'R'
    # environment # type of environment on this, default E as Empty, rest is Lakes, Wheat, Mines, Grassland, Fores, Swamp
    # tile # tile number, default 0
    # side # left right, default N as None, rest is Left or Right

class Board(object):
    def __init__(self, size):
        self.size = size
        self.board = [[Field() for _ in range(size)] for _ in range(size)]

    def get_pos(self, position):
        return self.board[position[0]][position[1]]

    def add_tile(self, tile, left_position, right_position):
        self.get_pos(left_position).add_left(tile)
        self.get_pos(right_position).add_right(tile)

    def show(self, attr):
        for i in range(self.size):
            for j in range(self.size):
                print(getattr(self.get_pos((i,j)),attr), end =" ")
            print()

t1 = Tile(1,'S','S','L',1)
t2 = Tile(2,'L','F','N',0)
b = Board(3)
b.add_tile(t1, (0,0), (0,1))
b.add_tile(t2, (1,2), (1,1))
b.show('side')