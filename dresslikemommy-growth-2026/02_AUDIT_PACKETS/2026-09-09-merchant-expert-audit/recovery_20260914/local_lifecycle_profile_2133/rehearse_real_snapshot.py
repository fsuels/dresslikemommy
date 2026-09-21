"""Rehearse the current adapter against preserved real evidence, without I/O to services."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

packet = Path(__file__).resolve().parent
audit = packet.parent.parent
local = audit / 'recovery_20260911/direct-feed-deployment/local_lifecycle_interim'
historical = local / 'runs/20260914T131200Z-us-freshness'
sys.path.insert(0, str(local))
import lifecycle as app

app.select_release_profile('native-holds-20260914')
app.verify_freeze()
with tempfile.TemporaryDirectory(prefix='dlm-merchant-offline-rehearsal-') as temp:
    run = Path(temp)
    completed = subprocess.run([str(app.NODE), str(packet / 'replay_real_snapshot.mjs'),
                                str(local), str(historical), str(run)],
                               capture_output=True, text=True, timeout=120, check=True)
    historical_result = json.loads(completed.stdout)
    app.save(run / 'prepare.json', {
        'offline_rehearsal': True, 'release_profile': app.RELEASE_PROFILE,
        'builder_freeze_sha256': app.FREEZE_SHA, 'config_sha256': app.CONFIG_SHA,
        'pointer_sha256': app.sha((run / 'before.pointer.json').read_bytes()),
        'before_feed_sha256': app.sha((run / 'before.tsv').read_bytes()),
        'planned_eligibility_holds_sha256': app.sha(app.HOLD_SPEC.read_bytes()),
    })
    app.save(run / 'build.json', {'live': False, 'returncode': 0, 'offline_rehearsal': True})
    app.contain(run)
    containment = app.verify_containment(run)
    try:
        app.candidate(run)
    except app.Stop as error:
        blocked_code = str(error)
        if blocked_code != 'successful_live_scan_required':
            raise
    else:
        raise RuntimeError('offline_rehearsal_was_not_blocked')
    result = {
        'recorded_at_utc': app.stamp(), 'status': 'VERIFIED_OFFLINE_ONLY',
        'release_profile': app.RELEASE_PROFILE, 'contract_sha256': app.FREEZE_SHA,
        'lifecycle_sha256': app.sha((local / 'lifecycle.py').read_bytes()),
        'historical_replay': historical_result,
        'native_containment': containment,
        'promotion_candidate_guard': blocked_code,
        'network_calls': 0, 'external_writes': 0, 'live_source_refresh': False,
        'temporary_candidate_removed_on_exit': True,
    }
app.save(packet / 'historical_replay_receipt.json', result)
print(json.dumps({
    'status': result['status'], 'rows': historical_result['rows'],
    'sha256': historical_result['feedSha256'],
    'identical_previously_published_bytes': historical_result['matchesPreviouslyPublishedFeedBytes'],
    'held_available_rows': containment['result']['removed_available_rows'],
    'promotion_candidate_guard': blocked_code, 'external_writes': 0,
}))
