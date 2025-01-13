#!/usr/bin/env python3
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

#importing tools from nanoAOD processing set up to store the ratio histograms in a root file
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class TrigMETAnalysis(Module):
    def __init__(self):
        self.writeHistFile=True
        self.reference_paths=reference_paths
        self.signal_paths=signal_paths

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)
        self.h_passreftrig  = ROOT.TH1F("h_passreftrig" , "; passed ref trigger", 2, 0. , 2.)
        self.h_met_all      = ROOT.TH1F("h_met_all" , "; E_{T}^{miss} [GeV]", 40, 100., 500.)
        self.h_met_passtrig = ROOT.TH1F("h_met_passtrig" , "; E_{T}^{miss} [GeV]", 40, 100., 500.)
        self.hList = []
        for path in self.signal_paths:
            histo = ROOT.TH1F("h_met_passtrig_HLT_%s" % (path), "; E_{T}^{miss} [GeV]", 40, 100., 500)
            self.hList.append(histo)
        self.addObject(self.h_passreftrig )
        self.addObject(self.h_met_all )
        self.addObject(self.h_met_passtrig )
        for h in self.hList:
            self.addObject(h)

    def analyze(self, event):

        met = Object(event, "MET")
        hlt = Object(event, "HLT")

        # Check if event passes the reference trigger(s)
        refAccept=False
        for path in self.reference_paths:
            bit = getattr(hlt, path)
            if bit:
                refAccept = True

        # Save the bit of reference trigger and skim event
        self.h_passreftrig.Fill(refAccept)
        if not refAccept:
           return False

        # Add any offline selection here:
        electrons = Collection(event, "Electron")
        nEle = 0
        for el in electrons:
            if abs(el.eta) > 2.4: continue
            if el.pt < 40: continue
            if el.cutBased < 4: continue # (cutBased ID: 0:fail, 1:veto, 2:loose, 3:medium, 4:tight)
            nEle += 1

        # Keep only events with exactly one electron with pT > 40 GeV, tight ID
        if not (nEle == 1):
            return False

        self.h_met_all.Fill(met.pt)

        # Check if event passes the signal trigger(s)
        signalOR = False
        for path in self.signal_paths:
            bit = getattr(hlt, path)
            if bit:
                if "140" in path: signalOR = True
                hist = next((h for h in self.hList if path in h.GetName()), None)
                hist.Fill(met.pt)

        if signalOR:
            self.h_met_passtrig.Fill(met.pt)

        return True

reference_paths = ["Ele32_WPTight_Gsf"]
signal_paths    = ["PFMET120_PFMHT120_IDTight", "PFMET130_PFMHT130_IDTight", "PFMET140_PFMHT140_IDTight", "PFMETTypeOne140_PFMHT140_IDTight", "PFMETNoMu140_PFMHTNoMu140_IDTight"]

preselection="MET_pt > 99"
files=[
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/043fa9aa-b27b-4371-8363-287537de8dba.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/06879ec8-1ba8-4c93-8e3e-823b68fd95d7.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/0ace69d3-c3f5-48ad-95f9-8a32d9a2f342.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/0bf20258-be43-4647-94a8-925451431d02.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/0c71c68e-416e-42a7-a6cf-d7d168dad678.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/0dd93ee7-a3ea-41b1-b15f-975be3b2e9a8.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/11400820-be63-4065-a7b0-ac9885a9bf74.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/117ddb44-eb84-4a98-8884-d5b5fb211fcb.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/12df1fe0-8f1f-4c44-a28c-d9692568e464.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/14bb8d8a-2596-4993-9532-9c8999db9d99.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/15c7be47-77f7-4cfb-8ecb-3da4766c8b32.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/15de96db-c531-460d-ae0f-3379137be808.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/16013cef-adb9-4f73-8431-369989b5b5af.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/17aa0120-6361-4df9-925f-0d2048bbd203.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/18c12337-03a0-4e82-a10a-307ece47505a.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/1d835e83-e589-4a1a-b99c-1b929101e2b0.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/1eb9da58-a3a4-47a6-b8d3-57062c445a46.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/1fb4b3a6-2a52-4f9a-9329-d7e7e576d922.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/1fcb849b-c984-48f9-bd73-96317b13b86e.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/20e9f5cb-da1a-4fc9-b7a8-adbd9488c030.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/24f83222-efa3-46fc-96b6-cb55ef8efc08.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/260fb52c-dcdd-4963-aa25-e79c789d123b.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/26b20fc9-14af-4355-9074-ba5cf45f05ec.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/26f71746-15ad-46ab-975a-e930d3b91bf2.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/2870867a-bb78-4e96-8bd9-696cd43f53c6.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/2ac63590-ec9d-4d95-a37e-13f8819e0503.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/2b1c16f8-18a0-4943-9df2-6fa0c279a130.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/2b243d64-b733-47d8-b58e-231cac2aec28.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/2b65abb2-7c41-43c6-b856-dc50a91025b3.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/3102c972-62cf-485b-95cc-aae178b35739.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/3111802e-c60f-46bf-9bed-791926ab3b36.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/356ca41e-e382-4e76-a2e2-de74bb94073d.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/36007139-e41f-4244-b2b4-bb4f6202a24a.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/3694ed05-4804-46a3-a2a8-c7cfa9146ad9.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/37b88c8b-349c-440b-be21-9838f351ceef.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/3942c309-33b1-470d-8512-c093143c779f.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/3d6fe278-70a4-4351-9946-b5ab1ec717fc.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/41a7f691-7325-411b-965f-1352efeda3eb.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/43c6f94f-d006-48fc-802a-11f061242635.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/4499931a-c79f-4154-b68e-a6b98f727e51.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/453c6d46-05cd-45b5-98f4-8b392af01734.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/458276d1-ecc0-4e0e-b8d5-bd016136af57.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/47369ab5-a384-4cca-993b-116542db50f1.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/4751c61e-f28b-43f5-a16b-e7068cd2ab4a.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/4c4b0184-b822-488f-9848-32d091d715b4.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/4c8d13f2-4445-42ae-9f47-4fad0be08995.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/4cb49e2e-22d2-4964-8921-676ebcf88375.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/50dcad60-04f6-4cdc-b702-87b0a32db910.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/55b0a9a4-0138-444b-8790-94ba030f408a.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/55e0e9ba-1068-49d6-9944-6e49200fa59c.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/598f49b3-524f-4d5f-8290-fa810caa1b9f.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/5a303ad4-19c9-49a7-8c1c-507d015081f9.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/5c68357e-51f6-4a4b-b711-6c3720775589.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/5d0a050d-514f-4352-bfaa-50174b5a0aa2.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/5e4b2bee-e7fa-43dd-bbc8-b16520cdb409.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/5fe37357-1e01-47c0-8ae9-1ffd41b5a066.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/6048a7d8-844f-402e-b0c7-f48d68cc234d.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/651f88b1-0d9d-48e2-a4e4-7961ebdb983b.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/65641c65-6ecd-48fb-b76d-8fa61c28ade2.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/6ead3365-5177-40a2-9b01-91cb96e3b680.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/6f0b2e5a-a565-4d3c-9870-576ca86bf7d6.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/71e7b55f-ab99-4470-adc1-6bb640d0e88c.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/7359ce21-9f07-4200-8bcb-ef6170d8e2fb.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/83e5089d-77c3-4d6b-86d9-324a1e7c98f5.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/8402968e-a24a-4c53-94e5-582617881d01.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/8568b686-1ba9-428d-9ae0-da6632b10434.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/8601bbd0-338a-4fcd-9e54-8f192861d80e.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/8626d971-9024-4c7b-accc-13a3e418662a.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/865dd7a0-2989-4c4e-b5b3-56673f0aa7a2.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/891ee609-1554-47fa-bbff-643f1e1b6e01.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/89f48f14-ee2a-469b-8e77-952b6fdf2cc9.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/8c80ada1-e936-401a-9649-20fa3a055796.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/91392bc0-f551-4420-8195-3da2a3b442ad.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/922b2d97-96a1-4e89-8a8c-1cd2ba3be9eb.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/95edc73b-00a8-4e22-acaa-c0ed403db8b3.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/9660430a-7a88-48ac-b340-89352ab2effc.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/96f93693-06a9-4d40-b739-722a903a6c72.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/992b8111-d8f8-40a5-886d-51e1dc2d0161.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/9a07fc8e-5a9b-4022-925f-3e06d30946ad.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/a13b103b-1b23-4fe2-9241-61a8ca4f2b7d.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/a31d2a9f-8beb-48fe-9d19-f7d38e8d69cc.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/a6e4b47a-db60-4c5b-981f-a7465307115e.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/a701a32d-5c9f-459e-8442-fc50a75abc36.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/ac1014b6-8591-4b6a-ab94-c626034ccc2c.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/adc39bc5-8caf-4d7e-b903-76622fd1f37f.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/ae07f437-b213-403f-bbcc-659680b7ce9b.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/b0db5b19-9256-4685-bc7a-a3b13cc2fef2.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/b241d82c-dcb3-47a2-9566-c11acb451c93.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/b31d5f58-0a03-4cd5-b5af-1351248d2683.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/b6108839-3fb1-4c7e-8f52-bbf8a75611d4.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/b63b81f9-190b-4f79-bb3c-3f6bf4fa3b12.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/b8ae90f9-3b7f-48c2-9d98-85836a1bafa8.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/c2ac601b-3eca-466b-b981-9f8a3da25af5.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/c3d63b85-154a-4d12-b0bd-19970393ce3a.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/c6415ce0-c94f-4fa6-8af5-dbec8387b1f9.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/c77b81b7-7ef1-4afc-8d14-27f152bec900.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/c78c7003-177e-4a37-ae54-fba66d578c5d.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/c94d5e59-d771-48e6-8350-8cfff456a001.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/c97771d2-23c8-4626-ac31-6ea1c859cb86.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/cc3dcaf5-1b85-488e-8f2e-db2ecabc6a87.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/cf8c5c24-0361-4fad-9cc8-c9c688d99ea4.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/d2dcbd3e-17da-4edc-9e5c-58f2dadf8df9.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/d358da63-5c9f-4c0c-92d9-9674c4d7d834.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/d674da59-4165-4206-8668-d92f5dc3d873.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/dcf2a63a-7473-4d8e-ac36-47fa55750dad.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/ddaf8c36-dd44-40d8-aa1d-9726d5328f2d.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/dea41310-96be-4016-bb14-b4c0a78b999b.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/e16579d7-9fd0-48d3-9568-6c4ad5cfc2f1.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/e2f89ebd-385d-48bc-b5a1-35086399605b.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/e41f8036-c411-4eae-9807-a659a9690505.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/e51e9fd3-4bf6-4f8a-a0f0-7aeefc2c4643.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/e89b75cb-acd3-481d-a13e-967ec4c04888.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/ebc277e6-4634-4b48-938b-7f953c6511d1.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/ed5c09d6-ffc8-4459-a7d1-b2d0ecc433de.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/ef60cb8c-1c10-4306-bdf0-70d6b90be5b5.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/efb51246-f8e8-405e-aace-7b946deda751.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/f03b46c8-61bb-4009-b485-1b5550eff0d1.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/f0fa7ff8-cd99-4c90-a22b-696f1f17e36a.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/f2eeac34-e2f2-4ade-b3c3-b38998d9a4e6.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/f4d30ec4-c1b0-417e-bc53-48ffeb080dc6.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/f61f4c3a-5744-45a2-beb2-ac0165a74071.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/f65c1244-eaf6-4fc7-98ee-e63896d4748e.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/f8242129-ff7e-4f17-952c-1f9d95e36d3e.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv1/fe8d5bd8-6aeb-4949-923c-7ce21bd0fff8.root",

    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/142f0a5e-1a8c-4048-a3f4-fb38cbc6966a.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/23d7ca77-f796-4443-a572-da5af19267ea.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/274cee2e-483e-41d7-876a-947fc4306cf7.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/2d8f5eaf-c5ae-4986-88df-b21ed954f277.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/2e373349-0378-4edf-848d-9ed193837bc4.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/30e92a86-8ac4-4b90-841c-b1aec2d7e1be.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/4a509520-9363-447f-9bf0-8d2d65cf55c3.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/512f2785-0812-4b53-a06c-08ef2e084c73.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/546abb59-5691-4323-9ed4-832493ddcf7a.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/62c08bc6-1efa-4f69-9206-bb5b15fa9bd8.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/70a32d57-586d-44a6-b4b0-b67a0a1247d0.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/775d1667-0080-45fb-8935-b8bbb1cfd0e8.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/79e538c5-7228-488d-8548-10585a6b6c2c.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/7e13a9ca-1473-496e-bbe8-01753c3d488f.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/81550de8-0b90-47ee-861e-b0ba7ed59ff8.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/81c5ab0a-cd28-46b5-b94c-df868d312ba7.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/826d4725-3b4a-43e9-b9d0-2edee81fbfd4.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/8665463e-a736-4573-83c1-b0499f6de73b.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/88f67549-4d5f-45a7-8aba-06f5b43fa5d7.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/8ff68f08-aa50-40e2-b0d6-28dd4da0526d.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/93273861-b59b-4348-9b6f-b19f50a52041.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/97acac8d-af9c-4481-80a7-5da0982d747b.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/9b38e671-508e-43b8-8486-9b341bfc2cac.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/a96e25c4-e783-4f7c-bf7c-49a1c63ec65c.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/b145921f-ace0-4ead-b498-bbc218587915.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/b5940a35-04a3-4c3f-8c8e-f83a21d5b8f0.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/dcd16ef5-976d-4d5e-b2ea-d08c112c10f3.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/e9af5f4f-e747-4765-9836-afc80d445e4b.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/eb1969f2-8f57-4258-b00b-da1739319d21.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/ebb5dd04-80cc-4f61-a224-a944962ce242.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/f3ee4f0f-9bfe-4b64-a154-3e4d0e6acda1.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/f459db8c-91c2-4715-87d8-913973285625.root",
    "/eos/user/c/cmsdas/2024/short-ex-triggers/NanoAOD_EGamma_2023/2023Dv2/f6334a70-5a9c-48e8-b3f9-ad9e7f1e0b7f.root",
]

p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[TrigMETAnalysis()],noOut=True,histFileName="histos_METTrigNanoAOD.root",histDirName="metTrigAnalyzerNanoAOD")
p.run()
