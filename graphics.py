import random
import copy
import pygame

width = 600
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('2048')

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

thickness = 50

class AI():
    def __init__(self, brain = None):
        self.brain = brain
    
    def make_choice(self, board):
        choice = random.randint(0,3)
        if choice == 0:
            board.move_left()
        if choice == 1:
            board.move_up()
        if choice == 2:
            board.move_right()
        if choice == 3:
            board.move_down()

class Board():
    def __init__(self, size = 4, score = 0, array = [], temp = False):
        self.size = size
        self.array = array
        if array == []:
            for i in range(size):
                self.array.append([0] * size)
        self.score = score
        self.temp = temp
        self.rect = (width / thickness, height - width * ((thickness - 1) / thickness), width * ((thickness - 2) / thickness), width * ((thickness - 2) / thickness))

    def add_tile(self):
        open_spots = []
        for x in range(self.size):
            for y in range(self.size):
                if self.array[x][y] == 0:
                    open_spots.append([x, y])
        if not open_spots:
            return
        new_spot = random.choice(open_spots)
        x, y = new_spot[0], new_spot[1]
        self.array[x][y] = random.choices([2, 4], weights = [0.9, 0.1])[0]
    
    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            temp_board = Board(array = copy.deepcopy(self.array), temp = True)
            temp_board.move_left()
            if temp_board.array != self.array:
                self.move_left()
        
        elif keys[pygame.K_RIGHT]:
            temp_board = Board(array = copy.deepcopy(self.array), temp = True)
            temp_board.move_right()
            if temp_board.array != self.array:
                self.move_right()

        elif keys[pygame.K_UP]:
            temp_board = Board(array = copy.deepcopy(self.array), temp = True)
            temp_board.move_up()
            if temp_board.array != self.array:
                self.move_up()

        elif keys[pygame.K_DOWN]:
            temp_board = Board(array = copy.deepcopy(self.array), temp = True)
            temp_board.move_down()
            if temp_board.array != self.array:
                self.move_down()

    def move_left(self):
        for row in self.array:
            for x in range(self.size):
                last_tile = 0
                for i in range(x-1, last_tile-1, -1):
                    if row[i] == 0:
                        if i == last_tile:
                            row[i] = int(row[x])
                            row[x] = 0
                            break
                    elif row[i] == row[x]:
                        row[i] *= 2
                        self.score += row[i]
                        row[x] = 0
                        last_tile = i + 1
                        break
                    else:
                        row[i+1] = int(row[x])
                        if i + 1 != x:
                            row[x] = 0
                        break
        if not self.temp:
            self.add_tile()

    def move_right(self):
        for row in self.array:
            row.reverse()
            for x in range(self.size):
                last_tile = 0
                for i in range(x-1, last_tile-1, -1):
                    if row[i] == 0:
                        if i == last_tile:
                            row[i] = int(row[x])
                            row[x] = 0
                            break
                    elif row[i] == row[x]:
                        row[i] *= 2
                        self.score += row[i]
                        row[x] = 0
                        last_tile = i + 1
                        break
                    else:
                        row[i+1] = int(row[x])
                        if i + 1 != x:
                            row[x] = 0
                        break
            row.reverse()
        if not self.temp:
            self.add_tile()

    def move_up(self):
        for y in range(self.size):
            col = []
            for x in range(self.size):
                col.append(int(self.array[x][y]))
            for x in range(self.size):
                last_tile = 0
                for i in range(x-1, last_tile-1, -1):
                    if col[i] == 0:
                        if i == last_tile:
                            col[i] = int(col[x])
                            col[x] = 0
                            break
                    elif col[i] == col[x]:
                        col[i] *= 2
                        self.score += col[i]
                        col[x] = 0
                        last_tile = i + 1
                        break
                    else:
                        col[i+1] = int(col[x])
                        if i + 1 != x:
                            col[x] = 0
                        break
            for x in range(self.size):
                self.array[x][y] = col[x]
        if not self.temp:
            self.add_tile()

    def move_down(self):
        for y in range(self.size):
            col = []
            for x in range(self.size):
                col.append(int(self.array[x][y]))
            col.reverse()
            for x in range(self.size):
                last_tile = 0
                for i in range(x-1, last_tile-1, -1):
                    if col[i] == 0:
                        if i == last_tile:
                            col[i] = int(col[x])
                            col[x] = 0
                            break
                    elif col[i] == col[x]:
                        col[i] *= 2
                        self.score += col[i]
                        col[x] = 0
                        last_tile = i + 1
                        break
                    else:
                        col[i+1] = int(col[x])
                        if i + 1 != x:
                            col[x] = 0
                        break
            col.reverse()
            for x in range(self.size):
                self.array[x][y] = col[x]
        if not self.temp:
            self.add_tile()

    def draw(self, win):
        # Score
        text = font.render('Score : ' + str(self.score), True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (width / 2, 50)
        win.blit(text, textRect)

        # Main Board Space
        pygame.draw.rect(win, (160, 160, 160), self.rect)

        # Tiles
        length = (thickness - 2 - self.size - 1) * width / (thickness * self.size)
        for x in range(self.size):
            for y in range(self.size):
                rect = (self.rect[0] + (width * (x + 1) / thickness) + length * x, self.rect[1] + (width * (y + 1) / thickness) + length * y, length, length)
                pygame.draw.rect(win, self.color(self.array[y][x]), rect)
                # Tile Value
                if self.array[y][x] != 0:
                    text = font.render(str(self.array[y][x]), True, (0,0,0))
                    textRect = text.get_rect()
                    textRect.center = (rect[0] + length / 2, rect[1] + length / 2)
                    win.blit(text, textRect)

    def check_loss(self):
        temp_board = Board(array = copy.deepcopy(self.array))
        temp_board.move_left()
        if temp_board.array != self.array:
            return False

        temp_board = Board(array = copy.deepcopy(self.array))
        temp_board.move_up()
        if temp_board.array != self.array:
            return False

        temp_board = Board(array = copy.deepcopy(self.array), temp = True)
        temp_board.move_right()
        if temp_board.array != self.array:
            return False

        temp_board = Board(array = copy.deepcopy(self.array), temp = True)
        temp_board.move_down()
        if temp_board.array != self.array:
            return False

        return True

    def restart(self):
        self.score = 0
        self.array = []
        for i in range(self.size):
            self.array.append([0] * self.size)
        self.add_tile()
        self.add_tile()

    def print_board(self):
        for row in self.array:
            print(row)

    def color(self, val):
        '''
        try:
            colors = [...]
            return colors[log_2(val)]
        except:
            return (255, 255, 255)
        '''
        if val == 0:
            return (180, 180, 180)
        if val == 2:
            return (238, 228, 218)
        if val == 4:
            return (237, 224, 200)
        if val == 8:
            return (242, 177, 121)
        if val == 16:
            return (245, 149, 99)
        if val == 32:
            return (246, 124, 95)
        if val == 64:
            return (246, 94, 59)
        if val == 128:
            return (237, 207, 114)
        if val == 256:
            return (237, 204, 97)
        if val == 512:
            return (237, 197, 63)
        if val == 1024:
            return (237, 197, 63)
        if val == 2048:
            return (237, 197, 30)
        if val == 4096:
            return (100, 184, 145)
        if val == 8192:
            return (56, 140, 100)
        if val == 16384:
            return (56, 107, 126)
        if val == 32768:
            return (46, 118, 190)
        return(255, 255, 255)

def redraw_window(win, board):
    win.fill((255, 255, 255))
    font.render('Score : ', False, (0, 0, 0))
    board.draw(win)
    pygame.display.update()

def main():
    
    clock = pygame.time.Clock()
 
    # Uncomment to have AI 'play' (in quotes because it currently plays randomly lol)
    # a = AI()

    current_size = 4

    b = Board(current_size)
    b.restart()

    averages = []
    scores = [[], []]

    while True:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        b.move()
        try:
            a.make_choice(b)
        except:
            b.move()
        if b.check_loss():

            '''
            scores[current_size - 4].append(b.score)
            print('Games Played :', len(scores[current_size - 4]))
            print('Current Score :', b.score)
            print('Current Average Score :', sum(scores[current_size - 4]) / len(scores[current_size - 4]))
            print('Average Scores', averages)
            if len(scores[current_size - 4]) == 100:
                scores.append([])
                f = open('scores.txt', 'a')
                f.write('Size (' + str(current_size)+') : ' + str(scores[current_size - 4]) + '\n')
                f.close()
                current_size += 1
                b.size = b.size + 1
            if current_size == 15:
                break
            '''

            b.restart()
        redraw_window(win, b)

main()
