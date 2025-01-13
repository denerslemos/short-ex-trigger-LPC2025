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
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(
        '/store/data/Run2023D/Muon0/MINIAOD/22Sep2023_v1-v1/2530000/0702e512-9557-4be0-a329-1a6c1ab4fbee.root',
        '/store/data/Run2023D/Muon0/MINIAOD/22Sep2023_v1-v1/2530000/0702e512-9557-4be0-a329-1a6c1ab4fbee.root',
        '/store/data/Run2023D/Muon0/MINIAOD/22Sep2023_v1-v1/2530000/0d9fa98c-b5ac-4bc0-8ab2-43ecd4546bb5.root',
        '/store/data/Run2023D/Muon0/MINIAOD/22Sep2023_v1-v1/2530000/0fa372a0-9054-467a-ad6e-9da4e5782cf7.root',
        '/store/data/Run2023D/Muon0/MINIAOD/22Sep2023_v1-v1/2530000/0fa55ced-a7cc-4a8a-a0e5-0381c3ac8e37.root',
#        '/store/data/Run2023D/Muon0/MINIAOD/22Sep2023_v1-v1/2530000/16fcc5e6-5626-4c7a-8566-0af091c1904a.root',
#        '/store/data/Run2023D/Muon0/MINIAOD/22Sep2023_v1-v1/2530000/194da3b5-dd63-4dfb-88af-fab8087cf75a.root',
#        '/store/data/Run2023D/Muon0/MINIAOD/22Sep2023_v1-v1/2530000/20fed695-eb7a-4855-b24b-d49c38aab185.root',
#        '/store/data/Run2023D/Muon0/MINIAOD/22Sep2023_v1-v1/2530000/21e2158f-336f-4832-a010-6caf2ea9f4b3.root',
#        '/store/data/Run2023D/Muon0/MINIAOD/22Sep2023_v1-v1/2530000/21fbdf12-a42e-4b82-a77a-c3909c6bc732.root',
#        '/store/data/Run2023D/Muon0/MINIAOD/22Sep2023_v1-v1/2530000/27a80b82-6bc2-4b42-a5ed-310783bebd46.root',
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

process.highptMuons = cms.EDFilter("PtMinCandViewSelector",
                           src = cms.InputTag("slimmedMuons"),
                           ptMin = cms.double(20)
)

process.dimuonFilter = cms.EDFilter("CandViewCountFilter",
  src = cms.InputTag("highptMuons"),
  minNumber = cms.uint32(2),
)

process.dimu_filter_step = cms.Path(process.highptMuons + process.dimuonFilter)


# Output definition

process.Out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string ("skim_5.root"),
                               outputCommands = cms.untracked.vstring('keep *'),
                               SelectEvents = cms.untracked.PSet(
                                   SelectEvents = cms.vstring('dimu_filter_step')
                               ),
)
  
process.GlobalTag.globaltag = "140X_dataRun3_Prompt_v2"

# Path and EndPath definitions
process.output_step = cms.EndPath(process.Out)

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10000
