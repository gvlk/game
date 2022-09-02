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
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Jogo')
font = pygame.freetype.Font('fontes/AlumniSansPinstripe-Regular.ttf', 24)
scrolling = True


class Background:
	def __init__(self, w, h):
		self.oimage = pygame.image.load('graphics/background/background.png').convert()
		self.image = pygame.transform.smoothscale(self.oimage, (w, h))
		self.surf = self.image

	def update(self, w, h):
		self.image = pygame.transform.smoothscale(self.oimage, (w, h))
		self.surf = self.image


class Scrollbox(pygame.sprite.Sprite):
	def __init__(self, w, h):
		super().__init__()
		self.image = pygame.surface.Surface((w, h))
		self.direcao = None


def gerarscrollbox(grupo):
	grossura = height * (1/8)
	scroll_sens = 7
	for i in range(4):
		if i == 0:
			box = Scrollbox(width, grossura)
			box.rect = box.image.get_rect(topleft=(0, 0))
			box.direcao = (0, scroll_sens)
		elif i == 1:
			box = Scrollbox(width, grossura)
			box.rect = box.image.get_rect(bottomleft=(0, height))
			box.direcao = (0, -scroll_sens)
		elif i == 2:
			box = Scrollbox(grossura, height)
			box.rect = box.image.get_rect(topleft=(0, 0))
			box.direcao = (scroll_sens, 0)
		elif i == 3:
			box = Scrollbox(grossura, height)
			box.rect = box.image.get_rect(topright=(width, 0))
			box.direcao = (-scroll_sens, 0)
		else:
			box = None
		box.image.set_colorkey((0, 0, 0))
		grupo.add(box)


def resize(w, h):
	return pygame.display.set_mode((w, h), pygame.RESIZABLE)


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

	from tabuleiro import Tabuleiro, bloco_tam, bloco_qnt
	tabuleiro = Tabuleiro()
	from hud import Hud
	hud = Hud()
	from personagem import Aliado, Inimigo

	if scrolling:
		scrollboxes = pygame.sprite.Group()
		gerarscrollbox(scrollboxes)
	else:
		scrollboxes = tuple()

	gerartimes(tabuleiro, bloco_qnt, n=4)
	tabuleiro.posicaoinicial()

	# DEBUGRENDER1 = pygame.USEREVENT + 1
	# pygame.time.set_timer(DEBUGRENDER1, 500)

	def execjogo():
		mx = my = int()
		ax, by = (-tabuleiro.rect.x, -tabuleiro.rect.y)
		# Constantes para descobrir a posição do mouse relativa ao tabuleiro
		mouse_scrollboxes = list()
		centro = (width/2, height/2)
		renderalltiles = True  # Primeiramente renderizar todos tiles
		box: Scrollbox
		perso: Aliado | Inimigo
		obj: Aliado | Inimigo | None
		obj = None
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
					resize(event.w, event.h)
					bg.update(event.w, event.h)

				elif event.type == pygame.MOUSEMOTION:
					mx, my = pygame.mouse.get_pos()
					mouse_scrollboxes = [s for s in scrollboxes if s.rect.collidepoint((mx, my))]
					tabuleiro.mousepos = (mx + ax, my + by)

				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:

						if tabuleiro.mode_atual != 'def':  # Primeiro checar se o menu foi clicado
							menuitem = hud.mouseslc((mx, my))
							if menuitem:
								tabuleiro.resettile()

								if menuitem.nome == 'mov':
									if tabuleiro.mode_atual != 'mov':
										if obj.mira:
											tabuleiro.resetobj(obj.mira)
										tabuleiro.resetobj(img='slc')
										tabuleiro.mode_atual = 'mov'

								elif menuitem.nome == 'atk':
									if tabuleiro.mode_atual != 'atk':
										tabuleiro.objslc.imgatk()
										tabuleiro.mode_atual = 'atk'

						if tabuleiro.mode_atual == 'def' or tabuleiro.mode_atual == 'slc':
							if tabuleiro.tileocupada():
								obj = tabuleiro.hoverobj(click=True)
								if obj:
									tabuleiro.mode_atual = 'slc'
							else:
								tabuleiro.resetobj(limparslc=True)
								tabuleiro.mode_atual = 'def'

						elif tabuleiro.mode_atual == 'atk':
							if isinstance(tabuleiro.objslc, Aliado):
								alvo = tabuleiro.hoverobj('ini')
							elif isinstance(tabuleiro.objslc, Inimigo):
								alvo = tabuleiro.hoverobj('ali')
							if alvo:
								tabuleiro.ataque(defensor=alvo, valor=1)
								tabuleiro.mode_atual = 'def'

				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:

						if tabuleiro.mode_atual == 'mov':
							if not hud.crect.collidepoint((mx, my)):
								if tabuleiro.moverobj2(tabuleiro.objslc):
									tabuleiro.mode_atual = 'def'

				elif event.type == pygame.KEYDOWN:
					if tabuleiro.mode_atual != 'def':
						tabuleiro.resettile()

						if event.key == pygame.K_ESCAPE:
							tabuleiro.resetobj(limparslc=True)
							tabuleiro.mode_atual = 'def'

						elif event.key == pygame.K_q:
							if tabuleiro.mode_atual != 'mov':
								if obj.mira:
									tabuleiro.resetobj(obj.mira)
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
								tabuleiro.hoverobj()  # Quando muda para 'mov' objslc que mostra selecionado

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
								tabuleiro.hoverobj()

				# elif event.type == DEBUGRENDER1:
				# 	if ligado:
				# 		# aliado1.image = pygame.image.load('graphics/inimigos/inimigo.png').convert_alpha()
				# 		ligado = False
				# 	else:
				# 		# aliado1.image = pygame.image.load('graphics/aliados/aliado.png').convert_alpha()
				# 		ligado = True

			if mouse_scrollboxes:
				for box in mouse_scrollboxes:
					movex = box.direcao[0]
					movey = box.direcao[1]
					if tabuleiro.rect.topleft[0] + movex > centro[0] or tabuleiro.rect.bottomright[0] + movex < centro[0]:
						movex = 0
					if tabuleiro.rect.topleft[1] + movey > centro[1] or tabuleiro.rect.bottomright[1] + movey < centro[1]:
						movey = 0
					tabuleiro.rect.move_ip(movex, movey)
					ax, by = (-tabuleiro.rect.x, -tabuleiro.rect.y)

			# Render
			screen.blit(bg.surf, (0, 0))
			# pygame.draw.rect(screen, 'Blue', (111, 20, 300, 300))
			screen.blit(tabuleiro.surf, tabuleiro.rect)

			if not renderalltiles:
				tabuleiro.sptchaoonscreen.draw(tabuleiro.surf)
			else:
				renderalltiles = False
				tabuleiro.sptchao.draw(tabuleiro.surf)

			tabuleiro.sptaliados.draw(tabuleiro.surf)
			tabuleiro.sptinimigos.draw(tabuleiro.surf)

			# scrollboxes.draw(screen)  Não precisa draw as scrollboxes ??? ue

			# Coisas que precisam acontecer constantemente
			if tabuleiro.mode_atual == 'def' or tabuleiro.mode_atual == 'slc':
				tabuleiro.hoverobj()

			if tabuleiro.mode_atual != 'def':  # 'slc', 'mov', 'atk'
				screen.blit(hud.hsurf, hud.hrect)
				hud.hsurf.blit(hud.csurf, hud.crect)
				hud.sptmenu.draw(screen)
				hud.mouseslc((mx, my))
				hud_botleft_surf, hud_botleft_rect = hud.bottomleftcontainer(tabuleiro.objslc)
				pygame.draw.rect(screen, hud.botleftcont_fundo_cor, hud.botleftcont_fundo)
				screen.blit(hud_botleft_surf, hud_botleft_rect)

				if tabuleiro.mode_atual == 'mov':
					tabuleiro.hovertile()

				elif tabuleiro.mode_atual == 'atk':
					if isinstance(tabuleiro.objslc, Aliado):
						tabuleiro.hoverobj('ini')
					elif isinstance(tabuleiro.objslc, Inimigo):
						tabuleiro.hoverobj('ali')

			for perso in tabuleiro.sptall:
				if perso.hb_show:
					pygame.draw.rect(tabuleiro.surf, (255, 0, 0), perso.hrect)
					pygame.draw.rect(tabuleiro.surf, (0, 0, 0), perso.hbbrect, 2)

			debug(f'tabuleiro.mode_atual = {tabuleiro.mode_atual}')
			debug(f'mx, my = {mx, my}', y=190)
			debug(f'tabuleiro.mousepos = {tabuleiro.mousepos}', y=210)
			debug(f'tile do mouse = {tabuleiro.mousepos[0] // bloco_tam, tabuleiro.mousepos[1] // bloco_tam}', y=230)
			debug(f'tabuleiro.sptchaoonscreen = {tabuleiro.sptchaoonscreen}', y=370)
			debug(f'tabuleiro.sptchao = {tabuleiro.sptchao}', y=390)

			pygame.display.update()
			clock.tick(60)

	execjogo()


if __name__ == "__main__":
	main()
