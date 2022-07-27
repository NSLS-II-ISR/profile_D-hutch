from ophyd.signal import EpicsSignalBase

EpicsSignalBase.set_defaults(timeout=10, connection_timeout=10)  # new style

import nslsii

nslsii.configure_base(get_ipython().user_ns, "isr")
