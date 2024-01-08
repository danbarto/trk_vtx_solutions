#!/usr/bin/env python3

import DataFormats.FWLite as fwlite
import ROOT
import os
ROOT.gROOT.SetBatch(True) # this allows pyroot to run in batch mode - which prevents the histograms from being displayed every time they are drawn.

events = fwlite.Events("root://cmseos.fnal.gov//store/user/cmsdas/2024/short_exercises/trackingvertexing/run321167_ZeroBias_MINIAOD.root")
eventsAOD = fwlite.Events("root://cmseos.fnal.gov//store/user/cmsdas/2024/short_exercises/trackingvertexing/run321167_ZeroBias_AOD.root")

tracks     = fwlite.Handle("std::vector<pat::PackedCandidate>")
losttracks = fwlite.Handle("std::vector<pat::PackedCandidate>")
tracksAOD = fwlite.Handle("std::vector<reco::Track>")

hist_pt       = ROOT.TH1F("pt",       "track pt; p_{T} [GeV]", 100, 0.0, 100.0)
hist_lowPt       = ROOT.TH1F("lowPt",       "track pt; p_{T} [GeV]", 100, 0.0, 5.0)
hist_eta      = ROOT.TH1F("eta",      "track eta; #eta", 60, -3.0, 3.0)
hist_phi      = ROOT.TH1F("phi",      "track phi; #phi", 64, -3.2, 3.2)

hist_normChi2     = ROOT.TH1F("hist_normChi2"    , "norm. chi2; norm #chi^{2}"        , 100, 0.0, 10.0)
hist_numPixelHits = ROOT.TH1F("hist_numPixelHits", "pixel hits; # pixel hits"         , 15, -0.5, 14.5)
hist_numValidHits = ROOT.TH1F("hist_numValidHits", "valid hits; # valid hits"         , 35, -0.5, 34.5)
hist_numTkLayers  = ROOT.TH1F("hist_numTkLayers" , "valid layers; # valid Tk layers"  , 25, -0.5, 24.5)

hist_pt_AOD       = ROOT.TH1F("ptAOD",       "track pt; p_{T} [GeV]", 100, 0.0, 100.0)
hist_lowPt_AOD    = ROOT.TH1F("lowPtAOD",       "track pt; p_{T} [GeV]", 100, 0.0, 5.0)
hist_eta_AOD      = ROOT.TH1F("etaAOD",      "track eta; #eta", 60, -3.0, 3.0)
hist_phi_AOD      = ROOT.TH1F("phiAOD",      "track phi; #phi", 64, -3.2, 3.2)

hist_normChi2_AOD     = ROOT.TH1F("hist_normChi2AOD"    , "norm. chi2; norm #chi^{2}"        , 100, 0.0, 10.0)
hist_numPixelHits_AOD = ROOT.TH1F("hist_numPixelHitsAOD", "pixel hits; # pixel hits"         , 15, -0.5, 14.5)
hist_numValidHits_AOD = ROOT.TH1F("hist_numValidHitsAOD", "valid hits; # valid hits"         , 35, -0.5, 34.5)
hist_numTkLayers_AOD  = ROOT.TH1F("hist_numTkLayersAOD" , "valid layers; # valid Tk layers"  , 25, -0.5, 24.5)

hist_pt_AOD.SetLineColor(ROOT.kRed)
hist_lowPt_AOD.SetLineColor(ROOT.kRed)
hist_eta_AOD.SetLineColor(ROOT.kRed)
hist_phi_AOD.SetLineColor(ROOT.kRed)

hist_normChi2_AOD.SetLineColor(ROOT.kRed)
hist_numPixelHits_AOD.SetLineColor(ROOT.kRed)
hist_numValidHits_AOD.SetLineColor(ROOT.kRed)
hist_numTkLayers_AOD.SetLineColor(ROOT.kRed)

for i, event in enumerate(events):
    event.getByLabel("packedPFCandidates", "", tracks)
    event.getByLabel("lostTracks", "", losttracks)

    alltracks  = [track for track in tracks.product()]
    alltracks += [track for track in losttracks.product()]

    for track in alltracks :
        if (not track.hasTrackDetails() or track.charge() == 0 ):
            continue
        if not track.trackHighPurity():
            continue
        hist_pt.Fill(track.pt())
        hist_lowPt.Fill(track.pt())
        hist_eta.Fill(track.eta())
        hist_phi.Fill(track.phi())

        hist_normChi2    .Fill(track.pseudoTrack().normalizedChi2())
        hist_numPixelHits.Fill(track.numberOfPixelHits())
        hist_numValidHits.Fill(track.pseudoTrack().hitPattern().numberOfValidHits())
        hist_numTkLayers .Fill(track.pseudoTrack().hitPattern().trackerLayersWithMeasurement())

    if i > 1000: break

for i, event in enumerate(eventsAOD):
    event.getByLabel("generalTracks", tracksAOD)

    for j, track in enumerate(tracksAOD.product()) :
        if not track.quality(track.qualityByName("highPurity")):
            continue

        hist_pt_AOD.Fill(track.pt())
        hist_lowPt_AOD.Fill(track.pt())
        hist_eta_AOD.Fill(track.eta())
        hist_phi_AOD.Fill(track.phi())

        hist_normChi2_AOD    .Fill(track.normalizedChi2())
        hist_numPixelHits_AOD.Fill(track.hitPattern().numberOfValidPixelHits())
        hist_numValidHits_AOD.Fill(track.hitPattern().numberOfValidHits())
        hist_numTkLayers_AOD .Fill(track.hitPattern().trackerLayersWithMeasurement())

    if i > 1000: break

c = ROOT.TCanvas( "c", "c", 800, 800)

# make an output directory
odir = "{0}/{1}/".format("plots", "miniAOD")
if not os.path.isdir(odir):
    os.makedirs(odir)

# draw and save histograms as pdf files (can alternatively save as png by replacing .pdf with .png
hist_pt.Draw()
hist_pt_AOD.Draw("same")
c.SetLogy()
c.SaveAs(odir+"track_pt_miniaod.pdf")

hist_lowPt_AOD.Draw()
hist_lowPt.Draw("same")
c.SetLogy()
c.SaveAs(odir+"track_lowPt_miniaod.pdf")
c.SetLogy(False)
hist_eta_AOD.Draw()
hist_eta.Draw("same")
c.SaveAs(odir+"track_eta_miniaod.pdf")
hist_phi_AOD.Draw()
hist_phi.Draw("same")
c.SaveAs(odir+"track_phi_miniaod.pdf")

hist_normChi2_AOD.Draw()
hist_normChi2.Draw("same")
c.SaveAs(odir+"track_normChi2_miniaod.pdf")
hist_numPixelHits_AOD.Draw()
hist_numPixelHits.Draw("same")
c.SaveAs(odir+"track_nPixelHits_miniaod.pdf")
hist_numValidHits_AOD.Draw()
hist_numValidHits.Draw("same")
c.SaveAs(odir+"track_nValHits_miniaod.pdf")
hist_numTkLayers_AOD.Draw()
hist_numTkLayers.Draw("same")
c.SaveAs(odir+"track_nTkLayers_miniaod.pdf")
