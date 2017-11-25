\ProvidesClass{luger-cv}[2017/11/02 CV class]
\NeedsTeXFormat{LaTeX2e}

\DeclareOption{print}{\def\@cv@print{}}
\DeclareOption*{%
  \PassOptionsToClass{\CurrentOption}{article}%
}
\ProcessOptions\relax
\LoadClass{article}

\RequirePackage{ifthen}

%%%%%%%%%%
% Colors %
%%%%%%%%%%

\RequirePackage{xcolor}

\definecolor{numcolor}{rgb}{0.5,0.5,0.5}

\definecolor{white}{RGB}{255,255,255}

\definecolor{darkgray}{HTML}{333333}
\definecolor{gray}{HTML}{4D4D4D}
\definecolor{lightgray}{HTML}{999999}

\definecolor{green}{HTML}{C2E15F}
\definecolor{orange}{HTML}{FDA333}
\definecolor{purple}{HTML}{D3A4F9}
\definecolor{red}{HTML}{FB4485}
\definecolor{blue}{HTML}{6CE0F1}

\ifdefined\@cv@print
  \colorlet{green}{gray}
  \colorlet{orange}{gray}
  \colorlet{purple}{gray}
  \colorlet{brown}{gray}
  \colorlet{red}{gray}
  \colorlet{blue}{gray}
  \colorlet{fillheader}{white}
  \colorlet{header}{gray}
\else
  \colorlet{fillheader}{gray}
  \colorlet{header}{white}
\fi
\colorlet{textcolor}{gray}
\colorlet{headercolor}{gray}


%%%%%%%%%%
% MISC   %
%%%%%%%%%%

% Text formatting.
\newcommand{\foreign}[1]{\textit{#1}}
\newcommand{\etal}{\foreign{et~al.}}
\newcommand{\project}[1]{\textsl{#1}}
\definecolor{grey}{rgb}{0.5,0.5,0.5}
\newcommand{\deemph}[1]{\textcolor{grey}{\footnotesize{#1}}}

% literature links--use doi if you can
\newcommand{\doi}[2]{\emph{\href{http://dx.doi.org/#1}{{#2}}}}
\newcommand{\ads}[2]{\href{http://adsabs.harvard.edu/abs/#1}{{#2}}}
\newcommand{\arxiv}[2]{\emph{\href{http://arxiv.org/abs/#1}{{#2}}}}
\newcommand{\isbn}[1]{{\footnotesize(\textsc{isbn:}{#1})}}

% Citation count arrow
\newcommand{\citearrow}[0]{
\begin{minipage}[l]{\linewidth}
\hspace{-0.65in}
\raisebox{0.3em}{\footnotesize citations}
\rotatebox[origin=c]{270}{\textcolor{grey}{$\Rsh$}}
\end{minipage}\hfill
}

% Journal names.
\newcommand{\aj}{AJ}
\newcommand{\apj}{ApJ}
\newcommand{\pasp}{PASP}
\newcommand{\mnras}{MNRAS}

%%%%%%%%%
% Fonts %
%%%%%%%%%

\RequirePackage[quiet]{fontspec}
\RequirePackage[math-style=TeX,vargreek-shape=unicode]{unicode-math}

\newfontfamily\bodyfont[]{Helvetica Neue}
\newfontfamily\thinfont[]{Helvetica Neue UltraLight}
\newfontfamily\headingfont[]{Helvetica Neue Condensed Bold}

\defaultfontfeatures{Mapping=tex-text}
\setmainfont[Mapping=tex-text, Color=textcolor]{Helvetica Neue Light}

%%%%%%%%%%
% Header %
%%%%%%%%%%

\RequirePackage{tikz}

\newcommand{\rolefont}{%
  \fontsize{14pt}{24pt}\selectfont%
  \thinfont%
  \color{white}%
}

\newcommand{\header}[2]{%
  \begin{tikzpicture}[remember picture,overlay]
    \node [rectangle, fill=white, anchor=north, minimum width=\paperwidth,
           minimum height=4cm] (box) at (current page.north)
           {\includegraphics[width=\paperwidth]{header.pdf}};
    \node [anchor=center] (name) at (box) {%
      \fontsize{40pt}{72pt}\color{gray}%
      \raisebox{3em}{{\headingfont #1 #2}}
    };
  \end{tikzpicture}
  \vspace{2.333cm}
  \vspace{-2\parskip}
}


%%%%%%%%%%%%%
% Structure %
%%%%%%%%%%%%%
\RequirePackage{parskip}

\renewcommand{\section}[1]{
  \par\vspace{\parskip}
  {%
    \LARGE\headingfont\color{headercolor}%
    #1%
  }
  \par\vspace{\parskip}
}

\renewcommand{\subsection}[1]{
  \par\vspace{.5\parskip}%
  {\Large\headingfont\color{headercolor} #1}
  \par\vspace{.25\parskip}%
}

\renewcommand{\subsubsection}[2]{
  \par\vspace{.5\parskip}%
  {\Large\headingfont\color{headercolor} #2}
  \par\vspace{.25\parskip}%
}

\pagestyle{empty}


%%%%%%%%%%%%%%%%%%%%
% List environment %
%%%%%%%%%%%%%%%%%%%%

\setlength{\tabcolsep}{0pt}
\newenvironment{entrylist}{%
  \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}ll}
}{%
  \end{tabular*}
}
\renewcommand{\bfseries}{\headingfont\color{headercolor}}
\newcommand{\entry}[4]{%
  #1&\parbox[t]{11.8cm}{%
    \textbf{#2}%
    \hfill%
    {\footnotesize\addfontfeature{Color=lightgray} #3}\\%
    #4\vspace{\parsep}%
  }\\}

% Set up the custom unordered list.
\newcommand{\cvlist}{%
    \rightmargin=0in
    \leftmargin=0.15in
    \topsep=0em
    \partopsep=0pt
    \itemsep=0ex
    \parsep=0pt
    \itemindent=0\leftmargin
    \listparindent=0\leftmargin
    \settowidth{\labelsep}{~}
}

\newcommand{\pubslist}{%
    \rightmargin=0in
    \leftmargin=0.15in
    \topsep=0ex
    \partopsep=0pt
    \itemsep=1.25ex
    \parsep=0pt
    \itemindent=-1.0\leftmargin
    \listparindent=0.0\leftmargin
    \settowidth{\labelsep}{~}
}

%%%%%%%%%%%%%%
% Side block %
%%%%%%%%%%%%%%

\RequirePackage[overlay]{textpos}
\setlength{\TPHorizModule}{1cm}
\setlength{\TPVertModule}{1cm}
\newcommand{\aside}[3]{
    \begin{textblock}{3.6}(-4.5, #2)
        \begin{flushright}
            \section{#1}
                #3
        \end{flushright}
    \end{textblock}
}

%%%%%%%%%%%%%%%%
% Other tweaks %
%%%%%%%%%%%%%%%%

\RequirePackage[left=6.1cm,top=2cm,right=1.5cm,bottom=2.5cm,nohead,nofoot]{geometry}
\RequirePackage{hyperref}
\hypersetup{
    colorlinks=false,
    linkcolor=red,
    citecolor=red,
    filecolor=red,
    urlcolor = red}

% A fix for \href{}{} colors not working with fontspec
\makeatletter
\def\HyColor@@@@UseColor#1\@nil{\addfontfeatures{Color=#1}}
\makeatother