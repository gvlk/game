import pygame


class Mouse(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		image = pygame.image.load('assets/images/extras/mouse.png')
		self.image = pygame.transform.scale(image, pygame.math.Vector2(image.get_size()) * 4).convert_alpha()
		self.rect = self.image.get_rect()
