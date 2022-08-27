import pygame
from random import randint

from personagem import Aliado, Inimigo


class Tabuleiro:
	def gerargrade(self):
		from bloco import Bloco
		grade = list()
		sptlist = list()
		for x in range(0, self.tam[0], self.bloco_tam):
			linha = list()
			for y in range(0, self.tam[1], self.bloco_tam):
				bloco = Bloco(x, y)
				sptlist.append(bloco)
				linha.append(bloco)
			grade.append(tuple(linha))
		self.sptchao = pygame.sprite.Group(sptlist)
		self.__setattr__('grade', tuple(grade))

	def __init__(self):
		from main import Setup
		width = Setup.width
		height = Setup.height
		self.width = width // 2
		self.height = self.width
		self.tam = (self.width, self.height)
		self.qnt_blocos = 10
		self.bloco_tam = self.width // self.qnt_blocos
		self.transf = (-(width - self.width) // 2, -(height - self.height) // 2)
		self.surf = pygame.Surface(self.tam)
		self.rect = self.surf.get_rect(center=(width // 2, height // 2))
		self.dictaliados = dict()
		self.dictinimigos = dict()
		self.sptchao = None
		self.sptaliados = pygame.sprite.Group()
		self.sptinimigos = pygame.sprite.Group()
		self.mode_atual = 'def'
		self.mode_tuple = ('def', 'slc', 'mov', 'atk')
		self.mousepos = (-1, -1)
		self.mouseblo = (None, None)
		self.objslc = None
		self.grade = None
		self.gerargrade()

	def mouseslc(self):
		for bloco in self.sptchao:
			if not bloco.rect.collidepoint(self.mousepos):
				bloco.imgdef()
			else:
				if not bloco.conteudo:
					bloco.imgslc()

	def add(self, tipo, nome=None):
		if not nome:
			nome = f'aliado{randint(100, 999)}'
		if tipo == 'ali':
			novoali = Aliado(nome)
			self.dictaliados[nome] = novoali
			self.sptaliados.add(novoali)
			return novoali
		elif tipo == 'ini':
			novoini = Inimigo(nome)
			self.dictinimigos[nome] = novoini
			self.sptinimigos.add(novoini)
			return novoini
		else:
			print('tipo não reconhecido')

	def slcobj(self):
		obj: Aliado | Inimigo
		for obj in self.sptaliados:
			if obj.rect.collidepoint(self.mousepos):
				obj.imgslc()
				return obj
		else:
			return None

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
