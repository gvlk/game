import pygame
from pygame import freetype
from sys import exit

from debug import debug

if __name__ == "__main__":
	pygame.init()

width = 1450
height = int((width * (9 / 16)))
s_res = (width, height)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Jogo')
font = pygame.freetype.Font('fontes/AlumniSansPinstripe-Regular.ttf', 24)


def resize(w, h):
	return pygame.display.set_mode((w, h), pygame.RESIZABLE)


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


class Background:
	def __init__(self, w, h):
		self.oimage = pygame.image.load('graphics/background/background.png').convert()
		self.image = pygame.transform.smoothscale(self.oimage, (w, h))
		self.surf = self.image

	def update(self, w, h):
		self.image = pygame.transform.smoothscale(self.oimage, (w, h))
		self.surf = self.image


def main():

	bg = Background(width, height)

	from tabuleiro import Tabuleiro, bloco_tam, bloco_qnt
	tabuleiro = Tabuleiro()
	from hud import Hud
	hud = Hud()
	from personagem import Aliado, Inimigo

	scrollboxes = pygame.sprite.Group()
	gerarscrollbox(scrollboxes)

	aliado1 = tabuleiro.add('ali', 'aliado1')
	aliado2 = tabuleiro.add('ali', 'aliado2')
	aliado3 = tabuleiro.add('ali', 'aliado3')
	aliado4 = tabuleiro.add('ali', 'aliado4')
	inimigo1 = tabuleiro.add('ini', 'inimigo1')

	tabuleiro.moverobj(aliado1, (0, 0))
	tabuleiro.moverobj(aliado2, (1, 2))
	tabuleiro.moverobj(aliado3, (3, 4))
	tabuleiro.moverobj(aliado4, (5, 6))
	tabuleiro.moverobj(inimigo1, (6, 4))

	tabuleiro.posicaoinicial()

	# DEBUGRENDER1 = pygame.USEREVENT + 1
	# pygame.time.set_timer(DEBUGRENDER1, 500)

	def execjogo():
		mx = my = int()
		ax, by = (-tabuleiro.rect.x, -tabuleiro.rect.y)  # Constantes para descobrir a posição do mouse relativa ao tabuleiro
		mouse_scrollboxes = list()
		centro = (width/2, height/2)
		renderalltiles = True  # Primeiramente renderizar todos tiles
		box: Scrollbox
		perso: Aliado | Inimigo
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
					mouseblo = (tabuleiro.mousepos[0] // bloco_tam, tabuleiro.mousepos[1] // bloco_tam)
					if (0 <= mouseblo[0] <= bloco_qnt - 1) and (0 <= mouseblo[1] <= bloco_qnt - 1):
						tabuleiro.mouseblo = mouseblo
					else:
						tabuleiro.mouseblo = (None, None)

				elif event.type == pygame.MOUSEBUTTONDOWN:
					if tabuleiro.mode_atual == 'def':
						obj = tabuleiro.objslc
						if obj:
							tabuleiro.mode_atual = 'slc'
					elif tabuleiro.mode_atual == 'atk':
						tabuleiro.objslc.atacar()
					else:
						menuitem = hud.mouseslc((mx, my))
						if menuitem:
							if menuitem.nome == 'mov':
								if tabuleiro.mode_atual != 'mov':
									tabuleiro.objslc.update()
									tabuleiro.objslc.imgslc()
									tabuleiro.mode_atual = 'mov'
							elif menuitem.nome == 'atk':
								if tabuleiro.mode_atual != 'atk':
									tabuleiro.objslc.imgatk()
									tabuleiro.mode_atual = 'atk'
						else:
							if tabuleiro.mode_atual == 'atk':
								tabuleiro.objslc.atacar()

				elif event.type == pygame.MOUSEBUTTONUP:
					if tabuleiro.mode_atual == 'mov':
						if not hud.crect.collidepoint((mx, my)):
							if (tabuleiro.mouseblo[0] is not None) and (tabuleiro.mouseblo[1] is not None):
								if tabuleiro.moverobj(tabuleiro.objslc, tabuleiro.mouseblo):
									tabuleiro.mode_atual = 'def'

				elif event.type == pygame.KEYDOWN:
					if tabuleiro.mode_atual != 'def':
						tabuleiro.mousepos = (-1, -1)
						if event.key == pygame.K_ESCAPE:
							tabuleiro.objslc.update()
							tabuleiro.mouseslc()
							tabuleiro.mode_atual = 'def'
						elif event.key == pygame.K_q:
							if tabuleiro.mode_atual != 'mov':
								tabuleiro.persoslc()  # Tirar o destaque o atual alvo
								tabuleiro.objslc.update()
								tabuleiro.objslc.imgslc()
								tabuleiro.mode_atual = 'mov'
						elif event.key == pygame.K_w:
							if tabuleiro.mode_atual != 'atk':
								tabuleiro.objslc.update()
								tabuleiro.mouseslc()  # Resetar textura do bloco atual
								tabuleiro.objslc.imgatk()
								tabuleiro.mode_atual = 'atk'

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

			scrollboxes.draw(screen)

			if tabuleiro.mode_atual == 'def':
				tabuleiro.persoslc()
			else:
				screen.blit(hud.hsurf, hud.hrect)
				hud.hsurf.blit(hud.csurf, hud.crect)
				hud.sptmenu.draw(screen)
				hud.mouseslc((mx, my))
				if tabuleiro.mode_atual == 'mov':
					tabuleiro.mouseslc()
				elif tabuleiro.mode_atual == 'atk':
					if isinstance(tabuleiro.objslc, Aliado):
						tabuleiro.persoslc('ini')
					elif isinstance(tabuleiro.objslc, Inimigo):
						tabuleiro.persoslc('ali')

			for perso in tabuleiro.sptall:
				if perso.hb_show:
					pygame.draw.rect(tabuleiro.surf, (255, 0, 0), perso.hrect)
					pygame.draw.rect(tabuleiro.surf, (0, 0, 0), perso.hbbrect, 2)

			debug(f'mx, my = {mx, my}')
			debug(f'tabuleiro.mousepos = {tabuleiro.mousepos}', y=170)
			debug(f'tabuleiro.mouseblo = {tabuleiro.mouseblo}', y=190)
			debug(f'tabuleiro.mode_atual = {tabuleiro.mode_atual}', y=210)
			debug(f'aliado1.pos = {aliado1.pos}', y=230)
			debug(f'aliado2.pos = {aliado2.pos}', y=250)
			debug(f'aliado3.pos = {aliado3.pos}', y=270)
			debug(f'aliado4.pos = {aliado4.pos}', y=290)
			debug(f'tabuleiro.sptchaoonscreen = {tabuleiro.sptchaoonscreen}', y=310)
			try:
				debug(f'tabuleiro.objslc.nome = {tabuleiro.objslc.nome}', y=330)
			except AttributeError:
				debug(f'tabuleiro.objslc.nome = None', y=330)
			try:
				debug(f'aliado1.mira.nome = {aliado1.mira.nome}', y=350)
			except AttributeError:
				debug(f'aliado1.mira.nome = None', y=350)
			debug(f'aliado1.current_health = {aliado1.current_health}', y=370)
			debug(f'inimigo1.current_health = {inimigo1.current_health}', y=390)
			debug(f'aliado1.hrect = {aliado1.hrect}', y=410)
			debug(f'inimigo1.hrect = {inimigo1.hrect}', y=430)

			pygame.display.update()
			clock.tick(60)

	execjogo()


if __name__ == "__main__":
	main()
