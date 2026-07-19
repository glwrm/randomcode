# GoStream

Minimal boilerplate code for viewing RTMP streams using OpenCV. Includes some
basic handling for dropped frames with a customizable limit.

## RTMP Setup
There are many ways to setup an RTMP server, but I would recommend MediaMTX
as it is the easiest. Install it: by downloading the executable binaries off
the [Github Releases Page](https://github.com/bluenviron/mediamtx/releases) or using `yay -S mediamtx` for Arch linux or other Arch-based distros.

### If using executable binary:
Run the file via the terminal.

### If using Arch:
Run these commands via the terminal:
```bash
sudo systemctl enable mediamtx # will make mediamtx automatically start upon reboot
sudo systemctl start mediamtx
```

## Requirements for the viewer

- **Python 3.7+**
- **OpenCV with FFmpeg support** — `opencv-python` ships with FFmpeg backends,
  which are required to read RTMP streams.

## Configuration

The RTMP URL is set near the top of `main.py`:

```python
RTMP_URL = "rtmp://localhost/live"
```

The consecutive dropped frame limit set under the RTMP URL:
```python
MAX_CONSECUTIVE_FAILURES = 30
```
