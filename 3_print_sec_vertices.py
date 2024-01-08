#!/usr/bin/env python3

import DataFormats.FWLite as fwlite

events = fwlite.Events("file:output.root")
secondaryVertices = fwlite.Handle("std::vector<reco::VertexCompositeCandidate>")

events.toBegin()
for i, event in enumerate(events):
    print "Event:", i
    event.getByLabel("SecondaryVerticesFromLooseTracks", "Kshort", secondaryVertices)
    for j, vertex in enumerate(secondaryVertices.product()):
        print "    Vertex:", j, vertex.vx(), vertex.vy(), vertex.vz()
    if i > 10: break
