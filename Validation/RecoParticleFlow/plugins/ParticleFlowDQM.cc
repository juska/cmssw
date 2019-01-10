#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DQMOffline/PFTau/interface/Matchers.h"
#include "DQMServices/Core/interface/DQMEDAnalyzer.h"
#include "DQMServices/Core/interface/DQMStore.h"
#include "DQMServices/Core/interface/MonitorElement.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include <algorithm>
#include <numeric>
#include <regex>
#include <sstream>
#include <vector>

class ParticleFlowDQM : public DQMEDAnalyzer {
public:
    ParticleFlowDQM(const edm::ParameterSet&);
    void analyze(const edm::Event&, const edm::EventSetup&) override;

protected:
    //Book histograms
    void bookHistograms(DQMStore::IBooker&, edm::Run const&, edm::EventSetup const&) override;
    void dqmBeginRun(const edm::Run&, const edm::EventSetup&) override {}
    void endRun(const edm::Run&, const edm::EventSetup&) override {}

private:
    class Plot {
    public:
        Plot(MonitorElement* me)
            : plot_(me)
        {
        }
        virtual ~Plot() {}
        const std::string& name() const { return plot_->getName(); }
        void fill(double value) { plot_->Fill(value); };

    protected:
        MonitorElement* plot_;
    };

    class Plot1D : public Plot {
    public:
        Plot1D(DQMStore::IBooker& booker, const std::string name, const std::string title, const uint32_t nbins, const double min, const double max)
            : Plot(booker.book1D(name, title, nbins, min, max))
        {
        }
        ~Plot1D() override {}
    };

    std::vector<Plot1D> jetResponsePlotByGenJetPt;
    std::vector<Plot1D> jetResponsePlotByGenJetEta;

    double jetDeltaR;
    std::vector<double> genJetPtBins;
    std::vector<double> genJetEtaBins;
    int responseNbins;
    double responseLow;
    double responseHigh;

    edm::InputTag recoJetsLabel;
    edm::InputTag genJetsLabel;
    edm::EDGetTokenT<edm::View<reco::Jet>> recoJetsToken;
    edm::EDGetTokenT<edm::View<reco::Jet>> genJetsToken;

    void fillJetResponse(edm::View<reco::Jet>& recoJetCollection, edm::View<reco::Jet>& genJetCollection);
};

template <typename T>
std::string histogram_name(std::string s1, T v1)
{
    std::stringstream ss;
    ss << s1 << v1;
    return ss.str();
}

ParticleFlowDQM::ParticleFlowDQM(const edm::ParameterSet& iConfig)
{
    recoJetsLabel = iConfig.getParameter<edm::InputTag>("recoJetCollection");
    genJetsLabel = iConfig.getParameter<edm::InputTag>("genJetCollection");

    //DeltaR for reco to gen jet matching
    jetDeltaR = iConfig.getParameter<double>("jetDeltaR");

    //Ordered increasing vector of pt and eta bins for the response histograms
    genJetPtBins = iConfig.getParameter<std::vector<double>>("genJetPtBins");
    genJetEtaBins = iConfig.getParameter<std::vector<double>>("genJetEtaBins");

    //Response histogram nbins, low and high bin
    responseNbins = iConfig.getParameter<int>("responseNbins");
    responseLow = iConfig.getParameter<double>("responseLow");
    responseHigh = iConfig.getParameter<double>("responseHigh");

    recoJetsToken = consumes<edm::View<reco::Jet>>(recoJetsLabel);
    genJetsToken = consumes<edm::View<reco::Jet>>(genJetsLabel);
}

void ParticleFlowDQM::bookHistograms(DQMStore::IBooker& booker, edm::Run const&, edm::EventSetup const&)
{
    std::cout << "ParticleFlowDQM booking histograms" << std::endl;

    //For each pt bin, create a histogram
    booker.setCurrentFolder("Physics/JetResponse/ByGenJetPt");
    for (unsigned int iBin = 0; iBin < genJetPtBins.size(); iBin++) {
        auto ptbin = genJetPtBins.at(iBin);
        Plot1D plot(
            booker,
            histogram_name("Bin", iBin),
            histogram_name("Jet response (pTreco / pTgen) in gen-jet pt bin ", ptbin),
            responseNbins, responseLow, responseHigh);
        jetResponsePlotByGenJetPt.push_back(plot);
    }
    assert(jetResponsePlotByGenJetPt.size() == genJetPtBins.size());

    //For each eta bin, create a histogram
    booker.setCurrentFolder("Physics/JetResponse/ByGenJetEta");
    for (unsigned int iBin = 0; iBin < genJetEtaBins.size(); iBin++) {
        auto etabin = genJetEtaBins.at(iBin);
        Plot1D plot(
            booker,
            histogram_name("Bin", iBin),
            histogram_name("Jet response (pTreco / pTgen) in gen-jet eta bin ", etabin),
            responseNbins, responseLow, responseHigh);
        jetResponsePlotByGenJetEta.push_back(plot);
    }
    assert(jetResponsePlotByGenJetEta.size() == genJetEtaBins.size());
}

//Given an ordered vector of bins and a value, returns the index of the last item that's smaller than the value
//Will return 0 in case value is too small or bins.size()-1 in case value is too large for the bins.
unsigned int getIndexFromOrderedVector(std::vector<double> bins, double val)
{
    auto idx = std::lower_bound(bins.begin(), bins.end(), val) - bins.begin();
    if (idx < 0) {
        idx = 0;
    } else if ((unsigned int)idx >= bins.size()) {
        idx -= 1;
    }
    auto uidx = static_cast<unsigned int>(idx);

    assert(uidx < bins.size());
    return uidx;
}

void ParticleFlowDQM::fillJetResponse(
    edm::View<reco::Jet>& recoJetCollection,
    edm::View<reco::Jet>& genJetCollection)
{

    //match reco jets to gen jets by DeltaR
    std::vector<int> matchIndices;
    PFB::match(recoJetCollection, genJetCollection, matchIndices, false, jetDeltaR);

    for (unsigned int i = 0; i < recoJetCollection.size(); i++) {

        const auto& recoJet = recoJetCollection.at(i);
        int iMatch = matchIndices[i];

        //If reco jet had a matched gen-jet
        if (iMatch != -1) {
            const auto& matchedJet = genJetCollection[iMatch];
            const auto pt_reco = recoJet.pt();
            const auto pt_gen = matchedJet.pt();
            const auto eta_gen = matchedJet.eta();
            const auto response = pt_reco / pt_gen;

            //Fill the pt-binned response histogram
            auto idx1 = getIndexFromOrderedVector(genJetPtBins, pt_gen);
            auto& hist1 = jetResponsePlotByGenJetPt.at(idx1);
            hist1.fill(response);

            //Fill the eta-binned response histogram
            auto idx2 = getIndexFromOrderedVector(genJetEtaBins, eta_gen);
            auto& hist2 = jetResponsePlotByGenJetEta.at(idx2);
            hist2.fill(response);
        }
    }
}

void ParticleFlowDQM::analyze(const edm::Event& iEvent, const edm::EventSetup&)
{

    edm::Handle<edm::View<reco::Jet>> recoJetCollectionHandle;
    iEvent.getByToken(recoJetsToken, recoJetCollectionHandle);

    edm::Handle<edm::View<reco::Jet>> genJetCollectionHandle;
    iEvent.getByToken(genJetsToken, genJetCollectionHandle);

    auto recoJetCollection = *recoJetCollectionHandle;
    auto genJetCollection = *genJetCollectionHandle;

    fillJetResponse(recoJetCollection, genJetCollection);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(ParticleFlowDQM);
