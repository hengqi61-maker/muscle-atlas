import hashlib
import importlib.util
import io
import pathlib
import tempfile
import unittest
import urllib.error

spec = importlib.util.spec_from_file_location('fetch_models', pathlib.Path(__file__).resolve().parents[1] / 'scripts/fetch-models.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
DATA = b'verified anatomy fixture'
HASH = hashlib.sha256(DATA).hexdigest()

class Response(io.BytesIO):
    def __init__(self, data, status=200, headers=None):
        super().__init__(data)
        self.status = status
        self.headers = headers or {}

class FetchTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.target = pathlib.Path(self.directory.name) / 'asset.glb'
    def run_fetch(self, opener, attempts=3):
        module.fetch(self.target, HASH, 'https://example.invalid/asset', opener=opener, attempts=attempts, sleep=lambda _: None)
    def test_valid_cache_never_requests(self):
        self.target.write_bytes(DATA)
        self.run_fetch(lambda *a, **k: self.fail('network request on cache hit'))
    def test_resume_checks_range_and_hash(self):
        self.target.with_name('asset.glb.part').write_bytes(DATA[:4])
        def opener(request, **kwargs):
            self.assertEqual(request.get_header('Range'), 'bytes=4-')
            return Response(DATA[4:], 206, {'Content-Range': f'bytes 4-{len(DATA)-1}/{len(DATA)}'})
        self.run_fetch(opener)
        self.assertEqual(self.target.read_bytes(), DATA)
    def test_ignored_range_restarts_instead_of_appending(self):
        self.target.with_name('asset.glb.part').write_bytes(b'old')
        self.run_fetch(lambda *a, **k: Response(DATA))
        self.assertEqual(self.target.read_bytes(), DATA)
    def test_invalid_range_is_rejected_then_restarted(self):
        self.target.with_name('asset.glb.part').write_bytes(DATA[:4])
        calls = []
        def opener(request, **kwargs):
            calls.append(request.get_header('Range'))
            return Response(b'bad', 206, {'Content-Range': 'bytes 0-2/3'}) if len(calls) == 1 else Response(DATA)
        self.run_fetch(opener)
        self.assertEqual(calls, ['bytes=4-', None])
    def test_hash_failure_never_overwrites_existing(self):
        self.target.write_bytes(b'old evidence')
        with self.assertRaises(RuntimeError):
            self.run_fetch(lambda *a, **k: Response(b'corrupt'))
        self.assertEqual(self.target.read_bytes(), b'old evidence')
        self.assertFalse(self.target.with_name('asset.glb.part').exists())
    def test_interrupted_transfer_resumes_verified_partial(self):
        class Interrupted(Response):
            def read(self, size=-1):
                if self.tell() == 0:
                    return super().read(4)
                raise OSError('connection interrupted')
        calls = []
        def opener(request, **kwargs):
            calls.append(request.get_header('Range'))
            if len(calls) == 1:
                return Interrupted(DATA)
            return Response(DATA[4:], 206, {'Content-Range': f'bytes 4-{len(DATA)-1}/{len(DATA)}'})
        self.run_fetch(opener)
        self.assertEqual(calls, [None, 'bytes=4-'])
        self.assertEqual(self.target.read_bytes(), DATA)

    def test_transport_failure_has_bounded_attempts(self):
        calls = []
        def opener(*a, **k):
            calls.append(1)
            raise urllib.error.URLError('offline')
        with self.assertRaises(RuntimeError):
            self.run_fetch(opener)
        self.assertEqual(len(calls), 3)
        self.assertFalse(self.target.exists())
    def test_truncated_response_is_not_published(self):
        with self.assertRaises(RuntimeError):
            self.run_fetch(lambda *a, **k: Response(DATA[:2], headers={'Content-Length': str(len(DATA))}), attempts=1)
        self.assertFalse(self.target.exists())

if __name__ == '__main__':
    unittest.main()
