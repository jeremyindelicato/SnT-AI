"""
Knowledge Base Module - Manages educational financial content
Provides context from concepts, glossary, and lessons without scraping
"""
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """
    Manages the knowledge base for educational financial content.

    Provides:
    - Concept definitions (P/E ratio, volatilité, etc.)
    - Glossary terms (bid, ask, spread, etc.)
    - Trading strategies and lessons
    - Asset context information
    """

    def __init__(self, kb_path: str = None):
        """
        Initialize the knowledge base.

        Args:
            kb_path: Path to knowledge_base.json file
        """
        if kb_path is None:
            # Default path relative to backend/app/
            kb_path = Path(__file__).parent.parent / "data" / "knowledge_base.json"
        else:
            kb_path = Path(kb_path)

        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            logger.info(f"Knowledge base loaded from {kb_path}")
        except Exception as e:
            logger.error(f"Failed to load knowledge base: {e}")
            self.data = {}

    def search_concepts(self, query: str) -> List[Dict]:
        """
        Search for relevant concepts based on keywords.

        Args:
            query: User query string

        Returns:
            List of matching concepts with their definitions
        """
        query_lower = query.lower()
        concepts = self.data.get("concepts", [])
        matches = []

        for concept in concepts:
            # Check if any keyword matches
            keywords = concept.get("keywords", [])
            if any(keyword in query_lower for keyword in keywords):
                matches.append({
                    "title": concept.get("title"),
                    "short_def": concept.get("short_def"),
                    "detailed_expl": concept.get("detailed_expl"),
                    "tags": concept.get("tags", [])
                })

        logger.debug(f"Found {len(matches)} concept matches for query")
        return matches

    def search_glossary(self, query: str) -> List[Dict]:
        """
        Search glossary for matching terms.

        Args:
            query: User query string

        Returns:
            List of matching glossary entries
        """
        query_lower = query.lower()
        glossary = self.data.get("glossary", {})
        matches = []

        for term, definition in glossary.items():
            # Check if term appears in query
            if term.replace("_", " ") in query_lower or term in query_lower:
                matches.append({
                    "term": term.replace("_", " ").title(),
                    "definition": definition
                })

        logger.debug(f"Found {len(matches)} glossary matches for query")
        return matches

    def get_asset_context(self, ticker: str) -> Optional[Dict]:
        """
        Get educational context about a specific asset.

        Args:
            ticker: Ticker symbol (e.g., "AAPL", "SPY", "BTC-USD")

        Returns:
            Asset context dict or None if not found
        """
        assets = self.data.get("assets", {})
        asset = assets.get(ticker)

        if asset:
            logger.debug(f"Found asset context for {ticker}")
            return {
                "name": asset.get("name"),
                "type": asset.get("type"),
                "description": asset.get("short_description"),
                "sector": asset.get("sector"),
                "risk_profile": asset.get("risk_profile"),
                "beginner_comment": asset.get("suitable_for_beginners_comment")
            }

        logger.debug(f"No asset context found for {ticker}")
        return None

    def get_trading_strategies(self, suitable_for_beginners: bool = None) -> List[Dict]:
        """
        Get trading strategies, optionally filtered for beginners.

        Args:
            suitable_for_beginners: Filter for beginner-friendly strategies

        Returns:
            List of trading strategies
        """
        strategies = self.data.get("trading_strategies", [])

        if suitable_for_beginners is not None:
            strategies = [
                s for s in strategies
                if s.get("suitable_for_beginners") == suitable_for_beginners
            ]

        return strategies

    def build_context_message(self, query: str, ticker: Optional[str] = None) -> str:
        """
        Build a comprehensive context message from knowledge base.

        Args:
            query: User query
            ticker: Optional ticker symbol for asset-specific context

        Returns:
            Formatted context string to inject into LLM
        """
        context_parts = []

        # 1. Search for relevant concepts
        concepts = self.search_concepts(query)
        if concepts:
            context_parts.append("[CONCEPTS PERTINENTS]\n")
            for concept in concepts[:3]:  # Limit to top 3
                context_parts.append(f"• {concept['title']}: {concept['detailed_expl']}\n")

        # 2. Search glossary
        glossary_matches = self.search_glossary(query)
        if glossary_matches:
            context_parts.append("\n[DÉFINITIONS]\n")
            for match in glossary_matches[:3]:  # Limit to top 3
                context_parts.append(f"• {match['term']}: {match['definition']}\n")

        # 3. Add asset-specific context if ticker provided
        if ticker:
            asset_context = self.get_asset_context(ticker)
            if asset_context:
                context_parts.append(f"\n[CONTEXTE PÉDAGOGIQUE - {ticker}]\n")
                context_parts.append(f"Type: {asset_context['type']}\n")
                context_parts.append(f"Secteur: {asset_context['sector']}\n")
                context_parts.append(f"Profil de risque: {asset_context['risk_profile']}\n")
                context_parts.append(f"Pour débutants: {asset_context['beginner_comment']}\n")

        # 4. Add disclaimers if relevant
        if context_parts:
            disclaimers = self.data.get("disclaimers", {})
            context_parts.append("\n[RAPPELS IMPORTANTS]\n")
            context_parts.append(f"• {disclaimers.get('no_financial_advice', '')}\n")

        if not context_parts:
            return ""

        context_message = (
            "[KNOWLEDGE BASE - CONTENU PÉDAGOGIQUE]\n\n" +
            "".join(context_parts) +
            "\n\nUtilise ces informations pour enrichir ta réponse de manière pédagogique."
        )

        logger.info(f"Built knowledge base context: {len(context_message)} chars")
        return context_message

    def get_beginner_mistakes(self) -> List[str]:
        """
        Get list of common beginner mistakes.

        Returns:
            List of mistake descriptions
        """
        guides = self.data.get("beginner_guides", {})
        return guides.get("common_mistakes", [])

    def get_psychology_tips(self) -> List[Dict]:
        """
        Get psychological tips for investors.

        Returns:
            List of psychology concepts (FOMO, confirmation bias, etc.)
        """
        guides = self.data.get("beginner_guides", {})
        return guides.get("psychology", [])
