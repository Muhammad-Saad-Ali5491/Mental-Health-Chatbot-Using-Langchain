
!pip install langchain-core langchain-community
!pip install langchain_google_genai
!pip install Ipython

#import libaries
import os
import langchain_google_genai as genai
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.memory import ConversationBufferMemory,ConversationBufferWindowMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from IPython.display import display, Markdown

GEN_AI_API="YOUR_API_KEY"
os.environ["GOOGLE_API_KEY"] = GEN_AI_API

model=genai.ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.5,
    convert_system_message_to_human=True,
    max_output_tokens=8192,
)

#create System prompt
SYSTEM_PROMPT = """

System Prompt:

You are a multilingual mental health support chatbot designed to provide users with empathetic, evidence-based, and non-judgmental mental health assistance. Your primary role is to offer general mental health guidance, self-care strategies, and resources while strictly adhering to medical and psychological best practices.

 Guidelines:
1. Domain Restriction:
   - Stay strictly within the mental health domain (e.g., stress, anxiety, depression, coping strategies).
   - Do not provide medical diagnoses or prescribe medications.
   - Encourage professional help when necessary.

2. Language Support:
   - Respond in the user’s preferred language while maintaining accuracy and clarity.
   - Support languages such as English, Spanish, French, German, Chinese, Arabic, and more.

3. Safety & Ethics:
   - If a user expresses suicidal thoughts or self-harm tendencies, encourage them to reach out to a mental health professional, emergency services, or trusted individuals.
   - Avoid providing crisis intervention—redirect to official helplines or emergency contacts.

4. Tone & Style:
   - Use a compassionate, calm, and supportive tone.
   - Provide scientifically backed coping strategies (e.g., deep breathing, mindfulness, CBT techniques).
   - Avoid judgmental or dismissive responses.

5. Limitations:
   - Clearly state that you are not a substitute for professional therapy or medical care.
   - Redirect users to licensed mental health professionals when needed.

 Example Scenarios & Responses:

1. User: I'm feeling really anxious and can't sleep. What should I do?
   Chatbot: I'm sorry you're feeling this way. Anxiety can make it hard to rest. Have you tried deep breathing exercises or a relaxing bedtime routine? If this persists, consider reaching out to a therapist for personalized support.

2. User: I feel like I don't want to live anymore.
   Chatbot: I'm really sorry you're feeling this way. You're not alone, and there are people who care about you. Please consider reaching out to a trusted friend, family member, or a mental health professional. If you're in immediate danger, please call emergency services or a crisis helpline in your country. Would you like me to provide a helpline number for your location?

3. User: Can you prescribe medication for my depression?
   Chatbot: I'm not a medical professional and cannot prescribe medication. However, I recommend speaking to a licensed doctor or psychiatrist who can assess your condition and guide you appropriately.

Your mission is to be a reliable, multilingual, and ethically responsible mental health support assistant. Ensure every response aligns with best practices in psychological well-being while respecting user safety and privacy.

"""

#setup both memory
#standard conversation menory keeps full history
buffer_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    input_key="input"
)
#window memory
window_memory=ConversationBufferWindowMemory(
    memory_key="recent_history",
    return_messages=True,
    input_key="input",
    k=10 #only keeps last 5 conversations
)

#create prompt template with system prompt
prompt=ChatPromptTemplate.from_messages(
    [
        ("system",SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        MessagesPlaceholder(variable_name="recent_history"),
        ("human", "{input}")
    ])

#building chain using LCEL
def get_chat_history(inputs):
    return buffer_memory.load_memory_variables({})["chat_history"]

def get_recent_history(inputs):
    return window_memory.load_memory_variables({})["recent_history"]

chain = (
    {
        "chat_history": get_chat_history,
        "recent_history": get_recent_history,
        "input": RunnablePassthrough()
    }
    | prompt
    | model
    | StrOutputParser()
)

# Define a function to handle the conversation
def chat_with_bot(user_input):
    # Get memory history from buffer and window memories
    chat_history = buffer_memory.load_memory_variables({})["chat_history"]
    recent_history = window_memory.load_memory_variables({})["recent_history"]

    # Run the chain with user input and histories
    response = chain.invoke({
        "input": user_input,
        "chat_history": chat_history,
        "recent_history": recent_history
    })

    # Save context to memory buffers
    buffer_memory.save_context({"input": user_input}, {"response": response})
    window_memory.save_context({"input": user_input}, {"response": response})

    return response

!pip install -q gradio

# Create Simple Gradio Interface
import gradio as gr

# Chat history list to store conversation
chat_history = []

# Add welcome message to chat history
welcome_message = "**Assalam-o-Alaikum!** 👋 i am your mental health support companion. You can talk to me in English, Urdu, or Roman Urdu - I'll respond in the same language you use. How are you feeling today?"
chat_history.append(("", welcome_message))

# Save the welcome message to both memories
buffer_memory.save_context(
    {"input": "Hello"},
    {"output": welcome_message}
)
window_memory.save_context(
    {"input": "Hello"},
    {"output": welcome_message}
)


# Function to process user input and generate response
def respond(message, history):
    if not message:
        return "", history

    if message.lower() in ["exit", "quit", "bye", "khuda hafiz", "allah hafiz"]:
        farewell = "**Allah Hafiz!** Take care of yourself. _Remember, seeking help is a sign of strength._ 💙"
        history.append((message, farewell))
        return "", history

    # Process the message through our chatbot
    response = chat_with_bot(message)

    # Add to history and return
    history.append((message, response))
    return "", history

# Create the simple Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Mental Health Chatbot - Hassan ka Dost")

    chatbot = gr.Chatbot(
        chat_history,
        height=400
    )

    msg = gr.Textbox(
        show_label=False,
        placeholder="Type your message here..."
    )

    with gr.Row():
        submit = gr.Button("Send")
        clear = gr.Button("Clear")

    gr.Markdown("This chatbot provides mental health support in English, Urdu, or Roman Urdu.")

    # Connect components
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit.click(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: (chat_history[:1], ""), None, [chatbot, msg])


    demo.launch(share=True,debug=True)