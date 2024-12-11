from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

questions = [
    {
        "question": "What is the capital of France?",
        "options": ["A. Berlin", "B. Madrid", "C. Paris", "D. Rome"],
        "answer": "C"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["A. Earth", "B. Mars", "C. Jupiter", "D. Saturn"],
        "answer": "B"
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["A. Elephant", "B. Blue Whale", "C. Giraffe", "D. Hippopotamus"],
        "answer": "B"
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["A. Charles Dickens", "B. Jane Austen", "C. William Shakespeare", "D. Mark Twain"],
        "answer": "C"
    },
    {
        "question": "What is the chemical symbol for water?",
        "options": ["A. CO2", "B. H2O", "C. O2", "D. NaCl"],
        "answer": "B"
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET'])
def get_questions():
    return jsonify(questions)

@app.route('/submit', methods=['POST'])
def submit_answers():
    user_answers = request.json.get('answers', [])
    correct_answers = 0
    wrong_answers = 0
    score = 0

    for user_answer, question in zip(user_answers, questions):
        if user_answer.upper() == question['answer']:
            correct_answers += 1
            score += 4
        else:
            wrong_answers += 1
            score -= 1

    result = {
        "total_questions": len(questions),
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "score": score
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
