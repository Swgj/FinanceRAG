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
    
    # get first 5 questions
    questions = lines[:5]

    for i, item in tqdm(enumerate(questions)):
        query = item.get("question")
        print(f"The {i+1}th question is: ")
        print(query)
        answer = pipeline(query)
        print("The answer is: ")
        print(answer)
        item["answer"] = answer
        print("\n")

        # save the answers
        with jsonlines.open(output_path, "a") as writer:
            writer.write(item)



if __name__ == "__main__":
    main()