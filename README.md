# Cadwiki Overleaf Tutorial
* Why to use Overleaf (collab, version control, formatting, separate content vs styles, citations in figures). Problems with it (no grammar check). Alternatives (local install, word).
* Why exporting from Matlab is tedious. Also why Visio is terrible

This document describes how to use Overleaf to generate clean vector graphic plots and diagrams, as well as preparing references for IEEE style compliance.



### Contents
* [General formatting](#general-formatting)
* [Basic setup](#basic-setup)
* [Preparing figures: plots](#preparing-figures-plots)
* [Generating clean circuit diagrams](#preparing-figures-circuit-diagrams)
* [Generating other figures](#other-figure-types)
* [Preparing references](#preparing-references)
* [Other tips](#other-tips)
* [Helpful links](#other-references)

Scripts discussed here and further documentation are available in the [doc/](doc/) folder.


### Example project
All of the examples shown here are implemented in the following Overleaf document, formatted for a generic IEEE conference (except ISSCC, which has its own format). 

* This example follows IEEE conference format (link to it; note this excludes ISSCC), but there are also templates for journals (link to it). Same ideas apply, you mostly just change the preamble.
[See the Overleaf document here](https://www.overleaf.com/read/qznyrkjntprq)


## General formatting
* General concept: separate formatting from content (goes along with plotting approach)
 * examples: font size (https://www.sascha-frank.com/latex-font-size.html) (likely used in figures)
* Custom commands: Makes it easier to reformat parts of the page
* Colors: good vs bad, colorblind, dashed on top of solid


## Basic setup
* Basics on the IEEE style (link to original)

In keeping with the separation between style and content, I use the following file structure:
* `bib/` contains the bibliography (BibTeX) file(s).
* `data/` contains all data to be plotted, in `.csv` format.
* `fig/` contains TeX files which generate the figures.
* `ieee/` contains IEEE-provided styles. (It is possible on Overleaf to create a workspace which automatically references these IEEE styles, but I found when copying a project it lost some references. I recommend manually providing these files, which will also allow you to compile locally if desired.)
* `main.tex` contains the actual text of the paper, and imports the figure TeX files from `fig/`.
* `preamble.tex` is where I import and configure packages, define custom commands, and other preamble.

Note that this project has an extra folder `doc/` and this file `README.md` which are only for documentation and providing helpful scripts.

To include the preamble in your main file, use `\include` (similarly to include figures). `main.tex` looks like this:
```latex
\documentclass[conference]{IEEEtran}
\input{preamble.tex}
\begin{document}
% Content goes here
\end{document}
```


## Preparing figures: plots
* PGFPlots: overview of what it can do (list some of the plot types, link to documentation)

To use pgfplots, include the following in your preamble. Note that this says you want compatibility with version 1.9 (currently the latest version, I believe).
```latex
\usepackage{pgfplots}
\pgfplotsset{compat=1.9}
\usetikzlibrary{pgfplots.groupplots}
```


### Data preparation
Before plotting, you need to save your data to file. In this example I will show how to export to CSV from Matlab, but PGFPlots can also import other file types (see the documentation if you're interested). 

By using a cell array to save the data, it is easy to have columns of different lengths (not taken advantage of in this example). This full script is at [doc/scripts/cadwiki_example.m](doc/scripts/cadwiki_example.m).
```matlab
%% Save to CSV file
% Create cell array to hold our data. Set it to the maximum size you might
% want: in this case, I need 5 columns (x, sq, sq1, sq3, sq5) and am 
% allowing for up to 1000 data points.
data = cell(1000, 5);
% Set the header row
data(1,:) = {'x', 'sq', 'sq1', 'sq3', 'sq5'};
% Set the data
data(2:1+length(x),1) = num2cell(x);
data(2:1+length(sq),2) = num2cell(sq);
data(2:1+length(sq1),3) = num2cell(sq1);
data(2:1+length(sq3),4) = num2cell(sq3);
data(2:1+length(sq5),5) = num2cell(sq5);
% Get rid of extra empty rows (in this case, it reduces to 201 rows)
data=data(~all(cellfun(@isempty,data),2),:);
% Save to CSV file
T = cell2table(data(2:end,:),'VariableNames',data(1,:));
writetable(T,'cadwiki_example.csv')
```

The CSV file will look something like the following (only the first few lines are shown). The first line contains text that identifies the contents of each column in order to be referenced in the LaTeX code. The data should all be numbers formatted as a general number. That is, `123456.789` instead of `1.23456789e5`. Also, when preparing your data, consider how many data points are actually required: typically a few hundred should be sufficient and exceeding this (>1000) can increase LaTeX compile time. The full CSV file is at [data/cadwiki_example.csv](data/cadwiki_example.csv).
```
x,sq,sq1,sq3,sq5
0,1,0,0,0
0.0100502512562814,1,0.0401943259304967,0.0803352430697792,0.120369470368499
0.0201005025125628,1,0.0803485852827736,0.160270538786003,0.239343306293108
0.0301507537688442,1,0.120422751417848,0.239409206221979,0.355553903386545
```


### Examples
To plot this, first copy that CSV file to the `data/` folder. Then, create a new file in the `fig/` folder in order to design the new figure. What follows is one example for making a plot, shown below. There are MANY more style options; see the manual (or StackOverflow) for more.

* TO DO: put a screenshot of the figure here

First, create an axis which we will then configure. This is equivalent to configuring both the "figure" and "axis" in Matlab, as well as a few other things (ex: legend). (This full TeX file is at [fig/single_plot.tex](fig/single_plot.tex).)
```latex
\begin{tikzpicture}
\begin{axis}[
	% Plot dimensions
	width=2in,
	height=2in,
	% Set font sizes to match your figure caption
	tick label style={font=\footnotesize},
	label style={font=\footnotesize},
	legend style={font=\footnotesize},
	% Axis labels, limits, tick marks, and grid lines. Limits and ticks will be auto-configurd if commented out.
	xlabel={Time (s)},
	ylabel={Amplitude (V)},
	xmin=0, xmax=2,
	ymin=-2, ymax=2,
	% xtick={-8, -4, 0, 4, 8},
	% ytick={-5, 0, 5},
	ymajorgrids=true,
	xmajorgrids=true,
	grid style=dashed,
	% Configure the legend
	% This sets the legend at the top center, just outside the plot. "Anchor" means that the southern point (i.e. bottom center) of the legend bounding box is set to the given coordinates.
	legend style={at={(0.50,1.00)}, anchor=south}, 
	% If -1, it will use a single row and as many columns as needed.
	legend columns=2,
	% Text alignment
	legend cell align={left},
	% Hide the border around the legend
	legend style={draw=none},
]
```

Then, create the plots. This is configured to read from a table separated by commas (i.e. CSV file), with a header row, and x-data found in column "x" and y-data found in column "sq".
```latex
\addplot[color=black,mark=none,style=very thick] table[col sep=comma,header=true,x=x,y=sq] {data/cadwiki_example.csv};
\addplot[color=blue,mark=none,style=very thick] table[col sep=comma,header=true,x=x,y=sq1] {data/cadwiki_example.csv};
\addplot[color=red,mark=none,style=very thick] table[col sep=comma,header=true,x=x,y=sq3] {data/cadwiki_example.csv};
\addplot[color=black,mark=none,style=densely dashed] table[col sep=comma,header=true,x=x,y=sq5] {data/cadwiki_example.csv};
```
Common plot style options are `color`, `mark` (`none`, `circle`, `square`, etc), and `style` (`very thick`, `solid`, `densely dashed`, etc). Other options are available in the [PGFPlots documentation](doc/external/pgfplots.pdf).

Lastly, create the legend. I felt that the first legend text was too close to the second, so I used `\phantom` to create some horizontal space. This isn't necessary, but looks nice. In addition, because your figures are created in LaTeX you can easily add citations.
```latex
\legend{Square wave\cite{Muratore2019}\phantom{--},Fundamental\phantom{--},Three harmonics\phantom{--},Five harmonics}
\end{axis}
\end{tikzpicture}
```

Instead of plotting all of these on a single plot, you could do a group plot with shared axes. The gist is that instead of `begin{axis}` you use `begin{groupplot}` and then include a configuration section to set the subplots:
```latex
    group style={
		% Name doesn't seem to matter (can probably be referenced somewhere)
        group name="analysis",
        group size=2 by 2,
        % Use shared x and y axes
        x descriptions at=edge bottom,
        y descriptions at=edge left,
		% Set spacing between plots
        horizontal sep=0.1in,
        vertical sep=0.1in,
    },
```
Then, use `\nextgroupplot` to increment which subplot you are adding to:
```latex
\nextgroupplot
\addplot[color=black,mark=none,style=very thick] table[col sep=comma,header=true,x=x,y=sq] {data/cadwiki_example.csv};
\addplot[color=blue,mark=none,style=very thick] table[col sep=comma,header=true,x=x,y=sq1] {data/cadwiki_example.csv};
\addplot[color=red,mark=none,style=very thick] table[col sep=comma,header=true,x=x,y=sq3] {data/cadwiki_example.csv};
\addplot[color=black,mark=none,style=densely dashed] table[col sep=comma,header=true,x=x,y=sq5] {data/cadwiki_example.csv};
\legend{Square wave\phantom{--},Fundamental\phantom{--},Three harmonics\phantom{--},Five harmonics}
\nextgroupplot
\addplot[color=blue,mark=none,style=very thick] table[col sep=comma,header=true,x=x,y=sq1] {data/cadwiki_example.csv};
\nextgroupplot
\addplot[color=red,mark=none,style=very thick] table[col sep=comma,header=true,x=x,y=sq3] {data/cadwiki_example.csv};
\nextgroupplot
\addplot[color=black,mark=none,style=densely dashed] table[col sep=comma,header=true,x=x,y=sq5] {data/cadwiki_example.csv};
```

* TO DO: show image of 2x2 array

This full TeX file for this example is at [fig/multi_plot.tex](fig/multi_plot.tex).


## Preparing figures: Circuit diagrams
* circuitikz: overview of some circuit elements it has (link to documentation)

To load circuitikz, include the following in the preamble. Note that this also does some global configuration.
```latex
\usepackage{circuitikz}
\tikzstyle{every path}=[line cap=round,line join=round]
\usetikzlibrary{calc}
```

### Example
* Show and explain a basic example
* Also show code for a more complicated example


## Other figure types
For timing diagrams, look into tikztiming ([here are some examples](http://www.texample.net/tikz/examples/more-tikz-timing-examples/)).


## Preparing references
References are all stored in a BibTeX file (`.bib`) and automatically ordered and formatted at compile time.
* TO DO: Brief overview of IEEE standards on this

For some reason the default IEEE style includes URLs in all references, which is usually not desired. To fix this, create `/bib/IEEEtransBSTCTL.bib` with the following text to disable URL use:
```bibtex
@IEEEtranBSTCTL{
	IEEEexample:BSTcontrol,
	CTLuse_url = "no",
}
```
This file can have many options to configure your references section; see the [documentation](./doc/external/IEEEtran_bst_HOWTO.pdf) for more options. In addition, the following line must appear before the first citation but after `\begin{document}` in order for that configuration to take effect.
```latex
\bstctlcite{IEEEexample:BSTcontrol}
```

As far as I can tell, there is no automatic way to split references easily between two columns (this is useful for ISCAS, for example, where the final page is exclusively references and they should be roughly evenly spread across the two columns). To split references, use the `\IEEEtriggeratref{x}` command, which will put reference `x` as the first reference on the new column.
```latex
\IEEEtriggeratref{13}
```
Then, create the bibliography using the IEEE abbreviated style, and including both your configuration and references files. File extensions are not needed.
```latex
\bibliographystyle{IEEEtran}
\bibliography{IEEEabrv,bib/IEEEtransBSTCTL,bib/cadwiki_example}
```

If your citations have any special characters, you may need to fix them. This should probably have been fixed in the BibTeX file, but this works too. (This replaces the given unicode characters with LaTeX-compatible code.)
```latex
\DeclareUnicodeCharacter{2052}{\%}
\DeclareUnicodeCharacter{00B5}{$\mu$}
```



### Export from Mendeley
I use Mendeley to manage my references and this makes BibTeX library generation easy: just select the desired set of papers and export as bib. However, the output file on its own will not format correctly. Here's an example of one entry from the output:
```bibtex
@article{Muratore2019,
author = {Muratore, Dante Gabriel and Tandon, Pulkit and Wootters, Mary and Chichilnisky, E. J. and Mitra, Subhasish and Murmann, Boris},
doi = {10.1109/TBCAS.2019.2935468},
issn = {1932-4545},
journal = {IEEE Transactions on Biomedical Circuits and Systems},
month = {dec},
number = {6},
pages = {1128--1140},
title = {{A Data-Compressive Wired-OR Readout for Massively Parallel Neural Recording}},
url = {https://ieeexplore.ieee.org/document/8801905/},
volume = {13},
year = {2019}
}
```

There are a few issues with this entry:
1. The article title has double curly brackets, meaning that capitalization will incorrectly remain as-is.
2. The journal name should be abbreviated for most IEEE publications.
3. The month has brackets, meaning that it will incorrectly be all-lowercase.

These can all be fixed easily and quickly with a Python script (it's written for Python 2.7; you may need to update for Python 3). This is a fairly dumb script which iterates over each line and fixes the errors, as described below. There is room for improvement. This script file is at [doc/scripts/fix_bib.py](doc/scripts/fix_bib.py).
```python
import fileinput
import re

x = []
for line in fileinput.input("cadwiki_example.bib", inplace=True):
```
First, fix the month line; this is easy.
```python
    # Fix months
    if line.startswith('month = {'):
        line = line.replace('{','').replace('}','')
```
Next, format journal names. IEEE uses keywords for journal names (see the full list [here](http://tug.ctan.org/tex-archive/biblio/bibtex/contrib/IEEEtran/IEEEfull.bib)). This way you can either load `IEEEabrv` or `IEEEfull` for an abbreviated or full bibliography, respectively. You might have to add additional journals here.
```python
    # Use IEEE format journal names
    if line.startswith('journal = {IEEE Transactions on Circuits and Systems I: Regular Papers},'):
        line = 'journal = IEEE_J_CASI_RP,\r\n'
    if line.startswith('journal = {IEEE Transactions on Circuits and Systems II: Express Briefs},'):
        line = 'journal = IEEE_J_CASII_EB,\r\n'
    if line.startswith('journal = {IEEE Transactions on Biomedical Circuits and Systems},'):
        line = 'journal = IEEE_J_BCAS,\r\n'
    if line.startswith('journal = {IEEE Journal of Solid-State Circuits},'):
        line = 'journal = IEEE_J_JSSC,\r\n'
```
I also included shortening for conference names (oddly called "booktitle" in the BibTeX file), following the IEEE style. This should be commented out if you are submitting to a journal that uses the `IEEEfull` style.
```python
    if line.startswith('booktitle = {'):
        line = line.replace('Conference', 'Conf.')
        line = line.replace('Proceedings of the', 'Proc.')
        line = line.replace('Proceedings of', 'Proc.')
        line = line.replace('Symposium', 'Symp.')
        line = line.replace('National', 'Nat.')
        line = line.replace('International', 'Int.')
```
Lastly, fix capitalization for article titles. The IEEE standard is to have sentence-case article titles, for example "A data-compressive wired-OR readout for massively parallel neural recording." To start, remove the extra set of curly brackets so that BibTeX can set the letter case.
```python
    # Fix titles: default no capitalization, except some specific words
    # Important: make sure all non-roman characters are in math (eg: mu should be $\mu$)
    if line.startswith('title = {'):
        line = line.replace('{{', '{').replace('}}', '}')
```
However, this would result in "A data-compressive wired-or readout for massively parallel neural recording," so there is some extra code to fix this. First, fix some known keywords like dB and Hz which would otherwise be formatted as "db" and "hz." Then, use regex to find all words which are all-caps and surround them in curly brackets. 
```python
        line = line.replace('dB','{dB}')
        line = line.replace('Hz','{Hz}')
        line = line.replace('mV','{mV}')
        line = line.replace('IoT','{IoT}')
        # Find all letters/words that are all caps, and standing on their own
        # Then replace them with {WORD} so that they're properly capitalized
        # TO DO: ignore anything already within {}
        # TO DO: Can I write this in a single line using re.sub? Seems inefficient to search, make a decision, then search again to replace
        words = re.split('[,-:+ {}\$(0-9)]', line.strip().strip('title = '))
        for word in words:
            if word == word.upper() and len(word) > 0 and word.isalnum():
                line = re.sub('(?P<a>[,-:+ {}\$(0-9)])('+word+u')(?P<b>[,-:+ {}\$(0-9)])', '\g<a>{' + word + '}\g<b>', line)
                x.append([word, line])
                
    print line,

for y in x:
    print(y)
```

The example above has now been fixed as,
```bibtex
@article{Muratore2019,
author = {Muratore, Dante Gabriel and Tandon, Pulkit and Wootters, Mary and Chichilnisky, E. J. and Mitra, Subhasish and Murmann, Boris},
doi = {10.1109/TBCAS.2019.2935468},
issn = {1932-4545},
journal = IEEE_J_BCAS,
month = dec,
number = {6},
pages = {1128--1140},
title = {{A} Data-Compressive Wired-{OR} Readout for Massively Parallel Neural Recording},
url = {https://ieeexplore.ieee.org/document/8801905/},
volume = {13},
year = {2019}
}
```
(The curly brackets around "A" in the title aren't necessary, but are a result of my simple method of fixing capitalization.)


## Other tips

### Tables
If you want to create a table with footnotes, I recommend the `threeparttable` package. To use this, include it in `preamble.tex`. I've also included some other useful table packages here.
```latex
\usepackage{tabularx}
\usepackage{multirow}
\usepackage[flushleft]{threeparttable}
```

Here is an example of it in use. This is an example of using custom commands to separate formatting from content: I can easily change the "yes" and "no" icons, and footnote labels, without touching the table environment.
```latex
%% Some custom commands I made in preamble.tex, to make the table more readable
\usepackage{pifont}
\newcommand{\n}[1][]{\phantom{$^{#1}$}-$^{#1}$}
\newcommand{\y}[1][]{\phantom{$^{#1}$}\ding{51}$^{#1}$}

%% Here is the table
\begin{table}[!t]
\centering
\begin{threeparttable}
% increase table row spacing, adjust to taste
\renewcommand{\arraystretch}{1.25}
\setlength\tabcolsep{0.24em}
\caption{Example of a Table With Checkboxes}
\label{table_example}
\centering
\begin{tabular}{l|ccccc}
\vspace{-0.3em}
Method & Item 1 & Item 2 & Item 3 & Item 4 & Item 5 \tabularnewline
\hline
First method \cite{Andrews2012,Andrews2010a} & \y[1] & \y & \y[2] & \n & \n \tabularnewline
Second method \cite{Muratore2019} & \n & \y & \y[2] & \y & \n \tabularnewline
Third method \cite{Kwon2018,Maas2003} & \y[3] & \n & \n & \y & \n \tabularnewline
Fourth method \cite{Hameed2018,Hameed2015,Hammler2014} & \y[1] & \y & \y[2] & \y & \y \tabularnewline
Fifth method \cite{Klumperink2017} & \y & \y & \n & \y & \y \tabularnewline
\end{tabular}
\begin{tablenotes}
\scriptsize
  \item $^1$A tabular footnote.
  \item $^2$Another tabular footnote.
  \item $^3$Another tabular footnote.
\end{tablenotes}
\end{threeparttable}
\end{table}
```

### White space

* include ack, include white space for authors/affiliations (if redacted for first submission). Can set spacing around various things: figures, equations, before each section/subsection


## Other references
* useful links. including all manuals (ieee style guides, pgfplots, circuitikz, etc) and latex help pages
* refer to doc/external/ folder which contains a bunch of these
https://www.ieee.org/conferences/publishing/templates.html
https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/authoring-tools-and-templates/ieee-article-templates/