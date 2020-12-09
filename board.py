from copy import deepcopy
import random

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
        self.string = ''
        self.left = Field()
        self.right =Field()

    def fill_tile(self, string):
        # 16W0F1  - tile with number 16 with wheat on the left and forest with one crown on the right
        self.string = string
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
        self.crown = int(environment[1])

    # environment # type of environment on this, default E as Empty, rest is Lakes, Wheat, Mines, Grassland, Fores, Swamp
    # tile # tile number, default 0
    # side # left right, default N as None, rest is Left or Right

class Board(object):
    def __init__(self, size):
        self.empty = True
        self.fullness = 0
        self.size = size
        self.full = False
        self.max_tiles = (self.size**2 - 1) / 2
        self.board = [[Field() for _ in range(size)] for _ in range(size)]
        self.board[int((size - 1) / 2)][int((size - 1) / 2)].environment = 'C' # castle in the middle? Do I want this?
        # self.board[0][0].environment = 'C'

    def add_tile(self, tile, left_position=None, right_position=None):
        if left_position:
            if self.empty:
                self.empty = False
            self.fullness += 1
            if self.fullness == self.max_tiles:
                self.full = True
            self.board[left_position[0]][left_position[1]] = tile.left
            self.board[right_position[0]][right_position[1]] = tile.right

    def remove_tile(self, left_position, right_position):
        self.full = False
        self.fullness -= 1
        if self.fullness == 0:
            self.empty = True
        tile = Tile()
        self.board[left_position[0]][left_position[1]] = tile.left
        self.board[right_position[0]][right_position[1]] = tile.right

    def pipe(self, temp_board, i, j, a, b):

        if temp_board[i][j] == temp_board[i + a][j + b]:
            if a:
                return '   |'
            else:
                return ' '
        else:
            if a:
                return '---|'
            else:
                return '|'

    def show(self, attr):
        if attr == 'all':
            split_and_merge(self.show('tile'), self.show('environment'), self.show('crown'))
            return

        table_string = ''
        temp_board = [[-1 for _ in range(self.size + 2)] for _ in range(self.size + 2)]
        for a in range(self.size):
            for b in range(self.size):
                temp_board[a + 1][b + 1] = getattr(self.board[a][b],'environment')

        table_string += '+' + '-'*self.size*3 + '----+' + '\n'
        for i in range(self.size):
            row = '|'
            row_under = '|'
            for j in range(self.size):
                content = getattr(self.board[i][j],attr)
                content = content if not content in ['E', 0] else ''
                row += "{:<3}".format(content) + self.pipe(temp_board, i + 1, j + 1, 0, 1)
            # row += '|'
                row_under += self.pipe(temp_board, i + 1, j + 1, 1, 0)
            table_string += row + '\n'
            table_string += row_under + '\n'
        return table_string
        # print('+' + '-'*self.size*3 + '----+')

    def all_possible_places(self, tile):
        list = []
        visited_board = self.create_visited_board()
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].environment == 'E':
                    continue
                left_match = self.board[i][j].environment == tile.left.environment
                right_match = self.board[i][j].environment == tile.right.environment
                castle_match = self.board[i][j].environment == 'C'
                if left_match or right_match or castle_match:



                    if self.empty:
                        neigh = [(int((self.size - 1)/2),int((self.size - 3)/2))]
                    else:
                        neigh = self.get_neighbours(i,j,'E', visited_board)
                    # neigh = self.get_neighbours(i, j, 'E', visited_board)  # 2.87  57.33

                    while neigh:
                        field = neigh.pop()
                        neigh2 = self.get_neighbours(*field, 'E', visited_board)
                        while neigh2:
                            field2 = neigh2.pop()
                            if left_match:
                                neigh3 = int(bool(self.get_neighbours(*field2, tile.right.environment, visited_board)))
                                list.append((field, field2, neigh3))
                            if right_match: # right match
                                neigh3 = int(bool(self.get_neighbours(*field2, tile.left.environment, visited_board)))
                                # if neigh3:
                                #     print(self.get_neighbours(*field2, tile.right.environment, visited_board))
                                #     print(tile.left.environment, tile.right.environment)
                                #     print(field, field2)
                                #     self.show('all')
                                list.append((field2, field, neigh3))
                            if not list and castle_match:
                                list.extend(((field, field2, -1), (field2, field, -1)))




        return set(list)

    def get_neighbours(self, i, j, env, visited_board):
        # close = [(0, 1), (1, 0), (0, -1), (-1, 0)] # 39.1225    2.27
        # close = [(1, 0), (0, 1), (0, -1), (-1, 0)] # 38.995   2.28
        # close = [(1, 0), (0, 1), (-1, 0), (0, -1)] # 38.995   2.28
        # close = [(0, 1), (1, 0), (0, -1), (-1, 0)] # 39.1225    2.27
        close = [(1, 0), (-1, 0), (0, -1), (0, 1)] # 39.625   2.43
        # close = [(-1, 0), (1, 0), (0, -1), (0, 1)] # 39.415   2.41
        # close = [(-1, 0), (1, 0), (0, 1), (0, -1)] # 38.5025  2.28
        # random.shuffle(close)  # 39.375  2.35
        neighbour = [(i + a[0], j + a[1]) for a in close if not visited_board[i + a[0] + 1][j + a[1] + 1] and
                         self.board[i + a[0]][j + a[1]].environment == env]
        return neighbour

    def bfs(self, visited_board, env, i, j):
        crowns = self.board[i][j].crown
        size = 1
        visited_board[i + 1][j + 1] = True
        queue = self.get_neighbours(i, j, env, visited_board)
        while queue:
            field = queue.pop()
            if not visited_board[field[0] + 1][field[1] + 1]:
                visited_board[field[0] + 1][field[1] + 1] = True
                size += 1
                crowns += self.board[field[0]][field[1]].crown
                queue.extend(self.get_neighbours(*field, env, visited_board))
        # print('size: %d, crowns: %d' %(size, crowns))
        if size%2 == 1 and env == 'E': # can not happen it divide E into two odd parts.
            return -50
        return size * crowns

    def create_visited_board(self):
        return [[False if 0 < i < self.size + 1 and 0 < j < self.size + 1 else True for i in range(self.size + 2)] for j in range(self.size + 2)]

    def score(self):
        points = 0
        visited_board = self.create_visited_board()
        for i in range(self.size):
            for j in range(self.size):
                if not visited_board[i + 1][j + 1]:
                    visited_board[i + 1][j + 1] = True
                    points += self.bfs(visited_board, self.board[i][j].environment, i, j)
        if self.full:
            points += 5
        return points

    def maximize_score(self, tile):
        score = -8
        place = []
        temp_board = deepcopy(self)
        for a, b, good in self.all_possible_places(tile):
            temp_place = (a, b)
            temp_board.add_tile(tile, *temp_place)
            temp_score = temp_board.score()
            if temp_score + (4 * good) > score:
                score = temp_score
                place = temp_place
            temp_board.remove_tile(*temp_place)

        return place, score

    def play(self, sample):
        score = -2
        pos = []
        tile = Tile()
        tile.fill_tile(sample[0])
        for s in sample:
            temp_tile = Tile()
            temp_tile.fill_tile(s)
            temp_pos, temp_score = self.maximize_score(temp_tile)
            if temp_score > score:
                score = temp_score
                pos = temp_pos
                tile = temp_tile
        self.add_tile(tile, *pos)
        return tile, pos

    def real_player(self, sample):
        tile = Tile()
        self.show('all')
        print(sample)
        print('Which tile:')
        tile.fill_tile(sample[int(input())])
        print('What coordinates:')
        a, b, c, d = [int(i) for i in input().split()]
        pos = ((a - 1,b - 1),(c - 1,d - 1))
        self.add_tile(tile, *pos)
        return tile, pos



    # def maximize_score_2(self, tile, previous_tile):
    #     score = -2
    #     place = []
    #     temp_board = deepcopy(self)
    #     for x, y, bad in self.all_possible_places(previous_tile):  #
    #         previous_place = (x, y)
    #         temp_board.add_tile(previous_tile, *previous_place)  #
    #         for a, b, good in self.all_possible_places(tile):
    #             temp_place = (a, b)
    #             temp_board.add_tile(tile, *temp_place)
    #             temp_score = temp_board.score()
    #             if temp_score > score or (temp_score - score >= -2 and good == 1):
    #                 temp_score += good * 2
    #                 score = temp_score
    #                 place = previous_place
    #             # temp_board.add_tile(Tile(), *temp_place)  # works as remove tile
    #             temp_board.remove_tile(*temp_place)
    #         temp_board.remove_tile(*previous_place)  #
    #     return place, score
    #
    # def play_2(self, sample, previous_sample=''):
    #     score = 0
    #     pos = []
    #     tile = Tile()
    #     tile.fill_tile(sample[0])
    #     num = 0
    #     previous_tile = Tile()
    #     if previous_sample:
    #         previous_tile.fill_tile(previous_sample)
    #     else:
    #         previous_tile.fill_tile(sample[0])
    #     for s in sample:
    #         temp_tile = Tile()
    #         temp_tile.fill_tile(s)
    #         temp_pos, temp_score = self.maximize_score_2(temp_tile, previous_tile)
    #         # temp_score += 3 - num
    #         # num += 1
    #         # print(temp_score, temp_tile.left.tile)
    #         if temp_score > score:
    #             score = temp_score
    #             pos = temp_pos
    #             tile = temp_tile
    #     self.add_tile(previous_tile, *pos)
    #     return tile, pos

def split_and_merge(*args):
    table = []
    for i in range(len(args)):
        # print(args[i].split('\n'))
        table.append(args[i].split('\n'))
    # print(table)
    for elem in list(map(list, zip(*table))):
        # print(elem, sep='E')
        for el in elem:
            print(el, sep='E', end ="   ")
        print()

def write_test(filename, sample):
    f = open(filename, "a")
    for s in sample:
        f.writelines(s + 'E')
    f.writelines('\n')
    f.close()

def get_test(filename, game, round):
    f = open(filename, "r")
    sample = [sam for sam in f.readlines()[12 * game + round].split()]
    return sample


## thousand games generation ##
# for _ in range(1000):
#     all = random.sample(tiles, 48)
#     for _ in range(12):
#         sample = []
#         for _ in range(4):
#             sample.append(all.pop())
#         write_test('games',sample)



#
# for i in range(12):
#     ha = get_test('games', 1, i)
#     print(ha)
# b1 = Board(5)
# tile, pos = b1.real_player(samples[0])
# print(tile, pos)

import time
# start = time.time()
# print("hello")
# end = time.time()
# print(end - start)

total_score = 0
total_full = 0
games = 100
m = 0
start = time.time()
for game in range(games):
    # all = random.sample(tiles, 48)
    b1 = Board(5)
    b2 = Board(5)
    b3 = Board(5)
    b4 = Board(5)
    order = [b1, b2, b3, b4]
    ind_current = [0, 1, 2, 3]
    ind_next = [0, 1, 2, 3]
    if game%10 == 0:
        print(game)
    sample = []
    for round in range(12):
        sample = get_test('games', game, round)
        if games == 0:
            split_and_merge(b1.show('tile'), b1.show('environment'), b1.show('crown'))
        # sample = []
        # for _ in range(4):
        #     sample.append(all.pop())

        sample.sort()
        temp_sample = deepcopy(sample)
        # write_test('games', sample)
        for i in range(4):
            # if ind_current[i] == 3:
            #     print(i + 1)
            #     print(temp_sample)
            #     split_and_merge(order[ind_current[i]].show('tile'), order[ind_current[i]].show('environment'),
            #                 order[ind_current[i]].show('crown'))
            if ind_current[i] == 5:
                tile, pos = order[ind_current[i]].real_player(temp_sample)
            else:
                tile, pos = order[ind_current[i]].play(temp_sample)
            # print(tile.string)
            # split_and_merge(order[ind_current[i]].show('tile'), order[ind_current[i]].show('environment'), order[ind_current[i]].show('crown'))
            ind = sample.index(tile.string)
            temp_sample.pop(temp_sample.index(tile.string))
            ind_next[ind] = ind_current[i]
        ind_current = deepcopy(ind_next)
    total_score += max(b1.score(), b2.score(), b3.score(), b4.score()) * 4
    # total_score += sum((b1.score(), b2.score(), b3.score(), b4.score()))
    # for b in order:
        # if 25 > b.score():
        #     print(game)
        #     m = b.score()
        #     print(m)
    # split_and_merge(b1.show('tile'), b1.show('environment'), b1.show('crown'))
    total_full += sum((int(b1.full), int(b2.full), int(b3.full), int(b4.full)))
if games == 1:
    for b in order:
        print(b.score(), end = '\n')
        split_and_merge(b.show('tile'), b.show('environment'), b.show('crown'))
print(total_full/games)
print(total_score/games/4)
# b.show('tile')
# b.show('environment')
# b.show('crown')
# print(b.score())

end = time.time()
print(end - start)