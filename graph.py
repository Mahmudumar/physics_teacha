import pygame
import sys
from rigid_physics_ball import RigidBody

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class point:
    def __init__(self, point) -> None:
        self.pos = point

    def draw(self, surf):
        pygame.draw.circle(surf, RED, self.pos, 4)


class Graph:
    def __init__(self, world) -> None:
        self.px_per_unit = 50
        self.world = world  # surface of the window
        self.height = self.world.get_height()
        self.width = self.world.get_width()

        self.center_x_axis = (self.width//2)
        self.center_y_axis = (self.height//2)

        self.origin = self.center_x_axis, self.center_y_axis

        # default lines
        self.def_lines = {
            # x axis
            "x": ((0, self.center_y_axis), (self.width, self.center_y_axis)),
            # y axis
            "y": ((self.center_x_axis, 0), (self.center_x_axis, self.height)),
        }
        self.show_grid()

    def show_grid(self):
        """generate numbers"""

        font = pygame.font.Font(None, size=15)

        # x axis
        for num in range(-7, 8):
            t = font.render(f"{num}", True, (0, 0, 0))
            x_pos = self.grid_pos((num, 0))
            self.world.blit(t, x_pos)

        # positive y axis
        for num in range(-5, 0):
            t = font.render(f"{-num}", True, (0, 0, 0))
            plus_y_pos = self.grid_pos((0, num))
            self.world.blit(t, plus_y_pos)

        # negative y axis
        for num in range(1, 6):
            t = font.render(f"{-num}", True, (0, 0, 0))
            plus_y_pos = self.grid_pos((0, num))
            self.world.blit(t, plus_y_pos)

    def grid_pos(self, pos):
        """place a position `pos` relative to
         your custom origin and 
        it will tell pygame where to put it"""
        self.pos_x = ((pos[0] * self.px_per_unit)+self.origin[0])
        self.pos_y = ((pos[1] * self.px_per_unit)+self.origin[1])

        # translate
        return [self.pos_x, self.pos_y]

    def grid_scale(self, by):
        """Scale an object relative to your 
        defined world coordinate

        it will tell pygame how exactly to scale"""
        return by*self.px_per_unit

    def draw(self):
        x_line = self.def_lines['x']
        y_line = self.def_lines['y']
        pygame.draw.line(self.world, (255, 0, 0), x_line[0], x_line[1], 1)
        pygame.draw.line(self.world, (0, 255, 0), y_line[0], y_line[1], 1)


class World:
    def __init__(self) -> None:
        # Initialize Pygame
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Rigid Body Physics Engine")
        self.clock = pygame.time.Clock()

        self.graph = Graph(self.screen)

        # set initial postion & scale
        box_pos = self.graph.grid_pos([0, 0])
        self.box = point(box_pos)

    def run(self):
        # Game loop
        by_x = 0
        by_y = 0
        while True:
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        by_y -= 1
                    if event.key == pygame.K_DOWN:
                        by_y += 1
                    if event.key == pygame.K_RIGHT:
                        by_x += 1
                    if event.key == pygame.K_LEFT:
                        by_x -= 1

            self.box.pos = self.graph.grid_pos([by_x, by_y])
            # self.box.graph_update()

            self.graph.draw()
            self.box.draw(self.screen)
            self.graph.show_grid()

            dt = self.clock.tick(60) / 1000  # Delta time in seconds
            pygame.display.flip()


World().run()
