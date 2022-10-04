import pygame

pygame.init()
font = pygame.font.Font('assets/fonts/IBMPlexMono-Regular.ttf', 12)


class Debug:

	@staticmethod
	def display(info, x=20, y=130):
		display_surf = pygame.display.get_surface()
		debug_surf = font.render(str(info), True, 'Black')
		debug_rect = debug_surf.get_rect(topleft=(x, y))
		display_surf.blit(debug_surf, debug_rect)