import pygame


class Bloco(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		imgdef = pygame.image.load('graphics/chao/chao.png')
		imgslc = pygame.image.load('graphics/chao/chao_slc.png')
		imgind = pygame.image.load('graphics/chao/chao_ind.png')
		imgdef = pygame.transform.scale(imgdef, pygame.math.Vector2(imgdef.get_size()) * 4).convert_alpha()
		imgslc = pygame.transform.scale(imgslc, pygame.math.Vector2(imgslc.get_size()) * 4).convert_alpha()
		imgind = pygame.transform.scale(imgind, pygame.math.Vector2(imgind.get_size()) * 4).convert_alpha()
		self.imgs = {'def': imgdef, 'slc': imgslc, 'ind': imgind}
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]
		self.rect = self.image.get_rect(topleft=(x, y))
		self.conteudo = None
		self.ind = False
		self.gcost = int()
		self.hcost = int()
		self.fcost = int()
		self.parent = None
		self.movs = dict()  # Dicionário de movimentos para cada personagem

	def imgdef(self):
		if self.imgatual != 'def':
			self.imgatual = 'def'
			self.image = self.imgs[self.imgatual]

	def imgslc(self):
		if self.imgatual != 'slc':
			self.imgatual = 'slc'
			self.image = self.imgs[self.imgatual]

	def imgind(self):
		if self.imgatual != 'ind':
			self.imgatual = 'ind'
			self.image = self.imgs[self.imgatual]


