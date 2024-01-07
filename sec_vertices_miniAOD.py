#!/usr/bin/env python3

import DataFormats.FWLite as fwlite
import ROOT
import os

# make an output directory
odir = "{0}/{1}/".format("plots", "sv")
if not os.path.isdir(odir):
    os.makedirs(odir)

events = fwlite.Events("/eos/uscms/store/user/cmsdas/2024/short_exercises/trackingvertexing/run321167_Charmonium_MINIAOD.root")
secondaryVertices = fwlite.Handle("std::vector<reco::VertexCompositePtrCandidate>")

mass_histogram = ROOT.TH1F("mass_histogram", "mass_histogram", 100, 1., 1.2)

events.toBegin()
for i, event in enumerate(events):
    event.getByLabel("slimmedLambdaVertices", "", secondaryVertices)
    for j, vertex in enumerate(secondaryVertices.product()):
        mass_histogram.Fill(vertex.mass())

c = ROOT.TCanvas()
mass_histogram.Draw()
c.SaveAs(odir+"mass_lambda_miniaod.png")
