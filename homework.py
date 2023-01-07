class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
        """Функция для объявления класса."""

    def get_message(self) -> str:
        """Вывод сообщения на экран."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # Расстояние в одно действие.
    M_IN_KM: int = 1000     # Количество метров в км.
    MIN_IN_H: int = 60      # Количество минут в часе.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        """Функция для объявления родительского класса."""
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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    LEN_STEP: float = 0.65

    def __init__(self, action: int, duration: float, weight: float) -> None:
        """Объявление дочернего класса."""
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество потраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = 0.65
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        """Объявление дочернего класса."""
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить потраченные калории."""
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                 + (((self.KMH_IN_MSEC * self.get_mean_speed())**2)
                    / self.height * self.CM_IN_M)
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight) * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWIM_CONST_FIRST: float = 1.1
    SWIM_CONST_SECOND: float = 2.0

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: int,
                 count_pool: int) -> None:
        """Объявление дочернего класса."""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        """Получить среднюю скорость."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        """Получить количество потраченных калорий."""
        return ((self.get_mean_speed() + self.SWIM_CONST_FIRST)
                * self.SWIM_CONST_SECOND * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    TYPES_OF_ACTIVITY: dict = {'SWM': Swimming,
                               'RUN': Running,
                               'WLK': SportsWalking}
    training: Training = TYPES_OF_ACTIVITY[workout_type](*data)
    return training


def main(training: Training) -> str:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(str(info.get_message()))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
