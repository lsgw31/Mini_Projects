from flask import Flask, render_template, request, jsonify
from puzzle_solver import Puzzle
from game_of_life import GameOfLife
from markupsafe import Markup

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve_puzzle", methods=['post'])
def get_puzzle_solution():
    puzzle = request.form['puzzle']
    return render_template("index.html", solution=Markup(Puzzle(puzzle).solve()))

game = None
@app.route("/create_GOL", methods=['post'])
def create_game():
    global game
    jsonData = request.get_json()
    density, size = float(jsonData['density']), int(jsonData['size'])
    game = GameOfLife(size,density)
    return {
            'response' : 'Created'
        }

@app.route("/next_state", methods=['get'])
def next_state():
    global game
    game.find_next_state()
    return jsonify('<code>' + '<br>'.join('&nbsp;'.join(('&nbsp;&nbsp;', '██')[j] for j in i) for i in game.m) + '</code>')
