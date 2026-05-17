import os

HIGH_SCORE_FILE = "highscore.txt"

def get_high_score():
    if not os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write("0")
    with open(HIGH_SCORE_FILE, "r") as f:
        return int(f.read())

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))