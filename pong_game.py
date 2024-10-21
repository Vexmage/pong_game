import pygame
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong with AI")

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
AI_SPEED = 4  # Speed for the AI paddle

# Player positions
player1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
ai_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
player1_x = 20
ai_x = WIDTH - PADDLE_WIDTH - 20

# Ball position and speed
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_x_vel = random.choice([BALL_X_SPEED, -BALL_X_SPEED])
ball_y_vel = random.choice([BALL_Y_SPEED, -BALL_Y_SPEED])

# Scoring
player1_score = 0
ai_score = 0
font = pygame.font.SysFont("comicsans", 50)

# Game loop control
run = True
clock = pygame.time.Clock()

# Functions
def draw():
    win.fill(BLACK)
    # Draw paddles
    pygame.draw.rect(win, WHITE, (player1_x, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(win, WHITE, (ai_x, ai_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    
    # Draw ball
    pygame.draw.circle(win, WHITE, (ball_x, ball_y), BALL_RADIUS)
    
    # Draw scores
    player1_text = font.render(str(player1_score), 1, WHITE)
    ai_text = font.render(str(ai_score), 1, WHITE)
    win.blit(player1_text, (WIDTH // 4, 20))
    win.blit(ai_text, (WIDTH * 3 // 4, 20))
    
    pygame.display.update()

def handle_ball_movement():
    global ball_x, ball_y, ball_x_vel, ball_y_vel, player1_score, ai_score

    ball_x += ball_x_vel
    ball_y += ball_y_vel

    # Bounce off top or bottom
    if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= HEIGHT:
        ball_y_vel = -ball_y_vel

    # Bounce off paddles
    if (ball_x - BALL_RADIUS <= player1_x + PADDLE_WIDTH and player1_y <= ball_y <= player1_y + PADDLE_HEIGHT) or \
       (ball_x + BALL_RADIUS >= ai_x and ai_y <= ball_y <= ai_y + PADDLE_HEIGHT):
        ball_x_vel = -ball_x_vel

    # Score for AI
    if ball_x - BALL_RADIUS <= 0:
        ai_score += 1
        reset_ball()

    # Score for player 1
    if ball_x + BALL_RADIUS >= WIDTH:
        player1_score += 1
        reset_ball()

def handle_ai_movement():
    global ai_y
    # Basic AI follows the ball with some delay
    if ball_y > ai_y + PADDLE_HEIGHT // 2:
        ai_y += AI_SPEED
    elif ball_y < ai_y + PADDLE_HEIGHT // 2:
        ai_y -= AI_SPEED

    # Prevent AI from going off the screen
    if ai_y < 0:
        ai_y = 0
    if ai_y + PADDLE_HEIGHT > HEIGHT:
        ai_y = HEIGHT - PADDLE_HEIGHT

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

    # Get key presses for Player 1 movement
    keys = pygame.key.get_pressed()
    
    # Player 1 movement
    if keys[pygame.K_w] and player1_y - PADDLE_SPEED > 0:
        player1_y -= PADDLE_SPEED
    if keys[pygame.K_s] and player1_y + PADDLE_HEIGHT + PADDLE_SPEED < HEIGHT:
        player1_y += PADDLE_SPEED

    # AI movement
    handle_ai_movement()

    # Handle ball movement
    handle_ball_movement()
    
    # Draw everything
    draw()

# Quit Pygame
pygame.quit()
