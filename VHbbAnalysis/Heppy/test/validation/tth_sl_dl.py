import sys, os
sys.path.append(os.environ.get("CMSSW_BASE") + "/src/VHbbAnalysis/Heppy/test")
import ROOT

ROOT.TH1.AddDirectory(False)
ROOT.TH1.SetDefaultSumw2(True)

prefix = "Loop_validation_tth_sl_dl_"
steps = [
    "step1",
    "step1-variables",
#    "step2",
]

nevents = 100

lumi = 10000.0
xs = {
    "tth_hbb": 0.29340449999999996,
    "ttjets": 831.76,
}

class Histo:
    def __init__(self, name, func, cut, bins):
        self.name = name
        self.func = func
        self.cut = cut
        self.h = ROOT.TH1D(name, name, *bins)

    def fill(self, tree, outdir):
        outdir.cd()
        outdir.Add(self.h)
        tree.Draw("{0} >> {1}".format(self.func, self.name), self.cut)

if __name__ == '__main__':

    if "step1" in steps:
        from vhbb_combined import *
        components = [
            cfg.MCComponent(
                files = [
                    "root://xrootd-cms.infn.it///store/mc/RunIISpring16MiniAODv2/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext3-v1/00000/000B9244-4B27-E611-91D2-7845C4FC3C6B.root"
                ],
                name = "ttjets",
                isEmbed=False,
                puFileMC="puMC.root",
                puFileData="puData.root", 
                puFileDataPlus="puDataPlus.root", 
                puFileDataMinus="puDataMinus.root", 
                isMC = True
            ),
            cfg.MCComponent(
                files = [
                    "root://xrootd-cms.infn.it///store/mc/RunIISpring16MiniAODv2/ttHTobb_M125_13TeV_powheg_pythia8/MINIAODSIM/PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/50000/0CFE0FCC-6E2C-E611-9789-02163E0116AC.root",
                ],
                name = "tth_hbb",
                isEmbed=False,
                puFileMC="puMC.root",
                puFileData="puData.root", 
                puFileDataPlus="puDataPlus.root", 
                puFileDataMinus="puDataMinus.root", 
                isMC = True
            )
        ]

        from PhysicsTools.HeppyCore.framework.looper import Looper
        for comp in components:
            print "processing",comp
            config.components = [comp]
            looper = Looper( prefix + comp.name, config, nPrint = 0, nEvents = nevents)
            looper.loop()
            looper.write()

    if "step1-variables" in steps:
        outfile = ROOT.TFile("tth_validation_step1.root", "RECREATE")
        for comp in ["tth_hbb", "ttjets"]:
            outdir = outfile.mkdir(comp)
            inf = ROOT.TFile(prefix+comp+"/tree.root")
            if not inf:
                raise Exception("Could not open input file, maybe vhbb_combined.py step failed")
            tree = inf.Get("tree")
            if not tree or tree.GetEntries() == 0:
                raise Exception("Could not find tree or tree is empty, preselection problem")
            hcount = inf.Get("Count")
            if not hcount:
                raise Exception("Count histogram not found")
            ngen = float(hcount.GetBinContent(1))

            xsweight = lumi * xs[comp] / ngen
            print "File {0} has {1} entries, xsw={2:.2f}".format(inf.GetName(), tree.GetEntries(), xsweight)

            histograms = [
                Histo("genWeight", "genWeight", "1", (20, -2.0, 2.0)),
                
                Histo("jet_pt", "Jet_pt", "1", (20, 0, 500)),
                Histo("jet_pt_uncorr", "Jet_pt/Jet_corr", "1", (20, 0, 500)),
                Histo("jet_pt_JESUp", "Jet_pt*Jet_corr_JECUp/Jet_corr", "1", (20, 0, 500)),
                Histo("jet_pt_JESDown", "Jet_pt*Jet_corr_JECDown/Jet_corr", "1", (20, 0, 500)),

                Histo("jet_pt_bw", "Jet_pt", "bTagWeight", (20, 0, 500)),
                Histo("jet_pt_bw_JESDown", "Jet_pt", "bTagWeight_JESDown", (20, 0, 500)),
                Histo("jet_pt_bw_JESUp", "Jet_pt", "bTagWeight_JESUp", (20, 0, 500)),

                Histo("jet_btagCSV_b", "Jet_btagCSV", "abs(Jet_hadronFlavour)==5", (20, 0, 1)),
                Histo("jet_btagCSV_c", "Jet_btagCSV", "abs(Jet_hadronFlavour)==4", (20, 0, 1)),
                Histo("jet_btagCSV_l", "Jet_btagCSV", "abs(Jet_hadronFlavour)!=4 && abs(Jet_hadronFlavour)!=5", (20, 0, 1)),
                Histo("jet_btagCMVA_b", "Jet_btagCMVA", "abs(Jet_hadronFlavour)==5", (20, -1, 1)),
                Histo("jet_btagCMVA_c", "Jet_btagCMVA", "abs(Jet_hadronFlavour)==4", (20, -1, 1)),
                Histo("jet_btagCMVA_l", "Jet_btagCMVA", "abs(Jet_hadronFlavour)!=4 && abs(Jet_hadronFlavour)!=5", (20, -1, 1)),
                    
                Histo("GenTop_decayMode", "GenTop_decayMode", "", (5, 0, 5)),
                
            ]
            if comp == "ttjets":
                histograms += [
                    Histo("ttCls", "ttCls", "", (60, 0, 60)),
                ]
            elif comp == "tth_hbb":
                histograms += [
                    Histo("genHiggsDecayMode", "genHiggsDecayMode", "", (5, 0, 5)),
                ]
            for histo in histograms:
                histo.fill(tree, outdir)
                histo.h.Scale(xs_weight)
            inf.Close()
        outfile.Write()
        outfile.Close()
