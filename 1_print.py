#!/usr/bin/env python3
from utils import fnal_path as in_path

import DataFormats.FWLite as fwlite
events = fwlite.Events(in_path+"run321167_ZeroBias_AOD.root")
tracks = fwlite.Handle("std::vector<reco::Track>")

for i, event in enumerate(events):
    if i >= 5: break # print info only about the first 5 events
    print "Event", i
    event.getByLabel("generalTracks", tracks)
    numTotal = tracks.product().size()
    print "total tracks: ", numTotal
    for j, track in enumerate(tracks.product()):
        if j >= 5: break # print info only about the first 5 tracks
        print "    Track", j,
        print "\t charge/pT: %.3f" %(track.charge()/track.pt()),
        print "\t phi: %.3f" %track.phi(),
        print "\t eta: %.3f" %track.eta(),
        print "\t dxy: %.4f" %track.dxy(),
        print "\t dz: %.4f"  %track.dz()
