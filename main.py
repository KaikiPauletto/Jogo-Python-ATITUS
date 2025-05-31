import pygame
import sys
import random
import math

from Recursos.Functions import iniciarJanela, carregarFonte, branco, preto, render_text_wrapped, desenhar_botoes_som
from Recursos.Functions import hitbox_reduzida
from Recursos.Functions import pausar_jogo


pygame.init()
pygame.mixer.init()

musicaAtiva = True
pygame.mixer.music.load("Recursos/sons/Trilha sonora.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


def verificarCliqueSom(evento, somLigado):
    if evento.type == pygame.MOUSEBUTTONDOWN:
        if evento.button == 1:
            posMouse = evento.pos
            botaoSom = pygame.Rect(920, 20, 40, 40)
            if botaoSom.collidepoint(posMouse):
                if somLigado:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                return not somLigado
    return somLigado


def telaInicial(tela):
    global musicaAtiva
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
    caixaMensagem.fill((0, 0, 0, 150))

    while ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            musicaAtiva = verificarCliqueSom(evento, musicaAtiva)
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

        xMsg = (tela.get_width() - larguraCaixa) // 2
        yMsg = 100
        tela.blit(caixaMensagem, (xMsg, yMsg))

        textoSombra = fonteTitulo.render("Insira seu nome:", True, (0, 0, 0))
        sombraRect = textoSombra.get_rect(center=(tela.get_width() // 2 + 2, yMsg + alturaCaixa // 2 + 2))
        tela.blit(textoSombra, sombraRect)

        textoInstrucao = fonteTitulo.render("Insira seu nome:", True, branco)
        textoRect = textoInstrucao.get_rect(center=(tela.get_width() // 2, yMsg + alturaCaixa // 2))
        tela.blit(textoInstrucao, textoRect)

        sombra = inputBox.move(4, 4)
        pygame.draw.rect(tela, (50, 50, 50), sombra, border_radius=10)
        pygame.draw.rect(tela, branco, inputBox, border_radius=10)
        pygame.draw.rect(tela, corAtual, inputBox, 3, border_radius=10)

        texto = fonteInput.render(nomeJogador, True, preto)
        tela.blit(texto, (inputBox.x + 10, inputBox.y + 5))

        # Botão de som
        desenhar_botoes_som(tela, musicaAtiva)

        pygame.display.flip()


def telaDeBoasVindas(tela, nomeJogador):
    global musicaAtiva
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
            musicaAtiva = verificarCliqueSom(evento, musicaAtiva)
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botaoStart.collidepoint(evento.pos):
                    return  # Sai para iniciar a gameplay

        tela.blit(fundo, (0, 0))

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

        corBotao = (0, 160, 0) if botaoStart.collidepoint(pygame.mouse.get_pos()) else (0, 128, 0)
        pygame.draw.rect(tela, corBotao, botaoStart, border_radius=12)

        textoBotao = fonteBotao.render("Start", True, branco)
        textoBotaoPos = textoBotao.get_rect(center=botaoStart.center)
        tela.blit(textoBotao, textoBotaoPos)

        # Botão de som
        desenhar_botoes_som(tela, musicaAtiva)

        pygame.display.flip()


def gameplay(tela):
    global musicaAtiva
    clock = pygame.time.Clock()

    # No começo da função gameplay, crie a fonte pequena:
    fonte_pequena = pygame.font.SysFont("arial", 16)  # Fonte menor para a mensagem

    # Carregar imagens
    porquinho_img = pygame.image.load("Recursos/imagens/Porquinho.png").convert_alpha()
    moeda1_img = pygame.image.load("Recursos/imagens/Moeda 1.png").convert_alpha()
    moeda50_img = pygame.image.load("Recursos/imagens/Moeda 50.png").convert_alpha()
    dinheiro5_img = pygame.image.load("Recursos/imagens/Dinheiro 5.png").convert_alpha()
    martelo_img = pygame.image.load("Recursos/imagens/Martelo.png").convert_alpha()
    fundoOriginal = pygame.image.load("Recursos/imagens/Cenário 2.jpg")
    passaro_img = pygame.image.load("Recursos/imagens/Passaro-removebg-preview.png").convert_alpha()
    

    # Redimensionar imagens se quiser (exemplo: manter escala proporcional)
    porquinho_img = pygame.transform.scale(porquinho_img, (140, 110))
    moeda1_img = pygame.transform.scale(moeda1_img, (80, 80))
    moeda50_img = pygame.transform.scale(moeda50_img, (80, 80))
    dinheiro5_img = pygame.transform.scale(dinheiro5_img, (80, 80))
    martelo_img = pygame.transform.scale(martelo_img, (80, 80))
    fundo = pygame.transform.scale(fundoOriginal, (tela.get_width(), tela.get_height()))
    passaro_img = pygame.transform.scale(passaro_img, (60, 60))  # tamanho pequeno

    # Centro do círculo onde o passarinho vai voar
    passaro_centro_x = tela.get_width() // 2
    passaro_centro_y = 150  # um pouco no topo da tela, ajusta depois se quiser

    passaro_raio = 100  # raio do círculo do voo
    passaro_angulo = 0  # ângulo inicial
    passaro_angulo_velocidade = 0.02  # velocidade do movimento circular

    # Player
    player_rect = porquinho_img.get_rect(midbottom=(tela.get_width()//2, tela.get_height() - 70))
    player_speed = 10

    # Listas de itens e obstáculos
    itens = []  # cada item: dict com 'rect', 'tipo', 'imagem', 'valor'
    obstaculos = []  # cada obstáculo: rect

    # Velocidades de queda
    velocidade_item = 5
    velocidade_obstaculo = 7

    # Controle de spawn
    tempo_spawn_item = 0
    tempo_spawn_obstaculo = 0

    # Pontuação e vidas
    score = 0
    vidas = 3
    dano_tomado = 0


    fonte = carregarFonte(30)

    rodando = True

    # Parâmetros do Sol pulsante
    raio_base = 40
    amplitude = 10
    tempo = 0

    while rodando:
        clock.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausar_jogo(tela, fonte)

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            musicaAtiva = verificarCliqueSom(evento, musicaAtiva)

        tela.blit(fundo, (0, 0))
        
        passaro_angulo += passaro_angulo_velocidade
        if passaro_angulo > 2 * math.pi:
            passaro_angulo -= 2 * math.pi

        passaro_x = passaro_centro_x + passaro_raio * math.cos(passaro_angulo)
        passaro_y = passaro_centro_y + passaro_raio * math.sin(passaro_angulo)
        passaro_rect = passaro_img.get_rect(center=(passaro_x, passaro_y))

        # Movimento do player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < tela.get_width():
            player_rect.x += player_speed

        # Spawn de itens (a cada ~1s)
        tempo_spawn_item += 1
        if tempo_spawn_item > 60:
            tempo_spawn_item = 0
            tipo = random.choices(
                ['moeda1', 'moeda50', 'dinheiro5'],
                weights=[50, 30, 20],
                k=1
            )[0]

            x_pos = random.randint(0, tela.get_width() - 50)
            if tipo == 'moeda1':
                img = moeda1_img
                valor = 1
                rect = img.get_rect(topleft=(x_pos, -40))
            elif tipo == 'moeda50':
                img = moeda50_img
                valor = 0.5
                rect = img.get_rect(topleft=(x_pos, -40))
            else:
                img = dinheiro5_img
                valor = 5
                rect = img.get_rect(topleft=(x_pos, -50))

            itens.append({'rect': rect, 'tipo': tipo, 'imagem': img, 'valor': valor})

        # Spawn de obstáculos (a cada 1.5s)
        tempo_spawn_obstaculo += 1
        if tempo_spawn_obstaculo > 90:
            tempo_spawn_obstaculo = 0
            x_pos = random.randint(0, tela.get_width() - 50)
            rect = martelo_img.get_rect(topleft=(x_pos, -50))
            obstaculos.append(rect)

        # Atualiza posição dos itens
        for item in itens[:]:
            item['rect'].y += velocidade_item
            if hitbox_reduzida(item['rect']).colliderect(hitbox_reduzida(player_rect, 20, 10)):
                score += item['valor']
                itens.remove(item)
            elif item['rect'].top > tela.get_height():
                itens.remove(item)

        # Atualiza posição dos obstáculos
        for obs in obstaculos[:]:
            obs.y += velocidade_obstaculo
            if hitbox_reduzida(obs).colliderect(hitbox_reduzida(player_rect, 20, 10)):
                vidas -= 1
                dano_tomado = 12
                obstaculos.remove(obs)
            elif obs.top > tela.get_height():
                obstaculos.remove(obs)

        # Desenha player
        tela.blit(porquinho_img, player_rect)
        if dano_tomado > 0:
            porquinho_tingido = porquinho_img.copy()
            # Pinta os pixels visíveis da imagem com vermelho mantendo a transparência
            tint_surface = pygame.Surface(porquinho_img.get_size(), pygame.SRCALPHA)
            tint_surface.fill((255, 0, 0, 120))  # vermelho semi-transparente
            porquinho_tingido.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            tela.blit(porquinho_tingido, player_rect)
            dano_tomado -= 1
        else:
            tela.blit(porquinho_img, player_rect)



        # Desenha itens
        for item in itens:
            tela.blit(item['imagem'], item['rect'])

        # Desenha obstáculos
        for obs in obstaculos:
            tela.blit(martelo_img, obs)

        # Interface (pontuação e vidas)
        score_text = fonte.render(f"Pontuação: {score:.1f}", True, (0, 0, 0))
        vidas_text = fonte.render(f"Vidas: {vidas}", True, (255, 0, 0))
        tela.blit(score_text, (10, 10))
        tela.blit(vidas_text, (10, 50))

        # Botão de som
        desenhar_botoes_som(tela, musicaAtiva)

        # Sol pulsante (círculo amarelo no canto superior direito)
        tempo += 0.05
        raio_sol = int(raio_base + amplitude * math.sin(tempo))
        pos_sol = (tela.get_width() - 120, 100)  # Posição do sol com margem

        pygame.draw.circle(tela, (255, 255, 0), pos_sol, raio_sol)

        tela.blit(passaro_img, passaro_rect)

        mensagem_pausa = "Press Space To Pause Game"
        texto_pausa = fonte_pequena.render(mensagem_pausa, True, (0, 0, 0))  # cor preta, pode mudar
        texto_rect = texto_pausa.get_rect(center=(tela.get_width() // 2, 65))  # 20 px do topo
        tela.blit(texto_pausa, texto_rect)

        pygame.display.flip()

        # Fim de jogo
        if vidas <= 0:
            s = pygame.Surface((tela.get_width(), tela.get_height()), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            tela.blit(s, (0, 0))

            fonte_fim = carregarFonte(72)
            texto_fim = fonte_fim.render("Fim de jogo!", True, (255, 0, 0))
            tela.blit(texto_fim, (tela.get_width()//2 - texto_fim.get_width()//2,
                                tela.get_height()//2 - texto_fim.get_height()//2))
            pygame.display.flip()
            pygame.time.delay(3000)
            rodando = False



def main():
    tela = iniciarJanela()

    nomeJogador = telaInicial(tela)
    print(f"Jogador: {nomeJogador}")

    telaDeBoasVindas(tela, nomeJogador)

    pygame.mixer.music.stop()

    gameplay(tela)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
