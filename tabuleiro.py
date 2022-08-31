import pygame
from random import randint, choice

from main import s_res

s_w, s_h = s_res
width = s_w
height = width
bloco_qnt = 100
bloco_tam = 64
render_dist = 20

from personagem import Aliado, Inimigo
from bloco import Bloco


class Tabuleiro:
	def gerargrade(self):
		from bloco import Bloco
		grade = list()
		sptlist = list()
		for c in range(0, bloco_qnt):
			x = c * bloco_tam
			coluna = list()
			for l in range(0, bloco_qnt):
				y = l * bloco_tam
				bloco = Bloco(x, y)
				sptlist.append(bloco)
				coluna.append(bloco)
				if len(coluna) == bloco_qnt:
					break
			grade.append(tuple(coluna))
			if len(grade) == bloco_qnt:
				break
		self.sptchao = pygame.sprite.Group(sptlist)
		self.__setattr__('grade', tuple(grade))

	def __init__(self):

		self.transf = (-(s_w - width) // 2, -(s_h - height) // 2)
		self.dictaliados = dict()
		self.dictinimigos = dict()
		self.sptchao = None
		self.sptchaoonscreen = pygame.sprite.Group()
		self.sptaliados = pygame.sprite.Group()
		self.sptinimigos = pygame.sprite.Group()
		self.sptall = pygame.sprite.Group()
		self.mode_atual = 'def'
		self.mode_tuple = ('def', 'slc', 'mov', 'atk')
		self.mousepos = (-1, -1)
		self.mouseblo = (None, None)
		self.objslc = None
		self.grade = None
		self.gerargrade()
		self.width = bloco_qnt * bloco_tam
		self.height = self.width
		self.surf = pygame.Surface((self.width, self.height))
		self.surf.fill('Red')
		self.rect = self.surf.get_rect(center=(width//2, height//2))

	def posicaoinicial(self):
		foco = choice(self.sptaliados.sprites())
		center_posx, center_posy = foco.rect.center
		center_pos = ((s_w / 2) + (self.rect.w / 2) - center_posx, (s_h / 2) + (self.rect.h / 2) - center_posy)
		self.rect = self.surf.get_rect(center=center_pos)

	def add(self, tipo, nome=None):
		if not nome:
			nome = f'aliado{randint(100, 999)}'
		if tipo == 'ali':
			novo = Aliado(nome)
			self.dictaliados[nome] = novo
			self.sptaliados.add(novo)
		elif tipo == 'ini':
			novo = Inimigo(nome)
			self.dictinimigos[nome] = novo
			self.sptinimigos.add(novo)
		else:
			novo = None
			print('tipo não reconhecido')
		self.sptall.add(novo)
		return novo

	def persoslc(self, grupo: str = None):
		obj: Aliado | Inimigo
		if not grupo:
			grupo = self.sptall
		elif grupo == 'ali':
			grupo = self.sptaliados
		elif grupo == 'ini':
			grupo = self.sptinimigos
		for obj in grupo:
			if not obj.rect.collidepoint(self.mousepos):
				obj.imgdef()
			else:
				obj.imgslc()
				if self.mode_atual == 'def':
					self.objslc = obj
				elif self.mode_atual == 'atk':
					self.objslc.mira = obj
					self.objslc.rotate()
		else:
			return None

	def mouseslc(self):
		bloco: Bloco
		for bloco in self.sptchaoonscreen:
			if not bloco.rect.collidepoint(self.mousepos):
				bloco.imgdef()
			else:
				if not bloco.conteudo:
					bloco.imgslc()

	def moverobj(self, obj, pos_d):
		novobloco = self.grade[pos_d[0]][pos_d[1]]
		novobloco.imgdef()
		pos_a = None
		if obj.pos:
			pos_a = obj.pos  # Posição atual será usada para limpar o render depois
			atualbloco = self.grade[pos_a[0]][pos_a[1]]
		else:
			atualbloco = None
		if not novobloco.conteudo:
			if atualbloco:
				atualbloco.conteudo = None
			novobloco.conteudo = obj
			obj.pos = pos_d
			obj.bloco = novobloco
			obj.update()
			self.renderchao(obj, pos_a)
			return True
		else:
			print('bloco ocupado')

	def renderchao(self, lista_objs: list | Aliado | Inimigo, pos_a):
		obj: Aliado | Inimigo
		if type(lista_objs) != list:
			lista_objs = [lista_objs]
		for obj in lista_objs:

			if pos_a:
				max_x = pos_a[0] + render_dist + 1
				min_x = pos_a[0] - render_dist
				max_y = pos_a[1] + render_dist + 1
				min_y = pos_a[1] - render_dist
				if max_x > bloco_qnt:
					max_x = bloco_qnt
				if min_x < 0:
					min_x = 0
				if max_y > bloco_qnt:
					max_y = bloco_qnt
				if min_y < 0:
					min_y = 0
				for y in range(min_y, max_y):
					for x in range(min_x, max_x):
						bloco = self.grade[x][y]
						if len(pygame.sprite.Sprite.groups(bloco)) == 3:  # Grupo chao, chaoonscreen, obj.area
							self.sptchaoonscreen.remove(bloco)
						obj.area.remove(bloco)

			max_x = obj.pos[0] + render_dist + 1
			min_x = obj.pos[0] - render_dist
			max_y = obj.pos[1] + render_dist + 1
			min_y = obj.pos[1] - render_dist
			if max_x > bloco_qnt:
				max_x = bloco_qnt
			if min_x < 0:
				min_x = 0
			if max_y > bloco_qnt:
				max_y = bloco_qnt
			if min_y < 0:
				min_y = 0
			for y in range(min_y, max_y):
				for x in range(min_x, max_x):
					bloco = self.grade[x][y]
					obj.area.add(bloco)
					self.sptchaoonscreen.add(bloco)

