import island
import variables
import pygame
from buttons import button
import menus
import tile_classes

class game_():
	__slots__ = ("t_size", "height", "main_island", "name", "build_buttons", "show_buildings", "building_image", "top_coords", "building_type")

	def __init__(self, win_size, name):
		self.t_size = 32
		self.height = 14
		self.main_island = island.island(int(win_size[0] / self.t_size), self.height)
		self.name = name
		self.show_buildings = False
		self.building_image = None

	def load(self):
		self.main_island.to_classes()
		self.build_buttons = tile_classes.build_buttons

	def save(self):
		self.main_island.to_save()
		self.build_buttons = None
		self.show_buildings = False
		self.building_image = None

	def reset_top_coords(self):
		self.top_coords = [[tower[-1].coords, tower[-1].name] for tower in self.main_island.top]

	def run(self, window, mouse_pos, mouse_press):
		window.fill(variables.sky_blue)
		self.main_island.draw_island(self.t_size, window)

		mouse_pos, mouse_press = pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0]
		self.build_buttons[0].draw(window, mouse_pos, mouse_press)
		if self.build_buttons[0].pressed:
			menus.wait_mouse_up()
			self.show_buildings = True

		if self.show_buildings:
			for button in self.build_buttons[1:]:
				button.draw(window, mouse_pos, mouse_press)
				if button.pressed:
					self.building_type = button.text
					self.building_image = pygame.image.load(tile_classes.paths[self.building_type] + '.png')
					self.building_image.fill((255, 255, 255, 120), None, pygame.BLEND_RGBA_MULT)
					break

			if self.building_image != None:
				closest = variables.round_spec(mouse_pos[0]), variables.round_spec(mouse_pos[1])
				window.blit(self.building_image, (closest))

				if mouse_press:
					self.reset_top_coords()
					closest = [closest[0] / 32, (closest[1] / 32) + 1]
					coords = [tile[0] for tile in self.top_coords]
					names = [tile[1] for tile in self.top_coords]

					if closest in coords:
						currently = names[coords.index(closest)]
						if currently == "grass" or currently == "roof":
							self.main_island.top[coords.index(closest)][-1] = tile_classes.create_class(self.building_type, closest)
							self.main_island.top[coords.index(closest)].append(tile_classes.roof([int(closest[0]), int(closest[1] - 1)]))

						# elif currently == "roof":
						# 	below = self.main_island.top[coords.index((closest[0], closest[1] + 1))].name

						# 	if self.building == 2:

						# 		self.main_island.top[coords.index(closest)] = tile_classes.woodcutting(closest)
						# 	elif self.building == 3:
						# 		self.main_island.top[coords.index(closest)] = tile_classes.mining(closest)
						# 	elif self.building == 4:
						# 		self.main_island.top[coords.index(closest)] = tile_classes.house(closest)



		pygame.display.update()