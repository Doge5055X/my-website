import pygame
import math
import random
import asyncio

# --- Configuration & Constants ---
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 700

# Colors
COLOR_BG = (15, 23, 42)          # Dark Slate
COLOR_COURT = (30, 41, 59)       # Dark Blue-Gray
COLOR_BALL = (234, 88, 12)       # Basketball Orange
COLOR_LINE = (255, 255, 255)     # White
COLOR_HOOP = (220, 38, 38)       # Red/Orange
COLOR_NET = (241, 245, 249)      # White
COLOR_TEXT = (255, 255, 255)     # White

# Physics
GRAVITY = 0.45
BOUNCE_DAMPING = 0.65

class Hoop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 70
        self.rim_radius = 5
        self.left_rim_x = self.x - self.width // 2
        self.right_rim_x = self.x + self.width // 2

    def draw(self, screen):
        # Backboard pole
        pygame.draw.rect(screen, (100, 116, 139), (self.x - 5, self.y - 70, 10, 70))
        # Backboard plate
        pygame.draw.rect(screen, (226, 232, 240), (self.x - 50, self.y - 65, 100, 50), border_radius=4)
        pygame.draw.rect(screen, COLOR_HOOP, (self.x - 50, self.y - 65, 100, 50), width=3, border_radius=4)
        pygame.draw.rect(screen, COLOR_HOOP, (self.x - 20, self.y - 40, 40, 25), width=2)

        # Net (Triangular mesh approximation)
        net_points_left = [(self.left_rim_x, self.y), (self.x - 20, self.y + 35), (self.x + 20, self.y + 35), (self.right_rim_x, self.y)]
        pygame.draw.lines(screen, COLOR_NET, False, net_points_left, 2)
        pygame.draw.line(screen, COLOR_NET, (self.x - 10, self.y), (self.x - 5, self.y + 35), 1)
        pygame.draw.line(screen, COLOR_NET, (self.x + 10, self.y), (self.x + 5, self.y + 35), 1)

        # Rim
        pygame.draw.line(screen, COLOR_HOOP, (self.left_rim_x, self.y), (self.right_rim_x, self.y), 6)
        pygame.draw.circle(screen, (185, 28, 28), (self.left_rim_x, self.y), self.rim_radius)
        pygame.draw.circle(screen, (185, 28, 28), (self.right_rim_x, self.y), self.rim_radius)


class Basketball:
    def __init__(self, x, y):
        self.spawn_x = x
        self.spawn_y = y
        self.radius = 22
        self.reset()

    def reset(self):
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.vx = 0
        self.vy = 0
        self.is_thrown = False
        self.has_scored = False

    def update(self):
        if self.is_thrown:
            # Apply Gravity
            self.vy += GRAVITY
            self.x += self.vx
            self.y += self.vy

            # Wall Collisions
            if self.x - self.radius < 0:
                self.x = self.radius
                self.vx *= -BOUNCE_DAMPING
            elif self.x + self.radius > SCREEN_WIDTH:
                self.x = SCREEN_WIDTH - self.radius
                self.vx *= -BOUNCE_DAMPING

            # Floor Collision / Reset if ball falls out of screen bottom
            if self.y - self.radius > SCREEN_HEIGHT:
                self.reset()
                return True # Indicates shot finished
        return False

    def draw(self, screen):
        # Draw Ball Shadow if on starting position
        if not self.is_thrown:
            pygame.draw.ellipse(screen, (30, 41, 59), (self.x - 20, self.y + 18, 40, 10))

        # Main Ball Circle
        pygame.draw.circle(screen, COLOR_BALL, (int(self.x), int(self.y)), self.radius)
        
        # Basketball Lines
        pygame.draw.circle(screen, (154, 52, 18), (int(self.x), int(self.y)), self.radius, width=2)
        pygame.draw.line(screen, (154, 52, 18), (int(self.x - self.radius), int(self.y)), (int(self.x + self.radius), int(self.y)), 2)
        pygame.draw.arc(screen, (154, 52, 18), (self.x - 15, self.y - 20, 30, 40), -1.2, 1.2, 2)


async def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mobile Basketball - Flick & Shoot")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 24, bold=True)
    score_font = pygame.font.SysFont("Arial", 48, bold=True)

    hoop = Hoop(SCREEN_WIDTH // 2, 180)
    ball = Basketball(SCREEN_WIDTH // 2, 580)

    score = 0
    high_score = 0
    swiping = False
    touch_start_pos = (0, 0)
    current_touch_pos = (0, 0)

    running = True
    while running:
        # --- Event Handling (Mouse & Touch Swipe) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Touch / Mouse Down (Start Swipe)
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                if not ball.is_thrown:
                    swiping = True
                    if event.type == pygame.FINGERDOWN:
                        touch_start_pos = (event.x * SCREEN_WIDTH, event.y * SCREEN_HEIGHT)
                    else:
                        touch_start_pos = event.pos
                    current_touch_pos = touch_start_pos

            # Touch / Mouse Drag
            elif event.type in (pygame.MOUSEMOTION, pygame.FINGERMOTION):
                if swiping:
                    if event.type == pygame.FINGERMOTION:
                        current_touch_pos = (event.x * SCREEN_WIDTH, event.y * SCREEN_HEIGHT)
                    else:
                        current_touch_pos = event.pos

            # Touch / Mouse Release (Execute Throw)
            elif event.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP):
                if swiping and not ball.is_thrown:
                    swiping = False
                    if event.type == pygame.FINGERUP:
                        end_pos = (event.x * SCREEN_WIDTH, event.y * SCREEN_HEIGHT)
                    else:
                        end_pos = event.pos

                    # Calculate swipe vector (from start to end)
                    dx = end_pos[0] - touch_start_pos[0]
                    dy = end_pos[1] - touch_start_pos[1]

                    # Only throw if swiped upward with minimum force
                    if dy < -20: 
                        ball.vx = dx * 0.12
                        ball.vy = dy * 0.14
                        # Cap max throw power
                        ball.vx = max(min(ball.vx, 15), -15)
                        ball.vy = max(min(ball.vy, -8), -22)
                        ball.is_thrown = True

        # --- Physics Update ---
        shot_reset = ball.update()
        if shot_reset and not ball.has_scored:
            score = 0 # Streak lost if shot misses completely

        # Rim Collision Logic
        if ball.is_thrown:
            for rim_x in (hoop.left_rim_x, hoop.right_rim_x):
                dist = math.hypot(ball.x - rim_x, ball.y - hoop.y)
                if dist < ball.radius + hoop.rim_radius:
                    # Elastic bounce off rim points
                    overlap = (ball.radius + hoop.rim_radius) - dist
                    nx = (ball.x - rim_x) / (dist or 1)
                    ny = (ball.y - hoop.y) / (dist or 1)
                    ball.x += nx * overlap
                    ball.y += ny * overlap
                    ball.vx = (ball.vx * 0.5) + (nx * 5)
                    ball.vy = (ball.vy * -0.5) + (ny * 5)

            # Score Checking (Ball passes through hoop traveling downward)
            if not ball.has_scored and ball.vy > 0:
                if (hoop.left_rim_x + 10 < ball.x < hoop.right_rim_x - 10) and (abs(ball.y - hoop.y) < 15):
                    ball.has_scored = True
                    score += 1
                    if score > high_score:
                        high_score = score

        # --- Drawing ---
        screen.fill(COLOR_BG)

        # Draw Court Floor / Key Line
        pygame.draw.rect(screen, COLOR_COURT, (0, 480, SCREEN_WIDTH, 220))
        pygame.draw.line(screen, (51, 65, 85), (0, 480), (SCREEN_WIDTH, 480), 3)

        # Draw Hoop Behind Ball
        hoop.draw(screen)

        # Draw Aim Trajectory Line during Swipe
        if swiping and not ball.is_thrown:
            pygame.draw.line(screen, (251, 146, 60), touch_start_pos, current_touch_pos, 3)
            pygame.draw.circle(screen, (251, 146, 60), (int(current_touch_pos[0]), int(current_touch_pos[1])), 6)

        # Draw Ball
        ball.draw(screen)

        # Score & UI Display
        score_surface = score_font.render(str(score), True, COLOR_TEXT)
        screen.blit(score_surface, (SCREEN_WIDTH // 2 - score_surface.get_width() // 2, 40))

        high_surface = font.render(f"BEST: {high_score}", True, (148, 163, 184))
        screen.blit(high_surface, (SCREEN_WIDTH - high_surface.get_width() - 20, 20))

        # Instructions Banner
        if not ball.is_thrown and score == 0:
            guide_text = font.render("SWIPE UP TO SHOOT", True, (100, 116, 139))
            screen.blit(guide_text, (SCREEN_WIDTH // 2 - guide_text.get_width() // 2, 520))

        pygame.display.flip()

        # Web / Pygbag Required Sleep
        await asyncio.sleep(0)
        clock.tick(60)

    pygame.quit()

# Run the async main loop
asyncio.run(main())