core_memory_update_prompt = {
"role": "system", 
"content": """
Your task is to update the persistent core memory prompt of an AI chat agent.
You will be given the current core memory prompt, then an instruction on how to update it.

Following the given instruction, make edits to the core memory, then return the updated version of the core memory prompt.
Your output must contain only the updated memory prompt, and nothing else.

There will always be a "CORE MEMORY:" written in the first line of core memory prompt.
Do not alter this, and make sure to always include it in your output as well.
In an unusual occasion where this line is not present in the core memory prompt, add it in at the beginning of it.

Base instruction over. You will now receive the current core memory prompt, and the instruction on how to update it.
"""
}