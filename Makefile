LATEX       = xelatex
BIB         = biber
BASH        = bash -c
ECHO        = echo
RM          = rm -rf
TMP_SUFFS   = aux bbl blg log dvi ps eps out
RM_TMP      = ${RM} $(foreach suff, ${TMP_SUFFS}, *.${suff})
CHECK_RERUN = grep Rerun $*.log
ALL_FILES = cv.pdf cv_nopubs.pdf cv_onepage.pdf publications.pdf

# Environment variables; set these in the commit message!
CITATION_SKIP = $(shell python get_env.py CITATION_SKIP 2.36)
CITATION_SKIP_PUBS = $(shell python get_env.py CITATION_SKIP_PUBS 3.85)

all: update ${ALL_FILES}

update:
	python get_pubs.py
	python get_metrics.py
	python get_git.py
	python write_tex.py
	python make_plots.py

cv.pdf: cv.tex luger-cv.cls pubs.tex talks.tex
	echo "\\\newcommand\\\citationskip{${CITATION_SKIP}}" > citationskip.tex
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv "\def\withpubs{}\def\withother{}\def\withtalks{}\input{cv}"
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv "\def\withpubs{}\def\withother{}\def\withtalks{}\input{cv}"

cv_nopubs.pdf: cv.tex luger-cv.cls
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv_nopubs "\def\withother{}\input{cv}"
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv_nopubs "\def\withother{}\input{cv}"

cv_onepage.pdf: cv.tex luger-cv.cls
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv_onepage "\def\onepage{}\input{cv}"
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv_onepage "\def\onepage{}\input{cv}"

publications.pdf: cv_pubs.tex luger-cv.cls
	echo "\\\newcommand\\\citationskip{${CITATION_SKIP_PUBS}}" > citationskip.tex
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv_pubs "\input{cv_pubs}"
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv_pubs "\input{cv_pubs}"

download:
	# Get updated JSON files
	git clone https://github.com/rodluger/cv && cd cv && git fetch && git checkout master-pdf && cp *.json ../ && cp citedates.txt ../ && cd .. && rm -rf cv

	# Write aux tex file & make plots
	python write_tex.py
	python make_plots.py

local:

	python write_tex.py
	python make_plots.py

	# cv.pdf
	echo "\\\newcommand\\\citationskip{${CITATION_SKIP}}" > citationskip.tex
	echo "\def\withpubs{}\def\withother{}\def\withtalks{}\input{cv}" | tectonic "-"
	mv texput.pdf cv.pdf

	# cv_nopubs.pdf
	echo "\def\withother{}\input{cv}" | tectonic "-"
	mv texput.pdf cv_nopubs.pdf

	# cv_onepage.pdf
	echo "\def\onepage{}\input{cv}" | tectonic "-"
	mv texput.pdf cv_onepage.pdf

	# publications.pdf
	echo "\\\newcommand\\\citationskip{${CITATION_SKIP_PUBS}}" > citationskip.tex
	echo "\input{cv_pubs}" | tectonic "-"
	mv texput.pdf publications.pdf

clean:
	${RM_TMP} ${ALL_FILES}
	${RM} talks.tex pubs_summary.tex pubs.tex
