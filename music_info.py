#!/usr/bin/env python3

import argparse
from pathlib import Path

from PIL import Image
from gi.repository import GLib
from sources import MPRISPlayer


def change_cover_image(player, path):
    outfile = path / "cover.png"
    cover = Image.open(player.cover_art)
    out = cover.resize((500, 500))
    out.save(outfile)

def write_info_text(player, path):
    outfile = path / "music_info.txt"
    text = "    :::    "
    if player.album:
        text += f"{player.album} / "
    artist = ", ".join(player.artist)
    text += f"{artist} - {player.title}"

    with outfile.open(mode="w") as f:
        f.write(text)

def main(args):
    path = args.path

    path.mkdir(parents=True, exist_ok=True)

    player = MPRISPlayer.get_player("cantata")
    if player:
        player.on_update(change_cover_image, path)
        player.on_update(write_info_text, path)
        player.update()
        GLib.MainLoop().run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Output cover and song information")
    parser.add_argument("--path", type=Path, help="The path where the files should be stored")
    args = parser.parse_args()
    main(args)
