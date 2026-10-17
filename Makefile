# Local builds. See pdf/README.md and tools/ for what each step does.
SECTIONS ?= caitra-krtyam vaisakha-krtyam jyestha-krtyam ashadha-krtyam
# One PDF for all finished months of the Saṃvatsara-dīdhiti; its name stays stable as months are added.
PDFNAME ?= sk-samvatsara
comma := ,
empty :=
space := $(empty) $(empty)
SECTIONLIST := $(subst $(space),$(comma),$(SECTIONS))

.PHONY: all validate generated pdf site serve clean

all: validate generated pdf site

validate:
	python3 tools/validate.py

generated:
	python3 tools/build_pages.py > data/pages.toml
	for s in $(SECTIONS); do python3 tools/checklist.py $$s > docs/proofreading/$$s.md; done

# Reading copy (corrections silent, logged in build/pdf/$(PDFNAME)-corrections.tsv) and proof copy.
pdf:
	python3 tools/build_pdf.py --section $(SECTIONLIST) --name $(PDFNAME)
	python3 tools/build_pdf.py --section $(SECTIONLIST) --name $(PDFNAME)-draft --draft

site: pdf
	hugo --minify
	mkdir -p public/pdf && cp build/pdf/$(PDFNAME).pdf build/pdf/$(PDFNAME)-draft.pdf build/pdf/$(PDFNAME)-corrections.tsv public/pdf/
	# Keep the address of the Caitra–Vaiśākha copy that was circulated earlier working.
	cp build/pdf/$(PDFNAME).pdf public/pdf/sk-caitra-vaisakha.pdf
	cp build/pdf/$(PDFNAME)-draft.pdf public/pdf/sk-caitra-vaisakha-draft.pdf
	npx --yes pagefind@1.5.2 --site public

serve:
	hugo server

clean:
	rm -rf build public resources/_gen .hugo_build.lock
