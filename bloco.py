import pygame

from tabuleiro import bloco_tam


class Bloco(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		imgdef = pygame.image.load('graphics/chao/chao.png').convert()
		imgdef = pygame.transform.smoothscale(imgdef, (bloco_tam, bloco_tam))
		imgslc = pygame.image.load('graphics/chao/chao_slc.png').convert()
		imgslc = pygame.transform.smoothscale(imgslc, (bloco_tam, bloco_tam))
		imgmov = pygame.image.load('graphics/chao/chao_mov.png').convert()
		imgmov = pygame.transform.smoothscale(imgmov, (bloco_tam, bloco_tam))
		self.imgs = {'def': imgdef, 'slc': imgslc, 'mov': imgmov}
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]
		self.rect = self.image.get_rect(topleft=(x, y))
		self.conteudo = None
		self.tocando = False

	def imgdef(self):
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]

	def imgslc(self):
		self.imgatual = 'slc'
		self.image = self.imgs[self.imgatual]

	def imgmov(self):
		self.imgatual = 'mov'
		self.image = self.imgs[self.imgatual]


