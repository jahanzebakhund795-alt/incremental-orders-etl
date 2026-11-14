"""Dependency Aware ETL Runner. Synthetic portfolio demonstration."""
def run(data):
    tasks = data['tasks']
    for name,spec in tasks.items():
        if any(dep not in tasks for dep in spec['depends']):
            raise ValueError('Unknown dependency')
        if spec['retries'] < 0 or spec['fail_first'] < 0:
            raise ValueError('Retry configuration must be nonnegative')
    order,visiting,visited = [],set(),set()
    def visit(name):
        if name in visiting:
            raise ValueError('Cycle detected')
        if name in visited:
            return
        visiting.add(name)
        for dep in tasks[name]['depends']:
            visit(dep)
        visiting.remove(name)
        visited.add(name)
        order.append(name)
    for name in tasks:
        visit(name)
    states,attempts = {},{}
    for name in order:
        spec = tasks[name]
        if any(states[dep] != 'success' for dep in spec['depends']):
            states[name],attempts[name] = 'blocked',0
            continue
        attempts[name] = min(spec['fail_first']+1,spec['retries']+1)
        states[name] = 'success' if spec['fail_first'] <= spec['retries'] else 'failed'
    return {'order':order,'states':states,'attempts':attempts}



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
