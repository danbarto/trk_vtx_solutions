#!/usr/bin/env python3

import DataFormats.FWLite as fwlite
import ROOT
import os

# make an output directory
odir = "{0}/{1}/".format("plots", "sv")
if not os.path.isdir(odir):
    os.makedirs(odir)


events = fwlite.Events("file:output.root")
secondaryVertices = fwlite.Handle("std::vector<reco::VertexCompositeCandidate>")

mass_histogram = ROOT.TH1F("mass", "mass", 100, 0.4, 0.6)

events.toBegin()
for event in events:
    event.getByLabel("SecondaryVerticesFromLooseTracks", "Kshort", secondaryVertices)
    for vertex in secondaryVertices.product():
        mass_histogram.Fill(vertex.mass())

c = ROOT.TCanvas ("c" , "c", 800, 800)
mass_histogram.Draw()
c.SaveAs(odir+"kshort_mass.png")



mass_histogram = ROOT.TH1F("mass", "mass", 100, 1.1, 1.16)

events.toBegin()
for event in events:
    event.getByLabel("SecondaryVerticesFromLooseTracks", "Lambda", secondaryVertices)
    for vertex in secondaryVertices.product():
        mass_histogram.Fill(vertex.mass())

c = ROOT.TCanvas ("c" , "c", 800, 800)
mass_histogram.Draw()
c.SaveAs(odir+"lambda_mass.png")
