from ophyd import (
    ProsilicaDetector,
    SingleTrigger,
    ImagePlugin,
    StatsPlugin,
    ROIPlugin,
    TransformPlugin,
    ProcessPlugin,
)
from ophyd import Component as Cpt


class StandardProsilica(SingleTrigger, ProsilicaDetector):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("labels", ["cameras"])
        super().__init__(*args, **kwargs)

    # tiff = Cpt(FileStoreIterativeWrite,
    #            suffix='TIFF1:',
    #            write_path_template='/XF04ID/data/%Y/%m/%d',
    #            root='/XF04ID/data/')
    image = Cpt(ImagePlugin, "image1:")
    stats1 = Cpt(StatsPlugin, "Stats1:")
    stats2 = Cpt(StatsPlugin, "Stats2:")
    stats3 = Cpt(StatsPlugin, "Stats3:")
    stats4 = Cpt(StatsPlugin, "Stats4:")
    stats5 = Cpt(StatsPlugin, "Stats5:")
    trans1 = Cpt(TransformPlugin, "Trans1:")
    roi1 = Cpt(ROIPlugin, "ROI1:")
    roi2 = Cpt(ROIPlugin, "ROI2:")
    roi3 = Cpt(ROIPlugin, "ROI3:")
    roi4 = Cpt(ROIPlugin, "ROI4:")
    proc1 = Cpt(ProcessPlugin, "Proc1:")


ccam = StandardProsilica("XF:04IDC-BI:1{Scr:3}", name="ccam")
vbd1 = StandardProsilica("XF:04IDA-BI:1{Scr:1}", name="vbd1")
vbd2 = StandardProsilica("XF:04IDA-BI:1{Scr:2}", name="vbd2")

for c in [ccam, vbd1, vbd2]:
    c.read_attrs = ["stats1"]
    c.stats1.read_attrs = ["total"]
    c.configuration_attrs = ["cam.acquire_time"]
