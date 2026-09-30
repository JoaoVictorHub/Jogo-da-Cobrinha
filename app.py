import pygame
import random
import array

# Inicialização
pygame.init()
pygame.mixer.init(frequency=44100,size=-16,channels=1)
pygame.display.set_caption('Jogo da Cobrinha')

# Constantes de configuração
larguraTela = 800
alturaTela = 600
tamanhoQuadrado = 20

# Cores RGB
preto = (18,18,18)
branco = (245,245,245)
vermelho = (239,68,68)
verdeCobra = (34,197,94)
verdeFolha = (16,185,129)
cinzaEscuro = (30,30,30)

tela = pygame.display.set_mode((larguraTela,alturaTela))
relogio = pygame.time.Clock()
fontePontos = pygame.font.SysFont(None,35)
fonteGameOver = pygame.font.SysFont(None,50)

# Áudio
def gerarSomSintetizado(frequencia,duracao_ms,volume=0.3):
    sampleRate = 44100
    nSamples = int(sampleRate * (duracao_ms / 1000.0))
    buffer = array.array('h')

    for i in range(nSamples):
        # Gera onda senoidal
        t = float(i) / sampleRate
        val = int(volume * 32767.0 * (0.5 * (1.0 + random.uniform(-0.1, 0.1) if frequencia == 0 else 0)))
        if frequencia > 0:
            import math
            val = int(volume * 32767.0 * math.sin(2.0 * math.pi * frequencia * t))
        buffer.append(val)

    return pygame.mixer.Sound(buffer=buffer)

# Sons gerados
somComer = gerarSomSintetizado(880,80,0.2)
somGameOver = gerarSomSintetizado(150,400,0.3)

def gerarComida():
    comidaX = round(random.randrange(0, larguraTela - tamanhoQuadrado) / float(tamanhoQuadrado)) * tamanhoQuadrado
    comidaY = round(random.randrange(0, alturaTela - tamanhoQuadrado) / float(tamanhoQuadrado)) * tamanhoQuadrado
    return comidaX,comidaY

def desenharGrade():
    for x in range(0,larguraTela,tamanhoQuadrado):
        pygame.draw.line(tela,cinzaEscuro,(x,0),(x,alturaTela))
    for y in range(0,alturaTela,tamanhoQuadrado):
        pygame.draw.line(tela,cinzaEscuro,(0,y),(larguraTela,y))

def desenharComida(comidaX,comidaY):
    centroX = comidaX + tamanhoQuadrado // 2
    centroY = comidaY + tamanhoQuadrado // 2
    raio = tamanhoQuadrado // 2 - 1

    # Corpo da Maçã
    pygame.draw.circle(tela,vermelho,(centroX,centroY),raio)
    # Folha
    pygame.draw.circle(tela,verdeFolha,(centroX + 3,comidaY + 3),3)

def desenharCobra(pixels,velocidadeX,velocidadeY):
    # Desenha o corpo da cobra
    for pixel in pixels[:-1]:
        rect = pygame.Rect(pixel[0],pixel[1],tamanhoQuadrado,tamanhoQuadrado)
        pygame.draw.rect(tela,verdeCobra,rect,border_radius=4)

    # Desenha a cabeça
    cabeca = pixels[-1]
    rectCabeca = pygame.Rect(cabeca[0],cabeca[1],tamanhoQuadrado,tamanhoQuadrado)
    pygame.draw.rect(tela,verdeCobra,rectCabeca,border_radius=6)

    # Posições relativas dos olhos com base na direção do movimento
    olhoRaio = 2
    cx,cy = cabeca[0],cabeca[1]

    posicaoOlho1 = (cx + 5, cy + 5)
    posicaoOlho2 = (cx + 15, cy + 5)

    if velocidadeX > 0:  # Direita
        posicaoOlho1,posicaoOlho2 = (cx + 14, cy + 5), (cx + 14, cy + 15)
    elif velocidadeX < 0:  # Esquerda
        posicaoOlho1,posicaoOlho2 = (cx + 5, cy + 5), (cx + 5, cy + 15)
    elif velocidadeY > 0:  # Baixo
        posicaoOlho1,posicaoOlho2 = (cx + 5, cy + 14), (cx + 15, cy + 14)
    elif velocidadeY < 0:  # Cima
        posicaoOlho1,posicaoOlho2 = (cx + 5, cy + 5), (cx + 15, cy + 5)

    pygame.draw.circle(tela,preto,posicaoOlho1,olhoRaio)
    pygame.draw.circle(tela,preto,posicaoOlho2,olhoRaio)

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
    filaMovimentos = []

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

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sairDoJogo = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    filaMovimentos.append((-tamanhoQuadrado,0))
                elif evento.key == pygame.K_RIGHT:
                    filaMovimentos.append((tamanhoQuadrado,0))
                elif evento.key == pygame.K_UP:
                    filaMovimentos.append((0,-tamanhoQuadrado))
                elif evento.key == pygame.K_DOWN:
                    filaMovimentos.append((0,tamanhoQuadrado))

        # Processa o próximo movimento válido da fila
        if filaMovimentos:
            proximoMovimentoX,proximoMovimentoY = filaMovimentos.pop(0)
            if (proximoMovimentoX != -velocidadeX or proximoMovimentoX == 0) and (proximoMovimentoY != -velocidadeY or proximoMovimentoY == 0):
                velocidadeX,velocidadeY = proximoMovimentoX,proximoMovimentoY

        # Atualização da posição
        x += velocidadeX
        y += velocidadeY

        # Colisão com as paredes
        if x < 0 or x >= larguraTela or y < 0 or y >= alturaTela:
            somGameOver.play()
            gameOver = True

        pixels.append([x,y])
        if len(pixels) > tamanhoCobra:
            del pixels[0]

        # Colisão com o corpo
        if velocidadeX != 0 or velocidadeY != 0:
            for pixel in pixels[:-1]:
                if pixel == [x,y]:
                    somGameOver.play()
                    gameOver = True

        # Renderização
        tela.fill(preto)
        desenharGrade()
        desenharComida(comidaX,comidaY)
        desenharCobra(pixels,velocidadeX,velocidadeY)
        desenharPontuacao(tamanhoCobra-1)

        pygame.display.update()

        # Colisão com a comida
        if x == comidaX and y == comidaY:
            somComer.play()
            tamanhoCobra += 1
            comidaX,comidaY = gerarComida()
            # Aumenta a velocidade levemente a cada comida adquirida
            velocidadeJogo += 0.1

        relogio.tick(velocidadeJogo)

    pygame.quit()

if __name__ == '__main__':
    rodarJogo()
