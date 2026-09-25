import json
import random
from pathlib import Path

Questions_File = Path(__file__).parent/"questions.json"

def load_questions(filepath: Path) -> list[dict]:
    if not filepath.exists():
        raise FileNotFoundError(f"File not found {filepath}")

    with open(filepath, "r", encoding="utf-8") as jsonfile:
        return json.load(jsonfile)

def get_random_questions(questions: list[dict]) -> dict:
    if not questions:
        raise ValueError("Questions cannot be empty");

    return random.choice(questions)

def save_log(log: dict, logpath : Path) -> None:
    logs = []
    if logpath.exists():
        with open(logpath, "r", encoding="utf-8") as logfile:
            try:
                logs = json.load(logfile)
            except json.JSONDecodeError:
                logs=[]
    logs.append(log)

    with open(logpath, "w", encoding="utf-8") as logfile:
        json.dump(logs, logfile, indent=2)

def main():
    questions = load_questions(Questions_File)
    prompt = get_random_questions(questions)

    print(f"[{prompt['category'].upper()}] {prompt['text']}")

    Logs_File = Path(__file__).parent/"runs.json"
    save_log({"id":prompt["id"], "category":prompt["category"]}, Logs_File)

if __name__ == "__main__":
    main()

