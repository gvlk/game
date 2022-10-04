import pygame

pygame.init()
font = pygame.font.Font('assets/fonts/IBMPlexMono-Regular.ttf', 12)


class Debug:

	@staticmethod
	def display(info, y):
		display_surf = pygame.display.get_surface()
		debug_surf = font.render(str(info), True, 'Black')
		debug_rect = debug_surf.get_rect(topleft=(20, 110 + (y * 20)))
		display_surf.blit(debug_surf, debug_rect)
