from random import choice, randint

import pygame
from typing import List, Optional, Tuple


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.

class GameObject():

    def __init__(self, position: Optional[Tuple[int, int]] = None,
                 body_color: Optional[Tuple[int, int, int]] = None) -> None:
        """инициализирует базовые атрибуты объекта, такие как его позиция и цвет."""

        self.position = position or ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color
    def draw(self) -> None:
        """это абстрактный метод, который предназначен для переопределения в дочерних классах.
        Этот метод должен определять, как объект будет отрисовываться на экране."""

        pass
class Apple(GameObject):

    def __init__(self) -> None:
        """задаёт цвет яблока и вызывает метод randomize_position,
        чтобы установить начальную позицию яблока."""

        super().__init__(None, APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self) -> None:
        """устанавливает случайное положение яблока на игровом поле — задаёт атрибуту
        position новое значение. Координаты выбираются так,
        чтобы яблоко оказалось в пределах игрового поля."""

        self.position = ( randint(0, GRID_WIDTH - 1) * GRID_SIZE , randint(0, GRID_HEIGHT - 1 ) * GRID_SIZE )

    def draw(self) -> None:
        """ отрисовывает яблоко на игровой поверхности"""

        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    def __init__(self) -> None:
        """инициализирует начальное состояние змейки."""
        super().__init__((GRID_WIDTH // 2 * GRID_SIZE,
                          GRID_HEIGHT // 2 * GRID_SIZE), SNAKE_COLOR)
        self.length = 1
        self.positions: List[Tuple[int, int]] = [self.position]
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Tuple[int, int] = None
        self.last = None
    def update_direction(self) -> None:
        """ обновляет направление движения змейки """
        if self.next_direction:
             self.direction = self.next_direction
             self.next_direction = None
    def move(self) -> None:

        """обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и удаляя последний элемент,
        если длина змейки не увеличилась"""

        position = self.get_head_position()
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        x, y = self.direction
        new_pos = ((position[0] + (x * GRID_SIZE)) % SCREEN_WIDTH, (position[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        self.positions.insert(0, new_pos)
        if len(self.positions) > self.length:
            self.positions.pop()


    def draw(self) -> None:
        """отрисовывает змейку на экране, затирая след"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> Tuple[int, int]:
        """возвращает позицию головы змейки (первый элемент в списке positions)."""

        return self.positions[0]
    def reset(self) -> None:
        """сбрасывает змейку в начальное состояние после столкновения с собой."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
def handle_keys(game_object) -> None:
    """обрабатывает нажатия клавиш, чтобы изменить направление движения змейки"""

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
def main() -> None:
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length+=1
            apple.randomize_position()
        if len(snake.positions) > 2 and \
           snake.get_head_position() in snake.positions[2:]:
            snake.reset()  # Сбрасываем игру после столкновения с собой


        # Отрисовываем элементы на экране
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        # Обновляем экран
        pygame.display.update()



if __name__ == '__main__':
    main()



