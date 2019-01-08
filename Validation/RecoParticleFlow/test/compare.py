#!/usr/bin/env python

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
    ("../tmp2/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root", "Option 1"),
    ("../tmp2/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root", "Option 2"),
]
# Files are grouped together as a "sample" (the files don't
# necessarily have to come from the same sample, like ttbar, but this
# is the abstraction here)
sample = SimpleSample("RelVal", # Prefix for subdirectory names
                      "TTbar13",   # The name appears in the HTML pages
                      filesLabels)     # Files and legend labels

# You can produce plots for multiple samples on one. Just construct
# multiple SimpleSample objects like above and add them to the list
# below.
samples = [
    sample
]

plotter = Plotter()

#make one plot
folder = [
    "DQMData/Run 1/ParticleFlow/Run summary/PFJetValidation/CompWithGenJet",
]
plots = [
    PlotGroup("CompWithGenJet", [
        Plot("pt_"),
        Plot("eta_"),
        Plot("phi_"),
    ])
]
plotter.append("ParticleFlow", folder, PlotFolder(*plots, loopSubFolders=False, page="pf", section="PFJetValidation"))

#make another one
folder = [
    "DQMData/Run 1/ParticleFlow/Run summary/PFJetValidation/CompWithCaloJet",
]
plots = [
    PlotGroup("CompWithCaloJet", [
        Plot("pt_"),
        Plot("eta_"),
        Plot("phi_"),
    ])
]
plotter.append("ParticleFlow", folder, PlotFolder(*plots, loopSubFolders=False, page="pf", section="PFJetValidation"))

val = SimpleValidation(samples, outputDir)
report = val.createHtmlReport(validationName=description)
val.doPlots([plotter],
    plotterDrawArgs=plotterDrawArgs,
)
report.write()
