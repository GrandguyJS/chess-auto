from flask import Flask, render_template, request, redirect, url_for, send_file

from converter import Board
from video import Video

import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("main.html")

@app.route("/board", methods = ["POST", "GET"])
def board():
    print(request.method)
    if request.method == "POST":
        global fen
        global board1
        
        fen = request.form["fen"]
        board1 = Board(fen)
        board = board1.create_board(None, False)
        board.save("./static/Boards/Board.png")
        return render_template("board.html", path=url_for('static', filename='Boards/Board.png'))
    else:
        return render_template("main.html")

@app.route("/move", methods = ["POST"])
def move():
    move = request.form["move"]
    board1.update_fen(move, False)

    board1.board_iter += 1
    board1.board.save(f"./static/Boards/Board{board1.board_iter}.png")
    print(board1.board_iter)
    return render_template("board.html", path=url_for('static', filename=f'Boards/Board{board1.board_iter}.png'))
    
@app.route("/video", methods = ["POST"])
def video():
    duration = request.form["duration"]
    video_id = uuid.uuid4()

    video = Video(image_folder = "./static/Boards/", output_name=video_id)
    video.create_video(duration)
    return send_file(f"../Output/{video_id}.mp4", as_attachment=True, download_name="chessvideo.mp4")

if __name__ == "__main__":
    app.run()