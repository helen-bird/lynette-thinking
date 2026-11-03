#!/usr/bin/env python3
"""Check the distributable package, language inventory, and local links offline."""
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


def check_release_paths(files):
    excluded_directories = {
        'evaluation', 'evaluations', 'test-results', 'release-notes', 'research',
    }
    excluded_documents = re.compile(
        r'^(?:controlled-comparison|creative-reassessment|creative-transfer|'
        r'novel-comparison|persona-decision|persona-protocol|'
        r'guided-resolution-comparison|guided-resolution-transcripts|evaluation)'
        r'(?:[.-]|$)'
    )
    old_examples = re.compile(r'^(?:comparisons|current-comparisons|persona-comparisons)\.')
    for name in files:
        path = PurePosixPath(name)
        require(not excluded_directories.intersection(path.parts[:-1]),
                'Development-only directory in package: ' + name)
        require(not path.name.endswith(('-transcripts.md', '-protocol.json')),
                'Development-only record in package: ' + name)
        require(not (path.parts[0] == 'docs' and excluded_documents.match(path.name)),
                'Development-only document in package: ' + name)
        require(not ('examples' in path.parts[:-1] and old_examples.match(path.name)),
                'Retired example in package: ' + name)


def check():
    files = set()
    for path in ROOT.rglob('*'):
        relative = path.relative_to(ROOT)
        if relative.parts[0] == '.git' or '__pycache__' in relative.parts:
            continue
        require(not path.is_symlink(), 'Unexpected symlink: ' + str(relative))
        if path.is_file() and path.suffix != '.pyc':
            files.add(relative.as_posix())
    check_release_paths(files)

    language = load('LANGUAGE_PARITY.json')
    listed = []
    for field in ('paired_documents', 'visual_pairs', 'license_translation'):
        for pair in language[field]:
            require(len(pair) == 2, 'Invalid language pair')
            listed.extend(pair)
    listed.extend(language['shared_files'])
    require(len(listed) == len(set(listed)), 'Duplicate language inventory entry')
    require(set(listed) == files, 'Language inventory differs from package: ' +
            repr(sorted(set(listed) ^ files)))

    version = (ROOT / 'VERSION').read_text().strip()
    require(bool(version) and language['version'] == version,
            'Language inventory version differs')
    for name in ('CHANGELOG.md', 'CHANGELOG.en.md'):
        require(version in (ROOT / name).read_text(), 'Missing release version: ' + name)
    require(language['homepage_languages'] == {
        'default': 'en', 'english': 'README.md', 'simplified_chinese': 'README.zh-CN.md',
    }, 'Homepage language configuration differs')

    links = 0
    for name in sorted(files):
        path = ROOT / name
        require(path.suffix.lower() not in ('.mp4', '.mov', '.mp3', '.wav'),
                'Media excluded from this release: ' + name)
        if path.suffix not in ('.md', '.json', '.py', '.yaml', '.svg'):
            continue
        text = path.read_text(encoding='utf-8')
        require(not re.search(r'/[U]sers/|/[p]rivate/(?:tmp|var)/|\bsk-[A-Za-z0-9]{20}|\bgh[pousr]_[A-Za-z0-9]{15}', text),
                'Review machine path or credential-like text: ' + name)
        if path.suffix != '.md':
            continue
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', text):
            target = target.strip('<>')
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                continue
            relative, _, fragment = target.partition('#')
            dest = (path.parent / unquote(relative)).resolve() if relative else path
            require(dest == ROOT or ROOT in dest.parents, 'Link leaves package: ' + target)
            require(dest.exists(), 'Broken link in ' + name + ': ' + target)
            if fragment:
                contents = dest.read_text(encoding='utf-8')
                anchors = set(re.findall(r'<a\s+id="([^"]+)"', contents))
                used = {}
                for heading in re.findall(r'^#+ (.*)$', contents, re.M):
                    slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
                    number = used.get(slug, 0)
                    anchors.add(slug + ('-' + str(number) if number else ''))
                    used[slug] = number + 1
                require(unquote(fragment) in anchors, 'Broken anchor in ' + name + ': ' + target)
            links += 1

    return {'version': version, 'files': len(files),
            'relative_links_and_anchors': links, 'language_inventory_complete': True,
            'development_materials_excluded': True}


if __name__ == '__main__':
    try:
        print(json.dumps(check(), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError) as exc:
        raise SystemExit('Package check failed: ' + str(exc))
