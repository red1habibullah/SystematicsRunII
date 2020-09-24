#!/usr/bin/python
import ROOT
import tdrStyle
import math
import array

tdrStyle.setTDRStyle()
ROOT.gStyle.SetErrorX(0.5)

tauVSeleNumerator = ["deepTauVSele_null_deepTauVSmu_vloose_deepTauVSjet_medium", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_medium", "deepTauVSele_vvloose_deepTauVSmu_vloose_deepTauVSjet_medium", "deepTauVSele_vloose_deepTauVSmu_vloose_deepTauVSjet_medium", "deepTauVSele_loose_deepTauVSmu_vloose_deepTauVSjet_medium", "deepTauVSele_medium_deepTauVSmu_vloose_deepTauVSjet_medium", "deepTauVSele_tight_deepTauVSmu_vloose_deepTauVSjet_medium", "deepTauVSele_vtight_deepTauVSmu_vloose_deepTauVSjet_medium", "deepTauVSele_vvtight_deepTauVSmu_vloose_deepTauVSjet_medium"]
tauDiscVSele = ["noDeepVSele", "vvvlooseDeepVSele", "vvlooseDeepVSele", "vlooseDeepVSele", "looseDeepVSele", "mediumDeepVSele", "tightDeepVSele", "vtightDeepVSele", "vvtightDeepVSele"]

tauVSmuNumerator = ["deepTauVSele_vvvloose_deepTauVSmu_null_deepTauVSjet_medium", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_medium", "deepTauVSele_vvvloose_deepTauVSmu_loose_deepTauVSjet_medium", "deepTauVSele_vvvloose_deepTauVSmu_medium_deepTauVSjet_medium", "deepTauVSele_vvvloose_deepTauVSmu_tight_deepTauVSjet_medium"]
tauDiscVSmu = ["noDeepVSmu", "vlooseDeepVSmu", "looseDeepVSmu", "mediumDeepVSmu", "tightDeepVSmu"]

tauVSjetNumerator = ["deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_vvloose", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_vloose", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_loose", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_medium", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_tight", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_vtight", "deepTauVSele_vvvloose_deepTauVSmu_vloose_deepTauVSjet_vvtight"]
tauDiscVSjet = ["vvlooseDeepVSjet", "vlooseDeepVSjet", "looseDeepVSjet", "mediumDeepVSjet", "tightDeepVSjet", "vtightDeepVSjet", "vvtightDeepVSjet"]

fileDir = ["DeepTauVSele/", "DeepTauVSmu/", "DeepTauVSjet/"]
tauDiscContainer = [tauVSeleNumerator, tauVSmuNumerator, tauVSjetNumerator]
tauClusterLabel = [tauDiscVSele, tauDiscVSmu, tauDiscVSjet]

histList = ["deltaRTauTau", "Tau2Pt"]
histLabel = ["#DeltaR(#mu_{3}#tau_{h})", "p_{T}(#tau_{h})[GeV]"]
binning = array.array('d', [8, 20, 30, 50, 100, 200])

amasses = ["5", "10", "15", "20"]
masresl = [[4.5, 5.5], [9, 11], [13.5, 16.5], [18, 22]]

Colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kMagenta, ROOT.kRed, ROOT.kOrange, ROOT.kGreen+1, ROOT.kGreen-8, ROOT.kCyan-7, ROOT.kOrange+3]

label1 = ROOT.TLatex(0.21,0.87, "CMS")
label1.SetNDC()
label1.SetTextSize(0.03)

label2 = ROOT.TLatex(0.19,0.96, "#sqrt{s} = 13 TeV, Lumi = 41.529 fb^{-1} (2017)")
label2.SetNDC()
label2.SetTextFont(42)
label2.SetTextSize(0.04)

label3 = ROOT.TLatex(0.21,0.82, "Preliminary")
label3.SetNDC()
label3.SetTextFont(52)
label3.SetTextSize(0.03)

inputFakeFile = ROOT.TFile("fakeTauEff_TauMuTauHad.root")

for k,kmass in enumerate(amasses):

    outputDataFile = ROOT.TFile("dataDriven_diMuMass_" + kmass + ".root", "RECREATE")
    
    for j,jdir in enumerate(fileDir):

        for ihist,histKey in enumerate(histList):

            # ===========  prepare the canvas for comparison  ===============
            canvas = ROOT.TCanvas("comparison","data",900,1200)
            canvas.cd()
            pad1 = ROOT.TPad("plot1","plot1",0.05,0.33,0.95,0.97)
            pad2 = ROOT.TPad("plot2","plot2",0.05,0.02,0.95,0.35)
            pad1.SetTopMargin(0.05)
            pad1.SetLeftMargin(0.15)
            pad1.SetBottomMargin(0)
            pad2.SetTopMargin(0.05)
            pad2.SetLeftMargin(0.15)
            pad2.SetBottomMargin(0.3)
            pad2.SetGridy()
            pad2.SetTicks()

            pad1.SetFillColor(0)
            pad1.SetFillStyle(4000)
            pad1.SetFrameFillStyle(0)
            pad2.SetFillColor(0)
            pad2.SetFillStyle(4000)
            pad2.SetFrameFillStyle(0)
            pad1.Draw()
            pad2.Draw()
            # ==============================================================

            legend = ROOT.TLegend(0.68,0.62,0.95,0.95)
            legend.SetFillColor(0)
            legend.SetTextSize(0.03)


            for i,tauDisc in enumerate(tauClusterLabel[j]):
                globals()["fin" + tauDisc] = ROOT.TFile(tauDiscContainer[j][i] + ".root")
                globals()["treein" + tauDisc] = globals()["fin" + tauDisc].Get("TreeMuMuTauTau")
                histFakeEff = inputFakeFile.Get(tauDisc)

                globals()["hist" + tauDisc] = ROOT.TH1D()

                if "deltaR" in histKey:
                    globals()["hist" + tauDisc] = ROOT.TH1D(tauDisc, tauDisc, 25, 0, 1)

                if "Pt" in histKey:
                    globals()["hist" + tauDisc] = ROOT.TH1D(tauDisc, tauDisc, 5, binning)

                for event in globals()["treein" + tauDisc]:

                    if (event.invMassMuMu < masresl[k][0] or event.invMassMuMu > masresl[k][1]):
                        continue

                    nbins = histFakeEff.GetNbinsX()
                    for ibin in xrange(nbins):
                        binlowEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1)
                        binhighEdge = histFakeEff.GetXaxis().GetBinLowEdge(ibin+1) + histFakeEff.GetXaxis().GetBinWidth(ibin+1)
                        if (event.Tau2Pt >= binlowEdge and event.Tau2Pt < binhighEdge):
                            fakeEff = histFakeEff.GetBinContent(ibin+1)/(1.0-histFakeEff.GetBinContent(ibin+1))
                            if fakeEff >= 0:
                                if "deltaR" in histKey:
                                    globals()["hist" + tauDisc].Fill(event.deltaRTauTau, fakeEff)

                                if "Pt" in histKey:
                                    globals()["hist" + tauDisc].Fill(event.Tau2Pt, fakeEff)

                            else:
                                if "deltaR" in histKey:
                                    globals()["hist" + tauDisc].Fill(event.deltaRTauTau)

                                if "Pt" in histKey:
                                    globals()["hist" + tauDisc].Fill(event.Tau2Pt)

                globals()["hist" + tauDisc].GetXaxis().SetTitle(histLabel[ihist])
                globals()["hist" + tauDisc].GetYaxis().SetTitle("# Events")

                if "deltaR" in histKey:
                    outputDataFile.cd()
                    globals()["hist" + tauDisc].Write()

                globals()["hist" + tauDisc].SetStats(0)
                globals()["hist" + tauDisc].Sumw2()
                globals()["hist" + tauDisc].SetFillColor(Colors[i])
                globals()["hist" + tauDisc].SetLineColor(Colors[i])
                globals()["hist" + tauDisc].SetMarkerStyle(20)
                globals()["hist" + tauDisc].SetLineWidth(3)
                globals()["hist" + tauDisc].SetMarkerColor(Colors[i])
                globals()["hist" + tauDisc].SetMarkerSize(2)

                nBins = globals()["hist" + tauDisc].GetNbinsX()
                for ibin in xrange(nBins):
                    value = globals()["hist" + tauDisc].GetBinContent(ibin+1)
                    if value == 0:
                        globals()["hist" + tauDisc].SetBinContent(ibin+1, 1e-10)
                        globals()["hist" + tauDisc].SetBinError(ibin+1, 1e-10)

                legend.AddEntry(globals()["hist" + tauDisc], tauDisc, "elp")

                pad1.cd()
                if i == 0:

                    globals()["basehist"] = globals()["hist" + tauDisc].Clone()

                    if histKey.find("deltaR")!=-1:
                       pad1.SetLogy()
                       globals()["hist" + tauDisc].GetYaxis().SetRangeUser(1, globals()["hist" + tauDisc].GetMaximum()*100.0)

                    if histKey.find("Pt")!=-1:
                       pad1.SetLogy()
                       globals()["hist" + tauDisc].GetYaxis().SetRangeUser(1, globals()["hist" + tauDisc].GetMaximum()*10.0)

                    globals()["hist" + tauDisc].GetXaxis().SetTitleOffset(1.3)
                    globals()["hist" + tauDisc].GetYaxis().SetTitleOffset(1.4)
                    globals()["hist" + tauDisc].GetYaxis().SetTitleSize(0.06)
                    globals()["hist" + tauDisc].GetYaxis().SetLabelSize(0.06)
                    globals()["hist" + tauDisc].Draw("elp")

                else:
                    globals()["hist" + tauDisc].Draw("elp same")


                pad2.cd()
                globals()["ratio" + tauDisc] = globals()["hist" + tauDisc].Clone()

                if i == 0:
                    nBins = globals()["ratio" + tauDisc].GetNbinsX()
                    for ibin in xrange(nBins):
                        value = globals()["ratio" + tauDisc].GetBinContent(ibin+1)
                        if value <= 1e-10:
                            continue
                        else:
                            error = globals()["ratio" + tauDisc].GetBinError(ibin+1)/value
                            globals()["ratio" + tauDisc].SetBinContent(ibin+1, 1.0)
                            globals()["ratio" + tauDisc].SetBinError(ibin+1, error)

                    globals()["ratio" + tauDisc].GetYaxis().SetRangeUser(0.01, 0.99);
                    globals()["ratio" + tauDisc].GetYaxis().SetNdivisions(5,2,0);
                    globals()["ratio" + tauDisc].GetYaxis().SetTitle("Efficiency");
                    globals()["ratio" + tauDisc].GetYaxis().SetTitleSize(0.1);
                    globals()["ratio" + tauDisc].GetYaxis().SetTitleOffset(0.7);
                    globals()["ratio" + tauDisc].GetYaxis().SetLabelSize(0.11);
                    globals()["ratio" + tauDisc].GetXaxis().SetTitleSize(0.11);
                    globals()["ratio" + tauDisc].GetXaxis().SetLabelSize(0.11);
                    globals()["ratio" + tauDisc].Draw("elp")

                else:
                    globals()["ratio" + tauDisc].Divide(globals()["basehist"])
                    globals()["ratio" + tauDisc].Draw("same")

            pad1.cd()
            label1.Draw("same")
            label2.Draw("same")
            label3.Draw("same")
            ROOT.gPad.RedrawAxis()
            legend.Draw("same")

            pad2.cd()
            ROOT.gPad.RedrawAxis()
            canvas.SaveAs("plots/" + jdir + histKey + "_diMuMass_" + kmass + ".pdf")

    outputDataFile.Close()
