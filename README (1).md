
# 🧠 Mental Health Chatbot – *Hassan ka Dost*

This is a multilingual, AI-powered mental health support chatbot that uses **LangChain**, **Google Gemini (Generative AI)**, and **Gradio** to provide compassionate and ethical support in English, Urdu, and Roman Urdu. It is designed to help users with stress, anxiety, depression, and self-care strategies in a safe and supportive environment.

## 🌟 Features

- 🤖 Powered by **Google Gemini 2.0 Flash** via LangChain
- 💬 Supports **English**, **Urdu**, and **Roman Urdu**
- 🧘 Offers general guidance on **stress**, **anxiety**, **coping strategies**, and **self-care**
- 🧠 Maintains chat context using **ConversationBufferMemory** and **WindowMemory**
- 🛡️ Includes **ethical safeguards** to redirect at-risk users to professional help
- 🌐 Simple, clean **Gradio** interface for easy interaction

---

## 🚀 Demo

> The chatbot is accessible via a local Gradio interface and can also be shared with others using a public Gradio link.

---

## 📁 Project Structure

```bash
.
├── lang_chain(mental_health_chat_bot).py  # Main application script
└── README.md                              # Project documentation
```

---

## 🔧 Installation

1. Clone the repository or download the `.py` file.
2. Make sure you have Python 3.8+ installed.
3. Install required libraries:

```bash
pip install langchain-core langchain-community langchain_google_genai Ipython gradio
```

---

## 🔑 Environment Setup

Before running the chatbot, ensure you’ve set your Google Generative AI API key properly.

```python
os.environ["GOOGLE_API_KEY"] = "your_api_key_here"
```

> ⚠️ **Important**: Keep your API key private and never expose it in public repositories.

---

## 🧠 How It Works

### System Prompt

A well-defined **system prompt** configures the chatbot with the following responsibilities:

- Stay within the mental health domain
- Avoid diagnosis or medication suggestions
- Encourage reaching out to licensed professionals when necessary
- Use compassionate and supportive language
- Respond in the user's language (English, Urdu, or Roman Urdu)

### Conversation Memory

- `ConversationBufferMemory`: Stores the entire conversation history.
- `ConversationBufferWindowMemory`: Stores only the last 10 interactions to reduce context overflow.

### LangChain Chain

A LangChain LCEL chain is constructed using:
- System prompt
- Memory (chat + recent)
- User input
- Google Gemini model (`gemini-2.0-flash`)
- Output parsing

### Gradio Interface

The app launches a Gradio interface with:
- Chatbot window
- Textbox for input
- Buttons to send or clear messages
- Welcome message in multiple languages

---

## 💡 Usage

Run the Python script:

```bash
python lang_chain(mental_health_chat_bot).py
```

Then access the Gradio interface either locally or through the public link provided after launching.

---

## ⚠️ Disclaimer

This chatbot:
- Does **not** replace licensed medical or psychological professionals
- Should not be used for **emergency situations**
- Will **redirect** users expressing self-harm or suicidal thoughts to professional help or helplines

---

## 🧩 Future Improvements

- Integrate with external mental health APIs for real-time resources
- Add emotion detection and sentiment analysis
- Extend language support beyond the current list
- Allow speech-to-text and text-to-speech for accessibility

---

## 👨‍💻 Author

- Developed by **[Your Name or Alias]**
- Designed for educational and humanitarian purposes
- Inspired by a desire to create accessible mental health tools

---

## 📜 License

This project is open-source. You are free to modify or distribute it **non-commercially**, with appropriate attribution.
