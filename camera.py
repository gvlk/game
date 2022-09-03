import pygame
from main import s_res


class CameraGroup(pygame.sprite.Group):
	def __init__(self, surface):
		super().__init__()
		self.surface = surface
		self.ground = None
		self.offset = pygame.math.Vector2()
		self.half_w, self.half_h = (s_res[0] / 2, s_res[1] / 2)
		self.camera_border = {
			'left': 200,
			'right': 200,
			'top': 100,
			'bottom': 100
		}
		l = self.camera_border['left']
		t = self.camera_border['top']
		w = s_res[0] - (self.camera_border['left'] + self.camera_border['right'])
		h = s_res[1] - (self.camera_border['top'] + self.camera_border['bottom'])
		self.camera_rect = pygame.Rect(l, t, w, h)
		self.keyboard_speed = 5
		self.mouse_speed = 0.4
		self.zoom = 1
		self.internal_surf_size = (2500, 2500)
		self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
		self.internal_rect = self.internal_surf.get_rect(center=(self.half_w, self.half_h))
		self.internal_surf_size_vector = pygame.math.Vector2(self.internal_surf_size)
		self.internal_offset = pygame.math.Vector2()
		self.internal_offset.x = self.internal_surf_size[0] / 2 - self.half_w
		self.internal_offset.y = self.internal_surf_size[1] / 2 - self.half_h
		self.scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_size_vector * self.zoom)
		self.scaled_rect = self.scaled_surf.get_rect(center=(self.half_w, self.half_h))

	def centralizar_alvo(self, alvo, tabuleiro):
		self.offset.x = (tabuleiro.rect.w / 2) - alvo.rect.centerx
		self.offset.y = (tabuleiro.rect.h / 2) - alvo.rect.centery
		tabuleiro.rect = self.tabuleiro_pos()

	def mouse_control(self, mouse):
		mouse = pygame.math.Vector2(mouse)
		mouse_offset = pygame.math.Vector2()
		left_border = self.camera_border['left']
		top_border = self.camera_border['top']
		right_border = s_res[0] - self.camera_border['right']
		bottom_border = s_res[1] - self.camera_border['bottom']

		if top_border < mouse.y < bottom_border:
			if mouse.x < left_border:
				mouse_offset.x = mouse.x - left_border
				pygame.mouse.set_pos((left_border, mouse.y))
			elif mouse.x > right_border:
				mouse_offset.x = mouse.x - right_border
				pygame.mouse.set_pos((right_border, mouse.y))
		elif mouse.y < top_border:
			if mouse.x < left_border:
				mouse_offset = mouse - pygame.math.Vector2(left_border, top_border)
				pygame.mouse.set_pos((left_border, top_border))
			elif mouse.x > right_border:
				mouse_offset = mouse - pygame.math.Vector2(right_border, top_border)
				pygame.mouse.set_pos((right_border, top_border))
		elif mouse.y > bottom_border:
			if mouse.x < left_border:
				mouse_offset = mouse - pygame.math.Vector2(left_border, bottom_border)
				pygame.mouse.set_pos((left_border, bottom_border))
			elif mouse.x > right_border:
				mouse_offset = mouse - pygame.math.Vector2(right_border, bottom_border)
				pygame.mouse.set_pos((right_border, bottom_border))
		if left_border < mouse.x < right_border:
			if mouse.y < top_border:
				mouse_offset.y = mouse.y - top_border
				pygame.mouse.set_pos((mouse.x, top_border))
			if mouse.y > bottom_border:
				mouse_offset.y = mouse.y - bottom_border
				pygame.mouse.set_pos((mouse.x, bottom_border))

		self.offset -= mouse_offset * self.mouse_speed

	def keyboard_control(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.offset.x -= self.keyboard_speed
		elif keys[pygame.K_RIGHT]:
			self.offset.x += self.keyboard_speed
		if keys[pygame.K_UP]:
			self.offset.y -= self.keyboard_speed
		elif keys[pygame.K_DOWN]:
			self.offset.y += self.keyboard_speed

	def tabuleiro_pos(self):
		offset_pos = pygame.math.Vector2(self.half_w, self.half_h) + self.offset + self.internal_offset
		return self.surface.get_rect(center=offset_pos)

	def drawsprites(self, tabuleiro, mouse):
		self.mouse_control(mouse)
		self.keyboard_control()
		tabuleiro.rect = self.tabuleiro_pos()
		for sprite in self.ground:
			offset_pos = sprite.rect.topleft
			self.surface.blit(sprite.image, offset_pos)

		for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft
			self.surface.blit(sprite.image, offset_pos)

		self.scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_size_vector * self.zoom)
		self.scaled_rect = self.scaled_surf.get_rect(center=(self.half_w, self.half_h))
