
# Quickstart

1. Set up using `source test/setup_cmssw.sh`.
2. Make a temporary directory in e.g. `$CMSSW_BASE/src/Validation/RecoParticleFlow/tmp`
2. Run the RECO sequence using `$CMSSW_BASE/src/Validation/RecoParticleFlow/test/run_relval.sh QCD reco $NJOB` where $NJOB is an integer in [0,249] that is used to select the events for this job, assuming 200 events per job and a RelVal dataset of 50k events
2. Run the DQM sequence using `test/run_relval.sh QCD dqm 0` 
3. Produce the plots using `test/compare.py`

# Running on condor
The reco sequence takes about 10-15 minutes / 100 events, so one would need 125 CPU-hours to run the full 50k events. We have prepared condor scripts to facilitate this on lxbatch.
Go to a temporary working directory e.g. `$CMSSW_BASE/src/Validation/RecoParticleFlow/tmp`, create a log directory with `mkdir log` and submit the condor jobs using
`condor_submit ${CMSSW_BASE}/src/Validation/RecoParticleFlow/test/condor_sub.jdl`. Once the jobs are done, the DQM sequence is able to use all step3 EDM files in a single job.
