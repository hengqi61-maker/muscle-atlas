"""Additive contact-v1.1 evidence metadata; unchanged v1.0 geometric kernel."""
import argparse
import copy
import hashlib
import json
from itertools import pairwise
from pathlib import Path

import jsonschema
import numpy as np
from contact_packet import ROOT, rigid
from contact_packet import run as run_v10
from contact_surface import scan_surface


def geometry_hash(vertices, triangles):
    """Portable hash of float64 LE XYZ followed by uint32 LE triangle indices."""
    vertices = np.asarray(vertices, dtype='<f8')
    indices = np.asarray(triangles)
    if (vertices.ndim != 2 or vertices.shape[1] != 3 or not np.isfinite(vertices).all()
            or indices.ndim != 2 or indices.shape[1] != 3
            or not np.issubdtype(indices.dtype, np.integer)
            or indices.min() < 0 or indices.max() >= len(vertices)):
        raise ValueError('invalid hash geometry')
    return hashlib.sha256(vertices.tobytes() + indices.astype('<u4').tobytes()).hexdigest()


def migrate_v10(packet):
    """Preserve values; unknown provenance remains unknown, never promoted to actual."""
    run_v10(packet)
    result = copy.deepcopy(packet)
    result['schemaVersion'] = '1.1.0'
    result['inputProvenance'] = {
        'producerCommit': '0' * 40, 'assetSha256': '0' * 64,
        'originalAssetSha256': '0' * 64, 'coordinateFrame': 'legacy declared world; unverified',
        'hashSerialization': 'float64-le-xyz-then-uint32-le-triples',
        'evidenceKind': 'legacy-unverified'}
    times = [s['timeSeconds'] for s in result['samples']]
    result['timeline'] = {'clipId': 'legacy-unspecified', 'durationSeconds': max(times),
                          'expectedTimesSeconds': times, 'interpolation': 'sampled-only',
                          'scope': 'discrete-samples-not-continuous-collision'}
    for sample in result['samples']:
        prop = sample['prop']
        prop.update(geometryKind='unknown', geometrySha256=geometry_hash(prop['vertices'], prop['triangles']))
        for hand in sample['hands']:
            hand.update(independentlyExported=False, handWorldMatrix=None)
            for source in hand['sources']:
                source.update(originalTriangleIds=list(range(len(source['triangles']))),
                              geometryKind='unknown', region='unknown',
                              posedGeometrySha256=geometry_hash(source['posedWorldVertices'], source['triangles']))
    return result


def validate(packet):
    schema = json.loads((ROOT / 'schemas/contact/packet-v1.1.schema.json').read_text(encoding='utf-8'))
    jsonschema.validate(packet, schema)
    times = [s['timeSeconds'] for s in packet['samples']]
    expected = packet['timeline']['expectedTimesSeconds']
    if (times != expected or any(not np.isfinite(t) for t in times)
            or any(b <= a for a, b in pairwise(times))
            or times[-1] > packet['timeline']['durationSeconds']):
        raise ValueError('timeline mismatch/nonfinite/nonmonotonic')
    for sample in packet['samples']:
        prop = sample['prop']
        rigid(prop['worldMatrix'])
        if any(not np.isfinite(d) or d <= 0 for d in prop['dimensionsM']):
            raise ValueError('positive finite prop dimensions required')
        if geometry_hash(prop['vertices'], prop['triangles']) != prop['geometrySha256']:
            raise ValueError('prop geometry SHA256 mismatch')
        identities = set()
        for hand in sample['hands']:
            for name in ['wristWorldMatrix', 'palmWorldMatrix']:
                if hand[name] is not None:
                    rigid(hand[name])
                elif hand['frameStatus'] != 'unknown':
                    raise ValueError('missing wrist/palm frame must remain unknown')
            frame = None if hand['handWorldMatrix'] is None else rigid(hand['handWorldMatrix'])
            for source in hand['sources']:
                identity = (hand['side'], source['sourceId'])
                if identity in identities:
                    raise ValueError('duplicate side/source identity')
                identities.add(identity)
                if len(source['originalTriangleIds']) != len(source['triangles']):
                    raise ValueError('original triangle identity length mismatch')
                if geometry_hash(source['posedWorldVertices'], source['triangles']) != source['posedGeometrySha256']:
                    raise ValueError('source posed geometry SHA256 mismatch')
                if 'posedHandVertices' in source:
                    if frame is None:
                        raise ValueError('hand-local geometry needs explicit proper hand frame')
                    local = np.asarray(source['posedHandVertices'])
                    world = np.asarray(source['posedWorldVertices'])
                    if local.shape != world.shape or not np.isfinite(local).all():
                        raise ValueError('invalid hand-local geometry')
                    if not np.allclose(local @ frame[:3, :3].T + frame[:3, 3], world,
                                       rtol=0, atol=packet['toleranceM']):
                        raise ValueError('independent hand local/world geometry mismatch')


def project_v10(packet):
    result = {k: copy.deepcopy(packet[k]) for k in
              ['coordinates', 'variant', 'provenance', 'toleranceM', 'samples']}
    result['schemaVersion'] = '1.0.0'
    for sample in result['samples']:
        for key in ['geometryKind', 'geometrySha256']:
            del sample['prop'][key]
        for hand in sample['hands']:
            for key in ['independentlyExported', 'handWorldMatrix']:
                del hand[key]
            for source in hand['sources']:
                for key in ['originalTriangleIds', 'geometryKind', 'region', 'posedGeometrySha256', 'posedHandVertices']:
                    source.pop(key, None)
    return result


def run(packet):
    validate(packet)
    # Hashes and labels are verified before invoking the existing numeric kernel.
    surface = any('triangle-surface' in sample['prop']['geometryKind'] for sample in packet['samples'])
    if surface:
        legacy = {'results': [], 'scope': 'actual triangle surfaces only; volume containment and depth unknown',
                  'uncertainty': ['No enclosed-volume clearance, continuous-time or physical grasp certification']}
        for sample in packet['samples']:
            prop = sample['prop']
            transform = rigid(prop['worldMatrix'])
            for hand in sample['hands']:
                for source in hand['sources']:
                    local = (np.asarray(source['posedWorldVertices']) - transform[:3, 3]) @ transform[:3, :3]
                    for index, matches in scan_surface(local, source['triangles'], prop['vertices'],
                                                       prop['triangles'], packet['toleranceM']):
                        selected = next((m for m in matches if m['classification'] == 'surface-crossing'),
                                        matches[0] if matches else {'classification': 'disjoint'})
                        selected = dict(selected)
                        position = selected.pop('positionM', None)
                        if position is not None:
                            selected['positionWorldM'] = (transform[:3, :3] @ position + transform[:3, 3]).tolist()
                        legacy['results'].append({'timeSeconds': sample['timeSeconds'], 'side': hand['side'],
                                                  'sourceId': source['sourceId'], 'triangleIndex': index,
                                                  'propId': prop['id'], 'surfaceMatches': len(matches), **selected})
    else:
        legacy = run_v10(project_v10(packet))
    lookup = {(s['timeSeconds'], h['side'], source['sourceId']): (s['prop'], h, source)
              for s in packet['samples'] for h in s['hands'] for source in h['sources']}
    for row in legacy['results']:
        prop, hand, source = lookup[(row['timeSeconds'], row['side'], row['sourceId'])]
        row['originalTriangleId'] = source['originalTriangleIds'][row['triangleIndex']]
        row['region'] = source['region']
        row['geometryKind'] = {'prop': prop['geometryKind'], 'source': source['geometryKind']}
        actual = (prop['geometryKind'] == 'actual-convex-mesh'
                  and source['geometryKind'] == 'actual-source-triangles'
                  and hand['independentlyExported']
                  and packet['inputProvenance']['evidenceKind'] == 'actual-export')
        row['observedState'] = {'disjoint': 'separation', 'surface-contact': 'contact',
                                'penetration-candidate': 'penetration', 'surface-crossing': 'surface-crossing',
                                'unknown': 'unknown'}[row['classification']]
        row['state'] = row['observedState'] if actual else 'unknown'
        row['uncertainties'] = ([] if actual else ['proxy, legacy or non-independent evidence cannot establish actual volume contact'])
        if surface:
            row['state'] = 'unknown'
            row['uncertainties'].append('Actual surface intersection is observed separately; volume penetration/separation is unknown')
        row['signedWitnessBoundM'] = (-row['depthLowerBoundM'] if 'depthLowerBoundM' in row
                                     else row.get('gapLowerBoundM'))
        row['signedBoundDefinition'] = 'positive separating-plane lower bound; negative interior witness depth lower bound; not exact signed distance'
    legacy['schemaVersion'] = '1.1.0'
    legacy['timeline'] = packet['timeline']
    legacy['inputProvenance'] = packet['inputProvenance']
    legacy['numerics'] = {'toleranceM': packet['toleranceM'], 'arithmetic': 'IEEE754 float64',
                          'boundary': 'tolerance-expanded intersection; contact means numerical boundary band, not physical force'}
    return legacy


def read_packet(path):
    raw = path.read_bytes()
    packet = json.loads(raw)
    report = run(packet)
    report['inputSha256'] = hashlib.sha256(raw).hexdigest()
    report['inputHashMeaning'] = 'exact input file bytes; no newline normalization'
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--migrate-v10', action='store_true')
    args = parser.parse_args()
    value = (migrate_v10(json.loads(args.input.read_bytes())) if args.migrate_v10 else read_packet(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes((json.dumps(value, indent=2, allow_nan=False) + '\n').encode('utf-8'))
