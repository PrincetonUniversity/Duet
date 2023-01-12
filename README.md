# Duet-Dolly (OpenPiton x PRGA) Research Platform

This repo hosts Dolly, the RTL model of Duet, a tightly-integrated,
manycore-FPGA architecture.
Duet promotes the embedded FPGAs (eFPGA) as equal peers with processors on
the on-chip network and enables fine-grained, reconfigurable hardware
acceleration.

A paper on Duet has been accepted to HPCA 2023 (
[arXiv preprint](https://arxiv.org/abs/2301.02785)):

```
Ang Li, August Ning, and David Wentzlaff.
"Duet: Creating Harmony between Processors and Embedded FPGAs."
In Proceedings of the 29th IEEE International Symposium on High-Performance
Computer Architecture (HPCA-29), Feb 2023.
```

Duet-Dolly integrates [PRGA](https://github.com/PrincetonUniversity/prga) into
[OpenPiton](https://github.com/PrincetonUniversity/openpiton).
Please refer to the [OpenPiton Documentation](/OPENPITON_README.md) for
instructions related to OpenPiton, and the [PRGA
Documentation](https://prga.readthedocs.io/en/latest/) for instructions
related to PRGA.

## Environment Setup

#### IMPORTANT NOTES

- Duet-Dolly is only tested with the Ariane core and the PyOCN on-chip
  network. Sparc/Pico or dynamic\_node are not supported.
- Ariane and PRGA are included as git submodules. Run `git submodule update
  --init --recursive` after cloning the repo to fetch the submodules.

#### Set up OpenPiton and Ariane

Please follow the instruction [here](/OPENPITON_README.md#environment-setup-1)
to set up OpenPiton and Ariane.

#### Set up PRGA

PRGA depends on [Yosys](https://github.com/YosysHQ/yosys) and
[VTR](https://github.com/verilog-to-routing/vtr-verilog-to-routing) to
generate bitstream for eFPGA-emulated reconfigurable accelerators.
To install the fully tested versions of these tools, run the following command
if you are running this for the first time:

```
cd $PITON_ROOT/piton/design/chip/tile/prga/prga
./envscr/install
```

## Running Duet Benchmarks

Duet-Dolly supports benchmarking at various levels of fidelity.
The RTL model could either instantiate the reconfigurable accelerator
(referred to as an "app" hereinafter) directly in the system, or instantiate
the eFPGA fabric, load the bitstream to emulate the app.
The former approach is called app-mocking and allows faster simulation.
The latter approach is more realistic, although it should not show any
performance difference.

Here we demonstrate how to run Duet Benchmarks with the `popcnt` example. 
The source code of the RTL for the accelerator is located at
[/piton/design/chip/tile/prga/app/popcnt](/piton/design/chip/tile/prga/app/popcnt).
The C test that calls this accelerator is located at
[/piton/verif/diag/c/prga/popcnt.c](/piton/verif/diag/c/prga/popcnt.c).

First, we need to set up the OpenPiton environment and activate the PRGA
virtual environment.

```
cd $PITON_ROOT
. ./piton/ariane_setup.sh
./piton/design/chip/tile/prga/prga/envscr/activate
```

Now we should be in a Python virtual environment. You can exit the environment
with the `deactivate` command.
Let us generate the RTL (and other necessary scripts) for the eFPGA fabric.
In this case we will be using `m2` ([/piton/design/chip/tile/prga/fabric/m2](/piton/design/chip/tile/prga/fabric/m2)),
an eFPGA fabric that has two sets of coherent memory interfaces.

```
cd $PITON_ROOT
cd piton/design/chip/tile/prga/fabric/m2
make
```

With all the information about the FPGA (e.g., port list, size, types and
numbers of available logic elements), the app RTL can be generated.

```
cd $PITON_ROOT
cd piton/design/chip/tile/prga/app/popcnt
make
```

Now we have the RTL of the app (`popcnt`), we can run app-mocking simulation.
To do so, we first build the simulator which instantiates the app directly
without the eFPGA fabric.

```
cd $PITON_ROOT/build
sims -sys=manycore -x_tiles=2 -y_tiles=2 \
    -prga=m2 -prga_mock_app=popcnt -prga_rxi_tile=1 -prga_yami_tiles=3 \
    -vcs_build
```

A few quick explanations:
- `-prga=m2` specifies the fabric to use. If you have other fabrics under
  [/piton/design/chip/tile/prga/fabric](/piton/design/chip/tile/prga/fabric), you can choose them instead
- `-prga_mock_app=popcnt` specifies the mock app to instantiate. If you have
  other apps under [/piton/design/chip/tile/prga/app](/piton/design/chip/tile/prga/app), you can choose them
  instead
- `-x_tiles=2 -y_tiles=2` is necessary in this case, since the fabric `m2`
  requires two on-chip network access points (routers) for the two coherent
  memory interfaces.
- `-prga_rxi_tile=1` places the RXI tile at tile 1, that is, tile (1, 0).
  Each RXI tile contains one control register interface and one coherent
  memory interface.
  Each system can only have one RXI tile.
- `-prga_yami_tiles=3` places one YAMI tile at tile 3, that is, tile (1, 1).
  Each YAMI tile contains one coherent memory interface.
  The number of YAMI tiles required is equal to the number of memory
  interfaces of the fabric minus one (because of the RXI tile).

To run the test, run:

```
cd $PITON_ROOT/build
sims -sys=manycore -x_tiles=1 -y_tiles=1 \
    -prga=m2 -prga_mock_app=popcnt -prga_rxi_tile=1 -prga_yami_tiles=3 \
    -rtl_timeout=100000000 -vcs_run popcnt.c
```

A few quick explanations:
- Note the options are now `-x_tiles=1 -y_tiles=1`.
  This specifies the number of active cores to be 1 (although the system has
  two cores -- 4 tiles, minus one RXI tile, minus one YAMI tile, then one core
  per tile).

If you wish to instantiate the eFPGA fabric and simulate the complete
bitstream loading and LUT-based emulation process (which takes much longer!),
we need to generate the bitstream first:

```
cd $PITON_ROOT
cd piton/design/chip/tile/prga/app/popcnt
make bitgen
```

These commands will generate the bitstream, convert to a static C array, and
generate a header ("popcnt\_bitstr.h") in
[/piton/verif/diag/assembly/include/prga](/piton/verif/diag/assembly/include/prga).

We then build the simulator that instantiates the eFPGA fabric without the
mock app.

```
cd $PITON_ROOT/build
sims -sys=manycore -x_tiles=2 -y_tiles=2 \
    -prga=m2 -prga_rxi_tile=1 -prga_yami_tiles=3 \
    -vcs_build
```

The simulation command is similar to the app-mocking flow, but be sure to
increase the value for `rtl_timeout`:

```
cd $PITON_ROOT/build
sims -sys=manycore -x_tiles=1 -y_tiles=1 \
    -prga=m2 -prga_rxi_tile=1 -prga_yami_tiles=3 \
    -rtl_timeout=10000000000 -vcs_run popcnt.c
```
