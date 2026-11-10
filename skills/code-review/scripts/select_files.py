from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from typing import NoReturn

CODE_EXTENSIONS = {
    '.astro',
    '.cjs',
    '.css',
    '.cts',
    '.js',
    '.jsx',
    '.mjs',
    '.mts',
    '.prisma',
    '.py',
    '.sh',
    '.sql',
    '.svelte',
    '.ts',
    '.tsx',
    '.vue',
}

TEST_DIRECTORY_NAMES = {'__mocks__', '__tests__', 'e2e', 'test', 'testing', 'tests'}

TEST_FILE_MARKERS = ['.spec.', '.test.']

STORY_FILE_MARKER = '.stories.'

GENERATED_ATTRIBUTE = 'linguist-generated'

EXCLUSION_REASONS = ['tests', 'stories', 'generated']

BASE_FLAG = '--base'

USAGE = f'Usage: python3 {sys.argv[0]} <path>... | {BASE_FLAG} <ref> [<path>...]'


@dataclass
class Selection:
    header: dict[str, str]
    listed_files: list[str]
    named_paths: list[str]


@dataclass
class Exclusion:
    reason: str
    # The outermost path the exclusion covers: naming it, or a path inside it, keeps the file.
    root: str


# ==========
# Selection
# ==========


def fail(message: str) -> NoReturn:
    sys.exit(message)


def run_git(args: list[str], cwd: str, stdin: str | None = None) -> str:
    return subprocess.run(
        ['git', *args], check=True, cwd=cwd, encoding='utf-8', input=stdin, stdout=subprocess.PIPE
    ).stdout


def list_git_paths(args: list[str], cwd: str) -> list[str]:
    return [entry for entry in run_git(args, cwd).split('\0') if entry]


def resolve_commit(ref: str, root: str) -> str:
    try:
        return run_git(['rev-parse', '--verify', '--quiet', f'{ref}^{{commit}}'], root).strip()
    except subprocess.CalledProcessError:
        fail(f'{ref} is not a git ref. {USAGE}')


def parse_args(args: list[str]) -> tuple[str | None, list[str]]:
    if args[:1] != [BASE_FLAG]:
        return None, args
    if len(args) < 2:
        fail(USAGE)
    return args[1], args[2:]


def resolve_selection(args: list[str], root: str) -> Selection:
    base_ref, paths = parse_args(args)
    if base_ref is None and not paths:
        fail(USAGE)
    missing_paths = [path for path in paths if not os.path.exists(path)]
    if missing_paths:
        fail(f'Not on disk: {", ".join(missing_paths)}. {USAGE}')
    named_paths = [os.path.relpath(os.path.abspath(path), root) for path in paths]
    if base_ref is None:
        git_args = ['ls-files', '-z', '--cached', '--others', '--exclude-standard', '--full-name', '--', *paths]
        return Selection(
            header={'mode': 'paths'},
            # `--cached` still lists tracked files deleted from the working tree.
            listed_files=[file for file in list_git_paths(git_args, os.getcwd()) if os.path.exists(os.path.join(root, file))],
            named_paths=named_paths,
        )
    base = run_git(['merge-base', resolve_commit(base_ref, root), 'HEAD'], root).strip()
    return Selection(
        header={'base': base, 'mode': 'ref'},
        listed_files=[
            *list_git_paths(['diff', '-z', '--name-only', '--diff-filter=d', base, '--', *named_paths], root),
            *list_git_paths(['ls-files', '-z', '--others', '--exclude-standard', '--', *named_paths], root),
        ],
        named_paths=named_paths,
    )


# ==========
# Exclusion
# ==========


def list_generated_files(files: list[str], root: str) -> set[str]:
    if not files:
        return set()
    stdin = ''.join(f'{file}\0' for file in files)
    # With `-z`, each file yields three fields: its path, the attribute and the attribute's value.
    fields = run_git(['check-attr', '-z', '--stdin', GENERATED_ATTRIBUTE], root, stdin).split('\0')
    return {path for path, value in zip(fields[0::3], fields[2::3]) if value in {'set', 'true'}}


def find_exclusion(file: str, generated_files: set[str]) -> Exclusion | None:
    segments = file.split('/')
    for index, segment in enumerate(segments[:-1]):
        if segment in TEST_DIRECTORY_NAMES:
            return Exclusion(reason='tests', root='/'.join(segments[: index + 1]))
    if any(marker in segments[-1] for marker in TEST_FILE_MARKERS):
        return Exclusion(reason='tests', root=file)
    if STORY_FILE_MARKER in segments[-1]:
        return Exclusion(reason='stories', root=file)
    if file in generated_files:
        return Exclusion(reason='generated', root=file)
    return None


def is_within(child: str, parent: str) -> bool:
    return child == parent or child.startswith(f'{parent}/')


def is_named(file: str, exclusion: Exclusion, named_paths: list[str]) -> bool:
    return any(is_within(named_path, exclusion.root) and is_within(file, named_path) for named_path in named_paths)


def count_lines(root: str, file: str) -> int:
    with open(os.path.join(root, file), 'rb') as stream:
        return stream.read().count(b'\n')


# ==========
# Output
# ==========


def main() -> None:
    root = run_git(['rev-parse', '--show-toplevel'], os.getcwd()).strip()
    selection = resolve_selection(sys.argv[1:], root)
    # A file named by its own path is a candidate whatever its extension.
    candidate_files = sorted(
        {
            file
            for file in selection.listed_files
            if os.path.splitext(file)[1] in CODE_EXTENSIONS or file in selection.named_paths
        }
    )
    generated_files = list_generated_files(candidate_files, root)
    files: list[str] = []
    excluded = {reason: 0 for reason in EXCLUSION_REASONS}
    for file in candidate_files:
        exclusion = find_exclusion(file, generated_files)
        if exclusion is None or is_named(file, exclusion, selection.named_paths):
            files.append(file)
        else:
            excluded[exclusion.reason] += 1
    output = {
        **selection.header,
        'fileCount': len(files),
        'lineCount': sum(count_lines(root, file) for file in files),
        'excluded': excluded,
        'files': files,
    }
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as error:
        # git has already printed its error.
        sys.exit(error.returncode)
