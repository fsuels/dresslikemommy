Confidence: H — **PASS** for the exact proposed user LaunchAgent.

Payload: **649 bytes**, SHA-256 `572e7b451fa9c4f8ecbbd4fe124e890f545aced4e7aca95244d0da95ad6ced6b`. Nine checks pass: valid plist, exact allowed keys/arguments, fixed system executable, user/Aqua scope, UID 501, absent destination, documented flags/restart behavior and scoped rollback.

Local manuals support display/idle-sleep prevention, declaring active user, and a timed process kept running by launchd. The configuration requests renewal after each 24-hour run; renewal and next-login behavior have not been tested.

Current explicit durable-prevention authorization fits this one file. Recheck that its destination and service label are absent; preserve any existing file/job. Install only **/Users/fsuels/Library/LaunchAgents/com.fsuels.codex-keep-awake.plist** in **gui/501**.

This deliberately keeps the display/session active, including on battery. It may keep an unattended desktop available. It does not guarantee access through manual locks, lid closure, logout/restart, power loss or security policies.

After bootstrap, verify the durable job's PID and its own display-sleep, idle-sleep and user-active assertions. Aggregate assertions alone are insufficient because the temporary process already supplies some.

Rollback: boot out **gui/501/com.fsuels.codex-keep-awake**, then remove only the installed regular file if its hash still matches this payload. Killing its child alone would allow KeepAlive to restart it. Other assertions remain untouched.

No password, TCC, FileVault, remote-access or business-setting change is included. No install/native action was performed by this reviewer.

[Machine review](/private/tmp/codex-keep-awake-review.json)

