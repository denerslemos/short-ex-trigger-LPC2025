import FWCore.ParameterSet.Config as cms

process = cms.Process('HLTANALYZER')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
                                #'file:/eos/user/c/cmsdas/2024/short-ex-triggers/skimmedMINIAOD_EGamma_2023/test/skim.root'
                                'file:/eos/user/c/cmsdas/2024/short-ex-triggers/skimmedMINIAOD_EGamma_2023/skim_1.root',
                                'file:/eos/user/c/cmsdas/2024/short-ex-triggers/skimmedMINIAOD_EGamma_2023/skim_2.root',
                                'file:/eos/user/c/cmsdas/2024/short-ex-triggers/skimmedMINIAOD_EGamma_2023/skim_3.root',
                                'file:/eos/user/c/cmsdas/2024/short-ex-triggers/skimmedMINIAOD_EGamma_2023/skim_4.root',
                            ),
)

process.options = cms.untracked.PSet()

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.20 $'),
    annotation = cms.untracked.string('RelVal nevts:100'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.TFileService = cms.Service("TFileService",
                                       fileName = cms.string('histos_METTrigAnalyzer.root')
                                   )

### analyzer configuration
process.metTrigAnalyzerMiniAOD = cms.EDAnalyzer("METTrigAnalyzerMiniAOD")
process.metTrigAnalyzerMiniAOD.refTriggerName = cms.untracked.string("HLT_Ele32_WPTight_Gsf_v19")
process.metTrigAnalyzerMiniAOD.sigTriggerNames= cms.untracked.vstring("HLT_PFMET120_PFMHT120_IDTight_v24", "HLT_PFMET130_PFMHT130_IDTight_v24", "HLT_PFMET140_PFMHT140_IDTight_v24",
                                                                      "HLT_PFMETTypeOne140_PFMHT140_IDTight_v15", "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v24", "HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v23",
                                                                      "HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v23")
process.metTrigAnalyzerMiniAOD.verbose = cms.untracked.bool(False)

process.GlobalTag.globaltag = "140X_dataRun3_Prompt_v2"

# Path and EndPath definitions
process.HLTanalyzers = cms.Path(process.metTrigAnalyzerMiniAOD)
