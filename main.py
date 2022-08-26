import pygame
from sys import exit

width = 1000
height = int((width * (9/16)))
cores = {
	'branco': (255, 255, 255),
	'preto': (0, 0, 0),
	'bubblegum': (232, 60, 58),
	'darkestsky': (5, 4, 10),
	'dutch': (5, 106, 160),
	'slipslide': (51, 176, 194),
	'today': (196, 238, 218)
}


# def centro(surface):
# 	halfw = surface.get_width // 2
# 	halfh = surface.get_height // 2
# 	return tuple((halfw, halfh))

class Background:
	def __init__(self):
		self.surf = pygame.Surface((width, height))
		self.surf.fill(cores['darkestsky'])


class Tabuleiro:

	class Bloco:

		def surfslc(self):
			return pygame.image.load('graphics/chao/chao_slc.png').convert()

		def __init__(self, x, y):
			self.surf = pygame.image.load('graphics/chao/chao.png').convert()
			self.rect = self.surf.get_rect(topleft=(x, y))
			self.conteudo = None

	def gerargrade(self):
		grade = list()
		bloco_tam = self.tam[0] // 10
		for y in range(0, self.tam[1], bloco_tam):
			linha = list()
			for x in range(0, self.tam[0], bloco_tam):
				bloco = self.Bloco(x, y)
				linha.append(bloco)
			grade.append(tuple(linha))
		self.__setattr__('grade', tuple(grade))

	def blitgrade(self):
		for linha in self.grade:
			for bloco in linha:
				self.surf.blit(bloco.surf, bloco.rect)

	def __init__(self):
		self.tam = (500, 500)
		self.surf = pygame.Surface(self.tam)
		self.surf.fill(cores['branco'])
		self.rect = self.surf.get_rect(center=(width // 2, height // 2))
		self.grade = None
		self.gerargrade()
		# self.blitgrade()

	def blitobj(self, objeto, celula):
		self.surf.blit(self.grade[celula[0]][celula[1]].surf, self.grade[celula[0]][celula[1]].rect)
		objeto.draw(self.grade[celula[0]][celula[1]].surf)

	def blitchao(self, mouse_pos=None):
		nlinhas = len(self.grade)
		for y in range(0, nlinhas):
			for x in range(0, nlinhas):
				bloco = self.grade[x][y]
				if mouse_pos:
					if bloco.rect.collidepoint(mouse_pos):
						# print(x, y, mouse_pos)
						self.surf.blit(bloco.surfslc(), bloco.rect)
					else:
						self.surf.blit(bloco.surf, bloco.rect)
				else:
					self.surf.blit(bloco.surf, bloco.rect)

	def slcbloco(self, mouse_pos):
		nlinhas = len(self.grade)
		for y in range(0, nlinhas):
			for x in range(0, nlinhas):
				bloco = self.grade[x][y]
				if bloco.rect.collidepoint(mouse_pos):
					return bloco

	def moverobj(self, obj, pos):
		if obj.pos:
			bloco = self.grade[obj.pos[0]][obj.pos[1]]
		else:
			bloco = None
		novobloco = self.grade[pos[0]][pos[1]]
		if not novobloco.conteudo:
			if bloco:
				bloco.conteudo = None
			novobloco.conteudo = obj
			obj.pos = pos
			obj.bloco = novobloco
		else:
			print('bloco ocupado')


class Aliado(pygame.sprite.Sprite):
	def __init__(self, pos=None):
		super().__init__()
		self.image = pygame.image.load('graphics/aliados/aliado.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.pos = pos
		self.bloco = None


class Inimigo(pygame.sprite.Sprite):
	def __init__(self, pos=None):
		super().__init__()
		self.image = pygame.image.load('graphics/inimigos/inimigo.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.pos = pos
		self.bloco = None


pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Jogo')
clock = pygame.time.Clock()

movimento_mode = False

bg = Background()
tabuleiro = Tabuleiro()

aliado1 = Aliado()
aliados = pygame.sprite.Group()
aliados.add(aliado1)
inimigo1 = Inimigo()
inimigos = pygame.sprite.Group()
inimigos.add(inimigo1)

tabuleiro.moverobj(aliado1, (4, 2))
tabuleiro.moverobj(inimigo1, (4, 6))

mouse_pos = (0, 0)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		elif event.type == pygame.MOUSEMOTION:
			mouse_pos = pygame.mouse.get_pos()
			mouse_pos = (mouse_pos[0]-250, mouse_pos[1]-30)
		elif event.type == pygame.MOUSEBUTTONUP:
			bloco = tabuleiro.slcbloco(mouse_pos)
			if bloco.conteudo:
				obj = bloco.conteudo
				movimento_mode = True

	screen.blit(bg.surf, (0, 0))
	screen.blit(tabuleiro.surf, tabuleiro.rect)

	if movimento_mode:
		tabuleiro.blitchao(mouse_pos)
	else:
		tabuleiro.blitchao()

	aliados.draw(aliado1.bloco.surf)
	inimigos.draw(inimigo1.bloco.surf)

	pygame.display.update()
	clock.tick(60)

