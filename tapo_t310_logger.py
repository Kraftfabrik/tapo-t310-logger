#!/usr/bin/env python3

import asyncio
import csv
from datetime import datetime
from pathlib import Path

from kasa import Credentials, Discover


HUBS_FILE = Path("config/hubs")
CREDENTIALS_FILE = Path("config/credentials")
CSV_FILE = Path("tapo_t310_data.csv")


def read_lines(path):
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


async def read_hub(hub_ip, credentials, timestamp):
    hub = await Discover.discover_single(
        hub_ip,
        credentials=credentials,
    )

    try:
        await hub.update()

        rows = []

        for sensor in hub.children:
            await sensor.update()

            if sensor.model != "T310":
                continue

            rows.append(
                {
                    "time": timestamp,
                    "device_id": sensor.features["device_id"].value,
                    "alias": sensor.alias,
                    "temperature": sensor.features["temperature"].value,
                    "humidity": sensor.features["humidity"].value,
                }
            )

        return rows

    finally:
        await hub.disconnect()


def append_rows(rows):
    if not rows:
        return

    with CSV_FILE.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=rows[0].keys(),
            quoting=csv.QUOTE_ALL,
        )

        if csv_file.tell() == 0:
            writer.writeheader()

        writer.writerows(rows)


async def main():
    credentials = Credentials(*read_lines(CREDENTIALS_FILE)[:2])
    timestamp = datetime.now().isoformat(timespec="seconds")

    rows = []

    for hub_ip in read_lines(HUBS_FILE):
        rows.extend(await read_hub(hub_ip, credentials, timestamp))

    append_rows(rows)


asyncio.run(main())
