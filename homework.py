from dataclasses import dataclass, asdict
from typing import Type, Dict, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    INFORMATION_MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Получение сообщения о тренировке."""
        return self.INFORMATION_MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000.0
    MIN_IN_H = 60.0

    def __init__(
        self,
        action: float,
        duration: float,
        weight: float,
    ) -> None:
        """Создание экземпляра класса."""
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Выполните эту функцию для дочерних классов.'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18.0
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    LEN_STEP = 0.65

    def get_spent_calories(self) -> float:
        """Получить количество потраченных калорий."""
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER
             * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP = 0.65
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100.0

    def __init__(
        self,
        action: float,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        """Создание экземпляра класса."""
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить потраченные калории."""
        return (
            (self.CALORIES_WEIGHT_MULTIPLIER
             * self.weight
             + (((self.KMH_IN_MSEC
                  * self.get_mean_speed())**2)
                / self.height
                * self.CM_IN_M)
             * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
             * self.weight)
            * self.duration
            * self.MIN_IN_H
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SWIMMING_MEAN_SPEED_SHIFT = 1.1
    SWIMMING_MEAN_SPEED_MULTIPLIE = 2.0

    def __init__(
        self, action: float,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float
    ) -> None:
        """Создание экземпляра класса."""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        """Получить среднюю скорость."""
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self):
        """Получить количество потраченных калорий."""
        return (
            (self.get_mean_speed()
             + self.SWIMMING_MEAN_SPEED_SHIFT)
            * self.SWIMMING_MEAN_SPEED_MULTIPLIE
            * self.weight
            * self.duration
        )


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    TYPES_OF_ACTIVITY: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in TYPES_OF_ACTIVITY:
        acceptable_values = ", ".join(TYPES_OF_ACTIVITY)
        raise ValueError(
            'Ошибка при вводе типа тренировки. '
            f'<< {workout_type} >> нет в списке доступных тренировок. '
            'Доступны лишь значения: '
            f'{acceptable_values}.'
        )
    return TYPES_OF_ACTIVITY[workout_type](*data)


def main(training: Type[Training]) -> str:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
