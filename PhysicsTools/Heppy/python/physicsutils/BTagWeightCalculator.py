import ROOT
import numpy as np

class BTagWeightCalculator:
    def __init__(self, fn_hf, fn_lf, btag_name="pfCombinedInclusiveSecondaryVertexV2BJetTags") :
        self.pdfs = {}
       
        #Set to True for debugging printout
        self.debug = False

        #heavy-flavour bins
        self.pt_bins_hf = np.array([20, 30, 40, 60, 100, 160, 10000])
        self.eta_bins_hf = np.array([0, 2.41])
        
        #light-flavour bins
        self.pt_bins_lf = np.array([20, 30, 40, 60, 10000])
        self.eta_bins_lf = np.array([0, 0.8, 1.6, 2.41])
        if self.debug:
            print "[BTagWeightCalculator] HF pt bins", self.pt_bins_hf
            print "[BTagWeightCalculator] HF eta bins", self.eta_bins_hf
            print "[BTagWeightCalculator] LF pt bins", self.pt_bins_lf
            print "[BTagWeightCalculator] LF eta bins", self.eta_bins_lf
        
        self.btag = btag_name
        self.init(fn_hf, fn_lf)

    def getBin(self, bvec, val):
        return int(bvec.searchsorted(val) - 1)

    def init(self, fn_hf, fn_lf):
        """
        fn_hf: filename with heavy-flavour scale factors 
        fn_lf: filename with light-flavour scale factors 
        """
        print "[BTagWeightCalculator]: Initializing from files", fn_hf, fn_lf

        self.pdfs["hf"] = self.getHistosFromFile(fn_hf)
        self.pdfs["lf"] = self.getHistosFromFile(fn_lf)

        return True

    def getHistosFromFile(self, fn):
        ret = {}
        tf = ROOT.TFile(fn)
        if not tf or tf.IsZombie():
            raise FileError("Could not open file {0}".format(fn))
        ROOT.gROOT.cd()
        for k in tf.GetListOfKeys():
            kn = k.GetName()
            if not kn.startswith("csv_ratio"):
                continue
            spl = kn.split("_")

            if spl[2] == "all":
                ptbin = -1
                etabin = -1
                kind = "all"
                syst = "nominal"
            else:
                ptbin = int(spl[2][2:])
                etabin = int(spl[3][3:])
                kind = spl[4]
                if len(spl)==6:
                    syst = spl[5]
                else:
                    syst = "nominal"
            ret[(ptbin, etabin, kind, syst)] = k.ReadObj().Clone()
        return ret

    def calcJetWeight(self, jet, kind, systematic):
        pt = jet.pt()
        aeta = abs(jet.eta())
        fl = abs(jet.mcFlavour)
        csv = jet.btag(self.btag)

        is_heavy = (fl == 5 or fl == 6)
        if is_heavy:
            ptbin = self.getBin(self.pt_bins_hf, pt)
            etabin = self.getBin(self.eta_bins_hf, aeta)
        else:
            ptbin = self.getBin(self.pt_bins_lf, pt)
            etabin = self.getBin(self.eta_bins_lf, aeta)

        if ptbin < 0 or etabin < 0:
            return 1.0

        k = (ptbin, etabin, kind, systematic)
        hdict = self.pdfs["lf"]
        if is_heavy:
            hdict = self.pdfs["hf"]
        h = hdict.get(k, None)
        if not h:
            return 1.0

        #Remember to set CSV to 1.0 for cases where CSV > 1.0.
        #https://twiki.cern.ch/twiki/bin/view/CMS/TTbarHbbRun2ReferenceAnalysis#Event_Selection
        if csv>=1:
            csv = 1
        
        csvbin = 1
        if csv>=0:
            csvbin = h.FindBin(csv)

        if csvbin <= 0 or csvbin > h.GetNbinsX():
            return 1.0
        w = h.GetBinContent(csvbin)
        return w

    def calcEventWeight(self, jets, kind, systematic):
        weights = np.array(
            [self.calcJetWeight(jet, kind, systematic)
            for jet in jets]
        )

        wtot = np.prod(weights)
        return wtot
