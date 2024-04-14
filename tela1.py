from tkinter import *
import random
import sys


# Dimens
lado = 20
q_largura = 10
q_altura = 20
largura = lado*q_largura
altura = lado*q_altura


def random_peca():
    return random.randint(1, 7)


class Peca:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        # self.grade[][]
        # self.size
        if (type == 1):
            # Dentro tem Colunas e fora tem as Linhas = Ao todo, 3 colunas e 3 linhas.
           self.grade = [[0,0,0],[type,type,0],[0,type,type]]
           self.size = 3
            # para diferenciar a grade de 3x3 e a de 4x4 (aquela quadrada).
        elif (type == 2):
            self.grade = [[0,0,0],[0,type,type],[type,type,0]]
            self.size  = 3
        elif (type == 3):
            self.grade = [[0,0,0],[0,type,type],[0,type,type]]
            self.size  = 3
        elif(type == 4):
            self.grade = [[0,0,0],[0,0,type],[type,type,type]]
            self.size  = 3
        elif(type == 5):
            self.grade = [[0,0,0],[type,0,0],[type,type,type]]
            self.size  = 3
        elif(type == 6):
            self.grade = [[0,0,0],[0,type,0],[type,type,type]]
            self.size  = 3
        elif(type == 7):
            self.grade = [[0,type,0,0],[0,type,0,0],[0,type,0,0],[0,type,0,0]]
            self.size  = 4

    def vira(self, Tela):
        copia = [[0 for i in range(self.size)] for j in range(self.size)]

        # Fez a copia girando a peça
        for lin in range(self.size):
            for col in range(self.size):
                copia[self.size-1-col][lin] = self.grade[lin][col]

        # Verifica se a copia colide com algo
        for lin in range(self.size):
            for col in range(self.size):
                if copia[lin][col] != 0 and (self.y+lin) >= q_altura:
                    return 0
                    # y+1 pois está abaixo
                # diferente de zero, ou seja, tiver alguma coisa
                elif copia[lin][col] != 0 and Tela.grade[self.y+lin][self.x+col] != 0:
                    return 0

        # Copiar a copia para o self.grade
        for lin in range(self.size):
            for col in range(self.size):
                self.grade[lin][col] = copia[lin][col]
        return 1  # consegui girar a peça

    # Verificar se há algo embaixo da peça

    def desce(self, Tela):
        for i in range(self.size):
            for j in range(self.size):
                # print(self.y+i+1)
                if self.grade[i][j] != 0 and (self.y+1+i) >= q_altura:
                    return 0
                    # y+1 pois está abaixo
                if self.grade[i][j] != 0 and Tela.grade[self.y+i+1][self.x+j] != 0:
                    return 0

        self.y = self.y + 1
        return 1  # a peça pode descer

    def direita(self, Tela):
        for i in range(self.size):
            for j in range(self.size):
                if self.grade[i][j] != 0 and (self.x+1+j) > q_largura - 1:
                    return 0
                    # y+1 pois está abaixo
                if Tela.grade[self.y][self.x+1]*self.grade[i][j] != 0:
                    return 0
        self.x = self.x + 1
        return 1

    def esquerda(self, Tela):
        for i in range(self.size):
            for j in range(self.size):
                if self.grade[i][j] != 0 and (self.x-1+j) < 0:
                    return 0
                if Tela.grade[self.y][self.x-1]*self.grade[i][j] != 0:
                    return 0
        self.x = self.x - 1
        return 1


class Tela:
    def __init__(self):
        self.grade = [[0 for i in range(q_largura)]
                      for j in range(q_altura)]  # vetor

    def elimina(self):
        l_elimina = []

        for lin in range(q_altura-1, -1, -1):
            for col in range(q_largura):
                if (self.grade[lin][col] == 0):
                    break
                if col == q_largura-1:
                    l_elimina.append(lin)
        return l_elimina

    def desce_linhas(self, l_elimina):
        for i in l_elimina:
            for lin in range(i, 0, -1):
                for col in range(q_largura):
                    self.grade[lin][col] = self.grade[lin-1][col]
            for j in range(len(l_elimina)):
                l_elimina[j] += 1
  
            '''for j in range(len(l_elimina)):
                l_elimina[j] += 1'''

            for col in range(q_largura):
                self.grade[0][col] = 0

    def add_pecas(self, p):
        for lin in range(p.size):  # for i
            for col in range(p.size):  # for j
                if p.grade[lin][col] != 0:
                    #print('linha:', lin+p.y, ' | col:', col+p.x)
                    self.grade[lin+p.y][col+p.x] = p.grade[lin][col]

    


class Game:
    def __init__(self):
        self.window = Tk()
        self.canvas = Canvas(self.window, width=largura,
                             height=altura, bg='black')
        self.canvas.pack()
        self.p = Peca(3, 1, random_peca())  # (random.randint(1, 7))(3, 1, 1)
        self.nump = 0
        self.t = Tela()

        self.window.bind('<Right>', self.move_direita)
        self.window.bind('<Left>', self.move_esquerda)
        self.window.bind('<Up>', self.gira)

    def gira(self, event):
        self.p.vira(self.t)

    def move_direita(self, event):
        self.p.direita(self.t)

    def move_esquerda(self, event):
        self.p.esquerda(self.t)

    # COLOR
    def meDeACor(self, type):
        if (type == 1):
            collor = 'blue'
        elif (type == 2):
            collor = 'yellow'
        elif (type == 3):
            collor = 'red'
        elif (type == 4):
            collor = 'orange'
        elif (type == 5):
            collor = 'green'
        elif (type == 6):
            collor = 'purple'
        elif (type == 7):
            collor = 'white'

        return collor
    

    def desenha(self):  # desenha peça
        for i in range(self.p.size):  #desenha peÃ§a
            for j in range(self.p.size):
                if self.p.grade[i][j] != 0:
                    self.canvas.create_polygon([(self.p.x+j)*lado+2, (self.p.y+i)*lado+2, (self.p.x+j)*lado+lado-2, (self.p.y+i)*lado+2,
                                                (self.p.x+j)*lado+lado-2, (self.p.y+i)*lado+lado-2, (self.p.x+j)*lado+2, (self.p.y+i)*lado+lado-2],
                                                fill=self.meDeACor(self.p.type))

        # Desenha tabuleiro
        for lin in range(q_altura):
            for col in range(q_largura):
                if self.t.grade[lin][col] != 0:
                    self.canvas.create_polygon([col*lado+2, lin*lado+2,
                                                col*lado+lado-2, lin*lado+2, col*lado+lado-2,
                                                lin*lado+lado-2, col*lado+2, lin*lado+lado-2],
                                                fill=self.meDeACor(self.t.grade[lin][col]))

    def run(self):
        time = 0

        while (True):
            self.canvas.delete('all')

            if time == 5:
                desceu = self.p.desce(self.t)
                time = 0
                if desceu == 0:
                    self.t.add_pecas(self.p)

                    l_elimina = self.t.elimina()
                    if (len(l_elimina) > 0):
                        self.t.desce_linhas(l_elimina)
                    self.p = Peca(3, 1, random_peca())

                    # CONDIÇÃO DE MORTE
                    for lin in range(self.p.size):
                        for col in range(self.p.size):
                            if self.p.grade[lin][col] != 0 and self.t.grade[self.p.y+lin][self.p.x+col] != 0:
                                print('Game Over')
                                sys.exit() # sys.exit is considered good to use in production code. This is because the sys module will always be there.
                                #quit()
            else:
                time += 1

            self.desenha()
            self.canvas.after(50)
            self.window.update_idletasks()
            self.window.update()


g = Game()
g.run()
