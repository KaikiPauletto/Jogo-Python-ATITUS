import pygame
import sys
from Recursos.Functions import iniciarJanela, carregarFonte, branco, preto, render_text_wrapped

def telaInicial(tela):
    fundoOriginal = pygame.image.load("Recursos/imagens/Menu celeiro dentro.png")
    fundo = pygame.transform.scale(fundoOriginal, (tela.get_width(), tela.get_height()))
    fonteTitulo = carregarFonte(36)
    fonteInput = pygame.font.SysFont("arial", 32)
    nomeJogador = ""
    ativo = True

    inputBox = pygame.Rect(300, 500, 400, 40)
    corAtiva = pygame.Color("dodgerblue2")
    corInativa = pygame.Color("gray15")
    corAtual = corInativa

    larguraCaixa = 600
    alturaCaixa = 100
    caixaMensagem = pygame.Surface((larguraCaixa, alturaCaixa), pygame.SRCALPHA)
    caixaMensagem.fill((0, 0, 0, 150))  # Fundo escuro com transparência

    while ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if inputBox.collidepoint(evento.pos):
                    corAtual = corAtiva
                else:
                    corAtual = corInativa
            if evento.type == pygame.KEYDOWN:
                if corAtual == corAtiva:
                    if evento.key == pygame.K_RETURN and nomeJogador != "":
                        return nomeJogador
                    elif evento.key == pygame.K_BACKSPACE:
                        nomeJogador = nomeJogador[:-1]
                    else:
                        nomeJogador += evento.unicode

        tela.blit(fundo, (0, 0))

        # Posição centralizada para a mensagem
        xMsg = (tela.get_width() - larguraCaixa) // 2
        yMsg = 100

        tela.blit(caixaMensagem, (xMsg, yMsg))

        # Sombra do texto
        textoSombra = fonteTitulo.render("Insira seu nome:", True, (0, 0, 0))
        sombraRect = textoSombra.get_rect(center=(tela.get_width() // 2 + 2, yMsg + alturaCaixa // 2 + 2))
        tela.blit(textoSombra, sombraRect)

        textoInstrucao = fonteTitulo.render("Insira seu nome:", True, branco)
        textoRect = textoInstrucao.get_rect(center=(tela.get_width() // 2, yMsg + alturaCaixa // 2))
        tela.blit(textoInstrucao, textoRect)

        # Sombra da caixa de entrada
        sombra = inputBox.move(4, 4)
        pygame.draw.rect(tela, (50, 50, 50), sombra, border_radius=10)

        # Caixa branca arredondada
        pygame.draw.rect(tela, branco, inputBox, border_radius=10)

        # Borda da caixa
        pygame.draw.rect(tela, corAtual, inputBox, 3, border_radius=10)

        texto = fonteInput.render(nomeJogador, True, preto)
        tela.blit(texto, (inputBox.x + 10, inputBox.y + 5))

        pygame.display.flip()


def telaDeBoasVindas(tela, nomeJogador):
    fundoOriginal = pygame.image.load("Recursos/imagens/Menu celeiro fora.png")
    fundo = pygame.transform.scale(fundoOriginal, (tela.get_width(), tela.get_height()))
    fonteTitulo = carregarFonte(48)
    fonteRegras = carregarFonte(20)
    fonteBotao = carregarFonte(30)

    botaoStart = pygame.Rect(400, 600, 200, 50)

    posRetangulo = (50, 80)
    larguraRetangulo = 900
    alturaRetangulo = 350

    regras = [
        "Mova-se usando as setas esquerda/direita",
        "Colete as moedas e o dinheiro",
        "Desvie dos martelos",
        "Você tem 3 vidas"
    ]

    ativo = True
    while ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botaoStart.collidepoint(evento.pos):
                    return

        tela.blit(fundo, (0, 0))

        # Caixa semitransparente atrás do texto
        s = pygame.Surface((larguraRetangulo, alturaRetangulo), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        tela.blit(s, posRetangulo)

        alturaTexto = render_text_wrapped(
            tela,
            f"Seja bem-vindo, {nomeJogador}!",
            fonteTitulo,
            branco,
            (posRetangulo[0] + 20, posRetangulo[1] + 20),
            larguraRetangulo - 40
        )

        posRegras_y = posRetangulo[1] + 20 + alturaTexto + 20

        for i, linha in enumerate(regras):
            textoRegra = fonteRegras.render(linha, True, branco)
            tela.blit(textoRegra, (posRetangulo[0] + 20, posRegras_y + i * 30))

        # Efeito de hover no botão
        corBotao = (0, 160, 0) if botaoStart.collidepoint(pygame.mouse.get_pos()) else (0, 128, 0)
        pygame.draw.rect(tela, corBotao, botaoStart, border_radius=12)

        textoBotao = fonteBotao.render("Start", True, branco)
        textoBotaoPos = textoBotao.get_rect(center=botaoStart.center)
        tela.blit(textoBotao, textoBotaoPos)

        pygame.display.flip()


def main():
    tela = iniciarJanela()
    nomeJogador = telaInicial(tela)
    print(f"Jogador: {nomeJogador}")
    telaDeBoasVindas(tela, nomeJogador)

    # Aqui pode continuar o jogo...

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
