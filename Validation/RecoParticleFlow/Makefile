TMPDIR=tmp
RELVALCMD=${CMSSW_BASE}/src/Validation/RecoParticleFlow/test/run_relval.sh

all: TTbar QCD ZMM
dqm: TTbar_dqm QCD_dqm ZMM_dqm

TTbar: TTbar_reco TTbar_dqm
QCD: QCD_reco QCD_dqm
ZMM: ZMM_reco ZMM_dqm

TTbar_reco:
	cd ${TMPDIR} && ${RELVALCMD} TTbar reco
TTbar_dqm:
	cd ${TMPDIR} && ${RELVALCMD} TTbar dqm

QCD_reco:
	cd ${TMPDIR} && ${RELVALCMD} QCD reco
QCD_dqm:
	cd ${TMPDIR} && ${RELVALCMD} QCD dqm

ZMM_reco:
	cd ${TMPDIR} && ${RELVALCMD} ZMM reco
ZMM_dqm:
	cd ${TMPDIR} && ${RELVALCMD} ZMM dqm

.PHONY: TTbar_reco QCD_reco ZMM_reco TTbar_dqm QCD_dqm ZMM_dqm
