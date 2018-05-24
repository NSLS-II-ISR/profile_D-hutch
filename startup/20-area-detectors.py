from types import SimpleNamespace
from datetime import datetime
from ophyd import (SingleTrigger, ImagePlugin, StatsPlugin, AreaDetector,
                   EpicsSignal, EpicsSignalRO, ROIPlugin, ProcessPlugin,
                   Device)
from ophyd.areadetector.base import ADComponent, EpicsSignalWithRBV
from ophyd.areadetector.filestore_mixins import (FileStoreBase, new_short_uid)
from ophyd import Component as Cpt, Signal
from ophyd.utils import set_and_wait
from pathlib import PurePath
from eiger_io.fs_handler_dask import EigerHandlerDask


class EigerSimulatedFilePlugin(Device, FileStoreBase):
    sequence_id = ADComponent(EpicsSignalRO, 'SequenceId')
    file_path = ADComponent(EpicsSignalWithRBV, 'FilePath', string=True)
    file_write_name_pattern = ADComponent(EpicsSignalWithRBV, 'FWNamePattern',
                                          string=True)
    file_write_images_per_file = ADComponent(EpicsSignalWithRBV,
                                             'FWNImagesPerFile')
    current_run_start_uid = Cpt(Signal, value='', add_prefix=())
    enable = SimpleNamespace(get=lambda: True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._datum_kwargs_map = dict()  # store kwargs for each uid
        self.filestore_spec = 'AD_EIGER2'

    def stage(self):
        res_uid = new_short_uid()
        write_path = datetime.now().strftime(self.write_path_template)
        set_and_wait(self.file_path, write_path)
        set_and_wait(self.file_write_name_pattern, '{}_$id'.format(res_uid))
        super().stage()
        fn = (PurePath(self.file_path.get()) / res_uid)
        ipf = int(self.file_write_images_per_file.get())
        # logger.debug("Inserting resource with filename %s", fn)
        self._fn = fn
        res_kwargs = {'images_per_file': ipf}
        self._generate_resource(res_kwargs)

    def generate_datum(self, key, timestamp, datum_kwargs):
        # The detector keeps its own counter which is uses label HDF5
        # sub-files.  We access that counter via the sequence_id
        # signal and stash it in the datum.
        seq_id = 1 + int(self.sequence_id.get())  # det writes to the NEXT one
        datum_kwargs.update({'seq_id': seq_id})
        return super().generate_datum(key, timestamp, datum_kwargs)


class EigerBase(AreaDetector):
    """
    Eiger, sans any triggering behavior.

    Use EigerSingleTrigger or EigerFastTrigger below.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('labels', ['detectors', 'cameras'])
        super().__init__(*args, **kwargs)


    num_triggers = ADComponent(EpicsSignalWithRBV, 'cam1:NumTriggers')
    file = Cpt(EigerSimulatedFilePlugin, suffix='cam1:',
               write_path_template='/GPFS/xf04id/DATA/Eiger1M/%Y/%m/%d/',
               root='/GPFS/xf04id/')

    beam_center_x = ADComponent(EpicsSignalWithRBV, 'cam1:BeamX')
    beam_center_y = ADComponent(EpicsSignalWithRBV, 'cam1:BeamY')
    wavelength = ADComponent(EpicsSignalWithRBV, 'cam1:Wavelength')
    det_distance = ADComponent(EpicsSignalWithRBV, 'cam1:DetDist')
    threshold_energy = ADComponent(EpicsSignalWithRBV, 'cam1:ThresholdEnergy')
    photon_energy = ADComponent(EpicsSignalWithRBV, 'cam1:PhotonEnergy')
    # the checkbox
    manual_trigger = ADComponent(EpicsSignalWithRBV, 'cam1:ManualTrigger')
    # the button next to 'Start' and 'Stop'
    special_trigger_button = ADComponent(EpicsSignal, 'cam1:Trigger')
    image = Cpt(ImagePlugin, 'image1:')
    stats1 = Cpt(StatsPlugin, 'Stats1:')
    stats2 = Cpt(StatsPlugin, 'Stats2:')
    stats3 = Cpt(StatsPlugin, 'Stats3:')
    stats4 = Cpt(StatsPlugin, 'Stats4:')
    stats5 = Cpt(StatsPlugin, 'Stats5:')
    roi1 = Cpt(ROIPlugin, 'ROI1:')
    roi2 = Cpt(ROIPlugin, 'ROI2:')
    roi3 = Cpt(ROIPlugin, 'ROI3:')
    roi4 = Cpt(ROIPlugin, 'ROI4:')
    proc1 = Cpt(ProcessPlugin, 'Proc1:')

    shutter_mode = ADComponent(EpicsSignalWithRBV, 'cam1:ShutterMode')

    # hotfix: shadow non-existant PV
    size_link = None

    def stage(self):
        # before parent
        super().stage()
        # after parent
        set_and_wait(self.manual_trigger, 1)

    def unstage(self):
        set_and_wait(self.manual_trigger, 0)
        super().unstage()


class EigerSingleTrigger(SingleTrigger, EigerBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs['cam.trigger_mode'] = 0
        self.stage_sigs['shutter_mode'] = 1  # 'EPICS PV'
        self.stage_sigs.update({'num_triggers': 1})

    def trigger(self):
        status = super().trigger()
        set_and_wait(self.special_trigger_button, 1)
        return status


def set_eiger_defaults(eiger):
    """Choose which attributes to read per-step (read_attrs) or
    per-run (configuration attrs)."""

    eiger.file.read_attrs = []
    eiger.read_attrs = ['file', 'stats1', 'stats2',
                        'stats3', 'stats4', 'stats5']
    for stats in [eiger.stats1, eiger.stats2, eiger.stats3,
                  eiger.stats4, eiger.stats5]:
        stats.read_attrs = ['total']
    eiger.configuration_attrs = ['beam_center_x', 'beam_center_y',
                                 'wavelength', 'det_distance', 'cam',
                                 'threshold_energy', 'photon_energy']
    eiger.cam.read_attrs = []
    eiger.cam.configuration_attrs = ['acquire_time', 'acquire_period',
                                     'num_images']
    eiger.stats2.total.kind = 'hinted'


# Eiger 1M using internal trigger
eiger1m_single = EigerSingleTrigger('XF:04IDD-ES{Det:Eig1M}',
                                    name='eiger1m_single')

set_eiger_defaults(eiger1m_single)

db.reg.register_handler('AD_EIGER2', EigerHandlerDask, overwrite=True)

