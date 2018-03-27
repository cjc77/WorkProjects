#! usr/bin/env python3

import os
import sys

thisdir = os.path.dirname(__file__)
libdir = os.path.join(thisdir, "../tools/")

if libdir not in sys.path:
    sys.path.insert(0, libdir)
