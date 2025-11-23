# Sentiment Analysis Chatbot

A production-ready Python chatbot that maintains full conversation history and performs sentiment analysis on user messages using VADER (Valence Aware Dictionary and sEntiment Reasoner). The chatbot provides intelligent, context-aware responses similar to ChatGPT while analyzing emotions in real-time.

## 🚀 Features

### Tier 1: Overall Conversation Sentiment
- Analyzes the entire conversation and provides a final overall sentiment classification (Positive, Negative, or Neutral)
- Combines all user messages to determine the overall emotional tone

### Tier 2: Message-Level Sentiment Analysis (Enabled by Default)
- Performs sentiment analysis on each individual user message
- Displays sentiment label and emoji alongside each bot response (😊 Positive, 😔 Negative, 😐 Neutral)
- Tracks mood trends across the conversation (improving, declining, or consistent)
- Provides detailed message-by-message sentiment breakdown in the final summary

### Intelligent Conversation Features
- **Context-aware responses**: Remembers conversation history and references previous topics
- **Natural language understanding**: Handles questions, statements, emotions, and feedback
- **Time and date queries**: Answers "What's the time?" and "What's the date?"
- **Mathematical calculations**: Performs basic calculations
- **Emotional support**: Responds appropriately to feelings and emotions
- **Feedback handling**: Processes both positive and negative feedback professionally
- **Special events**: Recognizes birthdays, anniversaries, and celebrations

## 📁 Project Structure

```
sentiment_chatbot/
│
├── chatbot.py               # Main conversation loop and bot logic
├── sentiment.py             # VADER sentiment analysis wrapper
├── utils.py                 # Helper utilities for input cleaning and formatting
├── README.md                # This comprehensive documentation
├── requirements.txt         # Python dependencies
└── tests/
    ├── __init__.py          # Test package initialization
    └── test_sentiment.py    # Unit tests for sentiment analysis
```

## 📦 Installation

### Prerequisites
- **Python 3.7 or higher** (Python 3.8+ recommended)
- **pip** (Python package installer)
- **Terminal/Command Prompt** access

### Step-by-Step Installation

1. **Navigate to the project directory:**
   ```bash
   cd sentiment_chatbot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install:
   - `vaderSentiment` (version 3.3.2) - The sentiment analysis library

3. **Verify installation:**
   ```bash
   python -c "import vaderSentiment; print('VADER installed successfully!')"
   ```

## 🎮 Usage

### Running the Chatbot

**Basic usage (Tier 2 enabled by default):**
```bash
python chatbot.py
```

**Run with Tier 1 only (disable per-message sentiment display):**
```bash
python chatbot.py --tier1-only
```

### During Conversation

- Type your messages and press **Enter**
- The bot will respond with appropriate replies
- If Tier 2 is enabled, you'll see sentiment labels (😊 Positive, 😔 Negative, 😐 Neutral) next to each bot response
- Type `exit` to end the conversation and view the sentiment analysis summary
- Press `Ctrl+C` to interrupt and exit

## 💬 Prompt Examples

### Basic Interactions

#### Greetings
```
You: Hello
Bot: Good morning! I'm a sentiment analysis chatbot. I can chat with you, answer questions, tell you the time, do calculations, and analyze emotions in your messages. How can I help you today? [Neutral 😐]

You: Hi there
Bot: Good morning! Nice to see you again. What would you like to talk about? [Neutral 😐]
```

#### Questions
```
You: What's the time?
Bot: The current time is 03:45 PM. [Neutral 😐]

You: What's the date?
Bot: Today's date is Monday, January 15, 2024. [Neutral 😐]

You: What is sentiment analysis?
Bot: Sentiment analysis is a technique that identifies and extracts emotional tone from text. I use VADER (Valence Aware Dictionary and sEntiment Reasoner) to analyze whether messages are positive, negative, or neutral. It's quite fascinating! [Neutral 😐]

You: How are you?
Bot: I'm doing great, thank you for asking! I'm here and ready to help. How are you doing today? [Neutral 😐]
```

#### Calculations
```
You: What is 25 + 17?
Bot: The answer is 42. [Neutral 😐]

You: Calculate 10 * 5
Bot: The answer is 50. [Neutral 😐]

You: What is 20 divided by 4?
Bot: The answer is 5.0. [Neutral 😐]
```

### Emotional Interactions

#### Positive Emotions
```
You: I'm feeling great today!
Bot: That's wonderful that you're feeling great! I'm glad to hear that. What's making you feel this way? I'd love to hear more. [Positive 😊]

You: I'm so happy!
Bot: That's wonderful that you're feeling happy! I'm glad to hear that. What's making you feel this way? I'd love to hear more. [Positive 😊]

You: I'm excited about my vacation
Bot: That's wonderful that you're feeling excited! I'm glad to hear that. What's making you feel this way? I'd love to hear more. [Positive 😊]
```

#### Negative Emotions
```
You: I'm feeling sad
Bot: I'm sorry to hear you're feeling sad. That must be difficult. Would you like to talk about what's causing these feelings? I'm here to listen. [Negative 😔]

You: I'm stressed about work
Bot: It sounds like you're feeling stressed. That can be really challenging. What's on your mind? I'm here to listen and help if I can. [Negative 😔]

You: I'm worried about my exam
Bot: It sounds like you're feeling worried. That can be really challenging. What's on your mind? I'm here to listen and help if I can. [Negative 😔]
```

### Special Events

#### Birthdays
```
You: It's my birthday today
Bot: Happy Birthday! 🎉🎂🎈 That's wonderful! I hope you have an amazing day filled with joy and celebration. How are you planning to celebrate? I'd love to hear about it! [Positive 😊]

You: I'm turning 25 today
Bot: Happy Birthday! 🎉🎂🎈 That's wonderful! Happy 25th birthday! I hope you have an amazing day filled with joy and celebration. How are you planning to celebrate? I'd love to hear about it! [Positive 😊]
```

#### Other Celebrations
```
You: I got a promotion
Bot: Congratulations on your promotion/new job! 🎉 That's fantastic news! I'm so happy for you. How are you feeling about it? [Positive 😊]

You: It's my anniversary
Bot: Congratulations on your anniversary! 🎉 That's a special milestone. How long have you been celebrating? I'd love to hear about it! [Positive 😊]
```

### Feedback and Criticism

#### Positive Feedback
```
You: You are very good
Bot: Thank you so much! That really means a lot to me. I'm glad I could help and that you're having a positive experience. Is there anything else you'd like to talk about or ask? [Positive 😊]

You: You are helpful
Bot: Thank you so much! That really means a lot to me. I'm glad I could help and that you're having a positive experience. Is there anything else you'd like to talk about or ask? [Positive 😊]
```

#### Negative Feedback
```
You: Your service disappoints me
Bot: I'm truly sorry to hear that you're disappointed with my service. Your feedback is important to me, and I want to help improve your experience. Could you tell me specifically what's not working well for you? I'd like to understand better so I can assist you more effectively. [Negative 😔]

You: This bot is terrible
Bot: I'm truly sorry to hear that you're disappointed with my service. Your feedback is important to me, and I want to help improve your experience. Could you tell me specifically what's not working well for you? I'd like to understand better so I can assist you more effectively. [Negative 😔]
```

#### Comparative Feedback
```
You: Last experience was better
Bot: I understand your concern about the experience. I'm sorry if things haven't been as good as before. Could you tell me more about what made the previous experience better? I'd like to learn from that and improve. [Negative 😔]

You: It used to be better
Bot: I understand your concern. I'm sorry things aren't as good as they were. Could you tell me more about what changed or what's different now? I'd like to help improve the situation. [Negative 😔]
```

### Conversational Flow

#### Reciprocal Questions
```
You: I'm good and you?
Bot: That's great to hear! I'm doing well, thank you for asking! I'm here and ready to help. Is there anything you'd like to talk about or ask? [Positive 😊]

You: Fine, what about you?
Bot: That's great to hear! I'm doing well, thank you for asking! I'm here and ready to help. Is there anything you'd like to talk about or ask? [Neutral 😐]
```

#### Apologies
```
You: Sorry
Bot: No worries at all! There's nothing to apologize for. What's on your mind? [Neutral 😐]

You: I apologize
Bot: That's okay, no need to apologize. How can I help you? [Neutral 😐]
```

#### Name Introduction
```
You: My name is John
Bot: Nice to meet you, John! I'll remember that. How are you doing today? [Neutral 😐]

You: Call me Sarah
Bot: Nice to meet you, Sarah! I'll remember that. How are you doing today? [Neutral 😐]
```

### Complex Conversations

#### Example Full Conversation:
```
============================================================
Welcome to the Sentiment Analysis Chatbot!
============================================================
Type 'exit' to end the conversation and see sentiment analysis.
============================================================

You: Hello
Bot: Good morning! I'm a sentiment analysis chatbot. I can chat with you, answer questions, tell you the time, do calculations, and analyze emotions in your messages. How can I help you today? [Neutral 😐]

You: My name is Alice
Bot: Nice to meet you, Alice! I'll remember that. How are you doing today? [Neutral 😐]

You: I'm feeling great! It's my birthday
Bot: Happy Birthday! 🎉🎂🎈 That's wonderful! I hope you have an amazing day filled with joy and celebration. How are you planning to celebrate? I'd love to hear about it! [Positive 😊]

You: I'm having a party tonight
Bot: I understand. That's interesting! Can you tell me more about that? How does that make you feel or what would you like to know about it? [Positive 😊]

You: What's the time?
Bot: The current time is 02:30 PM. [Neutral 😐]

You: What is 50 + 25?
Bot: The answer is 75. [Neutral 😐]

You: exit

============================================================
CONVERSATION SUMMARY
============================================================

Total messages: 6
Overall sentiment: Positive
Mood trend: consistent

------------------------------------------------------------
Message-by-Message Sentiment (Tier 2):
------------------------------------------------------------
1. [Neutral] Hello
2. [Neutral] My name is Alice
3. [Positive] I'm feeling great! It's my birthday
4. [Positive] I'm having a party tonight
5. [Neutral] What's the time?
6. [Neutral] What is 50 + 25?

============================================================

Sentiment Distribution:
  Neutral: 4 messages (66.7%)
  Positive: 2 messages (33.3%)
```

## 🔧 Technologies Used

- **Python 3.7+**: Core programming language
- **VADER SentimentIntensityAnalyzer**: Lexicon and rule-based sentiment analysis tool specifically attuned to social media text
  - No machine learning model training required
  - Fast and efficient
  - Works well with short, informal text
  - Handles slang, emoticons, and capitalization

## 🧠 Sentiment Analysis Logic

### How It Works

1. **VADER Analyzer**: Uses a pre-trained sentiment analyzer that calculates polarity scores:
   - `compound`: Normalized score between -1 (most negative) and +1 (most positive)
   - `pos`: Proportion of text that is positive
   - `neu`: Proportion of text that is neutral
   - `neg`: Proportion of text that is negative

2. **Compound Score Classification**:
   - **Positive**: compound score ≥ 0.05
   - **Negative**: compound score ≤ -0.05
   - **Neutral**: -0.05 < compound score < 0.05

3. **Message-Level Analysis (Tier 2)**:
   - Each user message is analyzed individually
   - Sentiment is determined immediately and stored with the conversation entry
   - Displayed in real-time with emoji indicators

4. **Overall Analysis (Tier 1)**:
   - All user messages are combined into a single text
   - The combined text is analyzed to determine overall conversation sentiment
   - Displayed in the final summary

5. **Mood Trend Detection (Tier 2)**:
   - Compares the average sentiment of the first half of the conversation with the second half
   - **Improving**: Second half is more positive than first half
   - **Declining**: Second half is more negative than first half
   - **Consistent**: No significant change in sentiment

## 📝 Code Structure

### `chatbot.py`
Main chatbot application with intelligent response generation.

**Key Classes and Methods:**
- `Chatbot` class: Main chatbot logic
  - `__init__(tier2_enabled=True)`: Initialize chatbot with optional Tier 2 features
  - `generate_response(user_input)`: Generate contextual response based on user input
  - `run()`: Main conversation loop
  - `_display_final_summary()`: Generates and displays final sentiment summary
  - `_extract_keywords(text)`: Extract keywords and detect conversation patterns
  - `_generate_contextual_response(user_input, keywords)`: Generate intelligent responses
  - `_handle_time_question(user_input)`: Handle time/date queries
  - `_handle_calculation(user_input)`: Perform mathematical calculations

**Features:**
- Context-aware responses
- Emotion detection and appropriate responses
- Time/date queries
- Mathematical calculations
- Feedback handling (positive and negative)
- Special event recognition (birthdays, anniversaries, etc.)
- Profanity and offensive language handling
- Comparative statement handling

### `sentiment.py`
VADER sentiment analysis wrapper.

**Key Classes and Methods:**
- `SentimentAnalyzer` class: Wrapper for VADER analyzer
  - `analyze_message(message)`: Analyze single message sentiment → "Positive"/"Negative"/"Neutral"
  - `analyze_overall(messages)`: Analyze overall conversation sentiment
  - `get_mood_trend(sentiment_list)`: Detect mood trends → "improving"/"declining"/"consistent"
  - `get_detailed_scores(message)`: Get detailed polarity scores for debugging

**Convenience Functions:**
- `analyze_message(message)`: Direct access to message analysis
- `analyze_overall(messages)`: Direct access to overall analysis
- `get_mood_trend(sentiment_list)`: Direct access to mood trend detection

### `utils.py`
Helper utilities for the chatbot.

**Functions:**
- `clean_input(text)`: Normalize and clean user input (remove excessive whitespace)
- `format_conversation_summary(conversation_history, overall_sentiment, mood_trend)`: Format final summary for display

## 🧪 Testing

Run the unit tests to verify sentiment analysis functionality:

**Using pytest:**
```bash
python -m pytest tests/test_sentiment.py
```

**Using unittest:**
```bash
python -m unittest tests.test_sentiment
```

**Run with verbose output:**
```bash
python -m unittest tests.test_sentiment -v
```

The tests verify:
- ✅ Positive sentences return "Positive"
- ✅ Negative sentences return "Negative"
- ✅ Neutral sentences return "Neutral"
- ✅ Overall sentiment analysis works correctly
- ✅ Mood trend detection functions properly
- ✅ Empty messages are handled correctly
- ✅ Detailed scores are returned correctly

## 🎯 Key Features Explained

### 1. Context-Aware Responses
The chatbot remembers your name, previous topics discussed, and builds on the conversation naturally without constantly repeating what you said.

### 2. Intelligent Question Handling
- Answers "what", "who", "how", "why", "where", "when" questions appropriately
- Handles time and date queries
- Performs mathematical calculations
- Responds to reciprocal questions like "and you?"

### 3. Emotional Intelligence
- Recognizes and responds to emotions (happy, sad, stressed, etc.)
- Provides appropriate emotional support
- Tracks mood trends across the conversation

### 4. Professional Feedback Handling
- Responds appropriately to positive feedback
- Handles criticism professionally
- Processes comparative statements about experiences

### 5. Special Event Recognition
- Detects and celebrates birthdays
- Recognizes anniversaries, graduations, promotions
- Provides appropriate celebratory responses

## 🐛 Troubleshooting

### Common Issues

**Issue: ModuleNotFoundError: No module named 'vaderSentiment'**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue: Import errors when running tests**
```bash
# Solution: Run from the sentiment_chatbot directory
cd sentiment_chatbot
python -m unittest tests.test_sentiment
```

**Issue: Sentiment not displaying correctly**
- Make sure Tier 2 is enabled (default)
- Check that the message contains actual text (not just whitespace)

**Issue: Bot not responding appropriately**
- The bot uses pattern matching, so try rephrasing your message
- Check that you're using clear, complete sentences

## 📊 Example Use Cases

### 1. Emotional Support Chat
```
You: I'm feeling really stressed about work
Bot: It sounds like you're feeling stressed. That can be really challenging. What's on your mind? I'm here to listen and help if I can. [Negative 😔]

You: I have too much work to do
Bot: I understand. That's interesting! Can you tell me more about that? How does that make you feel or what would you like to know about it? [Negative 😔]
```

### 2. Information Query
```
You: What is sentiment analysis?
Bot: Sentiment analysis is a technique that identifies and extracts emotional tone from text. I use VADER (Valence Aware Dictionary and sEntiment Reasoner) to analyze whether messages are positive, negative, or neutral. It's quite fascinating! [Neutral 😐]

You: How does it work?
Bot: Sentiment analysis works by analyzing words, phrases, and their emotional context. I use VADER, which examines text for positive/negative words, punctuation, capitalization, and other linguistic cues to determine emotional tone. It's quite sophisticated! [Neutral 😐]
```

### 3. Casual Conversation
```
You: Hi, how are you?
Bot: I'm doing great, thank you for asking! I'm here and ready to help. How are you doing today? [Neutral 😐]

You: I'm good and you?
Bot: That's great to hear! I'm doing well, thank you for asking! I'm here and ready to help. Is there anything you'd like to talk about or ask? [Positive 😊]
```

## 🔮 Future Enhancements

Potential improvements for future versions:

1. **Advanced Response Generation**:
   - Integration with GPT or other language models for more natural responses
   - Machine learning-based response generation
   - Context-aware responses based on conversation history

2. **Enhanced Sentiment Features**:
   - Emotion detection (joy, sadness, anger, fear, etc.)
   - Sentiment intensity levels (very positive, slightly negative, etc.)
   - Time-series sentiment visualization
   - Multi-language sentiment analysis

3. **Data Persistence**:
   - Save conversation history to database or file
   - Conversation analytics and insights
   - User profiles and conversation history

4. **User Interface**:
   - Web-based interface
   - Real-time sentiment visualization
   - Conversation export functionality
   - Graphical sentiment charts

5. **Multi-language Support**:
   - Sentiment analysis for multiple languages
   - Language detection and automatic switching
   - Translation capabilities

6. **Customization**:
   - Configurable sentiment thresholds
   - Custom response templates
   - User-defined sentiment categories
   - Personality customization

## 📄 License

This project is provided as-is for educational and demonstration purposes.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📧 Contact

For questions or feedback, please open an issue in the project repository.

## 🙏 Acknowledgments

- **VADER Sentiment**: For providing an excellent sentiment analysis tool
- **Python Community**: For the robust ecosystem and libraries

---

**Enjoy chatting with your sentiment analysis chatbot! 🎉**
