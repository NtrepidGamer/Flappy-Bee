import time
import pygame
import ctypes
import sys
import random
import json
import os
pygame.init()

data_file = "./data/high_score.json"
os.makedirs("./data", exist_ok=True)

high_score = 0
if os.path.exists(data_file):
    try:
        with open(data_file, "r") as f:
            data = json.load(f)
            high_score = data.get("high_score", 0)
    except (json.JSONDecodeError, ValueError):
        high_score = 0  # default if file is invalid or empty
# Screen setup
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.display.set_caption("Transparent Fullscreen Window")

# Window transparency setup
hwnd = pygame.display.get_wm_info()['window']
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x80000
LWA_COLORKEY = 0x1
ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE,
    ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE) | WS_EX_LAYERED)
transparent_color = (255, 0, 255)
color_key = (transparent_color[2] << 16) | (transparent_color[1] << 8) | transparent_color[0]
ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, color_key, 0, LWA_COLORKEY)

# Game variables
pipe_speed = 5
gap = 300
pipe_width = 100
pipe_distance = 800  # Distance between pipes

# Bird
box_width, box_height = 100, 50
box_x = (screen_width - box_width) // 4
box_y = (screen_height - box_height) // 2
box = pygame.Rect(box_x, box_y, box_width, box_height)
gravity_force = 0.5
velocity = 0
flap_strength = -12.5

font = pygame.font.SysFont(None, 48 * 3)

score = 0

# Pipe list
pipes = []

# Function to create a pipe pair
def create_pipe_pair(x_pos):
    top_height = random.randint(100, screen_height - gap - 100)
    top_pipe = pygame.Rect(x_pos, 0, pipe_width, top_height)
    bottom_pipe_y = top_height + gap
    bottom_pipe = pygame.Rect(x_pos, bottom_pipe_y, pipe_width, screen_height - bottom_pipe_y)
    return top_pipe, bottom_pipe

# Initial pipes
for i in range(4):
    pipe_x = screen_width + i * pipe_distance
    pipes.append(create_pipe_pair(pipe_x))

def reset_game():
    global box, velocity, pipes, score

    box.x = (screen_width - box_width) // 4
    box.y = (screen_height - box_height) // 2
    velocity = 0
    score = 0
    pipes = []

    for i in range(4):
        pipe_x = screen_width + i * pipe_distance
        pipes.append(create_pipe_pair(pipe_x))

reset_game()

# Main loop
running = True
clock = pygame.time.Clock()
while True:
    if not running:
        if score > high_score:
            high_score = score
            with open(data_file, "w") as f:
                json.dump({"high_score": high_score}, f)

        # You can skip reading again here since you just wrote it
        # with open(data_file, "r") as f:
        #     high_score = json.load(f)["high_score"]

        time.sleep(1 / 60)
        reset_game()
        running = True

    screen.fill(transparent_color)

    text = font.render(f"score: {str(score)}", True, (255, 255, 255))  # White text
    screen.blit(text, (20, 20))  # Position (10, 10) = near top-left
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    screen.blit(high_score_text, (20, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if score > high_score:
                    high_score = score
                    with open(data_file, "w") as f:
                        json.dump({"high_score": high_score}, f)
                sys.exit()
            if event.key == pygame.K_SPACE:
                velocity = flap_strength

    # Bird movement
    velocity += gravity_force
    box.y += velocity

    # Move and draw pipes
    for pair in pipes:
        top_pipe, bottom_pipe = pair
        top_pipe.x -= pipe_speed
        bottom_pipe.x -= pipe_speed
        pygame.draw.rect(screen, (0, 255, 0), top_pipe)
        pygame.draw.rect(screen, (0, 255, 0), bottom_pipe)

    # Recycle pipes when off-screen
    if pipes and pipes[0][0].right < 0:
        pipes.pop(0)
        score += 1
        if score > high_score:
            high_score = score
            with open(data_file, "w") as f:
                json.dump({"high_score": high_score}, f)
        new_x = pipes[-1][0].x + pipe_distance
        pipes.append(create_pipe_pair(new_x))

    # Draw bird
    pygame.draw.rect(screen, (255, 255, 0), box)

    # Collision with ground
    if box.bottom >= screen_height:
        running = False

    for pipe in pipes:
        top_pipe, bottom_pipe = pipe
        if box.colliderect(top_pipe) or box.colliderect(bottom_pipe):
            running = False

    pygame.display.update()
    clock.tick(60)
