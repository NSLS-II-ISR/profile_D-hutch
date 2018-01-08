import bluesky.plans as bp
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp


def look_up_settings(E, station):
    return {dcm.th: 0}


def adjust_energy_sketch(E, station):
    yield from bps.mv(dcm, E)
    settings = look_up_setting(E, station)
    for d, v in settings.items():
        yield from bps.mv(d, v)
