from ..constants import MODEL_SUMMARIZER, SUMMARIZER_PROMPT_PATH
from ..file import load_json

SUMMARIZER_PROMPT = load_json(SUMMARIZER_PROMPT_PATH)


def prompt_summarizer(prompt: list, client) -> str:
    '''
    summarizes a given prompt (must be a single element list of openai prompt format dic)
    '''
    completion = client.chat.completions.create(
        model=MODEL_SUMMARIZER, 
        messages=[SUMMARIZER_PROMPT] + prompt
    )

    summary = completion.choices[0].message.content

    return summary