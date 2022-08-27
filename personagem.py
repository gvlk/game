import pygame


class Aliado(pygame.sprite.Sprite):
	def __init__(self, nome, pos=None):
		super().__init__()
		imgdef = pygame.image.load('graphics/aliados/aliado.png').convert_alpha()
		imgslc = pygame.image.load('graphics/aliados/aliado_slc.png').convert_alpha()
		self.imgs = {'def': imgdef, 'slc': imgslc}
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]
		self.rect = self.image.get_rect()
		self.pos = pos
		self.nome = nome
		self.bloco = None

	def update(self):
		"""
		Atualizar a posição do sprite para o bloco atual e retorna para a imagem padrão
		"""
		self.rect = self.image.get_rect(topleft=(self.bloco.rect.x, self.bloco.rect.y))
		self.imgdef()

	def imgslc(self):
		self.imgatual = 'slc'
		self.image = self.imgs[self.imgatual]

	def imgdef(self):
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]


class Inimigo(pygame.sprite.Sprite):
	def __init__(self, nome, pos=None):
		super().__init__()
		imgdef = pygame.image.load('graphics/inimigos/inimigo.png').convert_alpha()
		imgslc = pygame.image.load('graphics/inimigos/inimigo_slc.png').convert_alpha()
		self.imgs = {'def': imgdef, 'slc': imgslc}
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]
		self.rect = self.image.get_rect()
		self.pos = pos
		self.nome = nome
		self.bloco = None

	def update(self):
		self.rect = self.image.get_rect(topleft=(self.bloco.rect.x, self.bloco.rect.y))
		self.imgdef()

	def imgslc(self):
		self.imgatual = 'slc'
		self.image = self.imgs[self.imgatual]

	def imgdef(self):
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]
