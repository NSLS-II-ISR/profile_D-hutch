from ophyd import EpicsMotor


th = EpicsMotor('XF:04IDD-ES:1{Dif:ISD-Ax:th}Mtr', name='th')
zeta = EpicsMotor('XF:04IDD-ES:1{Dif:ISD-Ax:zeta}Mtr', name='zeta')


