# Make ophyd listen to pyepics.
from ophyd import setup_ophyd
setup_ophyd()

# Connect to metadatastore and filestore.
from metadatastore.mds import MDS, MDSRO
from filestore.fs import FileStoreRO
from databroker import Broker
mds_config = {'host': 'xf04id-ca1',
              'port': 27017,
              'database': 'metadatastore-production-v1',
              'timezone': 'US/Eastern'}
fs_config = {'host':  'xf04id-ca1',
             'port': 27017,
             'database': 'filestore-production-v1'}
mds = MDS(mds_config)
mds_readonly = MDS(mds_config)
fs_readonly = FileStoreRO(fs_config)
db = Broker(mds_readonly, fs_readonly)

# Subscribe metadatastore to documents.
# If this is removed, data is not saved to metadatastore.
from bluesky.global_state import gs
gs.RE.subscribe('all', mds.insert)

# Import matplotlib and put it in interactive mode.
import matplotlib.pyplot as plt
plt.ion()

# Make plots update live while scans run.
from bluesky.utils import install_qt_kicker
install_qt_kicker()

# Optional: set any metadata that rarely changes.
# RE.md['beamline_id'] = 'YOUR_BEAMLINE_HERE'

# convenience imports
from ophyd.commands import *
from bluesky.callbacks import *
from bluesky.spec_api import *
from bluesky.global_state import gs, abort, stop, resume
from time import sleep
import numpy as np
import bluesky.plans as bp

RE = gs.RE  # convenience alias

# Uncomment the following lines to turn on verbose messages for debugging.
# import logging
# ophyd.logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)
