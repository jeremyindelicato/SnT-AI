"""
Test script for the routing system
Tests different query types to verify scoring and routing logic
"""
import asyncio
import logging
from backend.app.agent import FinancialAgent

# Configure logging to see routing decisions
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)

async def test_queries():
    """Test different query types"""

    agent = FinancialAgent()

    test_cases = [
        ("Quel est le prix d'Apple ?", "scraping"),
        ("C'est quoi un ratio P/E ?", "knowledge"),
        ("Bonjour, comment ça va ?", "conversational"),
        ("Apple est-elle chère ? Explique-moi le P/E", "hybrid"),
        ("Comment va LVMH aujourd'hui ?", "scraping"),
        ("Explique-moi la différence entre une action et un ETF", "knowledge"),
        ("Le Bitcoin est-il un bon investissement ?", "hybrid"),
        ("Merci pour ton aide", "conversational"),
        ("Quelle est la performance du CAC 40 ?", "scraping"),
        ("Qu'est-ce que la diversification ?", "knowledge"),
    ]

    print("\n" + "="*80)
    print("🧪 TEST DU SYSTÈME DE ROUTING")
    print("="*80 + "\n")

    for i, (query, expected_route) in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}/10: {query}")
        print(f"Expected route: {expected_route.upper()}")
        print(f"{'='*80}\n")

        result = await agent.chat(query)

        if result["success"]:
            routing_info = result.get("routing", {})
            actual_route = routing_info.get("strategy", "unknown")
            sources = routing_info.get("sources_used", [])
            scores = routing_info.get("scores", {})

            print(f"\n✅ Actual route: {actual_route.upper()}")
            print(f"📊 Scores: {scores}")
            print(f"📋 Sources: {', '.join(sources)}")
            print(f"💬 Response preview: {result['response'][:200]}...")

            # Check if route matches expectation
            match = "✓" if actual_route == expected_route else "✗"
            print(f"\n{match} Route match: {actual_route == expected_route}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")

        # Reset conversation for next test
        agent.reset_conversation()

        # Small delay between tests
        await asyncio.sleep(1)

    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED")
    print("="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(test_queries())
