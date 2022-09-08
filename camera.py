import pygame
from main import s_res
from personagem import Soldado


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
		lb = self.camera_border['left']
		tb = self.camera_border['top']
		wb = s_res[0] - (self.camera_border['left'] + self.camera_border['right'])
		hb = s_res[1] - (self.camera_border['top'] + self.camera_border['bottom'])
		self.camera_rect = pygame.Rect(lb, tb, wb, hb)
		self.keyboard_speed = 15
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

	def mouse_control(self, left, right, top, bottom, mouse):
		mouse = pygame.math.Vector2(mouse)
		mouse_offset = pygame.math.Vector2()
		limite = self.internal_surf_size[0] / 2
		if left < limite:
			left_border = self.camera_border['left']
		else:
			left_border = 0
		if right > limite:
			right_border = s_res[0] - self.camera_border['right']
		else:
			right_border = s_res[0]
		if top < limite:
			top_border = self.camera_border['top']
		else:
			top_border = 0
		if bottom > limite:
			bottom_border = s_res[1] - self.camera_border['bottom']
		else:
			bottom_border = s_res[1]

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

	def keyboard_control(self, left, right, top, bottom):
		limite = self.internal_surf_size[0] / 2
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			if left < limite:
				self.offset.x += self.keyboard_speed
		elif keys[pygame.K_RIGHT]:
			if right > limite:
				self.offset.x -= self.keyboard_speed
		if keys[pygame.K_UP]:
			if top < limite:
				self.offset.y += self.keyboard_speed
		elif keys[pygame.K_DOWN]:
			if bottom > limite:
				self.offset.y -= self.keyboard_speed

	def tabuleiro_pos(self):
		offset_pos = pygame.math.Vector2(self.half_w, self.half_h) + self.offset + self.internal_offset
		return self.surface.get_rect(center=offset_pos)

	def drawsprites(self, tabuleiro, mouse):
		sprite: Soldado
		self.mouse_control(tabuleiro.rect.left, tabuleiro.rect.right, tabuleiro.rect.top, tabuleiro.rect.bottom, mouse)
		self.keyboard_control(tabuleiro.rect.left, tabuleiro.rect.right, tabuleiro.rect.top, tabuleiro.rect.bottom)

		tabuleiro.rect = self.tabuleiro_pos()

		self.internal_surf.fill('Grey')

		for sprite in self.ground:
			offset_pos = sprite.rect.topleft
			self.surface.blit(sprite.image, offset_pos)

		for sprite in sorted(self.sprites(), key=lambda spr: spr.rect.centery):
			self.surface.blit(sprite.sombra_surf, sprite.sombra_rect)
			offset_pos = sprite.rect.topleft
			self.surface.blit(sprite.image, offset_pos)
			if sprite.hb_show:  # Health Bar
				pygame.draw.rect(self.surface, (255, 0, 0), sprite.hrect)
				pygame.draw.rect(self.surface, (0, 0, 0), sprite.hbbrect, 2)

		self.internal_surf.blit(tabuleiro.surf, tabuleiro.rect)

	# self.scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_size_vector * self.zoom)
	# self.scaled_rect = self.scaled_surf.get_rect(center=(self.half_w, self.half_h))
