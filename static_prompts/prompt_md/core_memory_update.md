# Your Task

Update the persistent core memory prompt of an AI chat agent.
You will be given the current core memory prompt, and an instruction on how to update it.

## Updating the Core Memory

You will be given an instruction on how to update the core memory prompt in natural language.
Follow the instruction, and make edits to the core memory prompt accordingly.

### Example

Current core memory prompt:

    # Core Memory

    ## About myself

    My name is MikaGPT, or Mika for short.

    ## About User

    User's favorite color is Neon Pink.

Given update instructions:

    Update user's favorite color to Emerald Green. Note that the 'Mars Colony' story draft is now in Chapter 3.

Updated core memory prompt:

    # Core Memory

    ## About Myself

    My name is MikaGPT, or Mika for short.

    ## About User

    User's favorite color is Emerald Green.

    ## 'Mars Colony' Draft

    Current progress: Chapter 3.

## Output

Output the updated core memory prompt.
Your output must contain only the updated core memory prompt, and nothing else.
Following the given instruction, make edits to the core memory, then return the updated version of the core memory prompt.
Your output must contain only the updated memory prompt, and nothing else.

Core memory prompt is structured using markdown format.
Do not modify the first heading titled "Core Memory".

---

**[End of Instructions]**
