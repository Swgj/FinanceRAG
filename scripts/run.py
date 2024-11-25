# get questions from dataset, and use pipeline to get the answers

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline import pipeline
from src.config import config
from tqdm import tqdm
import jsonlines


def main():
    # get questions from dataset
    questions_path = config.get_path("dataset", "question")
    output_path = config.get_path("output", "result")

    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    with jsonlines.open(questions_path) as reader:
        lines = list(reader)
        print(len(lines))
    
    count = 0
    # continue from the last question
    if os.path.exists(output_path):
        with jsonlines.open(output_path) as reader:
            answered = list(reader)
            count = len(answered)
            print(f"already get {count} answers")
            lines = lines[len(answered):]
            print(f"continue from the {count+1}th question")

    questions = lines

    for item in tqdm(questions):
        query = item.get("question")
        print(f"The {count+1}th question is: ")
        print(query)
        try:
            answer = pipeline(query)
        except Exception as e:
            answer = str(e)
        print("The answer is: ")
        print(answer)
        item["answer"] = answer
        print("\n")

        # save the answers
        with jsonlines.open(output_path, "a") as writer:
            writer.write(item)
        
        count += 1



if __name__ == "__main__":
    main()