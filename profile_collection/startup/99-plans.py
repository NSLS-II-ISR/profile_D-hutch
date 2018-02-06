# bpp, bp bps already in namespace from 00-base.py
def look_up_settings(E, station):
    return {dcm.th: 0}


def adjust_energy_sketch(E, station):
    yield from bps.mv(dcm, E)
    settings = look_up_setting(E, station)
    for d, v in settings.items():
        yield from bps.mv(d, v)

def default_scan():
    yield from bp.scan([eiger1m_single], th, 0, 1, 10, md={'purpose': 'test ...'})

