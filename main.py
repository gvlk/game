import pygame
from pygame import freetype
from sys import exit
from debug import debug

if __name__ == "__main__":
	pygame.init()


class Setup:
	width = 1000
	height = int((width * (9 / 16)))
	font = pygame.freetype.Font('fontes/AlumniSansPinstripe-Regular.ttf', 24)


class Background:
	def __init__(self):
		self.surf = pygame.Surface((Setup.width, Setup.height))


def main():
	screen = pygame.display.set_mode((Setup.width, Setup.height))
	pygame.display.set_caption('Jogo')
	clock = pygame.time.Clock()

	bg = Background()
	from tabuleiro import Tabuleiro
	tabuleiro = Tabuleiro()
	from hud import Hud
	hud = Hud()

	aliado1 = tabuleiro.add('ali', 'aliado1')
	inimigo1 = tabuleiro.add('ini', 'inimigo1')

	tabuleiro.moverobj(aliado1, (2, 4))
	tabuleiro.moverobj(inimigo1, (6, 4))

	pygame.event.custom_type()

	DEBUGRENDER1 = pygame.USEREVENT + 1
	pygame.time.set_timer(DEBUGRENDER1, 500)

	def execjogo():
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

				elif event.type == pygame.MOUSEMOTION:
					mousepos = pygame.mouse.get_pos()
					tabuleiro.mousepos = (mousepos[0] + tabuleiro.transf[0], mousepos[1] + tabuleiro.transf[1])
					mouseblo = (tabuleiro.mousepos[0] // tabuleiro.bloco_tam, tabuleiro.mousepos[1] // tabuleiro.bloco_tam)
					if (0 <= mouseblo[0] <= tabuleiro.qnt_blocos - 1) and (0 <= mouseblo[1] <= tabuleiro.qnt_blocos - 1):
						tabuleiro.mouseblo = mouseblo
					else:
						tabuleiro.mouseblo = (None, None)

				elif event.type == pygame.MOUSEBUTTONDOWN:
					if not tabuleiro.mode_atual == 'slc':
						obj = tabuleiro.slcobj()
						if obj:
							tabuleiro.objslc = obj
							tabuleiro.mode_atual = 'slc'

				elif event.type == pygame.MOUSEBUTTONUP:
					if tabuleiro.mode_atual == 'mov':
						if tabuleiro.moverobj(tabuleiro.objslc, tabuleiro.mouseblo):
							tabuleiro.mode_atual = 'def'

				if tabuleiro.mode_atual == 'slc':
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							tabuleiro.mode_atual = 'mov'
						elif event.key == pygame.K_w:
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

			# hud.font.render_to(screen, (100, 100), hud.texto, 'Blue')

			if tabuleiro.mode_atual != 'def':
				if tabuleiro.mode_atual == 'mov':
					tabuleiro.mouseslc()
				elif tabuleiro.mode_atual == 'atk':
					pass

			debug(f'tabuleiro.mousepos = {tabuleiro.mousepos}')
			debug(f'tabuleiro.mouseblo = {tabuleiro.mouseblo}', y=30)
			debug(f'tabuleiro.mode_atual = {tabuleiro.mode_atual}', y=70)
			debug(f'aliado1 = {aliado1}', y=90)
			debug(f'aliado1.pos = {aliado1.pos}', y=110)
			debug(f'aliado1.bloco = {aliado1.bloco}', y=130)
			debug(f'aliado1.bloco.rect = {aliado1.bloco.rect}', y=150)

			pygame.display.update()
			clock.tick(60)

	execjogo()


if __name__ == "__main__":
	main()
