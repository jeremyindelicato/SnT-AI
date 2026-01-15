"""
Simple test script for router and knowledge base only
Tests scoring logic without running full agent
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.router import QueryRouter
from app.knowledge_base import KnowledgeBase

def test_router():
    """Test the router scoring logic"""

    router = QueryRouter()
    kb = KnowledgeBase()

    test_cases = [
        ("Quel est le prix d'Apple ?", "scraping"),
        ("C'est quoi un ratio P/E ?", "knowledge"),
        ("Bonjour, comment ça va ?", "conversational"),
        ("Apple est-elle chère ? Explique-moi le P/E", "hybrid"),
        ("Comment va LVMH aujourd'hui ?", "scraping"),
        ("Explique-moi la différence entre une action et un ETF", "knowledge"),
        ("Le Bitcoin vaut combien ?", "scraping"),
        ("Merci pour ton aide", "conversational"),
        ("Quelle est la performance du CAC 40 ?", "scraping"),
        ("Qu'est-ce que la diversification ?", "knowledge"),
    ]

    print("\n" + "="*80)
    print("🧪 TEST DU SYSTÈME DE ROUTING (Router + Knowledge Base)")
    print("="*80 + "\n")

    results = {"correct": 0, "incorrect": 0}

    for i, (query, expected_route) in enumerate(test_cases, 1):
        print(f"\nTEST {i}/10: {query}")
        print(f"Expected: {expected_route.upper()}")

        # Score the query
        scores = router.score_query(query)

        # Route the query (without ticker detection for now)
        actual_route, scores = router.route_query(query, ticker_detected=False)

        # Get description
        description = router.get_route_description(actual_route)

        print(f"Actual: {actual_route.upper()}")
        print(f"Scores: scraping={scores['scraping']:.2f}, knowledge={scores['knowledge']:.2f}, conversational={scores['conversational']:.2f}, hybrid={scores['hybrid']:.2f}")
        print(f"Description: {description}")

        # Check if matches expectation
        match = actual_route == expected_route
        results["correct" if match else "incorrect"] += 1
        print(f"Result: {'✅ PASS' if match else '❌ FAIL'}")

        # Test knowledge base search
        if actual_route in ["knowledge", "hybrid"]:
            concepts = kb.search_concepts(query)
            glossary = kb.search_glossary(query)
            print(f"KB Results: {len(concepts)} concepts, {len(glossary)} glossary terms")

    print("\n" + "="*80)
    print(f"📊 RÉSULTATS FINAUX: {results['correct']}/10 tests réussis")
    print(f"✅ Correct: {results['correct']}")
    print(f"❌ Incorrect: {results['incorrect']}")
    print("="*80 + "\n")

if __name__ == "__main__":
    test_router()
