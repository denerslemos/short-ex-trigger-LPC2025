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
# Comparison between:
# - OR of (IsoMu24 || Mu50 || CascadeMu100 || HighPtTkMu100)
# - IsoMu24
# - Mu50
# - CascadeMu100
# - HighPtTkMu100
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
canvas=getCanvas()
legend=createLegend()

Denominator = workdir.Get("h_pt_all")

# OR of all SingleMuon triggers
Numerator   = workdir.Get("h_pt_passtrig")
Efficiency = ROOT.TGraphAsymmErrors(Numerator,Denominator,'Pt')
Efficiency = SetStyle(Efficiency, ROOT.kBlack, 20)
Efficiency.GetXaxis().SetTitle("p_{T} [GeV]")
Efficiency.GetYaxis().SetTitle("Efficiency")
Efficiency.GetYaxis().SetRange(0, 2) 
Efficiency.Draw("ap")
legend.AddEntry(Efficiency,"OR", "ep")

# HLT_IsoMu24
hNum_HLT_IsoMu24 = workdir.Get("h_pt_passtrig_HLT_IsoMu24")
hEff_HLT_IsoMu24 = ROOT.TGraphAsymmErrors(hNum_HLT_IsoMu24, Denominator)
hEff_HLT_IsoMu24 = SetStyle(hEff_HLT_IsoMu24, ROOT.kGreen+1, 22)
hEff_HLT_IsoMu24.Draw("pe same")
legend.AddEntry(hEff_HLT_IsoMu24, "HLT_IsoMu24_v")

# HLT_Mu50
hNum_HLT_Mu50 = workdir.Get("h_pt_passtrig_HLT_Mu50")
hEff_HLT_Mu50 = ROOT.TGraphAsymmErrors(hNum_HLT_Mu50, Denominator)
hEff_HLT_Mu50 = SetStyle(hEff_HLT_Mu50, ROOT.kBlue, 34)
hEff_HLT_Mu50.Draw("pe same")
legend.AddEntry(hEff_HLT_Mu50, "HLT_Mu50_v")

# HLT_CascadeMu100
hNum_HLT_CascadeMu100 = workdir.Get("h_pt_passtrig_HLT_CascadeMu100")
hEff_HLT_CascadeMu100 = ROOT.TGraphAsymmErrors(hNum_HLT_CascadeMu100, Denominator)
hEff_HLT_CascadeMu100 = SetStyle(hEff_HLT_CascadeMu100, ROOT.kRed, 29)
hEff_HLT_CascadeMu100.Draw("pe same")
legend.AddEntry(hEff_HLT_CascadeMu100, "HLT_CascadeMu100_v")

# HLT_HighPtTkMu100
hNum_HLT_HighPtTkMu100 = workdir.Get("h_pt_passtrig_HLT_HighPtTkMu100")
hEff_HLT_HighPtTkMu100 = ROOT.TGraphAsymmErrors(hNum_HLT_HighPtTkMu100, Denominator)
hEff_HLT_HighPtTkMu100 = SetStyle(hEff_HLT_HighPtTkMu100, ROOT.kMagenta, 29)
hEff_HLT_HighPtTkMu100.Draw("pe same")
legend.AddEntry(hEff_HLT_HighPtTkMu100, "HLT_HighPtTkMu100_v")

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
Denominator52 = workdir.Get("h_eta52_all")
Denominator102 = workdir.Get("h_eta102_all")

# OR of all SingleMuon triggers
Numerator   = workdir.Get("h_eta26_passtrig")
Efficiency = ROOT.TGraphAsymmErrors(Numerator,Denominator,'Eta')
Efficiency = SetStyle(Efficiency, ROOT.kBlack, 20)
Efficiency.GetXaxis().SetTitle("#eta")
Efficiency.GetYaxis().SetTitle("Efficiency")
Efficiency.GetYaxis().SetRangeUser(0.65, 1.0)
Efficiency.Draw("ap")
legend.AddEntry(Efficiency,"OR (p_{T} > 26 GeV)", "ep")

# HLT_IsoMu24
hNum_HLT_IsoMu24 = workdir.Get("h_eta26_passtrig_HLT_IsoMu24")
hEff_HLT_IsoMu24 = ROOT.TGraphAsymmErrors(hNum_HLT_IsoMu24, Denominator)
hEff_HLT_IsoMu24 = SetStyle(hEff_HLT_IsoMu24, ROOT.kGreen+1, 22)
hEff_HLT_IsoMu24.Draw("pe same")
legend.AddEntry(hEff_HLT_IsoMu24, "HLT_IsoMu24_v (p_{T} > 26 GeV)")

# HLT_Mu50
hNum_HLT_Mu50 = workdir.Get("h_eta52_passtrig_HLT_Mu50")
hEff_HLT_Mu50 = ROOT.TGraphAsymmErrors(hNum_HLT_Mu50, Denominator52)
hEff_HLT_Mu50 = SetStyle(hEff_HLT_Mu50, ROOT.kBlue, 34)
hEff_HLT_Mu50.Draw("pe same")
legend.AddEntry(hEff_HLT_Mu50, "HLT_Mu50_v (p_{T} > 52 GeV)")

# HLT_CascadeMu100
hNum_HLT_CascadeMu100 = workdir.Get("h_eta102_passtrig_HLT_CascadeMu100")
hEff_HLT_CascadeMu100 = ROOT.TGraphAsymmErrors(hNum_HLT_CascadeMu100, Denominator102)
hEff_HLT_CascadeMu100 = SetStyle(hEff_HLT_CascadeMu100, ROOT.kRed, 29)
hEff_HLT_CascadeMu100.Draw("pe same")
legend.AddEntry(hEff_HLT_CascadeMu100, "HLT_CascadeMu100_v (p_{T} > 102 GeV)")

# HLT_HighPtTkMu100
hNum_HLT_HighPtTkMu100 = workdir.Get("h_eta102_passtrig_HLT_HighPtTkMu100")
hEff_HLT_HighPtTkMu100 = ROOT.TGraphAsymmErrors(hNum_HLT_HighPtTkMu100, Denominator102)
hEff_HLT_HighPtTkMu100 = SetStyle(hEff_HLT_HighPtTkMu100, ROOT.kMagenta, 29)
hEff_HLT_HighPtTkMu100.Draw("pe same")
legend.AddEntry(hEff_HLT_HighPtTkMu100, "HLT_HighPtTkMu100_v (p_{T} > 102 GeV)")

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
Denominator52 = workdir.Get("h_phi52_all")
Denominator102 = workdir.Get("h_phi102_all")

# OR of all SingleMuon triggers
Numerator   = workdir.Get("h_phi26_passtrig")
Efficiency = ROOT.TGraphAsymmErrors(Numerator,Denominator,'Phi')
Efficiency = SetStyle(Efficiency, ROOT.kBlack, 20)
Efficiency.GetXaxis().SetTitle("#phi")
Efficiency.GetYaxis().SetTitle("Efficiency")
Efficiency.GetYaxis().SetRangeUser(0.65, 1.0)
Efficiency.Draw("ap")
legend.AddEntry(Efficiency,"OR (p_{T} > 26 GeV)", "ep")

# HLT_IsoMu24
hNum_HLT_IsoMu24 = workdir.Get("h_phi26_passtrig_HLT_IsoMu24")
hEff_HLT_IsoMu24 = ROOT.TGraphAsymmErrors(hNum_HLT_IsoMu24, Denominator)
hEff_HLT_IsoMu24 = SetStyle(hEff_HLT_IsoMu24, ROOT.kGreen+1, 22)
hEff_HLT_IsoMu24.Draw("pe same")
legend.AddEntry(hEff_HLT_IsoMu24, "HLT_IsoMu24_v (p_{T} > 26 GeV)")

# HLT_Mu50
hNum_HLT_Mu50 = workdir.Get("h_phi52_passtrig_HLT_Mu50")
hEff_HLT_Mu50 = ROOT.TGraphAsymmErrors(hNum_HLT_Mu50, Denominator52)
hEff_HLT_Mu50 = SetStyle(hEff_HLT_Mu50, ROOT.kBlue, 34)
hEff_HLT_Mu50.Draw("pe same")
legend.AddEntry(hEff_HLT_Mu50, "HLT_Mu50_v (p_{T} > 52 GeV)")

# HLT_CascadeMu100
hNum_HLT_CascadeMu100 = workdir.Get("h_phi102_passtrig_HLT_CascadeMu100")
hEff_HLT_CascadeMu100 = ROOT.TGraphAsymmErrors(hNum_HLT_CascadeMu100, Denominator102)
hEff_HLT_CascadeMu100 = SetStyle(hEff_HLT_CascadeMu100, ROOT.kRed, 29)
hEff_HLT_CascadeMu100.Draw("pe same")
legend.AddEntry(hEff_HLT_CascadeMu100, "HLT_CascadeMu100_v (p_{T} > 102 GeV)")

# HLT_HighPtTkMu100
hNum_HLT_HighPtTkMu100 = workdir.Get("h_phi102_passtrig_HLT_HighPtTkMu100")
hEff_HLT_HighPtTkMu100 = ROOT.TGraphAsymmErrors(hNum_HLT_HighPtTkMu100, Denominator102)
hEff_HLT_HighPtTkMu100 = SetStyle(hEff_HLT_HighPtTkMu100, ROOT.kMagenta, 29)
hEff_HLT_HighPtTkMu100.Draw("pe same")
legend.AddEntry(hEff_HLT_HighPtTkMu100, "HLT_HighPtTkMu100_v (p_{T} > 102 GeV)")

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
