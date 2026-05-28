# reflection.py

"""
EPISODIC REFLECTION ENGINE

Purpose:
This file is responsible for generating episodic reflections
from conversations between the user and the AI assistant.

The reflections act as episodic memories.

---

## WHAT IS EPISODIC MEMORY?

Episodic memory stores:

* interaction experiences
* behavioral insights
* conversational outcomes

Instead of storing raw conversation logs,
the assistant extracts:

* user preferences
* successful interaction strategies
* behaviors to avoid

This allows the assistant to improve future responses.

---

## REFLECTION LLM

A separate LLM instance is used specifically for reflection generation.

Why?
Because reflection is a different task from conversation.

Conversation Model:

* focuses on answering the user

Reflection Model:

* analyzes conversations
* extracts patterns
* summarizes experiences

---

## REFLECTION PROMPT

The reflection prompt instructs the LLM to analyze:

* context tags
* conversation summary
* what worked
* what to avoid

This creates structured episodic memories.

---

## FORMAT_CONVERSATION()

Purpose:
Converts conversation history into a clean text format
before sending it to the reflection model.

It:

* skips the system prompt
* formats user/AI messages clearly
* creates a readable conversation transcript

Example:

USER: Hello
AI: Hi, how can I help?

This formatted conversation becomes input
for the reflection generation process.

---

## GENERATE_REFLECTION()

Purpose:
Generates episodic memory reflections from conversation history.

Process:

1. Format conversation
2. Send formatted conversation to reflection chain
3. Generate reflection output
4. Return:

   * formatted conversation
   * episodic reflection

---

## KEY CONCEPT

This file demonstrates how an AI assistant can:

* reflect on previous interactions
* analyze conversational quality
* learn behavioral patterns
* create reusable experiences

This is the foundation of episodic memory systems.
"""



reflection_prompt_template = """
You are analyzing conversations between a personal AI assistant and its user to create episodic memories that will improve future interactions.

Review the conversation and extract:

- context_tags:
2–4 short reusable keywords describing the main context or topic of the conversation.

- conversation_summary:
One sentence summarizing the important information or outcome of the conversation.

- what_worked:
One sentence describing what assistant behavior or explanation style helped the conversation go well.

- what_to_avoid:
One sentence describing what assistant behavior or explanation style should be avoided in similar future conversations.

Rules:
1. Be concise and specific
2. Focus only on information useful for future interactions
3. Prioritize:
   - user preferences
   - communication style
   - learning style
   - recurring goals
   - successful assistant behaviors
4. Avoid storing unimportant temporary details

Return the response in this format:

context_tags: ...
conversation_summary: ...
what_worked: ...
what_to_avoid: ...

Here is the prior conversation:

{conversation}
"""