# bpp, bp bps already in namespace from 00-base.py
def look_up_settings(E, station):
    return {dcm.th: 0}


def adjust_energy_sketch(E, station):
    yield from bps.mv(dcm, E)
    settings = look_up_setting(E, station)
    for d, v in settings.items():
        yield from bps.mv(d, v)


def default_scan():
    yield from bp.scan([eiger1m_single], th, 0, 1, 10, md={"purpose": "test ..."})


import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp
import bluesky.plans as bp

attenuators = [bank]


def attenuation_level(n):

    s1, s2, s3, s4 = [{"0": "Close", "1": "Open"}[v] for v in format(n, "04b")]
    yield from bps.mv(
        bank.attn1,
        s1,
        bank.attn2,
        s2,
        bank.attn3,
        s3,
        bank.attn4,
        s4,
    )


def auto_attenuate(start, stop, steps):
    def trigger_and_read(devices, name="primary"):
        """
        Trigger and read a list of detectors and bundle readings into one Event.
        Parameters
        ----------
        devices : iterable
            devices to trigger (if they have a trigger method) and then read
        name : string, optional
            event stream name, a convenient human-friendly identifier; default
            name is 'primary'
        Yields
        ------
        msg : Msg
            messages to 'trigger', 'wait' and 'read'
        """
        # If devices is empty, don't emit 'create'/'save' messages.
        if not devices:
            yield from null()
        devices = bps.separate_devices(devices)  # remove redundant entries
        rewindable = bps.all_safe_rewind(devices)  # if devices can be re-triggered

        if eiger1m_single in devices:
            # do checks
            # put in all the attenuators

            for j in range(16):
                yield from attenuation_level(j)
                yield from bps.checkpoint()
                ret = yield from bps.trigger_and_read(
                    [eiger1m_single] + attenuators, name="auto_scale"
                )
                if len(ret) == 0:
                    break  # simulation mode
                # put in better logic!
                import numpy as np

                if (
                    ret[eiger1m_single.stats2.total.name]["value"] > 0
                    or np.random.rand() > 0.5
                ):

                    break

        def inner_trigger_and_read():

            grp = bps._short_uid("trigger")
            no_wait = True
            for obj in devices:
                if hasattr(obj, "trigger"):
                    no_wait = False
                    yield from bps.trigger(obj, group=grp)
            # Skip 'wait' if none of the devices implemented a trigger method.
            if not no_wait:
                yield from bps.wait(group=grp)
            yield from bps.create(name)
            ret = {}  # collect and return readings to give plan access to them
            for obj in devices:
                reading = yield from bps.read(obj)
                if reading is not None:
                    ret.update(reading)
            yield from bps.save()
            return ret

        return (yield from bpp.rewindable_wrapper(inner_trigger_and_read(), rewindable))

    def one_nd_step(detectors, step, pos_cache, take_reading=trigger_and_read):
        """
        Inner loop of an N-dimensional step scan
        This is the default function for ``per_step`` param`` in ND plans.
        Parameters
        ----------
        detectors : iterable
            devices to read
        step : dict
            mapping motors to positions in this step
        pos_cache : dict
            mapping motors to their last-set positions
        take_reading : plan, optional
            function to do the actual acquisition ::
            def take_reading(dets, name='primary'):
                    yield from ...
            Callable[List[OphydObj], Optional[str]] -> Generator[Msg], optional
            Defaults to `trigger_and_read`
        """
        motors = step.keys()
        yield from bps.move_per_step(step, pos_cache)
        yield from take_reading(list(detectors) + list(motors))

    yield from bp.scan(
        [eiger1m_single] + attenuators, th, start, stop, steps, per_step=one_nd_step
    )
