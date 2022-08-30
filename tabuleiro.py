import pygame
from random import randint

from main import s_res

s_w, s_h = s_res
width = s_w // 3
height = width
bloco_qnt = 10
bloco_tam = width // bloco_qnt

from personagem import Aliado, Inimigo


class Tabuleiro:
	def gerargrade(self):
		from bloco import Bloco
		grade = list()
		sptlist = list()
		for x in range(0, width, bloco_tam):
			coluna = list()
			for y in range(0, height, bloco_tam):
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
		self.sptaliados = pygame.sprite.Group()
		self.sptinimigos = pygame.sprite.Group()
		self.sptall = list()
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
		self.rect = self.surf.get_rect(center=(s_w // 2, s_h // 2))

	# def update(self, width, height):
	# 	self.width = width // 2
	# 	self.height = width
	# 	self.tam = (self.width, self.height)
	# 	self.bloco_tam = self.width // self.qnt_blocos
	# 	self.transf = (-(width - self.width) // 2, -(height - self.height) // 2)
	# 	self.surf = pygame.Surface(self.tam)
	# 	self.rect = self.surf.get_rect(center=(width // 2, height // 2))

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
		self.sptall.append(novo)
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
		for bloco in self.sptchao:
			if not bloco.rect.collidepoint(self.mousepos):
				bloco.imgdef()
			else:
				if not bloco.conteudo:
					bloco.imgslc()

	def moverobj(self, obj, posd):
		novobloco = self.grade[posd[0]][posd[1]]
		novobloco.imgdef()
		if obj.pos:
			atualbloco = self.grade[obj.pos[0]][obj.pos[1]]
		else:
			atualbloco = None
		if not novobloco.conteudo:
			if atualbloco:
				atualbloco.conteudo = None
			novobloco.conteudo = obj
			obj.pos = posd
			obj.bloco = novobloco
			obj.update()
			return True
		else:
			print('bloco ocupado')
