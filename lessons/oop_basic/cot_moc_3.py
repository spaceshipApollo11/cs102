import enum
from typing import List, Tuple

import pygame
from pygame import Surface
from pygame.color import Color

WIDTH: int = 1280
HEIGHT: int = 768
WHITE: Color = Color(255, 255, 255)
FPS: int = 30  # Số cảnh mỗi giây (frame per second)

pygame.init()
screen: Surface = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()


# Hàm hỗ trợ
def scale_image(image: Surface, scale: float) -> Surface:
    """Resize image by a factor of input arg `scale`."""
    new_dimension: Tuple[int, int] = (
        int(image.get_width() * scale),
        int(image.get_height() * scale),
    )
    return pygame.transform.scale(image, new_dimension)


# Hình nền:
BACKGROUND_SPRITE: Surface = pygame.image.load("assets/background.png").convert_alpha()
BACKGROUND_SPRITE.set_alpha(128)
BACKGROUND_SPRITE = pygame.transform.scale(BACKGROUND_SPRITE, [WIDTH, HEIGHT])

# Game Entities Sprites
PLAYER_SPRITE: Surface = scale_image(pygame.image.load("assets/player.png"), 0.2)
ROBOT_SPRITE: Surface = scale_image(pygame.image.load("assets/robot.png"), 0.08)
DIAMOND_BLUE_SPRITE: Surface = scale_image(pygame.image.load("assets/diamond_blue.png"), 0.02)
DIAMOND_RED_SPRITE: Surface = scale_image(pygame.image.load("assets/diamond_red.png"), 0.02)
TO_MO_SPRITE: Surface = scale_image(pygame.image.load("assets/to_mo.png"), 0.2)


class Player:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.image: Surface = PLAYER_SPRITE

    def move(self, dx: int, dy: int):
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 < new_x < WIDTH - self.image.get_width():
            self.x = new_x
        if 0 < new_y < HEIGHT - self.image.get_height():
            self.y = new_y


class Robot:
    def __init__(self, x: float, y: float, x_heading: float, y_heading: float) -> None:
        self.x: float = x
        self.y: float = y
        self.image: Surface = ROBOT_SPRITE
        self.x_heading: float = x_heading
        self.y_heading: float = y_heading

    def move(self):
        self.x = self.x + self.x_heading
        self.y = self.y + self.y_heading

        if self.x > WIDTH - self.image.get_width():
            self.x_heading = -self.x_heading
        if self.x < 0:
            self.x_heading = -self.x_heading
        if self.y > HEIGHT - self.image.get_height():
            self.y_heading = -self.y_heading
        if self.y < 0:
            self.y_heading = -self.y_heading


class Princess:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.image: Surface = TO_MO_SPRITE


class ItemType(enum.Enum):
    DIAMOND_BLUE = 0
    DIAMOND_RED = 1


class GameItem:
    def __init__(self, x: float, y: float, type: ItemType) -> None:
        self.x: float = x
        self.y: float = y
        self.image: Surface

        if type == ItemType.DIAMOND_BLUE:
            self.image = DIAMOND_BLUE_SPRITE
        elif type == ItemType.DIAMOND_RED:
            self.image = DIAMOND_RED_SPRITE


# Game States:
player: Player = Player(350, 200)

list_robot: List[Robot] = [
    Robot(500, 500, 1, 1),
    Robot(50, 50, -2, 2),
    Robot(500, 50, 3, 5),
]

list_item: List[GameItem] = [
    GameItem(600, 500, ItemType.DIAMOND_BLUE),
    GameItem(800, 500, ItemType.DIAMOND_RED),
    GameItem(1000, 400, ItemType.DIAMOND_RED),
]

to_mo: Princess = Princess(1000, 50)

# Bắt đầu game
end_game: bool = False
running: bool = True
while running:
    # Tạo hình nền
    screen.fill(WHITE)

    screen.blit(BACKGROUND_SPRITE, (0, 0))

    # Người chơi có tắt màn hình game chưa
    if pygame.event.peek(pygame.QUIT):
        running = False

    # ----------------------------------------
    if not end_game:
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            player.move(0, -10)
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            player.move(0, 10)
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            player.move(-10, 0)
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            player.move(10, 0)

        for robot in list_robot:
            robot.move()

    # ----------------------------------------
    # Vẽ các vật phẩm game
    screen.blit(player.image, (player.x, player.y))

    for robot in list_robot:
        screen.blit(robot.image, (robot.x, robot.y))

    for item in list_item:
        screen.blit(item.image, (item.x, item.y))

    screen.blit(to_mo.image, (to_mo.x, to_mo.y))

    pygame.display.flip()
    clock.tick(FPS)

# Ket thuc game
pygame.quit()
