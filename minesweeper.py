import random, time, sys, os, keyboard

global row, column, mine_count, victory_count, mine, room, mine_exploded, percentage, location, flag_count, win

row: int = 10
column: int = 10
percentage: float = 0.2
victory_count: int = 0
flag_count: int = 0
mine_count: int = 0
location: list[int] = [0,0]
win: bool = False
assistant: bool = False
known: bool = False
try:
    for i in range(len(sys.argv)):
        if known:
            known = False
            continue
        if sys.argv[i] == "--row":
            row = int(sys.argv[i+1])
            known = True
        if sys.argv[i] == "--column":
            column = int(sys.argv[i+1])
            known = True
        if sys.argv[i] == "--percentage":
            percentage = float(sys.argv[i+1]) / 100
            known = True
        if sys.argv[i] == "--assistant":
            assistant = True
except:
    print("매개변수 오류")
    exit()
del known

if percentage >= 1 or percentage < 0:
    print("확률은 0% 이상 100% 미만이어야 합니다.")
    exit()


mine: list[bool] =[[False for x in range(0,column)] for y in range(0,row)]
room: list[int|str] =[[" " for x in range(0,column)] for y in range(0,row)]


def clear():
    os.system('cls' if os.name=="nt" else "clear")


def create_mine():
    global mine_count
    for i in range(0, row):
        for j in range(0, column):
            random.seed()
            if random.random() <= percentage:
                mine[i][j] = True
                mine_count += 1
    if mine_count == row * column:
        mine[random.randrange(0,row)][random.randrange(0,column)]  = False
        mine_count -= 1
    elif mine_count == 0:
        mine[random.randrange(0,row)][random.randrange(0,column)]  = True
        mine_count += 1


def find_mine(x: int, y: int) -> bool:
    if x < 0 or y < 0:
        return False
    if mine[x][y]:
        room[x][y] = "X"
        return True
    if room[x][y] != " ":
        return False
    room[x][y] = 0
    for i in [x-1, x, x+1]:
        if i < 0 or i > row - 1:
            continue
        for j in [y-1, y, y+1]:
            if j < 0 or j > column - 1:
                continue
            if mine[i][j]:
                room[x][y] += 1
    if room[x][y] == 0:
        for i in [x-1, x, x+1]:
            if i < 0 or i > row - 1:
                continue
            for j in [y-1, y, y+1]:
                if j < 0 or j > column - 1:
                    continue
                elif i == x and j == y:
                    continue
                else:
                    find_additional_mine(i,j)
    return False


def find_additional_mine(x: int, y: int):
    if mine[x][y]:
        return
    elif room[x][y] != " ":
        return 
    else:
        room[x][y] = 0
        for i in [x-1, x, x+1]:
            if i < 0 or i > row - 1:
                continue
            for j in [y-1, y, y+1]:
                if j < 0 or j > column - 1:
                    continue
                if mine[i][j]:
                    room[x][y] += 1
        if room[x][y] == 0:
            for i in [x-1, x, x+1]:
                if i < 0 or i > row - 1:
                    continue
                for j in [y-1, y, y+1]:
                    if j < 0 or j > column - 1:
                        continue
                    elif i == x and j == y:
                        continue
                    else:
                        find_additional_mine(i,j)


def check_flag(x: int, y: int):
    global victory_count, flag_count, win
    if room[x][y] != "!" and room[x][y] != " ":
        return
    if room[x][y] == "!":
        room[x][y] = " "
        if mine[x][y]:
            victory_count -= 1
        flag_count -= 1
    elif room[x][y] == " ":
        room[x][y] = "!"
        if mine[x][y]:
            victory_count += 1
        flag_count += 1
    if victory_count == mine_count and flag_count == victory_count:
        win = True

def move(arg: str):
    if arg == 'left':
        if location[0] > 0:
            location[0] -= 1
        else:
            location[0] = row - 1
    if arg == 'right':
        if location[0] < row - 1:
            location[0] += 1
        else:
            location[0] = 0
    if arg == "up":
        if location[1] > 0:
            location[1] -= 1
        else:
            location[1] = column - 1
    if arg == "down":
        if location[1] < column - 1:
            location[1] += 1
        else:
            location[1] = 0


def assis():
    try_assistant = True
    loop_count = 0
    while try_assistant:
        if loop_count > row * column * 10:
            try_assistant = False
            break
        starting_x: int = random.randrange(0, row)
        starting_y: int = random.randrange(0, column)
        if mine[starting_x][starting_y]:
            continue
        check: int = 0
        for i in [starting_x-1, starting_x, starting_x+1]:
            if i < 0 or i > row -1:
                continue
            for j in [starting_y-1, starting_y, starting_y+1]:
                if j < 0 or j > column -1:
                    continue
                if mine[i][j]:
                    check += 1
        if check == 0:
            room[starting_x][starting_y] = "0"
            for i in [starting_x-1, starting_x, starting_x+1]:
                if i < 0 or i > row - 1:
                    continue
                for j in [starting_y-1, starting_y, starting_y+1]:
                    if j < 0 or j > column - 1:
                        continue
                    elif i == starting_x and j == starting_y:
                        continue
                    else:
                        find_additional_mine(i,j)
                        try_assistant = False
        loop_count += 1


def reset_map():
    for i in range(row):
        for j in range(column):
            room[i][j] = " "


create_mine()
mine_exploded: bool = False
if assistant:
    assis()
while True:
    clear()
    print("%d개의 지뢰가 있습니다." % mine_count)
    print("깃발의 갯수: %d" % flag_count)
    for i in range(0, column):
        for j in range(0, row):
            print("[%s]" % ("A" if location[0] == j and location[1] == i and room[j][i] != "X" and not win else str(room[j][i])), end="")
        print("")
    if win:
        print("지뢰를 모두 찾아내셨습니다!")
        exit()

    if mine_exploded:
        print("지뢰가 터졌습니다.")
        print("같은 맵으로 다시 하시려면 y를 눌러주세요. 종료하시려면 Enter를 눌러주세요.")
        key = None
        while key == None:
            key = keyboard.read_key()
            if key == 'y':
                reset_map()
                if assistant:
                    assis()
                mine_exploded = False
            elif key == 'enter':
                clear()
                print('안녕히가세요!')
                exit()
        continue
    print("방향키로 이동, f로 조사, c로 깃발 꽂기, ESC로 종료.")
    key = None
    while key == None:
        key = keyboard.read_key()
        if key == 'up' or key == 'down' or key == 'left' or key == 'right':
            move(key)
        if key == 'f':
            if find_mine(location[0], location[1]):
                mine_exploded = True
        if key == 'c':
            check_flag(location[0], location[1])
            time.sleep(0.1)
        if key == 'esc':
            clear()
            print("\n안녕히가세요!")
            exit()
        time.sleep(0.1)
