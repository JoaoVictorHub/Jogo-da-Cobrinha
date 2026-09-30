import pygame
import random

# Inicialização
pygame.init()
pygame.display.set_caption('Jogo da Cobrinha')


# Constantes de configuração
larguraTela = 800
alturaTela = 600
tamanhoQuadrado = 20

# Cores RGB
preto = (18,18,18)
branco = (245,245,245)
vermelho = (239,68,68)
verde = (34,197,94)
cinzaEscuro = (30,30,30)

tela = pygame.display.set_mode((larguraTela,alturaTela))
relogio = pygame.time.Clock()
fontePontos = pygame.font.SysFont(None,35)
fonteGameOver = pygame.font.SysFont(None,50)

def gerarComida():
    comidaX = round(random.randrange(0, larguraTela - tamanhoQuadrado) / float(tamanhoQuadrado)) * tamanhoQuadrado
    comidaY = round(random.randrange(0, alturaTela - tamanhoQuadrado) / float(tamanhoQuadrado)) * tamanhoQuadrado
    return comidaX, comidaY

def desenharGrade():
    for x in range(0,larguraTela,tamanhoQuadrado):
        pygame.draw.line(tela,cinzaEscuro,(x,0),(x,alturaTela))
    for y in range(0,alturaTela,tamanhoQuadrado):
        pygame.draw.line(tela,cinzaEscuro,(0,y),(larguraTela,y))

def desenharComida(comidaX,comidaY):
    pygame.draw.rect(tela,vermelho,[comidaX,comidaY,tamanhoQuadrado,tamanhoQuadrado])

def desenharCobra(pixels):
    for pixel in pixels:
        pygame.draw.rect(tela,verde,[pixel[0],pixel[1],tamanhoQuadrado,tamanhoQuadrado])

def desenharPontuacao(pontuacao):
    texto = fontePontos.render(f'Pontos: {pontuacao}',True,branco)
    tela.blit(texto,(10,10))

def rodarJogo():
    sairDoJogo = False
    gameOver = False

    # Posição inicial da cobra
    x = larguraTela / 2
    y = alturaTela / 2

    # Velocidade inicial
    velocidadeX = 0
    velocidadeY = 0

    tamanhoCobra = 1
    pixels = []
    velocidadeJogo = 12

    comidaX,comidaY = gerarComida()

    while not sairDoJogo:

        # Tela de Game Over
        while gameOver:
            tela.fill(preto)
            textoGameOver = fonteGameOver.render('Fim de Jogo!',True,vermelho)
            textoInstrucoes = fontePontos.render('Pressione R para Recomeçar ou Q para Sair',True,branco)
            
            tela.blit(textoGameOver, [larguraTela / 2 - 110, alturaTela / 3])
            tela.blit(textoInstrucoes, [larguraTela / 2 - 250, alturaTela / 2])
            desenharPontuacao(tamanhoCobra-1)
            
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    gameOver = False
                    sairDoJogo = True
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        gameOver = False
                        sairDoJogo = True
                    if evento.key == pygame.K_r:
                        rodarJogo()
                        return

        # Captura de Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sairDoJogo = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and velocidadeX == 0:
                    velocidadeX = -tamanhoQuadrado
                    velocidadeY = 0
                elif evento.key == pygame.K_RIGHT and velocidadeX == 0:
                    velocidadeX = tamanhoQuadrado
                    velocidadeY = 0
                elif evento.key == pygame.K_UP and velocidadeY == 0:
                    velocidadeX = 0
                    velocidadeY = -tamanhoQuadrado
                elif evento.key == pygame.K_DOWN and velocidadeY == 0:
                    velocidadeX = 0
                    velocidadeY = tamanhoQuadrado

        # Atualização da posição
        x += velocidadeX
        y += velocidadeY

        # Colisão com as paredes
        if x < 0 or x >= larguraTela or y < 0 or y >= alturaTela:
            gameOver = True

        pixels.append([x,y])
        if len(pixels) > tamanhoCobra:
            del pixels[0]

        # Colisão com o próprio corpo
        if velocidadeX != 0 or velocidadeY != 0:
            for pixel in pixels[:-1]:
                if pixel == [x,y]:
                    gameOver = True

        # Renderização
        tela.fill(preto)
        desenharGrade()
        desenharComida(comidaX,comidaY)
        desenharCobra(pixels)
        desenharPontuacao(tamanhoCobra-1)

        pygame.display.update()

        # Colisão com a comida
        if x == comidaX and y == comidaY:
            tamanhoCobra += 1
            comidaX,comidaY = gerarComida()
            # Aumenta a velocidade levemente a cada comida adquirida
            velocidadeJogo += 0.1

        relogio.tick(velocidadeJogo)

    pygame.quit()

if __name__ == '__main__':
    rodarJogo()