#!/usr/bin/env python3

import DataFormats.FWLite as fwlite
import ROOT
import os

# make an output directory
odir = "{0}/{1}/".format("plots", "lxy")
if not os.path.isdir(odir):
    os.makedirs(odir)

events = fwlite.Events("file:output.root")
secondaryVertices = fwlite.Handle("std::vector<reco::VertexCompositeCandidate>")
primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")

lxy_histogram = ROOT.TH1F("lxy", "lxy", 500, 0, 70)

events.toBegin()
for event in events:
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    pv = primaryVertices.product()[0]
    event.getByLabel("SecondaryVerticesFromLooseTracks", "Lambda", secondaryVertices)
    for vertex in secondaryVertices.product():
        lxy = ((vertex.vx()-pv.x())**2 + (vertex.vy() - pv.y())**2)**0.5
        lxy_histogram.Fill(lxy)
c = ROOT.TCanvas ("c" , "c", 800, 800)
lxy_histogram.Draw()
c.SaveAs(odir+"lambda_lxy.png")
