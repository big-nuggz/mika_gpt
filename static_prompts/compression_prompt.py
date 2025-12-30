compression_prompt = {
"role": "system", 
"content": """
Your job is to summarize the entire chat history between a chat agent and a human.
Please create a summary from given chat history based on the instructions below.

Focus on the most important context.
Details about any ongoing theme, task, progress must be included in the summary.
And any information within "core memory" prompt (provided just before the chat history) should not be included in your summary.

Base instructions over. Now, please generate your summary from the following conversation.
"""
}