import requests
import random

def fetch_questions(amount=20):
    url = f"https://opentdb.com/api.php?amount={amount}&type=multiple"
    data = requests.get(url).json()

    questions = []
    for item in data["results"]:
        options = item["incorrect_answers"] + [item["correct_answer"]]
        random.shuffle(options)
        correct_index = options.index(item["correct_answer"]) + 1

        questions.append({
            "question": item["question"],
            "options": options,
            "answer": correct_index
        })

    return questions