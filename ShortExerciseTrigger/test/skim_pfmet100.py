import FWCore.ParameterSet.Config as cms

process = cms.Process('SKIM')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.maxEvents = cms.untracked.PSet(
#    input = cms.untracked.int32(1000)
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(
        '/store/data/Run2023D/EGamma0/MINIAOD/22Sep2023_v1-v1/2530000/0161357b-bf17-4c3f-91dc-9b84c84de511.root',
        '/store/data/Run2023D/EGamma0/MINIAOD/22Sep2023_v1-v1/2530000/01705f10-4d36-47bf-a8f9-c09ecf8fb5c2.root',
        '/store/data/Run2023D/EGamma0/MINIAOD/22Sep2023_v1-v1/2530000/019135bd-c27d-49cc-9588-0d8e3bd293c6.root',
        '/store/data/Run2023D/EGamma0/MINIAOD/22Sep2023_v1-v1/2530000/021fef9a-9f99-440d-9d07-0b9695bdfdba.root',
        '/store/data/Run2023D/EGamma0/MINIAOD/22Sep2023_v1-v1/2530000/033cad21-9f14-46dc-a26f-69df39e71a92.root',
#        '/store/data/Run2023D/EGamma0/MINIAOD/22Sep2023_v1-v1/2530000/0380a48e-b684-407c-afe0-5e55b775a596.root',
#        '/store/data/Run2023D/EGamma0/MINIAOD/22Sep2023_v1-v1/2530000/03ab9a78-fad3-4a81-bc03-b80ba6b3df3f.root',
#        '/store/data/Run2023D/EGamma0/MINIAOD/22Sep2023_v1-v1/2530000/04acc00e-cb97-4d50-90fc-911babd90334.root',
#        '/store/data/Run2023D/EGamma0/MINIAOD/22Sep2023_v1-v1/2530000/04b17eaa-bc3b-4260-9068-06e2feaf1f09.root',
#        '/store/data/Run2023D/EGamma0/MINIAOD/22Sep2023_v1-v1/2530000/04b375e2-b78a-4392-a319-694f4daad0e3.root',
   ),
)


process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.20 $'),
    annotation = cms.untracked.string('RelVal nevts:100'),
    name = cms.untracked.string('Applications')
)

# JSON

import FWCore.PythonUtilities.LumiList as LumiList
process.source.lumisToProcess = LumiList.LumiList(filename = 'Cert_Collisions2023_366442_370790_Golden_JSON.txt').getVLuminosityBlockRange()

# skim definitions

process.highpfmet = cms.EDFilter("PtMinCandViewSelector",
                           src = cms.InputTag("slimmedMETs"),
                           ptMin = cms.double(100)
)

process.metFilter = cms.EDFilter("CandViewCountFilter",
  src = cms.InputTag("highpfmet"),
  minNumber = cms.uint32(1),
)

process.pfmet_filter_step = cms.Path(process.highpfmet + process.metFilter)


# Output definition

process.Out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string ("skim_met.root"),
                               outputCommands = cms.untracked.vstring('keep *'),
                               SelectEvents = cms.untracked.PSet(
                                   SelectEvents = cms.vstring('pfmet_filter_step')
                               ),
)
  
process.GlobalTag.globaltag = "140X_dataRun3_Prompt_v2"

# Path and EndPath definitions
process.output_step = cms.EndPath(process.Out)

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10000
