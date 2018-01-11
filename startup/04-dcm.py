from ophyd import Device, Component as Cpt, EpicsMotor


class DCM(Device):
    brag_th = Cpt(EpicsMotor, '-Ax:th}Mtr')
    cb = Cpt(EpicsMotor, '-Ax:CB}Mtr')
    z = Cpt(EpicsMotor, '-Ax:Z}Mtr')
    y2 = Cpt(EpicsMotor, '-Ax:Y2}Mtr')
    th2 = Cpt(EpicsMotor, '-Ax:th2}Mtr')
    chi2 = Cpt(EpicsMotor, '-Ax:chi2}Mtr')

    th2f = Cpt(EpicsMotor, '-Ax:th2f}Mtr')
    chi2f = Cpt(EpicsMotor, '-Ax:chi2f}Mtr')


dcm = DCM('XF:04IDA-OP:1{Mono:DCM', name='dcm')
