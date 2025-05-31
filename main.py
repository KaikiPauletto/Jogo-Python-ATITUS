import pygame
import sys
import random
import math

from Recursos.Functions import iniciarJanela, carregarFonte, branco, preto, render_text_wrapped, desenhar_botoes_som
from Recursos.Functions import hitbox_reduzida
from Recursos.Functions import pausar_jogo
from Recursos.Functions import registrar_resultado, ler_ultimos_registros
from Recursos.Functions import interacao_por_voz




pygame.init()
pygame.mixer.init()

icone_janela = pygame.image.load("Recursos/imagens/Icone-removebg-preview.png")
pygame.display.set_icon(icone_janela)


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
                    return  

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

        desenhar_botoes_som(tela, musicaAtiva)

        pygame.display.flip()


def gameplay(tela, nomeJogador, fala_ao_perder=True):
    global musicaAtiva
    clock = pygame.time.Clock()

    pygame.mixer.music.load("Recursos/sons/Pou music ost - ConnectCliff JumpCliff DashJet Pou.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    frames_passados = 0
    dificuldade_nivel = 1
    tempo_obstaculo_contador = 0
    intervalo_spawn_obstaculo = 90  
    quantidade_martelos = 1

    
    fonte_pequena = pygame.font.SysFont("arial", 16)  

    # Carregar imagens
    porquinho_img = pygame.image.load("Recursos/imagens/Porquinho.png").convert_alpha()
    moeda1_img = pygame.image.load("Recursos/imagens/Moeda 1.png").convert_alpha()
    moeda50_img = pygame.image.load("Recursos/imagens/Moeda 50.png").convert_alpha()
    dinheiro5_img = pygame.image.load("Recursos/imagens/Dinheiro 5.png").convert_alpha()
    martelo_img = pygame.image.load("Recursos/imagens/Martelo.png").convert_alpha()
    fundoOriginal = pygame.image.load("Recursos/imagens/Cenário 2.jpg")
    passaro_img = pygame.image.load("Recursos/imagens/Passaro-removebg-preview.png").convert_alpha()
    

    # Redimensionar imagens se quiser (exemplo: manter escala proporcional)
    porquinho_img = pygame.transform.scale(porquinho_img, (120, 90))
    moeda1_img = pygame.transform.scale(moeda1_img, (60, 60))
    moeda50_img = pygame.transform.scale(moeda50_img, (60, 60))
    dinheiro5_img = pygame.transform.scale(dinheiro5_img, (60, 60))
    martelo_img = pygame.transform.scale(martelo_img, (60, 60))
    fundo = pygame.transform.scale(fundoOriginal, (tela.get_width(), tela.get_height()))
    passaro_img = pygame.transform.scale(passaro_img, (60, 60))  # tamanho pequeno

    
    passaro_centro_x = tela.get_width() // 2
    passaro_centro_y = 150  

    passaro_raio = 100  
    passaro_angulo = 0  
    passaro_angulo_velocidade = 0.02  

    # Player
    player_rect = porquinho_img.get_rect(midbottom=(tela.get_width()//2, tela.get_height() - 90))
    player_speed = 10

    # Listas de itens e obstáculos
    itens = []  
    obstaculos = []  

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
        frames_passados += 1

        # Dificuldade
        if frames_passados % 900 == 0:
            dificuldade_nivel += 1
            print(f"Dificuldade aumentada: Nível {dificuldade_nivel}")
            if intervalo_spawn_obstaculo > 30:
                intervalo_spawn_obstaculo -= 5
            if quantidade_martelos < 3:
                quantidade_martelos += 1



            
            if velocidade_obstaculo < 20:
                velocidade_obstaculo += 1

            if tempo_spawn_obstaculo > 30:
                tempo_spawn_obstaculo -= 5
        
        tempo_obstaculo_contador += 1
        if tempo_obstaculo_contador > intervalo_spawn_obstaculo:
            tempo_obstaculo_contador = 0

            for _ in range(quantidade_martelos):
                x_pos = random.randint(0, tela.get_width() - 50)
                rect = martelo_img.get_rect(topleft=(x_pos, -50))
                mask = pygame.mask.from_surface(martelo_img)
                obstaculos.append({"rect": rect, "mask": mask})


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

        # Spawn de itens
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
            obs["rect"].y += velocidade_obstaculo
            offset = (obs["rect"].x - player_rect.x, obs["rect"].y - player_rect.y)
            if pygame.mask.from_surface(porquinho_img).overlap(obs["mask"], offset):
                vidas -= 1
                dano_tomado = 12
                obstaculos.remove(obs)
            elif obs["rect"].top > tela.get_height():
                obstaculos.remove(obs)

        tela.blit(porquinho_img, player_rect)
        if dano_tomado > 0:
            porquinho_tingido = porquinho_img.copy()
            tint_surface = pygame.Surface(porquinho_img.get_size(), pygame.SRCALPHA)
            tint_surface.fill((255, 0, 0, 120))  
            porquinho_tingido.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            tela.blit(porquinho_tingido, player_rect)
            dano_tomado -= 1
        else:
            tela.blit(porquinho_img, player_rect)

        for item in itens:
            tela.blit(item['imagem'], item['rect'])

        for obs in obstaculos:
            tela.blit(martelo_img, obs["rect"])

        score_text = fonte.render(f"Pontuação: {score:.1f}", True, (0, 0, 0))
        vidas_text = fonte.render(f"Vidas: {vidas}", True, (255, 0, 0))
        tela.blit(score_text, (10, 10))
        tela.blit(vidas_text, (10, 50))

        desenhar_botoes_som(tela, musicaAtiva)

        tempo += 0.05
        raio_sol = int(raio_base + amplitude * math.sin(tempo))
        pos_sol = (tela.get_width() - 120, 100)  

        pygame.draw.circle(tela, (255, 255, 0), pos_sol, raio_sol)

        tela.blit(passaro_img, passaro_rect)

        mensagem_pausa = "Press Space To Pause Game"
        texto_pausa = fonte_pequena.render(mensagem_pausa, True, (0, 0, 0))  
        texto_rect = texto_pausa.get_rect(center=(tela.get_width() // 2, 65))  
        tela.blit(texto_pausa, texto_rect)

        pygame.display.flip()

        # Fim de jogo
        if vidas <= 0:
            pygame.mixer.music.stop()
            registrar_resultado(nomeJogador, score)

            s = pygame.Surface((tela.get_width(), tela.get_height()), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            tela.blit(s, (0, 0))

            fonte_fim = carregarFonte(72)
            texto_fim = fonte_fim.render("Fim de jogo!", True, (255, 0, 0))
            texto_fim_rect = texto_fim.get_rect(center=(tela.get_width()//2, 150))
            tela.blit(texto_fim, texto_fim_rect)

            # Tabela
            registros = ler_ultimos_registros()
            fonte_registro = carregarFonte(18)
            altura_linha = 35
            largura_tabela = 500
            altura_tabela = 40 + (len(registros) + 1) * altura_linha + 20
            x_tabela = (tela.get_width() - largura_tabela) // 2
            y_tabela = texto_fim_rect.bottom + 30

            tabela_surface = pygame.Surface((largura_tabela, altura_tabela), pygame.SRCALPHA)
            tabela_surface.fill((0, 0, 0, 180))
            pygame.draw.rect(tabela_surface, (255, 255, 255), tabela_surface.get_rect(), 2, border_radius=10)

            # Cabeçalho
            cabecalho_font = carregarFonte(20)
            cabecalho_texto = cabecalho_font.render("Últimos 5 Jogos", True, (255, 255, 0))
            tabela_surface.blit(cabecalho_texto, (largura_tabela//2 - cabecalho_texto.get_width()//2, 10))

            col_font = carregarFonte(16)
            col_nomes = ["Nome", "Pontos", "Hora"]
            col_x = [30, 220, 370]

            for i, titulo in enumerate(col_nomes):
                txt = col_font.render(titulo, True, (200, 200, 200))
                tabela_surface.blit(txt, (col_x[i], 40))

            for i, (nome, pontos, hora) in enumerate(registros):
                y_linha = 40 + altura_linha + i * altura_linha
                for j, val in enumerate([nome, pontos, hora]):
                    txt = col_font.render(str(val), True, (255, 255, 255))
                    tabela_surface.blit(txt, (col_x[j], y_linha))

            tela.blit(tabela_surface, (x_tabela, y_tabela))

            # Definições de tamanho e espaçamento
            largura_jogar = 450
            largura_fechar = 450
            altura_botoes = 100
            espaco_entre_botoes = 60

            # Posições dos botões
            botao_jogar = pygame.Rect(
                tela.get_width() // 2 - largura_jogar - espaco_entre_botoes // 2,
                y_tabela + altura_tabela + 40,
                largura_jogar,
                altura_botoes
            )

            botao_fechar = pygame.Rect(
                tela.get_width() // 2 + espaco_entre_botoes // 2,
                y_tabela + altura_tabela + 40,
                largura_fechar,
                altura_botoes
            )

            # Desenha os botões
            pygame.draw.rect(tela, (0, 160, 0), botao_jogar, border_radius=12)
            pygame.draw.rect(tela, (160, 0, 0), botao_fechar, border_radius=12)

            # Textos nos botões
            botao_font = carregarFonte(28)
            texto_jogar = botao_font.render("Jogar Novamente", True, (255, 255, 255))
            texto_fechar = botao_font.render("Fechar", True, (255, 255, 255))

            tela.blit(texto_jogar, texto_jogar.get_rect(center=botao_jogar.center))
            tela.blit(texto_fechar, texto_fechar.get_rect(center=botao_fechar.center))

            # Mensagem acima dos botões
            fonte_fallback = carregarFonte(20)
            msg = fonte_fallback.render("Clique ou fale sua escolha:", True, (255, 255, 255))
            tela.blit(msg, (tela.get_width() // 2 - msg.get_width() // 2, botao_jogar.top - 40))

            pygame.display.flip()


            # Voz + Reconhecimento
            import threading, pyttsx3, speech_recognition as sr
            reconhecido = None

            def falar():
                engine = pyttsx3.init()
                engine.setProperty("rate", 160)
                engine.say("Você perdeu. Se deseja jogar novamente, fale jogar novamente. Se deseja sair, fale fechar.")
                engine.runAndWait()

            def escutar():
                nonlocal reconhecido
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    try:
                        r.adjust_for_ambient_noise(source)
                        audio = r.listen(source, timeout=7)
                        texto = r.recognize_google(audio, language="pt-BR").lower()
                        if "fechar" in texto:
                            reconhecido = "fechar"
                        elif "jogar" in texto:
                            reconhecido = "reiniciar"
                    except:
                        reconhecido = None

            threading.Thread(target=falar).start()
            threading.Thread(target=escutar).start()

            # Espera interação
            while True:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if botao_jogar.collidepoint(evento.pos):
                            return "reiniciar"
                        if botao_fechar.collidepoint(evento.pos):
                            pygame.quit()
                            sys.exit()
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

                if reconhecido == "fechar":
                    pygame.quit()
                    sys.exit()
                elif reconhecido == "reiniciar":
                    return "reiniciar"



def main():
    tela = iniciarJanela()

    while True:
        nomeJogador = telaInicial(tela)
        print(f"Jogador: {nomeJogador}")

        telaDeBoasVindas(tela, nomeJogador)

        pygame.mixer.music.stop()

        resultado = gameplay(tela, nomeJogador)

        if resultado != "reiniciar":
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
