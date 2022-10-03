import pygame
from random import randint


class Soldado(pygame.sprite.Sprite):

	def __init__(self, nome: str, time: str):
		super().__init__()
		self.nome = nome
		self.time = time
		self.atr = {  # Atributos do personagem
			'mhp': 8,
			'spd': 4,
			'dmg': (1, 3),  # Dano mínimo e máximo
			'acc': 3,
			'crt': 3  # Porcentagem de acerto crítico
		}
		self.imgs: dict = dict()
		self.sombra_surf = None
		self.sombra_rect = None
		self.getskin()
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]
		self.rect = self.image.get_rect()
		self.pos = None
		self.bloco = None
		self.mira = None
		self.imgf = {'def': self.imgdef, 'slc': self.imgslc, 'atk': self.imgatk}
		self.area = pygame.sprite.Group()  # Grupo de sprites do chão o qual esse objeto causa a renderização
		self.current_health = self.atr['mhp']
		self.health_bar_length = 10
		self.health_ratio = self.atr['mhp'] / self.health_bar_length
		self.hb_show = False
		self.hb_size = None
		self.hb_pos = None
		self.hrect = None
		self.hbbrect = pygame.Rect((0, 0), (10, (self.current_health / self.health_ratio) * 5))  # Barra vermelha)
		self.healthbarupdate()
		self.caminhos = dict()  # Dicionário destino: caminho
		self.caminhoativo = list()
		self.caminhosind = dict()
		self.xprox = int()
		self.yprox = int()
		self.velmov = 5
		self.hitchances = dict()

	def __str__(self):
		return f'{self.nome}, HP: {self.current_health}'

	def getskin(self):
		if self.time == 'A':
			imgdef = pygame.image.load('assets/images/aliados/aliado.png')
			imgslc = pygame.image.load('assets/images/aliados/aliado_slc.png')
			imgatk = pygame.image.load('assets/images/aliados/aliado_atk.png')
		else:
			imgdef = pygame.image.load('assets/images/inimigos/inimigo.png')
			imgslc = pygame.image.load('assets/images/inimigos/inimigo_slc.png')
			imgatk = pygame.image.load('assets/images/inimigos/inimigo_atk.png')
		imgdef = pygame.transform.scale(imgdef, pygame.math.Vector2(imgdef.get_size()) * 4).convert_alpha()
		imgslc = pygame.transform.scale(imgslc, pygame.math.Vector2(imgslc.get_size()) * 4).convert_alpha()
		imgatk = pygame.transform.scale(imgatk, pygame.math.Vector2(imgatk.get_size()) * 4).convert_alpha()
		sombra = pygame.image.load('assets/images/detalhes/sombra1.png')
		self.imgs = {'def': imgdef, 'slc': imgslc, 'atk': imgatk}
		self.sombra_surf = pygame.transform.scale(sombra, pygame.math.Vector2(sombra.get_size()) * 4).convert_alpha()
		self.sombra_rect = self.sombra_surf.get_rect()

	def update(self, img: str = 'def'):
		"""
		Atualizar a posição do sprite para o bloco atual entre outras coisas
		"""
		self.imgf[img]()
		self.mira = None
		self.rect = self.image.get_rect(midbottom=self.bloco.rect.midbottom)
		self.sombra_rect = self.sombra_surf.get_rect(midbottom=self.bloco.rect.midbottom)
		self.healthbarupdate()

	def healthbarupdate(self):
		self.hb_size = (10, (self.current_health / self.health_ratio) * 5)  # Barra vermelha
		self.hb_pos = (self.rect.x + self.rect.w - 20, self.rect.y + self.rect.h - 70)
		self.hrect = pygame.Rect(self.hb_pos, self.hb_size)
		self.hbbrect = pygame.Rect(self.hb_pos, self.hbbrect.size)  # Borda preta
		self.hrect.bottom = self.hbbrect.bottom  # Reposicionar barra vermelha

	def get_damage(self, valor):
		if self.current_health > 0:
			self.current_health -= valor
		else:
			self.current_health = 0

	def get_health(self, valor):
		if self.current_health < self.atr['mhp']:
			self.current_health += valor
		else:
			self.current_health = self.atr['mhp']

	def atacar(self):
		c = randint(1, 100)
		if c <= self.hitchances[self.mira]:
			dano = randint(self.atr['dmg'][0], self.atr['dmg'][1])
			c = randint(1, 100)
			if c <= self.atr['crt']:  # Crítico
				dano = self.atr['dmg'][1] + round(dano * 1.4)
			self.mira.get_damage(dano)
			if not self.mira.hb_show:
				self.mira.hb_show = True
			self.mira.update()
			self.update()  # Talvez não seja necessário
			return True
		return False

	def gethitchances(self, soldado, dst: int) -> int:
		chance = round(75 - ((dst ** 2) / 150) + (3 * self.atr['acc']))
		self.hitchances[soldado] = chance
		return chance

	def movimentar(self, blocodestino=None) -> bool:
		if blocodestino is None:
			vetor = pygame.math.Vector2()
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
			self.healthbarupdate()
		else:
			self.caminhoativo = list(self.caminhos[blocodestino])

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

	# def rotate(self):
	# 	if self.mira in self.miraangulos:
	# 		self.image = self.miraangulos[self.mira]['surf']
	# 		self.rect = self.miraangulos[self.mira]['rect']
	# 	else:
	# 		vetor1x, vetor1y = self.rect.center
	# 		vetor2x, vetor2y = self.mira.rect.center
	# 		angulo = atan2(vetor2y - vetor1y, vetor2x - vetor1x)
	# 		if radians(-89) < angulo < radians(91):  # Não precisa inverter horizontalmente
	# 			angulo = -degrees(angulo)
	# 			img = self.imgs[self.imgatual]
	# 		else:
	# 			angulo = -degrees(angulo) + 180
	# 			img = pygame.transform.flip(self.imgs[self.imgatual], flip_x=True, flip_y=False)
	#
	# 		rotsurf = pygame.transform.rotate(img, angulo)
	# 		rotrect = rotsurf.get_rect(center=self.rect.center)
	# 		self.miraangulos[self.mira] = {'surf': rotsurf, 'rect': rotrect}
	# 		self.image = rotsurf
	# 		self.rect = rotrect
