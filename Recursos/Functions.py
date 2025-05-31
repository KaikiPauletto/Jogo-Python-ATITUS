import pygame
import datetime
import sys
import pyttsx3
import speech_recognition as sr
import time

# Função que será usada várias vezes para carregar fontes
def carregarFonte(tamanho=20):
    return pygame.font.Font("Recursos/fontes/Press_Start_2P/PressStart2P-Regular.ttf", tamanho)

# Cores úteis
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)
amarelo = (255, 255, 0)

# Inicializa a janela (usada no main)
def iniciarJanela():
    pygame.init()
    tela = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Meu Jogo Personalizado")
    return tela

# Renderiza texto com quebra automática para não sair da largura max_width
def render_text_wrapped(surface, text, font, color, pos, max_width, line_height=None):
    if line_height is None:
        line_height = font.get_linesize()

    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        test_line = current_line + word + ' '
        width, _ = font.size(test_line)
        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    if current_line:
        lines.append(current_line)

    x, y = pos
    for line in lines:
        rendered_line = font.render(line.strip(), True, color)
        surface.blit(rendered_line, (x, y))
        y += line_height
    
    altura_total = len(lines) * line_height
    return altura_total

def desenhar_botoes_som(tela, som_ativo, posicao=(920, 20)):
    icone = pygame.image.load("Recursos/imagens/Audio_Sim-removebg-preview.png" if som_ativo else "Recursos/imagens/Audio_Não-removebg-preview.png")
    icone = pygame.transform.scale(icone, (40, 40))
    retangulo = icone.get_rect(topleft=posicao)
    tela.blit(icone, retangulo)
    return retangulo

def hitbox_reduzida(rect, reducao_x=10, reducao_y=10):
    nova_largura = max(1, rect.width - reducao_x)
    nova_altura = max(1, rect.height - reducao_y)
    nova_x = rect.x + reducao_x // 2
    nova_y = rect.y + reducao_y // 2
    return pygame.Rect(nova_x, nova_y, nova_largura, nova_altura)

def pausar_jogo(tela, fonte):
    pausa = True

    # Captura o frame atual da tela (congela a imagem)
    tela_congelada = tela.copy()

    texto_pausa = fonte.render("PAUSE", True, (255, 0, 0))
    texto_rect = texto_pausa.get_rect(center=(tela.get_width() // 2, tela.get_height() // 2))

    pygame.mixer.music.pause()

    while pausa:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausa = False
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Redesenha o último frame capturado
        tela.blit(tela_congelada, (0, 0))
        # Desenha a palavra "PAUSE" no centro
        tela.blit(texto_pausa, texto_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unpause()

def registrar_resultado(nome, pontuacao, caminho_log="log.dat"):
    agora = datetime.datetime.now()
    horario = agora.strftime("%H:%M:%S")
    with open(caminho_log, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"Nome: {nome}\nPontuação: {pontuacao:.1f}\nData: {horario}\n\n")

def ler_ultimos_registros(caminho_log="log.dat", n=5):
    try:
        with open(caminho_log, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.read().strip().split("\n\n")
            ultimos = linhas[-n:]
            registros = []
            for entrada in ultimos:
                partes = entrada.strip().split("\n")
                if len(partes) == 3:
                    nome = partes[0].split(":", 1)[1].strip()
                    pontos = partes[1].split(":", 1)[1].strip()
                    horario = partes[2].split(":", 1)[1].strip()
                    registros.append((nome, pontos, horario))
            return registros
    except FileNotFoundError:
        return []

def interacao_por_voz():
    # Inicializa o sintetizador de voz
    engine = pyttsx3.init()
    engine.say("Você perdeu. Se deseja fechar o jogo, fale FECHAR. Se deseja jogar novamente, fale JOGAR NOVAMENTE.")
    engine.runAndWait()

    # Aguarda um momento antes de começar a ouvir
    print("Esperando para escutar...")
    time.sleep(4.5)  # Tempo para o jogador se preparar

    # Inicializa o reconhecedor de voz
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Ouvindo agora...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            comando = recognizer.recognize_google(audio, language="pt-BR")
            print(f"RECONHECIDO (bruto): {comando}")
            comando = comando.lower()

            if "fechar" in comando:
                return "fechar"
            elif "jogar" in comando or "novamente" in comando:
                return "reiniciar"

            else:
                return "desconhecido"
        except sr.UnknownValueError:
            return "desconhecido"
        except sr.WaitTimeoutError:
            return "tempo_esgotado"
        except sr.RequestError:
            return "erro"





