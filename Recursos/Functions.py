import pygame

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





