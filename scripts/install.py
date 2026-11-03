#!/usr/bin/env python3
"""Install the bundled skill locally, without network calls or overwrites."""
import argparse
from pathlib import Path
import shutil
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, help='Exact new skill folder; default: ~/.agents/skills/lynette-thinking')
    args = parser.parse_args()
    source = Path(__file__).resolve().parent.parent / 'skills' / 'lynette-thinking'
    destination = (args.target or Path.home() / '.agents' / 'skills' / 'lynette-thinking').expanduser()
    if not (source / 'SKILL.md').is_file():
        parser.error('The bundled skill is missing. Run this script from a complete extracted repository.')
    if destination.exists() or destination.is_symlink():
        parser.error('Destination already exists. Review and back it up, then choose a new --target; nothing was overwritten.')
    if any(path.is_symlink() for path in source.rglob('*')):
        parser.error('Unexpected symbolic link in the package; review the source before installing.')
    destination = destination.resolve()
    try:
        destination.relative_to(source)
    except ValueError:
        pass
    else:
        parser.error('The destination must be outside the source skill folder.')
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, destination)
    except OSError as exc:
        print('Installation failed: {}. Review any partial destination before retrying.'.format(exc), file=sys.stderr)
        return 1
    print('Installed Lynette Thinking at {}'.format(destination))
    print('In Codex, ask: Use $lynette-thinking to help me decide my next step.')
    print('If it is not listed, restart Codex. Automatic selection is not guaranteed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
