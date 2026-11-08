import pygame
import random

# 1. Set up the game
pygame.init()

WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Stars")

clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 20, bold=True)
big_font = pygame.font.SysFont("monospace", 34, bold=True)

# 2. Retro pixel-art colors
NAVY = (12, 18, 45)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 70)
PINK = (255, 100, 170)
CYAN = (70, 230, 240)
PURPLE = (110, 75, 180)
GREEN = (100, 255, 150)

# Tiny background stars
background_stars = [
    (random.randrange(WIDTH), random.randrange(HEIGHT))
    for _ in range(65)
]

# 3. Player and game variables
basket_x = WIDTH // 2 - 30
basket_y = HEIGHT - 65
basket_speed = 6
basket_width = 60

stars = []
score = 0
missed = 0
MAX_MISSED = 5

spawn_timer = 0
game_state = "start"


# 4. Draw a pixel-art star
def draw_star(x, y, size, color):
    points = [
        (x, y - size),
        (x + size // 4, y - size // 4),
        (x + size, y),
        (x + size // 4, y + size // 4),
        (x, y + size),
        (x - size // 4, y + size // 4),
        (x - size, y),
        (x - size // 4, y - size // 4)
    ]
    pygame.draw.polygon(screen, color, points)


# 5. Reset the game
def reset_game():
    global basket_x, stars, score, missed
    global spawn_timer, game_state

    basket_x = WIDTH // 2 - 30
    stars = []
    score = 0
    missed = 0
    spawn_timer = 0
    game_state = "playing"


# 6. Main game loop
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == "start":
                if event.key == pygame.K_SPACE:
                    reset_game()

            elif game_state == "gameover":
                if event.key == pygame.K_r:
                    reset_game()

    # Draw the night sky
    screen.fill(NAVY)

    for sx, sy in background_stars:
        screen.fill(WHITE, (sx, sy, 2, 2))

    # 7. Play the game
    if game_state == "playing":

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            basket_x -= basket_speed

        if keys[pygame.K_RIGHT]:
            basket_x += basket_speed

        # Keep basket inside the screen
        basket_x = max(0, min(WIDTH - basket_width, basket_x))

        # Create falling stars
        spawn_timer += 1

        if spawn_timer >= 35:
            stars.append({
                "x": random.randint(15, WIDTH - 15),
                "y": -10,
                "speed": random.randint(3, 5) + score // 10,
                "color": random.choice([YELLOW, PINK, CYAN])
            })
            spawn_timer = 0

        # Move stars and check catches
        basket_rect = pygame.Rect(
            basket_x, basket_y, basket_width, 30
        )

        for star in stars[:]:
            star["y"] += star["speed"]

            star_rect = pygame.Rect(
                star["x"] - 9, star["y"] - 9, 18, 18
            )

            if basket_rect.colliderect(star_rect):
                stars.remove(star)
                score += 1

            elif star["y"] > HEIGHT:
                stars.remove(star)
                missed += 1

                if missed >= MAX_MISSED:
                    game_state = "gameover"

        # Draw the stars
        for star in stars:
            draw_star(
                star["x"], star["y"], 10, star["color"]
            )

        # Draw a pixel-art basket
        pygame.draw.rect(
            screen, PURPLE,
            (basket_x, basket_y, basket_width, 8)
        )
        pygame.draw.rect(
            screen, PINK,
            (basket_x + 5, basket_y + 8, 50, 8)
        )
        pygame.draw.rect(
            screen, PURPLE,
            (basket_x + 10, basket_y + 16, 40, 8)
        )
        pygame.draw.rect(
            screen, CYAN,
            (basket_x + 20, basket_y + 24, 20, 6)
        )

        # Show score and misses
        score_text = font.render(
            f"SCORE: {score}", True, WHITE
        )
        miss_text = font.render(
            f"MISSED: {missed}/{MAX_MISSED}", True, PINK
        )

        screen.blit(score_text, (20, 18))
        screen.blit(miss_text, (20, 48))

    # 8. Start screen
    elif game_state == "start":
        title = big_font.render(
            "CATCH THE STARS", True, YELLOW
        )
        instruction = font.render(
            "PRESS SPACE TO START", True, WHITE
        )
        controls = font.render(
            "USE LEFT / RIGHT ARROWS", True, CYAN
        )

        screen.blit(title, (145, 160))
        screen.blit(instruction, (155, 235))
        screen.blit(controls, (130, 275))

        for i in range(7):
            draw_star(
                100 + i * 75, 100 + (i % 2) * 25,
                10, random.choice([YELLOW, PINK, CYAN])
            )

    # 9. Game-over screen
    elif game_state == "gameover":
        title = big_font.render(
            "GAME OVER!", True, PINK
        )
        result = font.render(
            f"YOUR SCORE: {score}", True, YELLOW
        )
        restart = font.render(
            "PRESS R TO RESTART", True, WHITE
        )

        screen.blit(title, (190, 165))
        screen.blit(result, (205, 225))
        screen.blit(restart, (170, 280))

    # Show the completed frame
    pygame.display.flip()

pygame.quit()


catch the stars game
