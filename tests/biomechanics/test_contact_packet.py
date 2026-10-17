import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[2] / 'scripts/biomechanics'))
from contact_packet import run


def example():
    return json.loads((Path(__file__).parents[2] / 'research/contact/example.contact.json').read_text())


def test_example_and_handedness():
    packet = example()
    result = run(packet)
    assert result['results'][0]['classification'] == 'penetration-candidate'
    packet['samples'][0]['hands'][0]['side'] = 'right'
    assert run(packet)['results'][0]['side'] == 'right'


def test_reflection_and_bad_time_rejected():
    packet = example()
    packet['samples'][0]['prop']['worldMatrix'][0] = -1
    with pytest.raises(ValueError, match='proper rigid'):
        run(packet)
    packet = example()
    packet['samples'] *= 2
    with pytest.raises(ValueError, match='strictly increasing'):
        run(packet)


@pytest.mark.parametrize('side', ['left', 'right'])
def test_frozen_actual_source_triangle_witness(side):
    path = Path(__file__).parents[2] / f'research/contact/m2-{side}-triangle.contact.json'
    packet = json.loads(path.read_text())
    report = run(packet)
    assert report['results'][0]['classification'] == 'penetration-candidate'
    assert report['results'][0]['depthLowerBoundM'] > .022
    assert packet['samples'][0]['hands'][0]['frameStatus'] == 'unknown'
