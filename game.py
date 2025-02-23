import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 800
BIRD_WIDTH, BIRD_HEIGHT = 40, 40
PIPE_WIDTH = 150
PIPE_GAP = 130
BLOCK_WIDTH, BLOCK_HEIGHT = 40, 40
COIN_WIDTH, COIN_HEIGHT = 60, 60  # Increased the size of the gold coin

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird by KINU')

# Font
font = pygame.font.Font(None, 36)

# Load Bird PNGs from the birds directory
def load_birds(directory):
    bird_images = []
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            path = os.path.join(directory, filename)
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (BIRD_WIDTH, BIRD_HEIGHT))
            bird_images.append(image)
    return bird_images

# Assuming birds are stored in 'png/birds/' directory
bird_images = load_birds(r"png/birds")
if not bird_images:
    raise Exception("No bird images found in the 'png/birds/' directory.")

# Set the first bird as the default
current_bird_index = 0
current_bird_image = bird_images[current_bird_index]

# Background and Pipe Setup
background_image = pygame.image.load(r"png/background.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
pipe_top_image = pygame.image.load(r"png/top_pipe.png").convert_alpha()
pipe_bottom_image = pygame.image.load(r"png/bottom_pipe.png").convert_alpha()

# Persistent collected coin count
persistent_coins_collected = 0

# Function to reset game variables
def reset_game():
    bird.y = HEIGHT // 2 - BIRD_HEIGHT // 2
    bird_movement = 0
    pipe_top.x = WIDTH
    pipe_bottom.x = WIDTH
    global score
    score = 0
    return bird_movement

# Bird setup
bird = pygame.Rect(50, HEIGHT // 2 - BIRD_HEIGHT // 2, BIRD_WIDTH, BIRD_HEIGHT)
bird_movement = 0
gravity = 0.4

# Pipe setup
pipe_height = random.randint(300, 500)
pipe_top = pygame.Rect(WIDTH, 0, PIPE_WIDTH, pipe_height)
pipe_bottom = pygame.Rect(WIDTH, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe_height - PIPE_GAP)
pipe_speed = 6

# Game Variables
score = 0
game_over = False
paused = False

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not paused:
                bird_movement = -8
            if event.key == pygame.K_SPACE and game_over:
                bird_movement = reset_game()
                game_over = False
            if event.key == pygame.K_p:
                paused = not paused
            # Bird Switching Logic
            if event.key == pygame.K_RIGHT:
                current_bird_index = (current_bird_index + 1) % len(bird_images)
                current_bird_image = bird_images[current_bird_index]
            if event.key == pygame.K_LEFT:
                current_bird_index = (current_bird_index - 1) % len(bird_images)
                current_bird_image = bird_images[current_bird_index]

    if not paused and not game_over:
        # Background
        screen.blit(background_image, (0, 0))

        # Bird movement
        bird_movement += gravity
        bird.y += bird_movement

        # Pipe movement
        pipe_top.x -= pipe_speed
        pipe_bottom.x -= pipe_speed
        if pipe_top.x + PIPE_WIDTH < 0:
            pipe_height = random.randint(300, 500)
            pipe_top.x = WIDTH
            pipe_bottom.x = WIDTH
            pipe_top.height = pipe_height
            pipe_bottom.y = pipe_height + PIPE_GAP
            pipe_bottom.height = HEIGHT - pipe_height - PIPE_GAP

        # Check if the bird passes the pipes
        if pipe_top.x + PIPE_WIDTH < bird.x and not game_over:
            score += 1

        # Collision detection
        if bird.colliderect(pipe_top) or bird.colliderect(pipe_bottom) or bird.top <= 0 or bird.bottom >= HEIGHT:
            game_over = True

        # Draw everything
        screen.blit(current_bird_image, (bird.x, bird.y))
        screen.blit(pygame.transform.scale(pipe_top_image, (PIPE_WIDTH, pipe_top.height)), (pipe_top.x, pipe_top.y))
        screen.blit(pygame.transform.scale(pipe_bottom_image, (PIPE_WIDTH, pipe_bottom.height)), (pipe_bottom.x, pipe_bottom.y))
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))

    elif game_over:
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(2000)

    pygame.display.update()
    pygame.time.Clock().tick(30)
