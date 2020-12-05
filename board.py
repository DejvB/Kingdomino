# 26F1W0:
    # 26 - tile number
    # F1 - forest with 1 crown
    # W0 - wheat field without a crown
tiles = ['01W0W0','02W0W0','03F0F0','04F0F0','05F0F0','06F0F0','07L0L0','08L0L0',
         '09L0L0','10G0G0','11G0G0','12S0S0','13W0F0','14W0L0','15W0G0','16W0S0',
         '17F0L0','18F0G0','19W1F0','20W1L0','21W1G0','22W1S0','23W1M0','24F1W0',
         '25F1W0','26F1W0','27F1W0','28F1L0','29F1G0','30L1W0','31L1W0','32L1F0',
         '33L1F0','34L1F0','35L1F0','36W0G1','37L0G1','38W0S1','39G0S1','40M1W0',
         '41W0G2','42L0G2','43W0S2','44G0S2','45M2W0','46S0M2','47S0M2','48W0M3']

class Tile(object):
    def __init__(self):
        self.left = Field()
        self.right =Field()

    def fill_tile(self, string):
        # 16W0F1  - tile with number 16 with wheat on the left and forest with one crown on the right
        self.left.fill_field('L', string[:2], string[2:4])
        self.right.fill_field('R', string[:2], string[4:6])


class Field(object):
    def __init__(self):
        self.side = 'N'
        self.tile = 0
        self.environment = 'E'
        self.crown = 0

    def fill_field(self, side, number, environment):
        self.side = side
        self.tile = int(number)
        self.environment = environment[0]
        self.crown = environment[1]

    # environment # type of environment on this, default E as Empty, rest is Lakes, Wheat, Mines, Grassland, Fores, Swamp
    # tile # tile number, default 0
    # side # left right, default N as None, rest is Left or Right

class Board(object):
    def __init__(self, size):
        self.size = size
        self.board = [[Field() for _ in range(size)] for _ in range(size)]
        self.board[(size + 1) / 2][(size + 1) / 2].environment = 'C' # castle in the middle? Do I want this?

    def add_tile(self, tile, left_position, right_position):
        self.board[left_position[0]][left_position[1]] = tile.left
        self.board[right_position[0]][right_position[1]] = tile.right

    def show(self, attr):
        for i in range(self.size):
            for j in range(self.size):
                print(getattr(self.board[i][j],attr), end =" ")
            print()

    def all_possible_places(self, tile):
        places = []

        return places

    def score(self):
        points = 0
        
        return points

t1 = Tile()
t2 = Tile()
t1.fill_tile('01W0W0')
t2.fill_tile('30G2L0')
b = Board(3)
b.add_tile(t1, (0,0), (0,1))
b.add_tile(t2, (1,2), (1,1))
b.show('environment')