import pygame
import pygame.freetype

from main import s_res, font
s_w, s_h = s_res

from personagem import Soldado


class Hud:
	def gerarmenu(self):
		item_tam = int(self.cnt_res[1] * 0.7)
		item_posy = self.cnt_xy[1]
		item_qnt = len(self.menu)
		for i, item in enumerate(self.menu):
			nome = item
			item_posx = 9 + (self.cnt_xy[0] + ((self.cnt_res[0] / item_qnt) * (i - 1)))
			if item == 'mov':
				imgdef = self.imgmov
				imgslc = self.imgmovslc
			else:
				imgdef = self.imgatk
				imgslc = self.imgatkslc
			menuitem = MenuItem(
				nome,
				item_posx,
				item_posy,
				pygame.transform.smoothscale(imgdef, (item_tam, item_tam)),
				pygame.transform.smoothscale(imgslc, (item_tam, item_tam)))
			self.sptmenu.add(menuitem)
			self.menu[item] = menuitem

	def __init__(self):
		imgdef = pygame.image.load('graphics/hud/template/hud.png').convert_alpha()
		imgdef = pygame.transform.smoothscale(imgdef, s_res)
		imgcnt = pygame.image.load('graphics/hud/template/container.png')
		self.cnt_res = (112, 56)
		imgcnt = pygame.transform.smoothscale(imgcnt, self.cnt_res)
		self.imgmov = pygame.image.load('graphics/hud/menu/mov.png').convert_alpha()
		self.imgmovslc = pygame.image.load('graphics/hud/menu/mov_slc.png').convert_alpha()
		self.imgatk = pygame.image.load('graphics/hud/menu/atk.png').convert_alpha()
		self.imgatkslc = pygame.image.load('graphics/hud/menu/atk_slc.png').convert_alpha()
		self.font = font
		self.font.fgcolor = (255, 255, 255)
		self.font.size = 40
		self.botleftcont_pos = (s_w / 3, s_h / 1.2)
		self.botleftcont_fundo = pygame.rect.Rect((0, 0), (150, 50))
		self.botleftcont_fundo.center = (s_w / 3, s_h / 1.2)
		self.botleftcont_fundo_cor = (10, 10, 10)
		self.hsurf = imgdef
		self.hrect = self.hsurf.get_rect(center=(s_w // 2, s_h // 2))
		self.csurf = imgcnt
		self.cnt_xy = (s_w / 2, s_h / 1.2)
		self.crect = self.csurf.get_rect(center=self.cnt_xy)
		self.sptmenu = pygame.sprite.Group()
		self.menu = {
			'mov': None,
			'atk': None,
		}
		self.gerarmenu()

	def mouseslc(self, mousepos: tuple):
		item: MenuItem
		for item in self.sptmenu:
			if not item.rect.collidepoint(mousepos):
				item.imgdef()
			else:
				item.imgslc()
				return item

	def bottomleftcontainer(self, obj: Aliado | Inimigo):
		obj: Aliado | Inimigo
		surf, rect = self.font.render(text=obj.nome)
		rect.center = self.botleftcont_fundo.center
		return surf, rect


class MenuItem(pygame.sprite.Sprite):
	def __init__(self, nome, x, y, imgdef, imgslc):
		super().__init__()
		self.nome = nome
		self.imgs = {'def': imgdef, 'slc': imgslc}
		self.imgatual = 'def'
		self.image = self.imgs[self.imgatual]
		self.rect = self.image.get_rect(midleft=(x, y))

	def imgslc(self):
		if self.imgatual != 'slc':
			self.imgatual = 'slc'
			self.image = self.imgs[self.imgatual]

	def imgdef(self):
		if self.imgatual != 'def':
			self.imgatual = 'def'
			self.image = self.imgs[self.imgatual]











