from datetime import datetime

from openai.types.completion_usage import CompletionUsage


def get_unix_time() -> int:
    return round(datetime.now().timestamp())

def print_statistics(usage: CompletionUsage) -> None:
    print(f'tokens in the generated completion: {usage.completion_tokens}')
    print(f'tokens in the prompt: {usage.prompt_tokens}')
    print(f'total tokens used in the request: {usage.total_tokens}')