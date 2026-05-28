# main.py

"""
MAIN ORCHESTRATION FILE

Purpose:
This file acts as the central controller of the AI assistant system.
It manages:

* user interaction
* working memory
* episodic memory retrieval
* reflection generation
* AI response generation

This is the main runtime entry point of the assistant.

---

## WORKING MEMORY

The `messages` list represents working memory.

Working memory stores:

* recent conversation history
* current session context
* user and AI messages during runtime

Example:
messages = [system_prompt]

As the user and AI continue chatting:

* HumanMessage objects are appended
* AI responses are appended

This allows the model to maintain conversational continuity.

IMPORTANT:
Working memory only exists during runtime.
Once the Python program stops:

* messages are cleared
* context is lost

---

## EPISODIC MEMORY

The `episodic_memories` list stores reflections generated
from previous conversations.

Unlike working memory:
episodic memory does not store raw chat history.

Instead, it stores:

* interaction summaries
* behavioral insights
* communication preferences
* what worked well
* what should be avoided

These reflections help the assistant adapt future behavior.

---

## EPISODIC RETRIEVAL

Before generating a response:
the assistant searches episodic memories using:
retrieve_memory()

If relevant memories are found:
they are injected into the prompt as additional context.

This allows the assistant to:

* reuse past interaction experiences
* personalize responses
* adapt communication style

---

## TEST MODE

TEST_EPISODIC_MEMORY = True

When enabled:

* working memory influence is bypassed
* only episodic memories influence behavior

This helps verify that:
episodic retrieval genuinely affects responses
instead of the model simply reading chat history.

---

## RUNTIME FLOW

User Input
↓
Store in Working Memory
↓
Retrieve Relevant Episodic Memories
↓
Inject Retrieved Memories
↓
Generate AI Response
↓
Generate Reflection
↓
Store Reflection as Episodic Memory

---

## KEY CONCEPT

This file demonstrates how different memory systems
work together inside an AI assistant architecture.

Working memory handles:

* short-term conversational context

Episodic memory handles:

* reusable interaction experiences
* behavioral adaptation

The goal is not just memory storage,
but improving future assistant behavior using past interactions.
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from memory.reflection import generate_reflection
from memory.retrieval import retrieve_memory


# -------- Creating the Model --------

model = ChatOllama(
    model="qwen2.5:7b",
    temperature=0
)


# -------- System Prompt --------

system_prompt = SystemMessage(
    content="You are a helpful AI assistant. Answer the user's queries succinctly."
)


# -------- Working Memory --------

messages = [system_prompt]


# -------- Episodic Memory --------
# Temporary runtime memory storage

TEST_EPISODIC_MEMORY = True
episodic_memories = []


# -------- Chat Loop --------

while True:

    # User Input
    user_input = input("\nUser: ")

    # Exit Condition
    if user_input.lower() in ["exit", "bye", "goodbye"]:
        break

    # Convert User Input into HumanMessage object
    user_message = HumanMessage(content=user_input)

    # -------- Store in Working Memory --------

    messages.append(user_message)

    # -------- Episodic Retrieval --------

    retrieved_memories = retrieve_memory(
        user_input,
        episodic_memories
    )

    print("\n----- RETRIEVED EPISODIC MEMORIES -----\n")
    print(retrieved_memories)

    # -------- Inject Retrieved Episodic Memories --------

    if retrieved_memories:

        # Combines multiple retrieved memories into one formatted string
        memory_context = "\n".join(retrieved_memories)

        memory_message = SystemMessage(
            content=f"""
Relevant episodic memories from previous conversations:

{memory_context}

Use these memories to improve your response.
"""
        )

        messages.append(memory_message)

    # -------- Generate AI Response --------

    if TEST_EPISODIC_MEMORY:

        # Isolated episodic testing mode
        temp_messages = [system_prompt]

        # Inject episodic memories only
        if retrieved_memories:
            temp_messages.append(memory_message)

        # Add current user message only
        temp_messages.append(user_message)

        response = model.invoke(temp_messages)

    else:

        # Normal assistant behavior
        response = model.invoke(messages)

    print("\nAI:", response.content)

    # -------- Store AI Response in Working Memory --------

    messages.append(response)

    # -------- Episodic Reflection --------

    conversation, reflection = generate_reflection(messages)

    # Store episodic reflection temporarily
    episodic_memories.append(reflection.content)

    print("\n----- EPISODIC MEMORY -----\n")

    print(reflection.content)