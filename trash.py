import pygame
from random import randint

class Trash():
	def __init__(self, width, height, reduction, time_to_shrink):
		# image
		self.image = pygame.image.load("trash.png")
		self.size_max = 250
		self.size_min = 40
		# born
		self.size = int(self.size_max * 1.3)
		self.born = True
		self.born_up = self.size//2 / 60
		self.time_to_shrink_born = (self.size - self.size_max) / self.born_up

		# position
		self.width = width
		self.height = height
		self.x = width//2
		self.y = height + self.size//2
		self.x_speed = 0
		self.y_speed = 0
		# movement
		self.max_x_speed = 6
		self.max_y_speed = 4.5
		self.acceleration = 2
		self.decelerate = 1

		self.y_max = 400
		self.y_min = 100

		# shrink
		self.time_to_shrink = time_to_shrink
		self.shrink = False
		self.end_shrink = False
		self.fall_x = 0
		# reduction
		self.y_reduction = (self.y_max - self.y_min)/reduction
		self.size_reduction = (self.size_max - self.size_min)/reduction

	def end_life(self):
		if self.end_shrink and self.y >= self.height - self.size:
			return True
		else:
			return False

	def end_x(self):
		return int(self.x)

	def sub_time_shrink(self):
		if self.time_to_shrink == 0:
			self.shrink = True
		else:
			self.time_to_shrink -= 1

	def is_shrink_min(self):
		return self.size <= self.size_min

	def accelerate(self, x_speed, y_speed):
		# vertex x
		if abs(self.x_speed) < self.max_x_speed:
			self.x_speed += x_speed * self.acceleration
		# vertex y
		if abs(self.y_speed) < self.max_y_speed:
			self.y_speed += y_speed * self.acceleration

	def born_animation(self):
		if self.y <= self.height:
			self.born = False
		else:
			self.y -= self.born_up
			# reduce size
			if self.size > self.size_min:
				self.size -= self.size_reduction

	def rise(self):
		# reduce y
		if self.y > self.y_min:
			self.y -= self.y_reduction

	def fall(self):
		self.decelerate = 0.01
		self.accelerate(self.fall_x, 1)

	def update(self):
		if self.born: self.born_animation()
		if self.y <= self.y_min:
			self.end_shrink = True
			self.shrink = False
			self.fall_x = randint(-10,10)/10
		if self.end_shrink: self.fall()
		if self.shrink and (not self.end_shrink): self.rise()
		if self.shrink: self.size_update()
		if not self.born:
			self.movement_update()
			self.decel_update()

	def size_update(self):
		# reduce size
		if self.size > self.size_min:
			self.size -= self.size_reduction

	def movement_update(self):
		# update position
		self.x += self.x_speed
		self.y += self.y_speed
		# limits
		if self.x > self.width: self.x = self.width-1
		if self.x < 0: self.x = 1
		if self.y > self.height: self.y = self.height-1
		if self.y < 0: self.y = 1

	def decel_update(self):
		# decelerate (abs value)
		decelx, decely = (0,0)
		if self.x_speed != 0:
			if self.x_speed > 0: decelx = self.decelerate
			else: decelx = -self.decelerate
		if self.y_speed != 0:
			if self.y_speed > 0: decely = self.decelerate
			else: decely = -self.decelerate
		self.x_speed -= decelx
		self.y_speed -= decely

	def render(self, window):
		size = int(self.size)
		image = pygame.transform.scale(self.image, (size, size))
		x = self.x - size//2
		y = self.y - size//2
		window.blit(image, (x,y))
		# debug, red dot in the midle
		# pygame.draw.rect(window, (255,0,0), (self.x, self.y, 1, 1))
