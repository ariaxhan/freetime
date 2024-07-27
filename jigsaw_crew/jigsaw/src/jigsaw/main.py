#!/usr/bin/env python
import sys
import os
from dotenv import load_dotenv
from crew import JigsawCrew

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information.

def run():
    # Load environment variables
    load_dotenv()

    # Retrieve environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")

    """
    Run the crew.
    """
    inputs = {
        'query': 'Lands end in San Francisco'
    }
    JigsawCrew().crew().kickoff(inputs=inputs)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "query": "Golden Gate Bridge in San Francisco"
    }
    try:
        JigsawCrew().crew().train(n_iterations=int(sys.argv[2]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        JigsawCrew().crew().replay(task_id=sys.argv[2])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <run|train|replay> [arguments]")
        sys.exit(1)

    command = sys.argv[1].lower()
    if command == 'run':
        run()
    elif command == 'train':
        if len(sys.argv) < 3:
            print("Usage: python main.py train <n_iterations>")
            sys.exit(1)
        train()
    elif command == 'replay':
        if len(sys.argv) < 3:
            print("Usage: python main.py replay <task_id>")
            sys.exit(1)
        replay()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
