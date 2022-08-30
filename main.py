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
	ax, by = tabuleiro.transf  # Constantes para descobrir a posição do mouse relativa ao tabuleiro
	from hud import Hud
	hud = Hud()
	from personagem import Aliado, Inimigo

	aliado1 = tabuleiro.add('ali', 'aliado1')
	aliado2 = tabuleiro.add('ali', 'aliado2')
	aliado3 = tabuleiro.add('ali', 'aliado3')
	inimigo1 = tabuleiro.add('ini', 'inimigo1')

	tabuleiro.moverobj(aliado1, (2, 4))
	tabuleiro.moverobj(aliado2, (4, 6))
	tabuleiro.moverobj(aliado3, (3, 1))
	tabuleiro.moverobj(inimigo1, (6, 4))

	pygame.event.custom_type()

	DEBUGRENDER1 = pygame.USEREVENT + 1
	pygame.time.set_timer(DEBUGRENDER1, 500)

	def execjogo():
		mx = my = int()
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

				elif event.type == pygame.MOUSEBUTTONUP:
					if tabuleiro.mode_atual == 'mov':
						if tabuleiro.mouseblo[0] and tabuleiro.mouseblo[1]:
							if tabuleiro.moverobj(tabuleiro.objslc, tabuleiro.mouseblo):
								tabuleiro.mode_atual = 'def'

				elif event.type == pygame.KEYDOWN:
					if tabuleiro.mode_atual != 'def':
						if event.key == pygame.K_ESCAPE:
							tabuleiro.objslc.update()
							tabuleiro.mousepos = (-1, -1)
							tabuleiro.mouseslc()
							tabuleiro.mode_atual = 'def'
						elif event.key == pygame.K_q:
							if tabuleiro.mode_atual != 'mov':
								tabuleiro.objslc.update()
								tabuleiro.objslc.imgslc()
								tabuleiro.mode_atual = 'mov'
						elif event.key == pygame.K_w:
							if tabuleiro.mode_atual != 'atk':
								tabuleiro.objslc.update()
								tabuleiro.mousepos = (-1, -1)
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

			screen.blit(bg.surf, (0, 0))
			# pygame.draw.rect(screen, 'Blue', (111, 20, 300, 300))
			screen.blit(tabuleiro.surf, tabuleiro.rect)

			tabuleiro.sptchao.draw(tabuleiro.surf)
			tabuleiro.sptaliados.draw(tabuleiro.surf)
			tabuleiro.sptinimigos.draw(tabuleiro.surf)

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

			debug(f'mx, my = {mx, my}')
			debug(f'tabuleiro.mousepos = {tabuleiro.mousepos}', y=170)
			debug(f'tabuleiro.mouseblo = {tabuleiro.mouseblo}', y=190)
			debug(f'tabuleiro.mode_atual = {tabuleiro.mode_atual}', y=210)
			debug(f'aliado1 = {aliado1}', y=230)
			debug(f'aliado1.pos = {aliado1.pos}', y=250)
			debug(f'aliado1.bloco = {aliado1.bloco}', y=270)
			debug(f'aliado1.bloco.rect = {aliado1.bloco.rect}', y=290)
			debug(f'hud.menu["mov"].rect = {hud.menu["mov"].rect}', y=310)
			debug(f'hud.menu["atk"].rect = {hud.menu["atk"].rect}', y=330)
			debug(f'hud.crect = {hud.crect}', y=350)
			debug(f'hud.cnt_xy = {hud.cnt_xy}', y=370)
			try:
				debug(f'tabuleiro.objslc.nome = {tabuleiro.objslc.nome}', y=390)
				debug(f'type(tabuleiro.objslc) = {type(tabuleiro.objslc)}', y=410)
			except AttributeError:
				pass

			pygame.display.update()
			clock.tick(60)

	execjogo()


if __name__ == "__main__":
	main()
