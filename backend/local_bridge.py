"""Server-to-server JSON calls to the existing local/hosted Pomodoro API.
"""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def hosted():
    return (os.environ.get("RENDER", "").lower() == "true"
            or bool(os.environ.get("RENDER_EXTERNAL_HOSTNAME", "").strip()))



def peer_call(variable, default, path, data=None):
    base = os.environ.get(variable, "").strip() or default
    base = base.rstrip("/")
    try:
        u = urlsplit(base)
        port = u.port
    except ValueError as error:
        raise ValueError(variable + " must be a valid service origin.") from error
    local = u.hostname in ("localhost", "127.0.0.1", "::1")
    if (not u.hostname or u.username or u.password or u.path or u.query or u.fragment
            or any(c.isspace() for c in base)
            or not (u.scheme == "https" or (u.scheme == "http" and local and port is not None))):
        raise ValueError(variable + " must be an HTTPS origin, or a local http://127.0.0.1:PORT origin.")
    if not path.startswith("/api/") or any(c in path for c in ("?", "#", "\r", "\n")):
        raise ValueError("Invalid peer API path.")
    # Use the existing Pomodoro API; its deployed code needs no changes.
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    body = json.dumps(data).encode() if data is not None else None
    req = Request(base + path, data=body, headers=headers)

    def read_json(response):
        raw = response.read(12 * 1024 * 1024 + 1)
        if len(raw) > 12 * 1024 * 1024:
            raise ValueError("Peer response is too large.")
        return json.loads(raw)

    try:
        # Keep calls on the explicitly configured service origin.
        with build_opener(ProxyHandler({}), NoRedirect()).open(req, timeout=4) as response:
            return read_json(response), response.status
    except HTTPError as error:
        if error.code in (301, 302, 303, 307, 308):
            return {"error": "The peer redirected. Set its final HTTPS origin in Render Environment."}, 502
        if error.code in (401, 403) and u.scheme == "https":
            return {"error": "Pomodoro rejected this API request. Check its URL and confirm its deployed /api/timer endpoint accepts server requests."}, 503
        try:
            return read_json(error), error.code
        except (ValueError, UnicodeError):
            return {"error": "The other service returned an invalid response. It may still be starting."}, 502
    except (URLError, TimeoutError, OSError, ValueError, UnicodeError):
        return {"error": "The other service is unavailable or waking up. Open its website, wait for it to load, then retry."}, 503
