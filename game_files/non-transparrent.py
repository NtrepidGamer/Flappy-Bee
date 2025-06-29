import pygame, ctypes, sys, random, json, os

pygame.init()
screen_w, screen_h = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_w, screen_h), pygame.NOFRAME)
pygame.display.set_caption("Flappy Bird")

# Transparent background setup (Windows)
hwnd = pygame.display.get_wm_info()['window']
ctypes.windll.user32.SetWindowLongW(hwnd, -20, ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x80000)
ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0xFF00FF, 0, 1)

# File Setup
os.makedirs("./data", exist_ok=True)
score_file = "./data/high_score.json"
high_score = 0
if os.path.exists(score_file):
    try:
        high_score = json.load(open(score_file)).get("high_score", 0)
    except:
        pass

# Game Variables
pipe_gap, pipe_w, pipe_dist = 300, 100, 800
bird = pygame.Rect(screen_w // 4, screen_h // 2, 100, 50)
vel, gravity, flap = 0, 0.5, -12.5
pipes = []
font = pygame.font.SysFont(None, 144)
score, speed = 0, 5
color_key = (0, 100, 170)


# Pipe Generator
def new_pipe(x):
    h = random.randint(100, screen_h - pipe_gap - 100)
    return [pygame.Rect(x, 0, pipe_w, h), pygame.Rect(x, h + pipe_gap, pipe_w, screen_h)]


# Reset
def reset():
    global pipes, bird, vel, score
    bird.y, vel, score = screen_h // 2, 0, 0
    pipes.clear()
    for i in range(4): pipes.append(new_pipe(screen_w + i * pipe_dist))


reset()
clock = pygame.time.Clock()

# Main Loop
while True:
    screen.fill(color_key)

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            json.dump({"high_score": high_score}, open(score_file, "w"))
            pygame.quit();
            sys.exit()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE: vel = flap

    vel += gravity
    bird.y += vel
    pygame.draw.rect(screen, (255, 255, 0), bird)

    for t, b in pipes:
        t.x -= speed;
        b.x -= speed
        pygame.draw.rect(screen, (0, 255, 0), t)
        pygame.draw.rect(screen, (0, 255, 0), b)

    if pipes and pipes[0][0].right < 0:
        pipes.pop(0)
        score += 1
        if score > high_score:
            high_score = score
            json.dump({"high_score": high_score}, open(score_file, "w"))
        pipes.append(new_pipe(pipes[-1][0].x + pipe_dist))

    if bird.bottom > screen_h or any(bird.colliderect(p) for pair in pipes for p in pair) or bird.top < -1:
        pygame.time.wait(500)
        reset()

    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (20, 20))
    screen.blit(font.render(f"High: {high_score}", True, (255, 255, 255)), (20, 100))
    pygame.display.update()
    clock.tick(60)
