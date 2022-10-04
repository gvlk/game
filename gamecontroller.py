import pygame

from pygame.math import Vector2
from random import randint

from modules.mouse import Mouse
from modules.board import Board
from modules.debug import Debug


class GameController:
    def __init__(self, width: int, height: int):
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
        self.mouse_group = pygame.sprite.GroupSingle(self.mouse)
        self.board = Board((width, height))
        self.debug = Debug()

        # setup game variables
        self.mouse_pos = pygame.math.Vector2()
        self.offset = pygame.math.Vector2()
        self.moving_state = None
        self.soldier_iter = {
            'i': -1,
            'A': list(self.board.group_team_A),
            'B': list(self.board.group_team_B)
        }

        # initialize game
        self.generateTeams()
        self.setupSoldiers()
        self.initializeWorld()

    def generateTeams(self) -> None:
        for i in range(0, 2):
            if i % 2 == 0:
                while True:
                    if self.board.addSoldier(
                            f'Soldado{randint(100, 999)}',
                            'A',
                            (randint(1, self.board.tile_amount), randint(1, self.board.tile_amount))
                    ):
                        break
            else:
                while True:
                    if self.board.addSoldier(
                            f'Soldado{randint(100, 999)}',
                            'B',
                            (randint(1, self.board.tile_amount), randint(1, self.board.tile_amount))
                    ):
                        break

    def setupSoldiers(self) -> None:
        pass

    def initializeWorld(self) -> None:
        while True:
            self.catchEvents()
            self.tickWorld()

    def catchEvents(self) -> None:
        for event in pygame.event.get():

            # quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # resize window
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            # mouse movement
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = Vector2(pygame.mouse.get_pos())
                self.board.mouse_pos = self.mouse_pos + self.offset

            # mouse click down
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.board.current_mode == 'def' or self.board.current_mode == 'slc':
                        if self.board.isTileOccupied():
                            self.board.hoverSoldier(click=True)
                            self.board.current_mode = 'slc'
                        else:
                            if self.board.selected_soldier:  # Resetar soldado selecionado
                                self.board.selected_soldier.update()
                                self.board.selected_soldier.imageUpdate()
                                self.board.selected_soldier = None
                                self.board.current_mode = 'def'

            # mouse click up
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.board.current_mode == 'mov':
                        if self.board.moveSoldier(self.board.selected_soldier):
                            self.moving_state = self.board.selected_soldier
                            self.board.current_mode = 'def'
                        else:
                            self.moving_state = None

            # key press
            elif event.type == pygame.KEYDOWN:
                self.catchKeyPress(event)

    def catchKeyPress(self, event: pygame.event.Event) -> None:
        if self.board.current_mode != 'def':

            if event.key == pygame.K_ESCAPE:
                self.board.resetTiles({self.board.selected_soldier.tile})  # Resetar o tile atual
                self.board.resetTiles(self.board.selected_soldier.paths)  # Resetar os blocos da área de movimento
                self.board.selected_soldier.update()
                self.board.selected_soldier.imageUpdate()
                self.board.selected_soldier = None
                self.board.current_mode = 'def'

            elif event.key == pygame.K_q:
                if self.board.current_mode != 'mov':
                    self.board.resetTiles(self.board.selected_soldier.paths)  # Resetar os blocos da área de movimento
                    if self.board.selected_soldier.aim:
                        self.board.selected_soldier.aim.update()
                        self.board.selected_soldier.aim.imageUpdate()
                    self.board.current_mode = 'mov'

            elif event.key == pygame.K_w:
                if self.board.current_mode != 'atk':
                    self.board.generateHitChances()
                    self.board.resetTiles(self.board.selected_soldier.paths)  # Resetar os blocos da área de movimento
                    self.board.selected_soldier.imageUpdate('atk')
                    self.board.current_mode = 'atk'

            elif event.key == pygame.K_d or event.key == pygame.K_a:
                self.board.resetTiles([self.board.selected_soldier.tile])  # Resetar o tile atual
                self.board.resetTiles(self.board.selected_soldier.paths)  # Resetar os blocos da área de movimento
                if self.board.selected_soldier.aim:
                    self.board.selected_soldier.aim.update()
                    self.board.selected_soldier.aim.imageUpdate()
                if self.board.selected_soldier:
                    if self.board.selected_soldier in self.board.group_team_A or self.board.selected_soldier is None:
                        time = 'A'
                    else:
                        time = 'B'
                    self.soldier_iter['i'] = self.soldier_iter[time].index(self.board.selected_soldier)
                    if event.key == pygame.K_d:
                        self.soldier_iter['i'] += 1
                        if self.soldier_iter['i'] > len(self.soldier_iter[time]) - 1:
                            self.soldier_iter['i'] = 0
                        self.board.selected_soldier = self.soldier_iter[time][self.soldier_iter['i']]
                    else:  # event.key == pygame.K_a:
                        self.soldier_iter['i'] -= 1
                        if self.soldier_iter['i'] < 0:
                            self.soldier_iter['i'] = len(self.soldier_iter[time]) - 1
                        self.board.selected_soldier = self.soldier_iter[time][self.soldier_iter['i']]
                        self.board.hoverSoldier()  # Mudar sprite do objeto selecionado para 'slc'

        else:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    def tickWorld(self) -> None:

        # animação de movimento do soldado
        if self.moving_state:
            if self.moving_state.move():
                self.moving_state = None

        # hover
        if self.board.current_mode == 'def' or self.board.current_mode == 'slc':
            if self.board.hoverSoldier():
                self.mouse_group.remove(self.mouse)  # self.mouse some quando está sobre um personagem válido
            else:
                self.mouse_group.add(self.mouse)
        elif self.board.current_mode == 'mov':
            if self.board.hoverTile():
                self.mouse_group.remove(self.mouse)
            else:
                self.mouse_group.add(self.mouse)
        elif self.board.current_mode == 'atk':
            if self.board.selected_soldier in self.board.group_team_A:
                alvo = self.board.hoverSoldier('B')
            else:
                alvo = self.board.hoverSoldier('A')

            if alvo:
                self.mouse_group.remove(self.mouse)
            else:
                self.mouse_group.add(self.mouse)

        # render
        self.board.group_camera.drawSprites(self.board, self.mouse_pos)
        self.screen.blit(self.board.group_camera.internal_surf, self.board.group_camera.internal_rect)

        # mouse
        self.offset = self.getMouseOffset(
            self.board.rect.x,
            self.board.rect.y,
            self.board.group_camera.internal_surf_size[0],
            self.board.group_camera.internal_surf_size[1],
            self.screen.get_width(),
            self.screen.get_height(),
        )
        self.mouse.rect.center = self.mouse_pos
        self.mouse_group.draw(self.screen)

        # debug
        self.debug.display(f'FPS {int(self.clock.get_fps())}', 1)
        self.debug.display(f'Current Mode: {self.board.current_mode}', 2)
        self.debug.display(f'Selected Soldier: {self.board.selected_soldier}', 3)
        self.debug.display('Soldiers:', 4)
        for i, soldier in enumerate(self.board.group_soldiers):
            self.debug.display(f'{soldier}, Tile: {soldier.pos}, Rect: {soldier.rect}', 5 + i)

        # run tick
        pygame.display.update()
        self.clock.tick(60)

    @staticmethod
    def getMouseOffset(x: int, y: int, iw: int, ih: int, w: int, h: int) -> Vector2:
        return pygame.math.Vector2(
            ((iw - w) / 2) - x,
            ((ih - h) / 2) - y
        )
