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

file = ROOT.TFile("histos_METTrigNanoAOD.root")
workdir =file.GetDirectory("metTrigAnalyzerNanoAOD")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Comparison between:
# - OR of (HLT_PFMET140_PFMHT140_IDTight || HLT_PFMETNoMu140_PFMHTNoMu140_IDTight || HLT_PFMETTypeOne140_PFMHT140_IDTight_v)
# - HLT_PFMET140_PFMHT140_IDTight
# - HLT_PFMETNoMu140_PFMHTNoMu140_IDTight
# - HLT_PFMETTypeOne140_PFMHT140_IDTight_v
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
canvas=getCanvas()
legend=createLegend()

Denominator = workdir.Get("h_met_all")

# OR of all MET triggers
Numerator   = workdir.Get("h_met_passtrig")
Efficiency = ROOT.TGraphAsymmErrors(Numerator,Denominator,'MET')
Efficiency = SetStyle(Efficiency, ROOT.kBlack, 20)
Efficiency.GetXaxis().SetTitle("E_{T}^{miss} [GeV]")
Efficiency.GetYaxis().SetTitle("Efficiency")
Efficiency.GetYaxis().SetRange(0, 2) 
Efficiency.Draw("ap")
legend.AddEntry(Efficiency,"OR", "ep")

# HLT_PFMET140_PFMHT140_IDTight
hNum_HLT_PFMET140_PFMHT140_IDTight = workdir.Get("h_met_passtrig_HLT_PFMET140_PFMHT140_IDTight")
hEff_HLT_PFMET140_PFMHT140_IDTight = ROOT.TGraphAsymmErrors(hNum_HLT_PFMET140_PFMHT140_IDTight, Denominator)
hEff_HLT_PFMET140_PFMHT140_IDTight = SetStyle(hEff_HLT_PFMET140_PFMHT140_IDTight, ROOT.kGreen+1, 22)
hEff_HLT_PFMET140_PFMHT140_IDTight.Draw("pe same")
legend.AddEntry(hEff_HLT_PFMET140_PFMHT140_IDTight, "HLT_PFMET140_PFMHT140_IDTight_v")

# HLT_PFMETNoMu140_PFMHTNoMu140_IDTight
hNum_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight = workdir.Get("h_met_passtrig_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight")
hEff_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight = ROOT.TGraphAsymmErrors(hNum_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight, Denominator)
hEff_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight = SetStyle(hEff_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight, ROOT.kBlue, 34)
hEff_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight.Draw("pe same")
legend.AddEntry(hEff_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight, "HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v")

# HLT_PFMETTypeOne140_PFMHT140_IDTight_v
hNum_HLT_PFMETTypeOne140_PFMHT140_IDTight = workdir.Get("h_met_passtrig_HLT_PFMETTypeOne140_PFMHT140_IDTight")
hEff_HLT_PFMETTypeOne140_PFMHT140_IDTight = ROOT.TGraphAsymmErrors(hNum_HLT_PFMETTypeOne140_PFMHT140_IDTight, Denominator)
hEff_HLT_PFMETTypeOne140_PFMHT140_IDTight = SetStyle(hEff_HLT_PFMETTypeOne140_PFMHT140_IDTight, ROOT.kRed, 29)
hEff_HLT_PFMETTypeOne140_PFMHT140_IDTight.Draw("pe same")
legend.AddEntry(hEff_HLT_PFMETTypeOne140_PFMHT140_IDTight, "HLT_PFMETTypeOne140_PFMHT140_IDTight_v")

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
canvas.SaveAs("MET_Efficiency_HLT_PFMET140s_NanoAOD.pdf")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Comparison between triggers with different thresholds:
# - HLT_PFMET120_PFMHT120_IDTight
# - HLT_PFMET130_PFMHT130_IDTight
# - HLT_PFMET140_PFMHT140_IDTight
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
canvas=getCanvas()
legend=createLegend()

Denominator = workdir.Get("h_met_all")

# HLT_PFMET120_PFMHT120_IDTight
hNum_HLT_PFMET120_PFMHT120_IDTight = workdir.Get("h_met_passtrig_HLT_PFMET120_PFMHT120_IDTight")
hEff_HLT_PFMET120_PFMHT120_IDTight = ROOT.TGraphAsymmErrors(hNum_HLT_PFMET120_PFMHT120_IDTight, Denominator)
hEff_HLT_PFMET120_PFMHT120_IDTight = SetStyle(hEff_HLT_PFMET120_PFMHT120_IDTight, ROOT.kGreen+1, 22)
hEff_HLT_PFMET120_PFMHT120_IDTight.Draw("pe same")
hEff_HLT_PFMET120_PFMHT120_IDTight.Draw("ap")
legend.AddEntry(hEff_HLT_PFMET120_PFMHT120_IDTight, "HLT_PFMET120_PFMHT120_IDTight_v")

# HLT_PFMET130_PFMHT130_IDTight
hNum_HLT_PFMET130_PFMHT130_IDTight = workdir.Get("h_met_passtrig_HLT_PFMET130_PFMHT130_IDTight")
hEff_HLT_PFMET130_PFMHT130_IDTight = ROOT.TGraphAsymmErrors(hNum_HLT_PFMET130_PFMHT130_IDTight, Denominator)
hEff_HLT_PFMET130_PFMHT130_IDTight = SetStyle(hEff_HLT_PFMET130_PFMHT130_IDTight, ROOT.kRed, 23)
hEff_HLT_PFMET130_PFMHT130_IDTight.Draw("pe same")
legend.AddEntry(hEff_HLT_PFMET130_PFMHT130_IDTight, "HLT_PFMET130_PFMHT130_IDTight_v")

# HLT_PFMET140_PFMHT140_IDTight
hNum_HLT_PFMET140_PFMHT140_IDTight = workdir.Get("h_met_passtrig_HLT_PFMET140_PFMHT140_IDTight")
hEff_HLT_PFMET140_PFMHT140_IDTight = ROOT.TGraphAsymmErrors(hNum_HLT_PFMET140_PFMHT140_IDTight, Denominator)
hEff_HLT_PFMET140_PFMHT140_IDTight = SetStyle(hEff_HLT_PFMET140_PFMHT140_IDTight, ROOT.kBlue, 21)
hEff_HLT_PFMET140_PFMHT140_IDTight.Draw("pe same")
legend.AddEntry(hEff_HLT_PFMET140_PFMHT140_IDTight, "HLT_PFMET140_PFMHT140_IDTight")

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
canvas.SaveAs("MET_Efficiency_HLT_PFMETX_PFMHTX_IDTight_NanoAOD.pdf")
