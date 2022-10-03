import pygame

from pygame.math import Vector2

from random import randint, choice

from modules.mouse import Mouse
from modules.tabuleiro import Tabuleiro

class GameController:
    def __init__(self, width, height):
        # setup game parameters
        pygame.init()
        pygame.freetype.init()
        pygame.event.set_grab(True)
        pygame.display.set_caption('Jogo do GUI')
        pygame.freetype.Font('assets/fonts/AlumniSansPinstripe-Regular.ttf', 24)
        pygame.mouse.set_visible(False)

        # setup game
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        # setup game modules
        self.mouse = Mouse()
        self.mouse_group = pygame.sprite.Group(self.mouse)
        self.board = Tabuleiro((width, height))

        # setup game variable
        self.mouse_pos = pygame.math.Vector2()
        self.offset = pygame.math.Vector2()
        self.moving_state = None
        self.membroiter = {
			'i': -1,
			'A': list(self.board.grouptimeA),
			'B': list(self.board.grouptimeB)
		}

        # initialize game
        self.generateTeams()
        self.setupSoldiers()
        self.initializeWorld()

    def generateTeams(self):
        for i in range(0, 2):
            if i % 2 == 0:
                while True:
                    if self.board.add(False, 'A', (randint(1, self.board.tile_amount), randint(1, self.board.tile_amount))):
                        break
            else:
                while True:
                    if self.board.add(False, 'B', (randint(1, self.board.tile_amount), randint(1, self.board.tile_amount))):
                        break

    def setupSoldiers(self):
        pass

    def initializeWorld(self):
        while True:
            self.catchEvents()
            self.tickWorld()
            

    def catchEvents(self):
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            # Resize window
            if event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            # Mouse movement
            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()
                self.board.mousepos = (self.mouse_pos + self.offset) // self.board.camera_group.zoom

            # Mouse scroll
            # if event.type == pygame.MOUSEWHEEL:
            #     amp = event.y * 0.01
            #     if 0.5 <= self.board.camera_group.zoom + amp <= 1.5:
            #         self.board.camera_group.zoom += amp

            # Mouse click
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.board.mode_atual == 'mov':
                        if self.board.moverobj(self.board.objslc):
                            self.moving_state = self.board.objslc
                            self.board.mode_atual = 'def'
                        else:
                            self.moving_state = None

            # Key press
            if event.type == pygame.KEYDOWN:
                self.catchKeyPress(event)
    
    def catchKeyPress(self, event):
        if self.board.mode_atual != 'def':
            if event.key == pygame.K_ESCAPE:
                self.board.resettiles({self.board.objslc.bloco})  # Resetar o bloco atual
                self.board.resettiles(self.board.objslc.caminhos)  # Resetar os blocos da área de movimento
                self.board.resetobj(self.board.objslc, limparslc=True)
                self.board.mode_atual = 'def'
            elif event.key == pygame.K_q:
                if self.board.mode_atual != 'mov':
                    self.board.resettiles(self.board.objslc.caminhos)  # Resetar os blocos da área de movimento
                    if self.board.objslc.mira:
                        self.board.resetobj(self.board.objslc.mira)
                    self.board.resetobj(self.board.objslc, img='slc')
                    self.board.mode_atual = 'mov'
            elif event.key == pygame.K_w:
                if self.board.mode_atual != 'atk':
                    self.board.gerarchances()
                    self.board.resettiles(self.board.objslc.caminhos)  # Resetar os blocos da área de movimento
                    self.board.objslc.imgatk()
                    self.board.mode_atual = 'atk'
            elif event.key == pygame.K_d or event.key == pygame.K_a:
                self.board.resettiles([self.board.objslc.bloco])  # Resetar o bloco atual
                self.board.resettiles(self.board.objslc.caminhos)  # Resetar os blocos da área de movimento
                if self.board.objslc.mira:
                    self.board.resetobj(self.board.objslc.mira)
                if self.board.objslc:
                    if self.board.objslc in self.board.grouptimeA or self.board.objslc is None:
                        time = 'A'
                    else:
                        time = 'B'
                    self.membroiter['i'] = self.membroiter[time].index(self.board.objslc)
                    if event.key == pygame.K_d:
                        self.membroiter['i'] += 1
                        if self.membroiter['i'] > len(self.membroiter[time]) - 1:
                            self.membroiter['i'] = 0
                        self.board.objslc = self.membroiter[time][self.membroiter['i']]
                    else:  # event.key == pygame.K_a:
                        self.membroiter['i'] -= 1
                        if self.membroiter['i'] < 0:
                            self.membroiter['i'] = len(self.membroiter[time]) - 1
                        self.board.objslc = self.membroiter[time][self.membroiter['i']]
                        self.board.hoverobj()  # Mudar sprite do objeto selecionado para 'slc'
        else:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    def tickWorld(self):
        # Animação de movimento do soldado
        if self.moving_state:
            if self.moving_state.movimentar():
                self.moving_state = None

        # Hover
        if self.board.mode_atual == 'def' or self.board.mode_atual == 'slc':
            if self.board.hoverobj():
                self.mouse_group.remove(self.mouse)  # self.mouse some quando está sobre um personagem válido
            else:
                self.mouse_group.add(self.mouse)
        elif self.board.mode_atual == 'mov':
            if self.board.hovertile():
                self.mouse_group.remove(self.mouse)
            else:
                self.mouse_group.add(self.mouse)
        elif self.board.mode_atual == 'atk':
            if self.board.objslc in self.board.grouptimeA:
                alvo = self.board.hoverobj('B')
            else:
                alvo = self.board.hoverobj('A')

            if alvo:
                self.mouse_group.remove(self.mouse)
            else:
                self.mouse_group.add(self.mouse)

        # Render
        self.board.camera_group.drawsprites(self.board, self.mouse_pos)

        self.offset = self.getMouseOffset(
			self.board.rect.x, 
            self.board.rect.y,
			self.board.camera_group.internal_surf_size[0], 
            self.board.camera_group.internal_surf_size[1], 
            self.board.camera_group.zoom,
			self.screen.get_width(), 
            self.screen.get_height(), 
            self.board.rect.w
		)

		# self.screen.blit(self.board.camera_group.scaled_surf, self.board.camera_group.scaled_rect)  # Zoom Desligado
        self.screen.blit(self.board.camera_group.internal_surf, self.board.camera_group.internal_rect)

        # Mouse
        self.mouse.rect.center = self.mouse_pos
        self.mouse_group.draw(self.screen)
            
        # Debug
        # debug(f'FPS {int(clock.get_fps())}')
		# 	debug(f'mouse_pos = {mouse_pos}', y=150)
		# 	debug(f'tabuleiro mousepos = {tabuleiro.mousepos}', y=170)
		# 	debug(f'tile atual = {tabuleiro.mousepos[0] // 128, tabuleiro.mousepos[1] // 128}', y=190)
		# 	debug(f'tiles sendo atualizados = {tabuleiro.groupchao}', y=210)
		# 	debug(soldadoA, y=230)
		# 	debug(soldadoB, y=250)
		# 	debug(f'selecionado = {tabuleiro.objslc}', y=270)
		# 	try:
		# 		debug(f'tile do soldado = {tabuleiro.objslc.pos}', y=290)
		# 	except AttributeError:
		# 		debug(None, y=290)
		# 	debug(f'disância entre soldados = {tabuleiro.getdistance(soldadoA.bloco, soldadoB.bloco)}', y=310)
		# 	try:
		# 		debug(f'chance de hit (A -> B) = {soldadoA.hitchances[soldadoB]}%', y=330)
		# 	except KeyError:
		# 		debug(None, y=330)
		# 	try:
		# 		debug(f'chance de hit (B -> A) = {soldadoB.hitchances[soldadoA]}%', y=350)
		# 	except KeyError:
		# 		debug(None, y=350)

        # Run tick
        pygame.display.update()
        self.clock.tick(60)

    def getMouseOffset(self, x, y, iw, ih, z, w, h, ts) -> Vector2:
	    return pygame.math.Vector2(
	    	((iw - w + ts * (z - 1)) / 2) - x,
	    	((ih - h + ts * (z - 1)) / 2) - y
	    )
                

    
