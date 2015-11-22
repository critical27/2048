import copy
import random

class Matrix:
    def __init__(self,matrixSize):
        self.size = matrixSize

    def scanMatrix(self):
        empty = []
        for i in range(self.size):
            for j in range(self.size):
                if not self.matrix[i][j]:
                    empty.append((i,j))
        return empty

    def generateNum(self):
        empty = self.scanMatrix()
        index = random.choice(empty)
        self.matrix[index[0]][index[1]] = random.choice([2] * 9 + [4])

    def getNum(self,i,j):
        return self.matrix[i][j]

    def move(self,direction):
        curMatrix = copy.deepcopy(self.matrix)
        if direction == "Up":
            score = self.merge()
        elif direction == "Down":
            self.upsidedown()
            score = self.merge()
            self.upsidedown()
        elif direction == "Left":
            self.clockwise()
            score = self.merge()
            self.antiClockwise()
        elif direction == "Right":
            self.antiClockwise()
            score = self.merge()
            self.clockwise()
        newMatrix = copy.deepcopy(self.matrix)
        # 如果按下某一方向键后前后矩阵相同，维持不变，不生成新的数字
        if curMatrix == newMatrix:
            score = -1
        return score

    def merge(self):
        score = 0
        for j in range(self.size):
            column = []
            for i in range(self.size):
                if self.matrix[i][j]:
                    column.append(self.matrix[i][j])
            mergedColumn = []
            while(len(column)):
                if len(column) >= 2:
                    if column[0] == column[1]:
                        mergedColumn.append(column[0] * 2)
                        score += column[0] * 2
                        column.pop(0)
                        column.pop(0)
                    else:
                        mergedColumn.append(column[0])
                        column.pop(0)
                else:
                    mergedColumn.append(column[0])
                    column.pop(0)
            mergedColumn += [0] * (self.size - len(mergedColumn))
            for i in range(self.size):
                self.matrix[i][j] = mergedColumn[i]
        return score

    def upsidedown(self):
        if self.size % 2:
            upperBound = self.size // 2
        else:
            upperBound = self.size // 2 - 1
        for i in range(upperBound+1):
            for j in range(self.size):
                self.matrix[i][j], self.matrix[self.size-i-1][j]\
                = self.matrix[self.size-i-1][j], self.matrix[i][j]

    def clockwise(self):
        self.upsidedown()
        for i in range(self.size):
            for j in range(i+1):
                self.matrix[i][j], self.matrix[j][i]\
                = self.matrix[j][i], self.matrix[i][j]

    def antiClockwise(self):
        self.upsidedown()
        for i in range(self.size):
            for j in range(self.size-i):
                self.matrix[i][j], self.matrix[self.size-j-1][self.size-i-1]\
                = self.matrix[self.size-j-1][self.size-i-1], self.matrix[i][j]

    def isVacant(self):
        for i in range(self.size):
            if 0 in self.matrix[i]:
                return True
        return False

    def gameOver(self):
        if self.isVacant():
            return False
        for i in range(self.size):
            for j in range(self.size-1):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return False
                if self.matrix[j][i] == self.matrix[j+1][i]:
                    return False
        return True
