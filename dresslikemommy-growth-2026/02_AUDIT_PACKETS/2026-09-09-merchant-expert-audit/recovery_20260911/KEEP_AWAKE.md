Confidence: H

Persistent idle-sleep prevention was installed and verified on September 11, 2026. The user LaunchAgent starts at GUI login and keeps display and idle-system sleep inhibited while the user is logged in, including when Codex is closed. Its own caffeinate PID owns all three required assertions after the temporary helper was stopped. Future relogin start and 24-hour renewal are configured, not yet observed.

Installed file: `/Users/fsuels/Library/LaunchAgents/com.fsuels.codex-keep-awake.plist`. This keeps the display on and may increase energy use. Manual locking, logout, lid closure, restart/login barriers, power loss and security policies remain possible interruptions. No password, TCC, FileVault or remote-access setting was changed.

Rollback: unload only `gui/501/com.fsuels.codex-keep-awake` with `/bin/launchctl bootout`; then remove only the installed file if its hash still matches `keep_awake_receipt.json`.

Merchant access also succeeded after the owner confirmed the Mac was unlocked. Native Chrome full-screen capture was blank; normal View > Exit Full Screen restored the screenshot and readable return form. This does not establish Merchant product receipt.
