def quiz_app():
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

    correct_answers = 0
    wrong_answers = 0
    score = 0

    print("Welcome to the Quiz App!\n")

    for i, question in enumerate(questions, start=1):
        print(f"Q{i}: {question['question']}")
        for option in question['options']:
            print(option)
        
        user_answer = input("Your answer (A/B/C/D): ").strip().upper()
        
        if user_answer == question['answer']:
            print("Correct!\n")
            correct_answers += 1
            score += 4
        else:
            print(f"Wrong! The correct answer was {question['answer']}.\n")
            wrong_answers += 1
            score -= 1

    print("Quiz Completed!\n")
    print(f"Total Questions: {len(questions)}")
    print(f"Correct Answers: {correct_answers}")
    print(f"Wrong Answers: {wrong_answers}")
    print(f"Your Total Score: {score}")

if __name__ == "__main__":
    quiz_app()
