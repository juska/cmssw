import ROOT
from math import copysign

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

class CountAnalyzer( Analyzer ):
    
    def declareHandles(self):
        super(CountAnalyzer, self).declareHandles()
        if self.cfg_comp.isMC:
            self.handles['GenInfo'] = AutoHandle( ('generator','',''), 'GenEventInfoProduct' )
            self.handles['PDFWeightsProducer'] = AutoHandle( ('PDFWeightsProducer','outputHessianWeights','EX'), 'std::vector<float>' )
    
    def beginLoop(self,setup):
        super(CountAnalyzer,self).beginLoop(setup)
        outservice_name = "PhysicsTools.HeppyCore.framework.services.tfile.TFileService_outputfile"
        if outservice_name in setup.services :
            setup.services[outservice_name].file.cd()
            self.inputCounter = ROOT.TH1F("Count","Count",1,0,2)
            self.inputCounterFullWeighted = ROOT.TH1F("CountFullWeighted","Count with gen weight and pu weight",1,0,2)
            self.inputCounterWeighted = ROOT.TH1F("CountWeighted","Count with sign(gen weight) and pu weight",1,0,2)
            self.inputCounterPosWeight = ROOT.TH1F("CountPosWeight","Count genWeight>0",1,0,2)
            self.inputCounterNegWeight = ROOT.TH1F("CountNegWeight","Count genWeight<0",1,0,2)
            #for LHE_scale in range(6):
            setattr(self, "inputCounterWeightedLHEWeightScale", ROOT.TH1F("CountWeightedLHEWeightScale","Count with gen weight x LHE_weights_scale and pu weight",6,-0.5,5.5))
            setattr(self, "inputCounterWeightedLHEWeightPdf", ROOT.TH1F("CountWeightedLHEWeightPdf","Count with gen weight x LHE_weights_pdf and pu weight",103,-0.5,102.5))
            #for LHE_pdf in range(2):
            #   setattr(self, "inputCounterWeightedLHEWeightPdf_"+str(LHE_pdf), ROOT.TH1F("CountWeightedLHEWeightPdf_"+str(LHE_pdf),"Count with gen weight x LHE_weights_pdf["+str(LHE_pdf)+"] and pu weight",1,0,2))
    
    def process(self, event):
	#print "Event number",event.iEv
        self.readCollections( event.input )
        self.inputCounter.Fill(1)
        event.LHE_weights_pdf_eigen = []
        if self.cfg_comp.isMC:
            try:
                event.LHE_weights_pdf_eigen = self.handles['PDFWeightsProducer'].product()
            except Exception:
                pass
            genWeight = self.handles['GenInfo'].product().weight()
            self.inputCounterWeighted.Fill(1,copysign(1.0,genWeight)*event.puWeight)
            self.inputCounterFullWeighted.Fill(1,genWeight*event.puWeight)
            for LHE_scale in range(len(event.LHE_weights_scale)): 
               getattr(self, "inputCounterWeightedLHEWeightScale").Fill(LHE_scale,copysign(1.0, genWeight)*event.puWeight*(event.LHE_weights_scale[LHE_scale]).wgt) 
            for LHE_pdf in range(len(event.LHE_weights_pdf)): 
               getattr(self, "inputCounterWeightedLHEWeightPdf").Fill(LHE_pdf,copysign(1.0, genWeight)*event.puWeight*(event.LHE_weights_pdf[LHE_pdf]).wgt) 
            if genWeight > 0:
                self.inputCounterPosWeight.Fill(1)
            elif genWeight < 0:
                self.inputCounterNegWeight.Fill(1)
