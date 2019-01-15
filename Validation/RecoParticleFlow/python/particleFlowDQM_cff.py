import FWCore.ParameterSet.Config as cms

pfDQM = cms.EDAnalyzer("ParticleFlowDQM",
    recoJetCollection = cms.InputTag('ak4PFJets'),
    genJetCollection = cms.InputTag('ak4GenJets'),
    jetDeltaR = cms.double(0.5),
    genJetPtBins  = cms.vdouble(30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 150.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1200.0, 1400.0, 1600.0, 1800.0, 2000.0),
    genJetEtaBins  = cms.vdouble(-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0),

    responseNbins = cms.int32(50),
    responseLow = cms.double(0),
    responseHigh = cms.double(2),

)
