import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from server import Handler, add


@pytest.fixture
def base_url():
    srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()
    srv.server_close()
    t.join()


def get(url):
    try:
        with urllib.request.urlopen(url) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, json.load(e)


def test_add():
    assert add(2, 3) == 5


def test_health(base_url):
    assert get(base_url + "/") == (200, {"status": "ok"})


def test_add_endpoint(base_url):
    assert get(base_url + "/add/4/5") == (200, {"result": 9})


def test_bad_input(base_url):
    assert get(base_url + "/add/x/1")[0] == 400
