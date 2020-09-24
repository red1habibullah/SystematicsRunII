#!/usr/bin/python
import ROOT
import tdrStyle
import math
import array

tdrStyle.setTDRStyle()
ROOT.gStyle.SetErrorX(0.5)
ROOT.gROOT.SetBatch()

fileDir1 = ["../data/InvertedMu2Iso_DM0/", "../data/InvertedMu2Iso_DM1/", "../data/InvertedMu2Iso_DM5/", "../data/InvertedMu2Iso_DM6/", "../data/InvertedMu2Iso_DM10/", "../data/InvertedMu2Iso_DM11/"]
fileDir2 = ["../data/InvertedMu2Iso_InvertedTauIso_DM0/", "../data/InvertedMu2Iso_InvertedTauIso_DM1/", "../data/InvertedMu2Iso_InvertedTauIso_DM5/", "../data/InvertedMu2Iso_InvertedTauIso_DM6/", "../data/InvertedMu2Iso_InvertedTauIso_DM10/", "../data/InvertedMu2Iso_InvertedTauIso_DM11/",]

fakeEffFile = ROOT.TFile("../data/fakeTauEff_TauMuTauHad.root")

label = ["1 prong", "1 prong + #pi^{0}", "2 prongs", "2 prongs + #pi^{0}", "3 prongs", "3 prongs + #pi^{0}"]
fakeEffHist = ["decayMode0", "decayMode1", "decayMode5", "decayMode6", "decayMode10", "decayMode11"]
histKey = "tauPt"

label1 = ROOT.TLatex(0.19,0.87, "CMS")
label2 = ROOT.TLatex(0.35,0.96, "#sqrt{s} = 13 TeV, 41.529 fb^{-1} (2017)")
label3 = ROOT.TLatex(0.19,0.82, "Preliminary")
label1.SetNDC()
label1.SetTextSize(0.03)
label2.SetNDC()
label2.SetTextFont(42)
label2.SetTextSize(0.04)
label3.SetNDC()
label3.SetTextFont(52)
label3.SetTextSize(0.03)

Colors = [1, 2, 4, 6, 7, 8, 9]
binning = array.array('d', [8, 20, 30, 50, 100, 200])



for i,fileKey in enumerate(fileDir1):
    outputDataFile = ROOT.TFile("FakeRate_Uncertainty" + fakeEffHist[i] + ".root", "RECREATE")
    # ===========  prepare the canvas for comparison  ===============
    canvas = ROOT.TCanvas("comparison","data",900,1200)
    canvas.cd()
    pad1 = ROOT.TPad("plot1","plot1",0.05,0.05,0.97,0.98)
    #pad2 = ROOT.TPad("plot2","plot2",0.05,0.02,0.95,0.35)
    pad1.SetTopMargin(0.05)
    pad1.SetLeftMargin(0.10)
    pad1.SetBottomMargin(0.05)
    #pad2.SetTopMargin(0.05)
    #pad2.SetLeftMargin(0.15)
    #pad2.SetBottomMargin(0.3)
    #pad2.SetGridy()
    #pad2.SetTicks()

    pad1.SetFillColor(0)
    pad1.SetFillStyle(4000)
    pad1.SetFrameFillStyle(0)
    #pad2.SetFillColor(0)
    #pad2.SetFillStyle(4000)
    #pad2.SetFrameFillStyle(0)
    pad1.Draw()
    #pad2.Draw()
    # ==============================================================

    legend = ROOT.TLegend(0.60,0.78,0.95,0.95);
    legend.SetFillColor(0);
    legend.SetTextSize(0.02);

    globals()["dataFile1" + fileKey] = ROOT.TFile(fileDir1[i] + "data.root")
    globals()["dataFile2" + fileKey] = ROOT.TFile(fileDir2[i] + "data.root")

    globals()["dataHist1" + fileKey] = globals()["dataFile1" + fileKey].Get(histKey)
    globals()["dataHist1" + fileKey].Sumw2()
    globals()["dataHist1" + fileKey].SetStats(0)

    globals()["dataHist2" + fileKey] = globals()["dataFile2" + fileKey].Get(histKey)
    globals()["dataHist2" + fileKey].Sumw2()
    globals()["dataHist2" + fileKey].SetStats(0)


    globals()["fakeEffHist" + fileKey] = fakeEffFile.Get(fakeEffHist[i])

    nBins = globals()["dataHist1" + fileKey].GetNbinsX()
    globals()["fakeUncHist" + fileKey]=ROOT.TH1D("fakerate Uncertainty","fake Uncertainty",5,binning)
    for ibin in xrange(nBins):
                
        binContentC=globals()["dataHist1" + fileKey].GetBinContent(ibin+1)
        binContentD = globals()["dataHist2" + fileKey].GetBinContent(ibin+1)
        fakeEffContent = globals()["fakeEffHist" + fileKey].GetBinContent(ibin+1)
        if binContentC==0:
            continue
        
        product = (abs(binContentC - (binContentD * (fakeEffContent /(1 - fakeEffContent)))) / (binContentC))*100

        try:
            errorD = globals()["dataHist2" + fileKey].GetBinError(ibin+1)/binContentD
        except:
            errorD = 0

        try:
            fakeEffError = globals()["fakeEffHist" + fileKey].GetBinError(ibin+1)/fakeEffContent
        except:
            fakeEffError = 0
        
        try:
            errorC = globals()["dataHist1" + fileKey].GetBinError(ibin+1)/binContentC
        except:
            errorC = 0


        sumError = math.sqrt(pow(errorD, 2) + pow(fakeEffError, 2) + pow(errorC, 2))

        #globals()["dataHist2" + fileKey].SetBinContent(ibin+1, product)
        #globals()["dataHist2" + fileKey].SetBinError(ibin+1, sumError*product)
        globals()["fakeUncHist" + fileKey].SetBinContent(ibin+1, product)
        globals()["fakeUncHist" + fileKey].SetBinError(ibin+1, sumError*product)
        
        # value2 = globals()["dataHist2" + fileKey].GetBinContent(ibin+1)
        # if value2 <= 0:
        #    globals()["dataHist2" + fileKey].SetBinContent(ibin+1, 0.000001)
        #    globals()["dataHist2" + fileKey].SetBinError(ibin+1, 0.000001)

    # globals()["dataHist1" + fileKey].SetLineColor(1)
    # globals()["dataHist1" + fileKey].SetLineWidth(3)
    # globals()["dataHist1" + fileKey].SetMarkerStyle(20)
    # globals()["dataHist1" + fileKey].SetMarkerSize(2)
    # globals()["dataHist1" + fileKey].SetMarkerColor(1)

       
    
    # globals()["dataHist2" + fileKey].SetLineColor(2)
    # globals()["dataHist2" + fileKey].SetLineWidth(3)
    # globals()["dataHist2" + fileKey].SetMarkerStyle(20)
    # globals()["dataHist2" + fileKey].SetMarkerSize(2)
    # globals()["dataHist2" + fileKey].SetMarkerColor(2)

    #legend.AddEntry(globals()["dataHist1" + fileKey], "Observed", "elp")
    #legend.AddEntry(globals()["dataHist2" + fileKey], "DataDriven", "elp")
    legend.AddEntry(globals()["fakeUncHist" + fileKey], "fakeRate Uncertainty", "elp")

    pad1.cd()
    #pad1.SetLogy()
    globals()["fakeUncHist" + fileKey].SetLineColor(1)
    globals()["fakeUncHist" + fileKey].SetLineWidth(2)
    globals()["fakeUncHist" + fileKey].SetMarkerStyle(20)
    globals()["fakeUncHist" + fileKey].SetMarkerSize(1)
    globals()["fakeUncHist" + fileKey].SetMarkerColor(2)
    globals()["fakeUncHist" + fileKey].Draw("elp") 
    globals()["fakeUncHist" + fileKey].GetYaxis().SetTitle("Percentage Uncertainty [%]")
    globals()["fakeUncHist" + fileKey].GetXaxis().SetTitle("p_{T}(#tau) [GeV]")
    globals()["fakeUncHist" + fileKey].GetXaxis().SetTitleOffset(0.8)
    globals()["fakeUncHist" + fileKey].GetYaxis().SetTitleOffset(1.0)
    globals()["fakeUncHist" + fileKey].GetYaxis().SetTitleSize(0.03)
    globals()["fakeUncHist" + fileKey].GetXaxis().SetTitleSize(0.03)
    globals()["fakeUncHist" + fileKey].GetXaxis().SetLabelSize(0.02)
    globals()["fakeUncHist" + fileKey].GetYaxis().SetLabelSize(0.02)
     
    
    # globals()["dataHist2" + fileKey].GetXaxis().SetTitleOffset(0.8)
    # globals()["dataHist2" + fileKey].GetYaxis().SetTitleOffset(0.8)
    # globals()["dataHist2" + fileKey].GetYaxis().SetTitleSize(0.03)
    # globals()["dataHist2" + fileKey].GetYaxis().SetLabelSize(0.02)
    # globals()["dataHist2" + fileKey].GetYaxis().SetRangeUser(0.1, globals()["dataHist2" + fileKey].GetMaximum()*10)
    # globals()["dataHist2" + fileKey].Draw("elp")
    # globals()["dataHist1" + fileKey].Draw("elp same")
    
    
    #pad2.cd()

    # for ibin in xrange(nBins):
    #     value = globals()["dataHist2" + fileKey].GetBinContent(ibin+1)
    #     if value <= 0:
    #        globals()["dataHist2" + fileKey].SetBinContent(ibin+1, 0.000001)
    #        globals()["dataHist2" + fileKey].SetBinError(ibin+1, 0.000001)

    # globals()["ratioHist" + fileKey] = globals()["dataHist1" + fileKey].Clone()
    # globals()["ratioHist" + fileKey].Divide(globals()["dataHist2" + fileKey])

    # globals()["ratioHist" + fileKey].GetYaxis().SetRangeUser(0, 2);
    # #globals()["ratioHist" + fileKey].GetYaxis().SetRangeUser(0, 1);
    # globals()["ratioHist" + fileKey].GetYaxis().SetNdivisions(5,2,0);
    # globals()["ratioHist" + fileKey].GetYaxis().SetTitle("Obs/Exp");
    # globals()["ratioHist" + fileKey].GetYaxis().SetTitleSize(0.1);
    # globals()["ratioHist" + fileKey].GetYaxis().SetTitleOffset(0.7);
    # globals()["ratioHist" + fileKey].GetYaxis().SetLabelSize(0.11);
    # globals()["ratioHist" + fileKey].GetXaxis().SetTitleSize(0.11);
    # globals()["ratioHist" + fileKey].GetXaxis().SetLabelSize(0.11);
    # globals()["ratioHist" + fileKey].Draw("elp")


    #pad1.cd()
    label1.Draw("same")
    label2.Draw("same")
    label3.Draw("same")
    #ROOT.gPad.RedrawAxis()
    legend.Draw("same")
    ROOT.gPad.Update()
    ROOT.gPad.RedrawAxis()

    #pad2.cd()
    #ROOT.gPad.RedrawAxis()
    outputDataFile.cd()
    globals()["fakeUncHist" + fileKey].Write()
    #globals()["dataHist1" + fileKey].Write()
   #globals()["dataHist2" + fileKey].Write()
    
    #canvas.SaveAs("../data/plots_sidebandValidation/" + histKey + "_" + fakeEffHist[i] + ".pdf")
    #canvas.SaveAs("../data/plots_sidebandValidation/" + histKey + "_" + fakeEffHist[i] + ".png")
    canvas.SaveAs("../data/plots_sidebandValidation/" + histKey + "_fakerateUncertainty_" + fakeEffHist[i] + ".png")  
    outputDataFile.Close()
