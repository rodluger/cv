LATEX       = xelatex
BIB         = biber
BASH        = bash -c
ECHO        = echo
RM          = rm -rf

TMP_SUFFS   = aux bbl blg log dvi ps eps out
RM_TMP      = ${RM} $(foreach suff, ${TMP_SUFFS}, *.${suff})

CHECK_RERUN = grep Rerun $*.log

ALL_FILES = cv.pdf cv_pubs.pdf

all: ${ALL_FILES}

cv.pdf: cv.tex luger-cv.cls
	${LATEX} cv
	${LATEX} cv

cv_pubs.pdf: cv.tex luger-cv.cls pubs.tex
	${LATEX} -jobname=cv_pubs "\def\withpubs{}\input{cv}"
	${LATEX} -jobname=cv_pubs "\def\withpubs{}\input{cv}"

clean:
	${RM_TMP} ${ALL_FILES}
