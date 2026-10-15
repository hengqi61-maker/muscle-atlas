"""Pinned upstream importer: verified offline cache, bounded recovery, atomic publish."""
import argparse
import hashlib
import http.client
import json
import pathlib
import re
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
ASSETS = {
    'anatomy.glb': {'sha256': '6e84529b60b64cc8f8d5cef665fda932e359e828b66d0c2dd44ec1bd9d0bd01f', 'blob': 'a112885444785a9dd93c5753b46ac790e6e036b3'},
    'mesh_mapping.json': {'sha256': '231a4e8c52cfeab8144e62d6a8ccbfb27ae04361b3a8d0b4f03e50668ce94596', 'blob': '6e702859c44aa0a36eb3b44d988076c48675c493'},
}
BASE_URL = 'https://johanbellander.github.io/BodyExplorer/'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def fetch(target, expected, url, attempts=3, opener=urllib.request.urlopen, sleep=time.sleep):
    """Never contact upstream for a valid cache or expose an unverified final file."""
    if target.exists() and digest(target) == expected:
        print(json.dumps({'asset': target.name, 'state': 'verified-cache', 'sha256': expected}))
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(target.name + '.part')
    for attempt in range(1, attempts + 1):
        offset = partial.stat().st_size if partial.exists() else 0
        request = urllib.request.Request(url, headers={'Accept-Encoding': 'identity'})
        if offset:
            request.add_header('Range', f'bytes={offset}-')
        try:
            with opener(request, timeout=30) as response:
                status = response.status
                content_range = response.headers.get('Content-Range', '')
                match = re.fullmatch(r'bytes (\d+)-(\d+)/(\d+)', content_range)
                resume = (offset > 0 and status == 206 and match is not None
                          and int(match[1]) == offset and int(match[2]) >= offset
                          and int(match[3]) == int(match[2]) + 1)
                if status == 206 and not resume:
                    partial.unlink(missing_ok=True)
                    raise ValueError('Untrustworthy Content-Range; next attempt starts fresh')
                if status not in (200, 206):
                    raise ValueError(f'Unexpected HTTP status {status}')
                received = 0
                expected_length = response.headers.get('Content-Length')
                with partial.open('ab' if resume else 'wb') as stream:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        stream.write(chunk)
                        received += len(chunk)
                if expected_length is not None and received != int(expected_length):
                    raise IOError('Incomplete Content-Length')
            actual = digest(partial)
            if actual != expected:
                partial.unlink(missing_ok=True)
                raise ValueError(f'SHA256 mismatch: {actual}')
            partial.replace(target)
            print(json.dumps({'asset': target.name, 'state': 'downloaded', 'attempt': attempt, 'sha256': actual}))
            return
        except (OSError, ValueError, urllib.error.URLError, http.client.HTTPException) as error:
            if isinstance(error, urllib.error.HTTPError) and error.code == 416:
                partial.unlink(missing_ok=True)
            # Log only exception class: upstream/proxy error text may contain credentials.
            print(json.dumps({'asset': target.name, 'state': 'attempt-failed', 'attempt': attempt,
                              'error': type(error).__name__, 'partial_bytes': partial.stat().st_size if partial.exists() else 0}))
            if attempt == attempts:
                raise RuntimeError(f'{target.name}: download failed after {attempts} attempts') from error
            sleep(min(2 ** (attempt - 1), 4))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--offline', action='store_true', help='verify bundled assets without network access')
    args = parser.parse_args()
    for name, metadata in ASSETS.items():
        target = ROOT / 'public/models' / name
        if args.offline and (not target.exists() or digest(target) != metadata['sha256']):
            raise SystemExit(f'{name}: offline cache missing or invalid')
        fetch(target, metadata['sha256'], BASE_URL + name)
        if name == 'mesh_mapping.json':
            mirror = ROOT / 'src/data/mesh_mapping.json'
            if not mirror.exists() or digest(mirror) != metadata['sha256']:
                temporary = mirror.with_name(mirror.name + '.tmp')
                temporary.write_bytes(target.read_bytes())
                temporary.replace(mirror)


if __name__ == '__main__':
    main()
