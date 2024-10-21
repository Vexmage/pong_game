import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Game window dimensions
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong with AI, Teleport, and Flashing Ball")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game objects dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 10

# Speeds
PADDLE_SPEED = 6
TELEPORT_DISTANCE = 60  # Distance to teleport when Q or A is pressed
BALL_X_SPEED = 4
BALL_Y_SPEED = 4
FAST_BALL_SPEED = 8  # Speed when the ball is flashing red
AI_SPEED = 4  # Speed for the AI paddle

# Teleport visual effect duration
BOOST_VISUAL_DURATION = 0.1  # Time in seconds to flash red after teleport

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

# Ball state
ball_is_fast = False
ball_flash_end_time = 0

# Scoring
player1_score = 0
ai_score = 0
font = pygame.font.SysFont("comicsans", 50)

# Game loop control
run = True
clock = pygame.time.Clock()

# Track boost effect
boost_active = False
boost_end_time = 0

# Functions
def draw():
    win.fill(BLACK)
    
    # Set the paddle color based on whether boost is active
    paddle_color = RED if boost_active else WHITE
    
    # Set the ball color based on whether it's in fast mode
    ball_color = RED if ball_is_fast else WHITE

    # Draw paddles
    pygame.draw.rect(win, paddle_color, (player1_x, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(win, WHITE, (ai_x, ai_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    
    # Draw ball
    pygame.draw.circle(win, ball_color, (ball_x, ball_y), BALL_RADIUS)
    
    # Draw scores
    player1_text = font.render(str(player1_score), 1, WHITE)
    ai_text = font.render(str(ai_score), 1, WHITE)
    win.blit(player1_text, (WIDTH // 4, 20))
    win.blit(ai_text, (WIDTH * 3 // 4, 20))
    
    pygame.display.update()

def handle_ball_movement():
    global ball_x, ball_y, ball_x_vel, ball_y_vel, player1_score, ai_score, ball_is_fast

    # Move the ball
    ball_x += ball_x_vel
    ball_y += ball_y_vel

    # Bounce off top or bottom walls
    if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= HEIGHT:
        ball_y_vel = -ball_y_vel
        ball_is_fast = False  # Ball returns to normal after hitting a wall

    # Bounce off paddles
    if (ball_x - BALL_RADIUS <= player1_x + PADDLE_WIDTH and player1_y <= ball_y <= player1_y + PADDLE_HEIGHT) or \
       (ball_x + BALL_RADIUS >= ai_x and ai_y <= ball_y <= ai_y + PADDLE_HEIGHT):
        ball_x_vel = -ball_x_vel
        ball_is_fast = False  # Ball returns to normal after hitting a paddle

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
    global ball_x, ball_y, ball_x_vel, ball_y_vel, ball_is_fast
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_x_vel = random.choice([BALL_X_SPEED, -BALL_X_SPEED])
    ball_y_vel = random.choice([BALL_Y_SPEED, -BALL_Y_SPEED])
    ball_is_fast = False  # Reset ball to normal mode

def handle_player1_movement():
    global player1_y, boost_active, boost_end_time
    keys = pygame.key.get_pressed()

    # Regular movement with W and S
    if keys[pygame.K_w] and player1_y > 0:
        player1_y -= PADDLE_SPEED
    if keys[pygame.K_s] and player1_y + PADDLE_HEIGHT < HEIGHT:
        player1_y += PADDLE_SPEED

    # Check if the boost (teleport) visual effect should end
    current_time = time.time()
    if boost_active and current_time >= boost_end_time:
        boost_active = False

    # Teleport with Q (up) and A (down)
    if keys[pygame.K_q]:
        player1_y -= TELEPORT_DISTANCE
        if player1_y < 0:
            player1_y = 0
        boost_active = True
        boost_end_time = current_time + BOOST_VISUAL_DURATION  # Flash red for a short duration
    if keys[pygame.K_a]:
        player1_y += TELEPORT_DISTANCE
        if player1_y + PADDLE_HEIGHT > HEIGHT:
            player1_y = HEIGHT - PADDLE_HEIGHT
        boost_active = True
        boost_end_time = current_time + BOOST_VISUAL_DURATION  # Flash red for a short duration

def check_ball_paddle_collision():
    global ball_is_fast, ball_x_vel, ball_y_vel

    # Check if ball hits player 1's paddle while paddle is in boost mode
    if (ball_x - BALL_RADIUS <= player1_x + PADDLE_WIDTH and
            player1_y <= ball_y <= player1_y + PADDLE_HEIGHT and boost_active):
        ball_is_fast = True  # Make ball flash and go faster
        ball_x_vel = FAST_BALL_SPEED if ball_x_vel > 0 else -FAST_BALL_SPEED
        ball_y_vel = FAST_BALL_SPEED if ball_y_vel > 0 else -FAST_BALL_SPEED

# Main game loop
while run:
    clock.tick(60)  # 60 frames per second
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Player 1 movement with regular and teleport controls
    handle_player1_movement()

    # AI movement
    handle_ai_movement()

    # Handle ball movement
    handle_ball_movement()

    # Check for collision between ball and boosted paddle
    check_ball_paddle_collision()

    # Draw everything
    draw()

# Quit Pygame
pygame.quit()
