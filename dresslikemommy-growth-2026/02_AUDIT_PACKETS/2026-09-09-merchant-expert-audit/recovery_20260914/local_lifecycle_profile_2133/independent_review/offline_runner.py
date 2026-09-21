"""Single offline pass: existing focused suite plus independent native cases."""
import json
import os
import socket
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

OUT = Path(__file__).resolve().parent
LOCAL = OUT.parents[2] / 'recovery_20260911/direct-feed-deployment/local_lifecycle_interim'
sys.dont_write_bytecode = True
sys.path.insert(0, str(LOCAL))
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['TMPDIR'] = str(OUT / 'tmp')
os.environ['NODE_OPTIONS'] = '--import=' + str(OUT / 'no-network.mjs')

def forbidden(*args, **kwargs):
    raise AssertionError('independent_review_network_or_credentials_forbidden')

import lifecycle as app
with patch.object(socket.socket, 'connect', forbidden), patch.object(app.Cloudflare, '__init__', forbidden):
    names = ['test_lifecycle', 'test_cohort_filter', 'test_native_release_profile', 'review_cases']
    suite = unittest.defaultTestLoader.loadTestsFromNames(names)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    receipt = {'status': 'PASS' if result.wasSuccessful() else 'FAIL', 'testsRun': result.testsRun,
               'failures': len(result.failures), 'errors': len(result.errors),
               'skipped': len(result.skipped), 'independentAdversarialCases': 8,
               'networkAllowed': False, 'privateCredentialConstructorAllowed': False,
               'realNetworkCalls': 0, 'writes': 'Review temporary directory only; FakeApi objects are in memory.'}
    (OUT / 'offline-results.json').write_text(json.dumps(receipt, indent=2) + '\n')
    sys.exit(0 if result.wasSuccessful() else 1)
