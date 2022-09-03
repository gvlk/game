import pygame
from math import atan2, degrees, radians


class Aliado(pygame.sprite.Sprite):
	def __init__(self, nome, pos=None):
		super().__init__()
		imgdef = pygame.image.load('graphics/aliados/aliado.png').convert_alpha()
		imgslc = pygame.image.load('graphics/aliados/aliado_slc.png').convert_alpha()
		imgatk = pygame.image.load('graphics/aliados/aliado_atk.png').convert_alpha()
		self.imgs = {'def': imgdef, 'slc': imgslc, 'atk': imgatk}
		self.imgf = {'def': self.imgdef, 'slc': self.imgslc, 'atk': self.imgatk}
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]
		self.rect = self.image.get_rect()
		self.pos = pos
		self.nome = nome
		self.bloco = None
		self.mira: Aliado | Inimigo | None = None
		self.miraangulos = dict()
		self.area = pygame.sprite.Group()  # Grupo de sprites do chão o qual esse objeto causa a renderização
		self.current_health = 8
		self.maximum_health = 8
		self.health_bar_length = 10
		self.health_ratio = self.maximum_health / self.health_bar_length
		self.hb_show = True
		self.hb_pos = None
		self.hb_xy = None
		self.hrect = None
		self.hbbrect = None
		self.spd = 7
		self.areamov = set()

	def update(self, img: str = 'def', rot: bool = True):
		"""
		Atualizar a posição do sprite para o bloco atual entre outras coisas
		"""
		self.imgf[img]()
		self.rect = self.image.get_rect(midbottom=(self.bloco.rect.midbottom))
		self.hb_xy = ((self.current_health / self.health_ratio) * 5, 10)
		self.hb_pos = (self.rect.x + 7, self.rect.y - self.hb_xy[1])
		self.hrect = pygame.Rect(self.hb_pos, self.hb_xy)
		self.hbbrect = pygame.Rect(self.hb_pos, (self.health_bar_length * 5, self.hb_xy[1]))
		self.mira = None
		if rot:
			self.miraangulos.clear()

	def imgdef(self):
		if self.imgatual != 'def':
			self.imgatual = 'def'
			self.image = self.imgs[self.imgatual]

	def imgslc(self):
		if self.imgatual != 'slc':
			self.imgatual = 'slc'
			self.image = self.imgs[self.imgatual]

	def imgatk(self):
		if self.imgatual != 'atk':
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

	def atacar(self, valor: int = 1):
		self.mira.get_damage(valor)
		if self.mira.current_health < self.mira.maximum_health:
			self.mira.hb_show = True
		self.mira.update()

	def rotate(self):
		if self.mira in self.miraangulos:
			self.image = self.miraangulos[self.mira]['surf']
			self.rect = self.miraangulos[self.mira]['rect']
		else:
			vetor1x, vetor1y = self.rect.center
			vetor2x, vetor2y = self.mira.rect.center
			angulo = atan2(vetor2y - vetor1y, vetor2x - vetor1x)
			if radians(-89) < angulo < radians(91):  # Não precisa inverter horizontalmente
				angulo = -degrees(angulo)
				img = self.imgs[self.imgatual]
			else:
				angulo = -degrees(angulo) + 180
				img = pygame.transform.flip(self.imgs[self.imgatual], flip_x=True, flip_y=False)

			rotsurf = pygame.transform.rotate(img, angulo)
			rotrect = rotsurf.get_rect(center=self.rect.center)
			self.miraangulos[self.mira] = {'surf': rotsurf, 'rect': rotrect}
			self.image = rotsurf
			self.rect = rotrect


class Inimigo(pygame.sprite.Sprite):
	def __init__(self, nome, pos=None):
		super().__init__()
		imgdef = pygame.image.load('graphics/inimigos/inimigo.png').convert_alpha()
		imgslc = pygame.image.load('graphics/inimigos/inimigo_slc.png').convert_alpha()
		imgatk = pygame.image.load('graphics/inimigos/inimigo_atk.png').convert_alpha()
		self.imgs = {'def': imgdef, 'slc': imgslc, 'atk': imgatk}
		self.imgf = {'def': self.imgdef, 'slc': self.imgslc, 'atk': self.imgatk}
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]
		self.rect = self.image.get_rect()
		self.pos = pos
		self.nome = nome
		self.bloco = None
		self.mira: Aliado | Inimigo | None = None
		self.miraangulos = dict()
		self.area = pygame.sprite.Group()
		self.current_health = 8
		self.maximum_health = 8
		self.health_bar_length = 10
		self.health_ratio = self.maximum_health / self.health_bar_length
		self.hb_show = True
		self.hb_pos = None
		self.hb_xy = None
		self.hrect = None
		self.hbbrect = None
		self.spd = 3
		self.areamov = set()

	def update(self, img: str = 'def', rot: bool = True):
		"""
		Atualizar a posição do sprite para o bloco atual entre outras coisas
		"""
		self.imgf[img]()
		self.rect = self.image.get_rect(midbottom=self.bloco.rect.midbottom)
		self.hb_xy = ((self.current_health / self.health_ratio) * 5, 10)
		self.hb_pos = (self.rect.x + 7, self.rect.y - self.hb_xy[1])
		self.hrect = pygame.Rect(self.hb_pos, self.hb_xy)
		self.hbbrect = pygame.Rect(self.hb_pos, (self.health_bar_length * 5, self.hb_xy[1]))
		self.mira = None
		if rot:
			self.miraangulos.clear()

	def imgdef(self):
		if self.imgatual != 'def':
			self.imgatual = 'def'
			self.image = self.imgs[self.imgatual]

	def imgslc(self):
		if self.imgatual != 'slc':
			self.imgatual = 'slc'
			self.image = self.imgs[self.imgatual]

	def imgatk(self):
		if self.imgatual != 'atk':
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

	def atacar(self, valor: int = 1):
		self.mira.get_damage(valor)
		if self.mira.current_health < self.mira.maximum_health:
			self.mira.hb_show = True
		self.mira.update()

	def rotate(self):
		if self.mira in self.miraangulos:
			self.image = self.miraangulos[self.mira]['surf']
			self.rect = self.miraangulos[self.mira]['rect']
		else:
			vetor1x, vetor1y = self.rect.center
			vetor2x, vetor2y = self.mira.rect.center
			angulo = atan2(vetor2y - vetor1y, vetor2x - vetor1x)
			if radians(-89) < angulo < radians(91):  # Não precisa inverter horizontalmente
				angulo = -degrees(angulo)
				img = self.imgs[self.imgatual]
			else:
				angulo = -degrees(angulo) + 180
				img = pygame.transform.flip(self.imgs[self.imgatual], flip_x=True, flip_y=False)

			rotsurf = pygame.transform.rotate(img, angulo)
			rotrect = rotsurf.get_rect(center=self.rect.center)
			self.miraangulos[self.mira] = {'surf': rotsurf, 'rect': rotrect}
			self.image = rotsurf
			self.rect = rotrect
