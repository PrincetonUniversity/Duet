# ${FABRIC} should be set by parent script

PYTHON         ?= python
APP         := $(shell basename $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST)))))
FABRIC_DIR     := ${DV_ROOT}/design/chip/tile/prga/fabric/${FABRIC}
PICKLED_CTX := ${FABRIC_DIR}/ctx.pkl
FLIST         := Flist.${APP}
CONFIG         := config.yaml
EBLIF         := ${APP}.eblif
VPR_LOG     := vpr/vpr_stdout.log
BITSTR_RAW     := bitgen.out
BITSTR_H     := ${DV_ROOT}/verif/diag/assembly/include/prga/${APP}_bitstr.h

.PHONY: all bitgen syn pnr clean

all: ${FLIST}

bitgen: ${BITSTR_H}

syn: $(EBLIF)

pnr: $(VPR_LOG)
	@echo "---- Performance model with VTR flagship 40nm FPGA ----"
	@echo Fmax: $(shell grep Fmax $< | grep Final | awk '{print $$(NF-1)}') MHz
	@echo Area: $(shell grep area $< | grep Total | grep -v used | awk '{print $$NF}' | python -c 'import fileinput; print(sum(map(float, fileinput.input())))') MWTA '(min. width transistor area = 9.6e-8 mm^2)'

clean:
	rm -rf syn.log include rtl vpr app ${EBLIF} ${FLIST} ${CONFIG}

${FLIST}: ${PICKLED_CTX}
	$(PYTHON) app.py $< $(APP)
	cp src/*.v rtl
	echo "+incdir+./include" > ${FLIST}
	for f in `ls rtl`; do echo "rtl/$$f" >> ${FLIST}; done
	for f in ${EXTRA_FABRIC_RTL_DEPS}; do echo ${FABRIC_DIR}/rtl/$$f >> ${FLIST}; done

${CONFIG}: ${FLIST}
	echo 'context: ${PICKLED_CTX}' > $@
	echo 'compiler: vcs' >> $@
	echo 'app:' >> $@
	echo '  name: ${APP}' >> $@
	echo '  sources:' >> $@
	for f in `tail -n +2 $<`; do echo "    - $$f" >> $@; done
	echo '  includes:' >> $@
	echo '    - ${FABRIC_DIR}/include' >> $@
	echo '    - include' >> $@
	echo '  defines:' >> $@
	echo '    PRGA_POSTPNR_NO_MEMINIT: null' >> $@
	echo 'constraints:' >> $@
	echo '  io: ${FABRIC_DIR}/constraints/io.pads' >> $@

$(EBLIF): ${FLIST}
	APP=${APP} yosys -c ${DV_ROOT}/design/chip/tile/prga/syn/syn.tcl | tee syn.log

$(VPR_LOG): $(EBLIF)
	$(PRGA_ROOT)/vtr/vtr_flow/scripts/run_vtr_flow.py $< \
		$(PRGA_ROOT)/vtr/vtr_flow/arch/timing/k6_frac_N10_frac_chain_mem32K_40nm.xml \
		-starting_stage vpr \
		-delete_intermediate_files \
		-delete_result_files \
		-temp_dir vpr \
		--place_chan_width 120 \
		--route_chan_width 120

app: $(CONFIG)
	$(PYTHON) -O -m prga.tools.wizard $<

${BITSTR_RAW}: app
	$(MAKE) -C $< bitgen
	cp app/bitgen.out $@

${BITSTR_H}: ${BITSTR_RAW}
	prgamemh2h $< > $@
