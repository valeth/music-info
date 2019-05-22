#!/usr/bin/env python3

import argparse
from pathlib import Path

from PIL import Image
from gi.repository import GLib
from sources import MPRISPlayer


def change_cover_image(player, path):
    if not player.is_playing:
        return

    cover_file = path / "cover.png"

    outfile = path / ".cover.png"
    cover = Image.open(player.cover_art)
    out = cover.resize((500, 500))
    out.save(outfile)
    outfile.rename(cover_file)

def write_info_text(player, path):
    if not player.is_playing:
        return

    outfile = path / "music_info.txt"
    text = "    :::    "
    if player.album:
        text += f"{player.album} / "
    if player.artist:
        if type(player.artist) == list:
            artist = ", ".join(player.artist)
        else:
            artist = player.artist
        text += f"{artist} - "
    text += player.title

    with outfile.open(mode="w") as f:
        f.write(text)

def music_info(info_path, player_name):
    info_path.mkdir(parents=True, exist_ok=True)
    player = MPRISPlayer.get_player(player_name)

    if player:
        player.on_update(change_cover_image, info_path)
        player.on_update(write_info_text, info_path)
        player.update()
        GLib.MainLoop().run()
    else:
        print(f"Could not find {player_name}")

def _main():
    parser = argparse.ArgumentParser("Output cover and song information")
    parser.add_argument("--path", type=Path, help="The path where the files should be stored")
    parser.add_argument("--player", type=str, default="cantata", help="The player to use for playback information")
    args = parser.parse_args()
    music_info(args.path, args.player)


if __name__ == "__main__":
    _main()
