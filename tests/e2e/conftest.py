"""Fixtures for the browser tests only."""
import os

import pytest

# Playwright runs an event loop in the test's thread, and Django refuses to
# query the database from a thread with a running event loop unless this is set.
os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', 'true')


@pytest.fixture(scope='session')
def base_url(live_server):
    """Start a real server for the tests, so that page.goto('/') opens its home page."""
    return live_server.url


@pytest.fixture(autouse=True)
def cookies_over_http(settings):
    """The test server uses http, so the cookies cannot be limited to https."""
    settings.CSRF_COOKIE_SECURE = False
    settings.SESSION_COOKIE_SECURE = False
