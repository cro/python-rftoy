#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rftoy.py

Simple python interface to the [RFToy](https://opensprinkler.com/product/rftoy/).
"""

import asyncio
import sys

import httpx


async def _populate(hostname):
    """
    Calls the `jc` endpoint to get the status of all
    the RFToy stations (devices).
    """
    url = f"{hostname}/jc"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
    result = r.json()
    stations = result["stations"]
    return stations


class RFToy:
    """
    Main class for manipulating the RFToy
    """

    def __init__(self, hostname="http://rftoy"):
        self.hostname = hostname
        self.stations = []

    async def repopulate(self):
        """
        Update the object's understanding of the
        status of all devices
        """
        self.stations = await _populate(self.hostname)

    def find_station(self, station_name=None):
        """
        Iterate through the list of stations to
        find one that matches this name
        """
        index = 0
        for s in self.stations:
            if s["name"] == station_name:
                break

            index = index + 1
        station_id = index
        return station_id

    async def _onoff(self, station_id=0, station_name=None, state="on"):
        """
        Generic method for calling the endpoint with `turn=on` or `turn=off`.
        """
        if station_name:
            station_id = self.find_station(station_name=station_name)
        params = {"sid": station_id, "turn": state}
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.hostname}/cc", params=params)
        await self.repopulate()
        return r.json()["result"] == 0

    async def on(self, station_id=None, station_name=None):
        """
        Convenience method for `on`.
        """
        return await self._onoff(
            station_id=station_id, station_name=station_name, state="on"
        )

    async def off(self, station_id=None, station_name=None):
        """
        Convenience method for `on`.
        """
        return await self._onoff(
            station_id=station_id, station_name=station_name, state="off"
        )


async def main():
    """
    main() function for playing with the library from the CLI
    Example:
        ./rftoy 1 on
    First parameter is the station ID or the station name.
    Second parameter is True, 1, or on (to turn on) or
    False, 0, or off (to turn off)
    """
    station = sys.argv[1]
    status = sys.argv[2]

    r = RFToy()
    await r.repopulate()
    try:
        station_id = int(station)
        if status in [True, 1, "on"]:
            result = await r.on(station_id=station_id)
        if status in [False, 0, "off"]:
            result = await r.off(station_id=station_id)
    except ValueError:
        if status in [True, 1, "on"]:
            result = await r.on(station_name=station)
        if status in [False, 0, "off"]:
            result = await r.off(station_name=station)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
