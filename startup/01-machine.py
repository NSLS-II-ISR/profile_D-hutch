from ophyd import Device, Component as Cpt, PVPositioner, EpicsSignalRO, EpicsSignal


class VirtualGap(PVPositioner):
    readback = Cpt(EpicsSignalRO, "t2.C")
    setpoint = Cpt(EpicsSignal, "size")
    done = Cpt(EpicsSignalRO, "DMOV")
    done_value = 1


class VirtualCenter(PVPositioner):
    readback = Cpt(EpicsSignalRO, "t2.D")
    setpoint = Cpt(EpicsSignal, "center")
    done = Cpt(EpicsSignalRO, "DMOV")
    done_value = 1


class VirtualMotorCenterAndGap(Device):
    "Center and gap with virtual motors"
    x_cntr = Cpt(VirtualCenter, "-Ax:X}")
    y_cntr = Cpt(VirtualCenter, "-Ax:Y}")
    x_gap = Cpt(VirtualGap, "-Ax:X}")
    y_gap = Cpt(VirtualGap, "-Ax:Y}")


fe_slits = VirtualMotorCenterAndGap("FE:C04A-OP{Slt:12", name="fe_slits")
ring_current = EpicsSignalRO("SR:OPS-BI{DCCT:1}I:Real-I", name="ring_current")
ivu_gap = EpicsSignalRO("SR:C04-ID:G1{IVU:1-LEnc}Gap", name="ivu_gap")
