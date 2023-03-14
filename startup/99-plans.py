import numpy as np
import bluesky.plan_stubs as bps


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


def auto_attenuate(start, stop, steps):
    raise NotImplementedError("no brains yet")

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
        devices = bps.separate_devices(
            devices + attenuators
        )  # remove redundant entries
        rewindable = bps.all_safe_rewind(devices)  # if devices can be re-triggered

        if eiger1m_single in devices:
            # do checks
            # put in all the attenuators

            for j in range(16):
                yield from bank.set_attenuation_level(j)
                yield from bps.checkpoint()
                ret = yield from bps.trigger_and_read(devices, name="auto_scale")
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


def attenuated_scan(start, stop, steps, *, edges, levels, md=None, mtr=zeta):
    """
    Run a 1D scan over th while adjusting the attenuators.

    Parameters
    ----------
    start, stop : double
        The start and stop angles.

        Must fall with in the min/max of *edges*

    steps : int
        The number of measurements to take.

    edges : array[double]
        The th values to change the attenuators at.

        Must be monotonic and 1 longer than *levels*

    levels : int [0, 15]
        The attenuation level.  0 is the most attenuated, 15 is the least.
    """

    # validate the input
    if stop < edges[0] or start < edges[0]:
        raise ValueError(f"{start=} or {stop=} is less than {edges[0]=}")
    if stop > edges[-1] or start > edges[-1]:
        raise ValueError(f"{start=} or {stop=} is greater than {edges[-1]=}")
    if np.any(np.diff(edges) < 0):
        raise ValueError(f"{edges=} is not monotonic")
    if len(levels) + 1 != len(edges):
        raise ValueError(
            f"edges must be one longer that levels, not {len(edges)=} and {len(levels)=}"
        )

    def attenuating_nd_step(
        detectors, step, pos_cache, take_reading=bps.trigger_and_read
    ):
        # look up level for this angle and set attenuators
        yield from bank.set_attenuation_level(
            levels[np.searchsorted(edges, step[mtr]) - 1]
        )

        # run the default step sub-plan
        yield from bps.one_nd_step(
            detectors=detectors,
            step=step,
            pos_cache=pos_cache,
            take_reading=take_reading,
        )

    return (
        yield from bp.scan(
            [eiger1m_single, bank], mtr, start, stop, steps, per_step=attenuating_nd_step, md=md
        )
    )

edges =  [-14.6, -15, -15.3, -15.6]
levels = [8, 0, 8]