"""Pi tool backend sharing the pipeline's search, scoring evidence, and history formats."""
import json
import os
import sys
from pathlib import Path

from . import history as H
from .searcher import as_list, check_candidates, fit, run_search
from .telem import Telem
from .tree import Tree


def call(name, args, state, telem):
    if name == 'web_search':
        return run_search(state['method'], args.get('query') or state['question'],
                          {k: v for k, v in args.items() if k != 'query'}, telem)
    if name == 'fetch_pages':
        return telem.fetch(as_list(args.get('urls'))[:5])
    if name == 'check_candidates':
        return check_candidates(state['method'], args, telem)
    if name == 'submit':
        if not isinstance(args.get('finds'), list):
            return {'error': 'submit needs a finds list'}
        state['finds'] = [item for item in args['finds'] if isinstance(item, dict)]
        state['notes'], state['finished'] = args.get('notes', ''), True
        return {'ok': True}
    directory, allowed = Path(state['run_dir']), state['allowed_nodes']
    if name == 'search_history':
        return {'cards': Tree(directory).search(args.get('query', ''), kinds=args.get('kinds'),
                                                allowed=None if allowed is None else set(allowed))}
    if name == 'read_node':
        nid = args.get('id', '')
        return {'node': Tree(directory).read(nid, state.get('as_of_round'))[:6000]
                if allowed is None or nid in allowed else 'not available'}
    if name == 'read_attempt':
        if args.get('attempt_id') not in state['attempt_ids']:
            return {'error': 'not available'}
        log = H.load_log(directory, args['attempt_id'])
        ref = log.get('referee', {})
        return {'hunt': log['hunt'], 'notes': log['notes'], 'trace': log['trace'][:40],
                'telem_calls': log['telem_calls'][:40], 'spent': log['telem_spent'],
                'conditions': {'x': log.get('x'), 'y': log.get('y')},
                'verdicts': [{k: row.get(k) for k in ('name', 'status', 'half', 'providers')} for row in ref.get('rows', [])],
                'missed_count': len(ref.get('missed', []))}
    if name == 'propose':
        if not isinstance(args.get('candidates'), list) or not any(
                isinstance(c, dict) and c.get('instructions') for c in args['candidates']):
            return {'error': 'propose needs a list of candidate methods with instructions'}
        state['proposal'], state['finished'] = args, True
        return {'ok': True}
    return {'error': f'unknown tool {name}'}


def main():
    name, args = sys.argv[1], json.load(sys.stdin) or {}
    with open(os.environ['RSIS_STATE'], 'r+', encoding='utf-8') as file:
        state = json.load(file)
        telem = Telem(state['budget'])
        telem.spent, telem.session_id = state['spent'], state['session_id']
        telem.url_text = dict(state.get('url_text', {}))
        try:
            out = call(name, args, state, telem)
        except Exception as error:
            out = {'error': str(error)[:500]}
        state['spent'], state['session_id'] = telem.spent, telem.session_id
        state['calls'] += telem.calls
        state['url_text'] = telem.url_text
        for url, providers in telem.url_providers.items():
            state['url_providers'][url] = sorted(set(state['url_providers'].get(url, [])) | providers)
        state['trace'].append({'tool': name, 'args': args if name != 'propose' else '...',
                               'summary': {k: v for k, v in out.items() if k not in
                                           ('results', 'pages', 'checks', 'cards', 'node', 'trace', 'telem_calls', 'verdicts')}})
        file.seek(0)
        file.truncate()
        json.dump(state, file)
    print(fit(out) if name in ('web_search', 'fetch_pages', 'check_candidates') else json.dumps(out, ensure_ascii=False))


if __name__ == '__main__':
    main()
