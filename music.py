import os
import glob
import time
import chess
import chess.svg
import chess.pgn
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from scamp import *
import scamp_extensions
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate chess music and video from PGN input.")
    parser.add_argument("--instrument", type=str, default="piano", help="Instrument to use for audio.")
    parser.add_argument("--p_time", type=float, default=0.4, help="Duration of each half-move.")
    parser.add_argument("--w_bishop", type=str, default="Eb4", help="Note for white bishop.")
    parser.add_argument("--w_rook", type=str, default="F4", help="Note for white rook.")
    parser.add_argument("--w_knight", type=str, default="G4", help="Note for white knight.")
    parser.add_argument("--w_queen", type=str, default="Ab4", help="Note for white queen.")
    parser.add_argument("--w_king", type=str, default="Bb4", help="Note for white king.")
    parser.add_argument("--w_pawn", type=str, default="C5", help="Note for white pawn.")
    parser.add_argument("--b_bishop", type=str, default="D5", help="Note for black bishop.")
    parser.add_argument("--b_rook", type=str, default="Eb5", help="Note for black rook.")
    parser.add_argument("--b_knight", type=str, default="F5", help="Note for black knight.")
    parser.add_argument("--b_queen", type=str, default="G5", help="Note for black queen.")
    parser.add_argument("--b_king", type=str, default="Ab5", help="Note for black king.")
    parser.add_argument("--b_pawn", type=str, default="Bb5", help="Note for black pawn.")
    parser.add_argument("--nocleanup", action="store_true", help="Do not delete intermediate files.")
    parser.add_argument("--nomargin", action="store_true", help="Do not add margin with coordinates.")
    args = parser.parse_args()
    playback_settings.recording_file_path = 'chess_music.wav'
    session = Session()
    try:
        instrument = session.new_part(args.instrument)
    except:
        print(f"Instrument {args.instrument} not found. Using piano instead.")
        instrument = session.new_part("piano")
    session.start_transcribing()
    p_time = args.p_time
    w_bishop = args.w_bishop
    w_rook = args.w_rook
    w_knight = args.w_knight
    w_queen = args.w_queen
    w_king = args.w_king
    w_pawn = args.w_pawn
    b_bishop = args.b_bishop
    b_rook = args.b_rook
    b_knight = args.b_knight
    b_queen = args.b_queen
    b_king = args.b_king
    b_pawn = args.b_pawn
    counter = 0
    m_counter = 0
    notes = []
    cleanup = []
    pgnraw = input("Enter PGN without header.: ")
    pgn = list(pgnraw.split())
    instrument.play_note(0, 0, p_time)
    def note_to_int(note_str):
        offsets = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
        name = note_str[0].upper()  
        octave = int(note_str[-1])      
        modifier = 0                    
        if "b" in note_str:
            modifier = -1
        elif "#" in note_str:
            modifier = 1
        midi_val = (octave + 1) * 12 + offsets[name] + modifier
    
        return midi_val
    for move in pgn:
        counter = 0
        if '.' in move:
            continue
        m_counter += 1
        if 'O-O-O' in move or 'O-O' in move or '0-0-0' in move or '0-0' in move:
            if m_counter % 2 == 1:
                notes.append(w_king)
            else:
                notes.append(b_king)
            continue           
        for i in move:
            if counter == 0:
                if i == 'B':
                    if m_counter % 2 == 1:
                        notes.append(w_bishop)
                    else:
                        notes.append(b_bishop)
                elif i == 'R':
                    if m_counter % 2 == 1:
                        notes.append(w_rook)
                    else:
                        notes.append(b_rook)
                elif i == 'N':
                    if m_counter % 2 == 1:
                        notes.append(w_knight)
                    else:
                        notes.append(b_knight)
                elif i == 'Q':
                    if m_counter % 2 == 1:
                        notes.append(w_queen)
                    else:
                        notes.append(b_queen)
                elif i == 'K':
                    if m_counter % 2 == 1:
                        notes.append(w_king)
                    else:
                        notes.append(b_king)
                else:
                    if m_counter % 2 == 1:
                        notes.append(w_pawn)
                    else:
                        notes.append(b_pawn)
            counter += 1
    for note in notes:
        instrument.play_note(note_to_int(note), 0.8, p_time)
    performance = session.stop_transcribing()
    c_counter = 1
    board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    previous_move = None
    print("Generating video frames...")
    for m in pgn:
        if (c_counter-1)%3 != 0 and c_counter != 1:
            filename = f"board_{c_counter}.svg"
            if c_counter!=1:
                if not args.nomargin:
                    board_svg = chess.svg.board(board, lastmove=previous_move, size=1000)
                else:
                    board_svg = chess.svg.board(board, lastmove=previous_move, size=1000, coordinates=False)
            else:
                if not args.nomargin:
                    board_svg = chess.svg.board(board, size=1000)
                else:
                    board_svg = chess.svg.board(board, size=1000, coordinates=False)
            previous_move = board.parse_san(m)
            board.push_san(m)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(board_svg)
                cleanup.append(filename)
            drawing = svg2rlg(filename)
            renderPM.drawToFile(drawing, f"board_{c_counter}.png", fmt="PNG")
            cleanup.append(f"board_{c_counter}.png")
        c_counter += 1
    if not args.nomargin:
        board_svg = chess.svg.board(board, lastmove=previous_move, size=1000)
    else:
        board_svg = chess.svg.board(board, lastmove=previous_move, size=1000, coordinates=False)
    filename = f"board_{c_counter}.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(board_svg)
        cleanup.append(filename)
    drawing = svg2rlg(filename)
    renderPM.drawToFile(drawing, f"board_{c_counter}.png", fmt="PNG")
    cleanup.append(f"board_{c_counter}.png")
    png_files = sorted(glob.glob("board_*.png"), key=os.path.getmtime)
    clips= []
    for png in png_files:
        clip = ImageClip(png).with_duration(p_time)
        clips.append(clip)
    video = concatenate_videoclips(clips, method="compose")
    video = video.with_audio(AudioFileClip("chess_music.wav"))
    video.write_videofile("chess_music_video.mp4", fps=24)
    session.kill()
    if not args.nocleanup:
        for file in cleanup:
            os.remove(file)
if __name__ == "__main__":
    main()
