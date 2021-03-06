import FWCore.ParameterSet.Config as cms


# HLT Online -----------------------------------
# AlCa
#from DQM.HLTEvF.HLTAlCaMonPi0_cfi import *
#from DQM.HLTEvF.HLTAlCaMonEcalPhiSym_cfi import *
# JetMET
#from DQM.HLTEvF.HLTMonJetMETDQMSource_cfi import *
# Electron
#from DQM.HLTEvF.HLTMonEleBits_cfi import *
# Muon
#from DQM.HLTEvF.HLTMonMuonDQM_cfi import *
#from DQM.HLTEvF.HLTMonMuonBits_cfi import *
# Photon
#from DQM.HLTEvF.HLTMonPhotonBits_cfi import *
# Tau
#from DQM.HLTEvF.HLTMonTau_cfi import *
#from DQM.HLTEvF.hltMonBTagIPSource_cfi import *
#from DQM.HLTEvF.hltMonBTagMuSource_cfi import *
# hltMonjmDQM  bombs
# hltMonMuDQM dumps names of all histograms in the directory
# hltMonPhotonBits in future releases
# *hltMonJetMET makes a log file, need to learn how to turn it off
# *hltMonEleBits causes SegmentFaults in HARVESTING(step3) in inlcuded in step2

#import DQMServices.Components.DQMEnvironment_cfi
#dqmEnvHLTOnline = DQMServices.Components.DQMEnvironment_cfi.dqmEnv.clone()
#dqmEnvHLTOnline.subSystemFolder = 'HLT'

#onlineHLTSource = cms.Sequence(EcalPi0Mon*EcalPhiSymMon*hltMonEleBits*hltMonMuBits*hltMonTauReco*hltMonBTagIPSource*hltMonBTagMuSource*dqmEnvHLTOnline)
#onlineHLTSource = cms.Sequence(EcalPi0Mon*EcalPhiSymMon*hltMonMuBits*dqmEnvHLTOnline)

# HLT Offline -----------------------------------

# Egamma
from DQMOffline.Trigger.HLTGeneralOffline_cfi import *

from DQMOffline.Trigger.EgHLTOfflineSource_cfi import *
# Muon
from DQMOffline.Trigger.MuonOffline_Trigger_cff import *
# Top
#from DQMOffline.Trigger.QuadJetAna_cfi import *
# Tau
from DQMOffline.Trigger.HLTTauDQMOffline_cff import *
# JetMET
#from DQMOffline.Trigger.JetMETHLTOfflineSource_cfi import *
from DQMOffline.Trigger.JetMETHLTOfflineAnalyzer_cff import *


from DQMOffline.Trigger.FSQHLTOfflineSource_cfi import *
from DQMOffline.Trigger.HILowLumiHLTOfflineSource_cfi import *

# TnP
#from DQMOffline.Trigger.TnPEfficiency_cff import *
# Inclusive VBF
from DQMOffline.Trigger.HLTInclusiveVBFSource_cfi import *

# tracking
from DQMOffline.Trigger.TrackingMonitoring_cff import *

# strip
from DQMOffline.Trigger.SiStrip_OfflineMonitoring_cff import *

# photon jet
from DQMOffline.Trigger.HigPhotonJetHLTOfflineSource_cfi import * 

import DQMServices.Components.DQMEnvironment_cfi
dqmEnvHLT= DQMServices.Components.DQMEnvironment_cfi.dqmEnv.clone()
dqmEnvHLT.subSystemFolder = 'HLT'


# remove quadJetAna
from DQMOffline.Trigger.topHLTOfflineDQM_cff import *
offlineHLTSource = cms.Sequence(
    hltResults *
    egHLTOffDQMSource *
    muonFullOfflineDQM *
    HLTTauDQMOffline *
    #jetMETHLTOfflineSource *
    jetMETHLTOfflineAnalyzer *
    fsqHLTOfflineSourceSequence *
    HILowLumiHLTOfflineSourceSequence *
    #TnPEfficiency *
    hltInclusiveVBFSource *
    trackingMonitorHLT *
    sistripMonitorHLTsequence *
    higPhotonJetHLTOfflineSource*
    dqmEnvHLT *
    topHLTriggerOfflineDQM)

#triggerOfflineDQMSource =  cms.Sequence(onlineHLTSource*offlineHLTSource)
triggerOfflineDQMSource =  cms.Sequence(offlineHLTSource)
 
