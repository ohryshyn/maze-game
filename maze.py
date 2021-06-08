"""
AUTHOR: Oleh Hryshyn
"""
# constants for cell size and world dimensions
from tkinter import *
CELL_SIZE = 65
(x, y) = (15, 10)
SCALE = 0.2
score = 0
MOVE_REWARD = -x * y / 2
FONT = ('Arial', int(CELL_SIZE / 2.5))


def h_wall(y0, x1, x2):
    """
    Returns a list of (x,y) coordinates to render a horizontal wall (going from left to right)
    :param y0: y-coordinate of the wall
    :param x1: starting x-coordinate of the wall
    :param x2: ending x-coordinate of the wall
    """
    list_x_coord = [i for i in range(x1, x2)]
    list_y_coord = [y0 for i in range(x2 - x1)]
    return list(zip(list_x_coord, list_y_coord))


def v_wall(x0, y1, y2):
    """
    Returns a list of (x,y) coordinates to render a vertical wall (going from top to bottom)
    :param x0: x-coordinate of the wall
    :param y1: starting y-coordinate of the wall
    :param y2: ending y-coordinate of the wall
    """
    list_x_coord = [x0 for i in range(y2 - y1)]
    list_y_coord = [i for i in range(y1, y2)]
    return list(zip(list_x_coord, list_y_coord))


#  declare location of the sprites
WALLS = {'coordinates': [],
         'color': 'black'}

LAVA = {'coordinates': [*v_wall(7, 0, 3), *h_wall(8, 5, 8), *v_wall(13, 7, 9), *v_wall(11, 8, 10),
                        ],
        'color': 'firebrick3',
        'reward': -x * y * 4}

EXIT = {'coordinates': [(13, 1)],
        'color': 'green3',
        'reward': x * y * 100}

KEYS = {'coordinates': [(1, 1), (6, 9), (14, 7), (10, 4), (2, 6)],
        'color': ['gold', 'seashell3'],
        'reward': x * y * 1.5}

PLAYER_SPRITE = {'coordinates': [(0, 9)],
                 'color': 'purple'}

master = Tk()
master.title('Trial Maze')
w = Canvas(master, width=x * CELL_SIZE + 2 * CELL_SIZE, height=y * CELL_SIZE)


def build_grid():
    """ Renders a grid for the maze"""
    for i in range(x):
        for j in range(y):
            w.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                               (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                               fill='white')


def build_walls():
    """ Renders the walls """
    for i, j in WALLS['coordinates']:
        w.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                           (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                           fill=WALLS['color'])


def build_lava():
    """ Renders lava """
    for i, j in LAVA['coordinates']:
        w.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                           (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                           fill=LAVA['color'])


def build_exit():
    """ Renders exit """
    for i, j in EXIT['coordinates']:
        w.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                           (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                           fill=EXIT['color'])


def put_keys():
    """ Renders keys """
    n = 0
    for i, j in KEYS['coordinates']:
        w.create_oval(shrink(i), shrink(j),
                      shrink(i + 1, False), shrink(j + 1, False),
                      fill=KEYS['color'][0], tags=f'oval{n}')
        n += 1


def draw_guide():
    """ Displays a guide for the game """
    w.create_text(x * CELL_SIZE + CELL_SIZE * 0.85, CELL_SIZE * 1.6, text='you', font=FONT, anchor='e',
                  fill=PLAYER_SPRITE['color'])
    w.create_text(x * CELL_SIZE + CELL_SIZE * 1.4,
                  CELL_SIZE * 1.6, text='must', font=FONT)
    w.create_text(x * CELL_SIZE + CELL_SIZE * 1.28, CELL_SIZE *
                  2, text='gather', font=FONT, anchor='e')
    w.create_text(x * CELL_SIZE + CELL_SIZE * 1.6, CELL_SIZE * 2, text='all',
                  font=('Arial', int(CELL_SIZE / 2.5), 'bold'))
    w.create_text(x * CELL_SIZE + CELL_SIZE, CELL_SIZE * 2.4,
                  anchor='e', text='keys', font=FONT, fill=KEYS['color'][0])
    w.create_text(x * CELL_SIZE + CELL_SIZE + CELL_SIZE /
                  2.5, CELL_SIZE * 2.4, text='and', font=FONT)
    w.create_text(x * CELL_SIZE + CELL_SIZE * 1.1, CELL_SIZE *
                  2.8, anchor='e', text='avoid', font=FONT)
    w.create_text(x * CELL_SIZE + CELL_SIZE * 1.6, CELL_SIZE *
                  2.8, text='lava', font=FONT, fill=LAVA['color'])
    w.create_text(x * CELL_SIZE + CELL_SIZE * 1.5, CELL_SIZE *
                  3.2, text='to open', anchor='e', font=FONT)
    w.create_text(x * CELL_SIZE + CELL_SIZE * 0.7, CELL_SIZE *
                  3.6, text='the', anchor='e', font=FONT)
    w.create_text(x * CELL_SIZE + CELL_SIZE * 1.2, CELL_SIZE *
                  3.6, text='door', font=FONT, fill=EXIT['color'])


def create_player():
    """ Renders player character"""
    return w.create_rectangle(shrink(PLAYER_SPRITE['coordinates'][0][0]),
                              shrink(PLAYER_SPRITE['coordinates'][0][1]),
                              shrink(
                                  (PLAYER_SPRITE['coordinates'][0][0] + 1), False),
                              shrink(
                                  (PLAYER_SPRITE['coordinates'][0][1] + 1), False),
                              fill=PLAYER_SPRITE['color'])


def move(event):
    global score
    dx, dy = 0, 0
    m1, m2, m3, m4 = 1, 1, 1, 1
    score += MOVE_REWARD
    if wall_check_west():
        m1 = 0
    if wall_check_east():
        m2 = 0
    if wall_check_north():
        m3 = 0
    if wall_check_south():
        m4 = 0
    if event.char == "a":
        dx = -CELL_SIZE * m1
    if event.char == "d":
        dx = CELL_SIZE * m2
    if event.char == "w":
        dy = -CELL_SIZE * m3
    if event.char == "s":
        dy = CELL_SIZE * m4
    w.move(player, dx, dy)
    # print(score)
    pick_up_key()
    restart()


def shrink(coord, upper_left=True):
    if upper_left:
        return coord * CELL_SIZE + SCALE * CELL_SIZE
    else:
        return coord * CELL_SIZE - SCALE * CELL_SIZE


def get_coord(coord, upper_left=True):
    if upper_left:
        return int((coord - SCALE * CELL_SIZE) / CELL_SIZE)
    else:
        return int((coord + SCALE * CELL_SIZE) / CELL_SIZE)


def pick_up_key():
    pl = (get_coord(w.coords([player])[0]), get_coord(w.coords([player])[1]))
    if pl in KEYS['coordinates']:
        index = KEYS['coordinates'].index(pl)
        w.itemconfig(f'oval{index}', fill=KEYS['color'][1])


def wall_check_east():
    east = (get_coord(w.coords([player])[0]) +
            1, get_coord(w.coords([player])[1]))
    if (east in WALLS['coordinates']) or (east[0] == x):
        return True
    else:
        return False


def wall_check_west():
    west = (get_coord(w.coords([player])[0]) -
            1, get_coord(w.coords([player])[1]))
    if (west in WALLS['coordinates']) or (west[0] < 0):
        return True
    else:
        return False


def wall_check_south():
    south = (get_coord(w.coords([player])[0]),
             get_coord(w.coords([player])[1]) + 1)
    if (south in WALLS['coordinates']) or (south[1] == y):
        return True
    else:
        return False


def wall_check_north():
    north = (get_coord(w.coords([player])[0]),
             get_coord(w.coords([player])[1]) - 1)
    if (north in WALLS['coordinates']) or (north[1] < 0):
        return True
    else:
        return False


def reset_keys():
    for i in enumerate(KEYS['coordinates']):
        w.itemconfig(f'oval{i[0]}', fill=KEYS['color'][0])


def all_keys_gathered():
    c = 0
    for i in enumerate(KEYS['coordinates']):
        if w.itemconfig(f'oval{i[0]}', 'fill')[-1] == KEYS['color'][1]:
            c += 1
        else:
            continue
    if len(KEYS['coordinates']) == c:
        return True
    else:
        return False


def restart():
    global score
    if (get_coord(w.coords([player])[0]), get_coord(w.coords([player])[1])) in LAVA['coordinates']:
        w.coords(player,
                 shrink(PLAYER_SPRITE['coordinates'][0][0]),
                 shrink(PLAYER_SPRITE['coordinates'][0][1]),
                 shrink((PLAYER_SPRITE['coordinates'][0][0] + 1), False),
                 shrink((PLAYER_SPRITE['coordinates'][0][1] + 1), False))
        score += LAVA['reward']
        print(score)
        reset_keys()

    if all_keys_gathered():
        if (get_coord(w.coords([player])[0]), get_coord(w.coords([player])[1])) in EXIT['coordinates']:
            w.coords(player,
                     shrink(PLAYER_SPRITE['coordinates'][0][0]),
                     shrink(PLAYER_SPRITE['coordinates'][0][1]),
                     shrink((PLAYER_SPRITE['coordinates'][0][0] + 1), False),
                     shrink((PLAYER_SPRITE['coordinates'][0][1] + 1), False))
            score += EXIT['reward']
            print(score)
            score = 0
            reset_keys()


def draw_walls(event):
    """ Draws a cell of wall """
    p = (event.x // CELL_SIZE, event.y // CELL_SIZE)
    WALLS['coordinates'].append(p)
    build_walls()


def draw_lava(event):
    """ Draws a cell of wall """
    p = (event.x // CELL_SIZE, event.y // CELL_SIZE)
    LAVA['coordinates'].append(p)
    build_lava()


def main():
    global player
    build_grid()
    build_walls()
    build_lava()
    put_keys()
    draw_guide()
    build_exit()
    player = create_player()
    master.bind("<Key>", move)
    master.bind("<Button-1>", draw_walls)
    master.bind("<Button-2>", draw_lava)
    w.pack()
    mainloop()


if __name__ == '__main__':
    main()
