"""
Debug script to check what market types Cloudbet is actually using.
This will help us fix the moneyline filtering issue.
"""
import asyncio
import sys
from pathlib import Path
from collections import Counter

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.config_loader import load_config
from src.fetchers.cloudbet_fetcher import CloudbetFetcher


async def main():
    config = load_config("config/config.yaml")
    
    fetcher = CloudbetFetcher(
        api_key=config.apis.cloudbet.api_key,
        base_url=config.apis.cloudbet.base_url,
        timeout=config.apis.cloudbet.timeout,
        retry_attempts=config.apis.cloudbet.retry_attempts,
        retry_delay=config.apis.cloudbet.retry_delay,
        debug_api=config.debug_api
    )
    
    print("Fetching Cloudbet markets...")
    outcomes = await fetcher.fetch_all_markets()
    
    print(f"\nTotal outcomes fetched: {len(outcomes)}")
    
    # Count market types
    market_types = Counter()
    for outcome in outcomes:
        market_type = outcome.get('market_type', 'UNKNOWN')
        market_types[market_type] += 1
    
    print("\n" + "="*60)
    print("MARKET TYPES FOUND IN CLOUDBET:")
    print("="*60)
    for market_type, count in market_types.most_common():
        print(f"{market_type:30s} : {count:5d} outcomes")
    
    # Show sample basketball events
    print("\n" + "="*60)
    print("SAMPLE BASKETBALL EVENTS (first 5):")
    print("="*60)
    basketball_count = 0
    for outcome in outcomes:
        if outcome.get('sport_key') == 'basketball' and basketball_count < 5:
            print(f"\nEvent: {outcome.get('event_name')}")
            print(f"  Sport: {outcome.get('sport_key')}")
            print(f"  Market Type: {outcome.get('market_type')}")
            print(f"  Outcome: {outcome.get('outcome')}")
            print(f"  Odds: {outcome.get('odds')}")
            basketball_count += 1
    
    await fetcher.close()


if __name__ == "__main__":
    asyncio.run(main())
