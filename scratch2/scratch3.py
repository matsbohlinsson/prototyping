#!/usr/bin/env python
from pathlib import Path

import yaml

p = Path('items.yaml')
with p.open() as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    print(data)


