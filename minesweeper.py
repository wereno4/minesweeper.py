import random, time, sys, os

global row, column, mine_count, victory_count

row: int = 0
column: int = 0
victory_count: int = 0

if len(sys.argv) == 1:
    row = 10
    column = 10
else:
    row, column = map(int, sys.argv[1:3])

mine: list[bool] =[[False for x in range(0,row)] for y in range(0,column)]
room: list[int|str] =[[" " for x in range(0,row)] for y in range(0,column)]
mine_count: int = 0


def clear():
    os.system('cls' if os.name=="nt" else "clear")


def create_mine():
    global mine_count
    for i in range(0, row):
        for j in range(0, column):
            random.seed()
            if random.random() <= 0.2:
                mine[i][j] = True
                mine_count += 1


def find_mine(x: int, y: int) -> bool:
    if mine[x][y]:
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
    global victory_count
    if room[x][y] == "!":
        room[x][y] = " "
        if mine[x][y]:
            victory_count -= 1
    elif room[x][y] == " ":
        room[x][y] = "!"
        if mine[x][y]:
            victory_count += 1


create_mine()
while True:
    clear()
    print("%d개의 지뢰가 있습니다." % mine_count)
    for i in range(0, column):
        for j in range(0, row):
            print("[%s]" % str(room[j][i]), end="")
        print("")

    if victory_count == mine_count:
        print("지뢰를 모두 찾아내셨습니다!")
        exit()

    x, y = map(int, input("행동할 칸의 좌표를 입력하세요\nex.)1,1\n").split(",",1))
    action: str = input("조사할까요?(F) 아니면 깃발을 꽂을까요?(C)")[0]
    if action == "F" or action == "f":
        if find_mine(x-1, y-1):
            print("지뢰가 터졌습니다.")
            exit()
    if action == "C" or action == "c":
        check_flag(x-1, y-1)
