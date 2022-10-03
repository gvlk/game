import pygame
from random import randint

bloco_tam = 128
render_dist = 5

from entities.personagem import Soldado
from modules.bloco import Bloco
from modules.camera import CameraGroup


class Tabuleiro:
	def __init__(self, screen_resolution):
		self.tile_amount = 5

		self.groupchao_all = None
		self.groupchao = pygame.sprite.Group()
		self.grouptimeA = pygame.sprite.Group()
		self.grouptimeB = pygame.sprite.Group()
		self.grouptimeAB = pygame.sprite.Group()
		self.mode_atual = 'def'
		self.mousepos = (-1, -1)
		self.objslc: Soldado | None = None
		self.grade = tuple()
		self.caminhoativo = tuple()
		self.width = self.tile_amount * bloco_tam + (2 * bloco_tam)
		self.height = self.width
		self.surf = pygame.Surface((self.width, self.height))
		self.camera_group = CameraGroup(self.surf, screen_resolution)
		self.rect = self.camera_group.tabuleiro_pos()
		self.gerargrade()

	def gerargrade(self) -> None:
		from modules.bloco import Bloco
		grade = list()
		sptlist = list()
		for cx in range(0, self.tile_amount + 2):
			x = cx * bloco_tam
			coluna = list()
			for ly in range(0, self.tile_amount + 2):
				y = ly * bloco_tam
				bloco = Bloco(x, y)
				if ly == 0 or ly == self.tile_amount + 1 or cx == 0 or cx == self.tile_amount + 1:
					bloco.imgind()
					bloco.ind = True
				sptlist.append(bloco)
				coluna.append(bloco)
			grade.append(tuple(coluna))
		self.groupchao_all = pygame.sprite.Group(sptlist)
		self.grade = tuple(grade)

	def add(self, nome: str, time: str, pos: tuple) -> Soldado:
		"""
		Adição de um soldado no tabuleiro
		"""
		bloco: Bloco = self.grade[pos[0]][pos[1]]
		if not bloco.conteudo:
			if not nome:
				nome = f'Soldado{randint(100, 999)}'
			if time == 'A':
				novo = Soldado(nome, 'A')
				self.grouptimeA.add(novo)
			else:
				novo = Soldado(nome, 'B')
				self.grouptimeB.add(novo)
			novo.pos = pos
			novo.bloco = bloco
			novo.update()
			bloco.conteudo = novo
			self.camera_group.add(novo)
			self.grouptimeAB.add(novo)
			self.renderchao(novo)
			self.gerarmov(novo, pos)
			return novo

	def hoverobj(self, grupo: str = None, click: bool = False) -> bool | Soldado:
		"""
		Retorna o objeto apontado pelo mouse
		"""
		obj: Soldado
		hover: bool = False
		if not grupo:
			grupo = self.grouptimeAB
		elif grupo == 'A':
			grupo = self.grouptimeA
		elif grupo == 'B':
			grupo = self.grouptimeB
		for obj in grupo:
			if obj is not self.objslc:
				if not obj.bloco.rect.collidepoint(self.mousepos):
					obj.imgdef()
					obj.bloco.imgdef()
				else:
					obj.imgslc()
					obj.bloco.imgmse()
					hover = True
					# Em 'atk', quando clica para atacar, o self.objslc não pode mudar
					if self.mode_atual == 'def' or self.mode_atual == 'slc':
						if click:
							self.objslc = obj
					elif self.mode_atual == 'atk':
						if obj is not self.objslc.mira:
							self.objslc.mira = obj
						else:
							return obj
			else:
				if self.mode_atual != 'atk':
					obj.imgslc()
				else:
					obj.imgatk()
				obj.bloco.imgmse()

		if not click:
			return hover

	def hovertile(self) -> bool:
		"""
		Muda as tiles sob o mouse
		"""
		tile: Bloco
		hover: bool = False
		for tile in self.objslc.caminhos:
			if tile.rect.collidepoint(self.mousepos):
				self.caminhoativo = self.objslc.caminhos[tile]
				self.caminhoativo[-1].imgmovslc()
				for tilecaminho in self.caminhoativo[:-1]:
					tilecaminho.imgmov()
				hover = True
			if tile not in self.caminhoativo:
				tile.imgdef()

		if not hover:
			self.caminhoativo = tuple()
		return hover

	def moverobj(self, obj: Soldado) -> bool:
		prs: Soldado
		novobloco: Bloco
		atualbloco: Bloco
		if obj in self.grouptimeA:
			grupo_ad = self.grouptimeB
		else:
			grupo_ad = self.grouptimeA

		novobloco = self.getmousetile()

		if novobloco in obj.caminhos:
			pos_a = obj.pos  # Posição atual será usada para limpar o render depois
			atualbloco = self.grade[pos_a[0]][pos_a[1]]
			atualbloco.imgdef()
			atualbloco.conteudo = None
			novobloco.conteudo = obj
			obj.movimentar(novobloco)
			obj.pos = (novobloco.rect.x // bloco_tam, novobloco.rect.y // bloco_tam)
			obj.bloco = novobloco
			obj.hitchances.clear()  # Resetar as chances de hit
			for prs in grupo_ad:  # Remover o membro das chances de hit dos inimigos
				if obj in prs.hitchances:
					del prs.hitchances[obj]
			self.resettiles(obj.caminhos)  # Mudar todos tiles da área de movimento para 'def'
			self.renderchao(obj, pos_a)
			self.objslc = None
			self.gerarmov(obj, pos_a)
			return True  # Movimento realizado
		else:
			return False  # Tile fora do range do personagem

	# Erro: o tile inicial não é adicionado aos caminhos indisponíveis então fica invisível para os outros personagens
	# até que esse outro personagem se movimente e o tile entre em seu range
	def gerarmov(self, obj: Soldado, pos_a: tuple) -> None:
		"""
		Gera o range de tiles para o qual o membro pode se movimentar.
		"""
		tile: Bloco
		obj: Soldado
		obj2: Soldado
		obj.caminhos.clear()
		obj_posx, obj_posy = obj.pos

		# Criar area de possíveis movimentos e testa-los
		for x in range(obj_posx - obj.atr['spd'], obj_posx + obj.atr['spd'] + 1):
			if x < 1:
				continue
			if x > self.tile_amount:
				break
			for y in range(obj_posy - obj.atr['spd'], obj_posy + obj.atr['spd'] + 1):
				if y < 1:
					continue
				if y > self.tile_amount:
					break
				dis = abs(x - obj_posx) + abs(y - obj_posy)
				if 0 < dis <= obj.atr['spd']:
					tile = self.grade[x][y]
					if not tile.conteudo and not tile.ind:
						caminho = self.findpath(obj.pos, (x, y))
						if caminho is not None and len(caminho) <= obj.atr['spd']:
							obj.caminhos[tile] = caminho

		# Lidar com como o movimento realizado afeta os outros soldados e seus movimentos possíveis
		for obj2 in self.grouptimeAB:
			if obj2 is not obj:

				# Remover o novo bloco do range dos outros personagens
				delitems = list()
				if obj.bloco in obj2.caminhos:
					del obj2.caminhos[obj.bloco]
					for destino, caminho in obj2.caminhos.items():  # Remover o novo bloco dos caminhos já descobertos
						if obj.bloco in caminho:
							tiledestino = (destino.rect.x // bloco_tam, destino.rect.y // bloco_tam)
							novocaminho = self.findpath(obj2.pos, tiledestino)
							if novocaminho is not None and len(novocaminho) <= obj2.atr['spd']:  # Tentar achar outro caminho
								obj2.caminhos[destino] = novocaminho
							else:
								obj2.caminhosind[destino] = caminho  # Joga esse caminho para os caminhos indisponíveis
								delitems.append(destino)  # Impossível deletar um item de dicionário no meio da iteração
					for i in delitems:
						del obj2.caminhos[i]
					delitems.clear()

				# Adicionar o bloco do qual saiu ao range dos outros personagens se possível
				if self.inobjmov(obj2, pos_a):
					caminho = self.findpath(obj2.pos, pos_a)
					if caminho is not None and len(caminho) <= obj2.atr['spd']:
						tile = self.grade[pos_a[0]][pos_a[1]]
						obj2.caminhos[tile] = caminho

				# Testar se algum caminho de outro personagem ficou disponível
				for destino, caminho in obj2.caminhosind.items():
					if obj.bloco is not destino and obj.bloco not in caminho:
						tiledestino = (destino.rect.x // bloco_tam, destino.rect.y // bloco_tam)
						if self.inobjmov(obj2, tiledestino):
							caminho = self.findpath(obj2.pos, tiledestino)
							if caminho is not None and len(caminho) <= obj2.atr['spd']:
								obj2.caminhos[destino] = caminho
								delitems.append(destino)
						else:
							delitems.append(destino)
				for i in delitems:
					del obj2.caminhosind[i]
				delitems.clear()

	def findpath(self, origem: tuple, destino: tuple) -> tuple | None:
		tile: Bloco
		vizinho: Bloco
		origembloco: Bloco
		destinobloco: Bloco
		caminho = list()
		opentiles = list()  # Implementar estrutura de árvore ordenada para melhorar o desempenho
		closedtiles = set()
		ngbrs = list()
		limpar = list()  # Lista de tiles que devem ser limpos no final. tile.parent = None
		caminhoencontrado = False
		origembloco = self.grade[origem[0]][origem[1]]
		destinobloco = self.grade[destino[0]][destino[1]]
		opentiles.append((origembloco, origem))

		while len(opentiles) > 0:
			opentiles = sorted(opentiles, key=lambda x: x[0].fcost)
			bloco = opentiles[0]
			tile = bloco[0]
			cordx, cordy = bloco[1]
			opentiles.remove(bloco)
			closedtiles.add(bloco)
			if tile is destinobloco:  # Achou um caminho
				caminhoencontrado = True
				break

			ngbrs.append((self.grade[cordx + 1][cordy], (cordx + 1, cordy)))
			ngbrs.append((self.grade[cordx - 1][cordy], (cordx - 1, cordy)))
			ngbrs.append((self.grade[cordx][cordy + 1], (cordx, cordy + 1)))
			ngbrs.append((self.grade[cordx][cordy - 1], (cordx, cordy - 1)))

			for bloco in ngbrs:
				vizinho = bloco[0]
				if vizinho.conteudo or (bloco in closedtiles) or (bloco in opentiles) or vizinho.ind:
					continue

				vizinho.gcost = self.getdistance(origembloco, vizinho)
				vizinho.hcost = self.getdistance(destinobloco, vizinho)
				vizinho.fcost = vizinho.gcost + vizinho.hcost
				vizinho.parent = tile
				limpar.append(vizinho)
				opentiles.append(bloco)
			else:
				ngbrs.clear()

		if caminhoencontrado:
			aux: Bloco
			aux = destinobloco
			while aux.parent:
				caminho.append(aux)
				aux = aux.parent
			caminho.reverse()
			caminho = tuple(caminho)
		else:
			caminho = None

		for tile in limpar:  # Limpar as tiles usadas para descobrir o caminho
			tile.parent = None

		return caminho

	@staticmethod
	def inobjmov(obj: Soldado, pos: tuple) -> bool:
		if pos:
			posx, posy = pos
			dis = abs(posx - obj.pos[0]) + abs(posy - obj.pos[1])
			if 0 < dis <= obj.atr['spd']:
				return True
			else:
				return False
		else:
			return False

	@staticmethod
	def getdistance(tile_a: Bloco, tile_b: Bloco) -> int:
		dstX = abs(tile_a.rect.centerx // bloco_tam - tile_b.rect.centerx // bloco_tam)
		dstY = abs(tile_a.rect.centery // bloco_tam - tile_b.rect.centery // bloco_tam)
		if dstX > dstY:
			return (14 * dstY) + (10 * (dstX - dstY))
		else:
			return (14 * dstX) + (10 * (dstY - dstX))

	def getmousetile(self) -> Bloco:
		posx, posy = int(self.mousepos[0] // bloco_tam), int(self.mousepos[1] // bloco_tam)
		# Clamp
		if posx <= 1:
			posx = 1
		elif posx >= self.tile_amount:
			posx = self.tile_amount
		if posy <= 1:
			posy = 1
		elif posy >= self.tile_amount:
			posy = self.tile_amount
		return self.grade[posx][posy]

	def renderchao(self, obj: Soldado, pos_a: tuple = False) -> None:
		if pos_a:  # Limpar os tiles renderizados na posição antiga
			max_x = pos_a[0] + render_dist + 1
			min_x = pos_a[0] - render_dist
			max_y = pos_a[1] + render_dist + 1
			min_y = pos_a[1] - render_dist
			if max_x > self.tile_amount + 2:
				max_x = self.tile_amount + 2
			if min_x < 0:
				min_x = 0
			if max_y > self.tile_amount + 2:
				max_y = self.tile_amount + 2
			if min_y < 0:
				min_y = 0
			for y in range(min_y, max_y):
				for x in range(min_x, max_x):
					bloco = self.grade[x][y]
					if len(pygame.sprite.Sprite.groups(bloco)) == 2:  # groupchao, obj.area
						self.groupchao.remove(bloco)
					obj.area.remove(bloco)

		max_x = obj.pos[0] + render_dist + 1
		min_x = obj.pos[0] - render_dist
		max_y = obj.pos[1] + render_dist + 1
		min_y = obj.pos[1] - render_dist
		if max_x > self.tile_amount + 2:
			max_x = self.tile_amount + 2
		if min_x < 0:
			min_x = 0
		if max_y > self.tile_amount + 2:
			max_y = self.tile_amount + 2
		if min_y < 0:
			min_y = 0
		for y in range(min_y, max_y):
			for x in range(min_x, max_x):
				bloco = self.grade[x][y]
				obj.area.add(bloco)
				self.groupchao.add(bloco)
		self.camera_group.ground = self.groupchao

	def resettiles(self, grupo: list | tuple | set = False) -> None:
		tile: Bloco
		if not grupo:
			tile = self.getmousetile()
			tile.imgdef()
		else:
			for tile in grupo:
				tile.imgdef()

	def tileocupada(self) -> bool:
		tile: Bloco
		tile = self.getmousetile()
		if tile.conteudo is None:
			return False
		else:
			return True

	def resetobj(self, obj: Soldado, limparslc: bool = False, img: str = 'def') -> None:
		obj.bloco.imgdef()
		obj.update(img=img)
		if limparslc:
			self.objslc = None

	def ataque(self, atacante: Soldado, defensor: Soldado):
		atacante.mira = defensor
		atacante.atacar()
		self.objslc = None

	def gerarchances(self):
		soldado: Soldado
		atacante = self.objslc
		if atacante in self.grouptimeA:
			grupo_ad = self.grouptimeB
		else:
			grupo_ad = self.grouptimeA
		for soldado in grupo_ad:
			if soldado in atacante.hitchances:
				continue
			else:
				dst = self.getdistance(atacante.bloco, soldado.bloco)
				atacante.gethitchances(soldado, dst)  # Faltando um parâmetro que diz se há barreira entre os dois
