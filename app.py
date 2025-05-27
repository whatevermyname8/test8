from flask import Flask, render_template, jsonify, request
import random
import threading

app = Flask(__name__)

# Initialize the game board with random colors
board = [[random.choice(['red', 'blue']) for _ in range(10)] for _ in range(10)]
team_scores = {'red': 0, 'blue': 0}
game_over = False

@app.route('/')
def index():
return render_template('index.html',board=board)

@app.route('/click', methods=['POST'])
def click():
global board, team_scores
if game_over:
return jsonify({'status':'game_over'})      

data = request.json
row = data['row']
col = data['col']
team = data['team']

# Toggle the color of the clicked box
board[row][col] = 'blue' if board[row][col] == 'red' else 'red'

# Update team scores
team_scores['red'] = sum(row.count('red') for row in board)
team_scores['blue'] = sum(row.count('blue') for row in board)

return jsonify({'board': board, 'team_scores': team_scores})

def end_game():
global game_over
game_over = True

# Start the timer when the app runs
if __name__ == '__main__':]
threading.Timer(60.0, end_game).start()
app.run(debug=True)
