#!/usr/bin/env python3
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import requests

CONTRACT = '0x495f947276749ce646f68ac8c248420045cb7b5e'
CREATOR = '0x054a2e4b3b5ea2c62372e92358fdf7fb74b4f34a'
CREATOR_INT = int(CREATOR, 16)
SNAPSHOT_BLOCK = 25764033
RPCS = ['https://ethereum-rpc.publicnode.com', 'https://eth.drpc.org']
TRANSFER_SINGLE = '0xc3d58168c5bfaa...'
TRANSFER_SINGLE = '0xc3d58168c5bfaa...'
