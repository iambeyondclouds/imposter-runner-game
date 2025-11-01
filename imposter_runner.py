import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🤖 Imposter Runner")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
gravity = 0.6
jump_power = -12
speed = 6

# Load robot image
robot_img = pygame.image.load("robot.png")
robot_img = pygame.transform.scale(robot_img, (100, 100))  # Resize
player_rect = robot_img.get_rect()
player_rect.topleft = (100, 260)
player_y_velocity = 0
is_jumping = False

# Obstacles
obstacles = []
spawn_timer = 0

# Fonts
font = pygame.font.SysFont("Arial", 30)

# Score
score = 0

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Jump on space key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                player_y_velocity = jump_power=-14
                is_jumping = True

    # Gravity effect
    player_y_velocity += gravity
    player_rect.y += player_y_velocity

    # Ground collision
    if player_rect.y >= 300:
        player_rect.y = 300
        player_y_velocity = 0
        is_jumping = False

    # Spawn obstacles
    spawn_timer += 1
    if spawn_timer > 80:
        obstacle = pygame.Rect(WIDTH, 340, 40, 40)
        obstacles.append(obstacle)
        spawn_timer = 0

    # Move obstacles
    for obstacle in obstacles[:]:
        obstacle.x -= speed
        if obstacle.x < -40:
            obstacles.remove(obstacle)
            score += 1

    # Collision detection
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle.inflate(-10, -10)):
            text = font.render("💥 Game Over! Score: " + str(score), True, (255, 0, 0))
            screen.blit(text, (200, 150))
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

    # Draw robot and obstacles
    screen.blit(robot_img, player_rect)
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, obstacle)

    # Draw score
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

