import pygame

pygame.init()
font = pygame.font.Font('fontes/IBMPlexMono-Regular.ttf', 12)


def debug(info, x=20, y=150):
	display_surf = pygame.display.get_surface()
	debug_surf = font.render(str(info), True, 'Grey')
	debug_rect = debug_surf.get_rect(topleft=(x, y))
	display_surf.blit(debug_surf, debug_rect)
