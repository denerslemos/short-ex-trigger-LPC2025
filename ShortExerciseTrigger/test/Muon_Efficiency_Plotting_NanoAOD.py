'''
Usage:
 python3 SingleMuon_Efficiency_NanoAOD.py (to produce the histograms)
 python3 Muon_Efficiency_Plotting_NanoAOD.py (to plot the efficiencies)
'''
import ROOT
import math 
import time

def getCanvas():
    d = ROOT.TCanvas("", "", 800, 700)
    d.SetLeftMargin(0.12)
    d.SetRightMargin(0.15)
    d.SetLeftMargin(0.13)
    return d

def AddPrivateWorkText(setx=0.21, sety=0.905):
    tex = ROOT.TLatex(0.,0., 'Private Work');
    tex.SetNDC();
    tex.SetX(setx);
    tex.SetY(sety);
    tex.SetTextFont(53);
    tex.SetTextSize(28);
    tex.SetLineWidth(2)
    return tex

def AddCMSText(setx=0.205, sety=0.905):
    texcms = ROOT.TLatex(0.,0., 'CMS');
    texcms.SetNDC();
    texcms.SetTextAlign(31);
    texcms.SetX(setx);
    texcms.SetY(sety);
    texcms.SetTextFont(63);
    texcms.SetLineWidth(2);
    texcms.SetTextSize(30);
    return texcms

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTextFont(42)

def GetLabel(var):
    if "pt" in var:
        return "p_{T} [GeV]"
    elif "eta" in var:
        return "#eta"
    elif "phi" in var:
        return "#phi [rad]"
    print("Uknown variable %s. Please add a x-label" % (var))
    return "x-label [units]"

def CreatePlot(var):

    # Create the canvas
    canvas=getCanvas()
    xLabel = GetLabel(var)
    
    legend = ROOT.TLegend(0.35, 0.20, 0.55, 0.30)
    legend.SetFillColor(0)
    legend.SetFillStyle(0);
    legend.SetBorderSize(0);
    
    # Efficiency vs pt
    hDen = workdir.Get("h_%s_probe_all" % (var))

    hNum = workdir.Get("h_%s_probe_pass" % (var))
    hEff = ROOT.TGraphAsymmErrors(hNum, hDen)
    hEff.SetLineColor(ROOT.kRed)
    hEff.SetMarkerColor(ROOT.kRed)
    hEff.SetMarkerStyle(20)
    hEff.GetXaxis().SetTitle(xLabel)
    hEff.GetYaxis().SetTitle("Efficiency")
    hEff.GetYaxis().SetRangeUser(0.0, 1.05)
    hEff.Draw()
    legend.AddEntry(hEff,"HLT_IsoMu24", "ep")
    
    # Additional text
    tex_cms = AddCMSText()
    tex_cms.Draw("same")
    
    private = AddPrivateWorkText()
    private.Draw("same")
    
    header = ROOT.TLatex()
    header.SetTextSize(0.04)
    header.DrawLatexNDC(0.57, 0.905, "2022, #sqrt{s} = 13.6 TeV")
    
    legend.Draw("same")
    canvas.Update()
    canvas.Modified()
    canvas.SaveAs("IsoMu24_Efficiency_vs_%s_NanoAOD.pdf" % (var))
    return

file = ROOT.TFile("histos_SingleMuTrigAnalyzer_NanoAOD.root")
workdir = file.GetDirectory("singleMuTrigAnalyzerNanoAOD")
variables = ["pt", "eta", "phi"]
for var in variables:
    CreatePlot(var)



