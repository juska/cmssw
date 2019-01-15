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
description = "Simple ParticleFlow comparison"

plotterDrawArgs = dict(
    separate=False, # Set to true if you want each plot in it's own canvas
#    ratio=False,   # Uncomment to disable ratio pad
)

if len(sys.argv) != 3:
    print "Usage: compare.py path1 path2"
    print "where path1 and path2 are the folders that contain the [TTBar|QCD|ZMM]/DQM*.root output of 'make all'"
    sys.exit(0)

#paths to the relval runs
path1 = sys.argv[1]
path2 = sys.argv[2]

# Pairs of file names and legend labels
filesLabels = [
    (path1 + "/TTbar/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root", "Option 1"),
    (path2 + "/TTbar/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root", "Option 2"),
]
# Files are grouped together as a "sample" (the files don't
# necessarily have to come from the same sample, like ttbar, but this
# is the abstraction here)
sample1 = SimpleSample("RelVal_TTbar13", # Prefix for subdirectory names
                      "RelVal_TTbar13",   # The name appears in the HTML pages
                      filesLabels)     # Files and legend labels

filesLabels = [
    (path1 + "/QCD/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root", "Option 1"),
    (path2 + "/QCD/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root", "Option 2"),
]
sample2 = SimpleSample("RelVal_QCD", # Prefix for subdirectory names
                      "RelVal_QCD",   # The name appears in the HTML pages
                      filesLabels)     # Files and legend labels

filesLabels = [
    (path1 + "/ZMM/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root", "Option 1"),
    (path2 + "/ZMM/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root", "Option 2"),
]
sample3 = SimpleSample("RelVal_ZMM", # Prefix for subdirectory names
                      "RelVal_ZMM",   # The name appears in the HTML pages
                      filesLabels)     # Files and legend labels

# You can produce plots for multiple samples on one. Just construct
# multiple SimpleSample objects like above and add them to the list
# below.
samples = [
    sample1,
    sample2,
    sample3
]

def addPlots(plotter, folder, name, section, bin_range):
    folders = [folder]
    plots = [PlotGroup(name, [Plot("Bin{0}".format(ibin)) for ibin in bin_range])]
    plotter.append("ParticleFlow", folders, PlotFolder(*plots, loopSubFolders=False, page="pf", section=section))

plotter = Plotter()

addPlots(plotter, "DQMData/Run 1/Physics/Run summary/JetResponse/ByGenJetPt", "ByGenJetPt1", "JetResponse", range(0,6))
addPlots(plotter, "DQMData/Run 1/Physics/Run summary/JetResponse/ByGenJetPt", "ByGenJetPt2", "JetResponse", range(6,12))

addPlots(plotter, "DQMData/Run 1/Physics/Run summary/JetResponse/ByGenJetEta", "ByGenJetEta1", "JetResponse", range(0,6))
addPlots(plotter, "DQMData/Run 1/Physics/Run summary/JetResponse/ByGenJetEta", "ByGenJetEta2", "JetResponse", range(6,12))
addPlots(plotter, "DQMData/Run 1/Physics/Run summary/JetResponse/ByGenJetEta", "ByGenJetEta3", "JetResponse", range(12,13))

val = SimpleValidation(samples, outputDir)
report = val.createHtmlReport(validationName=description)
val.doPlots([plotter],
    plotterDrawArgs=plotterDrawArgs,
)
report.write()
