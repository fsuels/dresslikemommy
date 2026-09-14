#!/usr/bin/env python3
"""Install, inspect, or stop the local growth-dashboard LaunchAgent on macOS.

Install enables startup at login and restart on failure. Stop disables startup
and stops this exact registered job, retaining its plist and any prior backup.
No browser, business account, remote service, or unrelated process is changed.
"""

from __future__ import annotations

import argparse
import datetime as dt
import http.client
import json
import os
import plistlib
import re
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from marketing_dashboard_server import DEFAULT_PORT, SERVICE, ROOT, workspace_id


LABEL = "com.dresslikemommy.growth-dashboard"
PYTHON = Path(sys.executable).resolve()


class InstallationError(RuntimeError):
    pass


def paths(home: Path) -> tuple[Path, Path]:
    return (
        home / "Library/LaunchAgents" / f"{LABEL}.plist",
        home / "Library/Logs/dresslikemommy/growth-dashboard",
    )


def build_plist(root: Path, python_bin: Path, home: Path, port: int = DEFAULT_PORT) -> dict:
    if not 1 <= port <= 65535:
        raise InstallationError("Use a port from 1 to 65535.")
    root, python_bin, home = root.resolve(), python_bin.resolve(), home.resolve()
    _, logs = paths(home)
    payload = {
        "Label": LABEL,
        "ProgramArguments": [str(python_bin), "-u", str(root / "ops/scripts/marketing_dashboard_server.py"), "--root", str(root), "--port", str(port)],
        "WorkingDirectory": str(root), "RunAtLoad": True, "KeepAlive": True,
        "ThrottleInterval": 10, "ProcessType": "Background", "Umask": 0o077,
        "StandardOutPath": str(logs / "stdout.log"),
        "StandardErrorPath": str(logs / "stderr.log"),
    }
    if plistlib.loads(plistlib.dumps(payload)) != payload:
        raise InstallationError("LaunchAgent configuration did not validate.")
    return payload


def run(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(args, text=True, capture_output=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise InstallationError("The requested local service operation could not run.") from error
    if check and result.returncode:
        raise InstallationError(f"Local service operation failed ({Path(args[0]).name} {args[1]}). Existing backup files were retained.")
    return result


def validate_interpreter(python_bin: Path) -> None:
    if not python_bin.is_absolute() or not python_bin.is_file() or not os.access(python_bin, os.X_OK):
        raise InstallationError("The selected absolute Python interpreter is unavailable.")
    result = run([str(python_bin), "-c", "import sys; assert sys.version_info >= (3, 10); print('DLM_PYTHON_OK')"])
    if result.stdout.strip() != "DLM_PYTHON_OK":
        raise InstallationError("The selected Python interpreter did not pass its version check.")


def validate_existing(payload: dict, root: Path, port: int) -> None:
    expected_script = str(root.resolve() / "ops/scripts/marketing_dashboard_server.py")
    args = payload.get("ProgramArguments", [])
    try:
        script_matches = len(args) == 7 and args[1:4] == ["-u", expected_script, "--root"]
        interpreter_matches = Path(args[0]).is_absolute() and bool(re.fullmatch(r"python(?:3(?:\.\d+)?)?", Path(args[0]).name))
        root_matches = args[4] == str(root.resolve())
        port_matches = args[5] == "--port" and int(args[6]) == port
    except (ValueError, IndexError, TypeError):
        raise InstallationError("An existing LaunchAgent has different or unreadable configuration; it was preserved.")
    if payload.get("Label") != LABEL or payload.get("WorkingDirectory") != str(root.resolve()) or not all((script_matches, interpreter_matches, root_matches, port_matches)):
        raise InstallationError("An existing LaunchAgent belongs to a different service, checkout, or port; it was preserved.")


def read_existing(plist_path: Path, root: Path, port: int) -> dict | None:
    if plist_path.is_symlink():
        raise InstallationError("The LaunchAgent path is a symlink; it was preserved.")
    if not plist_path.exists():
        return None
    try:
        payload = plistlib.loads(plist_path.read_bytes())
    except (OSError, ValueError, plistlib.InvalidFileException) as error:
        raise InstallationError("The existing LaunchAgent is unreadable; it was preserved.") from error
    if not isinstance(payload, dict):
        raise InstallationError("The existing LaunchAgent is not a valid service configuration.")
    validate_existing(payload, root, port)
    return payload


def port_receipt(port: int, root: Path) -> dict:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.5):
            pass
    except ConnectionRefusedError:
        return {"occupied": False, "ours": False, "status": None}
    except OSError:
        # Do not mistake permission, route, or timeout failures for a free port.
        return {"occupied": True, "ours": False, "status": None}
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=1.5)
    try:
        connection.request("GET", "/api/status")
        response = connection.getresponse()
        raw = response.read(128 * 1024)
        payload = json.loads(raw)
        ours = response.status == 200 and isinstance(payload, dict) and payload.get("service") == SERVICE and payload.get("workspace_id") == workspace_id(root)
        return {"occupied": True, "ours": ours, "status": payload if ours else None}
    except (OSError, ValueError, http.client.HTTPException):
        return {"occupied": True, "ours": False, "status": None}
    finally:
        connection.close()


def launch_target() -> str:
    return f"gui/{os.getuid()}"


def loaded() -> bool:
    return run(["/bin/launchctl", "print", f"{launch_target()}/{LABEL}"], check=False).returncode == 0


def disabled() -> bool:
    output = run(["/bin/launchctl", "print-disabled", launch_target()], check=False).stdout
    return bool(re.search(r'"' + re.escape(LABEL) + r'"\s*=>\s*true', output))


def atomic_plist(plist_path: Path, payload: dict) -> Path | None:
    """Preserve an exact before-copy and replace only this service's plist."""
    plist_path.parent.mkdir(parents=True, exist_ok=True)
    serialized = plistlib.dumps(payload, sort_keys=True)
    if plist_path.exists() and plist_path.read_bytes() == serialized:
        return None
    backup: Path | None = None
    if plist_path.exists():
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup = plist_path.with_name(plist_path.name + ".before-" + stamp)
        with backup.open("xb") as handle:
            handle.write(plist_path.read_bytes())
        backup.chmod(0o600)
    with tempfile.NamedTemporaryFile("wb", dir=plist_path.parent, prefix=".growth-dashboard-", suffix=".plist", delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(serialized)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        run(["/usr/bin/plutil", "-lint", str(temporary)])
        os.replace(temporary, plist_path)
        plist_path.chmod(0o600)
    finally:
        temporary.unlink(missing_ok=True)
    return backup


def service_status(root: Path, home: Path, port: int) -> dict:
    plist_path, _ = paths(home)
    existing = read_existing(plist_path, root, port)
    receipt = port_receipt(port, root)
    return {
        "label": LABEL, "installed": existing is not None,
        "loaded": loaded(), "enabled_at_login": existing is not None and not disabled(),
        "running": receipt["ours"], "port_conflict": receipt["occupied"] and not receipt["ours"],
        "url": f"http://127.0.0.1:{port}/", "content_error": (receipt["status"] or {}).get("content_error"),
    }


def install(root: Path, python_bin: Path, home: Path, port: int) -> dict:
    root, python_bin, home = root.resolve(strict=True), python_bin.resolve(), home.resolve()
    validate_interpreter(python_bin)
    if not (root / "ops/scripts/marketing_dashboard_server.py").is_file():
        raise InstallationError("The dashboard server is missing from the selected checkout.")
    plist_path, logs = paths(home)
    existing = read_existing(plist_path, root, port)
    payload = build_plist(root, python_bin, home, port)
    is_loaded = loaded()
    receipt = port_receipt(port, root)
    if receipt["occupied"] and not receipt["ours"]:
        raise InstallationError("The dashboard port is occupied by another service. Nothing was stopped or replaced.")
    if is_loaded and existing is None:
        raise InstallationError("A job with this label is loaded without a matching plist. It was preserved.")
    if receipt["ours"] and not is_loaded:
        raise InstallationError("This dashboard is already running outside the registered LaunchAgent. Stop that instance before installation; no process was stopped.")
    logs.mkdir(parents=True, exist_ok=True, mode=0o700)
    if logs.is_symlink():
        raise InstallationError("The dashboard log folder is a symlink; it was preserved.")
    logs.chmod(0o700)
    for name in ("stdout.log", "stderr.log"):
        log = logs / name
        if log.is_symlink():
            raise InstallationError("A dashboard log path is a symlink; it was preserved.")
        log.touch(exist_ok=True, mode=0o600)
        log.chmod(0o600)
    backup = None
    if payload != existing:
        backup = atomic_plist(plist_path, payload)
        if is_loaded:
            run(["/bin/launchctl", "bootout", f"{launch_target()}/{LABEL}"])
            is_loaded = False
    run(["/bin/launchctl", "enable", f"{launch_target()}/{LABEL}"])
    if not is_loaded:
        run(["/bin/launchctl", "bootstrap", launch_target(), str(plist_path)])
    elif not receipt["ours"]:
        run(["/bin/launchctl", "kickstart", f"{launch_target()}/{LABEL}"])
    deadline = time.monotonic() + 6
    while time.monotonic() < deadline:
        if port_receipt(port, root)["ours"]:
            result = service_status(root, home, port)
            result["before_backup_created"] = backup is not None
            return result
        time.sleep(0.2)
    raise InstallationError("The LaunchAgent was installed, but its dashboard did not become reachable. Inspect status; no unrelated process was changed.")


def stop(root: Path, home: Path, port: int) -> dict:
    plist_path, _ = paths(home)
    if read_existing(plist_path, root, port) is None:
        raise InstallationError("No matching dashboard LaunchAgent is installed. No process was stopped.")
    run(["/bin/launchctl", "disable", f"{launch_target()}/{LABEL}"])
    if loaded():
        run(["/bin/launchctl", "bootout", f"{launch_target()}/{LABEL}"])
    result = service_status(root, home, port)
    result["configuration_retained"] = True
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "status", "stop"))
    parser.add_argument("--python", type=Path, default=PYTHON, help="Absolute Python 3.10+ interpreter; defaults to this running interpreter.")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    if sys.platform != "darwin":
        parser.error("LaunchAgent management requires macOS.")
    if not 1 <= args.port <= 65535:
        parser.error("Use a port from 1 to 65535.")
    try:
        if args.action == "install":
            result = install(args.root, args.python, Path.home(), args.port)
        elif args.action == "stop":
            result = stop(args.root, Path.home(), args.port)
        else:
            result = service_status(args.root, Path.home(), args.port)
    except (InstallationError, OSError) as error:
        raise SystemExit(str(error) if isinstance(error, InstallationError) else "A local service file operation failed; existing records were preserved.")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
