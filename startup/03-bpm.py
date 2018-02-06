from ophyd import Device, Component as Cpt, EpicsMotor


class BPM3(Device):
    x = Cpt(EpicsMotor, 'Ax:X}Mtr')
    y = Cpt(EpicsMotor, 'Ax:Y}Mtr')


bpm3 = BPM3('XF:04IDB-BI:1{BPM:3-', name='bpm3')
