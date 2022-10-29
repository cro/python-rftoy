#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import sys

import httpx
import logging

log = logging.getLogger(__file__)


async def _populate(hostname):
    url = f"{hostname}/jc"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
    result = r.json()
    stations = result["stations"]
    newstations = []
    for s in stations:
        if s["code"] != "----------------":
            newstations.append(s)
        else:
            log.debug("Dropping station %s, no code.", s["name"])
    return newstations


class RFToy(object):
    def __init__(self, hostname="http://rftoy.home.ncbt.org"):
        self.hostname = hostname

    async def repopulate(self):
        self.stations = await _populate(self.hostname)

    def find_station(self, station_name=None):
        index = 0
        for s in self.stations:
            if s["name"] == station_name:
                break
            else:
                index = index + 1
        station_id = index
        return station_id

    async def _onoff(self, station_id=0, station_name=None, state="on"):
        if station_name:
            station_id = self.find_station(station_name=station_name)
        params = {"sid": station_id, "turn": state}
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.hostname}/cc", params=params)
        if r.json()["result"] == 0:
            await self.repopulate()
            return True
        else:
            return False

    async def on(self, station_id=None, station_name=None):
        return await self._onoff(station_id=station_id, station_name=station_name, state="on")

    async def off(self, station_id=None, station_name=None):
        return await self._onoff(
            station_id=station_id, station_name=station_name, state="off"
        )



async def main():
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