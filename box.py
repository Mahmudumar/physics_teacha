import pygame
import sys
import math
import random

WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 100, 0)


class RigidBox1:
    def __init__(self, x, y, size, mass):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0
        self.angular_velocity = 0
        self.size = size
        self.mass = mass
        self.inertia = (1/6) * mass * size ** 2  # moment of inertia for square
        self.gravity = pygame.Vector2(0, 500)

    def update(self, dt, domain_size):
        # Linear motion
        self.vel += self.gravity * dt
        self.pos += self.vel * dt

        # Angular motion (just spinning for now)
        self.angular_velocity += 0  # no torque yet
        self.angle += self.angular_velocity * dt

        # Ground collision (very simple bounce and stop rotation)
        if self.pos.y + self.size / 2 > domain_size[1]:
            self.pos.y = domain_size[1] - self.size / 2
            self.vel.y *= -0.6
            self.angular_velocity *= 0.7

    def draw(self, surface):
        half = self.size / 2
        corners = [
            pygame.Vector2(-half, -half),
            pygame.Vector2(half, -half),
            pygame.Vector2(half, half),
            pygame.Vector2(-half, half),
        ]

        # Rotate and translate corners
        rotated = []
        for corner in corners:
            rotated_corner = corner.rotate_rad(self.angle)
            rotated.append(self.pos + rotated_corner)

        pygame.draw.polygon(surface, BLUE, rotated)


class RigidBox:
    def __init__(self, x, y, size, mass, color, is_static=False):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0
        self.angular_velocity = 0
        self.size = size
        self.mass = mass
        self.color = color
        self.is_static = is_static
        self.gravity = pygame.Vector2(0, 500 if not is_static else 0)
        
        self.on_ground = False
        self.friction = .3

    def update(self, dt, domain_size=(300, 300)):
        if not self.is_static:
            # Linear motion
            self.vel += self.gravity * dt
            self.pos += self.vel * dt

            # Angular motion
            self.angle += self.angular_velocity * dt

            # wall collision
            if self.pos.x + self.size > domain_size[0]:
                self.pos.x = domain_size[0] - self.size
                

                if self.on_ground:
                    self.vel.x *= -self.friction
                else:
                    self.vel.x *= -0.7

            if self.pos.x + self.size <= 0-self.size:
                self.pos.x = 0 - self.size

                if self.on_ground:
                    self.vel.x *= -self.friction
                else:
                    self.vel.x *= -0.7
                

            # Simple ground collision
            if self.pos.y + self.size / 2 > domain_size[1]:
                self.pos.y = domain_size[1] - self.size / 2
                self.vel.y *= -.7
                self.angular_velocity *= 0.7
                self.on_ground = True
            else:
                self.on_ground=False



    def get_corners(self):
        half = self.size / 2
        local = [
            pygame.Vector2(-half, -half),
            pygame.Vector2(half, -half),
            pygame.Vector2(half, half),
            pygame.Vector2(-half, half),
        ]
        return [self.pos + corner.rotate_rad(self.angle) for corner in local]

    def draw(self, surface):
        corners = self.get_corners()
        pygame.draw.polygon(surface, self.color, corners)


class World:
    def __init__(self) -> None:
        # Initialize Pygame
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen_size = (self.WIDTH, self.HEIGHT)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Rigid Body Physics Engine")
        self.clock = pygame.time.Clock()

        # Create one rigid body
        particle_amount = 200
        self.particles = [RigidBox(random.random()*xpos,
                                   random.random()*550, random.random()*20, 1,
                                   (random.random()*254,
                                    random.random()*254,
                                    random.random()*254))
                          for xpos in range(20, particle_amount)]
        
        for p in self.particles:
            p.vel = pygame.Vector2(-200, -200)
            p.gravity = pygame.Vector2(0,500)
            # p.angular_velocity = math.radians(random.random()*100)

        self.body = RigidBox(400, 100, 20, 1, RED)
        # self.body.vel = pygame.Vector2(100, -200)         # move right and up
        # self.body.angular_velocity = math.radians(
        #     90)     # spin 90 degrees per second

    def run(self):
        # Game loop
        while True:
            dt = self.clock.tick(60) / 1000  # Delta time in seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # self.body.update(dt, self.screen_size)

            for boxes in self.particles:
                boxes.update(dt, self.screen_size)

            self.screen.fill(WHITE)
            self.body.draw(self.screen)

            for boxes in self.particles:
                boxes.draw(self.screen)
            pygame.display.flip()

if __name__ == "__main__":

    World().run()