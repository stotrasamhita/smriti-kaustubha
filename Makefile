# Local builds. See pdf/README.md and tools/ for what each step does.
SECTION ?= caitra-krtyam
PDFNAME ?= sk-caitra-pilot

.PHONY: all validate generated pdf site serve clean

all: validate generated pdf site

validate:
	python3 tools/validate.py

generated:
	python3 tools/build_pages.py > data/pages.toml
	python3 tools/checklist.py $(SECTION) > docs/proofreading/$(SECTION).md

pdf:
	python3 tools/build_pdf.py --section $(SECTION) --name $(PDFNAME)

site: pdf
	hugo --minify
	mkdir -p public/pdf && cp build/pdf/$(PDFNAME).pdf public/pdf/
	npx --yes pagefind@1.5.2 --site public

serve:
	hugo server

clean:
	rm -rf build public resources/_gen .hugo_build.lock
