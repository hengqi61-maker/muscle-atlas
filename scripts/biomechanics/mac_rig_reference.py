"""Read frozen GLB frames/rotation tracks; never infer anatomical axes from names."""
import argparse
import hashlib
import json
import struct
import subprocess
from pathlib import Path

import numpy as np


def rotation(q):
    x, y, z, w = np.asarray(q, float) / np.linalg.norm(q)
    return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
                     [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
                     [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])


def basis_axis(rest_q, track_q):
    # glTF local = rest-local * basis; remove rest before interpreting motion.
    r = rotation(rest_q).T @ rotation(track_q)
    angle = float(np.arccos(np.clip((np.trace(r)-1)/2, -1, 1)))
    if angle < 1e-6:
        return angle, None
    axis = np.array([r[2, 1]-r[1, 2], r[0, 2]-r[2, 0], r[1, 0]-r[0, 1]])
    if np.linalg.norm(axis) < 1e-8:
        return angle, None  # pi-axis needs a different extraction; never invent it.
    return angle, (axis / np.linalg.norm(axis)).tolist()


def inspect(raw, commit, asset):
    magic, version, length = struct.unpack_from('<III', raw)
    if magic != 0x46546C67 or version != 2 or length != len(raw):
        raise ValueError('invalid GLB')
    chunks = {}; offset = 12
    while offset < len(raw):
        size, kind = struct.unpack_from('<II', raw, offset)
        chunks[kind] = raw[offset+8:offset+8+size]; offset += 8+size
    data = json.loads(chunks[0x4E4F534A]); binary = chunks[0x004E4942]

    def accessor(index):
        a = data['accessors'][index]
        if a['componentType'] != 5126 or 'sparse' in a:
            raise ValueError('only dense float32 accessor supported')
        v = data['bufferViews'][a['bufferView']]
        if v.get('buffer', 0) != 0:
            raise ValueError('external buffer unsupported')
        width = {'SCALAR': 1, 'VEC4': 4, 'MAT4': 16}[a['type']]
        start = v.get('byteOffset', 0)+a.get('byteOffset', 0)
        return np.ndarray((a['count'], width), dtype='<f4', buffer=binary,
                          offset=start, strides=(v.get('byteStride', width*4), 4)).copy()

    nodes = data['nodes']; parents = {}
    for i, n in enumerate(nodes):
        for child in n.get('children', []):
            if child in parents:
                raise ValueError('multiple parents')
            parents[child] = i
    world = {}

    def matrix(i, active=None):
        if i in world:
            return world[i]
        active = set() if active is None else active
        if i in active:
            raise ValueError('cycle')
        active.add(i); n = nodes[i]
        m = np.eye(4)
        if 'matrix' in n:
            m = np.array(n['matrix']).reshape(4, 4, order='F')
        else:
            m[:3, :3] = rotation(n.get('rotation', [0, 0, 0, 1])) @ np.diag(n.get('scale', [1, 1, 1]))
            m[:3, 3] = n.get('translation', [0, 0, 0])
        world[i] = matrix(parents[i], active) @ m if i in parents else m
        active.remove(i)
        return world[i]

    skin = data['skins'][0]; joints = skin['joints']; inverse = accessor(skin['inverseBindMatrices'])
    frames = []
    for k, i in enumerate(joints):
        w = matrix(i); ib = inverse[k].reshape(4, 4, order='F')
        frames.append({'name': nodes[i]['name'], 'nodeIndex': i,
                       'parentName': nodes[parents[i]].get('name') if i in parents else None,
                       'worldDefaultColumnMajor': w.flatten(order='F').tolist(),
                       'inverseBindColumnMajor': ib.flatten(order='F').tolist(),
                       'worldDefaultTimesInverseBindResidualToIdentity': float(np.max(np.abs(w @ ib-np.eye(4)))),
                       'determinant': float(np.linalg.det(w[:3, :3]))})
    clips = []
    for clip in data.get('animations', []):
        tracks = []
        for channel in clip['channels']:
            i = channel['target']['node']; name = nodes[i].get('name', '')
            if channel['target']['path'] != 'rotation' or not any(s in name for s in ['Forearm', 'Humerus', 'Scapula', 'Clavicle']):
                continue
            sampler = clip['samplers'][channel['sampler']]
            if sampler.get('interpolation', 'LINEAR') not in ['LINEAR', 'STEP']:
                raise ValueError('unsupported rotation interpolation')
            times = accessor(sampler['input']).ravel(); values = accessor(sampler['output'])
            if len(times) != len(values) or not np.isfinite(values).all() or np.any(np.diff(times) <= 0):
                raise ValueError('invalid rotation timeline')
            samples = []
            for time, q in zip(times, values):
                angle, axis = basis_axis(nodes[i].get('rotation', [0, 0, 0, 1]), q)
                samples.append({'timeSeconds': float(time), 'basisAngleRadians': angle, 'axisInRestLocal': axis})
            tracks.append({'name': name, 'interpolation': sampler.get('interpolation', 'LINEAR'), 'samples': samples})
        clips.append({'name': clip['name'], 'tracks': tracks})
    return {'sourceCommit': commit, 'assetPath': asset, 'assetSha256': hashlib.sha256(raw).hexdigest(),
            'scriptSha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'coordinates': 'Serialized glTF model-root metres, right-handed, column-major active; no anatomical registration',
            'jointCount': len(joints), 'frames': frames, 'clips': clips,
            'limits': ['Bone frame axes are engineering bind axes, not measured anatomical joint axes',
                       'Rotation-axis sign follows principal SO(3) angle; near-zero/pi axis is null',
                       'No physiological joint limits can be inferred from sampled track extrema',
                       'OpenSim-to-Mac A/B reference transforms and landmark correspondence remain unknown']}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('commit'); p.add_argument('output', type=Path)
    args = p.parse_args(); asset = 'public/experimental/rig-v2/unified-rig-prototype.glb'
    raw = subprocess.check_output(['git', 'show', f'{args.commit}:{asset}'])
    result = inspect(raw, args.commit, asset)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n', encoding='utf-8')
