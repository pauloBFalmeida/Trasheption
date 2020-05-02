import pygame
from random import randint
from trash import Trash
from text import Text
pygame.init()

class Trasheption:
	def __init__(self, width, height, title):
		self.width = width
		self.height = height
		self.win = pygame.display.set_mode((width, height))
		pygame.display.set_caption(title)
		icon = pygame.image.load("trash.png")
		pygame.display.set_icon(icon)
		self.credits = Text(width-65,height-10, "Made by Paulo BF Almeida", 9)

		self.clock = pygame.time.Clock()
		self.running = True
		self.FPS = 60
		self.background = (0, 0, 0)

		self.reduction = 3		# can be float
		self.time_shrink = 2	# was to be int

	def new_trash(self):
		self.trash_list.append(Trash(
								self.width,
								self.height,
								self.reduction*self.FPS,
								self.time_shrink))

	def add_sec(self):
		self.sec += 1
		pygame.time.set_timer(pygame.NUMEVENTS-1, 1000)		# wait 1 sec
		self.trash_list[-1].sub_time_shrink()
		if self.trash_list[-1].is_shrink_min():
			self.new_trash()


	def start(self):
		self.points = 0
		self.text = Text(self.width//2,30, "Throw the Trash in the Trash", 45)
		self.trash_list = [Trash(	self.width,
									self.height,
									self.reduction*self.FPS,
									3)]
		self.sec = -1
		self.add_sec()
		self.point_duration = 0
		self.point_textbox = Text(100,200, "+1 Point", 35)


	def input(self, keys):
		# Player Controls
		if keys[pygame.K_a] or keys[pygame.K_LEFT]:
			self.trash_list[-1].accelerate(-1,0)
		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			self.trash_list[-1].accelerate(1,0)
		if keys[pygame.K_ESCAPE]:
			self.game_running = False

	def logic(self):
		for trash in list(self.trash_list):
			trash.update()
			if trash.end_life():
				end_x = trash.end_x()
				self.trash_list.remove(trash)
				x = self.trash_list[-1].x
				half = self.trash_list[-1].size//2
				if (x-half < end_x) and (x+half > end_x):
					self.points += 1
					self.point_duration = int(1.5 * self.FPS)
					self.point_textbox.new_color()
		self.text.update()
		self.credits.update()

	def render(self, window):
		window.fill(self.background)		# background
		self.text.render(window)
		for trash in self.trash_list:
			trash.render(window)
		if self.point_duration > 0:			# point
			self.point_textbox.render(window)
			self.point_duration -= 1
		self.credits.render(window)			# credits
		pygame.display.update()				# update screen

def main():
	game = Trasheption(800, 600, "Trasheption")
	game.start()							# start game

	while game.running:
		game.clock.tick(game.FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game.running = False
			elif event.type == pygame.NUMEVENTS-1:
				game.add_sec()

		game.input(pygame.key.get_pressed())
		game.logic()
		game.render(game.win)

	print("points: "+str(game.points))

if __name__ == "__main__":
	main()
	pygame.quit()
	quit()
