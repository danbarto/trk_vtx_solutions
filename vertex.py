#!/usr/bin/env python3

import DataFormats.FWLite as fwlite
import math
import ROOT
from utils import fnal_path as in_path
import os

# make an output directory
odir = "{0}/{1}/".format("plots", "vertex")
if not os.path.isdir(odir):
    os.makedirs(odir)

events = fwlite.Events(in_path+"run321167_ZeroBias_AOD.root")
primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")
tracks = fwlite.Handle("std::vector<reco::Track>")

rho_z_histogram = ROOT.TH2F("rho_z", "rho_z", 100, 0.0, 30.0, 100, 0.0, 10.0)

events.toBegin()
for event in events:
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    for vertex in primaryVertices.product():
        rho_z_histogram.Fill(abs(vertex.z()),
                             math.sqrt(vertex.x()**2 + vertex.y()**2))

c = ROOT.TCanvas("c", "c", 800, 800)
rho_z_histogram.Draw()
c.SaveAs(odir+"rho_z.png")

deltaz_histogram = ROOT.TH1F("deltaz", "deltaz", 1000, -20.0, 20.0)

events.toBegin()
for event in events:
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    pv = primaryVertices.product()
    for i in xrange(pv.size() - 1):
        for j in xrange(i + 1, pv.size()):
            deltaz_histogram.Fill(pv[i].z() - pv[j].z())

c = ROOT.TCanvas ("c", "c", 800, 800)
deltaz_histogram.Draw()
c.SaveAs(odir+"deltaz.png")

events.toBegin()
for i, event in enumerate(events):
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    print "Pile-up:", primaryVertices.product().size()
    if i > 100: break

histogram = ROOT.TH2F("ntracks_vs_nvertex","ntracks_vs_nvertex",
                      30, 0.0, 29.0, 100, 0.0,2000.0)

events.toBegin()
for event in events:
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    event.getByLabel("generalTracks", tracks)
    histogram.Fill(primaryVertices.product().size(), tracks.product().size())

c = ROOT.TCanvas("c", "c", 800, 800)
histogram.Draw()
c.SaveAs(odir+"ntracks_vs_nvertex.png")
