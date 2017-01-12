
def look_up_settings(E, station):
    return {dcm.th: 0}

def adjust_energy_sketch(E, station):
    yield from bp.mv(dcm, E)
    settings = look_up_setting(E, station)
    for d, v in settings.items():
        yield from bp.mv(d, v)
