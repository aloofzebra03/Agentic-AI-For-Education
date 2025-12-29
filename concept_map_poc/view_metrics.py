"""
Metrics Viewer
==============
Simple command-line tool to view logged metrics.

Usage:
    python view_metrics.py              # Show summary stats
    python view_metrics.py --recent 5   # Show 5 most recent runs
    python view_metrics.py --all        # Show all runs
"""

import argparse
from metrics_logger import get_summary_stats, get_recent_metrics, load_all_metrics
from datetime import datetime
import json


def print_separator():
    print("=" * 80)


def print_summary():
    """Print summary statistics"""
    print_separator()
    print("📊 METRICS SUMMARY")
    print_separator()
    
    stats = get_summary_stats()
    
    if stats.get('total_runs', 0) == 0:
        print("\n❌ No metrics data available yet.")
        print("   Run the concept map generator to create metrics.\n")
        return
    
    print(f"\n🔢 TOTAL RUNS: {stats['total_runs']}")
    print(f"   ✅ Successful: {stats['successful_runs']}")
    print(f"   ❌ Failed: {stats['failed_runs']}")
    print(f"   📈 Success Rate: {stats['success_rate']}")
    
    print(f"\n🪙 TOKEN USAGE:")
    print(f"   Total Tokens Used: {stats['tokens']['total_tokens_used']:,}")
    print(f"   ├─ Prompt Tokens: {stats['tokens']['total_prompt_tokens']:,}")
    print(f"   └─ Completion Tokens: {stats['tokens']['total_completion_tokens']:,}")
    print(f"   Average per Run: {stats['tokens']['avg_tokens_per_run']:.1f}")
    
    print(f"\n⏱️  TIMING:")
    print(f"   Average API Duration: {stats['timing']['avg_api_duration_seconds']:.3f}s")
    print(f"   Total API Time: {stats['timing']['total_api_time_seconds']:.2f}s")
    
    print(f"\n📝 OUTPUT:")
    print(f"   Average Concepts per Run: {stats['output']['avg_concepts_per_run']:.1f}")
    print(f"   Total Concepts Extracted: {stats['output']['total_concepts_extracted']}")
    
    if stats['date_range']['first_run']:
        first = datetime.fromisoformat(stats['date_range']['first_run'])
        last = datetime.fromisoformat(stats['date_range']['last_run'])
        print(f"\n📅 DATE RANGE:")
        print(f"   First Run: {first.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Last Run:  {last.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print()


def print_recent(limit=5):
    """Print recent runs"""
    print_separator()
    print(f"📋 RECENT RUNS (Last {limit})")
    print_separator()
    
    recent = get_recent_metrics(limit)
    
    if not recent:
        print("\n❌ No metrics data available yet.\n")
        return
    
    for i, run in enumerate(recent, 1):
        timestamp = datetime.fromisoformat(run['timestamp'])
        status = "✅" if run['status']['success'] else "❌"
        
        print(f"\n{i}. {status} {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Description: {run['input']['description_preview'][:80]}...")
        print(f"   Level: {run['input']['educational_level']}")
        print(f"   Tokens: {run['tokens']['total_tokens']} (prompt: {run['tokens']['prompt_tokens']}, completion: {run['tokens']['completion_tokens']})")
        print(f"   Duration: {run['timing']['total_duration_seconds']:.3f}s")
        print(f"   Output: {run['output']['concepts_count']} concepts, {run['output']['relationships_count']} relationships")
        
        if not run['status']['success']:
            print(f"   Error: {run['status']['error']}")
    
    print()


def print_all():
    """Print all runs"""
    print_separator()
    print("📋 ALL RUNS")
    print_separator()
    
    all_runs = load_all_metrics()
    
    if not all_runs:
        print("\n❌ No metrics data available yet.\n")
        return
    
    print(f"\n{'#':<4} {'Timestamp':<20} {'Status':<8} {'Tokens':<10} {'Duration':<10} {'Concepts':<10}")
    print("-" * 80)
    
    for i, run in enumerate(all_runs, 1):
        timestamp = datetime.fromisoformat(run['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        status = "✅ OK" if run['status']['success'] else "❌ FAIL"
        tokens = run['tokens']['total_tokens']
        duration = f"{run['timing']['total_duration_seconds']:.2f}s"
        concepts = run['output']['concepts_count']
        
        print(f"{i:<4} {timestamp:<20} {status:<8} {tokens:<10} {duration:<10} {concepts:<10}")
    
    print()


def print_detailed(index):
    """Print detailed view of a specific run"""
    all_runs = load_all_metrics()
    
    if not all_runs:
        print("\n❌ No metrics data available yet.\n")
        return
    
    if index < 1 or index > len(all_runs):
        print(f"\n❌ Invalid index. Valid range: 1-{len(all_runs)}\n")
        return
    
    run = all_runs[index - 1]
    
    print_separator()
    print(f"📄 DETAILED VIEW - Run #{index}")
    print_separator()
    
    print(json.dumps(run, indent=2))
    print()


def main():
    parser = argparse.ArgumentParser(description='View concept map generation metrics')
    parser.add_argument('--recent', type=int, metavar='N', help='Show N most recent runs')
    parser.add_argument('--all', action='store_true', help='Show all runs')
    parser.add_argument('--detail', type=int, metavar='INDEX', help='Show detailed view of run #INDEX')
    
    args = parser.parse_args()
    
    if args.detail:
        print_detailed(args.detail)
    elif args.all:
        print_all()
    elif args.recent:
        print_recent(args.recent)
    else:
        print_summary()


if __name__ == '__main__':
    main()
