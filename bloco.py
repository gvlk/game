import pygame


class Bloco(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		imgdef = pygame.image.load('graphics/chao/chao.png')
		imgslc = pygame.image.load('graphics/chao/chao_slc.png')
		imgind = pygame.image.load('graphics/chao/chao_ind.png')
		imgmse = pygame.image.load('graphics/chao/chao_mse.png')
		imgmov = pygame.image.load('graphics/chao/chao_mov.png')
		imgmovslc = pygame.image.load('graphics/chao/chao_movslc.png')
		imgdef = pygame.transform.scale(imgdef, pygame.math.Vector2(imgdef.get_size()) * 4).convert_alpha()
		imgslc = pygame.transform.scale(imgslc, pygame.math.Vector2(imgslc.get_size()) * 4).convert_alpha()
		imgind = pygame.transform.scale(imgind, pygame.math.Vector2(imgind.get_size()) * 4).convert_alpha()
		imgmse = pygame.transform.scale(imgmse, pygame.math.Vector2(imgmse.get_size()) * 4).convert_alpha()
		imgmov = pygame.transform.scale(imgmov, pygame.math.Vector2(imgmov.get_size()) * 4).convert_alpha()
		imgmovslc = pygame.transform.scale(imgmovslc, pygame.math.Vector2(imgmovslc.get_size()) * 4).convert_alpha()
		self.imgs = {'def': imgdef, 'slc': imgslc, 'ind': imgind, 'mse': imgmse, 'mov': imgmov, 'movslc': imgmovslc}
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]
		self.rect = self.image.get_rect(topleft=(x, y))
		self.conteudo = None
		self.ind = False
		self.gcost = int()
		self.hcost = int()
		self.fcost = int()
		self.parent = None

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

	def imgmse(self):
		if self.imgatual != 'mse':
			self.imgatual = 'mse'
			self.image = self.imgs[self.imgatual]

	def imgmov(self):
		if self.imgatual != 'mov':
			self.imgatual = 'mov'
			self.image = self.imgs[self.imgatual]

	def imgmovslc(self):
		if self.imgatual != 'movslc':
			self.imgatual = 'movslc'
			self.image = self.imgs[self.imgatual]
