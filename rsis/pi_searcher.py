"""Run the existing search method through Pi and return the standard search record."""
import json
import os
import uuid
from pathlib import Path

from . import pi
from .config import ATTEMPT_BUDGET, ROOT
from .searcher import prompts


def attempt(m, hunt, budget=ATTEMPT_BUDGET, model=None, work_dir=None):
    aid = uuid.uuid4().hex[:10]
    system, prompt = prompts(m, hunt, budget)
    work = Path(work_dir) if work_dir else Path(os.environ.get('RSIS_RUN_DIR', ROOT / 'runs' / 'pi-trial')) / 'logs'
    state, meta = pi.agent(model or pi.model('searcher'), system, prompt,
        {'id': aid, 'method': m, 'question': hunt['question'], 'budget': budget, 'spent': 0.0,
         'session_id': None, 'calls': [], 'url_providers': {}, 'trace': [], 'finds': [], 'notes': ''}, 'searcher', work)
    return {'attempt_id': aid, 'method': m['id'], 'hunt': hunt['name'], 'kind': hunt['kind'],
            'x': hunt['x'], 'y': hunt['y'], 'pool': hunt['pool'], 'finds': state['finds'], 'notes': state['notes'],
            'telem_calls': state['calls'], 'telem_spent': round(state['spent'], 4), 'telem_session': state['session_id'],
            'trace': state['trace'], 'url_providers': state['url_providers'], 'url_text': state['url_text'], **meta}


if __name__ == '__main__':
    import argparse
    from . import loop
    parser = argparse.ArgumentParser(prog='python -m rsis.pi_searcher')
    parser.add_argument('method')
    parser.add_argument('task')
    parser.add_argument('--model', help='Pi provider/model:effort; defaults to SEARCHER_MODEL and SEARCHER_EFFORT')
    args = parser.parse_args()
    directory = loop.run_dir('pi-trial')
    method = json.loads(Path(args.method).read_text(encoding='utf-8'))
    print(json.dumps(loop.run_and_score(directory, method, args.task, 0, 'pi-trial',
        make=lambda task: attempt(method, task, model=args.model, work_dir=directory / 'logs')), indent=1))
