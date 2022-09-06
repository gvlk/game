import pygame
from math import atan2, degrees, radians


class Aliado(pygame.sprite.Sprite):
	def __init__(self, nome, pos=None):
		super().__init__()
		imgdef = pygame.image.load('graphics/aliados/aliado.png')
		imgslc = pygame.image.load('graphics/aliados/aliado_slc.png')
		imgatk = pygame.image.load('graphics/aliados/aliado_atk.png')
		sombra = pygame.image.load('graphics/detalhes/sombra1.png')
		imgdef = pygame.transform.scale(imgdef, pygame.math.Vector2(imgdef.get_size()) * 4).convert_alpha()
		imgslc = pygame.transform.scale(imgslc, pygame.math.Vector2(imgslc.get_size()) * 4).convert_alpha()
		imgatk = pygame.transform.scale(imgatk, pygame.math.Vector2(imgatk.get_size()) * 4).convert_alpha()
		self.sombra_surf = pygame.transform.scale(sombra, pygame.math.Vector2(sombra.get_size()) * 4).convert_alpha()
		self.sombra_rect = self.sombra_surf.get_rect()
		self.imgs = {'def': imgdef, 'slc': imgslc, 'atk': imgatk}
		self.imgf = {'def': self.imgdef, 'slc': self.imgslc, 'atk': self.imgatk}
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]
		self.mask = pygame.mask.from_surface(self.image)
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
		self.hb_show = False
		self.hb_size = (10, (self.current_health / self.health_ratio) * 5)  # Barra vermelha
		self.hb_pos = (self.rect.x, self.rect.y)
		self.hrect = pygame.Rect(self.hb_pos, self.hb_size)
		self.hbbrect = pygame.Rect(self.hb_pos, (self.health_bar_length, self.hb_size[1]))  # Borda preta
		self.hrect.bottom = self.hbbrect.bottom  # Reposicionar barra vermelha
		self.spd = 3
		self.areamov = set()
		self.caminhos = dict()  # Dicionário destino: caminho
		self.caminhoativo = list()
		self.caminhosind = dict()
		self.xprox = int()
		self.yprox = int()
		self.velmov = 4

	def update(self, img: str = 'def', rot: bool = True, movimentar=False, blocodestino=None):
		"""
		Atualizar a posição do sprite para o bloco atual entre outras coisas
		"""
		self.imgf[img]()
		if movimentar:
			self.movimentar(blocodestino)
		else:
			self.rect = self.image.get_rect(midbottom=self.bloco.rect.midbottom)
			self.sombra_rect = self.sombra_surf.get_rect(midbottom=self.bloco.rect.midbottom)
			self.hb_size = (10, (self.current_health / self.health_ratio) * 5)  # Barra vermelha
			self.hb_pos = (self.rect.x + self.rect.w - 20, self.rect.y + self.rect.h - 70)
			self.hrect = pygame.Rect(self.hb_pos, self.hb_size)
			self.hbbrect = pygame.Rect(self.hb_pos, self.hbbrect.size)  # Borda preta
			self.hrect.bottom = self.hbbrect.bottom  # Reposicionar barra vermelha
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

	def movimentar(self, blocodestino=None):
		vetor = pygame.math.Vector2()
		if blocodestino:
			self.caminhoativo = list(self.caminhos[blocodestino])
		else:
			self.xprox = self.caminhoativo[0].rect.midbottom[0]
			self.yprox = self.caminhoativo[0].rect.midbottom[1]

			if self.rect.midbottom[0] - self.velmov > self.xprox:
				vetor.x = self.rect.midbottom[0] - self.velmov
			elif self.rect.midbottom[0] + self.velmov < self.xprox:
				vetor.x = self.rect.midbottom[0] + self.velmov
			else:
				vetor.x = self.xprox
			if self.rect.midbottom[1] - self.velmov > self.yprox:
				vetor.y = self.rect.midbottom[1] - self.velmov
			elif self.rect.midbottom[1] + self.velmov < self.yprox:
				vetor.y = self.rect.midbottom[1] + self.velmov
			else:
				vetor.y = self.yprox

			if vetor == self.bloco.rect.midbottom:
				self.update()
				return True
			elif vetor == (self.xprox, self.yprox):
				self.caminhoativo.pop(0)

			self.rect = self.image.get_rect(midbottom=vetor)
			self.sombra_rect = self.sombra_surf.get_rect(midbottom=vetor)
			self.hb_pos = (self.rect.x + self.rect.w - 20, self.rect.y + self.rect.h - 70)
			self.hrect = pygame.Rect(self.hb_pos, self.hb_size)
			self.hbbrect = pygame.Rect(self.hb_pos, self.hbbrect.size)  # Borda preta
			self.hrect.bottom = self.hbbrect.bottom  # Reposicionar barra vermelha

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
		imgdef = pygame.image.load('graphics/inimigos/inimigo.png')
		imgslc = pygame.image.load('graphics/inimigos/inimigo_slc.png')
		imgatk = pygame.image.load('graphics/inimigos/inimigo_atk.png')
		sombra = pygame.image.load('graphics/detalhes/sombra1.png')
		imgdef = pygame.transform.scale(imgdef, pygame.math.Vector2(imgdef.get_size()) * 4).convert_alpha()
		imgslc = pygame.transform.scale(imgslc, pygame.math.Vector2(imgslc.get_size()) * 4).convert_alpha()
		imgatk = pygame.transform.scale(imgatk, pygame.math.Vector2(imgatk.get_size()) * 4).convert_alpha()
		self.sombra_surf = pygame.transform.scale(sombra, pygame.math.Vector2(sombra.get_size()) * 4).convert_alpha()
		self.sombra_rect = self.sombra_surf.get_rect()
		self.imgs = {'def': imgdef, 'slc': imgslc, 'atk': imgatk}
		self.imgf = {'def': self.imgdef, 'slc': self.imgslc, 'atk': self.imgatk}
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]
		self.mask = pygame.mask.from_surface(self.image)
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
		self.hb_show = False
		self.hb_size = (10, (self.current_health / self.health_ratio) * 5)  # Barra vermelha
		self.hb_pos = (self.rect.x, self.rect.y)
		self.hrect = pygame.Rect(self.hb_pos, self.hb_size)
		self.hbbrect = pygame.Rect(self.hb_pos, (self.health_bar_length, self.hb_size[1]))  # Borda preta
		self.hrect.bottom = self.hbbrect.bottom  # Reposicionar barra vermelha
		self.spd = 3
		self.areamov = set()
		self.caminhos = dict()
		self.caminhoativo = list()
		self.caminhosind = dict()
		self.xprox = int()
		self.yprox = int()
		self.velmov = 4

	def update(self, img: str = 'def', rot: bool = True, movimentar=False, blocodestino=None):
		"""
		Atualizar a posição do sprite para o bloco atual entre outras coisas
		"""
		self.imgf[img]()
		if movimentar:
			self.movimentar(blocodestino)
		else:
			self.rect = self.image.get_rect(midbottom=self.bloco.rect.midbottom)
			self.sombra_rect = self.sombra_surf.get_rect(midbottom=self.bloco.rect.midbottom)
			self.hb_size = (10, (self.current_health / self.health_ratio) * 5)  # Barra vermelha
			self.hb_pos = (self.rect.x + self.rect.w - 20, self.rect.y + self.rect.h - 70)
			self.hrect = pygame.Rect(self.hb_pos, self.hb_size)
			self.hbbrect = pygame.Rect(self.hb_pos, self.hbbrect.size)  # Borda preta
			self.hrect.bottom = self.hbbrect.bottom  # Reposicionar barra vermelha
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

	def movimentar(self, blocodestino=None):
		vetor = pygame.math.Vector2()
		if blocodestino:
			self.caminhoativo = list(self.caminhos[blocodestino])
		else:
			self.xprox = self.caminhoativo[0].rect.midbottom[0]
			self.yprox = self.caminhoativo[0].rect.midbottom[1]

			if self.rect.midbottom[0] - self.velmov > self.xprox:
				vetor.x = self.rect.midbottom[0] - self.velmov
			elif self.rect.midbottom[0] + self.velmov < self.xprox:
				vetor.x = self.rect.midbottom[0] + self.velmov
			else:
				vetor.x = self.xprox
			if self.rect.midbottom[1] - self.velmov > self.yprox:
				vetor.y = self.rect.midbottom[1] - self.velmov
			elif self.rect.midbottom[1] + self.velmov < self.yprox:
				vetor.y = self.rect.midbottom[1] + self.velmov
			else:
				vetor.y = self.yprox

			if vetor == self.bloco.rect.midbottom:
				self.update()
				return True
			elif vetor == (self.xprox, self.yprox):
				self.caminhoativo.pop(0)

			self.rect = self.image.get_rect(midbottom=vetor)
			self.sombra_rect = self.sombra_surf.get_rect(midbottom=vetor)
			self.hb_pos = (self.rect.x + self.rect.w - 20, self.rect.y + self.rect.h - 70)
			self.hrect = pygame.Rect(self.hb_pos, self.hb_size)
			self.hbbrect = pygame.Rect(self.hb_pos, self.hbbrect.size)  # Borda preta
			self.hrect.bottom = self.hbbrect.bottom  # Reposicionar barra vermelha

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
