#include "TFile.h"
#include "TH1.h"
#include "TH2F.h"
#include "TLegend.h"
#include "TString.h"
#include "TCanvas.h"
#include "TEfficiency.h"
#include "TStyle.h"

void plot_trigeff_met (const TString& infile = "histos_METTrigAnalyzer.root") {

  gStyle->SetPadTopMargin(0.08);
  gStyle->SetPadBottomMargin(0.12);
  gStyle->SetPadLeftMargin(0.15);
  gStyle->SetPadRightMargin(0.05);
  gStyle->SetOptStat(0);

  TH1::SetDefaultSumw2();
  
  TFile* f_in = new TFile(infile);

  // ---- Get all histograms
  
  TH1F* h_met_denom = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_all");
  TH1F* h_met_num_HLT_PFMET120_PFMHT120_IDTight_v = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_passtrig_HLT_PFMET120_PFMHT120_IDTight_v24");
  TH1F* h_met_num_HLT_PFMET130_PFMHT130_IDTight_v = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_passtrig_HLT_PFMET130_PFMHT130_IDTight_v24");
  TH1F* h_met_num_HLT_PFMET140_PFMHT140_IDTight_v = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_passtrig_HLT_PFMET140_PFMHT140_IDTight_v24");
  TH1F* h_met_num_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_passtrig_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v24");
  TH1F* h_met_num_HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_passtrig_HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v23");
  TH1F* h_met_num_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_passtrig_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v23");
  TH1F* h_met_num_HLT_PFMETTypeOne140_PFMHT140_IDTight_v = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_passtrig_HLT_PFMETTypeOne140_PFMHT140_IDTight_v15");
  TH1F* h_met_num = (TH1F*) f_in->Get("metTrigAnalyzerMiniAOD/h_met_passtrig");
  
  // ---- Create TEfficiency histograms
  TEfficiency* h_met_eff = new TEfficiency(*h_met_num, *h_met_denom);
  TEfficiency* h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v = new TEfficiency(*h_met_num_HLT_PFMET120_PFMHT120_IDTight_v, *h_met_denom);
  TEfficiency* h_met_eff_HLT_PFMET130_PFMHT130_IDTight_v = new TEfficiency(*h_met_num_HLT_PFMET130_PFMHT130_IDTight_v, *h_met_denom);
  TEfficiency* h_met_eff_HLT_PFMET140_PFMHT140_IDTight_v = new TEfficiency(*h_met_num_HLT_PFMET140_PFMHT140_IDTight_v, *h_met_denom);
  TEfficiency* h_met_eff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v = new TEfficiency(*h_met_num_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v, *h_met_denom);
  TEfficiency* h_met_eff_HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v = new TEfficiency(*h_met_num_HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v, *h_met_denom);
  TEfficiency* h_met_eff_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v = new TEfficiency(*h_met_num_HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v, *h_met_denom);
  TEfficiency* h_met_eff_HLT_PFMETTypeOne140_PFMHT140_IDTight_v = new TEfficiency(*h_met_num_HLT_PFMETTypeOne140_PFMHT140_IDTight_v, *h_met_denom);
  
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  // Comparison between:
  // - OR of (HLT_PFMET120_PFMHT120_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight || HLT_PFMETTypeOne140_PFMHT140_IDTight_v)
  // - HLT_PFMET120_PFMHT120_IDTight
  // - HLT_PFMETNoMu120_PFMHTNoMu120_IDTight
  // - HLT_PFMETTypeOne140_PFMHT140_IDTight_v
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  TCanvas* c_met = new TCanvas("c_met", "c_met", 800, 700);
  c_met->SetLeftMargin(0.12);
  c_met->SetRightMargin(0.15);
  c_met->SetLeftMargin(0.13);
  c_met->cd();
  
  auto legend = new TLegend(0.5,0.20,0.90,0.50);
  legend->SetFillColor(0);
  legend->SetFillStyle(0);
  legend->SetBorderSize(0);
  
  TH2F* h_met_axis = new TH2F("h_met_axis",";E_{T}^{miss} [GeV];Efficiency",40,100,500,20,0,1);
  h_met_axis->GetYaxis()->SetTitleOffset(0.98);
  h_met_axis->SetMaximum(1.05);
  h_met_axis->Draw();
  
  // Logical OR of all signal paths
  h_met_eff->SetLineColor(kBlack);
  h_met_eff->SetMarkerColor(kBlack);
  h_met_eff->SetMarkerStyle(20);
  h_met_eff->Draw("pe same");
  legend->AddEntry(h_met_eff, "OR");
  
  h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v->SetLineColor(kGreen+1);
  h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v->SetMarkerColor(kGreen+1);
  h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v->SetMarkerStyle(22);
  h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v->Draw("pe same");
  legend->AddEntry(h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v, "HLT_PFMET120_PFMHT120_IDTight_v");
    
  h_met_eff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v->SetLineColor(kBlue);
  h_met_eff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v->SetMarkerColor(kBlue);
  h_met_eff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v->SetMarkerStyle(34);
  h_met_eff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v->Draw("pe same");
  legend->AddEntry(h_met_eff_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v, "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v");
  
  h_met_eff_HLT_PFMETTypeOne140_PFMHT140_IDTight_v->SetLineColor(kRed);
  h_met_eff_HLT_PFMETTypeOne140_PFMHT140_IDTight_v->SetMarkerStyle(29);
  h_met_eff_HLT_PFMETTypeOne140_PFMHT140_IDTight_v->SetMarkerColor(kRed);
  h_met_eff_HLT_PFMETTypeOne140_PFMHT140_IDTight_v->Draw("pe same");
  legend->AddEntry(h_met_eff_HLT_PFMETTypeOne140_PFMHT140_IDTight_v, "HLT_PFMETTypeOne140_PFMHT140_IDTight_v");
  
  legend->Draw("same");
  
  c_met->Modified();
  c_met->Update();
  c_met->SaveAs("METEfficiency_MiniAOD.pdf");
  
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  // Comparison between:
  // - HLT_PFMET120_PFMHT120_IDTight
  // - HLT_PFMET130_PFMHT130_IDTight
  // - HLT_PFMET140_PFMHT140_IDTight
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  TCanvas* c2 = new TCanvas("c2", "c2", 800, 700);
  c2->SetLeftMargin(0.12);
  c2->SetRightMargin(0.15);
  c2->SetLeftMargin(0.13);
  c2->cd();
  
  auto legend2 = new TLegend(0.5,0.20,0.90,0.50);
  legend2->SetFillColor(0);
  legend2->SetFillStyle(0);
  legend2->SetBorderSize(0);
  
  h_met_axis->Draw();
  
  h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v->SetLineColor(kGreen+1);
  h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v->SetMarkerColor(kGreen+1);
  h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v->SetMarkerStyle(22);
  h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v->Draw("pe same");
  legend2->AddEntry(h_met_eff_HLT_PFMET120_PFMHT120_IDTight_v, "HLT_PFMET120_PFMHT120_IDTight_v");
  
  h_met_eff_HLT_PFMET130_PFMHT130_IDTight_v->SetLineColor(kRed);
  h_met_eff_HLT_PFMET130_PFMHT130_IDTight_v->SetMarkerColor(kRed);
  h_met_eff_HLT_PFMET130_PFMHT130_IDTight_v->SetMarkerStyle(21);
  h_met_eff_HLT_PFMET130_PFMHT130_IDTight_v->Draw("pe same");
  legend2->AddEntry(h_met_eff_HLT_PFMET130_PFMHT130_IDTight_v, "HLT_PFMET130_PFMHT130_IDTight_v");
  
  h_met_eff_HLT_PFMET140_PFMHT140_IDTight_v->SetLineColor(kBlue);
  h_met_eff_HLT_PFMET140_PFMHT140_IDTight_v->SetMarkerColor(kBlue);
  h_met_eff_HLT_PFMET140_PFMHT140_IDTight_v->SetMarkerStyle(22);
  h_met_eff_HLT_PFMET140_PFMHT140_IDTight_v->Draw("pe same");
  legend2->AddEntry(h_met_eff_HLT_PFMET140_PFMHT140_IDTight_v, "HLT_PFMET140_PFMHT140_IDTight_v");
  
  legend2->Draw("same");
  c2->Modified();
  c2->Update();
  c2->SaveAs("METEfficiency_HLT_PFMETX_PFMHTX_IDTight_MiniAOD.pdf");
  
  return;
}
