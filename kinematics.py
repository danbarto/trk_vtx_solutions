#!/usr/bin/env python3

import DataFormats.FWLite as fwlite
import ROOT
import math
from utils import fnal_path as in_path

events = fwlite.Events(in_path+"run321167_ZeroBias_AOD.root")
tracks = fwlite.Handle("std::vector<reco::Track>")

for i, event in enumerate(events):
    event.getByLabel("generalTracks", tracks)
    for track in tracks.product():
        print track.pt(), track.p(), track.px(), track.py(), track.pz()
        print "energy: ", math.sqrt(0.140**2 + track.p()**2)
    if i > 20: break

events.toBegin()
for i, event in enumerate(events):
    if i >= 15: break            # only the first 15 events
    print "Event", i
    event.getByLabel("globalMuons", tracks)
    for j, track in enumerate(tracks.product()):
        print "    Track", j, track.charge()/track.pt(), track.phi(), track.eta(), track.dxy(), track.dz()
