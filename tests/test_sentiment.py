

import unittest
import sys
import os

# Add parent directory to path to import sentiment module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sentiment import SentimentAnalyzer


class TestSentimentAnalysis(unittest.TestCase):
    """Test cases for sentiment analysis."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = SentimentAnalyzer()
    
    def test_positive_sentence(self):
        """Test that a clearly positive sentence returns 'Positive'."""
        positive_sentences = [
            "I am so happy and excited!",
            "This is wonderful and amazing!",
            "I love this! It's fantastic!",
            "Great job! You did excellent work!",
            "I'm feeling great today!"
        ]
        
        for sentence in positive_sentences:
            result = self.analyzer.analyze_message(sentence)
            self.assertEqual(
                result, "Positive",
                f"Expected 'Positive' for: '{sentence}', got '{result}'"
            )
    
    def test_negative_sentence(self):
        """Test that a clearly negative sentence returns 'Negative'."""
        negative_sentences = [
            "I am so sad and depressed.",
            "This is terrible and awful!",
            "I hate this! It's horrible!",
            "Bad job! You did terrible work!",
            "I'm feeling awful today."
        ]
        
        for sentence in negative_sentences:
            result = self.analyzer.analyze_message(sentence)
            self.assertEqual(
                result, "Negative",
                f"Expected 'Negative' for: '{sentence}', got '{result}'"
            )
    
    def test_neutral_sentence(self):
        """Test that a neutral sentence returns 'Neutral'."""
        neutral_sentences = [
            "The weather is cloudy today.",
            "I went to the store.",
            "The book has 300 pages.",
            "It is 3 o'clock.",
            "The cat sat on the mat."
        ]
        
        for sentence in neutral_sentences:
            result = self.analyzer.analyze_message(sentence)
            self.assertEqual(
                result, "Neutral",
                f"Expected 'Neutral' for: '{sentence}', got '{result}'"
            )
    
    def test_empty_message(self):
        """Test that empty or whitespace-only messages return 'Neutral'."""
        empty_inputs = ["", "   ", "\n", "\t", "   \n\t   "]
        
        for empty_input in empty_inputs:
            result = self.analyzer.analyze_message(empty_input)
            self.assertEqual(
                result, "Neutral",
                f"Expected 'Neutral' for empty input, got '{result}'"
            )
    
    def test_analyze_overall(self):
        """Test overall sentiment analysis of multiple messages."""
        # Test with positive messages
        positive_messages = [
            "I'm feeling great!",
            "This is wonderful!",
            "I love it!"
        ]
        result = self.analyzer.analyze_overall(positive_messages)
        self.assertEqual(result, "Positive")
        
        # Test with negative messages
        negative_messages = [
            "I'm feeling terrible.",
            "This is awful.",
            "I hate it."
        ]
        result = self.analyzer.analyze_overall(negative_messages)
        self.assertEqual(result, "Negative")
        
        # Test with mixed messages
        mixed_messages = [
            "I'm feeling great!",
            "The weather is cloudy.",
            "I'm feeling terrible."
        ]
        result = self.analyzer.analyze_overall(mixed_messages)
        # Result could be any of the three, just check it's valid
        self.assertIn(result, ["Positive", "Negative", "Neutral"])
    
    def test_mood_trend(self):
        """Test mood trend detection."""
        # Improving trend
        improving_sentiments = ["Negative", "Neutral", "Positive", "Positive"]
        trend = self.analyzer.get_mood_trend(improving_sentiments)
        self.assertEqual(trend, "improving")
        
        # Declining trend
        declining_sentiments = ["Positive", "Neutral", "Negative", "Negative"]
        trend = self.analyzer.get_mood_trend(declining_sentiments)
        self.assertEqual(trend, "declining")
        
        # Consistent trend
        consistent_sentiments = ["Neutral", "Neutral", "Neutral", "Neutral"]
        trend = self.analyzer.get_mood_trend(consistent_sentiments)
        self.assertEqual(trend, "consistent")
        
        # Single sentiment (should return consistent)
        single_sentiment = ["Positive"]
        trend = self.analyzer.get_mood_trend(single_sentiment)
        self.assertEqual(trend, "consistent")
    
    def test_detailed_scores(self):
        """Test that detailed scores are returned correctly."""
        message = "I am very happy!"
        scores = self.analyzer.get_detailed_scores(message)
        
        # Check that all expected keys are present
        self.assertIn('compound', scores)
        self.assertIn('pos', scores)
        self.assertIn('neu', scores)
        self.assertIn('neg', scores)
        
        # Check that scores are in valid ranges
        self.assertGreaterEqual(scores['compound'], -1.0)
        self.assertLessEqual(scores['compound'], 1.0)
        self.assertGreaterEqual(scores['pos'], 0.0)
        self.assertLessEqual(scores['pos'], 1.0)
        self.assertGreaterEqual(scores['neu'], 0.0)
        self.assertLessEqual(scores['neu'], 1.0)
        self.assertGreaterEqual(scores['neg'], 0.0)
        self.assertLessEqual(scores['neg'], 1.0)


if __name__ == '__main__':
    unittest.main()

