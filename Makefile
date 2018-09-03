LATEX       = xelatex
BIB         = biber
BASH        = bash -c
ECHO        = echo
RM          = rm -rf

TMP_SUFFS   = aux bbl blg log dvi ps eps out
RM_TMP      = ${RM} $(foreach suff, ${TMP_SUFFS}, *.${suff})

CHECK_RERUN = grep Rerun $*.log

ALL_FILES = cv.pdf cv_nopubs.pdf cv_onepage.pdf

all: update ${ALL_FILES}

update:
	python get_pubs.py
	python write_tex.py
	python make_plots.py

cv.pdf: cv.tex luger-cv.cls pubs.tex talks.tex
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv "\def\withpubs{}\def\withother{}\def\withtalks{}\input{cv}"
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv "\def\withpubs{}\def\withother{}\def\withtalks{}\input{cv}"

cv_nopubs.pdf: cv.tex luger-cv.cls
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv_nopubs "\def\withother{}\input{cv}"
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv_nopubs "\def\withother{}\input{cv}"

cv_onepage.pdf: cv.tex luger-cv.cls
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv_onepage "\def\onepage{}\input{cv}"
	${LATEX} -interaction=nonstopmode -halt-on-error -jobname=cv_onepage "\def\onepage{}\input{cv}"

clean:
	${RM_TMP} ${ALL_FILES}
	${RM} talks.tex pubs_summary.tex pubs.tex
