#!/usr/bin/env python3
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
import math

#importing tools from nanoAOD processing set up to store the ratio histograms in a root file
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

def deltaR(eta1, phi1, eta2, phi2):
    return math.sqrt((eta2-eta1)**2 + (phi2-phi1)**2)

# is_nth_bit_set
def is_nth_bit_set(self, x, n):
    if x & (1 << n): ## & and << -> bitwise operators
        return True
    return False

class TrigMuonAnalysis(Module):
    def __init__(self):
        self.writeHistFile=True
        self.signal_path=signal_path

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)
        self.h_passtrig      = ROOT.TH1F("h_passtrig", "; passed trigger", 2, 0. , 2.)
        self.h_mll_allpairs  = ROOT.TH1F("h_mll_allpairs", "; m_{#mu#mu} [GeV]", 75 , 0. , 150.)
        self.h_mll_cut       = ROOT.TH1F("h_mll_cut", "; m_{#mu#mu} [GeV]", 75 , 0. , 150.)
        self.h_pt_probe_all  = ROOT.TH1F("h_pt_probe_all", "; p_{T} [GeV]", 100 , 0. , 100.)
        self.h_pt_probe_pass = ROOT.TH1F("h_pt_probe_pass", "; p_{T} [GeV]", 100 , 0. , 100.)
        self.h_pt_probe_fail = ROOT.TH1F("h_pt_probe_fail", "; p_{T} [GeV]", 100 , 0. , 100.)
        self.h_eta_probe_all = ROOT.TH1F("h_eta_probe_all", "; #eta", 100 , -3. , 3.)
        self.h_eta_probe_pass= ROOT.TH1F("h_eta_probe_pass", "; #eta", 100 , -3. , 3.)
        self.h_eta_probe_fail= ROOT.TH1F("h_eta_probe_fail", "; #eta", 100 , -3. , 3.)
        self.h_phi_probe_all = ROOT.TH1F("h_phi_probe_all", "; #phi", 100 , -3.14 , 3.14)
        self.h_phi_probe_pass= ROOT.TH1F("h_phi_probe_pass", "; #phi", 100 , -3.14 , 3.14)
        self.h_phi_probe_fail= ROOT.TH1F("h_phi_probe_fail", "; #phi", 100 , -3.14 , 3.14)
        self.addObject(self.h_passtrig)
        self.addObject(self.h_mll_allpairs)
        self.addObject(self.h_mll_cut)
        self.addObject(self.h_pt_probe_all)
        self.addObject(self.h_pt_probe_pass)
        self.addObject(self.h_pt_probe_fail)
        self.addObject(self.h_eta_probe_all)
        self.addObject(self.h_eta_probe_pass)
        self.addObject(self.h_eta_probe_fail)
        self.addObject(self.h_phi_probe_all)
        self.addObject(self.h_phi_probe_pass)
        self.addObject(self.h_phi_probe_fail)

    def analyze(self, event):

        hlt = Object(event, "HLT")

        # Check if event passes the IsoMu24 path
        bit=getattr(hlt, "IsoMu24")

        # Save the bit of reference trigger and skim event
        self.h_passtrig.Fill(bit)
        if not bit:
           return False

        def CheckTriggerMatching(offline_mu):

            for trgObj in Collection(event, 'TrigObj'):
                trgObj_pt = trgObj.pt
                trgObj_eta = trgObj.eta
                trgObj_phi = trgObj.phi
                trgObj_ID  = trgObj.id
                trgObj_filterBits = trgObj.filterBits

                # keep only the trigger objects associated with a muon (13)
                if (trgObj_ID != 13): continue

                # Check if trigger filters of HLT_IsoMu24 (index=3) are fired
                if (is_nth_bit_set(self, trgObj.filterBits, 3)):
                    deltaR_mu_trgObj = deltaR(trgObj_eta, trgObj_phi, offline_mu.eta, offline_mu.phi)
                    if (deltaR_mu_trgObj < 0.1):
                        return True
            return False

        # Add any offline selection here:
        muons = Collection(event, "Muon")

        muons_index   = -1
        tag_mu_index  = -1
        prob_mu_index = -1

        for tag_mu in muons:
            muons_index += 1

            # Tag muon requirements: pT > 26 GeV, |eta|<2.4, Tight ID + PFIsolation
            if tag_mu.pt < 26: continue
            if abs(tag_mu.eta) > 2.4: continue
            if not tag_mu.tightId: continue
            if not tag_mu.pfIsoId > 3: continue # PFIso ID from miniAOD selector (1=PFIsoVeryLoose, 2=PFIsoLoose, 3=PFIsoMedium, 4=PFIsoTight, 5=PFIsoVeryTight, 6=PFIsoVeryVeryTight)
            tag_mu_index = muons_index
            tag_mu_isTrgMatched = CheckTriggerMatching(tag_mu)

            # Keep event only if tag muon is matched
            if not tag_mu_isTrgMatched:
                continue

            prob_mu_index = -1
            # Look for a probe muon
            for prob_mu in muons:

                prob_mu_index += 1
                if (prob_mu_index == tag_mu_index):
                    continue

                # Require the same selections for the probe muon
                if prob_mu.pt < 15: continue
                if abs(prob_mu.eta) > 2.4: continue
                if not prob_mu.tightId: continue
                if not prob_mu.pfIsoId > 3: continue

                mll = (prob_mu.p4() + tag_mu.p4()).M()
                self.h_mll_allpairs.Fill(mll)

                if (mll < 81 or mll > 101): continue
                self.h_mll_cut.Fill(mll)

                self.h_pt_probe_all.Fill(prob_mu.pt)
                if prob_mu.pt > 26:
                    self.h_eta_probe_all.Fill(prob_mu.eta)
                    self.h_phi_probe_all.Fill(prob_mu.phi)

                # Now check if the probe muons is trigger matched
                probe_mu_isTrgMatched = CheckTriggerMatching(prob_mu)
                if (probe_mu_isTrgMatched):
                    self.h_pt_probe_pass.Fill(prob_mu.pt)
                    if prob_mu.pt > 26:
                        self.h_eta_probe_pass.Fill(prob_mu.eta)
                        self.h_phi_probe_pass.Fill(prob_mu.phi)
                else:
                    self.h_pt_probe_fail.Fill(prob_mu.pt)
                    if prob_mu.pt > 26:
                        self.h_eta_probe_fail.Fill(prob_mu.eta)
                        self.h_phi_probe_fail.Fill(prob_mu.phi)

        return True

preselection=""
files=[
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/1210167a-e6ea-423a-bff6-512819d2f544.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/14461664-aebb-4a4a-bd86-3ad03bc3d8a4.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/146f29c9-26ff-4f1d-853f-06acb5c3b2c1.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/19386d41-110d-4756-b04f-577d4c0d6a79.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/3fd2edec-3ec5-40a9-9106-0d3f9b118bfc.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/5004d03d-76d7-47e3-9afc-62c3a66e8c84.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/840632af-4ee3-410d-bb96-2d486c2474df.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/b01c272b-1afe-4151-87f9-1a56463a0f4b.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/ba3d8bf5-e5c8-4b99-af24-ccbe0254ac4c.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/bc15e86e-4678-4e60-be6c-ad723aff6b04.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/be0e61a1-7dda-4100-9325-31b703c8ac59.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/c3cff39d-6ad1-41ac-bfbd-aafca2b92c93.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/c717c139-7158-4818-9878-3e8c566295e1.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/db91cf74-77ef-4cbc-9bd3-2cf0f4225f7b.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/e56926e3-a813-4023-a608-cc0b189e0f75.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/e7dad2fc-7362-496a-9b52-15f1f4423975.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_Muon_2023/2023Dv2/f29eb305-f8ed-4217-ba91-a666ed14db1a.root",
]

signal_path = ["IsoMu24"]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[TrigMuonAnalysis()],noOut=True,histFileName="histos_SingleMuTrigNanoAOD_TnP.root",histDirName="singleMuTrigAnalyzerNanoAOD")
p.run()
