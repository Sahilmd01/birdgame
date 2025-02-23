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

# Load Background PNG
background_image = pygame.image.load(r"png/background.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale the background to fit the screen

# Load New Background PNG for Level 2
new_background_image = pygame.image.load(r"png/new_background.jpg").convert()
new_background_image = pygame.transform.scale(new_background_image, (WIDTH, HEIGHT))  # Scale to fit

# Load New Background PNG for Level 3
new_background_image2 = pygame.image.load(r"png/new_background2.jpg").convert()
new_background_image2 = pygame.transform.scale(new_background_image2, (WIDTH, HEIGHT))  # Scale to fit

# Load Pipe PNGs (top and bottom)
pipe_top_image = pygame.image.load(r"png/top_pipe.png").convert_alpha()  # Use your actual top pipe image path
pipe_bottom_image = pygame.image.load(r"png/bottom_pipe.png").convert_alpha()  # Use your actual bottom pipe image path

# Load Moving Block PNG
block_image = pygame.image.load(r"png/block.png").convert_alpha()  # Use your actual block image path
block_image = pygame.transform.scale(block_image, (BLOCK_WIDTH, BLOCK_HEIGHT))  # Scale to fit the block dimensions

# Load Gold Coin PNG
coin_image = pygame.image.load(r"png/gold.png").convert_alpha()  # Use your actual gold coin image path
coin_image = pygame.transform.scale(coin_image, (COIN_WIDTH, COIN_HEIGHT))  # Scale to coin size

# Persistent collected coin count (this value will not reset)
persistent_coins_collected = 0

# Function to reset game variables
def reset_game():
    bird.y = HEIGHT // 2 - BIRD_HEIGHT // 2
    bird_movement = 0
    pipe_top.x = WIDTH
    pipe_bottom.x = WIDTH
    global score, pipe_speed, block_list, coin_list
    score = 0
    pipe_speed = 6  # Reset pipe speed on game restart
    block_list = []  # Reset block list
    coin_list = []  # Reset coin list
    return bird_movement

# Bird setup
bird = pygame.Rect(50, HEIGHT // 2 - BIRD_HEIGHT // 2, BIRD_WIDTH, BIRD_HEIGHT)
bird_movement = 0
gravity = 0.4

# Pipe setup
pipe_height = random.randint(400, 400)
pipe_top = pygame.Rect(WIDTH, 0, PIPE_WIDTH, pipe_height)
pipe_bottom = pygame.Rect(WIDTH, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe_height - PIPE_GAP)
pipe_speed = 6

# Moving block setup
block_list = []  # List to hold multiple blocks
block_speed = 8  # Speed of the block

# Gold coin setup (multiple coins)
coin_list = []  # List to hold multiple coins
coin_speed = pipe_speed  # Coins move with the pipes

# Game Variables
score = 0
game_over = False
paused = False  # Variable to track pause state
selection_mode = False  # Variable to track if in selection screen

# Function to create a new block
def create_block():
    block = pygame.Rect(-BLOCK_WIDTH, random.randint(100, HEIGHT - BLOCK_HEIGHT), BLOCK_WIDTH, BLOCK_HEIGHT)
    return block

# Function to create a new coin
def create_coin():
    coin_x = WIDTH + random.randint(300, 600)  # Spawns coin further along the screen
    coin_y = random.randint(100, HEIGHT - COIN_HEIGHT)
    return pygame.Rect(coin_x, coin_y, COIN_WIDTH, COIN_HEIGHT)

# Function to create a row of coins (3-5 coins in a row)
def create_coin_row():
    num_coins = random.randint(1,2)  # Set coins in a row between 3 and 5
    coins = []
    # Ensure coins do not overlap with the pipes
    base_y = random.randint(100, HEIGHT - COIN_HEIGHT -5)  # Base Y position for coins
    for i in range(num_coins):
        coin_y = base_y + i * (COIN_HEIGHT +5)  # Arrange coins in a vertical row
        coin_x = WIDTH + random.randint(300, 600)  # Spawns coin further along the screen
        coins.append(pygame.Rect(coin_x, coin_y, COIN_WIDTH, COIN_HEIGHT))
    return coins

# Function to create multiple rows of coins
def create_multiple_coin_rows(num_rows):
    coins = []
    for _ in range(num_rows):
        coins.extend(create_coin_row())
    return coins

# Function to display "Game Over" and wait for restart
def game_over_screen():
    text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    pygame.display.update()

    # Wait for key press to restart
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press SPACE to restart
                    waiting = False
        pygame.time.Clock().tick(30)

# Function to display pause screen
def pause_screen():
    text = font.render("Paused", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()

# Function to display bird selection screen
def bird_selection_screen():
    screen.blit(background_image, (0, 0))  # Draw background first

    # Display instruction text
    instruction_text = font.render("Select Your Bird", True, BLACK)
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, 50))

    # Calculate positions for bird images
    margin = 50
    spacing = 20
    birds_per_row = 4
    bird_size = BIRD_WIDTH, BIRD_HEIGHT
    start_x = margin
    start_y = 100
    selected_bird_rects = []

    for index, bird_img in enumerate(bird_images):
        row = index // birds_per_row
        col = index % birds_per_row
        x = start_x + col * (bird_size[0] + spacing)
        y = start_y + row * (bird_size[1] + spacing)
        screen.blit(bird_img, (x, y))
        bird_rect = pygame.Rect(x, y, bird_size[0], bird_size[1])
        selected_bird_rects.append(bird_rect)

    pygame.display.update()

    # Wait for user to select a bird
    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for idx, rect in enumerate(selected_bird_rects):
                    if rect.collidepoint(mouse_pos):
                        select_bird(idx)
                        selecting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to cancel selection
                    selecting = False
        pygame.time.Clock().tick(30)

# Function to select a bird
def select_bird(index):
    global current_bird_image, current_bird_index
    if 0 <= index < len(bird_images):
        current_bird_index = index
        current_bird_image = bird_images[current_bird_index]

# Function to display current bird selection
def display_current_bird():
    text = font.render(f"Current Bird: {current_bird_index + 1}", True, BLACK)
    screen.blit(text, (WIDTH - 250, 10))

# Function to display vault with collected coins
def display_vault():
    screen.fill(WHITE)  # Clear the screen
    vault_text = font.render(f"Total Coins Collected: {persistent_coins_collected}", True, BLACK)
    screen.blit(vault_text, (WIDTH // 2 - vault_text.get_width() // 2, HEIGHT // 2))

    pygame.display.update()
    pygame.time.wait(2000)  # Show for 2 seconds before returning

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not paused:
                bird_movement = -8  # Flap the bird up
            if event.key == pygame.K_SPACE and game_over:
                game_over = False  # Restart the game
            if event.key == pygame.K_p and not selection_mode:  # Pause the game
                paused = not paused
            if event.key == pygame.K_m and not selection_mode:  # Show Vault
                display_vault()
            if event.key == pygame.K_b:  # Bird selection
                selection_mode = True
                bird_selection_screen()
                selection_mode = False

    if not paused and not game_over and not selection_mode:
        # Background Scrolling Logic
        if score < 10:
            screen.blit(background_image, (0, 0))  # Level 1 background
        elif 10 <= score < 20:
            screen.blit(new_background_image, (0, 0))  # Level 2 background
        else:
            screen.blit(new_background_image2, (0, 0))  # Level 3 background

        # Bird Movement
        bird_movement += gravity
        bird.y += bird_movement

        # Move Pipes
        pipe_top.x -= pipe_speed
        pipe_bottom.x -= pipe_speed

        # If pipes move out of the screen, reposition them
        if pipe_top.x + PIPE_WIDTH < 0:
            pipe_height = random.randint(400, 400)
            pipe_top.x = WIDTH
            pipe_bottom.x = WIDTH
            pipe_top.height = pipe_height
            pipe_bottom.y = pipe_height + PIPE_GAP
            pipe_bottom.height = HEIGHT - pipe_height - PIPE_GAP

        # Move Coins
        for coin in coin_list:
            coin.x -= coin_speed

        # If coin moves out of the screen, reposition it
        coin_list = [coin for coin in coin_list if coin.x + COIN_WIDTH > 0]

        # Check if we need to create more coins
        if len(coin_list) < 5:  # Keep at least 5 rows of coins on screen at all times
            coin_list.extend(create_multiple_coin_rows(5 - len(coin_list)))

        # Check if Bird Collects Coin
        for coin in coin_list[:]:
            if bird.colliderect(coin):
                persistent_coins_collected += 1  # Persistently store coins collected
                coin_list.remove(coin)

        # Move and draw the blocks
        for block in block_list:
            block.x += block_speed
            screen.blit(block_image, (block.x, block.y))  # Draw block

            # If block moves out of the screen, reset its position
            if block.x > WIDTH:
                block.x = -BLOCK_WIDTH
                block.y = random.randint(100, HEIGHT - BLOCK_HEIGHT)

        # Draw Bird
        screen.blit(current_bird_image, (bird.x, bird.y))  # Replace bird block with current bird image

        # Draw Pipes using PNG images
        screen.blit(pygame.transform.scale(pipe_top_image, (PIPE_WIDTH, pipe_top.height)), (pipe_top.x, pipe_top.y))
        screen.blit(pygame.transform.scale(pipe_bottom_image, (PIPE_WIDTH, pipe_bottom.height)), (pipe_bottom.x, pipe_bottom.y))

        # Draw Coins
        for coin in coin_list:
            screen.blit(coin_image, (coin.x, coin.y))  # Draw the coin

        # Collision Detection
        for block in block_list:
            if bird.colliderect(block):
                game_over = True

        if bird.colliderect(pipe_top) or bird.colliderect(pipe_bottom) or bird.top <= 0 or bird.bottom >= HEIGHT:
            game_over = True

        # Draw Score
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))

        # Draw Vault with coins collected in the corner
        vault_text = font.render(f'Coins: {persistent_coins_collected}', True, BLACK)
        screen.blit(vault_text, (10, 50))

        # Optionally display current bird selection
        display_current_bird()

    elif paused and not selection_mode:
        # Game is paused
        pause_screen()

    elif game_over and not selection_mode:
        # Game Over
        game_over_screen()

        # Reset game variables for the next round, coins persist
        bird_movement = reset_game()
        game_over = False

    # Update Screen
    pygame.display.update()

    # Frame Rate
    pygame.time.Clock().tick(30)
