PYTHON ?= python
PICKLED_CTX := ctx.pkl

.PHONY: all clean
all: $(PICKLED_CTX)

$(PICKLED_CTX): fabric.py
	$(PYTHON) $< | tee fabric.log

clean:
	rm -rf *.pkl rtl include syn vpr constraints fabric.log
