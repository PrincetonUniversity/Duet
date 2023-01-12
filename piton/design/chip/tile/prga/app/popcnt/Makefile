PYTHON?=python
CURDIR:=$(shell basename $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST)))))
PICKLED_CTX := ${DV_ROOT}/design/chip/tile/prga/fabric/m2/ctx.pkl
FLIST := Flist.${CURDIR}
CONFIG := config.yaml
EBLIF := $(CURDIR).eblif
VPR_LOG := vpr/vpr_stdout.log

.PHONY: all clean backup clean-backup recover

all: ${PICKLED_CTX}
	$(PYTHON) app.py $< $(CURDIR)
	cp src/*.v rtl
	echo "+incdir+./include" > ${FLIST}
	for f in `ls rtl`; do echo "rtl/$$f" >> ${FLIST}; done
	echo $(shell dirname ${PICKLED_CTX})/rtl/prga_fifo_resizer.v >> ${FLIST}

app: $(CONFIG)
	$(PYTHON) -O -m prga.tools.wizard $<

syn: $(EBLIF)

pnr: $(VPR_LOG)

clean:
	rm -rf include rtl app

$(EBLIF):
	APP=${CURDIR} yosys -c ${DV_ROOT}/design/chip/tile/prga/syn/syn.tcl | tee syn.log

$(VPR_LOG): $(EBLIF)
	$(PRGA_ROOT)/vtr/vtr_flow/scripts/run_vtr_flow.py $< \
		$(PRGA_ROOT)/vtr/vtr_flow/arch/timing/k6_frac_N10_frac_chain_mem32K_40nm.xml \
		-starting_stage vpr \
		-delete_intermediate_files \
		-delete_result_files \
		-temp_dir vpr \
		--place_chan_width 120 \
		--route_chan_width 120
