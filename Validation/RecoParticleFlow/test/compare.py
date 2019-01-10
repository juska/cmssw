#!/usr/bin/env python
import sys

# This is an example of plotting the standard tracking validation
# plots from an explicit set of DQM root files.

from Validation.RecoTrack.plotting.validation import SimpleValidation, SimpleSample
import Validation.RecoTrack.plotting.trackingPlots as trackingPlots
import Validation.RecoVertex.plotting.vertexPlots as vertexPlots

from Validation.RecoTrack.plotting.plotting import Subtract, FakeDuplicate, CutEfficiency, Transform, AggregateBins, ROC, Plot, PlotEmpty, PlotGroup, PlotOnSideGroup, PlotFolder, Plotter
from Validation.RecoTrack.plotting.html import PlotPurpose

outputDir = "plots" # Plot output directory
description = "Short description of your comparison"

plotterDrawArgs = dict(
    separate=False, # Set to true if you want each plot in it's own canvas
#    ratio=False,   # Uncomment to disable ratio pad
)

# Pairs of file names and legend labels
filesLabels = [
    ("tmp/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root", "Option 1"),
    ("tmp/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root", "Option 2"),
]
# Files are grouped together as a "sample" (the files don't
# necessarily have to come from the same sample, like ttbar, but this
# is the abstraction here)
sample1 = SimpleSample("RelVal_TTbar13", # Prefix for subdirectory names
                      "RelVal_TTbar13",   # The name appears in the HTML pages
                      filesLabels)     # Files and legend labels

filesLabels = [
    ("tmp2/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root", "Option 1"),
    ("tmp2/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root", "Option 2"),
]
sample2 = SimpleSample("RelVal_QCD", # Prefix for subdirectory names
                      "RelVal_QCD",   # The name appears in the HTML pages
                      filesLabels)     # Files and legend labels

filesLabels = [
    ("tmp3/Zmm/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root", "Option 1"),
    ("tmp3/Zmm/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root", "Option 2"),
]
sample3 = SimpleSample("RelVal_Zmm", # Prefix for subdirectory names
                      "RelVal_Zmm",   # The name appears in the HTML pages
                      filesLabels)     # Files and legend labels

# You can produce plots for multiple samples on one. Just construct
# multiple SimpleSample objects like above and add them to the list
# below.
samples = [
    sample1,
    sample2,
#    sample3
]

plotter = Plotter()


folder = [
    "DQMData/Run 1/Physics/Run summary/JetResponse/ByGenJetPt",
]
plots = [
    PlotGroup("ByGenJetPt1", [
        Plot("Bin0"),
        Plot("Bin1"),
        Plot("Bin2"),
        Plot("Bin3"),
        Plot("Bin4"),
        Plot("Bin5"),
    ])
]
plotter.append("ParticleFlow", folder, PlotFolder(*plots, loopSubFolders=False, page="pf", section="JetResponse"))

plots = [
    PlotGroup("ByGenJetPt2", [
        Plot("Bin6"),
        Plot("Bin7"),
        Plot("Bin8"),
        Plot("Bin9"),
        Plot("Bin10"),
        Plot("Bin11"),
    ])
]
plotter.append("ParticleFlow", folder, PlotFolder(*plots, loopSubFolders=False, page="pf", section="JetResponse"))



folder = [
    "DQMData/Run 1/Physics/Run summary/JetResponse/ByGenJetEta",
]
plots = [
    PlotGroup("ByGenJetEta1", [
        Plot("Bin0"),
        Plot("Bin1"),
        Plot("Bin2"),
        Plot("Bin3"),
        Plot("Bin4"),
        Plot("Bin5"),
    ])
]
plotter.append("ParticleFlow", folder, PlotFolder(*plots, loopSubFolders=False, page="pf", section="JetResponse"))


plots = [
    PlotGroup("ByGenJetEta2", [
        Plot("Bin6"),
        Plot("Bin7"),
        Plot("Bin8"),
        Plot("Bin9"),
        Plot("Bin10"),
        Plot("Bin11"),
    ])
]
plotter.append("ParticleFlow", folder, PlotFolder(*plots, loopSubFolders=False, page="pf", section="JetResponse"))



plots = [
    PlotGroup("ByGenJetEta3", [
        Plot("Bin12"),
    ])
]
plotter.append("ParticleFlow", folder, PlotFolder(*plots, loopSubFolders=False, page="pf", section="JetResponse"))



val = SimpleValidation(samples, outputDir)
report = val.createHtmlReport(validationName=description)
val.doPlots([plotter],
    plotterDrawArgs=plotterDrawArgs,
)
report.write()
