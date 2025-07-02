import pygame
import sys

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)


# Rigid Body Class
class RigidBody:
    def __init__(self, x, y, size, mass):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.size = size
        self.mass = mass
        self.gravity = pygame.Vector2(0, 500)  # pixels per second^2

    def update(self, dt, domain_size=(300, 300)):
        # Apply gravity
        self.vel += self.gravity * dt
        self.pos += self.vel * dt

        # wall collision
        if self.pos.x + self.size > domain_size[0]:
            self.pos.x = domain_size[0] - self.size
            self.vel.x *= -0.7

        # Ground collision
        if self.pos.y + self.size > domain_size[1]:
            self.pos.y = domain_size[1] - self.size
            self.vel.y *= -0.7  # Simple bounce with energy loss

    def graph_update(self):
        self.pos += self.vel

    def draw(self, surface):
        self.rect = pygame.draw.circle(surface, RED, self.pos, self.size)


class World:
    def __init__(self) -> None:
        # Initialize Pygame
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Rigid Body Physics Engine")
        self.clock = pygame.time.Clock()

        # Create one rigid body
        self.body = RigidBody(400, 100, 30, 1)

    def run(self):
        # Game loop
        while True:
            dt = self.clock.tick(60) / 1000  # Delta time in seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.body.update(dt, (self.WIDTH, self.HEIGHT))

            self.screen.fill(WHITE)
            self.body.draw(self.screen)
            pygame.display.flip()


if __name__ == "__main__":

    World().run()
