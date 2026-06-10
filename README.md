# tapo-t310-logger

Small local CSV logger for TP-Link Tapo T310 sensors using [python-kasa](https://github.com/python-kasa/python-kasa).

The script reads configured TP-Link Tapo H100 hub IP addresses, collects values from connected T310 sensors, and appends them to a local CSV file.

Example output:

| time | device_id | alias | temperature | humidity |
|---|---|---|---:|---:|
| 2026-06-09T16:30:00 | 802C2EE12C... | Living room | 24.2 | 57 |

Local CSV logging only. No cloud dashboard. No database. No MQTT. No Home Assistant.

## Requirements

- Python 3 with python3-pip and python3-venv
- One or more TP-Link Tapo H100 hubs and T310 sensors
- Tapo account credentials
- Local network acceess to H100

## Compatibility

Currently tested with the TP-Link Tapo H100 hub only:
- Hardware: 1.0 (EU)
- Firmware: 1.6.1 Build 250324 Rel.173226

Other Tapo hubs may work, but I cannot verify this because I do not own one. Feedback and reports are welcome.

## Setup

**1. Clone the repository:**
```bash
git clone https://github.com/kraftfabrik/tapo-t310-logger.git
cd tapo-t310-logger
cp config/credentials.example config/credentials
cp config/hubs.example config/hubs
```

**2. Edit the *plaintext* config files in `config/`.**

**2.1. `config/credentials:`**
```plaintext
your-tapo-email@example.com
your-tapo-password
```

**2.1.1. Restrict access to the `credentials` file:**
```bash
chmod 600 config/credentials
```

**2.2 `config/hubs:`**

```plaintext
# Kitchen
160.140.100.240

# Living room
160.140.100.241
```

Empty lines and lines starting with `#` are ignored.

**3. Run the logger:**
```bash
./run.sh
```
`run.sh` creates a local virtual environment and installs the required Python dependency if needed.


## Output
Sensor data is appended to `tapo_t310_data.csv` in the project directory.

## Example Raspberry Pi / cron

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
Adjust */path/to/tapo-t310-logger* to your local project path.

A `cron.log` file will be created in the project directory.

### License

GPL-3.0-or-later

### Disclaimer

This project is not affiliated with, endorsed by, or sponsored by TP-Link.
