from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from prompts.reflection_prompt import reflection_prompt_template

# Reflection LLM
reflection_llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0.3
)

# Reflection prompt
reflection_prompt = ChatPromptTemplate.from_template(
    reflection_prompt_template
)

# Reflection chain
reflect = reflection_prompt | reflection_llm



# -------- Format Conversation --------

def format_conversation(messages):

    conversation = []

    # Skip system prompt
    for message in messages[1:]:

        conversation.append(
            f"{message.type.upper()}: {message.content}"
        )

    return "\n".join(conversation)


# -------- Generate Reflection --------

def generate_reflection(messages):

    conversation = format_conversation(messages)

    reflection = reflect.invoke({
        "conversation": conversation
    })

    return conversation, reflection