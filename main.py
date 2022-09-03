import pygame
from pygame import freetype
from sys import exit
from random import randint

from debug import debug

if __name__ == "__main__":
	pygame.init()
	pygame.freetype.init()

width = 1450
height = int((width * (9 / 16)))
s_res = (width, height)
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.event.set_grab(True)
pygame.display.set_caption('Jogo')
font = pygame.freetype.Font('fontes/AlumniSansPinstripe-Regular.ttf', 24)


class Background:
	def __init__(self, w, h):
		self.oimage = pygame.image.load('graphics/background/background.png').convert()
		self.image = pygame.transform.smoothscale(self.oimage, (w, h))
		self.surf = self.image

	def update(self, w, h):
		self.image = pygame.transform.scale(self.image, (w, h))
		self.surf = self.image


def gerartimes(tabuleiro, bloco_qnt, n: int = 4):
	for i in range(0, 2 * n):
		if i % 2 == 0:
			membro = tabuleiro.add('ali')
		else:
			membro = tabuleiro.add('ini')
		while True:
			if tabuleiro.moverobj(membro, (randint(1, bloco_qnt), randint(1, bloco_qnt))):
				break


def main():

	bg = Background(width, height)

	from tabuleiro import Tabuleiro, bloco_tam
	tabuleiro = Tabuleiro()
	from hud import Hud
	hud = Hud()
	from personagem import Aliado, Inimigo
	camera = tabuleiro.camera_group

	personagem1 = tabuleiro.add('ali')
	personagem2 = tabuleiro.add('ini')
	personagem3 = tabuleiro.add('ali')
	personagem4 = tabuleiro.add('ini')
	tabuleiro.moverobj(personagem1, (1, 1))
	tabuleiro.moverobj(personagem2, (1, 2))
	tabuleiro.moverobj(personagem3, (2, 1))
	tabuleiro.moverobj(personagem4, (5, 5))

	camera.centralizar_alvo(personagem1, tabuleiro)

	# tabuleiro.findpath((1, 1), (5, 5))

	def execjogo():
		mx = my = int()
		ax, by = (-tabuleiro.rect.x, -tabuleiro.rect.y)
		# Constantes para descobrir a posição do mouse relativa ao tabuleiro
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
					bg.update(event.w, event.h)
					ax, by = (-tabuleiro.rect.x, -tabuleiro.rect.y)

				elif event.type == pygame.MOUSEMOTION:
					mx, my = pygame.mouse.get_pos()
					tabuleiro.mousepos = (mx + ax, my + by)

				elif event.type == pygame.MOUSEWHEEL:
					camera.zoom += event.y * 0.15

				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:

						if tabuleiro.mode_atual != 'def':
							menuitem = hud.mouseslc((mx, my))
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
							if tabuleiro.tileocupada():
								tabuleiro.hoverobj(click=True)
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
							if not hud.crect.collidepoint((mx, my)):
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

			# TODO: Resolver o rastro e colisões
			# Render
			if renderalltiles:
				renderalltiles = False
				tabuleiro.sptchao.draw(tabuleiro.surf)

			camera.drawsprites(tabuleiro, (mx, my))
			camera.internal_surf.blit(tabuleiro.surf, tabuleiro.rect)
			ax, by = (-tabuleiro.rect.x, -tabuleiro.rect.y)
			screen.blit(bg.surf, (0, 0))
			screen.blit(camera.scaled_surf, camera.scaled_rect)

			if tabuleiro.mode_atual != 'def':  # 'slc', 'mov', 'atk'
				screen.blit(hud.hsurf, hud.hrect)
				hud.hsurf.blit(hud.csurf, hud.crect)
				hud.sptmenu.draw(screen)
				hud.mouseslc((mx, my))
				hud_botleft_surf, hud_botleft_rect = hud.bottomleftcontainer(tabuleiro.objslc)
				pygame.draw.rect(screen, hud.botleftcont_fundo_cor, hud.botleftcont_fundo)
				screen.blit(hud_botleft_surf, hud_botleft_rect)

			# Health Bars
			# for perso in tabuleiro.sptall:
			# 	if perso.hb_show:
			# 		pygame.draw.rect(tabuleiro.surf, (255, 0, 0), perso.hrect)
			# 		pygame.draw.rect(tabuleiro.surf, (0, 0, 0), perso.hbbrect, 2)

			debug(f'tabuleiro.mode_atual = {tabuleiro.mode_atual}')
			debug(f'screen.get_width(), screen.get_height() = {screen.get_width(), screen.get_height()}', y=170)
			debug(f'mx, my = {mx, my}', y=190)
			debug(f'tabuleiro.mousepos = {tabuleiro.mousepos}', y=210)
			debug(f'tile do mouse = {tabuleiro.mousepos[0] // bloco_tam, tabuleiro.mousepos[1] // bloco_tam}', y=230)
			debug(f'centro = {width // 2, height // 2}', y=250)
			debug(f'personagem 1 centro = {personagem1.rect.centerx, personagem1.rect.centery}', y=270)
			debug(f'tabuleiro centro = {tabuleiro.rect.centerx, tabuleiro.rect.centery}', y=290)
			debug(f'internal centro = {camera.internal_rect.centerx, camera.internal_rect.centery}', y=310)
			debug(f'tabuleiro.sptchaoonscreen = {tabuleiro.sptchaoonscreen}', y=370)
			debug(f'tabuleiro.sptchao = {tabuleiro.sptchao}', y=390)

			pygame.display.update()
			clock.tick(60)

	execjogo()


if __name__ == "__main__":
	main()
