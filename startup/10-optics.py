from ophyd import EpicsMotor


th = EpicsMotor("XF:04IDD-ES:1{Dif:ISD-Ax:th}Mtr", name="th", labels=["optics"])
zeta = EpicsMotor("XF:04IDD-ES:1{Dif:ISD-Ax:zeta}Mtr", name="zeta", labels=["optics"])
