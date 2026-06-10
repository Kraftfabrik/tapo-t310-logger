# tapo-t310-logger

Simple CSV logger for Tapo T310 temperature and humidity sensors connected to H100 hubs using [python-kasa](https://github.com/python-kasa/python-kasa).

The script reads configured TP-Link Tapo H100 hub IP addresses, collects values from connected T310 sensors, and appends them to a local CSV file.

Example output:

| time | device_id | alias | temperature | humidity |
|---|---|---|---:|---:|
| 2026-06-09T16:30:00 | 802C2EE12C... | Living room | 24.2 | 57 |

Local CSV logging only. No cloud dashboard. No database. No MQTT. No Home Assistant.

## Requirements

- Python 3 with `pip` and `venv`
- One or more TP-Link Tapo H100 hubs
- One or more TP-Link Tapo T310 sensors
- Tapo account credentials
- Local network access to the H100 hub

On Debian, Ubuntu, Linux Mint and similar distributions, you may need to install `python3-venv` and `python3-pip` first.

## Compatibility

Currently tested with the TP-Link Tapo H100 hub only:

- Hardware: 1.0 (EU)
- Firmware: 1.6.1 Build 250324 Rel.173226

Other Tapo hubs may work, but I cannot verify this. I do not own one. Feedback are welcome.

## Setup

### 1. Clone the repository and copy config exampels

```bash
git clone https://github.com/kraftfabrik/tapo-t310-logger.git
cd tapo-t310-logger
cp config/credentials.example config/credentials
cp config/hubs.example config/hubs
```

### 2. Edit the plaintext config files in `config/`

#### `config/credentials`

```text
your-tapo-email@example.com
your-tapo-password
```

Restrict access to the credentials file:

```bash
chmod 600 config/credentials
```

#### `config/hubs`

```text
# Kitchen
192.168.1.240

# Living room
192.168.1.241
```

Empty lines and lines starting with `#` are ignored.

### 3. Run the logger

```bash
./run.sh
```

`run.sh` creates a local virtual environment and installs the required Python dependency if needed.

## Output

Sensor data is appended to `tapo_t310_data.csv` in the project directory.

## Example Raspberry Pi setup with cron

A common use case is running the logger on a Raspberry Pi in the same local network as the Tapo H100 hub.

Example: run the logger every 30 minutes using cron.

Open the user crontab:

```bash
crontab -e
```

Add this line:

```cron
*/30 * * * * cd /path/to/tapo-t310-logger && ./run.sh >> cron.log 2>&1
```

Adjust `/path/to/tapo-t310-logger` to your local project path.

A `cron.log` file will be created in the project directory.

## Optional: Cloud-free operation

The H100 hubs do not require Internet access for this logger. After the initial setup and any desired firmware updates, Internet access can be blocked, for example at the router level.

The logger communicates directly with the H100 hubs over the local network and does not require the Tapo cloud.

When Internet access is blocked:

- CSV logging continues to work
- Local communication between H100 hubs and T310 sensors continues to work
- Cloud features stop working
- Remote access through the Tapo smartphone app is no longer available
- Firmware updates are no longer possible until Internet access is restored

This allows the H100 hubs and T310 sensors to operate without the Tapo cloud after initial configuration.

For long-term stability, it is recommended to keep the H100 hubs offline after setup and to keep the Python environment and dependencies stable. The logger should continue to work as long as the local H100 API remains unchanged and the same Python environment and dependencies are used.

## License

GPL-3.0-or-later

This project is not affiliated with, endorsed by, or sponsored by TP-Link.
