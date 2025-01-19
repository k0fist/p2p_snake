from random import randint

import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 10
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


class GameObject:
    """Базовый класс для объектов игры."""

    def __init__(self):
        """
        Инициализируем позицию в центре экрана 320 на 240
        и задаем цвет None.
        """
        initial_x = (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE
        initial_y = (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
        self.position = (initial_x, initial_y)
        self.body_color = None

    def draw(self):
        """Абстрактный метод отрисовки"""
        pass


class Apple(GameObject):
    """Класс объекта яблока."""

    body_color = APPLE_COLOR
    position: tuple

    def __init__(self):
        super().__init__()
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Задается рандомная позиция от 0 до n-1 ячейки"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, screen):
        """Отрисовывается яблочко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс объекта змеи"""

    def __init__(self):
        """Инициализируется злейка"""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.positions = [self.position]

    def update_direction(self):
        """Обновление направления змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейки (добавление головы)."""
        current_head = self.positions[0]
        delta_x, delta_y = self.direction
        new_head_x = current_head[0] + delta_x * GRID_SIZE
        new_head_y = current_head[1] + delta_y * GRID_SIZE

        if new_head_x < 0:
            new_head_x = SCREEN_WIDTH - GRID_SIZE
        elif new_head_x >= SCREEN_WIDTH:
            new_head_x = 0

        if new_head_y < 0:
            new_head_y = SCREEN_HEIGHT - GRID_SIZE
        elif new_head_y >= SCREEN_HEIGHT:
            new_head_y = 0

        new_head = (new_head_x, new_head_y)

        if new_head in self.positions:
            self.reset()

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, screen):
        """Отрисовывание змеи"""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Вернуть поцизию головы змеи"""
        return self.positions[0]

    def reset(self):
        """Вернуть змею в начальную позицию при проигрыше"""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """Считывание действий игрока."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция запуска игры"""
    pygame.init()
    apple = Apple()
    snake = Snake()

    pygame.display.set_caption('Змейка')

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
