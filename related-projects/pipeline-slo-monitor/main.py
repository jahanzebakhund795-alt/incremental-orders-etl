"""Pipeline SLO Monitor. Synthetic portfolio demonstration."""
import math

def run(data):
    runs,target = data['runs'],data['target']
    if not runs or not 0 < target < 1:
        raise ValueError('Need observations and 0 < target < 1')
    if any(r['latency_ms'] < 0 or r['completed_at'] > data['now'] for r in runs):
        raise ValueError('Invalid latency or completion time')
    good = sum(r['ok'] and r['latency_ms'] <= data['latency_limit_ms'] for r in runs)
    availability = good/len(runs)
    latencies = sorted(r['latency_ms'] for r in runs)
    successful = [r['completed_at'] for r in runs if r['ok']]
    freshness = data['now']-max(successful) if successful else None
    return {'good_event_ratio':availability,'p95_ms':latencies[math.ceil(.95*len(runs))-1],
            'error_budget_burn_rate':(1-availability)/(1-target),
            'freshness_seconds':freshness,
            'freshness_alert':freshness is None or freshness > data['freshness_limit_seconds']}



if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path(__file__).with_name('sample.json'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run(json.loads(args.input.read_text()))
    serialized = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
    if args.output:
        args.output.write_text(serialized + '\n')
    else:
        print(serialized)
