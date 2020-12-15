from copy import deepcopy
import random
import numpy as np
import time
# start = time.time()
# end = time.time()
# print(end - start)

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
        self.tiles = []
        self.selected = []
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
            self.tiles.append(tile.string)

    def remove_tile(self, left_position, right_position):
        self.full = False
        self.fullness -= 1
        if self.fullness == 0:
            self.empty = True
        tile = Tile()
        self.board[left_position[0]][left_position[1]] = tile.left
        self.board[right_position[0]][right_position[1]] = tile.right
        self.tiles.pop()

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
                row += " {:<2}".format(content) + self.pipe(temp_board, i + 1, j + 1, 0, 1)
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
                    # if self.empty:
                    #     neigh = [(int((self.size - 1)/2),int((self.size - 3)/2))]
                    # else:
                    #     neigh = self.get_neighbours(i,j,'E', visited_board)
                    neigh = self.get_neighbours(i, j, 'E', visited_board)  # 2.87  57.33

                    while neigh:
                        field = neigh.pop()
                        neigh2 = self.get_neighbours(*field, 'E', visited_board)
                        while neigh2:
                            field2 = neigh2.pop()
                            if left_match and right_match: #  50.777 62.929 3.419, 50.8095 62.796 3.642
                                right_match == False
                            if left_match:
                                neigh3 = int(bool(self.get_neighbours(*field2, tile.right.environment, visited_board)))
                                castle_1 = int(bool(self.get_neighbours(*field2, 'C', visited_board)))
                                castle_2 = int(bool(self.get_neighbours(*field, 'C', visited_board)))
                                list.append((field, field2, neigh3 - castle_1 - castle_2))
                            if right_match: # right match
                                neigh3 = int(bool(self.get_neighbours(*field2, tile.left.environment, visited_board)))
                                castle_1 = int(bool(self.get_neighbours(*field2, 'C', visited_board)))
                                castle_2 = int(bool(self.get_neighbours(*field, 'C', visited_board)))
                                list.append((field2, field, neigh3 - castle_1 - castle_2))
                            if not list and castle_match:
                            # if not left_match and not right_match and castle_match:
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
            return size, -50
        return size,  crowns

    def create_visited_board(self):
        return [[False if 0 < i < self.size + 1 and 0 < j < self.size + 1 else True for i in range(self.size + 2)] for j in range(self.size + 2)]

    def score(self):
        points = 0
        fiefs = []
        visited_board = self.create_visited_board()
        for i in range(self.size):
            for j in range(self.size):
                if not visited_board[i + 1][j + 1]:
                    visited_board[i + 1][j + 1] = True
                    fief_size, crowns = self.bfs(visited_board, self.board[i][j].environment, i, j)
                    points += fief_size * crowns
                    if self.board[i][j].environment != 'E':
                        fiefs.append(fief_size)
        if self.full:
            points += 5
        return points, sum(fiefs) / len(fiefs)


    def maximize_score(self, tile):
        score = -10
        place = []
        temp_board = deepcopy(self)
        for a, b, good in self.all_possible_places(tile):
            temp_place = (a, b)
            temp_board.add_tile(tile, *temp_place)
            temp_score, fief_coef = temp_board.score()
            if temp_score + (2 * good) + fief_coef > score:   #  48.4475 60.434 2.988
                score = temp_score  + (2 * good) + fief_coef
                place = temp_place
            temp_board.remove_tile(*temp_place)

        return place, score

    def play(self, sample):
        score = -10
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



    def maximize_score_2(self, tile, previous_tile, score):
        # score = -10
        place = []
        previous_place = []
        temp_board = deepcopy(self)
        previous_possible = False
        current_possible = False
        for x, y, bad in self.all_possible_places(previous_tile):
            previous_possible = True
            temp_previous_place = (x, y)
            temp_board.add_tile(previous_tile, *temp_previous_place)
            for a, b, good in temp_board.all_possible_places(tile):
                current_possible = True
                temp_place = (a, b)
                temp_board.add_tile(tile, *temp_place)
                temp_score, fief_coef = temp_board.score()
                if temp_score + (2 * good) + (2 * bad) + fief_coef > score:
                    score = temp_score + (2 * good) + (2 * bad) + fief_coef
                    place = temp_place
                    previous_place = temp_previous_place
                # if previous_tile.string == '47S0M2':
                #     print('Chosen: ', previous_tile.string, previous_place, tile.string, place, score)
                #     print('Temp: ', previous_tile.string, temp_previous_place, tile.string, temp_place, temp_score + (2 * good) + fief_coef)
                #     temp_board.show('all')
                temp_board.remove_tile(*temp_place)
            temp_board.remove_tile(*temp_previous_place)
        if current_possible:
            return previous_place, place, score
        elif previous_possible:
            place, score = self.maximize_score(previous_tile)
            return place, [], score
        elif temp_board.all_possible_places(tile):
            place, score = self.maximize_score(tile)
            return [], place, score
        else:
            return [], [], score

    def play_2(self, sample, previous_sample=''):
        score = -10
        pos = []
        previous_pos = []
        tile = Tile()
        tile.fill_tile(sample[0])
        previous_tile = Tile()
        if previous_sample:
            previous_tile.fill_tile(previous_sample)
            for s in sample:
                temp_tile = Tile()
                temp_tile.fill_tile(s)
                # if tile.string == '07L0L0': # 03F0F0
                #     print(tile.string, pos, previous_tile.string, previous_pos)
                temp_previous_pos, temp_pos, temp_score = self.maximize_score_2(temp_tile, previous_tile, score)
                if temp_score > score:
                    score = temp_score
                    pos = temp_pos
                    previous_pos = temp_previous_pos
                    tile = temp_tile
            if previous_sample:
                self.add_tile(previous_tile, *previous_pos)
            return tile, previous_pos, pos
        else:
            for s in sample:
                temp_tile = Tile()
                temp_tile.fill_tile(s)
                temp_pos, temp_score = self.maximize_score(temp_tile)
                if temp_score > score:
                    score = temp_score
                    pos = temp_pos
                    tile = temp_tile
            return tile, pos, pos

def split_and_merge(*args):
    table = []
    for i in range(len(args)):
        table.append(args[i].split('\n'))
    for elem in list(map(list, zip(*table))):
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

def stats(boards):
    max_points = 0
    sum_points = 0
    filled = 0
    for board in boards:
        points, _ = board.score()
        max_points = points if points > max_points else max_points
        sum_points += points
        filled = filled + 1 if board.full else filled
    return [sum_points, max_points, filled]



def start_game(game, players=4, results=False):
    if players == 2:
        b1 = Board(7)
        b2 = Board(7)
        order = random.shuffle([b1, b2, b1, b2])
    elif players == 4: # what about three players?
        b1 = Board(5)
        b2 = Board(5)
        b3 = Board(5)
        b4 = Board(5)
        order = [b1, b2, b3, b4]
    ind_current = [0, 1, 2, 3]
    ind_next = [0, 1, 2, 3]
    for round in range(12):
        sample = get_test('games', game, round)
        sample.sort()
        temp_sample = deepcopy(sample)
        for i in range(4):
            print('round: ' + str(round) + '  player: ' + str(ind_current[i]))  ###
            if ind_current[i] == 5:
                tile, pos = order[ind_current[i]].real_player(temp_sample)
            else:
                tile, pos = order[ind_current[i]].play(temp_sample)
            print('Selected: ', tile.string)  ###
            ind = sample.index(tile.string)
            temp_sample.pop(temp_sample.index(tile.string))
            ind_next[ind] = ind_current[i]
            # if ind_current[i] == 3:
            #     b4.show('all')
        ind_current = deepcopy(ind_next)
    # for b in order:
        # if b.score()[0] < 25: # 47, 86
        #     print(game)
    if results:
        for b in order:
            print(b.score()[0], end='\n')
            split_and_merge(b.show('tile'), b.show('environment'), b.show('crown'))
    return stats(order)

def update_tile_stats(board):
    for tile in board.tiles:
        tile_stats[tile] += board.score()[0]


def start_game_2(game, players=4, results=False):
    if players == 2:
        b1 = Board(7)
        b2 = Board(7)
        order = random.shuffle([b1, b2, b1, b2])
        order = [b1, b2, b2, b1]
    elif players == 4: # what about three players?
        b1 = Board(5)
        b2 = Board(5)
        b3 = Board(5)
        b4 = Board(5)
        order = [b1, b2, b3, b4]
    ind_current = [0, 1, 2, 3]
    ind_previous = [0, 1, 2, 3]
    ind_next = [0, 1, 2, 3]
    sample = []
    for round in range(12):
        if sample:
            previous_sample = deepcopy(sample)
        else:
            previous_sample = ['', '', '', '']
        sample = get_test('games', game, round)
        sample.sort()
        temp_sample = deepcopy(sample)
        # print(sample)
        for i in range(4):
            # print('round: ' + str(round) + '  player: ' + str(ind_current[i]))  ###
            # print(sample)  ###
            # print(temp_sample)  ###
            # order[ind_current[i]].show('all')  ###
            if ind_current[i] == 1:
                # tile, previous_pos = order[ind_current[i]].real_player(temp_sample)
                tile, previous_pos, pos = order[ind_current[i]].play_2(temp_sample, previous_sample[i])
            else:
                # print(previous_sample, ind_previous, ind_current, i)
                tile, pos = order[ind_current[i]].play(temp_sample)
                # tile, previous_pos, pos = order[ind_current[i]].play_2(temp_sample, previous_sample[i])
            order[ind_current[i]].selected.append(tile.string)
            # print('Selected: ', tile.string)  ###
            if round == 11:
                # print(tile.string, previous_pos, pos)
                order[ind_current[i]].add_tile(tile, *pos)
            ind = sample.index(tile.string)
            temp_sample.pop(temp_sample.index(tile.string))
            ind_next[ind] = ind_current[i]
        ind_previous = deepcopy(ind_current)
        ind_current = deepcopy(ind_next)
    # for b in order:
        # if b.score()[0] < 250:
            # print(game)
            # print(b.selected)
            # print(b.tiles)
            # b.show('all')
    for b in order:
        # update_tile_stats(b)
        if b.score()[0] < 25:
            print(game)
            print(b.tiles)
            b.score()[0]
            b.show('all')
    if results:
        for b in order:
            # print(sample, ind_previous)
            print(b.score()[0], end='\n')
            split_and_merge(b.show('tile'), b.show('environment'), b.show('crown'))
            print(b.tiles)
    return stats(order)


def test(games, shift, players):
    start = time.time()
    stats = []
    if games <= 10:
        for game in range(games):
            stats.append(start_game_2(game + shift, players, True))   # start_game
    else:
        for game in range(games):
            if game%10 == 0:
                print(game)
            stats.append(start_game_2(game + shift, players, False))  # start_game_2
    stats = np.array(stats)
    print(sum(stats[:,0])/games/players, sum(stats[:,1])/games, sum(stats[:,2])/games)
    end = time.time()
    print('Total time is: ', end - start)

## thousand games generation ##
# for _ in range(1000):
#     all = random.sample(tiles, 48)
#     for _ in range(12):
#         sample = []
#         for _ in range(4):
#             sample.append(all.pop())
#         write_test('games',sample)

# tile_stats = {i : 0 for i in tiles}
test(1,356,4)
# for t in tiles:
#     print(t, tile_stats[t] / 100)


