import pygame
from random import randint, choice

from main import s_res

s_w, s_h = s_res
width = s_w
height = width
bloco_qnt = 10  # Mais 2 tiles externos de borda
bloco_tam = 64
render_dist = 20

from personagem import Aliado, Inimigo
from bloco import Bloco


class Tabuleiro:
	def gerargrade(self):
		from bloco import Bloco
		grade = list()
		sptlist = list()
		for c in range(0, bloco_qnt+2):
			x = c * bloco_tam
			coluna = list()
			for l in range(0, bloco_qnt+2):
				y = l * bloco_tam
				bloco = Bloco(x, y)
				if l == 0 or l == bloco_qnt + 1 or c == 0 or c == bloco_qnt + 1:
					bloco.imgind()
					bloco.ind = True
				sptlist.append(bloco)
				coluna.append(bloco)
			grade.append(tuple(coluna))
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
		self.objslc = None
		self.grade = None
		self.gerargrade()
		self.width = bloco_qnt * bloco_tam + (2 * bloco_tam)
		self.height = self.width
		self.surf = pygame.Surface((self.width, self.height))
		self.surf.fill('Red')
		self.rect = self.surf.get_rect(center=(width//2, height//2))

	def posicaoinicial(self):
		center_posx, center_posy = choice(self.sptaliados.sprites()).rect.center
		center_pos = ((s_w / 2) + (self.rect.w / 2) - center_posx, (s_h / 2) + (self.rect.h / 2) - center_posy)
		self.rect = self.surf.get_rect(center=center_pos)

	def add(self, tipo: str, nome: str = None):
		if not nome:
			if tipo == 'ali':
				nome = f'aliado{randint(100, 999)}'
			else:
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
		if not click:
			return None
		else:
			return self.objslc

	def hovertile(self):
		"""
		Muda as tiles sob o mouse para 'imgslc'
		"""
		bloco: Bloco
		for bloco in self.sptchaoonscreen:
			if not bloco.ind:
				if not bloco.rect.collidepoint(self.mousepos):
					bloco.imgdef()
				else:
					if not bloco.conteudo:
						bloco.imgslc()

	def moverobj(self, obj, pos_d: tuple = None, mode: str = 'cor'):
		if mode == 'cor':
			if pos_d[0] < 1:
				pos_d = (1, pos_d[1])
			elif pos_d[0] > bloco_qnt:
				pos_d = (bloco_qnt, pos_d[1])
			if pos_d[1] < 1:
				pos_d = (pos_d[0], 1)
			elif pos_d[1] > bloco_qnt:
				pos_d = (pos_d[0], bloco_qnt)
		elif mode == 'pos' or not pos_d:
			pos_d = (self.mousepos[0] // bloco_tam, self.mousepos[1] // bloco_tam)
			return self.moverobj(obj, pos_d)

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
			self.objslc = None
			self.removermira(obj)
			return True
		else:
			print('bloco ocupado')
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

	def resettile(self):
		"""
		Tile sob o mouse retorna para 'imgdef'
		"""
		tile: Bloco
		tile = self.grade[self.mousepos[0] // bloco_tam][self.mousepos[1] // bloco_tam]
		if not tile.ind:
			tile.imgdef()

	def resetobj(self, obj: Aliado | Inimigo = None, limparslc: bool = False, img: str = 'def', rot: bool = False):
		if not obj:
			obj = self.objslc
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




