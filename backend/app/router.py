"""
Router Module - Intelligent query routing with scoring system
Determines whether to use scraping, knowledge base, LLM only, or hybrid approach
"""
import logging
import json
from pathlib import Path
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


class QueryRouter:
    """
    Routes user queries to appropriate data sources based on intent scoring.

    Scoring dimensions:
    - scraping: Need for real-time market data (0.0 - 1.0)
    - knowledge: Need for educational/theoretical content (0.0 - 1.0)
    - conversational: General chat/greetings (0.0 - 1.0)
    - hybrid: Combination of scraping + knowledge (0.0 - 1.0)
    """

    def __init__(self, knowledge_base_path: str = None):
        """
        Initialize the router with knowledge base patterns.

        Args:
            knowledge_base_path: Path to knowledge_base.json file
        """
        if knowledge_base_path is None:
            # Default path relative to backend/app/
            kb_path = Path(__file__).parent.parent / "data" / "knowledge_base.json"
        else:
            kb_path = Path(knowledge_base_path)

        # Load query patterns from knowledge base
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                kb_data = json.load(f)
                self.query_patterns = kb_data.get("query_patterns", {})

            logger.info(f"Router initialized with patterns from {kb_path}")
        except Exception as e:
            logger.error(f"Failed to load knowledge base patterns: {e}")
            # Fallback patterns
            self.query_patterns = {
                "scraping_indicators": ["prix", "cours", "valeur", "combien"],
                "knowledge_indicators": ["c'est quoi", "explique", "comment"],
                "conversational_indicators": ["bonjour", "merci", "salut"]
            }

    def score_query(self, user_message: str) -> Dict[str, float]:
        """
        Score a user query across multiple dimensions.

        Args:
            user_message: The user's input message

        Returns:
            Dict with scores for each dimension:
            {
                "scraping": 0.8,
                "knowledge": 0.2,
                "conversational": 0.0,
                "hybrid": 0.5
            }
        """
        message_lower = user_message.lower()

        # Count matches for each category
        scraping_matches = sum(
            1 for indicator in self.query_patterns.get("scraping_indicators", [])
            if indicator in message_lower
        )

        knowledge_matches = sum(
            1 for indicator in self.query_patterns.get("knowledge_indicators", [])
            if indicator in message_lower
        )

        conversational_matches = sum(
            1 for indicator in self.query_patterns.get("conversational_indicators", [])
            if indicator in message_lower
        )

        # Normalize scores (cap at 1.0)
        scraping_score = min(1.0, scraping_matches * 0.3)  # Each match = 0.3
        knowledge_score = min(1.0, knowledge_matches * 0.4)  # Each match = 0.4
        conversational_score = min(1.0, conversational_matches * 0.5)  # Each match = 0.5

        # Hybrid score: high when both scraping AND knowledge indicators present
        hybrid_score = 0.0
        if scraping_matches > 0 and knowledge_matches > 0:
            hybrid_score = min(1.0, (scraping_score + knowledge_score) / 2)

        scores = {
            "scraping": scraping_score,
            "knowledge": knowledge_score,
            "conversational": conversational_score,
            "hybrid": hybrid_score
        }

        logger.debug(f"Query scores: {scores}")
        return scores

    def route_query(self, user_message: str, ticker_detected: bool = False) -> Tuple[str, Dict[str, float]]:
        """
        Determine the routing strategy based on query scoring.

        Args:
            user_message: The user's input message
            ticker_detected: Whether a ticker was detected in the message

        Returns:
            Tuple of (route_strategy, scores)
            route_strategy can be: "scraping", "knowledge", "conversational", "hybrid"
        """
        scores = self.score_query(user_message)

        # Decision logic with priorities

        # 1. If ticker detected, strongly favor scraping
        if ticker_detected:
            # Even with ticker, check if user wants explanation
            if scores["knowledge"] > 0.3:
                route = "hybrid"
                logger.info(f"Route: HYBRID (ticker={ticker_detected}, knowledge_need={scores['knowledge']:.2f})")
            else:
                route = "scraping"
                logger.info(f"Route: SCRAPING (ticker={ticker_detected})")
            return route, scores

        # 2. Conversational (greetings, thanks, etc.) - highest priority for clear signals
        if scores["conversational"] >= 0.5:
            route = "conversational"
            logger.info(f"Route: CONVERSATIONAL (score={scores['conversational']:.2f})")
            return route, scores

        # 3. Hybrid (both data and explanation needed) - check early
        if scores["hybrid"] > 0.3:
            route = "hybrid"
            logger.info(f"Route: HYBRID (score={scores['hybrid']:.2f})")
            return route, scores

        # 4. Knowledge base (educational questions) - lowered threshold
        if scores["knowledge"] >= 0.4 and scores["scraping"] < 0.3:
            route = "knowledge"
            logger.info(f"Route: KNOWLEDGE (score={scores['knowledge']:.2f})")
            return route, scores

        # 5. Scraping (data request) - lowered threshold
        if scores["scraping"] >= 0.3:
            route = "scraping"
            logger.info(f"Route: SCRAPING (score={scores['scraping']:.2f})")
            return route, scores

        # 6. If knowledge score is high but scraping also present
        if scores["knowledge"] > scores["scraping"] and scores["knowledge"] > 0.3:
            route = "knowledge"
            logger.info(f"Route: KNOWLEDGE (dominant score={scores['knowledge']:.2f})")
            return route, scores

        # 7. Default: conversational (let LLM handle)
        route = "conversational"
        logger.info(f"Route: CONVERSATIONAL (default, no strong signals)")
        return route, scores

    def get_route_description(self, route: str) -> str:
        """
        Get a human-readable description of the route strategy.

        Args:
            route: The route strategy

        Returns:
            Description string
        """
        descriptions = {
            "scraping": "📊 Données en temps réel (via scraping Yahoo Finance)",
            "knowledge": "📚 Base de connaissances (concepts financiers)",
            "conversational": "💬 Réponse conversationnelle (LLM uniquement)",
            "hybrid": "🔀 Hybride (données temps réel + explications pédagogiques)"
        }
        return descriptions.get(route, "❓ Route inconnue")
