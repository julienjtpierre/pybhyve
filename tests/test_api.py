"""Define tests for the REST API."""
import json

import aiohttp
import pytest

from pybhyve import Client
from pybhyve.errors import RequestError

from .const import TEST_USERNAME, TEST_PASSWORD
from .fixtures.api import devices_json


@pytest.mark.asyncio
async def test_api_error(aresponses, event_loop, devices_json):
    aresponses.add(
        "api.orbitbhyve.com",
        "/v1/devices",
        "get",
        aresponses.Response(text="", status=500),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        client = Client(TEST_USERNAME, TEST_PASSWORD, None, session, None)

        with pytest.raises(RequestError):
            await client.devices


@pytest.mark.asyncio
async def test_get_devices(aresponses, event_loop, devices_json):
    aresponses.add(
        "api.orbitbhyve.com",
        "/v1/devices",
        "get",
        aresponses.Response(text=json.dumps(devices_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        client = Client(TEST_USERNAME, TEST_PASSWORD, None, session, None)

        devices = await client.devices
        assert len(devices) == 2
