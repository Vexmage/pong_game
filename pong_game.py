import pygame
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game objects dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 10

# Speeds
PADDLE_SPEED = 6
BALL_X_SPEED = 4
BALL_Y_SPEED = 4

# Player positions
player1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
player2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
player1_x = 20
player2_x = WIDTH - PADDLE_WIDTH - 20

# Ball position and speed
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_x_vel = random.choice([BALL_X_SPEED, -BALL_X_SPEED])
ball_y_vel = random.choice([BALL_Y_SPEED, -BALL_Y_SPEED])

# Scoring
player1_score = 0
player2_score = 0
font = pygame.font.SysFont("comicsans", 50)

# Game loop control
run = True
clock = pygame.time.Clock()

# Functions
def draw():
    win.fill(BLACK)
    # Draw paddles
    pygame.draw.rect(win, WHITE, (player1_x, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(win, WHITE, (player2_x, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    
    # Draw ball
    pygame.draw.circle(win, WHITE, (ball_x, ball_y), BALL_RADIUS)
    
    # Draw scores
    player1_text = font.render(str(player1_score), 1, WHITE)
    player2_text = font.render(str(player2_score), 1, WHITE)
    win.blit(player1_text, (WIDTH // 4, 20))
    win.blit(player2_text, (WIDTH * 3 // 4, 20))
    
    pygame.display.update()

def handle_ball_movement():
    global ball_x, ball_y, ball_x_vel, ball_y_vel, player1_score, player2_score

    ball_x += ball_x_vel
    ball_y += ball_y_vel

    # Bounce off top or bottom
    if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= HEIGHT:
        ball_y_vel = -ball_y_vel

    # Bounce off paddles
    if (ball_x - BALL_RADIUS <= player1_x + PADDLE_WIDTH and player1_y <= ball_y <= player1_y + PADDLE_HEIGHT) or \
       (ball_x + BALL_RADIUS >= player2_x and player2_y <= ball_y <= player2_y + PADDLE_HEIGHT):
        ball_x_vel = -ball_x_vel

    # Score for player 2
    if ball_x - BALL_RADIUS <= 0:
        player2_score += 1
        reset_ball()

    # Score for player 1
    if ball_x + BALL_RADIUS >= WIDTH:
        player1_score += 1
        reset_ball()

def reset_ball():
    global ball_x, ball_y, ball_x_vel, ball_y_vel
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_x_vel = random.choice([BALL_X_SPEED, -BALL_X_SPEED])
    ball_y_vel = random.choice([BALL_Y_SPEED, -BALL_Y_SPEED])

# Main game loop
while run:
    clock.tick(60)  # 60 frames per second
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Get key presses
    keys = pygame.key.get_pressed()
    
    # Player 1 movement
    if keys[pygame.K_w] and player1_y - PADDLE_SPEED > 0:
        player1_y -= PADDLE_SPEED
    if keys[pygame.K_s] and player1_y + PADDLE_HEIGHT + PADDLE_SPEED < HEIGHT:
        player1_y += PADDLE_SPEED

    # Player 2 movement
    if keys[pygame.K_UP] and player2_y - PADDLE_SPEED > 0:
        player2_y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player2_y + PADDLE_HEIGHT + PADDLE_SPEED < HEIGHT:
        player2_y += PADDLE_SPEED

    # Handle ball movement
    handle_ball_movement()
    
    # Draw everything
    draw()

# Quit Pygame
pygame.quit()
