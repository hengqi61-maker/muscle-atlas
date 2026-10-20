"""Resumeable full-cycle scan of hash-locked, gzip-framed actual source triangles."""
import argparse
import collections
import gzip
import hashlib
import json
import os
import time
import uuid
from pathlib import Path

from contact_v11 import run


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def atomic_write(path, value):
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        with temporary.open('xb') as stream:
            stream.write((json.dumps(value, indent=2) + '\n').encode())
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def execute(directory, output, limit=None, partition=0, partitions=1):
    raw = (directory / 'manifest.json').read_bytes()
    manifest = json.loads(raw)
    expected = {(exercise, side, frame) for exercise, sides in [('pulldown', ['left', 'right']), ('curl', ['both'])]
                for side in sides for frame in range(121)}
    observed = [(row['exercise'], row['side'], row['frame']) for row in manifest['frames']]
    if len(observed) != len(expected) or set(observed) != expected:
        raise ValueError('full timeline missing or duplicate frame identity')
    output.mkdir(parents=True, exist_ok=True)
    code_hashes = {p.name: sha(p.read_bytes()) for p in Path(__file__).parent.glob('contact*.py')}
    code_hashes[Path(__file__).name] = sha(Path(__file__).read_bytes())
    for schema in (Path(__file__).parents[2] / 'schemas/contact').glob('packet-v*.schema.json'):
        code_hashes[schema.name] = sha(schema.read_bytes())
    results = []
    frames = [frame for i, frame in enumerate(manifest['frames']) if i % partitions == partition][:limit]
    for index, frame in enumerate(frames):
        path = directory / frame['file']
        if path.resolve().parent != directory.resolve():
            raise ValueError('frame path escaped directory')
        compressed = path.read_bytes()
        payload = gzip.decompress(compressed)
        if sha(compressed) != frame['inputSha256'] or sha(payload) != frame['payloadSha256']:
            raise ValueError('compressed/payload byte identity mismatch')
        packet = json.loads(payload)
        if (frame['file'] != f"{frame['exercise']}-{frame['side']}-{frame['frame']:03d}.json.gz"
                or abs(frame['timeSeconds'] - frame['frame'] * 4 / 120) > 1e-12
                or packet['variant'] != f"frozen-{frame['exercise']}-original-fingers"
                or packet['inputProvenance']['assetSha256'] != manifest['assets'][frame['exercise']]['sha256']
                or packet['inputProvenance']['originalAssetSha256'] != manifest['originalAssetSha256']
                or packet['inputProvenance']['producerCommit'] != manifest['producerCommit']
                or packet['timeline']['durationSeconds'] != 4):
            raise ValueError('frame/exercise/asset provenance identity mismatch')
        if len(packet['samples']) != 1 or packet['samples'][0]['timeSeconds'] != frame['timeSeconds']:
            raise ValueError('frame time identity mismatch')
        actual_sides = {hand['side'] for hand in packet['samples'][0]['hands']}
        if actual_sides != ({'left', 'right'} if frame['side'] == 'both' else {frame['side']}):
            raise ValueError('frame side identity mismatch')
        cached = output / (path.name + '.summary.json')
        if cached.exists():
            try:
                prior = json.loads(cached.read_bytes())
            except (ValueError, UnicodeError):
                prior = {}
            if (prior.get('inputSha256') == frame['inputSha256'] and prior.get('codeHashes') == code_hashes
                    and prior.get('manifestSha256') == sha(raw)
                    and all(prior.get(key) == value for key, value in frame.items())):
                results.append(prior)
                continue
        started = time.perf_counter()
        report = run(packet)
        sources = {}
        witnesses = []
        for row in report['results']:
            key = row['side'] + ':' + row['sourceId']
            value = sources.setdefault(key, {'side': row['side'], 'sourceId': row['sourceId'],
                                             'states': collections.Counter(), 'observations': collections.Counter(),
                                             'maxWitnessDepthLowerBoundM': 0., 'witness': None})
            value['states'][row['state']] += 1
            value['observations'][row['observedState']] += 1
            depth = row.get('depthLowerBoundM', 0.)
            if depth > value['maxWitnessDepthLowerBoundM']:
                value['maxWitnessDepthLowerBoundM'] = depth
                value['witness'] = row
            elif value['witness'] is None and row['classification'] != 'disjoint':
                value['witness'] = row
        for value in sources.values():
            if value['witness']:
                witnesses.append(value['witness'])
        result = {**frame, 'manifestSha256': sha(raw), 'codeHashes': code_hashes, 'sources': list(sources.values()),
                  'elapsedSeconds': time.perf_counter() - started, 'witnesses': witnesses,
                  'numerics': report['numerics'], 'scope': report['scope']}
        atomic_write(cached, result)
        results.append(result)
        print(json.dumps({'completed': index + 1, 'total': len(manifest['frames']), 'frame': frame['file'],
                          'elapsedSeconds': result['elapsedSeconds'],
                          'observations': dict(collections.Counter(r['observedState'] for r in report['results']))}), flush=True)
    counts = collections.Counter()
    for row in results:
        for source in row['sources']:
            counts.update(source['observations'])
    summary = {'schemaVersion': '1.1.0', 'manifestSha256': sha(raw), 'codeHashes': code_hashes,
               'sourceCommit': manifest['sourceCommit'], 'producerCommit': manifest['producerCommit'],
               'completeDiscreteTimeline': len(results) == len(expected),
               'framesCompleted': len(results), 'framesExpected': len(expected),
               'observationCounts': dict(counts), 'unknownSources': manifest['unknownSources'],
               'limits': ['Discrete121times per pair/exercise, not continuous collision clearance',
                          'Dumbbell nonconvex surface intersections only; volume penetration/depth unknown',
                          'Excluded original-topology mismatches are unknown, not PASS',
                          'No measured anatomical wrist/palm frame, skin or finger-bone coverage claimed'],
               'frames': results}
    name = 'scan-summary.json' if partitions == 1 else f'scan-summary-part{partition}.json'
    atomic_write(output / name, summary)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--partition', type=int, default=0)
    parser.add_argument('--partitions', type=int, default=1)
    args = parser.parse_args()
    if not 0 <= args.partition < args.partitions <= 4:
        parser.error('require 0 <= partition < partitions <= 4')
    execute(args.directory, args.output, args.limit, args.partition, args.partitions)
