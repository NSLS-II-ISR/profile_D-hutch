from ophyd import Device, Component as Cpt, EpicsMotor


class Mirror(Device):
    x = Cpt(EpicsMotor, '-Ax:X}Mtr')
    pitch = Cpt(EpicsMotor, '-Ax:P}Mtr')
    y = Cpt(EpicsMotor, '-Ax:Y}Mtr')
    yaw = Cpt(EpicsMotor, '-Ax:Yaw}Mtr')
    roll = Cpt(EpicsMotor, '-Ax:R}Mtr')


class BendM(Mirror):
    bender = Cpt(EpicsMotor, '-Ax:Bender}Mtr')


class DHRM(Mirror):
    froll = Cpt(EpicsMotor, '-Ax:fRoll}Mtr')
    fpitch = Cpt(EpicsMotor, '-Ax:fPitch}Mtr')


hfm = BendM('XF:04IDA-OP:1{Mir:HFM', name='hfm')
vfm = BendM('XF:04IDA-OP:1{Mir:VFM', name='vfm')
dhrm = DHRM('XF:04IDB-OP:1{Mir:DHRM', name='dhrm')
