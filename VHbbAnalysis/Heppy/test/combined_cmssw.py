""" combined_cmssw.py
cmsRun config file to be used with the CmsswPreprocessor for Heppy-Ntupelizing.
Schedules:
 - b-tagging
 - boosted variables
"""

########################################
# Imports/Setup
########################################

import sys

import FWCore.ParameterSet.Config as cms

process = cms.Process("EX")
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring("file:///scratch/gregor/TTJets_MSDecaysCKM_central_Tune4C_13TeV_MiniAOD.root")
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.OUT = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('test.root'),
    outputCommands = cms.untracked.vstring(['drop *'])
)
process.endpath= cms.EndPath(process.OUT)

# Let CMSSW take care of scheduling 
process.options = cms.untracked.PSet(     
    wantSummary = cms.untracked.bool(True),
    allowUnscheduled = cms.untracked.bool(True)
)

########################################
# Boosted Substructure
########################################

# Import some jet clustering defaults
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.PFJetParameters_cfi import *

# Select candidates that would pass CHS requirements
process.chs = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedPFCandidates"), cut = cms.string("fromPV"))

# HEPTopTagger (MultiR)
process.looseOptRHTT = cms.EDProducer(
    "HTTTopJetProducer",
    PFJetParameters,
    AnomalousCellParameters,
    optimalR       = cms.bool(True),
    algorithm      = cms.int32(1),
    jetAlgorithm   = cms.string("CambridgeAachen"),
    rParam         = cms.double(1.5),
    mode           = cms.int32(4),
    minFatjetPt    = cms.double(200.),
    minCandPt      = cms.double(200.),
    minSubjetPt    = cms.double(30.),
    writeCompound  = cms.bool(True),
    minCandMass    = cms.double(0.),
    maxCandMass    = cms.double(1000),
    massRatioWidth = cms.double(100.),
    minM23Cut      = cms.double(0.),
    minM13Cut      = cms.double(0.),
    maxM13Cut      = cms.double(2.))
process.looseOptRHTT.src = cms.InputTag("chs")
process.looseOptRHTT.jetPtMin = cms.double(200.)

# AntiKt, R=0.8, pT > 200 GeV
process.ak08PFJetsCHS = cms.EDProducer(
        "FastjetJetProducer",
        PFJetParameters,
        AnomalousCellParameters,
        jetAlgorithm = cms.string("AntiKt"),
        rParam       = cms.double(0.8))
process.ak08PFJetsCHS.src = cms.InputTag("chs")
process.ak08PFJetsCHS.jetPtMin = cms.double(200.)

# CA, R=1.5, pT > 200 GeV
process.ca15PFJetsCHS = cms.EDProducer(
        "FastjetJetProducer",
        PFJetParameters,
        AnomalousCellParameters,
        jetAlgorithm = cms.string("CambridgeAachen"),
        rParam       = cms.double(1.5))
process.ca15PFJetsCHS.src = cms.InputTag("chs")
process.ca15PFJetsCHS.jetPtMin = cms.double(200.)


# Calculate tau1, tau2 and tau3 for ungroomed CA R=1.5 jets
process.ca15PFJetsCHSNSubjettiness  = cms.EDProducer("NjettinessAdder",
                                                     src=cms.InputTag("ca15PFJetsCHS"),
                                                     cone=cms.double(1.5),
                                                     Njets = cms.vuint32(1,2,3),
                                                     # variables for measure definition : 
                                                     measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
                                                     beta = cms.double(1.0),              # CMS default is 1
                                                     R0 = cms.double(1.5),                # CMS default is jet cone size
                                                     Rcutoff = cms.double( -999.0),       # not used by default
                                                     # variables for axes definition :
                                                     axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
                                                     nPass = cms.int32(-999),             # not used by default
                                                     akAxesR0 = cms.double(-999.0)        # not used by default
)

# Calculate tau1, tau2 and tau3 for ungroomed AK R=0.8 jets
process.ak08PFJetsCHSNSubjettiness  = cms.EDProducer("NjettinessAdder",
                                                     src=cms.InputTag("ak08PFJetsCHS"),
                                                     cone=cms.double(0.8),
                                                     Njets = cms.vuint32(1,2,3),
                                                     # variables for measure definition : 
                                                     measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
                                                     beta = cms.double(1.0),              # CMS default is 1
                                                     R0 = cms.double(0.8),                # CMS default is jet cone size
                                                     Rcutoff = cms.double( -999.0),       # not used by default
                                                     # variables for axes definition :
                                                     axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
                                                     nPass = cms.int32(-999),             # not used by default
                                                     akAxesR0 = cms.double(-999.0)        # not used by default
)

# Apply pruning to AK R=0.8 jets
process.ak08PFPrunedJetsCHS = process.ak08PFJetsCHS.clone(
    usePruning = cms.bool(True),
    nFilt = cms.int32(2),
    zcut = cms.double(0.1),
    rcut_factor = cms.double(0.5),
    useExplicitGhosts = cms.bool(True),
    writeCompound = cms.bool(True), # Also write subjets for pruned fj
    jetCollInstanceName=cms.string("SubJets",)
)

# Apply softdrop to AK R=0.8 jets
process.ak08PFSoftdropJetsCHS = process.ak08PFJetsCHS.clone(
    useSoftDrop = cms.bool(True),
    zcut = cms.double(0.1),
    beta = cms.double(0.0),
    R0 = cms.double(0.8),
    useExplicitGhosts = cms.bool(True))

# Apply pruning to CA R=1.5 jets
process.ca15PFPrunedJetsCHS = process.ca15PFJetsCHS.clone(
    usePruning = cms.bool(True),
    nFilt = cms.int32(2),
    zcut = cms.double(0.1),
    rcut_factor = cms.double(0.5),
    useExplicitGhosts = cms.bool(True),
    writeCompound = cms.bool(True), # Also write subjets for pruned fj
    jetCollInstanceName=cms.string("SubJets"),
)

# Apply softdrop to CA R=1.5 jets
process.ca15PFSoftdropJetsCHS = process.ca15PFJetsCHS.clone(
    useSoftDrop = cms.bool(True),
    zcut = cms.double(0.1),
    beta = cms.double(0.0),
    R0 = cms.double(1.5),
    useExplicitGhosts = cms.bool(True))

# Apply trimming to CA R=1.5 jets
process.ca15PFTrimmedJetsCHS = process.ca15PFJetsCHS.clone(
    useTrimming = cms.bool(True),
    rFilt = cms.double(0.2),
    trimPtFracMin = cms.double(0.06),
    useExplicitGhosts = cms.bool(True))

process.OUT.outputCommands.append("keep *_ak08PFJetsCHS_*_EX")
process.OUT.outputCommands.append("keep *_ca15PFJetsCHS_*_EX")
process.OUT.outputCommands.append("keep *_ak08PFPrunedJetsCHS_*_EX")
process.OUT.outputCommands.append("keep *_ca15PFPrunedJetsCHS_*_EX")
process.OUT.outputCommands.append("keep *_ak08PFSoftdropJetsCHS_*_EX")
process.OUT.outputCommands.append("keep *_ca15PFSoftdropJetsCHS_*_EX")
process.OUT.outputCommands.append("keep *_ca15PFTrimmedJetsCHS_*_EX")
process.OUT.outputCommands.append("keep *_ak08PFJetsCHSNSubjettiness_*_EX")
process.OUT.outputCommands.append("keep *_ca15PFJetsCHSNSubjettiness_*_EX")
process.OUT.outputCommands.append("keep *_looseOptRHTT_*_EX")


########################################
# Hbb Tagging
########################################

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load("RecoBTag.Configuration.RecoBTag_cff") # this loads all available b-taggers
from RecoBTag.SoftLepton.softPFMuonTagInfos_cfi import *
from RecoBTag.SoftLepton.softPFElectronTagInfos_cfi import *

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')


for fatjet_name in ["ak08PFJetsCHS", "ca15PFJetsCHS"]:
    
    if fatjet_name == "ak08PFJetsCHS":        
        delta_r = 0.8
        maxSVDeltaRToJet = 0.7
        weightFile = cms.FileInPath('RecoBTag/SecondaryVertex/data/BoostedDoubleSV_AK8_BDT.weights.xml.gz')
    elif fatjet_name == "ca15PFJetsCHS":        
        delta_r = 1.5
        maxSVDeltaRToJet = 1.3
        weightFile = cms.FileInPath('RecoBTag/SecondaryVertex/data/BoostedDoubleSV_CA15_BDT.weights.xml.gz')
    else:
        print "Invalid fatjet for b-tagging: ", fatjet_name
        sys.exit()

    # Define the module names
    impact_info_name          = fatjet_name + "ImpactParameterTagInfos"
    isv_info_name             = fatjet_name + "pfInclusiveSecondaryVertexFinderTagInfos"        
    sm_info_name              = fatjet_name + "softPFMuonsTagInfos"
    se_info_name              = fatjet_name + "softPFElectronsTagInfos"
    bb_comp_name              = fatjet_name + "candidateBoostedDoubleSecondaryVertexComputer"
    tag_name                  = fatjet_name + "pfBoostedDoubleSecondaryVertexBJetTags"

    # Setup the modules
    # IMPACT PARAMETER
    setattr(process, 
            impact_info_name, 
            process.pfImpactParameterTagInfos.clone(
                primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices"),
                candidates = cms.InputTag("packedPFCandidates"),
                computeProbabilities = cms.bool(False),
                computeGhostTrack = cms.bool(False),
                maxDeltaR = cms.double(delta_r),
                jets = cms.InputTag(fatjet_name),
            ))
    getattr(process, impact_info_name).explicitJTA = cms.bool(True)

    # ISV
    setattr(process,
            isv_info_name,                
            process.pfInclusiveSecondaryVertexFinderTagInfos.clone(
               extSVCollection               = cms.InputTag('slimmedSecondaryVertices'),
               trackIPTagInfos               = cms.InputTag(impact_info_name),                
            ))
    getattr(process, isv_info_name).useSVClustering = cms.bool(True)
    getattr(process, isv_info_name).rParam = cms.double(delta_r)
    getattr(process, isv_info_name).extSVDeltaRToJet = cms.double(delta_r)
    getattr(process, isv_info_name).trackSelection.jetDeltaRMax = cms.double(delta_r)
    getattr(process, isv_info_name).vertexCuts.maxDeltaRToJetAxis = cms.double(delta_r)
    getattr(process, isv_info_name).jetAlgorithm = cms.string("AntiKt")
    getattr(process, isv_info_name).fatJets  =  cms.InputTag(fatjet_name)
    getattr(process, isv_info_name).groomedFatJets  =  cms.InputTag(fatjet_name)

    # SOFT MUON
    setattr(process,
            sm_info_name,
            softPFMuonsTagInfos.clone(
                jets = cms.InputTag(fatjet_name),
                muons = cms.InputTag("slimmedMuons"),
                primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices")                
            ))
    
    # SOFT ELECTRON
    setattr(process,
            se_info_name,
            softPFElectronsTagInfos.clone(
                jets = cms.InputTag(fatjet_name),
                electrons = cms.InputTag("slimmedElectrons"),
                primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices"),                
                DeltaRElectronJet=cms.double(delta_r),
            ))

    # DOUBLE B COMPUTER
    setattr(process,
            bb_comp_name,
            cms.ESProducer("CandidateBoostedDoubleSecondaryVertexESProducer",
                           beta = cms.double(1.0),
                           R0 = cms.double(delta_r),
                           maxSVDeltaRToJet = cms.double(maxSVDeltaRToJet),
                           weightFile = weightFile))

    # TAGS
    setattr(process,
            tag_name, 
            cms.EDProducer("JetTagProducer",
                           jetTagComputer = cms.string(bb_comp_name),
                           tagInfos = cms.VInputTag(cms.InputTag(impact_info_name),
                                                    cms.InputTag(isv_info_name),
                                                    cms.InputTag(sm_info_name),
                                                    cms.InputTag(se_info_name))))
    

    # Produce the output
    process.OUT.outputCommands.append("keep *_{0}_*_EX".format(tag_name))
    

########################################
# Generator level hadronic tau decays
########################################

process.load("PhysicsTools.JetMCAlgos.TauGenJets_cfi")
process.tauGenJets.GenParticles = cms.InputTag('prunedGenParticles')
process.load("PhysicsTools.JetMCAlgos.TauGenJetsDecayModeSelectorAllHadrons_cfi")

process.OUT.outputCommands.append("keep *_tauGenJetsSelectorAllHadrons_*_EX")
