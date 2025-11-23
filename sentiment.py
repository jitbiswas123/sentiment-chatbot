
# VADER (Valence Aware Dictionary and sEntiment Reasoner) for sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    """Sentiment analyzer using VADER SentimentIntensityAnalyzer."""
    
    def __init__(self):
        # Initialize VADER analyzer (this is the actual VADER library being used)
        self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze_message(self, message):
        if not message or not message.strip():
            return "Neutral"
        
        # Get polarity scores
        scores = self.analyzer.polarity_scores(message)
        compound_score = scores['compound']
        
        # Convert compound score to sentiment label
        if compound_score >= 0.05:
            return "Positive"
        elif compound_score <= -0.05:
            return "Negative"
        else:
            return "Neutral"
    
    def analyze_overall(self, messages):
        if not messages:
            return "Neutral"
        
        # Combine all messages into a single text
        combined_text = " ".join(messages)
        
        # Analyze the combined text
        return self.analyze_message(combined_text)
    
    def get_mood_trend(self, sentiment_list):
        if len(sentiment_list) < 2:
            return "consistent"
        
        # Convert sentiments to numeric values for trend analysis
        sentiment_values = []
        for sentiment in sentiment_list:
            if sentiment == "Positive":
                sentiment_values.append(1)
            elif sentiment == "Negative":
                sentiment_values.append(-1)
            else:
                sentiment_values.append(0)
        
        # Calculate trend by comparing first half to second half
        mid_point = len(sentiment_values) // 2
        first_half_avg = sum(sentiment_values[:mid_point]) / mid_point if mid_point > 0 else 0
        second_half_avg = sum(sentiment_values[mid_point:]) / (len(sentiment_values) - mid_point) if len(sentiment_values) - mid_point > 0 else 0
        
        if second_half_avg > first_half_avg + 0.1:
            return "improving"
        elif second_half_avg < first_half_avg - 0.1:
            return "declining"
        else:
            return "consistent"
    
    def get_detailed_scores(self, message):
        if not message or not message.strip():
            return {'compound': 0.0, 'pos': 0.0, 'neu': 1.0, 'neg': 0.0}
        
        return self.analyzer.polarity_scores(message)


# Global analyzer instance (initialized once)
_analyzer = None


def get_analyzer():
    
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentAnalyzer()
    return _analyzer


def analyze_message(message):
    
    return get_analyzer().analyze_message(message)


def analyze_overall(messages):
    
    return get_analyzer().analyze_overall(messages)


def get_mood_trend(sentiment_list):
    
    return get_analyzer().get_mood_trend(sentiment_list)

