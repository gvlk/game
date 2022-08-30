import pygame
from math import atan2, degrees

from tabuleiro import bloco_tam


class Aliado(pygame.sprite.Sprite):
	def __init__(self, nome, pos=None):
		super().__init__()
		imgdef = pygame.image.load('graphics/aliados/aliado.png').convert_alpha()
		imgdef = pygame.transform.smoothscale(imgdef, (bloco_tam, bloco_tam))
		imgslc = pygame.image.load('graphics/aliados/aliado_slc.png').convert_alpha()
		imgslc = pygame.transform.smoothscale(imgslc, (bloco_tam, bloco_tam))
		imgatk = pygame.image.load('graphics/aliados/aliado_atk.png').convert_alpha()
		imgatk = pygame.transform.smoothscale(imgatk, (bloco_tam, bloco_tam))
		self.imgs = {'def': imgdef, 'slc': imgslc, 'atk': imgatk}
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]
		self.rect = self.image.get_rect()
		self.pos = pos
		self.nome = nome
		self.bloco = None
		self.mira: Aliado | Inimigo | None = None
		self.current_health = 6
		self.maximum_health = 8
		self.health_bar_length = 10
		self.health_ratio = self.maximum_health / self.health_bar_length

	def update(self):
		"""
		Atualizar a posição do sprite para o bloco atual e retorna para a imagem padrão
		"""
		self.rect = self.image.get_rect(topleft=(self.bloco.rect.x, self.bloco.rect.y))
		self.imgdef()

	def imgdef(self):
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]

	def imgslc(self):
		self.imgatual = 'slc'
		self.image = self.imgs[self.imgatual]

	def imgatk(self):
		self.imgatual = 'atk'
		self.image = self.imgs[self.imgatual]

	def get_damage(self, valor):
		if self.current_health > 0:
			self.current_health -= valor
		else:
			self.current_health = 0

	def get_health(self, valor):
		if self.current_health < self.maximum_health:
			self.current_health += valor
		else:
			self.current_health = self.maximum_health

	def rotate(self):
		if self.mira:
			vetor1x, vetor1y = self.rect.center
			vetor2x, vetor2y = self.mira.rect.center
			angulo = atan2(vetor2y - vetor1y, vetor2x - vetor1x)
			angulo = -degrees(angulo)
			rotsurf = pygame.transform.rotate(self.imgs[self.imgatual], angulo)
			rotrect = rotsurf.get_rect(center=self.rect.center)
			self.image = rotsurf
			self.rect = rotrect


class Inimigo(pygame.sprite.Sprite):
	def __init__(self, nome, pos=None):
		super().__init__()
		imgdef = pygame.image.load('graphics/inimigos/inimigo.png').convert_alpha()
		imgdef = pygame.transform.smoothscale(imgdef, (bloco_tam, bloco_tam))
		imgslc = pygame.image.load('graphics/inimigos/inimigo_slc.png').convert_alpha()
		imgslc = pygame.transform.smoothscale(imgslc, (bloco_tam, bloco_tam))
		imgatk = pygame.image.load('graphics/inimigos/inimigo_atk.png').convert_alpha()
		imgatk = pygame.transform.smoothscale(imgatk, (bloco_tam, bloco_tam))
		self.imgs = {'def': imgdef, 'slc': imgslc, 'atk': imgatk}
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]
		self.rect = self.image.get_rect()
		self.pos = pos
		self.nome = nome
		self.bloco = None
		self.mira: Aliado | Inimigo | None = None
		self.current_health = 6
		self.maximum_health = 8
		self.health_bar_length = 10
		self.health_ratio = self.maximum_health / self.health_bar_length

	def update(self):
		self.rect = self.image.get_rect(topleft=(self.bloco.rect.x, self.bloco.rect.y))
		self.imgdef()

	def imgdef(self):
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]

	def imgslc(self):
		self.imgatual = 'slc'
		self.image = self.imgs[self.imgatual]

	def imgatk(self):
		self.imgatual = 'atk'
		self.image = self.imgs[self.imgatual]

	def rotate(self):
		if self.mira:
			vetor1x, vetor1y = self.rect.center
			vetor2x, vetor2y = self.mira.rect.center
			angulo = atan2(vetor1x - vetor2x, vetor1y - vetor2y)
			self.image = pygame.transform.rotate(self.imgs[self.imgatual], angulo)




