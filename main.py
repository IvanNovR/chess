import pygame
import time
from classes import *
from PIL import Image


pygame.init()
Colors = ('White', 'Black')
Names = ('Pawn', 'Rook', 'Knight', 'Bishop', 'Queen', 'King')
Pieces = []
Desk = []
n = 720 # размер высоты и ширины окна
fps = 144
maxturns = 3 # Насколько ходов вперед искуственный интелект продумывает игру
AI = True # Искуственный интелект
ShowSettings = True # Показывать кто сейчас ходит
GameOn = True
CurrentTurn = Colors[0] # Кто ходит первым
display = pygame.display.set_mode((n, n))


def Mate(cd, b=[], c=0, r=0, t=[], iter=2, a=[]):
    for i in range(8):
        for j in range(8):
            if cd[i][j] != 0:
                if cd[i][j].name == 'King' and cd[i][j].color != CurrentTurn:
                    t = CheckMoves(cd, j, i)
                    for g in range(len(t)):
                        for k in range(8):
                            for l in range(8):
                                if cd[k][l] != 0:
                                    if cd[k][l].color == CurrentTurn:
                                        a.append(CheckMoves(cd, l, k))
                                        for f in range(len(a[-1])):
                                            if a[-1][f][0] == j and a[-1][f][1] == i or a[-1][f]==g:
                                                c += 1
                                                for q in range(8):
                                                    for w in range(8):
                                                        if cd[q][w] != 0:
                                                            if cd[q][w].color != CurrentTurn:
                                                                b.append(CheckMoves(cd, w, q))
                                                                for e in range(len(b[-1])):
                                                                    if b[-1][e][0] == l and b[-1][e][1] == k and iter!=1:
                                                                        cd[k][l] = cd[q][w]
                                                                        cd[q][w]= 0
                                                                        if Mate(cd, iter=1):
                                                                            return True
    if c == len(t)+1:
        return True
    else:
        return False


def Simulation(cd, turns=maxturns, copyfig=None, LastPlace=None, CurrentTurn='Black'): # симуляция возможных вариантов хода
    cd = tuple(cd)
    AllPosMoves = {}
    AfterMoveDecks = []
    AfterMoveValues = []
    for i in range(len(cd)):
        for j in range(len(cd)):
            if cd[i][j] != 0:
                if cd[i][j].color == CurrentTurn:
                    AllPosMoves[(j, i)] = CheckMoves(cd, j, i, copyfig, LastPlace)
                    if AllPosMoves[(j, i)] == []:
                        del AllPosMoves[(j, i)]
    for fig in AllPosMoves:
        for move in AllPosMoves[fig]:
            Desk1 = []
            for k in range(8):
                Desk1.append([])
                for m in range(8):
                    Desk1[k].append(cd[k][m])
            copyfig = Desk1[fig[1]][fig[0]]
            Desk1[fig[1]][fig[0]] = 0
            Desk1[move[1]][move[0]] = copyfig
            LastPlace = (fig[0], fig[1])
            if Desk1[move[1]][move[0]].name == 'King' and abs(move[0] - fig[0]) == 2:
                if move[0] == 2:
                    Desk1[fig[0]][3] = Desk1[fig[0]][0]
                    Desk1[fig[0]][0] = 0
                else:
                    Desk1[fig[0]][5] = Desk1[fig[0]][7]
                    Desk1[fig[0]][7] = 0
            if Desk1[move[1]][move[0]].name == 'Pawn' and move[1] == 0 and Desk1[move[1]][move[0]].color == 'White':
                Desk1[move[1]][move[0]] = Queen('White', 'Queen', n)
            if Desk1[move[1]][move[0]].name == 'Pawn' and move[1] == 7 and Desk1[move[1]][move[0]].color == 'Black':
                Desk1[move[1]][move[0]] = Queen('Black', 'Queen', n)
            AfterMoveDecks.append(tuple(Desk1))
            if turns != 1:
                if CurrentTurn == 'Black':
                    AfterMoveValues.append(Simulation(AfterMoveDecks[-1], turns - 1, copyfig, LastPlace, 'White'))
                else:
                    AfterMoveValues.append(Simulation(AfterMoveDecks[-1], turns - 1, copyfig, LastPlace, 'Black'))

    if turns == 1:
        for desk in AfterMoveDecks:
            AfterMoveValues.append(GetValue(desk))
    if turns != maxturns:  # Максимальное кол-во
        if turns % 2 == maxturns % 2:
            return max(AfterMoveValues)
        else:
            return min(AfterMoveValues)

    if turns == maxturns:
        return AfterMoveDecks[AfterMoveValues.index(max(AfterMoveValues))]


def GetValue(cd, bv=1, wv=1, KnK=0.01, BsK=0.01, QwK=0.1, PwK=0.05, KgK=0.02, RoK=0.02): # считывает позиции на доске
    for i in range(8):
        for j in range(8):
            if cd[i][j] != 0:
                if cd[i][j].name == 'Knight':
                    DefendAndAttack = 0
                    Value = cd[i][j].BaseValue() + (KnK / abs(i - 3.5) / abs(j - 3.5))

                elif cd[i][j].name == 'Bishop':
                    Same = 0
                    for k in range(8):
                        for l in range(8):
                            if cd[k][l] != 0:
                                if cd[k][l].color == cd[i][j].color:
                                    Same += 1

                    Value = cd[i][j].BaseValue() + (BsK * (32 - Same))
                    Value += BsK * 20 / abs(i - 3.5)
                elif cd[i][j].name == 'Pawn':
                    DefendAndAttack = 0
                    if j != 7:
                        if cd[i + 1][j + 1] != 0:
                            DefendAndAttack += 1
                        if cd[i - 1][j + 1] != 0:
                            DefendAndAttack += 1
                    if j != 0:
                        if cd[i + 1][j - 1] != 0:
                            DefendAndAttack += 1
                        if cd[i - 1][j - 1] != 0:
                            DefendAndAttack += 1
                    Value = cd[i][j].BaseValue() + (PwK * DefendAndAttack / 1.5)
                    if (j == 3 or j == 4) and (i == 3 or i == 4):
                        Value += PwK * 10
                elif cd[i][j].name == 'Queen':
                    Value = cd[i][j].BaseValue() + QwK
                elif cd[i][j].name == 'Rook':
                    asc = 0
                    for k in range(8):
                        if cd[k][j] == 0:
                            asc += 1
                    for l in range(8):
                        if cd[i][l] == 0:
                            asc += 1
                    Value = cd[i][j].BaseValue() + RoK * asc
                elif cd[i][j].name == 'King':
                    Pawns = 0
                    for fig in cd[i][j].AllMoves(j, i):
                        if fig[0] <= 7 and fig[0] >= 0 and fig[1] <= 7 and fig[1] >= 0:
                            if cd[fig[1]][fig[0]] != 0:
                                if cd[fig[1]][fig[0]].name == 'Pawn':
                                    Pawns += 1
                    Value = cd[i][j].BaseValue() + (KgK * Pawns)
                    Value += KgK * abs(6 - j)
                    Value += KgK * abs(1 - j)

                if cd[i][j].color == 'Black':
                    bv += Value
                elif cd[i][j].color == 'White':
                    wv += Value
    delta = bv / wv
    return delta


def CheckMoves(cd, x, y, copyfig=None, LastPlace=None): # проверка возможности хода
    CurrentMoves = cd[y][x].AllMoves(x, y)
    g = 0

    while g < len(CurrentMoves):
        a = CurrentMoves[g]
        # Проверка, что ход не ведёт за пределы доски
        if CurrentMoves[g][0] > 7 or CurrentMoves[g][0] < 0 or CurrentMoves[g][1] > 7 or CurrentMoves[g][1] < 0:
            del CurrentMoves[g]
            continue
        # Проверка, что поля для хода не перекрыты фигурами
        if cd[CurrentMoves[g][1]][CurrentMoves[g][0]] != 0:
            if cd[CurrentMoves[g][1]][CurrentMoves[g][0]].color == cd[y][x].color:
                del CurrentMoves[g]
                continue
        try:
            if cd[y][x].name == 'Pawn':
                if cd[CurrentMoves[g][1]][CurrentMoves[g][0]] == 0 and CurrentMoves[g][0] != x or \
                        cd[CurrentMoves[g][1]][CurrentMoves[g][0]] != 0 and CurrentMoves[g][0] == x:
                    del CurrentMoves[g]
                    continue
                if cd[y][x].moves != 0 and abs(CurrentMoves[g][1] - y) == 2 or len(CurrentMoves) == 1 and abs(
                        CurrentMoves[0][1] - y) == 2:
                    del CurrentMoves[g]
                    continue

            if cd[y][x].name == 'Rook' or cd[y][x].name == 'Queen':
                if CurrentMoves[g][0] > x and CurrentMoves[g][1] == y:
                    for i in range(x + 1, CurrentMoves[g][0]):
                        if cd[CurrentMoves[g][1]][i] != 0:
                            del CurrentMoves[g]
                            break
                elif CurrentMoves[g][0] < x and CurrentMoves[g][1] == y:
                    for i in range(CurrentMoves[g][0] + 1, x):
                        if cd[CurrentMoves[g][1]][i] != 0:
                            del CurrentMoves[g]
                            break
                elif CurrentMoves[g][1] > y and CurrentMoves[g][0] == x:
                    for i in range(y + 1, CurrentMoves[g][1]):
                        if cd[i][CurrentMoves[g][0]] != 0:
                            del CurrentMoves[g]
                            break
                elif CurrentMoves[g][1] < y and CurrentMoves[g][0] == x:
                    for i in range(CurrentMoves[g][1] + 1, y):
                        if cd[i][CurrentMoves[g][0]] != 0:
                            del CurrentMoves[g]
                            break
            if a != CurrentMoves[g]:
                continue
            if cd[y][x].name == 'Bishop' or cd[y][x].name == 'Queen':
                if CurrentMoves[g][0] > x and CurrentMoves[g][1] > y:
                    j = y + 1
                    for i in range(x + 1, CurrentMoves[g][0]):
                        if cd[j][i] != 0:
                            del CurrentMoves[g]
                            break
                        j += 1
                elif CurrentMoves[g][0] < x and CurrentMoves[g][1] > y:
                    j = x - 1
                    for i in range(y + 1, CurrentMoves[g][1]):
                        if cd[i][j] != 0:
                            del CurrentMoves[g]
                            break
                        j -= 1
                elif CurrentMoves[g][1] < y and CurrentMoves[g][0] > x:
                    j = y - 1
                    for i in range(x + 1, CurrentMoves[g][0]):
                        if cd[j][i] != 0:
                            del CurrentMoves[g]
                            break
                        j -= 1
                elif CurrentMoves[g][1] < y and CurrentMoves[g][0] < x:
                    j = CurrentMoves[g][0] + 1
                    for i in range(CurrentMoves[g][1] + 1, y):
                        if cd[i][j] != 0:
                            del CurrentMoves[g]
                            break
                        j += 1
            try:
                if a == CurrentMoves[g]:
                    g += 1
            except:
                g = 0
        except:
            g = 0
    # Рокировка
    if cd[y][x].name == 'King' and cd[y][x].moves == 0:
        if cd[y][0] != 0:
            if cd[y][0].name == 'Rook' and cd[y][0].moves == 0 and cd[y][1] == 0 and cd[y][2] == 0 and cd[y][
                3] == 0:
                CurrentMoves.append((2, y))
        if cd[y][7] != 0:
            if cd[y][7].name == 'Rook' and cd[y][7].moves == 0 and cd[y][6] == 0 and cd[y][5] == 0:
                CurrentMoves.append((6, y))
    return CurrentMoves


def moving(i, j, CurrentTurn): # перемещение фигуры
    global Desk
    global LastPlace
    global copyfig
    PossibleMoves = CheckMoves(Desk, i, j)
    draw(True, PossibleMoves, i, j)
    while True:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                return CurrentTurn
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                YNEW = 8 * event.pos[1] // n
                XNEW = 8 * event.pos[0] // n
                if (XNEW, YNEW) in PossibleMoves or (XNEW, YNEW, '0') in PossibleMoves or (
                        XNEW, YNEW, '1') in PossibleMoves:
                    Desk[j][i].moves += 1
                    copyfig = Desk[j][i]
                    Desk[j][i] = 0
                    Desk[YNEW][XNEW] = copyfig
                    LastPlace = (i, j)
                    if Desk[YNEW][XNEW].name == 'King' and abs(XNEW - i) == 2:
                        if XNEW == 2:
                            Desk[YNEW][3] = Desk[YNEW][0]
                            Desk[YNEW][0] = 0
                        else:
                            Desk[YNEW][5] = Desk[YNEW][7]
                            Desk[YNEW][7] = 0
                        if (XNEW, YNEW, '0') in PossibleMoves:
                            Desk[YNEW + 1][XNEW] = 0
                        if (XNEW, YNEW, '1') in PossibleMoves:
                            Desk[YNEW - 1][XNEW] = 0
                    elif copyfig.name == 'Pawn' and YNEW == 0 and copyfig.color == 'White':
                        Desk[YNEW][XNEW] = Queen('White', 'Queen', n)
                    elif copyfig.name == 'Pawn' and YNEW == 7 and copyfig.color == 'Black':
                        Desk[YNEW][XNEW] = Queen('Black', 'Queen', n)
                    if CurrentTurn == 'Black':
                        return 'White'
                    else:
                        return 'Black'


def draw(moving=False, PossibleMoves=None, x=None, y=None):
    display.blit(Background, (0, 0))
    if moving == True:
        display.blit(Chosen, (x * n // 8, y * n // 8))
    for i in range(8):
        for j in range(8):
            if Desk[i][j] != 0:
                Desk[i][j].DrawFigure(display, j, i)
    if moving == True:
        for i in PossibleMoves:
            display.blit(MoveDot, (i[0] * n // 8, i[1] * n // 8))
    if ShowSettings:
        setting_show()
    pygame.display.update()


def setting_show():
    font = pygame.font.Font('SF-UI-Text-Regular.ttf', 15)
    color = (0, 0, 0)
    colorBox = (255, 255, 255)
    pygame.draw.rect(display, colorBox, (0, 0, 150, 20))
    text = font.render('Сейчас ходят ' + CurrentTurn, True, color)
    display.blit(text, (0, 0))

# Подгонка доски и маркеров под размер дисплея
Background = Image.open('Figures/Desk1.png')
Background = Background.resize((n, n))
Background.save('Figures/Desk11.png')
Background = pygame.image.load('Figures/Desk11.png')

Chosen = Image.open('Figures/Chosen.png')
Chosen = Chosen.resize((n // 8, n // 8))
Chosen.save('Figures/Chosen1.png')
Chosen = pygame.image.load('Figures/Chosen1.png')

MoveDot = Image.open('Figures/CanMove.png')
MoveDot = MoveDot.resize((n // 8, n // 8))
MoveDot.save('Figures/CanMove1.png')
MoveDot = pygame.image.load('Figures/CanMove1.png')

# Создание массива со всеми возможными фигурами
for i in Colors:
    for j in Names:
        if j == 'Pawn':
            for k in range(8):
                Pieces.append(Pawn(i, j, n))
        elif j == 'Rook':
            Pieces.append(Rook(i, j, n))
            Pieces.append(Rook(i, j, n))
        elif j == 'Bishop':
            Pieces.append(Bishop(i, j, n))
            Pieces.append(Bishop(i, j, n))
        elif j == 'Knight':
            Pieces.append(Knight(i, j, n))
            Pieces.append(Knight(i, j, n))
        elif j == 'King':
            Pieces.append(King(i, j, n))
        elif j == 'Queen':
            Pieces.append(Queen(i, j, n))

# Изначальная расстановка фигур на доске
for i in range(8):
    Desk.append([])
    for j in range(8):
        if i == 0 and j < 3:
            Desk[i].append(Pieces[24 + j * 2])
        elif i == 0 and j == 3:
            Desk[i].append(Pieces[-2])
        elif i == 0 and j == 4:
            Desk[i].append(Pieces[-1])
        elif i == 0:
            Desk[i].append(Pieces[-2 * j + 7])
        elif i == 1:
            Desk[i].append(Pieces[j + 16])
        elif i == 6:
            Desk[i].append(Pieces[j])
        elif i == 7 and j < 3:
            Desk[i].append(Pieces[8 + j * 2])
        elif i == 7 and j == 3:
            Desk[i].append(Pieces[14])
        elif i == 7 and j == 4:
            Desk[i].append(Pieces[15])
        elif i == 7:
            Desk[i].append(Pieces[-2 * j + 23])

        else:
            Desk[i].append(0)
draw()


while GameOn:
    pygame.time.delay(round(1000 / fps))
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        # При нажатии ЛКМ проверяется, находится ли на этой клетке фигура
        # Если да, и сейчас ходят фигуры этого цвета, то можно совершить ход
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            y = 8 * event.pos[1] // n
            x = 8 * event.pos[0] // n
            if Desk[y][x] != 0:
                if CurrentTurn == Desk[y][x].color:
                    CurrentTurn = moving(x, y, CurrentTurn)
                    draw()
            if Mate(Desk):
                print('Вы выиграли')
            #else:
            #    print('Ы')
    if CurrentTurn == 'Black' and AI:
        a = time.time()
        Desk = Simulation(tuple(Desk))
        CurrentTurn = 'White'
        print('Затрачено времени на ход ', time.time() - a)
        print('Дельта ', GetValue(Desk))
        for i in range(2, 5):
            for j in range(8):
                if Desk[i][j] != 0:
                    Desk[i][j].moves = Desk[i][j].moves + 1 if Desk[i][j].name == 'Pawn' else Desk[i][j].moves + 0
        draw()
        if Mate(Desk):
            print('Вы проиграли')
        #else:
        #    print('Ы')
    if keys[pygame.K_ESCAPE] or event.type == pygame.QUIT:
        GameOn = False

pygame.quit()
