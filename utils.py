
import re


def clean_input(text):
    
    if not text:
        return ""
    
    # Strip whitespace
    text = text.strip()
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text


def format_conversation_summary(conversation_history, overall_sentiment, mood_trend=None):
    summary_lines = []
    summary_lines.append("\n" + "="*60)
    summary_lines.append("CONVERSATION SUMMARY")
    summary_lines.append("="*60)
    summary_lines.append(f"\nTotal messages: {len(conversation_history)}")
    summary_lines.append(f"Overall sentiment: {overall_sentiment}")
    
    if mood_trend:
        summary_lines.append(f"Mood trend: {mood_trend}")
    
    summary_lines.append("\n" + "-"*60)
    summary_lines.append("Message-by-Message Sentiment (Tier 2):")
    summary_lines.append("-"*60)
    
    for i, entry in enumerate(conversation_history, 1):
        user_msg = entry.get('user', '')
        sentiment = entry.get('sentiment', 'Unknown')
        # Truncate long messages for display
        display_msg = user_msg[:50] + "..." if len(user_msg) > 50 else user_msg
        summary_lines.append(f"{i}. [{sentiment}] {display_msg}")
    
    summary_lines.append("="*60 + "\n")
    
    return "\n".join(summary_lines)

