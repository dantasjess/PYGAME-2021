import pygame
import pygame.locals
from random import randrange

print("Módulos importados com sucesso")

try:
    pygame.init()
    print("Pygame inicializado")
except:
    print("Alguma coisa deu erro")

largura = 640
altura = 480
tamanho = 20
placar = 40
branco = (255, 255, 255)
dourado = (255,215,0)
dourado2 = (255,236,139)
dourado3 = (205,173,0)
dourado4 = (218,165,32)
dourado5 = (255,248,220)

frames = pygame.time.Clock()
fundo = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("The Gold")



class Texto:
    def __init__(self, msg, cor, tam):
        self.font = pygame.font.SysFont(None, tam)
        self.texto = self.font.render(msg, True, cor)
    def mostrar(self, x, y):
        fundo.blit(self.texto, [x, y])


class OURO_CONSEGUIDO:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inicio= [x, y]
        self.comp = 1
        self.fila = [self.inicio]
        self.direcao = ""
    def movimento(self, x, y):
        self.inicio = [x, y]
        self.fila.append([x, y])
    def cresce(self):
        self.comp += 1
    def mostrar(self):
        indice = 0
        for XY in self.fila:
            if indice == len(self.fila) - 1:
                pygame.draw.rect(fundo, dourado4, [XY[0], XY[1], tamanho, tamanho])
            else:
                pygame.draw.rect(fundo, dourado4, [XY[0], XY[1], tamanho, tamanho])
            indice += 1
    def rastro(self):
        if len(self.fila) > self.comp:
            del self.fila[0]
    def parou(self):
        if any(Bloco == self.inicio for Bloco in self.fila[:-1]):
            return True
        return False
    def reinicia(self, x, y):
        self.x = x
        self.y = y
        self.inicio = [x, y]
        self.comp = 1
        self.fila = [self.inicio]



class Ouro:
    def __init__(self):
        self.x = randrange(0, largura - tamanho, 20)
        self.y = randrange(0, altura - tamanho - placar, 20)


    def mostrar(self):
        pygame.draw.rect(fundo, dourado4, [self.x, self.y, tamanho, tamanho])


    def reposicionar(self):
        self.x = randrange(0, largura - tamanho, 20)
        self.y = randrange(0, altura - tamanho - placar, 20)



# noinspection DuplicatedCode
class Jogo:
    def __init__(self):
        self.jogando = False
        self.perdeu = False
        self.noMenu = True
        self.modo = None

        self.fundo = dourado5

        self.pos_x = randrange(0, largura - tamanho, 20)
        self.pos_y = randrange(0, altura - tamanho - placar, 20)

        self.velocidade_x = 0
        self.velocidade_y = 0

        self.pontuacao = 0

        self.fila = OURO_CONSEGUIDO(self.pos_x, self.pos_y)
        self.ouro = Ouro()


    def play(self):
        pontuacao_fundo = 0
        while self.jogando:


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.jogando = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.fila.direcao != "direita":
                        self.fila.direcao = "esquerda"
                    if event.key == pygame.K_RIGHT and self.fila.direcao != "esquerda":
                        self.fila.direcao = "direita"
                    if event.key == pygame.K_UP and self.fila.direcao != "baixo":
                        self.fila.direcao = "cima"
                    if event.key == pygame.K_DOWN and self.fila.direcao != "cima":
                        self.fila.direcao = "baixo"

            if self.jogando:
                fundo.fill(self.fundo)
                if self.fila.direcao == "cima":
                    self.pos_y -= tamanho
                elif self.fila.direcao == "baixo":
                    self.pos_y += tamanho
                elif self.fila.direcao == "esquerda":
                    self.pos_x -= tamanho
                elif self.fila.direcao == "direita":
                    self.pos_x += tamanho
                else:
                    pass

                if self.pos_x == self.ouro.x and self.pos_y == self.ouro.y:
                    self.ouro.reposicionar()
                    self.fila.cresce()
                    self.pontuacao += 1
                    pontuacao_fundo += 1

                if self.modo == "livre":
                    if self.pos_x + tamanho > largura:
                        self.pos_x = 0
                    if self.pos_x < 0:
                        self.pos_x = largura - tamanho
                    if self.pos_y + tamanho > altura - placar:
                        self.pos_y = 0
                    if self.pos_y < 0:
                        self.pos_y = altura - tamanho - placar
                else:
                    pygame.draw.rect(fundo, branco, [0, 0, 2, altura])
                    pygame.draw.rect(fundo, branco, [0, 0, largura, 2])
                    pygame.draw.rect(fundo, branco, [largura - 2, 0, 2, altura])
                    pygame.draw.rect(fundo, branco, [0, altura - placar - 2, largura, 2])
                    if self.pos_x + tamanho > largura:
                        self.jogando = False
                        self.perdeu = True
                        self.lost()
                    if self.pos_x < 0:
                        self.jogando = False
                        self.perdeu = True
                        self.lost()
                    if self.pos_y + tamanho > altura - placar:
                        self.jogando = False
                        self.perdeu = True
                        self.lost()
                    if self.pos_y < 0:
                        self.jogando = False
                        self.perdeu = True
                        self.lost()
                self.fila.movimento(self.pos_x, self.pos_y)
                self.fila.rastro()

                if self.fila.parou():
                    self.jogando = False
                    self.perdeu = True
                    self.lost()
                self.fila.mostrar()

                pygame.draw.rect(fundo, branco, [0, altura - placar, largura, placar])
                textoPlacarS = Texto("Score:" + str(self.pontuacao), dourado2, 25)
                textoPlacarS.mostrar(9, altura - 31)

                self.ouro.mostrar()
                pygame.display.update()
                frames.tick(15)


    def lost(self):
        while self.perdeu:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.jogando = False
                    self.perdeu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.jogando = False
                        self.perdeu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_x = mouse_pos[0]
                    mouse_y = mouse_pos[1]
                    if 143 < mouse_x < 143 + 369 and 168 < mouse_y < 168 + 51:
                        self.jogando = False
                        self.perdeu = False
                        self.noMenu = True
                        self.pos_x = randrange(0, largura - tamanho, 20)
                        self.pos_y = randrange(0, altura - tamanho - placar, 20)
                        self.fila.direcao = ""
                        self.ouro.reposicionar()
                        self.fila.reinicia(self.pos_x, self.pos_y)
                        self.velocidade_x = 0
                        self.velocidade_y = 0
                        self.pontuacao = 0
                    if 193 < mouse_x < 193 + 279 and 268 < mouse_y < 268 + 58:
                        self.jogando = True
                        self.perdeu = False
                        self.pos_x = randrange(0, largura - tamanho, 20)
                        self.pos_y = randrange(0, altura - tamanho - placar, 20)
                        self.fila.direcao = ""
                        self.ouro.reposicionar()
                        self.fila.reinicia(self.pos_x, self.pos_y)
                        self.velocidade_x = 0
                        self.velocidade_y = 0
                        self.pontuacao = 0

            fundo.fill(dourado2)

            textoLostS = Texto("You Missed Out", dourado3, 80)
            textoLostS.mostrar(139, 29)
            textoLost = Texto("You Missed Out", dourado, 80)
            textoLost.mostrar(140, 30)

            textoPontuacaoS = Texto("Final Score: " + str(self.pontuacao), dourado3, 50)
            textoPontuacaoS.mostrar(219, 99)
            textoPontuacao = Texto("Final Score: " + str(self.pontuacao), dourado, 50)
            textoPontuacao.mostrar(220, 100)

            pygame.draw.rect(fundo, dourado3, [143, 168, 369, 51])
            pygame.draw.rect(fundo, dourado, [145, 170, 365, 47])
            textoComecar = Texto("Back to Menu", branco, 70)
            textoComecar.mostrar(150, 173)

            pygame.draw.rect(fundo, dourado3, [193, 268, 279, 58])
            pygame.draw.rect(fundo, dourado, [195, 270, 275, 54])
            textoComecar = Texto("New Game", branco, 70)
            textoComecar.mostrar(210, 273)

            pygame.display.update()

    def menu(self):
        while self.noMenu:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.noMenu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.noMenu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_x = mouse_pos[0]
                    mouse_y = mouse_pos[1]
                    if 143 < mouse_x < 143 + 359 and 168 < mouse_y < 168 + 51:
                        self.jogando = True
                        self.perdeu = False
                        self.noMenu = False
                        self.modo = "classico"
                        self.play()
                    if 183 < mouse_x < 183 + 279 and 268 < mouse_y < 268 + 51:
                        self.jogando = True
                        self.noMenu = False
                        self.perdeu = False
                        self.modo = "livre"
                        self.play()
            fundo.fill(dourado2)

            textoInicioS = Texto("The Gold", dourado3, 100)
            textoInicioS.mostrar(168, 28)
            textoInicio = Texto("The Gold", dourado, 100)
            textoInicio.mostrar(170, 30)

            pygame.draw.rect(fundo, dourado3, [143, 168, 359, 51])
            pygame.draw.rect(fundo, dourado, [145, 170, 355, 47])
            textoComecar = Texto("Classic Mode", branco, 70)
            textoComecar.mostrar(150, 175)

            pygame.draw.rect(fundo, dourado3, [183, 268, 279, 51])
            pygame.draw.rect(fundo, dourado, [185, 270, 275, 47])
            textoComecar = Texto("Free Mode", branco, 70)
            textoComecar.mostrar(190, 273)

            pygame.display.update()


if __name__ == '__main__':
    instancia = Jogo()
    instancia.menu()

pygame.quit()

