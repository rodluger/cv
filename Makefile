LATEX       = xelatex
BIB         = biber
BASH        = bash -c
ECHO        = echo
RM          = rm -rf
TMP_SUFFS   = aux bbl blg log dvi ps eps out
RM_TMP      = ${RM} $(foreach suff, ${TMP_SUFFS}, *.${suff})
CHECK_RERUN = grep Rerun $*.log
ALL_FILES = cv.pdf cv_nopubs.pdf cv_onepage.pdf publications.pdf

all: update ${ALL_FILES}

update:
	python get_pubs.py --clobber
	python get_metrics.py --clobber
	python get_git.py --clobber
	python write_tex.py
	python make_plots.py

luger_cv.pdf: luger_cv.tex luger-cv.cls pubs.tex talks.tex
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv "\input{luger_cv}"
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv "\input{luger_cv}"

luger_cv_academic.pdf: luger_cv_academic.tex luger-cv.cls pubs.tex talks.tex
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv "\input{luger_cv_academic}"
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv "\input{luger_cv_academic}"

download:
	# Get updated JSON files
	git clone https://github.com/rodluger/cv && cd cv && git fetch && git checkout master-pdf && cp *.json ../ && cp citedates.txt ../ && cd .. && rm -rf cv

	# Write aux tex file & make plots
	python write_tex.py
	python make_plots.py

clean:
	${RM_TMP} ${ALL_FILES}
	${RM} talks.tex pubs_summary.tex pubs.tex
