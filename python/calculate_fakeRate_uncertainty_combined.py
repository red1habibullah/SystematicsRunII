#!/usr/bin/python
import ROOT
import tdrStyle
import math
import array

tdrStyle.setTDRStyle()
ROOT.gStyle.SetErrorX(0.5)
ROOT.gROOT.SetBatch()

fileDir1 = ["../data/TauMuTauHad/InvertedMu2Iso_DM0/", "../data/TauMuTauHad/InvertedMu2Iso_DM1/", "../data/TauMuTauHad/InvertedMu2Iso_DM5/", "../data/TauMuTauHad/InvertedMu2Iso_DM6/", "../data/TauMuTauHad/InvertedMu2Iso_DM10/", "../data/TauMuTauHad/InvertedMu2Iso_DM11/"]
fileDir2 = ["../data/TauMuTauHad/InvertedMu2Iso_InvertedTauIso_DM0/", "../data/TauMuTauHad/InvertedMu2Iso_InvertedTauIso_DM1/", "../data/TauMuTauHad/InvertedMu2Iso_InvertedTauIso_DM5/", "../data/TauMuTauHad/InvertedMu2Iso_InvertedTauIso_DM6/", "../data/TauMuTauHad/InvertedMu2Iso_InvertedTauIso_DM10/", "../data/TauMuTauHad/InvertedMu2Iso_InvertedTauIso_DM11/",]

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

# ===========  prepare the canvas for comparison  ===============
canvas = ROOT.TCanvas("comparison","data",900,1200)
canvas.cd()
pad1 = ROOT.TPad("plot1","plot1",0.05,0.05,0.97,0.98)
pad1.SetTopMargin(0.05)
pad1.SetLeftMargin(0.10)
pad1.SetBottomMargin(0.05)

pad1.SetFillColor(0)
pad1.SetFillStyle(4000)
pad1.SetFrameFillStyle(0)

pad1.Draw()
    
legend = ROOT.TLegend(0.60,0.78,0.95,0.95);
legend.SetFillColor(0);
legend.SetTextSize(0.02);
# ==============================================================
globals()['Observed']=ROOT.TH1D("Observed","Observed",12,0,12)
globals()['Datadriven']=ROOT.TH1D("Datadriven","Datadriven",12,0,12)

    
for i,fileKey in enumerate(fileDir1):
    
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
    globals()["DataC" + fileKey]=ROOT.TH1D("expected","expected",1,0,1)
    globals()["DatadrivenD" + fileKey]=ROOT.TH1D("Datadriven","Datadriven",1,0,1)
    
    
    for ibin in xrange(nBins):
                
        binContentD = globals()["dataHist2" + fileKey].GetBinContent(ibin+1)
        fakeEffContent = globals()["fakeEffHist" + fileKey].GetBinContent(ibin+1)
        product = (fakeEffContent/(1 - fakeEffContent))*binContentD

        try:
            errorD = globals()["dataHist2" + fileKey].GetBinError(ibin+1)/binContentD
        except:
            errorD = 0

        try:
            fakeEffError = globals()["fakeEffHist" + fileKey].GetBinError(ibin+1)/fakeEffContent
        except:
            fakeEffError = 0
            
       

        sumError = math.sqrt(pow(errorD, 2) + pow(fakeEffError, 2)) #+ pow(errorC, 2))
        
        globals()["dataHist2" + fileKey].SetBinContent(ibin+1, product)
        globals()["dataHist2" + fileKey].SetBinError(ibin+1, sumError*product)
        
        
    Integral_C= globals()["dataHist1" + fileKey].Integral()
    Integral_D=globals()["dataHist2" + fileKey].Integral()
    

    globals()["DataC" + fileKey].SetBinContent(1,Integral_C)
    error_C=globals()["DataC" + fileKey].GetBinError(1)
    globals()["DataC" + fileKey].SetBinError(1,error_C)

    globals()["DatadrivenD" + fileKey].SetBinContent(1,Integral_D)
    error_D=globals()["DatadrivenD" + fileKey].GetBinError(1)
    globals()["DatadrivenD" + fileKey].SetBinError(1,error_D)
    
   
    globals()['Observed'].SetBinContent(int(fakeEffHist[i].split('e')[-1])+1,Integral_C)
    globals()['Observed'].GetXaxis().SetNdivisions(12)
    globals()['Observed'].GetXaxis().SetTitle("#tau_{h} Decay Mode")
    globals()['Observed'].GetYaxis().SetTitle("Events")

      
    globals()['Datadriven'].SetBinContent(int(fakeEffHist[i].split('e')[-1])+1,Integral_D)
    
    globals()["Observed"].SetLineColor(1)
    globals()["Observed"].SetMarkerSize(2)
    globals()["Observed"].SetMarkerColor(1)
    globals()["Observed"].SetLineWidth(3)
    globals()["Observed"].GetXaxis().SetTitleOffset(0.8)
    globals()["Observed"].GetYaxis().SetTitleOffset(1.0)
    globals()["Observed"].GetYaxis().SetTitleSize(0.03)
    globals()["Observed"].GetXaxis().SetTitleSize(0.03)
    globals()["Observed"].GetXaxis().SetLabelSize(0.02)
    globals()["Observed"].GetYaxis().SetLabelSize(0.02)

    globals()["Datadriven"].SetLineColor(2)
    globals()["Datadriven"].SetMarkerColor(2)
    globals()["Datadriven"].SetMarkerSize(1)
    globals()["Datadriven"].SetLineWidth(3)
    
pad1.cd()
globals()["Observed" ].GetYaxis().SetRangeUser(0, 600)  

legend.AddEntry(globals()["Observed"], "Observed", "elp")
legend.AddEntry(globals()["Datadriven"], "Datadriven", "elp")

globals()["Observed"].Draw("elp") 
globals()["Datadriven"].Draw("elp same")

label1.Draw("same")
label2.Draw("same")
label3.Draw("same")
legend.Draw("same")

ROOT.gPad.Update()
ROOT.gPad.RedrawAxis()

canvas.SaveAs("../data/plots_sidebandValidation/" + histKey + "tmth_fakerateUncertainty_combine" + ".png")  
    
