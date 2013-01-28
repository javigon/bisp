# ex:set ts=2:

from color import *
from debug import *
from fileops import *
import sys

class SimPlot:
  def __init__ (self, prefix, terminal, sizing=None, lmarg=12):
    self.prefix = prefix
    self.terminal = terminal
    self.plotlist = []
    self.sizing = sizing
    self.lmarg = lmarg
    if not terminal in ["pdf", "png"]:
      print textred("Err: Unknown terminal '"+self.terminal+"'")
      dumpstack()
      sys.exit(3)
  
  def append (self, hkey, vkey, logs, hindices, vindices, style, titles, yaxisscale="lin"):
    lines = []
    lines.append("# plot "+str(len(self.plotlist)+1)+"\n")
    lines.append("set lmarg "+str(self.lmarg)+"\n")
    lines.append("set datafile separator \""+logs[0].sep+"\"\n")
    lines.append("set xlabel \""+hkey+"\"\n")
    lines.append("set ylabel \""+vkey+"\"\n")
    if yaxisscale=="lin": lines.append("set yrange [0:]\n")
    else:
      lines.append("set yrange [ * : * ] noreverse nowriteback\n")
      lines.append("set autoscale yfixmin\n")
      lines.append("set autoscale yfixmax\n")
    if yaxisscale=="log": lines.append("set logscale y\n")
    for i in range(len(logs)):
      l = ""
      if i==0: l += "plot"
      else:    l += "    "
      l += " '"+logs[i].filename+"'"
      l += " using "+str(logs[i].index(hindices[i])+2)+":"+str(logs[i].index(vindices[i])+2)
      l += " with "+style
      l += " title \""+titles[i]+"\""
      if i!=len(logs)-1: l += ", \\"
      l += "\n"
      lines.append(l)
    lines.append("\n")
    self.plotlist.append(lines)
  
  def generate (self, timeformat="stamps"):
    gnuplotfilename = self.prefix+".gnuplot"
    plotfilename    = self.prefix+"."+self.terminal
    lines = []
    
    # header
    lines.append("# header\n")
    lines.append("set terminal "+self.terminal+("" if self.sizing==None else " "+self.sizing)+(" font \",4\"" if self.terminal=="pdf" else "")+"\n")
    lines.append("set output \""+plotfilename+"\"\n")
    lines.append("set multiplot layout "+str(len(self.plotlist))+", 1\n")
    if timeformat=="stamps": lines.append("set xdata time\n")
#    lines.append("set xtics 60*60*24*364.25\n")
    if timeformat=="stamps": lines.append("set format x \"%Y\"\n")
    if timeformat=="stamps": lines.append("set timefmt \"%Y-%m-%d %H:%M:%S\"\n")
    lines.append("\n")
    
    # body
    for chunk in self.plotlist:
      lines.extend(chunk)
    
    writefile(gnuplotfilename, lines)
    system("gnuplot "+gnuplotfilename)
  
  

