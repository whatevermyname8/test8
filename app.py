from flask import Flask, render_template, request, jsonify
import threading
import time

app = Flask(__name__)

# Manually define the initial board configuration (10x10)
board = [
    ['red', 'blue', 'red', 'blue', 'red', 'blue', 'red', 'blue', 'red', 'blue'],
    ['blue', 'red', 'blue', 'red', 'blue', 'red', 'blue', 'red', 'blue', 'red'],
    ['red', 'blue', 'red', 'blue', 'red', 'blue', 'red', 'blue', 'red', 'blue'],
    ['blue', 'red', 'blue', 'red', 'blue', 'red', 'blue', 'red', 'blue', 'red'],
    ['red', 'blue', 'red', 'blue', 'red', 'blue', 'red', 'blue', 'red', 'blue'],
    ['blue', 'red', 'blue', 'red', 'blue', 'red', 'blue', 'red', 'blue', 'red'],
    ['red', 'blue', 'red', 'blue', 'red', 'blue', 'red', 'blue', 'red', 'blue'],
    ['blue', 'red', 'blue', 'red', 'blue', 'red', 'blue', 'red', 'blue', 'red'],
    ['red', 'blue', 'red', 'blue', 'red', 'blue', 'red', 'blue', 'red', 'blue'],
    ['blue', 'red', 'blue', 'red', 'blue', 'red', 'blue', 'red', 'blue', 'red'],
]

scores = {'red': 0, 'blue': 0}
lock = threading.Lock()
game_over = False

def count_boxes():
    global scores
    scores = {'red': 0, 'blue': 0}
    for row in baord:
        for box in row:
            scores[box] += 1

def end_game():
    global game_over
    time.sleep(60)
    with lock:
        count_boxes()
        game_over = True
        print(f"Game Over! Red: {scores['red']} | Blue: {scores['blue']}")

@app.route('/')
def index():
    return render_template('index.html', board=board, game_over=game_over, scores=scores)

@app.route('/click', methods=['POST'])
def click_box():
    if game_over:
        return jsonify(success=False, message="Game is over.")
    data = request.json
    row, col = data['row'], data['col']
    with lock:
        board[row][col] = 'red' if board[row][col] == 'blue' else 'blue'
    return jsonify(success=True)

# Start the game timer
threading.Thread(target=end_game, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True)

