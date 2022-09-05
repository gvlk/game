import pygame
from pygame import freetype
from sys import exit
from random import randint
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
		self.image = pygame.image.load('graphics/detalhes/mosue.png')
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()


def gerartimes(tabuleiro, bloco_qnt, n: int = 4):
	for i in range(0, 2 * n):
		if i % 2 == 0:
			membro = tabuleiro.add('ali')
		else:
			membro = tabuleiro.add('ini')
		while True:
			if tabuleiro.moverobj(membro, (randint(1, bloco_qnt), randint(1, bloco_qnt))):
				break


def getmouseoffset(x, y, iw, ih, z, w, h, ts) -> Vector2:
	return pygame.math.Vector2(
		((iw - w + ts * (z - 1)) / 2) - x,
		((ih - h + ts * (z - 1)) / 2) - y
	)


def main():

	# bg = Background(width, height)

	from tabuleiro import Tabuleiro, bloco_tam
	tabuleiro = Tabuleiro()
	from hud import Hud
	hud = Hud()
	from personagem import Aliado, Inimigo
	camera = tabuleiro.camera_group
	mouse = Mouse()

	personagem1 = tabuleiro.add('ali')
	personagem2 = tabuleiro.add('ini')
	personagem3 = tabuleiro.add('ali')
	personagem4 = tabuleiro.add('ini')
	tabuleiro.moverobj(personagem1, (1, 1))
	tabuleiro.moverobj(personagem2, (1, 2))
	tabuleiro.moverobj(personagem3, (2, 1))
	tabuleiro.moverobj(personagem4, (5, 5))

	# camera.centralizar_alvo(personagem1, tabuleiro)

	# tabuleiro.findpath((1, 1), (5, 5))

	def execjogo():
		global screen
		# Constantes para descobrir a posição do mouse relativa ao tabuleiro
		mouse_pos = pygame.math.Vector2()
		offset = pygame.math.Vector2()
		renderalltiles = False  # Primeiramente renderizar todos tiles
		perso: Aliado | Inimigo
		alvo: Aliado | Inimigo | None
		alvo = None
		membroiter = {
			'i': -1,
			'ali': list(tabuleiro.sptaliados),
			'ini': list(tabuleiro.sptinimigos)
		}

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

				elif event.type == pygame.MOUSEWHEEL:
					amp = event.y * 0.01
					if 0.5 <= camera.zoom + amp <= 1.5:
						camera.zoom += amp

				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:

						if tabuleiro.mode_atual != 'def':
							menuitem = hud.mouseslc(mouse_pos)
							if menuitem:  # Primeiro checar se o menu foi clicado
								tabuleiro.resettile()

								if menuitem.nome == 'mov':
									if tabuleiro.mode_atual != 'mov':
										if tabuleiro.objslc.mira:
											tabuleiro.resetobj(tabuleiro.objslc.mira)
										tabuleiro.resetobj(img='slc')
										tabuleiro.mode_atual = 'mov'

								elif menuitem.nome == 'atk':
									if tabuleiro.mode_atual != 'atk':
										tabuleiro.mode_atual = 'atk'

						if tabuleiro.mode_atual == 'def' or tabuleiro.mode_atual == 'slc':
							obj = tabuleiro.hoverobj(click=True)
							if obj:
								tabuleiro.mode_atual = 'slc'
							else:
								tabuleiro.resetobj(limparslc=True)  # Imagem do membro selecionado volta para default
								tabuleiro.mode_atual = 'def'

						elif tabuleiro.mode_atual == 'atk':
							if alvo:
								tabuleiro.ataque(defensor=alvo, valor=1)
								tabuleiro.mode_atual = 'def'

				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:

						if tabuleiro.mode_atual == 'mov':
							if not hud.crect.collidepoint(mouse_pos):
								if tabuleiro.moverobj(tabuleiro.objslc):
									tabuleiro.mode_atual = 'def'

				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_BACKSPACE:
						pygame.quit()
						exit()

					if tabuleiro.mode_atual != 'def':
						tabuleiro.resettile()

						if event.key == pygame.K_ESCAPE:
							tabuleiro.resetobj(limparslc=True)
							tabuleiro.mode_atual = 'def'

						elif event.key == pygame.K_q:
							if tabuleiro.mode_atual != 'mov':
								if tabuleiro.objslc.mira:
									tabuleiro.resetobj(tabuleiro.objslc.mira)
								tabuleiro.resetobj(img='slc')
								tabuleiro.mode_atual = 'mov'

						elif event.key == pygame.K_w:
							if tabuleiro.mode_atual != 'atk':
								tabuleiro.objslc.imgatk()
								tabuleiro.mode_atual = 'atk'

						elif event.key == pygame.K_d:
							if tabuleiro.objslc:
								if isinstance(tabuleiro.objslc, Aliado):
									time = 'ali'
								else:
									time = 'ini'
								membroiter['i'] = membroiter[time].index(tabuleiro.objslc)
								membroiter['i'] += 1
								if membroiter['i'] > len(membroiter[time]) - 1:
									membroiter['i'] = 0
								tabuleiro.objslc = membroiter[time][membroiter['i']]

						elif event.key == pygame.K_a:
							if tabuleiro.objslc:
								if isinstance(tabuleiro.objslc, Aliado):
									time = 'ali'
								else:
									time = 'ini'
								membroiter['i'] = membroiter[time].index(tabuleiro.objslc)
								membroiter['i'] -= 1
								if membroiter['i'] < 0:
									membroiter['i'] = len(membroiter[time]) - 1
								tabuleiro.objslc = membroiter[time][membroiter['i']]

			# Hover
			if tabuleiro.mode_atual == 'def' or tabuleiro.mode_atual == 'slc':
				tabuleiro.hoverobj()
			elif tabuleiro.mode_atual == 'mov':
				tabuleiro.hovertile()
			elif tabuleiro.mode_atual == 'atk':
				if isinstance(tabuleiro.objslc, Aliado):
					alvo = tabuleiro.hoverobj('ini')
				elif isinstance(tabuleiro.objslc, Inimigo):
					alvo = tabuleiro.hoverobj('ali')

			# Render
			if renderalltiles:
				renderalltiles = False
				tabuleiro.sptchao.draw(tabuleiro.surf)

			screen.fill('Grey')
			camera.drawsprites(tabuleiro, mouse_pos)
			offset = getmouseoffset(
				tabuleiro.rect.x, tabuleiro.rect.y,
				camera.internal_surf_size[0], camera.internal_surf_size[1], camera.zoom,
				screen.get_width(), screen.get_height(), tabuleiro.rect.w
			)
			# screen.blit(camera.scaled_surf, camera.scaled_rect)  # Zoom Desligado
			screen.blit(camera.internal_surf, camera.internal_rect)

			if tabuleiro.mode_atual != 'def':  # 'slc', 'mov', 'atk'
				screen.blit(hud.hsurf, hud.hrect)
				hud.hsurf.blit(hud.csurf, hud.crect)
				hud.sptmenu.draw(screen)
				hud.mouseslc(mouse_pos)
				hud_botleft_surf, hud_botleft_rect = hud.bottomleftcontainer(tabuleiro.objslc)
				pygame.draw.rect(screen, hud.botleftcont_fundo_cor, hud.botleftcont_fundo)
				screen.blit(hud_botleft_surf, hud_botleft_rect)

			# Health Bars
			# for perso in tabuleiro.sptall:
			# 	if perso.hb_show:
			# 		pygame.draw.rect(tabuleiro.surf, (255, 0, 0), perso.hrect)
			# 		pygame.draw.rect(tabuleiro.surf, (0, 0, 0), perso.hbbrect, 2)

			# Mouse
			mouse.rect.center = mouse_pos
			screen.blit(mouse.image, mouse.rect)

			debug(f'screen.get_width(), screen.get_height() = {screen.get_width(), screen.get_height()}', y=170)
			debug(f'mouse_pos = {mouse_pos}', y=190)
			debug(f'offset = {offset}', y=210)
			debug(f'tabuleiro.mousepos = {tabuleiro.mousepos}', y=230)
			debug(f'tile do mouse = {tabuleiro.mousepos[0] // bloco_tam, tabuleiro.mousepos[1] // bloco_tam}', y=250)
			debug(f'centro = {width // 2, height // 2}', y=270)
			debug(f'tabuleiro x,y / centerx, centery {tabuleiro.rect.x, tabuleiro.rect.y, tabuleiro.rect.centerx, tabuleiro.rect.centery}', y=310)
			debug(f'camera.zoom = {camera.zoom}', y=330)
			debug(f'internal centro = {camera.internal_rect.centerx, camera.internal_rect.centery}', y=370)
			debug(f'tabuleiro.sptchaoonscreen = {tabuleiro.sptchaoonscreen}', y=390)
			debug(f'tabuleiro.sptchao = {tabuleiro.sptchao}', y=4100)

			pygame.display.update()
			clock.tick(60)

	execjogo()


if __name__ == "__main__":
	main()
