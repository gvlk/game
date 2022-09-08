import pygame
from pygame import freetype
from sys import exit
from random import randint, choice
from pygame.math import Vector2

from debug import debug

if __name__ == "__main__":
	pygame.init()
	pygame.freetype.init()

width = 1280
height = int((width * (9 / 16)))
s_res = (width, height)
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.event.set_grab(True)
pygame.display.set_caption('Jogo')
font = pygame.freetype.Font('fontes/AlumniSansPinstripe-Regular.ttf', 24)
pygame.mouse.set_visible(False)


class Background:
	def __init__(self, w, h):
		self.oimage = pygame.image.load('graphics/background/background.png').convert()
		self.image = pygame.transform.smoothscale(self.oimage, (w, h))
		self.surf = self.image
		self.rect = self.surf.get_rect(center=(w/2, h/2))


class Mouse(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		image = pygame.image.load('graphics/detalhes/mosue.png')
		self.image = pygame.transform.scale(image, pygame.math.Vector2(image.get_size()) * 4).convert_alpha()
		self.rect = self.image.get_rect()


def gerartimes(tabuleiro, bloco_qnt, n: int = 1):
	for i in range(0, 2 * n):
		if i % 2 == 0:
			while True:
				if tabuleiro.add(False, 'A', (randint(1, bloco_qnt), randint(1, bloco_qnt))):
					break
		else:
			while True:
				if tabuleiro.add(False, 'B', (randint(1, bloco_qnt), randint(1, bloco_qnt))):
					break


def getmouseoffset(x, y, iw, ih, z, w, h, ts) -> Vector2:
	return pygame.math.Vector2(
		((iw - w + ts * (z - 1)) / 2) - x,
		((ih - h + ts * (z - 1)) / 2) - y
	)


def main():

	# bg = Background(width, height)

	from tabuleiro import Tabuleiro, bloco_qnt
	tabuleiro = Tabuleiro()
	from personagem import Soldado
	camera = tabuleiro.camera_group
	mouse = Mouse()
	mousegroup = pygame.sprite.GroupSingle(mouse)

	gerartimes(tabuleiro, bloco_qnt)

	camera.centralizar_alvo(choice(list(tabuleiro.grouptimeAB)), tabuleiro)

	soldadoA: Soldado = tabuleiro.grouptimeA.sprites()[0]
	soldadoB: Soldado = tabuleiro.grouptimeB.sprites()[0]

	def execjogo():
		global screen
		alvo: Soldado | None
		movimentando: Soldado | None
		mouse_pos = pygame.math.Vector2()
		offset = pygame.math.Vector2()
		alvo = None
		movimentar = False
		movimentando = None
		membroiter = {
			'i': -1,
			'A': list(tabuleiro.grouptimeA),
			'B': list(tabuleiro.grouptimeB)
		}
		tabuleiro.groupchao_all.draw(tabuleiro.surf)  # Primeiramente renderizar todos tiles
		tabuleiro.groupchao_all.empty()
		del tabuleiro.groupchao_all

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

				elif event.type == pygame.VIDEORESIZE:
					screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

				elif event.type == pygame.MOUSEMOTION:
					mouse_pos = pygame.mouse.get_pos()
					tabuleiro.mousepos = (mouse_pos + offset) // camera.zoom

				# elif event.type == pygame.MOUSEWHEEL:
				# 	amp = event.y * 0.01
				# 	if 0.5 <= camera.zoom + amp <= 1.5:
				# 		camera.zoom += amp

				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:

						# if tabuleiro.mode_atual != 'def':  # HUD
						# 	menuitem = hud.mouseslc(mouse_pos)
						# 	if menuitem:  # Primeiro checar se o menu foi clicado
						# 		tabuleiro.resettiles()
						#
						# 		if menuitem.nome == 'mov':
						# 			if tabuleiro.mode_atual != 'mov':
						# 				if tabuleiro.objslc.mira:
						# 					tabuleiro.resetobj(tabuleiro.objslc.mira)
						# 				tabuleiro.resetobj(tabuleiro.objslc, img='slc')
						# 				tabuleiro.mode_atual = 'mov'
						#
						# 		elif menuitem.nome == 'atk':
						# 			if tabuleiro.mode_atual != 'atk':
						# 				tabuleiro.mode_atual = 'atk'

						if tabuleiro.mode_atual == 'def' or tabuleiro.mode_atual == 'slc':
							if tabuleiro.tileocupada():
								tabuleiro.hoverobj(click=True)
								tabuleiro.mode_atual = 'slc'
							else:
								tabuleiro.resetobj(tabuleiro.objslc, limparslc=True)  # Imagem do membro selecionado volta para default
								tabuleiro.mode_atual = 'def'

						elif tabuleiro.mode_atual == 'atk':
							if alvo:
								tabuleiro.ataque(tabuleiro.objslc, alvo)
								tabuleiro.mode_atual = 'def'

				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:

						if tabuleiro.mode_atual == 'mov':
							movimentando = tabuleiro.objslc
							if tabuleiro.moverobj(tabuleiro.objslc):
								movimentar = True
								tabuleiro.mode_atual = 'def'
							else:
								movimentando = None

				elif event.type == pygame.KEYDOWN:
					if tabuleiro.mode_atual != 'def':
						if event.key == pygame.K_ESCAPE:
							tabuleiro.resettiles({tabuleiro.objslc.bloco})  # Resetar o bloco atual
							tabuleiro.resettiles(tabuleiro.objslc.caminhos)  # Resetar os blocos da área de movimento
							tabuleiro.resetobj(tabuleiro.objslc, limparslc=True)
							tabuleiro.mode_atual = 'def'

						elif event.key == pygame.K_q:
							if tabuleiro.mode_atual != 'mov':
								tabuleiro.resettiles(tabuleiro.objslc.caminhos)  # Resetar os blocos da área de movimento
								if tabuleiro.objslc.mira:
									tabuleiro.resetobj(tabuleiro.objslc.mira)
								tabuleiro.resetobj(tabuleiro.objslc, img='slc')
								tabuleiro.mode_atual = 'mov'

						elif event.key == pygame.K_w:
							if tabuleiro.mode_atual != 'atk':
								tabuleiro.gerarchances()
								tabuleiro.resettiles(tabuleiro.objslc.caminhos)  # Resetar os blocos da área de movimento
								tabuleiro.objslc.imgatk()
								tabuleiro.mode_atual = 'atk'

						elif event.key == pygame.K_d or event.key == pygame.K_a:
							tabuleiro.resettiles([tabuleiro.objslc.bloco])  # Resetar o bloco atual
							tabuleiro.resettiles(tabuleiro.objslc.caminhos)  # Resetar os blocos da área de movimento
							if tabuleiro.objslc.mira:
								tabuleiro.resetobj(tabuleiro.objslc.mira)
							if tabuleiro.objslc:
								if tabuleiro.objslc in tabuleiro.grouptimeA or tabuleiro.objslc is None:
									time = 'A'
								else:
									time = 'B'
								membroiter['i'] = membroiter[time].index(tabuleiro.objslc)
								if event.key == pygame.K_d:
									membroiter['i'] += 1
									if membroiter['i'] > len(membroiter[time]) - 1:
										membroiter['i'] = 0
									tabuleiro.objslc = membroiter[time][membroiter['i']]
								else:  # event.key == pygame.K_a:
									membroiter['i'] -= 1
									if membroiter['i'] < 0:
										membroiter['i'] = len(membroiter[time]) - 1
									tabuleiro.objslc = membroiter[time][membroiter['i']]
								tabuleiro.hoverobj()  # Mudar sprite do objeto selecionado para 'slc'
					else:
						if event.key == pygame.K_ESCAPE:
							pygame.quit()
							exit()

			# Animação de movimento do soldado
			if movimentar:
				if movimentando.movimentar():
					movimentar = False

			# Hover
			if tabuleiro.mode_atual == 'def' or tabuleiro.mode_atual == 'slc':
				if tabuleiro.hoverobj():
					mousegroup.remove(mouse)  # Mouse some quando está sobre um personagem válido
				else:
					mousegroup.add(mouse)
			elif tabuleiro.mode_atual == 'mov':
				if tabuleiro.hovertile():
					mousegroup.remove(mouse)
				else:
					mousegroup.add(mouse)
			elif tabuleiro.mode_atual == 'atk':
				if tabuleiro.objslc in tabuleiro.grouptimeA:
					alvo = tabuleiro.hoverobj('B')
				else:
					alvo = tabuleiro.hoverobj('A')
				if alvo:
					mousegroup.remove(mouse)
				else:
					mousegroup.add(mouse)

			# Render
			camera.drawsprites(tabuleiro, mouse_pos)
			offset = getmouseoffset(
				tabuleiro.rect.x, tabuleiro.rect.y,
				camera.internal_surf_size[0], camera.internal_surf_size[1], camera.zoom,
				screen.get_width(), screen.get_height(), tabuleiro.rect.w
			)
			# screen.blit(camera.scaled_surf, camera.scaled_rect)  # Zoom Desligado
			screen.blit(camera.internal_surf, camera.internal_rect)

			# Mouse
			mouse.rect.center = mouse_pos
			mousegroup.draw(screen)

			# Debug
			debug(f'FPS {int(clock.get_fps())}')
			debug(f'mouse_pos = {mouse_pos}', y=150)
			debug(f'tabuleiro mousepos = {tabuleiro.mousepos}', y=170)
			debug(f'tile atual = {tabuleiro.mousepos[0] // 128, tabuleiro.mousepos[1] // 128}', y=190)
			debug(f'tiles sendo atualizados = {tabuleiro.groupchao}', y=210)
			debug(soldadoA, y=230)
			debug(soldadoB, y=250)
			debug(f'selecionado = {tabuleiro.objslc}', y=270)
			try:
				debug(f'tile do soldado = {tabuleiro.objslc.pos}', y=290)
			except AttributeError:
				debug(None, y=290)
			debug(f'disância entre soldados = {tabuleiro.getdistance(soldadoA.bloco, soldadoB.bloco)}', y=310)
			try:
				debug(f'chance de hit (A -> B) = {soldadoA.hitchances[soldadoB]}%', y=330)
			except KeyError:
				debug(None, y=330)
			try:
				debug(f'chance de hit (B -> A) = {soldadoB.hitchances[soldadoA]}%', y=350)
			except KeyError:
				debug(None, y=350)

			pygame.display.update()
			clock.tick(60)

	execjogo()


if __name__ == "__main__":
	main()
