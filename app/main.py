from flask import Flask, render_template, url_for, redirect, session, flash, jsonify
from flask import request

from SudokuModel import SudokuModel
from utils import string_to_grid

from waitress import serve

app = Flask(__name__)
app.secret_key = "super secret key"

# stores the model generated
data = {}

# difficulty mapping
difficulties = {1: "easy", 2: "medium", 3: "hard"}

# supported themes
index_themes = {"grey": 'index.html', "donda": 'donda_index.html'}
play_themes = {"grey": 'playGame.html', "donda": 'donda_playGame.html'}


# the home page
@app.route("/")
@app.route("/<chosen_theme>")
def index(chosen_theme=None):
    if 'theme' not in session:
        session['theme'] = 'grey'

    if chosen_theme is not None and chosen_theme in index_themes and 'theme' in session:
        session['theme'] = chosen_theme

    return render_template(index_themes.get(session['theme'], 'index.html'))


# creates a random board according to difficulty submitted by gen form
@app.route("/makeBoard", methods=['POST', 'GET'])
def make_board():
    if request.method == 'POST':
        diff = request.form.get('difficulty')
        data['model'] = SudokuModel(difficulty=diff)
        return redirect(url_for('play_game'))

    elif request.method == 'GET':
        data['model'] = SudokuModel()
        return redirect(url_for('play_game'))

    return redirect(url_for('index'))


@app.route("/togglingIncorrect")
def toggle_incorrect():
    if "toggled" not in session:
        session["toggled"] = True
    else:
        session["toggled"] = not session["toggled"]
    return redirect(url_for('play_game'))


# resets board to original
@app.route("/resetBoard")
def reset():
    model = data.get('model', None)
    if model is None:
        return redirect(url_for('index'))
    else:
        model.reset()
        return redirect(url_for('play_game'))


# resets board to solved state
@app.route("/solveBoard")
def solve():
    model = data.get('model', None)
    if model is None:
        return redirect(url_for('index'))
    else:
        model.solve()
        return redirect(url_for('play_game'))


@app.route("/uploadBoard", methods=['POST'])
def upload_board():
    if request.method == 'POST':
        input_board = string_to_grid(request.form.get('input_board'))
        if len(input_board) == 0:
            flash("Invalid board input, try again")
            return redirect(url_for('index'))
        else:
            try:
                data['model'] = SudokuModel(input_board)
                return redirect(url_for('play_game'))
            except TypeError:
                flash("Invalid board input, try again")
                return redirect(url_for('index'))


#
# main page for game play
@app.route("/play_game<row><col>", methods=['GET', 'POST'])
@app.route("/play_game")
def play_game(row=-1, col=-1):
    model = data.get('model', None)

    if model is None:
        return redirect(url_for('index'))
    # initial call from index page
    if row == -1 or col == -1:
        return render_template(play_themes.get(session['theme'], "playGame.html"), board=model.get_board(),
                               original=model.original,
                               flag=False,
                               model=model, incorrects=model.get_incorrect())
    else:
        row_num = int(row)
        col_num = int(col)

        # for when selecting a cell
        if request.method == 'GET':
            return render_template(play_themes.get(session['theme'], "playGame.html"), flag=True, row=row_num,
                                   col=col_num,
                                   board=model.get_board(),
                                   original=model.original, testPage=True, incorrects=model.get_incorrect())
        # for when filling a cell
        elif request.method == 'POST':
            new_val = int(request.form.get('val'))
            model.fill(row_num, col_num, new_val)
            return redirect(url_for('play_game'))


@app.route("/ajax_playGame", methods=['POST', 'GET'])
def ajax_playGame():
    model = data.get('model', None)

    if model is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        value = int(request.form.get('lol', "HOLÁ"))
        row = int(request.form.get('row'))
        col = int(request.form.get('col'))
        model.fill(row, col, value)

        return render_template('board.html', flag=False, board=model.get_board(), original=model.original,
                               incorrects=model.get_incorrect())

    loc = request.args.get('jsdata')

    row = int(loc[1])
    col = int(loc[4])

    return render_template("board.html", row=row, col=col, flag=True, board=model.get_board(),
                           original=model.original,
                           incorrects=model.get_incorrect())


@app.route("/escape")
def escape():
    model = data.get('model', None)

    if model is None:
        return redirect(url_for('index'))
    return render_template("board.html", flag=True, board=model.get_board(),
                           original=model.original,
                           incorrects=model.get_incorrect())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
    # serve(app, host="0.0.0.0", port=80)
