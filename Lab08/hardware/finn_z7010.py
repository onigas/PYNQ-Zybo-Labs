"""FINN Docker: initial feasibility build for GTSRB CNV on Z-7010.

NOT TESTED on a FINN host; resource feasibility remains unknown.
Generates estimated reports and stitched IP, NOT a ready-to-run bitstream.
Based on Xilinx/finn-examples/build/gtsrb/build.py.
"""
from pathlib import Path
import os
import finn.builder.build_dataflow as build
import finn.builder.build_dataflow_config as cfgmod
from finn.builder.build_dataflow_config import default_build_dataflow_steps
from qonnx.core.datatype import DataType
import numpy as np
from onnx import helper as oh

here = Path(__file__).resolve().parent
model_path = here.parent / 'models' / 'cnv_1w1a_gtsrb.onnx'
assert model_path.is_file(), 'Missing ' + str(model_path)


def add_preproc(model, cfg):
    # Same input pre-processing step as Xilinx's official GTSRB build:
    # accept raw uint8 RGB and divide by 255 in generated dataflow.
    old_input = model.graph.input[0].name
    new_name = model.make_new_valueinfo_name()
    div_init = model.make_new_valueinfo_name()
    model.set_initializer(div_init, np.asarray(255.0, dtype=np.float32))
    model.graph.node.insert(0, oh.make_node('Div', [old_input, div_init], [new_name], name='PreprocDiv'))
    model.graph.node[1].input[0] = new_name
    model.set_tensor_datatype(old_input, DataType.UINT8)
    return model

build_cfg = cfgmod.DataflowBuildConfig(
    output_dir=str(here / 'out_z7010'),
    fpga_part='xc7z010clg400-1',
    synth_clk_period_ns=10.0,
    target_fps=10,
    folding_config_file=str(here / 'folding_z7010.json'),
    steps=[add_preproc] + default_build_dataflow_steps,
    specialize_layers_config_file=str(here / 'specialize_gtsrb.json'),
    generate_outputs=[
        cfgmod.DataflowOutputType.ESTIMATE_REPORTS,
        cfgmod.DataflowOutputType.STITCHED_IP,
        cfgmod.DataflowOutputType.PYNQ_DRIVER,
    ],
)
print('Target FPGA: xc7z010clg400-1 — resource estimates only')
build.build_dataflow_cfg(str(model_path), build_cfg)
