import pygame, sys, random

# Initialize pygame
pygame.init()

# Initialize mixer and play background music
pygame.mixer.init()
pygame.mixer.music.load("music.wav")
pygame.mixer.music.play(-1)  # -1 means loop forever
pygame.mixer.music.set_volume(0.5)  # 0.0 to 1.0 (adjust volume)    



# Screen setup
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)

# Game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0

# Fonts
game_font = pygame.font.Font(None, 40)

# Bird
bird_surface = pygame.image.load("ghost.png").convert_alpha()
bird_surface = pygame.transform.scale(bird_surface, (60, 60 ))
bird_rect = bird_surface.get_rect(center=(100, HEIGHT // 2))

# Pipes
pipe_width = 70  
pipe_height = 400
pipe_gap = 150
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

def create_pipe():
    random_pipe_pos = random.randint(200, 400)
    bottom_pipe = {'rect': pygame.Rect(WIDTH, random_pipe_pos, pipe_width, pipe_height), 'scored': False}
    top_pipe = {'rect': pygame.Rect(WIDTH, random_pipe_pos - pipe_gap - pipe_height, pipe_width, pipe_height), 'scored': False}
    return bottom_pipe, top_pipe



def move_pipes(pipes):
    for pipe in pipes:
        pipe['rect'].centerx -= 4
    return [pipe for pipe in pipes if pipe['rect'].right > 0]


def draw_pipes(pipes):
    for pipe in pipes:
        rect = pipe['rect']
        if rect.bottom >= HEIGHT:
            pygame.draw.rect(screen, GREEN, rect)
        else:
            pygame.draw.rect(screen, GREEN, rect)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe['rect']):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= HEIGHT:
        return False
    return True


def display_score(score):
    score_surface = game_font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, HEIGHT // 2)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.fill(BLUE)

    if game_active:
        # Bird movement
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect) 

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Collision
        game_active = check_collision(pipe_list)

        # Scoring
        for pipe in pipe_list:
            if pipe['rect'].centerx < bird_rect.centerx and not pipe['scored']:
                score += 0.5
                pipe['scored'] = True

        display_score(int(score))


    else:
        # 🖼️ Game Over Image
        game_over_surface = pygame.image.load("hehe.jpg").convert_alpha()
        game_over_surface = pygame.transform.scale(game_over_surface, (500, 200))  # Adjust size
        game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

        # Show Game Over Image
        screen.blit(game_over_surface, game_over_rect)

        # Optional message under the image
        msg_surface = game_font.render("Press SPACE to Restart", True, (255, 0, 0))
        screen.blit(msg_surface, (60, HEIGHT // 2 + 80))
        


    pygame.display.update()
    clock.tick(60)
