from pathlib import Path
import pydbus as dbus

from .player import Player, PlaybackStatus


class MPRISPlayer(Player):
    BUS_NAME_PREFIX = "org.mpris.MediaPlayer2"
    BUS_OBJECT_PATH = "/org/mpris/MediaPlayer2"

    def __init__(self, bus_name):
        self._bus_name = bus_name
        self._bus = dbus.SessionBus()
        self._dbus_interface.onPropertiesChanged = self._updated
        self._callbacks = []


    @property
    def title(self):
        return self._metadata["title"]

    @property
    def artist(self):
        return self._metadata["artist"]

    @property
    def album(self):
        return self._metadata["album"]

    @property
    def track_number(self):
        return self._metadata["track_number"]

    @property
    def cover_art(self):
        cover = self._metadata["cover_art"]
        if cover:
            try:
                return Path(cover.rpartition(":")[-1])
            except TypeError:
                pass
        return Path("./res/default_cover.jpg").absolute()

    @property
    def name(self):
        return self._dbus_interface.Identity

    @property
    def status(self):
        s = self._dbus_interface.PlaybackStatus
        return PlaybackStatus[s.upper()]

    @property
    def song_changed(self):
        return self._metadata != self._current_track_metadata

    def update(self):
        self._metadata = self._current_track_metadata
        self._run_callbacks()

    def on_update(self, callback, *args):
        self._callbacks.append((callback, args))


    @classmethod
    def get_players(cls):
        bus = dbus.SessionBus()
        proxy = bus.get("org.freedesktop.DBus", "/org/freedesktop/DBus")
        return dict([[p.split(".")[-1], cls(p)] for p in proxy.ListNames() if p.startswith(cls.BUS_NAME_PREFIX)])

    @classmethod
    def get_player(cls, name=None):
        return cls.get_players().get(name)


    @property
    def _dbus_interface(self):
        return self._bus.get(self._bus_name, self.BUS_OBJECT_PATH)

    @property
    def _current_track_metadata(self):
        raw_metadata = self._dbus_interface.Metadata
        return {
            "title": raw_metadata.get("xesam:title"),
            "artist": raw_metadata.get("xesam:artist"),
            "album": raw_metadata.get("xesam:album"),
            "cover_art": raw_metadata.get("mpris:artUrl"),
            "track_number": raw_metadata.get("xesam:trackNumber"),
        }

    def _run_callbacks(self):
        for (callback, args) in self._callbacks:
            callback(self, *args)

    def _updated(self, *_args):
        if self.song_changed:
            self.update()

