from flask import Flask, render_template, request, redirect, Response
import mysql.connector
import config
import json

app = Flask(__name__)
try:
    conn = mysql.connector.connect(database=config.database, user=config.user, host="127.0.0.1",password=config.password)
except:
    print("MySQL login failed:Update your config.py file")
    exit()
cursor = conn.cursor(buffered=True)

def expected(Rb, Ra):
	return 1/(1 + pow(10, (Rb-Ra)/400))

def win(score, expected, k = 24):
	return score + k * (1-expected)

def loss(score, expected, k = 24):
	return score + k * (0-expected)
	
def rate(x,y):
	query="SELECT * FROM images WHERE image_id = {};".format(x)
	cursor.execute(query)
	winner = cursor.fetchone()
	query="SELECT * FROM images WHERE image_id = {};".format(y)
	cursor.execute(query)
	loser= cursor.fetchone()
	#Update scores
	winner_expected = expected(loser[2], winner[2])
	winner_score = win(winner[2], winner_expected)
	query="UPDATE images SET score = {}, wins = wins+1 WHERE image_id = {};".format(winner_score, x)
	cursor.execute(query)
	loser_expected = expected(winner[2], loser[2])
	loser_score = loss(loser[2], loser_expected)
	query="UPDATE images SET score = {}, losses = losses+1 WHERE image_id = {};".format(loser_score, y)
	cursor.execute(query)
	query="INSERT INTO battles SET winner = {}, loser = {};".format(x,y)
	cursor.execute(query)
	cursor.execute(("commit;"))
	return

@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
	if request.method == "POST":
		a = request.form['send_button']
		a = a.split(";")
		rate(a[0],a[1])
		query="SELECT image_id, filename FROM images where image_id != " + str(a[-2]) + " ORDER BY RAND() LIMIT 1"
		cursor.execute(query)
		row = cursor.fetchall()
		query="SELECT image_id, filename FROM images where image_id = " + str(a[-2])
		cursor.execute(query)
		row += cursor.fetchall()
	else:
		query="SELECT image_id, filename FROM images ORDER BY RAND() LIMIT 2"
		cursor.execute(query)
		row = cursor.fetchall()
	return render_template('main.html', row=row)

@app.route('/rankings', methods=['POST','GET'])
def rankings():
	query="SELECT filename, score, wins, losses FROM images ORDER BY score DESC"
	cursor.execute(query)
	rows = cursor.fetchall()
	return render_template('rankings.html', rows=rows)

		
if __name__ == '__main__':
    app.run(debug=True)
