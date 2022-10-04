import pygame

bloco_tam = 128
render_dist = 5

from entities.soldier import Soldier
from modules.tile import Tile
from modules.camera import CameraGroup


class Board:
	def __init__(self, screen_resolution):
		self.tile_amount = 5
		self.group_tiles_all = None
		self.group_tiles = pygame.sprite.Group()
		self.group_team_A = pygame.sprite.Group()
		self.group_team_B = pygame.sprite.Group()
		self.group_soldiers = pygame.sprite.Group()
		self.current_mode = 'def'
		self.mouse_pos = (-1, -1)
		self.selected_soldier: Soldier | None = None
		self.tile_grid = tuple()
		self.active_path = tuple()
		self.width = self.tile_amount * bloco_tam + (2 * bloco_tam)
		self.height = self.width
		self.surf = pygame.Surface((self.width, self.height))
		self.group_camera = CameraGroup(self.surf, screen_resolution)
		self.rect = self.group_camera.getBoardRect()
		self.generateTileGrid()

	def generateTileGrid(self) -> None:
		from modules.tile import Tile
		grade = list()
		sptlist = list()
		for cx in range(0, self.tile_amount + 2):
			x = cx * bloco_tam
			coluna = list()
			for ly in range(0, self.tile_amount + 2):
				y = ly * bloco_tam
				bloco = Tile(x, y)
				if ly == 0 or ly == self.tile_amount + 1 or cx == 0 or cx == self.tile_amount + 1:
					bloco.imageUpdate('ind')
					bloco.unavailable = True
				sptlist.append(bloco)
				coluna.append(bloco)
			grade.append(tuple(coluna))
		self.group_tiles_all = pygame.sprite.Group(sptlist)
		self.tile_grid = tuple(grade)

	def addSoldier(self, name: str, team: str, pos: tuple) -> Soldier:
		"""
		Adição de um soldado no board
		"""
		bloco: Tile = self.tile_grid[pos[0]][pos[1]]
		if not bloco.content:
			if team == 'A':
				novo = Soldier(name, 'A')
				self.group_team_A.add(novo)
			else:
				novo = Soldier(name, 'B')
				self.group_team_B.add(novo)
			novo.pos = pos
			novo.tile = bloco
			novo.update()
			bloco.content = novo
			self.group_camera.add(novo)
			self.group_soldiers.add(novo)
			self.getVisibleTiles(novo)
			self.generateSoldierMovement(novo, pos)
			return novo

	def hoverSoldier(self, grupo: str = None, click: bool = False) -> bool | Soldier:
		"""
		Retorna o objeto apontado pelo mouse
		"""
		obj: Soldier
		hover: bool = False
		if not grupo:
			grupo = self.group_soldiers
		elif grupo == 'A':
			grupo = self.group_team_A
		elif grupo == 'B':
			grupo = self.group_team_B
		for obj in grupo:
			if obj is not self.selected_soldier:
				if not obj.tile.rect.collidepoint(self.mouse_pos):
					obj.imageUpdate('def')
					obj.tile.imageUpdate('def')
				else:
					obj.imageUpdate('slc')
					obj.tile.imageUpdate('mse')
					hover = True
					# Em 'atk', quando clica para atacar, o self.selected_soldier não pode mudar
					if self.current_mode == 'def' or self.current_mode == 'slc':
						if click:
							self.selected_soldier = obj
					elif self.current_mode == 'atk':
						if obj is not self.selected_soldier.aim:
							self.selected_soldier.aim = obj
						else:
							return obj
			else:
				if self.current_mode != 'atk':
					obj.imageUpdate('slc')
				else:
					obj.imageUpdate('atk')
				obj.tile.imageUpdate('mse')

		if not click:
			return hover

	def hoverTile(self) -> bool:
		"""
		Muda as tiles sob o mouse
		"""
		tile: Tile
		hover: bool = False
		for tile in self.selected_soldier.paths:
			if tile.rect.collidepoint(self.mouse_pos):
				self.active_path = self.selected_soldier.paths[tile]
				self.active_path[-1].imageUpdate('movslc')
				for tilecaminho in self.active_path[:-1]:
					tilecaminho.imageUpdate('mov')
				hover = True
			if tile not in self.active_path:
				tile.imageUpdate('def')

		if not hover:
			self.active_path = tuple()
		return hover

	def moveSoldier(self, soldier: Soldier) -> bool:
		prs: Soldier
		novobloco: Tile
		atualbloco: Tile
		if soldier in self.group_team_A:
			grupo_ad = self.group_team_B
		else:
			grupo_ad = self.group_team_A

		novobloco = self.getMouseTile()

		if novobloco in soldier.paths:
			pos_a = soldier.pos  # Posição atual será usada para limpar o render depois
			atualbloco = self.tile_grid[pos_a[0]][pos_a[1]]
			atualbloco.imageUpdate('mov')
			atualbloco.content = None
			novobloco.content = soldier
			soldier.move(novobloco)
			soldier.pos = (novobloco.rect.x // bloco_tam, novobloco.rect.y // bloco_tam)
			soldier.tile = novobloco
			soldier.hit_chances.clear()  # Resetar as chances de hit
			for prs in grupo_ad:  # Remover o membro das chances de hit dos inimigos
				if soldier in prs.hit_chances:
					del prs.hit_chances[soldier]
			self.resetTiles(soldier.paths)  # Mudar todos tiles da área de movimento para 'def'
			self.getVisibleTiles(soldier, pos_a)
			self.selected_soldier = None
			self.generateSoldierMovement(soldier, pos_a)
			return True  # Movimento realizado
		else:
			return False  # Tile fora do range do personagem

	# Erro: o tile inicial não é adicionado aos paths indisponíveis então fica invisível para os outros personagens
	# até que esse outro personagem se movimente e o tile entre em seu range
	def generateSoldierMovement(self, obj: Soldier, pos_a: tuple) -> None:
		"""
		Gera o range de tiles para o qual o membro pode se movimentar.
		"""
		tile: Tile
		obj: Soldier
		obj2: Soldier
		obj.paths.clear()
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
					tile = self.tile_grid[x][y]
					if not tile.content and not tile.unavailable:
						caminho = self.findPath(obj.pos, (x, y))
						if caminho is not None and len(caminho) <= obj.atr['spd']:
							obj.paths[tile] = caminho

		# Lidar com como o movimento realizado afeta os outros soldados e seus movimentos possíveis
		for obj2 in self.group_soldiers:
			if obj2 is not obj:

				# Remover o novo tile do range dos outros personagens
				delitems = list()
				if obj.tile in obj2.paths:
					del obj2.paths[obj.tile]
					for destino, caminho in obj2.paths.items():  # Remover o novo tile dos paths já descobertos
						if obj.tile in caminho:
							tiledestino = (destino.rect.x // bloco_tam, destino.rect.y // bloco_tam)
							novocaminho = self.findPath(obj2.pos, tiledestino)
							if novocaminho is not None and len(novocaminho) <= obj2.atr['spd']:  # Tentar achar outro caminho
								obj2.paths[destino] = novocaminho
							else:
								obj2.blocked_paths[destino] = caminho  # Joga esse caminho para os paths indisponíveis
								delitems.append(destino)  # Impossível deletar um item de dicionário no meio da iteração
					for i in delitems:
						del obj2.paths[i]
					delitems.clear()

				# Adicionar o tile do qual saiu ao range dos outros personagens se possível
				if self.isInSoldierRange(obj2, pos_a):
					caminho = self.findPath(obj2.pos, pos_a)
					if caminho is not None and len(caminho) <= obj2.atr['spd']:
						tile = self.tile_grid[pos_a[0]][pos_a[1]]
						obj2.paths[tile] = caminho

				# Testar se algum caminho de outro personagem ficou disponível
				for destino, caminho in obj2.blocked_paths.items():
					if obj.tile is not destino and obj.tile not in caminho:
						tiledestino = (destino.rect.x // bloco_tam, destino.rect.y // bloco_tam)
						if self.isInSoldierRange(obj2, tiledestino):
							caminho = self.findPath(obj2.pos, tiledestino)
							if caminho is not None and len(caminho) <= obj2.atr['spd']:
								obj2.paths[destino] = caminho
								delitems.append(destino)
						else:
							delitems.append(destino)
				for i in delitems:
					del obj2.blocked_paths[i]
				delitems.clear()

	def findPath(self, origem: tuple, destino: tuple) -> tuple | None:
		tile: Tile
		vizinho: Tile
		origembloco: Tile
		destinobloco: Tile
		caminho = list()
		opentiles = list()  # Implementar estrutura de árvore ordenada para melhorar o desempenho
		closedtiles = set()
		ngbrs = list()
		limpar = list()  # Lista de tiles que devem ser limpos no final. tile.parent = None
		caminhoencontrado = False
		origembloco = self.tile_grid[origem[0]][origem[1]]
		destinobloco = self.tile_grid[destino[0]][destino[1]]
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

			ngbrs.append((self.tile_grid[cordx + 1][cordy], (cordx + 1, cordy)))
			ngbrs.append((self.tile_grid[cordx - 1][cordy], (cordx - 1, cordy)))
			ngbrs.append((self.tile_grid[cordx][cordy + 1], (cordx, cordy + 1)))
			ngbrs.append((self.tile_grid[cordx][cordy - 1], (cordx, cordy - 1)))

			for bloco in ngbrs:
				vizinho = bloco[0]
				if vizinho.content or (bloco in closedtiles) or (bloco in opentiles) or vizinho.unavailable:
					continue

				vizinho.gcost = self.getDistance(origembloco, vizinho)
				vizinho.hcost = self.getDistance(destinobloco, vizinho)
				vizinho.fcost = vizinho.gcost + vizinho.hcost
				vizinho.parent = tile
				limpar.append(vizinho)
				opentiles.append(bloco)
			else:
				ngbrs.clear()

		if caminhoencontrado:
			aux: Tile
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
	def isInSoldierRange(obj: Soldier, pos: tuple) -> bool:
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
	def getDistance(tile_a: Tile, tile_b: Tile) -> int:
		dstX = abs(tile_a.rect.centerx // bloco_tam - tile_b.rect.centerx // bloco_tam)
		dstY = abs(tile_a.rect.centery // bloco_tam - tile_b.rect.centery // bloco_tam)
		if dstX > dstY:
			return (14 * dstY) + (10 * (dstX - dstY))
		else:
			return (14 * dstX) + (10 * (dstY - dstX))

	def getMouseTile(self) -> Tile:
		posx, posy = int(self.mouse_pos[0] // bloco_tam), int(self.mouse_pos[1] // bloco_tam)
		# Clamp
		if posx <= 1:
			posx = 1
		elif posx >= self.tile_amount:
			posx = self.tile_amount
		if posy <= 1:
			posy = 1
		elif posy >= self.tile_amount:
			posy = self.tile_amount
		return self.tile_grid[posx][posy]

	def getVisibleTiles(self, obj: Soldier, pos_a: tuple = False) -> None:
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
					bloco = self.tile_grid[x][y]
					if len(pygame.sprite.Sprite.groups(bloco)) == 2:  # group_tiles, soldier.area
						self.group_tiles.remove(bloco)
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
				bloco = self.tile_grid[x][y]
				obj.area.add(bloco)
				self.group_tiles.add(bloco)
		self.group_camera.ground = self.group_tiles

	def resetTiles(self, grupo: list | tuple | set = None) -> None:
		tile: Tile
		if not grupo:
			tile = self.getMouseTile()
			tile.imageUpdate('def')
		else:
			for tile in grupo:
				tile.imageUpdate('def')

	def isTileOccupied(self) -> bool:
		tile: Tile
		tile = self.getMouseTile()
		if tile.content is None:
			return False
		else:
			return True

	def atack(self, atacante: Soldier, defensor: Soldier) -> None:
		atacante.aim = defensor
		atacante.atack()
		self.selected_soldier = None

	def generateHitChances(self) -> None:
		soldado: Soldier
		atacante = self.selected_soldier
		if atacante in self.group_team_A:
			grupo_ad = self.group_team_B
		else:
			grupo_ad = self.group_team_A
		for soldado in grupo_ad:
			if soldado in atacante.hit_chances:
				continue
			else:
				dst = self.getDistance(atacante.tile, soldado.tile)
				atacante.getHitChances(soldado, dst)  # Faltando um parâmetro que diz se há barreira entre os dois
