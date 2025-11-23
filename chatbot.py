
import sys
import re
from datetime import datetime
from sentiment import analyze_message, analyze_overall, get_mood_trend
from utils import clean_input, format_conversation_summary


class Chatbot:
    def __init__(self, tier2_enabled=True):
        
        self.conversation_history = []
        self.tier2_enabled = tier2_enabled
        self.greeting_count = 0
        self.user_info = {}  # Store user information from conversation
        self.discussed_topics = []  # Track topics discussed in conversation
        self.conversation_memory = {}  # Store important facts from conversation
    
    def _extract_keywords(self, text):
        """Extract important keywords and topics from user input."""
        text_lower = text.lower()
        keywords = {
            'name': None,
            'feeling': None,
            'topic': None,
            'is_question': text_lower.strip().endswith('?') or any(word in text_lower for word in ['what', 'who', 'where', 'when', 'why', 'how']),
            'is_apology': any(word in text_lower for word in ['sorry', 'apologize', 'apology', 'forgive']),
            'is_greeting': any(word in text_lower for word in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'morning', 'afternoon', 'evening']),
            'is_goodbye': any(word in text_lower for word in ['bye', 'goodbye', 'see you', 'farewell', 'later']),
            'is_thanks': any(word in text_lower for word in ['thank', 'thanks', 'appreciate', 'grateful']),
            'is_birthday': any(phrase in text_lower for phrase in ['birthday', 'my birthday', "it's my birthday", 'today is my birthday', 'turning', 'years old today', 'born today']),
            'is_special_event': any(phrase in text_lower for phrase in ['anniversary', 'graduation', 'wedding', 'promotion', 'new job', 'got engaged']),
            'is_reciprocal_question': any(phrase in text_lower for phrase in ['and you', 'what about you', 'how about you', 'you?', 'and yourself']),
            'is_complaint': any(word in text_lower for word in ['disappoint', 'disappointing', 'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'sucks', 'useless', 'stupid', 'dumb', 'waste', 'poor', 'pathetic']),
            'is_criticism': any(phrase in text_lower for phrase in ['your service', 'you are bad', "you're bad", 'you are terrible', "you're terrible", 'you are awful', "you're awful", 'you are horrible', "you're horrible", 'you are worst', "you're worst", 'you suck', 'this bot', 'this chatbot', 'not helpful', 'not working', 'does not work', "doesn't work"]),
            'is_positive_feedback': any(phrase in text_lower for phrase in ['you are good', "you're good", 'you are great', "you're great", 'you are excellent', "you're excellent", 'you are amazing', "you're amazing", 'you are wonderful', "you're wonderful", 'you are awesome', "you're awesome", 'you are very good', "you're very good", 'you are the best', "you're the best", 'you are helpful', "you're helpful", 'you are perfect', "you're perfect"]),
            'is_comparison': any(phrase in text_lower for phrase in ['was better', 'was worse', 'used to be', 'better than', 'worse than', 'not as good', 'not as bad', 'improved', 'got worse', 'declined', 'better before', 'worse before']),
            'is_experience_feedback': any(phrase in text_lower for phrase in ['experience was', 'last experience', 'previous experience', 'this experience', 'my experience', 'the experience']),
            'is_profanity': any(re.search(r'\b' + re.escape(word) + r'\b', text_lower) for word in ['fuck', 'damn', 'hell', 'shit', 'asshole', 'bitch', 'bastard', 'crap', 'piss', 'dick', 'cock', 'pussy', 'motherfucker', 'fucking', 'fucked']),
            'is_offensive': any(phrase in text_lower for phrase in ['fuck you', 'fuck off', 'go to hell', 'screw you', 'shut up', 'shut your', 'kill yourself', 'die']),
            'needs_time': any(word in text_lower for word in ['time', 'what time', 'current time', 'clock']),
            'needs_date': any(phrase in text_lower for phrase in ['what date', 'what\'s the date', 'what is the date', 'what day is it', 'what day is today', 'date today', 'today\'s date', 'current date']) or (('date' in text_lower or 'day is it' in text_lower) and any(q_word in text_lower for q_word in ['what', 'when', 'which'])),
            'needs_calc': bool(re.search(r'\d+\s*[+\-*/]\s*\d+', text)) or any(word in text_lower for word in ['calculate', 'what is', 'equals', '=']),
        }
        
        # Extract feelings/emotions FIRST (before name extraction to avoid conflicts)
        feeling_words = ['happy', 'sad', 'angry', 'excited', 'worried', 'anxious', 
                        'stressed', 'tired', 'energetic', 'confused', 'frustrated',
                        'grateful', 'proud', 'disappointed', 'relieved', 'upset', 'mad',
                        'depressed', 'down', 'unhappy', 'great', 'wonderful', 'amazing',
                        'fine', 'okay', 'ok', 'terrible', 'awful', 'horrible']
        for word in feeling_words:
            if word in text_lower:
                keywords['feeling'] = word
                break
        
        # Try to extract name - but ONLY if no feeling was detected
        # Also use more specific patterns that are less likely to match emotions
        if not keywords['feeling']:
            # Extended blacklist of words that should never be treated as names
            name_blacklist = [
                'feeling', 'doing', 'going', 'here', 'there', 'sorry', 'fine', 'good', 'bad',
                'happy', 'sad', 'angry', 'excited', 'worried', 'anxious', 'stressed', 'tired',
                'energetic', 'confused', 'frustrated', 'grateful', 'proud', 'disappointed',
                'relieved', 'upset', 'mad', 'depressed', 'down', 'unhappy', 'great', 'wonderful',
                'amazing', 'okay', 'ok', 'terrible', 'awful', 'horrible', 'feeling', 'being',
                'working', 'studying', 'learning', 'trying', 'thinking', 'wondering'
            ]
            
            # More specific name patterns (prefer these)
            specific_name_patterns = [
                r"my name is (\w+)",
                r"call me (\w+)",
                r"name's (\w+)",
                r"i go by (\w+)",
                r"people call me (\w+)"
            ]
            
            for pattern in specific_name_patterns:
                match = re.search(pattern, text_lower)
                if match:
                    potential_name = match.group(1).lower()
                    if potential_name not in name_blacklist and len(potential_name) > 1:
                        keywords['name'] = potential_name.capitalize()
                        break
            
            # Less specific patterns (only if no specific pattern matched and still no feeling)
            if not keywords['name']:
                less_specific_patterns = [
                    r"i'm (\w+)",
                    r"i am (\w+)"
                ]
                for pattern in less_specific_patterns:
                    match = re.search(pattern, text_lower)
                    if match:
                        potential_name = match.group(1).lower()
                        # Be very strict with these patterns - check if it's clearly a name
                        if (potential_name not in name_blacklist and 
                            len(potential_name) > 2 and  # Names are usually longer
                            not any(char.isdigit() for char in potential_name) and  # No numbers
                            potential_name[0].isalpha()):  # Starts with letter
                            keywords['name'] = potential_name.capitalize()
                            break
        
        return keywords
    
    def _handle_time_question(self, user_input):
        """Handle time-related questions."""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")  # 12-hour format with AM/PM
        date_str = now.strftime("%A, %B %d, %Y")  # Day, Month Day, Year
        
        user_lower = user_input.lower()
        
        # Check if it's actually asking for time/date (not just mentioning it)
        is_time_question = any(phrase in user_lower for phrase in ['what time', 'current time', 'time now', 'time is it', 'what\'s the time'])
        is_date_question = any(phrase in user_lower for phrase in ['what date', 'what\'s the date', 'date today', 'today\'s date', 'current date', 'what day is it', 'what day is today'])
        
        if is_time_question:
            return f"The current time is {time_str}."
        elif is_date_question:
            return f"Today's date is {date_str}."
        elif 'day' in user_lower and any(q_word in user_lower for q_word in ['what', 'which']):
            day_name = now.strftime("%A")
            return f"Today is {day_name}."
        elif 'time' in user_lower:
            # Generic time mention - only respond if it seems like a question
            if user_lower.endswith('?') or any(q_word in user_lower for q_word in ['what', 'when', 'which']):
                return f"The current time is {time_str}."
        elif 'date' in user_lower:
            # Generic date mention - only respond if it seems like a question
            if user_lower.endswith('?') or any(q_word in user_lower for q_word in ['what', 'when', 'which']):
                return f"Today's date is {date_str}."
        
        # Default fallback (shouldn't reach here if needs_time/needs_date is set correctly)
        return f"The current time is {time_str} and today's date is {date_str}."
    
    def _handle_calculation(self, user_input):
        """Handle mathematical calculations in natural language or mathematical notation."""
        try:
            user_lower = user_input.lower()
            
            # Handle natural language calculations
            # Pattern: "what is X plus/minus/times/divided by Y"
            natural_patterns = [
                (r'what is (\d+)\s+plus\s+(\d+)', lambda m: int(m.group(1)) + int(m.group(2))),
                (r'what is (\d+)\s+(\+)\s+(\d+)', lambda m: int(m.group(1)) + int(m.group(3))),
                (r'(\d+)\s+plus\s+(\d+)', lambda m: int(m.group(1)) + int(m.group(2))),
                (r'what is (\d+)\s+minus\s+(\d+)', lambda m: int(m.group(1)) - int(m.group(2))),
                (r'what is (\d+)\s+(\-)\s+(\d+)', lambda m: int(m.group(1)) - int(m.group(3))),
                (r'(\d+)\s+minus\s+(\d+)', lambda m: int(m.group(1)) - int(m.group(2))),
                (r'what is (\d+)\s+times\s+(\d+)', lambda m: int(m.group(1)) * int(m.group(2))),
                (r'what is (\d+)\s+(\*)\s+(\d+)', lambda m: int(m.group(1)) * int(m.group(3))),
                (r'(\d+)\s+times\s+(\d+)', lambda m: int(m.group(1)) * int(m.group(2))),
                (r'what is (\d+)\s+divided by\s+(\d+)', lambda m: int(m.group(1)) / int(m.group(2)) if int(m.group(2)) != 0 else None),
                (r'what is (\d+)\s+(\/)\s+(\d+)', lambda m: int(m.group(1)) / int(m.group(3)) if int(m.group(3)) != 0 else None),
                (r'(\d+)\s+divided by\s+(\d+)', lambda m: int(m.group(1)) / int(m.group(2)) if int(m.group(2)) != 0 else None),
            ]
            
            for pattern, func in natural_patterns:
                match = re.search(pattern, user_lower)
                if match:
                    result = func(match)
                    if result is None:
                        return "I can't divide by zero!"
                    return f"The answer is {result}."
            
            # Handle direct mathematical expressions (e.g., "5 + 3", "10 * 2")
            # Extract mathematical expression - keep numbers, operators, and parentheses
            expression = re.sub(r'[^0-9+\-*/().\s]', '', user_input)
            expression = expression.strip()
            
            # Safety: only allow basic math operations
            if expression and re.match(r'^[\d+\-*/().\s]+$', expression):
                # Evaluate safely
                result = eval(expression)
                return f"The answer is {result}."
            
            return None
        except ZeroDivisionError:
            return "I can't divide by zero!"
        except Exception:
            return None
    
    def _get_conversation_context(self, lookback=5):
        """Get recent conversation context for better responses."""
        if len(self.conversation_history) == 0:
            return []
        
        # Get last N exchanges for context
        recent = self.conversation_history[-lookback:]
        return recent
    
    def _extract_topics_from_history(self, user_input):
        """Extract and match topics from conversation history."""
        user_lower = user_input.lower()
        matched_topics = []
        
        # Check if user is referring to something mentioned before
        for entry in self.conversation_history[-10:]:  # Check last 10 messages
            prev_user_msg = entry['user'].lower()
            prev_bot_msg = entry['bot'].lower()
            
            # Extract key nouns and topics from previous messages
            # Simple keyword matching for now
            prev_words = set(prev_user_msg.split() + prev_bot_msg.split())
            current_words = set(user_lower.split())
            
            # Find common meaningful words (excluding common words)
            common_words = prev_words.intersection(current_words)
            stop_words = {'i', 'am', 'is', 'the', 'a', 'an', 'and', 'or', 'but', 'to', 'for', 'of', 'in', 'on', 'at', 'by', 'it', 'this', 'that', 'what', 'how', 'why', 'when', 'where', 'who'}
            meaningful_common = common_words - stop_words
            
            if meaningful_common:
                matched_topics.append({
                    'keywords': list(meaningful_common),
                    'previous_message': entry['user'],
                    'context': entry
                })
        
        return matched_topics
    
    def _find_relevant_context(self, user_input):
        """Find relevant context from conversation history based on current input."""
        user_lower = user_input.lower()
        context = self._get_conversation_context(lookback=8)
        
        relevant_info = {
            'recent_topics': [],
            'mentioned_before': [],
            'user_info_mentioned': []
        }
        
        # Check for references to previous topics
        for entry in context:
            prev_msg = entry['user'].lower()
            
            # Check if user is asking about something mentioned before
            if any(word in user_lower for word in prev_msg.split() if len(word) > 3):
                relevant_info['mentioned_before'].append(entry)
            
            # Extract topics from previous messages
            if len(prev_msg.split()) > 3:
                # Simple topic extraction - get key nouns
                words = [w for w in prev_msg.split() if w not in ['i', 'am', 'is', 'the', 'a', 'an', 'and', 'or', 'but', 'to', 'for', 'of', 'in', 'on', 'at', 'by']]
                if words:
                    relevant_info['recent_topics'].extend(words[:3])
        
        return relevant_info
    
    def _build_contextual_response(self, user_input, keywords, relevant_context):
        """Build a response that references previous conversation only when necessary."""
        user_lower = user_input.lower()
        user_name = self.user_info.get('name', '')
        name_prefix = f"{user_name}, " if user_name else ""
        
        # Only reference previous conversation for explicit follow-up questions with pronouns
        # Don't constantly repeat what was said before
        if keywords['is_question'] and any(pronoun in user_lower for pronoun in ['it', 'that', 'this', 'they']):
            # User is asking a follow-up question - acknowledge naturally without repeating
            return f"{name_prefix}I'd be happy to help with that. Could you clarify what specifically you'd like to know?"
        
        return None
    
    def _extract_and_store_info(self, user_input):
        """Extract and store important information from user input."""
        user_lower = user_input.lower()
        
        # Extract and store facts (simple pattern matching)
        # Store preferences, facts, etc.
        if 'i like' in user_lower or 'i love' in user_lower:
            # Extract what they like
            match = re.search(r'i (like|love) (.+?)(?:\.|$|,|and)', user_lower)
            if match:
                item = match.group(2).strip()
                if 'likes' not in self.conversation_memory:
                    self.conversation_memory['likes'] = []
                if item not in self.conversation_memory['likes']:
                    self.conversation_memory['likes'].append(item)
        
        if 'i am' in user_lower or "i'm" in user_lower:
            # Extract characteristics
            match = re.search(r"i (am|'m) (.+?)(?:\.|$|,|and)", user_lower)
            if match:
                char = match.group(2).strip()
                if char not in ['feeling', 'doing', 'going', 'here', 'there', 'sorry', 'fine', 'good', 'bad']:
                    if 'characteristics' not in self.conversation_memory:
                        self.conversation_memory['characteristics'] = []
                    if char not in self.conversation_memory['characteristics']:
                        self.conversation_memory['characteristics'].append(char)
        
        # Store topics discussed
        if len(user_input.split()) > 2:
            # Extract key nouns as topics
            words = [w for w in user_input.split() if w.lower() not in ['i', 'am', 'is', 'the', 'a', 'an', 'and', 'or', 'but', 'to', 'for', 'of', 'in', 'on', 'at', 'by']]
            if words:
                topic = ' '.join(words[:3])
                if topic not in self.discussed_topics:
                    self.discussed_topics.append(topic)
    
    def _generate_contextual_response(self, user_input, keywords):
        """Generate a ChatGPT-like response that actually addresses what the user said."""
        user_lower = user_input.lower().strip()
        user_name = self.user_info.get('name', '')
        name_prefix = f"{user_name}, " if user_name else ""
        
        # Extract and store information from current input
        self._extract_and_store_info(user_input)
        
        # Get relevant context from conversation history
        relevant_context = self._find_relevant_context(user_input)
        
        # Try to build contextual response first
        contextual_response = self._build_contextual_response(user_input, keywords, relevant_context)
        if contextual_response:
            return contextual_response
        
        # 0.1. Handle greetings FIRST (before everything else to avoid conflicts)
        if keywords['is_greeting']:
            self.greeting_count += 1
            # Determine time of day for appropriate greeting
            now = datetime.now()
            hour = now.hour
            if 5 <= hour < 12:
                time_greeting = "Good morning"
            elif 12 <= hour < 17:
                time_greeting = "Good afternoon"
            elif 17 <= hour < 21:
                time_greeting = "Good evening"
            else:
                time_greeting = "Hello"
            
            if self.greeting_count == 1:
                return f"{time_greeting}! I'm a sentiment analysis chatbot. I can chat with you, answer questions, tell you the time, do calculations, and analyze emotions in your messages. How can I help you today?"
            else:
                return f"{name_prefix}{time_greeting}! Nice to see you again. What would you like to talk about?"
        
        # 0.3. Handle profanity and offensive language (after greetings)
        if keywords['is_profanity'] or keywords['is_offensive']:
            # Check if it's directed at the bot or just general profanity
            directed_at_bot = any(phrase in user_lower for phrase in ['fuck you', 'fuck off', 'you', 'your', 'screw you', 'shut up'])
            
            if directed_at_bot or keywords['is_offensive']:
                # Professional response to offensive language directed at bot
                return f"{name_prefix}I understand you might be frustrated. I'm here to help, not to upset you. Is there something specific that's bothering you? I'd like to assist you in a more constructive way."
            else:
                # General profanity - acknowledge but redirect
                return f"{name_prefix}I can sense you're feeling strongly about something. Would you like to talk about what's on your mind? I'm here to listen and help if I can."
        
        # 0.4. Handle positive feedback FIRST (before complaints to catch positive comments)
        if keywords['is_positive_feedback']:
            return f"{name_prefix}Thank you so much! That really means a lot to me. I'm glad I could help and that you're having a positive experience. Is there anything else you'd like to talk about or ask?"
        
        # 0.5. Handle complaints and criticism (but only if it's actually negative)
        if keywords['is_complaint'] or keywords['is_criticism']:
            # Check if it's specifically about the service/bot
            service_keywords = ['service', 'bot', 'chatbot', 'you', 'this']
            is_about_service = any(keyword in user_lower for keyword in service_keywords)
            
            # Make sure it's actually negative - check for negative words
            has_negative_word = any(word in user_lower for word in ['bad', 'terrible', 'awful', 'horrible', 'worst', 'disappoint', 'suck', 'not helpful', 'not working', 'does not work', "doesn't work"])
            
            if (is_about_service or keywords['is_criticism']) and has_negative_word:
                # Genuine response to service criticism
                return f"{name_prefix}I'm truly sorry to hear that you're disappointed with my service. Your feedback is important to me, and I want to help improve your experience. Could you tell me specifically what's not working well for you? I'd like to understand better so I can assist you more effectively."
            # If it's a general complaint (not about service), let it fall through to feeling handler
        
        # 1. Handle emotional statements (before name extraction to avoid conflicts)
        if keywords['feeling']:
            feeling = keywords['feeling']
            
            if feeling in ['happy', 'excited', 'great', 'wonderful', 'amazing', 'grateful', 'proud', 'relieved']:
                return f"{name_prefix}That's wonderful that you're feeling {feeling}! I'm glad to hear that. What's making you feel this way? I'd love to hear more."
            elif feeling in ['sad', 'unhappy', 'depressed', 'down', 'disappointed']:
                return f"{name_prefix}I'm sorry to hear you're feeling {feeling}. That must be difficult. Would you like to talk about what's causing these feelings? I'm here to listen."
            elif feeling in ['worried', 'anxious', 'stressed', 'frustrated']:
                return f"{name_prefix}It sounds like you're feeling {feeling}. That can be really challenging. What's on your mind? I'm here to listen and help if I can."
            elif feeling in ['tired', 'confused']:
                return f"{name_prefix}I understand feeling {feeling}. Sometimes it helps to talk things through. What's going on? I'm here to help."
        
        # 2. Handle name extraction and storage (only if no feeling was detected)
        if keywords['name']:
            self.user_info['name'] = keywords['name']
            return f"Nice to meet you, {keywords['name']}! I'll remember that. How are you doing today?"
        
        # 3. Handle time/date questions - ACTUALLY ANSWER THEM
        if keywords['needs_time'] or keywords['needs_date']:
            return self._handle_time_question(user_input)
        
        # 4. Handle calculations - ACTUALLY CALCULATE
        if keywords['needs_calc']:
            calc_result = self._handle_calculation(user_input)
            if calc_result:
                return calc_result
        
        # 5. Handle apologies - SAY SORRY BACK (like ChatGPT)
        if keywords['is_apology']:
            if 'sorry' in user_lower:
                return f"{name_prefix}No worries at all! There's nothing to apologize for. What's on your mind?"
            return f"{name_prefix}That's okay, no need to apologize. How can I help you?"
        
        # 6. Handle birthdays and special events
        if keywords['is_birthday']:
            # Extract age if mentioned
            age_match = re.search(r'(\d+)\s*(?:years?\s*old|turning)', user_lower)
            age_text = ""
            if age_match:
                age = age_match.group(1)
                # Determine ordinal suffix
                if age.endswith('1') and age != '11':
                    suffix = 'st'
                elif age.endswith('2') and age != '12':
                    suffix = 'nd'
                elif age.endswith('3') and age != '13':
                    suffix = 'rd'
                else:
                    suffix = 'th'
                age_text = f" Happy {age}{suffix} birthday!"
            
            return f"{name_prefix}Happy Birthday! 🎉🎂🎈 That's wonderful!{age_text} I hope you have an amazing day filled with joy and celebration. How are you planning to celebrate? I'd love to hear about it!"
        
        if keywords['is_special_event']:
            if 'anniversary' in user_lower:
                return f"{name_prefix}Congratulations on your anniversary! 🎉 That's a special milestone. How long have you been celebrating? I'd love to hear about it!"
            elif 'graduation' in user_lower:
                return f"{name_prefix}Congratulations on your graduation! 🎓 That's a huge achievement! What did you study? I'm so happy for you!"
            elif 'wedding' in user_lower or 'engaged' in user_lower:
                return f"{name_prefix}Congratulations! 💍 That's such exciting news! Whether it's a wedding or engagement, that's a beautiful milestone. Tell me more about it!"
            elif 'promotion' in user_lower or 'new job' in user_lower:
                return f"{name_prefix}Congratulations on your promotion/new job! 🎉 That's fantastic news! I'm so happy for you. How are you feeling about it?"
            else:
                return f"{name_prefix}That's wonderful news! Congratulations! 🎉 I'm so happy for you. Tell me more about it!"
        
        # 7. Handle goodbyes
        if keywords['is_goodbye']:
            return f"{name_prefix}Goodbye! It was nice talking with you. Take care!"
        
        # 8. Handle thanks
        if keywords['is_thanks']:
            return f"{name_prefix}You're very welcome! I'm glad I could help. Is there anything else you'd like to know?"
        
        # 8.5. Handle reciprocal questions like "and you?", "what about you?" - CHECK BEFORE QUESTIONS
        if keywords['is_reciprocal_question']:
            # Check if user mentioned they're doing well/good/fine
            if any(word in user_lower for word in ['good', 'great', 'fine', 'well', 'okay', 'ok', 'alright', 'excellent', 'wonderful', 'amazing', 'doing well', 'doing good']):
                return f"{name_prefix}That's great to hear! I'm doing well, thank you for asking! I'm here and ready to help. Is there anything you'd like to talk about or ask?"
            else:
                # User asked "and you?" but didn't mention their status
                return f"{name_prefix}I'm doing great, thank you for asking! I'm here and ready to help. How are you doing today?"
        
        # 8.6. Handle comparative statements and experience feedback
        if keywords['is_comparison'] or keywords['is_experience_feedback']:
            # Check if it's a positive comparison (better) or negative (worse)
            is_positive_comparison = any(word in user_lower for word in ['better', 'improved', 'good', 'great', 'excellent'])
            is_negative_comparison = any(word in user_lower for word in ['worse', 'declined', 'not as good', 'bad', 'terrible'])
            
            if keywords['is_experience_feedback']:
                if is_positive_comparison:
                    return f"{name_prefix}I'm glad to hear that your previous experience was positive! I appreciate you sharing that. Is there something specific from that experience that you'd like me to help recreate or improve upon?"
                elif is_negative_comparison:
                    return f"{name_prefix}I understand your concern about the experience. I'm sorry if things haven't been as good as before. Could you tell me more about what made the previous experience better? I'd like to learn from that and improve."
                else:
                    # Neutral experience feedback
                    return f"{name_prefix}Thank you for sharing your experience. I'd like to understand better - what aspects of the experience would you like to discuss? I'm here to help improve things."
            elif keywords['is_comparison']:
                if is_positive_comparison:
                    return f"{name_prefix}That's great to hear! I'm glad things are better now. What specifically made it better? I'd love to understand what's working well."
                elif is_negative_comparison:
                    return f"{name_prefix}I understand your concern. I'm sorry things aren't as good as they were. Could you tell me more about what changed or what's different now? I'd like to help improve the situation."
                else:
                    return f"{name_prefix}I see you're making a comparison. Could you tell me more about what you're comparing? I'd like to understand better so I can help."
        
        # 9. Handle questions - ANSWER THEM PROPERLY WITH CONTEXT
        if keywords['is_question']:
            # Check for follow-up questions (using "it", "that", "this", etc.)
            # Only acknowledge naturally without repeating previous messages
            if any(pronoun in user_lower for pronoun in ['it', 'that', 'this', 'they', 'them']):
                return f"{name_prefix}I'd be happy to help with that. Could you clarify what specifically you'd like to know?"
            
            # What questions
            if 'what' in user_lower:
                if 'what time' in user_lower or "what's the time" in user_lower:
                    return self._handle_time_question(user_input)
                elif 'what date' in user_lower or "what's the date" in user_lower:
                    return self._handle_time_question(user_input)
                elif 'what is' in user_lower or "what's" in user_lower:
                    # Extract the topic
                    topic = re.sub(r"what is|what's", "", user_lower).strip(' ?')
                    
                    if 'sentiment' in topic or 'feeling' in topic:
                        return f"{name_prefix}Sentiment analysis is a technique that identifies and extracts emotional tone from text. I use VADER (Valence Aware Dictionary and sEntiment Reasoner) to analyze whether messages are positive, negative, or neutral. It's quite fascinating!"
                    elif 'your name' in topic or 'you called' in topic:
                        return f"{name_prefix}I'm a sentiment analysis chatbot! I help analyze emotions in conversations and can answer various questions. What would you like to know?"
                    elif topic:
                        return f"{name_prefix}You're asking about '{topic}'. That's interesting! Could you tell me more specifically what you'd like to know about it?"
                    else:
                        return f"{name_prefix}I'm here to help! Could you be more specific about what you'd like to know?"
                elif 'what do you' in user_lower or 'what can you' in user_lower:
                    return f"{name_prefix}I'm a sentiment analysis chatbot. I can: analyze emotions in your messages, answer questions, tell you the current time and date, perform calculations, have conversations, and track mood trends. What would you like to try?"
                else:
                    # Reference what they asked
                    return f"{name_prefix}You asked: '{user_input}'. Could you rephrase that or provide more context? I'd like to give you a better answer."
            
            # Who questions
            elif 'who' in user_lower:
                if 'who are you' in user_lower:
                    return f"{name_prefix}I'm a sentiment analysis chatbot designed to understand emotions in conversations. I use VADER to analyze sentiment and can help with various questions. How can I assist you?"
                elif 'who is' in user_lower or "who's" in user_lower:
                    person = re.sub(r"who is|who's", "", user_lower).strip(' ?')
                    if person:
                        return f"{name_prefix}You're asking about '{person}'. I don't have specific information about individuals, but I'm here to chat and help with other questions!"
                    return f"{name_prefix}Could you tell me who specifically you're asking about?"
                else:
                    return f"{name_prefix}Could you clarify your 'who' question? I'd like to help you better."
            
            # How questions
            elif 'how' in user_lower:
                if 'how are you' in user_lower:
                    return f"{name_prefix}I'm doing great, thank you for asking! I'm here and ready to help. How are you doing today?"
                elif 'how does' in user_lower or 'how do' in user_lower:
                    if 'sentiment' in user_lower or 'work' in user_lower:
                        return f"{name_prefix}Sentiment analysis works by analyzing words, phrases, and their emotional context. I use VADER, which examines text for positive/negative words, punctuation, capitalization, and other linguistic cues to determine emotional tone. It's quite sophisticated!"
                    else:
                        topic = re.sub(r"how does|how do", "", user_lower).strip(' ?')
                        if topic:
                            return f"{name_prefix}You're asking how '{topic}' works. That's a good question! Could you provide more context so I can give you a better explanation?"
                        return f"{name_prefix}I'd be happy to explain! What specifically would you like to know how it works?"
                else:
                    return f"{name_prefix}I'd be happy to help explain. Could you provide more details about what you're asking?"
            
            # Why questions
            elif 'why' in user_lower:
                topic = re.sub(r"why", "", user_lower).strip(' ?')
                if topic:
                    return f"{name_prefix}You're asking why '{topic}'. That's a thoughtful question! Could you provide more context so I can give you a meaningful answer?"
                return f"{name_prefix}That's an interesting 'why' question. Could you tell me more about what specifically you're wondering about?"
            
            # Where questions
            elif 'where' in user_lower:
                location = re.sub(r"where", "", user_lower).strip(' ?')
                if location:
                    return f"{name_prefix}You're asking about where '{location}'. I don't have specific location information, but I'm here to help with other questions!"
                return f"{name_prefix}Could you clarify what location you're asking about?"
            
            # When questions
            elif 'when' in user_lower:
                if 'when' in user_lower and ('time' in user_lower or 'now' in user_lower):
                    return self._handle_time_question(user_input)
                event = re.sub(r"when", "", user_lower).strip(' ?')
                if event:
                    return f"{name_prefix}You're asking when '{event}'. I don't have specific timing information, but I can tell you the current time and date if that helps!"
                return f"{name_prefix}Could you clarify what you're asking about the timing of?"
        
        # 10. Handle statements - RESPOND NATURALLY WITHOUT CONSTANT REPETITION
        # Only reference previous context when user explicitly uses pronouns or asks follow-up questions
        context = self._get_conversation_context()
        
        # Only check for explicit references (pronouns like "it", "that", "this" referring to previous topic)
        if context and any(pronoun in user_lower for pronoun in ['it', 'that', 'this', 'they', 'them']) and len(user_input.split()) <= 5:
            # User is likely referring to something specific from previous conversation
            # But don't repeat the whole previous message, just acknowledge naturally
            return f"{name_prefix}I understand. Can you tell me more about that?"
        
        # If user said something specific, acknowledge it naturally without repeating
        if len(user_input.split()) > 2:
            # Extract key phrases from what they said
            meaningful_words = [w for w in user_input.split() if w.lower() not in ['i', 'am', 'is', 'the', 'a', 'an', 'and', 'or', 'but', 'to', 'for', 'of', 'in', 'on', 'at', 'by']]
            if meaningful_words:
                # Just acknowledge naturally without repeating everything
                return f"{name_prefix}I understand. That's interesting! Can you tell me more about that? How does that make you feel or what would you like to know about it?"
        
        # 11. Default - engage naturally
        responses = [
            f"{name_prefix}I see. That's interesting. Can you tell me more about that?",
            f"{name_prefix}I understand. How does that make you feel?",
            f"{name_prefix}Thank you for sharing that. What else is on your mind?",
            f"{name_prefix}I'm listening. Please continue, I'd like to hear more.",
            f"{name_prefix}That's helpful to know. Is there something specific you'd like to discuss or ask about?"
        ]
        
        response_index = hash(user_input) % len(responses)
        return responses[response_index]
    
    def generate_response(self, user_input):
        """Generate a contextual response based on user input."""
        keywords = self._extract_keywords(user_input)
        return self._generate_contextual_response(user_input, keywords)
    
    def run(self):
        """Main conversation loop."""
        print("\n" + "="*60)
        print("Welcome to the Sentiment Analysis Chatbot!")
        print("="*60)
        print("Type 'exit' to end the conversation and see sentiment analysis.")
        print("="*60 + "\n")
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Check for exit command
                if user_input.lower() == 'exit':
                    break
                
                # Skip empty inputs
                if not user_input:
                    continue
                
                # Clean input
                user_input = clean_input(user_input)
                
                # Analyze sentiment for this message
                message_sentiment = analyze_message(user_input)
                
                # Generate bot response
                bot_response = self.generate_response(user_input)
                
                # Store conversation entry
                conversation_entry = {
                    "user": user_input,
                    "bot": bot_response,
                    "sentiment": message_sentiment
                }
                self.conversation_history.append(conversation_entry)
                
                # Display bot response
                if self.tier2_enabled:
                    # Tier 2: Show sentiment with each message
                    sentiment_emoji = {
                        "Positive": "😊",
                        "Negative": "😔",
                        "Neutral": "😐"
                    }
                    emoji = sentiment_emoji.get(message_sentiment, "😐")
                    print(f"Bot: {bot_response} [{message_sentiment} {emoji}]")
                else:
                    print(f"Bot: {bot_response}")
                
                print()  # Empty line for readability
            
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Exiting...")
                break
            except EOFError:
                print("\n\nEnd of input. Exiting...")
                break
            except Exception as e:
                print(f"\nError: {e}")
                continue
        
        # Generate and display final summary
        self._display_final_summary()
    
    def _display_final_summary(self):
        """Display final conversation summary with sentiment analysis."""
        if not self.conversation_history:
            print("\nNo conversation to analyze. Goodbye!\n")
            return
        
        # Extract all user messages
        all_user_messages = [entry["user"] for entry in self.conversation_history]
        
        # Tier 1: Overall conversation sentiment
        overall_sentiment = analyze_overall(all_user_messages)
        
        # Tier 2: Mood trend (if enabled)
        mood_trend = None
        if self.tier2_enabled:
            sentiment_list = [entry["sentiment"] for entry in self.conversation_history]
            mood_trend = get_mood_trend(sentiment_list)
        
        # Format and display summary
        summary = format_conversation_summary(
            self.conversation_history,
            overall_sentiment,
            mood_trend
        )
        print(summary)
        
        # Additional summary statistics
        sentiment_counts = {}
        for entry in self.conversation_history:
            sentiment = entry["sentiment"]
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        
        print("Sentiment Distribution:")
        for sentiment, count in sentiment_counts.items():
            percentage = (count / len(self.conversation_history)) * 100
            print(f"  {sentiment}: {count} messages ({percentage:.1f}%)")
        print()


def main():
    """Entry point for the chatbot application."""
    # Enable Tier 2 by default (can be changed via command line argument)
    tier2_enabled = True
    if len(sys.argv) > 1 and sys.argv[1] == "--tier1-only":
        tier2_enabled = False
    
    chatbot = Chatbot(tier2_enabled=tier2_enabled)
    chatbot.run()


if __name__ == "__main__":
    main()

