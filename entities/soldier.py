import pygame
from random import randint


class Soldier(pygame.sprite.Sprite):

	def __init__(self, name: str, team: str):
		super().__init__()
		self.name = name
		self.team = team
		self.atr = {  # Atributos do personagem
			'mhp': 8,
			'spd': 4,
			'dmg': (1, 3),  # Dano mínimo e máximo
			'acc': 3,
			'crt': 3  # Porcentagem de acerto crítico
		}
		self.imgs: dict = self.getSkin()
		self.current_img = 'def'
		shadow = pygame.image.load('assets/images/extras/shadow.png')
		self.shadow_surf = pygame.transform.scale(shadow, pygame.math.Vector2(shadow.get_size()) * 4).convert_alpha()
		self.shadow_rect = self.shadow_surf.get_rect()
		self.image = self.imgs[self.current_img]
		self.rect = self.image.get_rect()
		self.pos = None
		self.tile = None
		self.aim = None
		self.area = pygame.sprite.Group()  # Grupo de sprites do chão o qual esse objeto causa a renderização
		self.current_health = self.atr['mhp']
		self.health_bar_length = 10
		self.health_ratio = self.atr['mhp'] / self.health_bar_length
		self.hb_show = False
		self.hb_size = None
		self.hb_pos = None
		self.hb_rect = None
		self.hb_b_rect = pygame.Rect((0, 0), (10, (self.current_health / self.health_ratio) * 5))  # Barra vermelha)
		self.healthbarUpdate()
		self.paths = dict()  # Dicionário destino: caminho
		self.active_path = list()
		self.blocked_paths = dict()
		self.xprox = int()
		self.yprox = int()
		self.velmov = 5
		self.hit_chances = dict()

	def __str__(self) -> str:
		return f'{self.name}, HP: {self.current_health}'

	def getSkin(self) -> dict:
		if self.team == 'A':
			imgdef = pygame.image.load('assets/images/soldier/soldier_A.png')
			imgslc = pygame.image.load('assets/images/soldier/soldier_slc_A.png')
			imgatk = pygame.image.load('assets/images/soldier/soldier_atk_A.png')
		else:
			imgdef = pygame.image.load('assets/images/soldier/soldier_B.png')
			imgslc = pygame.image.load('assets/images/soldier/soldier_slc_B.png')
			imgatk = pygame.image.load('assets/images/soldier/soldier_atk_B.png')
		imgdef = pygame.transform.scale(imgdef, pygame.math.Vector2(imgdef.get_size()) * 4).convert_alpha()
		imgslc = pygame.transform.scale(imgslc, pygame.math.Vector2(imgslc.get_size()) * 4).convert_alpha()
		imgatk = pygame.transform.scale(imgatk, pygame.math.Vector2(imgatk.get_size()) * 4).convert_alpha()
		return {'def': imgdef, 'slc': imgslc, 'atk': imgatk}

	def update(self) -> None:
		self.aim = None
		self.rect = self.image.get_rect(midbottom=self.tile.rect.midbottom)
		self.shadow_rect = self.shadow_surf.get_rect(midbottom=self.tile.rect.midbottom)
		self.healthbarUpdate()

	def imageUpdate(self, mode: str = 'def') -> None:
		if self.current_img != mode:
			self.current_img = mode
			self.image = self.imgs[mode]

	def healthbarUpdate(self) -> None:
		self.hb_size = (10, (self.current_health / self.health_ratio) * 5)  # Barra vermelha
		self.hb_pos = (self.rect.x + self.rect.w - 20, self.rect.y + self.rect.h - 70)
		self.hb_rect = pygame.Rect(self.hb_pos, self.hb_size)
		self.hb_b_rect = pygame.Rect(self.hb_pos, self.hb_b_rect.size)  # Borda preta
		self.hb_rect.bottom = self.hb_b_rect.bottom  # Reposicionar barra vermelha

	def getDamage(self, valor) -> None:
		if self.current_health > 0:
			self.current_health -= valor
		else:
			self.current_health = 0

	def getHealth(self, valor) -> None:
		if self.current_health < self.atr['mhp']:
			self.current_health += valor
		else:
			self.current_health = self.atr['mhp']

	def atack(self) -> bool:
		c = randint(1, 100)
		if c <= self.hit_chances[self.aim]:
			dano = randint(self.atr['dmg'][0], self.atr['dmg'][1])
			c = randint(1, 100)
			if c <= self.atr['crt']:  # Crítico
				dano = self.atr['dmg'][1] + round(dano * 1.4)
			self.aim.getDamage(dano)
			if not self.aim.hb_show:
				self.aim.hb_show = True
			self.aim.update()
			self.update()  # Talvez não seja necessário
			return True
		return False

	def getHitChances(self, soldado, dst: int) -> int:
		chance = round(75 - ((dst ** 2) / 150) + (3 * self.atr['acc']))
		self.hit_chances[soldado] = chance
		return chance

	def move(self, blocodestino=None) -> bool:
		if blocodestino is None:
			vetor = pygame.math.Vector2()
			self.xprox = self.active_path[0].rect.midbottom[0]
			self.yprox = self.active_path[0].rect.midbottom[1]

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

			if vetor == self.tile.rect.midbottom:
				self.update()
				return True
			elif vetor == (self.xprox, self.yprox):
				self.active_path.pop(0)

			self.rect = self.image.get_rect(midbottom=vetor)
			self.shadow_rect = self.shadow_surf.get_rect(midbottom=vetor)
			self.healthbarUpdate()
		else:
			self.active_path = list(self.paths[blocodestino])

	# def rotate(self):
	# 	if self.aim in self.miraangulos:
	# 		self.image = self.miraangulos[self.aim]['surf']
	# 		self.rect = self.miraangulos[self.aim]['rect']
	# 	else:
	# 		vetor1x, vetor1y = self.rect.center
	# 		vetor2x, vetor2y = self.aim.rect.center
	# 		angulo = atan2(vetor2y - vetor1y, vetor2x - vetor1x)
	# 		if radians(-89) < angulo < radians(91):  # Não precisa inverter horizontalmente
	# 			angulo = -degrees(angulo)
	# 			img = self.imgs[self.current_img]
	# 		else:
	# 			angulo = -degrees(angulo) + 180
	# 			img = pygame.transform.flip(self.imgs[self.current_img], flip_x=True, flip_y=False)
	#
	# 		rotsurf = pygame.transform.rotate(img, angulo)
	# 		rotrect = rotsurf.get_rect(center=self.rect.center)
	# 		self.miraangulos[self.aim] = {'surf': rotsurf, 'rect': rotrect}
	# 		self.image = rotsurf
	# 		self.rect = rotrect
