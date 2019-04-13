from enum import Enum, unique
from pathlib import Path
from abc import ABC, abstractmethod


@unique
class PlaybackStatus(Enum):
    PLAYING = 1
    PAUSED = 2
    STOPPED = 3
    UNKNOWN = 4


class Player(ABC):
    @property
    @abstractmethod
    def title(self):
        pass

    @property
    @abstractmethod
    def artist(self):
        pass

    @property
    @abstractmethod
    def album(self):
        pass

    @property
    @abstractmethod
    def track_number(self):
        pass

    @property
    def cover_art(self):
        return Path("./res/default_cover.jpg").absolute()

    @property
    def status(self):
        return PlaybackStatus.UNKNOWN

    @property
    @abstractmethod
    def on_update(self, callback, *args):
        pass

