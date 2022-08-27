import pygame


class Hud:
	def __init__(self):
		from main import Setup
		width = Setup.width
		height = Setup.height
		self.font = Setup.font
		self.dispsurf = pygame.display.get_surface()
		self.texto = "TESTE TESTE TESTE TESTE TESTE TESTE TESTE TESTE TESTE \n" # Freetype nao tem \n




