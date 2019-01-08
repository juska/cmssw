#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DQMServices/Core/interface/DQMStore.h"
#include "DQMServices/Core/interface/DQMEDAnalyzer.h"
#include "DQMServices/Core/interface/MonitorElement.h"
#include "FWCore/Framework/interface/Event.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

#include <regex>
#include <sstream>
#include <numeric>
 
class ParticleFlowDQM : public DQMEDAnalyzer {
    public:

        ParticleFlowDQM(const edm::ParameterSet&);
        void analyze(const edm::Event&, const edm::EventSetup&) override;

    protected:
        //Book histograms
        void bookHistograms(DQMStore::IBooker &, edm::Run const &, edm::EventSetup const &) override;
        void dqmBeginRun(const edm::Run&, const edm::EventSetup&) override {}
        void endRun(const edm::Run&, const edm::EventSetup&) override {}
      
    private:
        class Plot {
            public: 
                Plot(MonitorElement * me) : plot_(me) {}
                virtual ~Plot() {}
                const std::string & name() const { return plot_->getName(); }
                void fill(double value) { plot_->Fill(value); };
            protected:
                MonitorElement * plot_;
        };

        class Plot1D : public Plot {
            public:
                Plot1D(DQMStore::IBooker & booker, const std::string name, const std::string title, const uint32_t nbins, const double min, const double max) :
                    Plot(booker.book1D(name, title, nbins, min, max))
                {
                }
                ~Plot1D() override {}
        };

        std::unique_ptr<Plot1D> plot;


 };

ParticleFlowDQM::ParticleFlowDQM(const edm::ParameterSet & iConfig) 
{
}

void ParticleFlowDQM::bookHistograms(DQMStore::IBooker & booker, edm::Run const &, edm::EventSetup const &) {
    std::cout << "ParticleFlowDQM booking histograms" << std::endl;
    booker.setCurrentFolder("Physics/ParticleFlowDQM");
    plot = std::make_unique<Plot1D>(booker, "testPF", "testPF", 100, 0, 300); 
}

void ParticleFlowDQM::analyze(const edm::Event &iEvent, const edm::EventSetup &) {
    plot->fill(1.0);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(ParticleFlowDQM);
