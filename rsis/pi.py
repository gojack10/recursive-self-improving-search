"""Run Pi roles through the existing Codex account router and pipeline tools."""
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

from .config import ROOT, role

CODEX_ROUTER = Path.home() / '.pi' / 'agent' / 'extensions' / 'codex-workspaces.ts'
BASE = ['pi', '--print', '--no-session', '--no-builtin-tools', '--no-extensions',
        '--no-skills', '--no-prompt-templates', '--no-context-files', '--no-mcp']


def model(role_name):
    cfg = role(role_name)
    if not cfg['model'].startswith('pi:'):
        return None
    return cfg['model'][3:] + (f":{cfg['effort']}" if cfg['effort'] else '')


def command(model, system, prompt, extensions=(), mode='text'):
    cmd = [*BASE, '--mode', mode, '--model', model, '--system-prompt', system]
    if model.startswith('openai-codex-personal/'):
        if not CODEX_ROUTER.is_file():
            raise RuntimeError('Codex personal needs the local account-router extension; use openai-codex/<model> with stock Pi')
        cmd += ['-e', str(CODEX_ROUTER)]
    for extension in extensions:
        cmd += ['-e', str(extension)]
    return [*cmd, '--', prompt]


def complete(model, system, prompt, timeout=300):
    result = subprocess.run(command(model, system, prompt), capture_output=True, text=True, timeout=timeout,
                            cwd=tempfile.gettempdir(), env={**os.environ, 'FACTORY_FLOOR': '1'})
    if result.returncode or not result.stdout.strip():
        raise RuntimeError(f"Pi {model}: {(result.stderr or result.stdout)[-500:]}")
    return result.stdout


def agent(model, system, prompt, state, tools_role, work):
    from .searcher import SEARCH_TOOL, FETCH_TOOL, CHECK_TOOL, SUBMIT_TOOL
    from .improver import HIST_TOOL, READ_TOOL, LOG_TOOL, PROPOSE_TOOL
    tools = ([SEARCH_TOOL, HIST_TOOL, READ_TOOL, LOG_TOOL, PROPOSE_TOOL] if tools_role == 'improver'
             else [SEARCH_TOOL, FETCH_TOOL, CHECK_TOOL, SUBMIT_TOOL])
    state = {'finished': False, 'url_text': {}, **state}
    work.mkdir(parents=True, exist_ok=True)
    state_file, stream = work / f"{state['id']}.state.json", work / f"{state['id']}.pi.jsonl"
    state_file.write_text(json.dumps(state), encoding='utf-8')
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='rsis-pi-') as directory:
        schemas = Path(directory) / 'tools.json'
        schemas.write_text(json.dumps([t['function'] for t in tools]), encoding='utf-8')
        env = {**os.environ, 'RSIS_STATE': str(state_file), 'RSIS_ROOT': str(ROOT),
               'RSIS_PYTHON': sys.executable, 'RSIS_TOOLS': str(schemas), 'FACTORY_FLOOR': '1'}
        with stream.open('w', encoding='utf-8') as output:
            process = subprocess.Popen(command(model, system, prompt, [ROOT / 'pi' / 'search-tools.ts'], 'json'),
                                       cwd=directory, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       encoding='utf-8', errors='replace')
            limit = threading.Timer(900, process.kill)
            limit.start()
            for line in process.stdout:
                # Each event is recorded with the time it arrived, so a saved run can be replayed at its real pace.
                output.write(f'{{"t":{time.time():.3f},{line[1:]}' if line.startswith('{"') else line)
                output.flush()
            limit.cancel()
            returncode = process.wait()
    usage, turns, errors = {'prompt_tokens': 0, 'completion_tokens': 0}, 0, []
    for line in stream.read_text(encoding='utf-8').splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            if line.strip():
                errors.append(line[-500:])
            continue
        if not isinstance(event, dict) or event.get('type') != 'turn_end':
            continue
        turns += 1
        message = event.get('message') or {}
        tokens = message.get('usage') or {}
        usage['prompt_tokens'] += tokens.get('input', 0) + tokens.get('cacheRead', 0)
        usage['completion_tokens'] += tokens.get('output', 0)
        if message.get('errorMessage'):
            errors.append(message['errorMessage'])
    state = json.loads(state_file.read_text(encoding='utf-8'))
    if returncode or not state['finished']:
        raise RuntimeError(f"Pi {model} did not finish: {'; '.join(errors[-3:]) or 'no submission'}")
    return state, {'seconds': round(time.monotonic() - started, 1), 'tokens': usage, 'model': model, 'turns': turns}
