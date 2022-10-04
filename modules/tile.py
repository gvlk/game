import pygame


class Tile(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		imgdef = pygame.image.load('assets/images/floortiles/tile.png')
		imgslc = pygame.image.load('assets/images/floortiles/tile_slc.png')
		imgind = pygame.image.load('assets/images/floortiles/tile_ind.png')
		imgmse = pygame.image.load('assets/images/floortiles/tile_mse.png')
		imgmov = pygame.image.load('assets/images/floortiles/tile_mov.png')
		imgmovslc = pygame.image.load('assets/images/floortiles/tile_movslc.png')
		imgdef = pygame.transform.scale(imgdef, pygame.math.Vector2(imgdef.get_size()) * 4).convert_alpha()
		imgslc = pygame.transform.scale(imgslc, pygame.math.Vector2(imgslc.get_size()) * 4).convert_alpha()
		imgind = pygame.transform.scale(imgind, pygame.math.Vector2(imgind.get_size()) * 4).convert_alpha()
		imgmse = pygame.transform.scale(imgmse, pygame.math.Vector2(imgmse.get_size()) * 4).convert_alpha()
		imgmov = pygame.transform.scale(imgmov, pygame.math.Vector2(imgmov.get_size()) * 4).convert_alpha()
		imgmovslc = pygame.transform.scale(imgmovslc, pygame.math.Vector2(imgmovslc.get_size()) * 4).convert_alpha()
		self.imgs = {'def': imgdef, 'slc': imgslc, 'ind': imgind, 'mse': imgmse, 'mov': imgmov, 'movslc': imgmovslc}
		self.current_img = 'def'
		self.image = self.imgs[self.current_img]
		self.rect = self.image.get_rect(topleft=(x, y))
		self.content = None
		self.unavailable = False
		self.gcost = int()
		self.hcost = int()
		self.fcost = int()
		self.parent = None

	def imageUpdate(self, mode: str) -> None:
		if self.current_img != mode:
			self.current_img = mode
			self.image = self.imgs[mode]
