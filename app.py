from flask import Flask, render_template, request, jsonify
import threading
import time

app = Flask(__name__)

# Initialize the game board
board = [['blue' if (i + j) % 2 == 0 else 'red' for j in range(10)] for i in range(10)]
lock = threading.Lock()
game_running = False

@app.route('/')
def index():
    return render_template('index.html', board=board)

@app.route('/click', methods=['POST'])
def click():
    global board
    data = request.json
    row = data['row']
    col = data['col']
    with lock:
        board[row][col] = 'red' if board[row][col] == 'blue' else 'blue'
    return jsonify(success=True)

@app.route('/start_game', methods=['POST'])
def start_game():
    global game_running
    game_running = True
    threading.Thread(target=game_timer).start()
    return jsonify(success=True)

def game_timer():
    global game_running
    time.sleep(60)
    game_running = False
    red_count = sum(row.count('red') for row in board)
    blue_count = sum(row.count('blue') for row in board)
    winner = 'red' if red_count > blue_count else 'blue'
    print(f"Game over! Red: {red_count}, Blue: {blue_count}. Winner: {winner}")

if __name__ == '__main__':
    app.run(debug=True)
