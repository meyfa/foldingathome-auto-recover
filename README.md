# foldingathome-auto-recover

Script for automatic pause/unpause of F@H worker slots if they fail to download
new WUs, which often fixes that problem faster than simply waiting until enough
attempts have been made.

## Setup / Usage

- Install recent release of Python 3 (must include `pip` package manager)
- Install dependencies: run `pip install -r requirements.txt`
- Configure this script, especially the path settings

To start: run `python fah_auto_recover.py`

The script will stay active until it notices a failed slot. It will then try to
bring it back fast. Works for me, but your mileage may vary.
