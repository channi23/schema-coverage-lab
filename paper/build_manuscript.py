"""Create matching readable Markdown and portable LaTeX from reviewed prose."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
source = (ROOT/'manuscript.md').read_text()
dest = ROOT

def text_latex(s):
    tokens = []
    def protect(value):
        tokens.append(value)
        return '\x01'+str(len(tokens)-1)+'\x02'
    s = re.sub(r'\$([^$]+)\$', lambda m: protect('$'+m[1]+'$'), s)
    s = re.sub(r'`([^`]+)`', lambda m: protect('\\texttt{'+('\\allowbreak{}').join(escape(c) for c in m[1])+'}'), s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: protect('\\href{'+m[2].replace('%','\\%')+'}{'+escape(m[1])+'}'), s)
    s = re.sub(r'\[(\d+(?:,\d+)*)\]', lambda m: protect('\\cite{'+','.join('ref'+x for x in m[1].split(','))+'}'), s)
    s = re.sub(r'\*\*([^*]+)\*\*', lambda m: protect('\\textbf{'+escape(m[1])+'}'), s)
    s = escape(s)
    return re.sub(r'\x01(\d+)\x02', lambda m: tokens[int(m[1])], s)

def escape(s):
    mapping={'\\':'\\textbackslash{}','&':'\\&','%':'\\%','$':'\\$','#':'\\#','_':'\\_',
             '{':'\\{','}':'\\}','~':'\\textasciitilde{}','^':'\\textasciicircum{}'}
    return ''.join(mapping.get(c,c) for c in s)

preamble=r'''\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,booktabs,hyperref,graphicx,listings}
\hypersetup{colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue,pdftitle={Semantic Independence Coverage for JSON Schema},pdfauthor={Sri Hari Haran Sharma}}
\lstset{basicstyle=\ttfamily\footnotesize,breaklines=true,breakatwhitespace=false,columns=fullflexible,frame=single,keepspaces=true,showstringspaces=false}
\setlength{\emergencystretch}{2em}
\title{Semantic Independence Coverage for JSON Schema:\\A Bounded Reproducible Study}
\author{Sri Hari Haran Sharma\\\href{mailto:hariharansharma588@gmail.com}{\texttt{hariharansharma588@gmail.com}}}
\date{November 2026\\\small Research manuscript for author review}
\begin{document}
\maketitle
'''
out=[preamble]
lines=source.splitlines();i=0;paragraph=[];started=False;abstract=False;appendix=False
def flush():
    if paragraph:
        out.append(text_latex(' '.join(paragraph))+'\n\n');paragraph.clear()

while i<len(lines):
    line=lines[i]
    if not started:
        if line=='## Abstract':
            started=True;abstract=True;out.append('\\begin{abstract}\n')
        i+=1;continue
    if line.startswith('## '):
        flush()
        if abstract:
            out.append('\\end{abstract}\n');abstract=False
        heading=line[3:]
        if heading=='References':
            out.append('\\begin{thebibliography}{99}\n\\small\n\\raggedright\n')
            for ref in lines[i+1:]:
                m=re.match(r'\[(\d+)\] (.*)',ref)
                if m:out.append('\\bibitem{ref'+m[1]+'} '+text_latex(m[2])+'\n\n')
            out.append('\\end{thebibliography}\n');break
        if heading.startswith('Appendix '):
            if not appendix:out.append('\\appendix\n');appendix=True
            heading=re.sub(r'^Appendix [A-Z]\. ','',heading)
        else:heading=re.sub(r'^\d+\. ','',heading)
        out.append('\\section{'+escape(heading)+'}\n');i+=1;continue
    if line.startswith('```'):
        flush();code=[];i+=1
        while i<len(lines) and not lines[i].startswith('```'):
            code.append(lines[i]);i+=1
        out.append('\\begin{lstlisting}\n'+'\n'.join(code)+'\n\\end{lstlisting}\n');i+=1;continue
    if line=='$$':
        flush();math=[];i+=1
        while i<len(lines) and lines[i]!='$$':math.append(lines[i]);i+=1
        out.append('\\[\n'+'\n'.join(math)+'\n\\]\n');i+=1;continue
    if line.startswith('|'):
        flush();table=[]
        while i<len(lines) and lines[i].startswith('|'):
            table.append([x.strip() for x in lines[i].strip('|').split('|')]);i+=1
        out.append(r'''\begin{table}[htbp]
\centering\small
\caption{Equal-budget schema-macro means (percent). Independence uses 21 target-bearing schemas; pool-distinguishable mutant coverage uses 31 eligible schemas. Random means average seeds within schema first.}
\begin{tabular}{rlrr}
\toprule
\shortstack{Distinct\\inputs} & Selector & \shortstack{Independence\\coverage (\%)} & \shortstack{Pool-distinguishable\\mutant coverage (\%)}\\
\midrule
''')
        for row in table[2:]:
            row=[x.replace('Random (within-schema mean)','Random mean') for x in row]
            out.append(' & '.join(text_latex(x) for x in row)+' \\\\\n')
        out.append('\\bottomrule\n\\end{tabular}\n\\end{table}\n')
        out.append(r'''\IfFileExists{figures/results.pdf}{
\begin{figure}[htbp]
\centering\includegraphics[width=\textwidth]{figures/results.pdf}
\caption{Coverage and root mutation outcomes are distinct. Values are descriptive schema-macro means under the frozen-pool protocol; see Table 1 for eligible denominators.}
\end{figure}
}{}
''')
        continue
    if not line.strip():flush()
    else:paragraph.append(line.strip())
    i+=1
flush();out.append('\\end{document}\n')
tex=''.join(out)
# Keep the witness definition readable in a standard single-column page.
tex=tex.replace('W_i=\\{\\{x,y\\}:v_i(x)\\ne v_i(y),\\ D(x)\\ne D(y),\n\\ v_j(x)=v_j(y)\\text{ for all }j\\ne i\\}.',
'''\\begin{aligned}
W_i=\\{\\{x,y\\}:&\\ v_i(x)\\ne v_i(y),\\ D(x)\\ne D(y),\\\\
&v_j(x)=v_j(y)\\text{ for every }j\\ne i\\}.
\\end{aligned}''')
(dest/'main.tex').write_text(tex)


print('Wrote Markdown and standalone LaTeX',len(source.split()),'words')
