import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Paddle dimensions
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90

# Ball dimensions
BALL_SIZE = 15

# Game variables
PADDLE_SPEED = 5
BALL_SPEED_X = 3
BALL_SPEED_Y = 3

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong by alexzedev")

# Create game clock
clock = pygame.time.Clock()

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dy):
        self.rect.y += dy
        self.rect.clamp_ip(screen.get_rect())

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.dx = BALL_SPEED_X * random.choice((1, -1))
        self.dy = BALL_SPEED_Y * random.choice((1, -1))

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy = -self.dy

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

# Create game objects
player = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2)
opponent = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)

# Score
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 36)

def reset_ball():
    ball.rect.center = (WIDTH // 2, HEIGHT // 2)
    ball.dx = BALL_SPEED_X * random.choice((1, -1))
    ball.dy = BALL_SPEED_Y * random.choice((1, -1))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player's paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.move(-PADDLE_SPEED)
    if keys[pygame.K_DOWN]:
        player.move(PADDLE_SPEED)

    # Move the opponent's paddle (simple AI)
    if opponent.rect.centery < ball.rect.centery:
        opponent.move(PADDLE_SPEED)
    elif opponent.rect.centery > ball.rect.centery:
        opponent.move(-PADDLE_SPEED)

    # Move the ball
    ball.move()

    # Check for collisions
    if ball.rect.colliderect(player.rect) or ball.rect.colliderect(opponent.rect):
        ball.dx = -ball.dx

    # Check for scoring
    if ball.rect.left <= 0:
        opponent_score += 1
        reset_ball()
    elif ball.rect.right >= WIDTH:
        player_score += 1
        reset_ball()

    # Clear the screen
    screen.fill(BLACK)

    # Draw game objects
    player.draw()
    opponent.draw()
    ball.draw()

    # Draw the score
    player_text = font.render(str(player_score), True, WHITE)
    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(player_text, (WIDTH // 4, 20))
    screen.blit(opponent_text, (3 * WIDTH // 4, 20))

    # Draw the center line
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Update the display
    pygame.display.flip()

    # Control game speed
    clock.tick(60)

# Quit the game
pygame.quit()