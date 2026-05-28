# retrieval.py

"""
EPISODIC MEMORY RETRIEVAL SYSTEM

Purpose:
This file is responsible for retrieving relevant episodic memories
based on the current user input.

---

## WHY RETRIEVAL IS IMPORTANT

Generating memories alone is not enough.

For episodic memory to work:
the assistant must:

* search previous experiences
* retrieve relevant memories
* reuse them in future interactions

This process is called memory retrieval.

---

## HOW RETRIEVAL WORKS

The retrieve_memory() function compares:

* current user input
  with
* stored episodic memories

The goal is to identify memories
related to the current conversation.

---

## TEXT PROCESSING

The retrieval system uses:
re.findall(r"\b\w+\b", text.lower())

Purpose:

* remove punctuation
* normalize text
* extract clean words

Example:

Input:
"I feel upset."

Processed:
["i", "feel", "upset"]

This improves word matching accuracy.

---

## WORD OVERLAP MATCHING

The system checks for overlapping words
between:

* user input
* episodic memories

If overlap exists:
the memory is considered relevant.

Example:

User Input:
"I need listening today."

Memory:
"context_tags: listening preference..."

Overlap:
{"listening"}

This triggers episodic retrieval.

---

## MEMORY INJECTION

Retrieved memories are later injected into the AI prompt.

This allows the assistant to:

* adapt behavior
* personalize communication
* reuse past interaction experiences

---

## CURRENT LIMITATION

This retrieval system currently uses:

* symbolic word matching

It does NOT yet use:

* embeddings
* semantic similarity
* vector databases

Because of this:
retrieval only works well when words overlap directly.

Later improvements may include:

* semantic retrieval
* embedding similarity search
* vector memory systems

---

## KEY CONCEPT

This file demonstrates the core idea of episodic retrieval:

Past interaction experiences
can influence future assistant behavior
through memory retrieval and prompt injection.
"""


import re


def retrieve_memory(user_input, episodic_memories):

    relevant_memories = []

    # Remove punctuation properly
    user_words = set(
        re.findall(r"\b\w+\b", user_input.lower())
    )

    print("\nUSER WORDS:\n", user_words)

    for memory in episodic_memories:

        memory_words = set(
            re.findall(r"\b\w+\b", memory.lower())
        )

        print("\nMEMORY WORDS:\n", memory_words)

        overlap = user_words.intersection(memory_words)

        print("\nOVERLAP:\n", overlap)

        if len(overlap) >= 1:

            relevant_memories.append(memory)

    return relevant_memories[-1:]