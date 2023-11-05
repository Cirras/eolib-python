import argparse
import os
import re
import shutil
import keepachangelog
from pathlib import Path


def change_working_directory():
    working_dir = str(Path(__file__).parent.resolve())
    os.chdir(working_dir)


def validate_version(version):
    if not re.match(r'^\d+\.\d+\.\d+([a-z]+\d+)?$', version):
        raise RuntimeError('invalid SemVer version: expected format "major.minor.patch[label]"')


def validate_git_status():
    if shutil.which('git') is None:
        raise RuntimeError('git could not be found')
    if os.popen('git status --porcelain').read():
        raise RuntimeError('dirty working tree: commit changes and try again')


def validate_tag(tag):
    if os.popen(f'git tag -l {tag}').read():
        raise RuntimeError(f'tag {tag} already exists')


def write_about_file(version):
    with open('src/eolib/__about__.py', 'w') as about:
        about.write(f'__version__ = "{version}"\n')


def bump_changelog(version):
    keepachangelog.release('CHANGELOG.md', version)


def commit(tag):
    if (
        os.system('git add .')
        or os.system(f'git commit -m "Release {tag}"')
        or os.system(f'git tag {tag} HEAD')
    ):
        raise RuntimeError('failed to commit/tag changes')


def prepare_release(version):
    tag = f'v{version}'

    change_working_directory()

    validate_version(version)
    validate_git_status()
    validate_tag(tag)

    write_about_file(version)
    bump_changelog(version)
    commit(tag)

    print(tag)


parser = argparse.ArgumentParser(description='Prepare release')
parser.add_argument(
    'version', type=str, help='New version in SemVer format (e.g., major.minor.patch[label])'
)
version = parser.parse_args().version

try:
    prepare_release(version)
except RuntimeError as e:
    print(str(e))
    exit(1)
