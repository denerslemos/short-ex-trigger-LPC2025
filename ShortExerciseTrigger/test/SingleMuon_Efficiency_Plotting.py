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

def createLegend():
    legend = ROOT.TLegend(0.44, 0.193, 0.82, 0.44)
    legend.SetFillColor(0)
    legend.SetFillStyle(0);
    legend.SetBorderSize(0);
    return legend

def SetStyle(h, color, marker_style):
    h.SetLineColor(color)
    h.SetMarkerColor(color)
    h.SetMarkerStyle(marker_style)
    return h

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTextFont(42)

file = ROOT.TFile("histos_SingleMuTrigNanoAOD.root")
workdir =file.GetDirectory("singlemuTrigAnalyzerNanoAOD")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# - IsoMu24
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
canvas=getCanvas()
legend=createLegend()

Denominator = workdir.Get("h_pt_all")

# OR of all SingleMuon triggers
Numerator   = workdir.Get("h_pt_passtrig_HLT_IsoMu24")
Efficiency = ROOT.TGraphAsymmErrors(Numerator,Denominator,'Pt')
Efficiency = SetStyle(Efficiency, ROOT.kBlack, 20)
Efficiency.GetXaxis().SetTitle("p_{T} [GeV]")
Efficiency.GetYaxis().SetTitle("Efficiency")
Efficiency.GetYaxis().SetRange(0, 2) 
Efficiency.Draw("ap")
legend.AddEntry(Efficiency,"HLT_IsoMu24_v", "ep")

# Additional text
tex_cms = AddCMSText()
tex_cms.Draw("same")

private = AddPrivateWorkText()
private.Draw("same")

header = ROOT.TLatex()
header.SetTextSize(0.04)
header.DrawLatexNDC(0.57, 0.905, "2023D, #sqrt{s} = 13.6 TeV")

legend.Draw("same")
canvas.Update()
canvas.Modified()
canvas.SaveAs("SingleMuonEfficiency_NanoAOD_pt.pdf")

### eff vs. eta

canvas=getCanvas()
legend=createLegend()

Denominator = workdir.Get("h_eta26_all")

# HLT_IsoMu24
Numerator   = workdir.Get("h_eta26_passtrig_HLT_IsoMu24")
Efficiency = ROOT.TGraphAsymmErrors(Numerator,Denominator,'Eta')
Efficiency = SetStyle(Efficiency, ROOT.kBlack, 20)
Efficiency.GetXaxis().SetTitle("#eta")
Efficiency.GetYaxis().SetTitle("Efficiency")
Efficiency.GetYaxis().SetRangeUser(0.65, 1.0)
Efficiency.Draw("ap")
legend.AddEntry(Efficiency,"HLT_IsoMu24_v (p_{T} > 26 GeV)", "ep")

# Additional text
tex_cms = AddCMSText()
tex_cms.Draw("same")

private = AddPrivateWorkText()
private.Draw("same")

header = ROOT.TLatex()
header.SetTextSize(0.04)
header.DrawLatexNDC(0.57, 0.905, "2023D, #sqrt{s} = 13.6 TeV")

legend.Draw("same")
canvas.Update()
canvas.Modified()
canvas.SaveAs("SingleMuonEfficiency_NanoAOD_eta.pdf")

### eff vs. phi

canvas=getCanvas()
legend=createLegend()

Denominator = workdir.Get("h_phi26_all")

# HLT_IsoMu24
Numerator   = workdir.Get("h_phi26_passtrig_HLT_IsoMu24")
Efficiency = ROOT.TGraphAsymmErrors(Numerator,Denominator,'Phi')
Efficiency = SetStyle(Efficiency, ROOT.kBlack, 20)
Efficiency.GetXaxis().SetTitle("#phi")
Efficiency.GetYaxis().SetTitle("Efficiency")
Efficiency.GetYaxis().SetRangeUser(0.65, 1.0)
Efficiency.Draw("ap")
legend.AddEntry(Efficiency,"HLT_IsoMu24_v (p_{T} > 26 GeV)", "ep")

# Additional text
tex_cms = AddCMSText()
tex_cms.Draw("same")

private = AddPrivateWorkText()
private.Draw("same")

header = ROOT.TLatex()
header.SetTextSize(0.04)
header.DrawLatexNDC(0.57, 0.905, "2023D, #sqrt{s} = 13.6 TeV")

legend.Draw("same")
canvas.Update()
canvas.Modified()
canvas.SaveAs("SingleMuonEfficiency_NanoAOD_phi.pdf")
