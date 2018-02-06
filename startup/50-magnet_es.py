from ophyd import Device, Component as Cpt, EpicsMotor


class MagDiff(Device):
    th = Cpt(EpicsMotor, 'Ax:th}Mtr')
    tth = Cpt(EpicsMotor, 'Ax:tth}Mtr')
    phi = Cpt(EpicsMotor, 'Ax:phi}Mtr')
    chi = Cpt(EpicsMotor, 'Ax:chi}Mtr')

    ath = Cpt(EpicsMotor, 'Ax:ath}Mtr')
    atth = Cpt(EpicsMotor, 'Ax:atth}Mtr')


class MagTable(Device):
    table_y1 = Cpt(EpicsMotor, 'Ax:TblY1}Mtr')
    table_y2 = Cpt(EpicsMotor, 'Ax:TblY2}Mtr')
    table_y3 = Cpt(EpicsMotor, 'Ax:TblY3}Mtr')
    table_x = Cpt(EpicsMotor, 'Ax:TblX}Mtr')

    cryo_x = Cpt(EpicsMotor, 'Ax:CryoX}Mtr')
    cryo_y = Cpt(EpicsMotor, 'Ax:CryoY}Mtr')
    cryo_z = Cpt(EpicsMotor, 'Ax:CryoZ}Mtr')

    stag_y = Cpt(EpicsMotor, 'Ax:StagY}Mtr')


mag_table = MagTable('XF:04IDC-ES:1{Dif:Mag-', name='mag_table')
mag_diff = MagDiff('XF:04IDC-ES:1{Dif:Mag-', name='mag_diff')
