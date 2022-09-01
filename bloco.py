import pygame

from tabuleiro import bloco_tam


class Bloco(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		imgdef = pygame.image.load('graphics/chao/chao.png').convert()
		imgslc = pygame.image.load('graphics/chao/chao_slc.png').convert()
		imgind = pygame.image.load('graphics/chao/chao_ind.png').convert()
		self.imgs = {'def': imgdef, 'slc': imgslc, 'ind': imgind}
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]
		self.rect = self.image.get_rect(topleft=(x, y))
		self.conteudo = None
		self.ind = False

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


