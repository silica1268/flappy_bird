import pygame
from pygame.locals import *

import random
import math

w, h = 1280, 720

pygame.init()
screen = pygame.display.set_mode((w, h), RESIZABLE)
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# todo: save score and best score, add start screen

# bird constants
bird_h = 1/16
bird_w = bird_h
bird_x = 1/math.e-bird_w/2
bird_a = 1/2048
bird_jump_v = -1/64
minimum_v_to_jump = 0

# pipe constants
pipe_hole_w = bird_w*3
pipe_hole_h = bird_h*6
pipe_spacing = bird_w*8+pipe_hole_w
pipe_v = bird_w/16

# game constants
high_score = 0

# graphics
sky_img = pygame.image.load("sky.png")
sky_img_size = sky_img.get_rect().size

bird_img = pygame.image.load("bird.png")
bird_img_size = bird_img.get_rect().size

pipe_img = pygame.image.load("pipe.png")
pipe_img_flipped = pygame.transform.flip(pipe_img, False, True)
pipe_img_size = pipe_img.get_rect().size

font = pygame.font.Font("custom_font.ttf", 40)


space_was_pressed = False


def init_parameters():
	global bird_y, bird_v, first_pipe_x, pipe_hole_ys, score

	bird_y = 1/2-bird_h/2
	bird_v = 0

	first_pipe_x = bird_w*10
	pipe_hole_ys = [get_new_pipe_hole_y()]

	score = 0

def get_new_pipe_hole_y():
	return random.uniform(0, 1-pipe_hole_h)

def get_pipe_x(i):
	return bird_x*w + (first_pipe_x + i*pipe_spacing)*h

def draw_img(img, img_x, img_y, img_w, img_h):
	screen.blit(pygame.transform.scale(img, (img_w, img_h)), (img_x, img_y))

init_parameters()

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	screen.fill(pygame.Color(0, 180, 230))

	# todo: add infinite sky

	draw_img(sky_img, 0, 0, int(h*sky_img_size[0]/sky_img_size[1]), h)

	w, h = pygame.display.get_surface().get_size()

	pipe_hole_h_pixels = pipe_hole_h*h
	pipe_hole_w_pixels = pipe_hole_w*h
	bird_x_pixels = bird_x*w
	bird_y_pixels = bird_y*h
	bird_w_pixels = bird_w*h
	bird_h_pixels = bird_h*h

	n_pipes_to_add = math.floor((w-get_pipe_x(len(pipe_hole_ys)-1))/(pipe_spacing*h))
	if n_pipes_to_add > 0:
		for i in range(n_pipes_to_add):
			pipe_hole_ys.append(get_new_pipe_hole_y())

	for i in reversed(range(len(pipe_hole_ys))):
		# todo: get most pixel parameters out of the loop
		pipe_hole_y_pixels = pipe_hole_ys[i]*h
		pipe_x_pixels = get_pipe_x(i)
		if bird_x_pixels+bird_w_pixels > pipe_x_pixels and bird_x_pixels < pipe_x_pixels+pipe_hole_w_pixels and (bird_y_pixels < pipe_hole_y_pixels or bird_y_pixels+bird_h_pixels > pipe_hole_y_pixels+pipe_hole_h_pixels):
			init_parameters()
			break
		if pipe_x_pixels < -pipe_hole_w_pixels:
			first_pipe_x += pipe_spacing
			pipe_hole_ys = pipe_hole_ys[i+1:]
			score += 1
			if score > high_score:
				high_score = score
			break
		pipe_img_h_scaled = pipe_img_size[1]*pipe_hole_w_pixels/pipe_img_size[0]
		# pygame.draw.rect(screen, "green", pygame.Rect(int(pipe_x_pixels), int(0), int(pipe_hole_w_pixels), int(pipe_hole_y_pixels)))
		draw_img(pipe_img_flipped, int(pipe_x_pixels), int(pipe_hole_y_pixels-pipe_img_h_scaled), int(pipe_hole_w_pixels), int(pipe_img_h_scaled))
		# pygame.draw.rect(screen, "green", pygame.Rect(int(pipe_x_pixels), int(pipe_hole_y_pixels+pipe_hole_h_pixels), int(pipe_hole_w_pixels), int(h-pipe_hole_h_pixels-pipe_hole_y_pixels)))
		draw_img(pipe_img, int(pipe_x_pixels), int(pipe_hole_y_pixels+pipe_hole_h_pixels), int(pipe_hole_w_pixels), int(pipe_img_h_scaled))


	# pygame.draw.rect(screen, "yellow", pygame.Rect(int(bird_x*w), int(bird_y*h), int(bird_w*h), int(bird_h*h)))

	draw_img(bird_img, int(bird_x_pixels), int(bird_y_pixels), int(bird_w_pixels), int(bird_h_pixels))

	font_img = font.render(str(score)+"/"+str(high_score), True, "white")
	screen.blit(font_img, (w/64, h/64))

	pygame.display.flip()

	if bird_y < -bird_h or bird_y > 1:
		init_parameters()

	if pygame.key.get_pressed()[pygame.K_SPACE]:
		if not space_was_pressed and bird_v > minimum_v_to_jump:
			bird_v = bird_jump_v
			space_was_pressed = True
	else:
		space_was_pressed = False

	bird_v += bird_a
	bird_y += bird_v

	first_pipe_x -= pipe_v

	clock.tick(120)


pygame.quit()