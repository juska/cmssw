#!/bin/bash
#https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCmsDriver
#https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookDataFormats

N=1000

#by default, use the RelVal sample
INPUT_FILE=root://cms-xrd-global.cern.ch///store/relval/CMSSW_9_4_11_cand2/RelValTTbar_13/GEN-SIM-DIGI-RAW/94X_mc2017_realistic_v15-v1/10000/FA0F368D-D4D2-E811-A159-0025905B8600.root
CONDITIONS=auto:phase1_2017_realistic
ERA=Run2_2017,run2_nanoAOD_94XMiniAODv1
NTHREADS=4

##In case you want to generate your own events
#cmsDriver.py TTbarLepton_13TeV_TuneCUETP8M1_cfi  --conditions $CONDITIONS -n $N --era $ERA --eventcontent FEVTDEBUG --relval 9000,100 -s GEN,SIM --datatier GEN-SIM --beamspot Realistic50ns13TeVCollision --fileout file:step1.root  > step1.log  2>&1
#INPUT_FILE=step1.root

##This step does the detector simulation to end up with the input required for RECO
##Particle flow is not run in this step and it can be skipped if you start from GEN-SIM-DIGI-RAW
#
##DIGI: simulate detector response to MC particles
##L1: simulate L1 trigger
##DIGI2RAW: Convert detector response to RAW (DAQ output) used in online data taking
##HLT: run HLT
##On lxplus, this step takes about 30 minutes / 1000 events
#cmsDriver.py step2  --conditions $CONDITIONS  -s DIGI:pdigi_valid,L1,DIGI2RAW,HLT:@relval2017 --datatier GEN-SIM-DIGI-RAW-HLTDEBUG --nThreads $NTHREADS -n $N --era $ERA --eventcontent FEVTDEBUGHLT --filein file:$INPUT_FILE --fileout file:step2.root  > step2.log  2>&1
#INPUT_FILE=step2.root

#Run the actual CMS reco with particle flow.
#On lxplus, this step takes about 15 minutes / 1000 events
cmsDriver.py step3  --runUnscheduled  --conditions $CONDITIONS -s RAW2DIGI,L1Reco,RECO,RECOSIM,EI,PAT --datatier RECOSIM,AODSIM,MINIAODSIM --nThreads $NTHREADS -n $N --era $ERA --eventcontent RECOSIM,AODSIM,MINIAODSIM --filein file:$INPUT_FILE --fileout file:step3.root > step3.log  2>&1

#NanoAOD
#Can be skipped if doing DQM directly from RECO
#On lxplus, this step takes about 1 minute / 1000 events
#cmsDriver.py step4 --conditions $CONDITIONS -s NANO --datatier NANOAODSIM --nThreads $NTHREADS -n $N --era $ERA --eventcontent NANOAODSIM --filein file:step3_inMINIAODSIM.root --fileout file:step4.root > step4.log 2>&1

cmsDriver.py step5 --conditions $CONDITIONS -s DQM:@pfDQM --datatier DQMIO --nThreads $NTHREADS -n $N --era $ERA --eventcontent DQM --filein file:step3.root --fileout file:step5.root > step5.log 2>&1

#Harvesting seems not to be needed
#cmsDriver.py step6 --conditions $CONDITIONS -s HARVESTING --era $ERA --filetype DQM --filein file:step5.root --fileout file:step6.root > step6.log 2>&1
