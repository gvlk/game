import pygame
from random import randint
from math import sqrt

bloco_qnt = 5  # Mais 2 tiles externos de borda
bloco_tam = 32
render_dist = 20

from personagem import Aliado, Inimigo
from bloco import Bloco
from camera import CameraGroup


class Tabuleiro:
	def gerargrade(self):
		from bloco import Bloco
		grade = list()
		sptlist = list()
		for c in range(0, bloco_qnt + 2):
			x = c * bloco_tam
			coluna = list()
			for l in range(0, bloco_qnt + 2):
				y = l * bloco_tam
				bloco = Bloco(x, y)
				if l == 0 or l == bloco_qnt + 1 or c == 0 or c == bloco_qnt + 1:
					bloco.imgind()
					bloco.ind = True
				elif (l == 3 or l == 4) and (c == 3 or c == 4):
					bloco.imgind()
					bloco.ind = True
				sptlist.append(bloco)
				coluna.append(bloco)
			grade.append(tuple(coluna))
		self.sptchao = pygame.sprite.Group(sptlist)
		self.__setattr__('grade', tuple(grade))

	def __init__(self):
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
		self.objslc = None
		self.grade = None
		self.width = bloco_qnt * bloco_tam + (2 * bloco_tam)
		self.height = self.width
		self.surf = pygame.Surface((self.width, self.height))
		self.surf.fill('Red')
		self.camera_group = CameraGroup(self.surf)  # Working on it
		self.rect = self.camera_group.tabuleiro_pos()
		self.gerargrade()

	def add(self, tipo: str, nome: str = None):
		if not nome:
			if tipo == 'ali':
				nome = f'aliado{randint(100, 999)}'
			else:
				nome = f'inimigo{randint(100, 999)}'
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
		self.camera_group.add(novo)
		self.sptall.add(novo)
		return novo

	def hoverobj(self, grupo: str = None, click: bool = False):
		"""
		Retorna o objeto apontado pelo mouse
		"""
		obj: Aliado | Inimigo
		alvo: Aliado | Inimigo | None
		if not grupo:
			grupo = self.sptall
		elif grupo == 'ali':
			grupo = self.sptaliados
		elif grupo == 'ini':
			grupo = self.sptinimigos
		for obj in grupo:
			if obj is not self.objslc:
				if not obj.rect.collidepoint(self.mousepos):
					obj.imgdef()
				else:
					obj.imgslc()
					# Em 'atk', quando clica para atacar, o self.objslc não pode mudar
					if self.mode_atual == 'def' or self.mode_atual == 'slc':
						if click:
							self.objslc = obj
					elif self.mode_atual == 'atk':
						if obj is not self.objslc.mira:
							self.objslc.mira = obj
							self.objslc.rotate()
						else:
							return obj
			else:
				obj.imgslc()

		if not click:
			return None
		else:
			return self.objslc

	def hovertile(self):
		"""
		Muda as tiles sob o mouse para 'imgslc'
		"""
		tile: Bloco
		for tile in self.objslc.areamov:
			if not tile.rect.collidepoint(self.mousepos):
				tile.imgdef()
			else:
				tile.imgslc()

	def moverobj(self, obj: Aliado | Inimigo, pos_d: tuple = None) -> bool:
		novobloco: Bloco
		atualbloco: Bloco | None
		if not pos_d:
			pos_d = (self.mousepos[0] // bloco_tam, self.mousepos[1] // bloco_tam)
		try:
			novobloco = self.grade[pos_d[0]][pos_d[1]]
		except IndexError:  # Mouse fora do tabuleiro
			return False
		if novobloco in obj.areamov or not obj.pos:
			pos_a = obj.pos  # Posição atual será usada para limpar o render depois
			if pos_a:
				atualbloco = self.grade[pos_a[0]][pos_a[1]]
				atualbloco.conteudo = None
			else:
				pos_a = None
			novobloco.conteudo = obj
			novobloco.imgdef()
			obj.pos = pos_d
			obj.bloco = novobloco
			obj.update()
			self.gerarmov(obj, pos_a)
			self.renderchao(obj, pos_a)
			self.removermira(obj)
			self.objslc = None
			return True  # Movimento realizado
		else:
			return False  # Tile fora do range do personagem ou ocupado

	def gerarmov(self, obj: Aliado | Inimigo, pos_a: tuple):
		"""
		Gera o range de tiles para o qual o membro pode se movimentar.
		"""
		tile: Bloco
		obj: Aliado | Inimigo
		obj2: Aliado | Inimigo
		obj.areamov.clear()  # Ao invés de começar do zero sempre, pode haver alguma forma de otimização
		obj_posx, obj_posy = obj.pos
		for x in range(obj_posx - obj.spd, obj_posx + obj.spd + 1):
			if x < 1:
				continue
			if x > bloco_qnt:
				break
			for y in range(obj_posy - obj.spd, obj_posy + obj.spd + 1):
				if y < 1:
					continue
				if y > bloco_qnt:
					break
				dis = abs(x - obj.pos[0]) + abs(y - obj.pos[1])
				if 0 < dis <= obj.spd:
					tile = self.grade[x][y]
					if not tile.conteudo and not tile.ind:
						obj.areamov.add(tile)
			# if self.findpath(obj.pos, (x, y)):
			# 	pass

		for obj2 in self.sptall:
			if obj.bloco in obj2.areamov:  # Remover o novo bloco do range dos outros personagens
				obj2.areamov.remove(obj.bloco)
			if self.inobjmov(obj2, pos_a):
				obj2.areamov.add(self.grade[pos_a[0]][pos_a[1]])

	def findpath(self, origem: tuple, destino: tuple):
		tile: Bloco
		vizinho: Bloco
		caminho = list()
		opentiles = list()
		closedtiles = list()
		ngbrs = list()
		origembloco = self.grade[origem[0]][origem[1]]
		origemx, origemy = origembloco.rect.center
		destinobloco = self.grade[destino[0]][destino[1]]
		destinox, destinoy = destinobloco.rect.center
		opentiles.append((origembloco, origem))
		iteracoes = 0

		while True:
			iteracoes += 1
			bloco = opentiles[0]
			tile = bloco[0]
			cordx, cordy = bloco[1]
			opentiles.remove(bloco)
			closedtiles.append(bloco)
			if tile is destinobloco:  # Achou um caminho
				break

			ngbrs.append((self.grade[cordx + 1][cordy], (cordx + 1, cordy)))
			ngbrs.append((self.grade[cordx - 1][cordy], (cordx - 1, cordy)))
			ngbrs.append((self.grade[cordx][cordy + 1], (cordx, cordy + 1)))
			ngbrs.append((self.grade[cordx][cordy - 1], (cordx, cordy - 1)))

			for bloco in ngbrs:
				vizinho = bloco[0]
				if vizinho.conteudo or (bloco in closedtiles) or (bloco in opentiles) or vizinho.ind:
					continue

				vizinho.gcost = int(
					sqrt(((origemx - vizinho.rect.center[0]) ** 2) + ((origemy - vizinho.rect.center[1]) ** 2)))
				vizinho.hcost = int(
					sqrt(((destinox - vizinho.rect.center[0]) ** 2) + ((destinoy - vizinho.rect.center[1]) ** 2)))
				vizinho.fcost = vizinho.gcost + vizinho.hcost
				vizinho.parent = tile
				opentiles.append(bloco)
				opentiles = sorted(opentiles, key=lambda x: x[0].fcost)
			else:
				ngbrs.clear()
		aux: Bloco
		aux = destinobloco
		while aux.parent:
			caminho.append(aux)
			aux = aux.parent
		caminho.reverse()
		caminho = tuple(caminho)
		print(iteracoes)
		for x in caminho:
			print(x.rect.top // 64, x.rect.left // 64)

	@staticmethod
	def inobjmov(obj: Aliado | Inimigo, pos: tuple) -> bool:
		if pos:
			posx, posy = pos
			dis = abs(posx - obj.pos[0]) + abs(posy - obj.pos[1])
			if 0 < dis < obj.spd:
				return True
			else:
				return False
		else:
			return False

	def renderchao(self, lista_objs: list | Aliado | Inimigo, pos_a):
		obj: Aliado | Inimigo
		if type(lista_objs) != list:
			lista_objs = [lista_objs]
		for obj in lista_objs:

			if pos_a:  # Limpar os tiles renderizados na posição antiga
				max_x = pos_a[0] + render_dist + 1
				min_x = pos_a[0] - render_dist
				max_y = pos_a[1] + render_dist + 1
				min_y = pos_a[1] - render_dist
				if max_x > bloco_qnt + 2:
					max_x = bloco_qnt + 2
				if min_x < 0:
					min_x = 0
				if max_y > bloco_qnt + 2:
					max_y = bloco_qnt + 2
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
			if max_x > bloco_qnt + 2:
				max_x = bloco_qnt + 2
			if min_x < 0:
				min_x = 0
			if max_y > bloco_qnt + 2:
				max_y = bloco_qnt + 2
			if min_y < 0:
				min_y = 0
			for y in range(min_y, max_y):
				for x in range(min_x, max_x):
					bloco = self.grade[x][y]
					obj.area.add(bloco)
					self.sptchaoonscreen.add(bloco)
		self.camera_group.ground = self.sptchaoonscreen

	def resettile(self):
		"""
		Tile sob o mouse retorna para 'imgdef'
		"""
		tile: Bloco
		try:
			tile = self.grade[self.mousepos[0] // bloco_tam][self.mousepos[1] // bloco_tam]
		except IndexError:
			pass  # Mouse está fora do tabuleiro
		else:
			if not tile.ind:
				tile.imgdef()

	def tileocupada(self):
		tile: Bloco
		try:
			tile = self.grade[self.mousepos[0] // bloco_tam][self.mousepos[1] // bloco_tam]
		except IndexError:
			return False  # Mouse está fora do tabuleiro
		else:
			if tile.conteudo is None:
				return False
			else:
				return True

	def resetobj(self, obj: Aliado | Inimigo = None, limparslc: bool = False, img: str = 'def', rot: bool = False):
		if not obj:
			if self.objslc:
				obj = self.objslc
			else:
				return None  # Não há objeto para resetar
		obj.update(img=img, rot=rot)
		if limparslc:
			self.objslc = None

	def removermira(self, obj: Aliado | Inimigo = None):
		"""
		Remove o obj do dicionário de mira (cache) dos adversários
		"""
		grupo = None
		perso: Aliado | Inimigo
		if isinstance(obj, Aliado):
			grupo = self.sptinimigos
		elif isinstance(obj, Inimigo):
			grupo = self.sptaliados
		for perso in grupo:
			if obj in perso.miraangulos:
				del perso.miraangulos[obj]

	def ataque(self, atacante: Aliado | Inimigo | None = None, defensor: Aliado | Inimigo | None = None, valor: int = 1):
		if not atacante:
			atacante = self.objslc
		atacante.mira = defensor
		atacante.atacar(valor)
		atacante.update()
		self.objslc = None
