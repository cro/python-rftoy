# RFToy Tests
import asyncio
import re
import pytest
from pytest_httpx import HTTPXMock
from rftoy import RFToy

DEFAULT_DATA = {
    "stations": [
        {"name": "C. R. Office Light", "status": 0, "code": "09c99809c99800fa"},
        {"name": "Office Fan Low", "status": 0, "code": "09c99509c99200fa"},
        {"name": "Office Fan Med", "status": 0, "code": "09c99909c99200fa"},
        {"name": "Office Fan Hi", "status": 0, "code": "09c99409c99200fa"},
        {"name": "Floor Fan (etek1)", "status": 0, "code": "44553344553c00c2"},
        {"name": "Station 06", "status": 0, "code": "4455c34455cc00c2"},
        {"name": "Station 07", "status": 0, "code": "44570344570c00c3"},
        {"name": "Station 08", "status": 0, "code": "445d03445d0c00c2"},
        {"name": "Station 09", "status": 0, "code": "44750344750c00c1"},
        {"name": "Station 10", "status": 0, "code": "----------------"},
        {"name": "Station 11", "status": 0, "code": "----------------"},
        {"name": "Station 12", "status": 0, "code": "----------------"},
        {"name": "Station 13", "status": 0, "code": "----------------"},
        {"name": "Station 14", "status": 0, "code": "----------------"},
        {"name": "Station 15", "status": 0, "code": "----------------"},
        {"name": "Station 16", "status": 0, "code": "----------------"},
        {"name": "Station 17", "status": 0, "code": "----------------"},
        {"name": "Station 18", "status": 0, "code": "----------------"},
        {"name": "Station 19", "status": 0, "code": "----------------"},
        {"name": "Station 20", "status": 0, "code": "----------------"},
        {"name": "Station 21", "status": 0, "code": "----------------"},
        {"name": "Station 22", "status": 0, "code": "----------------"},
        {"name": "Station 23", "status": 0, "code": "----------------"},
        {"name": "Station 24", "status": 0, "code": "----------------"},
        {"name": "Station 25", "status": 0, "code": "----------------"},
        {"name": "Station 26", "status": 0, "code": "----------------"},
        {"name": "Station 27", "status": 0, "code": "----------------"},
        {"name": "Station 28", "status": 0, "code": "----------------"},
        {"name": "Station 29", "status": 0, "code": "----------------"},
        {"name": "Station 30", "status": 0, "code": "----------------"},
        {"name": "Station 31", "status": 0, "code": "----------------"},
        {"name": "Station 32", "status": 0, "code": "----------------"},
        {"name": "Station 33", "status": 0, "code": "----------------"},
        {"name": "Station 34", "status": 0, "code": "----------------"},
        {"name": "Station 35", "status": 0, "code": "----------------"},
        {"name": "Station 36", "status": 0, "code": "----------------"},
        {"name": "Station 37", "status": 0, "code": "----------------"},
        {"name": "Station 38", "status": 0, "code": "----------------"},
        {"name": "Station 39", "status": 0, "code": "----------------"},
        {"name": "Station 40", "status": 0, "code": "----------------"},
        {"name": "Station 41", "status": 0, "code": "----------------"},
        {"name": "Station 42", "status": 0, "code": "----------------"},
        {"name": "Station 43", "status": 0, "code": "----------------"},
        {"name": "Station 44", "status": 0, "code": "----------------"},
        {"name": "Station 45", "status": 0, "code": "----------------"},
        {"name": "Station 46", "status": 0, "code": "----------------"},
        {"name": "Station 47", "status": 0, "code": "----------------"},
        {"name": "Station 48", "status": 0, "code": "----------------"},
        {"name": "Station 49", "status": 0, "code": "----------------"},
        {"name": "Station 50", "status": 0, "code": "----------------"},
    ]
}

DEFAULT_DATA_1_ON = {
    "stations": [
        {"name": "C. R. Office Light", "status": 0, "code": "09c99809c99800fa"},
        {"name": "Office Fan Low", "status": 1, "code": "09c99509c99200fa"},
        {"name": "Office Fan Med", "status": 0, "code": "09c99909c99200fa"},
        {"name": "Office Fan Hi", "status": 0, "code": "09c99409c99200fa"},
        {"name": "Floor Fan (etek1)", "status": 0, "code": "44553344553c00c2"},
        {"name": "Station 06", "status": 0, "code": "4455c34455cc00c2"},
        {"name": "Station 07", "status": 0, "code": "44570344570c00c3"},
        {"name": "Station 08", "status": 0, "code": "445d03445d0c00c2"},
        {"name": "Station 09", "status": 0, "code": "44750344750c00c1"},
        {"name": "Station 10", "status": 0, "code": "----------------"},
        {"name": "Station 11", "status": 0, "code": "----------------"},
        {"name": "Station 12", "status": 0, "code": "----------------"},
        {"name": "Station 13", "status": 0, "code": "----------------"},
        {"name": "Station 14", "status": 0, "code": "----------------"},
        {"name": "Station 15", "status": 0, "code": "----------------"},
        {"name": "Station 16", "status": 0, "code": "----------------"},
        {"name": "Station 17", "status": 0, "code": "----------------"},
        {"name": "Station 18", "status": 0, "code": "----------------"},
        {"name": "Station 19", "status": 0, "code": "----------------"},
        {"name": "Station 20", "status": 0, "code": "----------------"},
        {"name": "Station 21", "status": 0, "code": "----------------"},
        {"name": "Station 22", "status": 0, "code": "----------------"},
        {"name": "Station 23", "status": 0, "code": "----------------"},
        {"name": "Station 24", "status": 0, "code": "----------------"},
        {"name": "Station 25", "status": 0, "code": "----------------"},
        {"name": "Station 26", "status": 0, "code": "----------------"},
        {"name": "Station 27", "status": 0, "code": "----------------"},
        {"name": "Station 28", "status": 0, "code": "----------------"},
        {"name": "Station 29", "status": 0, "code": "----------------"},
        {"name": "Station 30", "status": 0, "code": "----------------"},
        {"name": "Station 31", "status": 0, "code": "----------------"},
        {"name": "Station 32", "status": 0, "code": "----------------"},
        {"name": "Station 33", "status": 0, "code": "----------------"},
        {"name": "Station 34", "status": 0, "code": "----------------"},
        {"name": "Station 35", "status": 0, "code": "----------------"},
        {"name": "Station 36", "status": 0, "code": "----------------"},
        {"name": "Station 37", "status": 0, "code": "----------------"},
        {"name": "Station 38", "status": 0, "code": "----------------"},
        {"name": "Station 39", "status": 0, "code": "----------------"},
        {"name": "Station 40", "status": 0, "code": "----------------"},
        {"name": "Station 41", "status": 0, "code": "----------------"},
        {"name": "Station 42", "status": 0, "code": "----------------"},
        {"name": "Station 43", "status": 0, "code": "----------------"},
        {"name": "Station 44", "status": 0, "code": "----------------"},
        {"name": "Station 45", "status": 0, "code": "----------------"},
        {"name": "Station 46", "status": 0, "code": "----------------"},
        {"name": "Station 47", "status": 0, "code": "----------------"},
        {"name": "Station 48", "status": 0, "code": "----------------"},
        {"name": "Station 49", "status": 0, "code": "----------------"},
        {"name": "Station 50", "status": 0, "code": "----------------"},
    ]
}

EXPECTED_DATA = [
    {"name": "C. R. Office Light", "status": 0, "code": "09c99809c99800fa"},
    {"name": "Office Fan Low", "status": 0, "code": "09c99509c99200fa"},
    {"name": "Office Fan Med", "status": 0, "code": "09c99909c99200fa"},
    {"name": "Office Fan Hi", "status": 0, "code": "09c99409c99200fa"},
    {"name": "Floor Fan (etek1)", "status": 0, "code": "44553344553c00c2"},
    {"name": "Station 06", "status": 0, "code": "4455c34455cc00c2"},
    {"name": "Station 07", "status": 0, "code": "44570344570c00c3"},
    {"name": "Station 08", "status": 0, "code": "445d03445d0c00c2"},
    {"name": "Station 09", "status": 0, "code": "44750344750c00c1"},
]

EXPECTED_DATA_1_ON = [
    {"name": "C. R. Office Light", "status": 0, "code": "09c99809c99800fa"},
    {"name": "Office Fan Low", "status": 1, "code": "09c99509c99200fa"},
    {"name": "Office Fan Med", "status": 0, "code": "09c99909c99200fa"},
    {"name": "Office Fan Hi", "status": 0, "code": "09c99409c99200fa"},
    {"name": "Floor Fan (etek1)", "status": 0, "code": "44553344553c00c2"},
    {"name": "Station 06", "status": 0, "code": "4455c34455cc00c2"},
    {"name": "Station 07", "status": 0, "code": "44570344570c00c3"},
    {"name": "Station 08", "status": 0, "code": "445d03445d0c00c2"},
    {"name": "Station 09", "status": 0, "code": "44750344750c00c1"},
]

EXPECTED_DATA_0_OFF = [
    {"name": "C. R. Office Light", "status": 0, "code": "09c99809c99800fa"},
    {"name": "Office Fan Low", "status": 0, "code": "09c99509c99200fa"},
    {"name": "Office Fan Med", "status": 0, "code": "09c99909c99200fa"},
    {"name": "Office Fan Hi", "status": 0, "code": "09c99409c99200fa"},
    {"name": "Floor Fan (etek1)", "status": 0, "code": "44553344553c00c2"},
    {"name": "Station 06", "status": 0, "code": "4455c34455cc00c2"},
    {"name": "Station 07", "status": 0, "code": "44570344570c00c3"},
    {"name": "Station 08", "status": 0, "code": "445d03445d0c00c2"},
    {"name": "Station 09", "status": 0, "code": "44750344750c00c1"},
]

DEFAULT_DATA_RESPONSE = {"result": 0}


@pytest.mark.asyncio()
async def test_get_stations(httpx_mock):
    httpx_mock.add_response(url="http://sample.invalid/jc", json=DEFAULT_DATA)
    rftoy = RFToy(hostname="http://sample.invalid")
    await rftoy.repopulate()
    assert rftoy.stations == EXPECTED_DATA


@pytest.mark.asyncio()
async def test_find_station(httpx_mock):
    httpx_mock.add_response(url="http://sample.invalid/jc", json=DEFAULT_DATA)
    rftoy = RFToy(hostname="http://sample.invalid")
    await rftoy.repopulate()
    assert rftoy.find_station("Station 08") == 7
    assert rftoy.find_station("C. R. Office Light") == 0


@pytest.mark.asyncio()
async def test_on(httpx_mock):
    cc_url = r"http://sample.invalid/cc?sid=1&turn=on"
    httpx_mock.add_response(url="http://sample.invalid/jc", json=DEFAULT_DATA)
    httpx_mock.add_response(url=cc_url, json=DEFAULT_DATA_RESPONSE)

    rftoy = RFToy(hostname="http://sample.invalid")
    await rftoy.repopulate()
    assert rftoy.stations == EXPECTED_DATA

    httpx_mock.add_response(url="http://sample.invalid/jc", json=DEFAULT_DATA_1_ON)
    await rftoy.on(station_name="Office Fan Low")
    assert rftoy.stations == EXPECTED_DATA_1_ON


@pytest.mark.asyncio()
async def test_off(httpx_mock):
    cc_url = r"http://sample.invalid/cc?sid=1&turn=off"
    httpx_mock.add_response(url="http://sample.invalid/jc", json=DEFAULT_DATA_1_ON)
    httpx_mock.add_response(url=cc_url, json=DEFAULT_DATA_RESPONSE)

    rftoy = RFToy(hostname="http://sample.invalid")
    await rftoy.repopulate()
    assert rftoy.stations == EXPECTED_DATA_1_ON

    httpx_mock.add_response(url="http://sample.invalid/jc", json=DEFAULT_DATA)
    await rftoy.off(station_name="Office Fan Low")
    assert rftoy.stations == EXPECTED_DATA
