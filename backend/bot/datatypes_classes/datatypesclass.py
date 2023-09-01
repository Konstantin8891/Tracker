"""
    Классы, определяющие Наблюдателя и Подписчика,
    а также интерфейс для их взаимодействия.
"""

from abc import ABC, abstractmethod

from bot.classes.bot import Bot
from bot.classes.tguser import TgUser


class Subject(ABC):
    """ Интферфейс издателя объявляет набор методов
    для управлениями подписчиками."""

    @abstractmethod
    def attach(self, observer: 'Observer') -> None:
        """Присоединяет наблюдателя к издателю."""

    @abstractmethod
    def clean(self, observer: 'Observer') -> None:
        """Очищает список наблюдателей издателя."""

    @abstractmethod
    def notify(self) -> None:
        """Уведомляет всех наблюдателей о событии."""


class Observer(ABC):
    """Интерфейс Наблюдателя объявляет метод уведомления, который издатели
    используют для оповещения своих подписчиков."""

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """Получить обновление от субъекта."""


class Road(Subject):
    """Издатель владеет некоторым важным состоянием и оповещает наблюдателей
    о его изменениях."""

    state: str | None = None
    """Для удобства в этой переменной хранится состояние Издателя, необходимое
    всем подписчикам."""

    _observers: list[Observer] = []
    """Список подписчиков."""

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def clean(self, observer: Observer) -> None:
        self._observers.clear()

    def notify(self, tgbot: Bot, tguser: TgUser, **kwargs) -> None:
        """Запуск обновления в каждом подписчике."""
        for observer in self._observers:
            observer.update(self, tgbot, tguser, **kwargs)

        self.clean(observer)

    def go(self, state: str, tgbot: Bot, tguser: TgUser, **kwargs) -> None:
        """Получаем состояние state и запускаем оповещение всех
        прикреплённых на данный момент подписчиков."""
        self.state = state
        self.notify(tgbot, tguser, **kwargs)
