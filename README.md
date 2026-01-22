# Chess videos with music
Sharing your favorite chess games with your friends or on social media? Why not share it in a video format where the music is generated from the game as well! This repository contains a python script which creates a video and unique music based on the game from the game moves.
# How does it work?
The script takes the game's PGN (important that you enter it without headers, only the moves themselves) you enter as input and then generates music. Each piece (white and black pieces are different) is assigned a musical note. When that piece moves the note assigned is played. All the notes can be customized (see **Arguments**). Then, the Board states are generated in SVG thanks to python-chess and converted into PNG. Finally all the parts are joined into an MP4 file with moviepy.
# Requirements
Run this pip command to install required python libraries:
`pip install python-chess svglib reportlab moviepy scamp scamp_extensions clockblocks python-rtmidi numpy decorator proglog`
Most likely you will also need to install [GTK Runtime](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/tag/2022-01-04) and [Scarb](https://docs.swmansion.com/scarb/download.html#windows).
# Arguments
| Argument | Description | Default value |
| :--- | :--- | :--- |
| `--instrument` | Instrument to use for audio. | `piano` |
| `--p_time` | Duration of each half-move shown on screen. | `0.4` |
| `--w_bishop` | Note for white bishop. | `Eb4` |
| `--w_rook` | Note for white rook. | `F4` |
| `--w_knight` | Note for white knight. | `G4` |
| `--w_queen` | Note for white queen. | `Ab4` |
| `--w_king` | Note for white king. | `Bb4` |
| `--w_pawn` | Note for white pawn. | `C5` |
| `--b_bishop` | Note for black bishop. | `D5` |
| `--b_rook` | Note for black rook. | `Eb5` |
| `--b_knight` | Note for black knight. | `F5` |
| `--b_queen` | Note for black queen. | `G5` |
| `--b_king` | Note for black king. | `Ab5` |
| `--b_pawn` | Note for black pawn. | `Bb5` |
| `--nocleanup` | Do not delete intermediate files. | `False` |

