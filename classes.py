import pygame
from PIL import Image


class Figure:
    def __init__(self, color, name, n, moves=0):
        self.moves = moves
        self.n = n
        self.color = color
        self.name = name
        self.image = pygame.image.load(self.Resize())

    # Отрисовка фигуры
    def DrawFigure(self, display, x, y):
        self.x = x
        self.y = y
        self.topleft = (self.x * self.n // 8, self.y * self.n // 8)
        display.blit(self.image, self.topleft)

    # Подгонка фигур под размер дисплея
    def Resize(self):
        img = Image.open('Figures/' + self.color + self.name + '.png')
        img = img.resize((self.n // 8, self.n // 8))
        img.save('Figures/' + self.color + self.name + '1.png')
        return 'Figures/' + self.color + self.name + '1.png'


class Pawn(Figure):
    def BaseValue(self):
        return 1

    def AllMoves(self, x, y):
        CanMove = []
        if self.color == 'White':
            CanMove.append((x, y - 1))
            CanMove.append((x - 1, y - 1))
            CanMove.append((x + 1, y - 1))
            CanMove.append((x, y - 2))
        else:
            CanMove.append((x, y + 1))
            CanMove.append((x + 1, y + 1))
            CanMove.append((x - 1, y + 1))
            CanMove.append((x, y + 2))
        return CanMove


class King(Figure):
    def BaseValue(self):
        return 42

    def AllMoves(self, x, y):
        CanMove = [(x, y - 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1),
                   (x, y + 1), (x - 1, y + 1), (x - 1, y), (x - 1, y - 1)]
        return CanMove


class Knight(Figure):
    def BaseValue(self):
        return 3

    def AllMoves(self, x, y):
        CanMove = [(x + 1, y - 2), (x + 2, y - 1), (x + 2, y + 1),
                   (x + 1, y + 2),
                   (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1),
                   (x - 1, y - 2)]
        return CanMove


class Bishop(Figure):
    def BaseValue(self):
        return 3

    def AllMoves(self, x, y):
        CanMove = []
        for i in range(1, 8 - x):
            CanMove.append((x + i, y - i))
            CanMove.append((x + i, y + i))
        for i in range(1, x + 1):
            CanMove.append((x - i, y - i))
            CanMove.append((x - i, y + i))
        return CanMove


class Rook(Figure):
    def BaseValue(self):
        return 5

    def AllMoves(self, x, y):
        CanMove = []
        for i in range(8):
            if i != x:
                CanMove.append((i, y))
        for i in range(8):
            if i != y:
                CanMove.append((x, i))
        return CanMove


class Queen(Figure):
    def BaseValue(self):
        return 9

    def AllMoves(self, x, y):
        CanMove = []
        for i in range(1, 8 - x):
            CanMove.append((x + i, y - i))
            CanMove.append((x + i, y + i))
        for i in range(1, x + 1):
            CanMove.append((x - i, y - i))
            CanMove.append((x - i, y + i))
        for i in range(8):
            if i != x:
                CanMove.append((i, y))
        for i in range(8):
            if i != y:
                CanMove.append((x, i))
        return CanMove