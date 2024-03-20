from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('baza.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html', active_page='index')

@app.route('/test')
def test():
    with get_db_connection() as conn:
        questions = conn.execute('SELECT * FROM auto_quiz').fetchall()
        return render_template('test.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    group = request.form['group']
    correct_answers = 0
    with get_db_connection() as conn:
        questions = conn.execute('SELECT * FROM auto_quiz').fetchall()
        for question in questions:
            answer = request.form.get(f'question_{question["id"]}')
            if answer and int(answer) == question['correct_answer']:
                correct_answers += 1
        conn.execute('INSERT INTO test (name, gruppa, otvet) VALUES (?, ?, ?)', (name, group, str(correct_answers)))
        conn.commit()
    return render_template('result.html', name=name, group=group, score=correct_answers, total=len(questions))

if __name__ == '__main__':
    app.run(debug=True)