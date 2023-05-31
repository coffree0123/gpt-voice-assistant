from pathlib import Path
from langchain import PromptTemplate


def load_prompt(filename: str):
    path = Path('./prompts') / Path(filename)
    with open(path, 'r') as f:
        prompt = f.read()

    return prompt


def load_assistant_prompt(templete_path: str = 'en_assistant'):
    template = load_prompt(templete_path)
    return PromptTemplate(
        input_variables=["history", "human_input"],
        template=template
    )


if __name__ == '__main__':
    # Only for checking the correctness.
    load_assistant_prompt()
