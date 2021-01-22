#!/usr/bin/python
import ROOT
import tdrStyle
import math
import array

tdrStyle.setTDRStyle()
ROOT.gStyle.SetErrorX(0.5)
ROOT.gROOT.SetBatch()


#baseDir='/eos/uscms/store/user/zfwd666/2017/fakeTauValidation/TauETauHad/NobVeto/'

#baseDirMVA='/eos/uscms/store/user/zfwd666/2017/fakeTauValidation/MVATauID/TauMuTauHad/NobVeto/'

#baseDirMVA='/eos/uscms/store/user/zfwd666/2017/fakeTauValidation/MVATauID/TauMuTauHad/'
baseDirMVA='/eos/uscms/store/user/zfwd666/2017/fakeTauValidation/MVATauID/TauETauHad/'
#baseDir='/eos/uscms/store/user/zfwd666/2017/fakeTauValidation/TauMuTauHad/'
#baseDir='/eos/uscms/store/user/zfwd666/2017/fakeTauValidation/TauETauHad/'
#fakeTauEff_TauETauHad_DeepTauID_WithoutAdjacentEle.root


#fileDir1MVA = ["InvertedMu2Iso_DM0/", "InvertedMu2Iso_DM1/", "InvertedMu2Iso_DM10/"]
#fileDir2MVA = ["InvertedMu2Iso_InvertedTauIso_DM0/", "InvertedMu2Iso_InvertedTauIso_DM1/", "InvertedMu2Iso_InvertedTauIso_DM10/"]

fileDir1MVA = ["InvertedMu2Iso_DM0/", "InvertedMu2Iso_DM1/"] #,"InvertedMu2Iso_DM10/"]
fileDir2MVA = ["InvertedMu2Iso_InvertedTauIso_DM0/", "InvertedMu2Iso_InvertedTauIso_DM1/" ] #,"InvertedMu2Iso_InvertedTauIso_DM10/"]

#fakeTauEff_TauMuTauHad_NoAdjMu_MVA.root

#fakeEffFile = ROOT.TFile("../data/fakeTauEff_TauMuTauHad_AdjMu_MVA.root")
fakeEffFile=ROOT.TFile("../data/fakeTauEff_TauETauHad_MVATauID_WithAdjacentEle.root")

label = ["1 prong", "1 prong + #pi^{0}", "2 prongs", "2 prongs + #pi^{0}", "3 prongs", "3 prongs + #pi^{0}"]
fakeEffHistMVA=["decayMode0", "decayMode1"] #,"decayMode10"]

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

#Colors = [1, 2, 4, 6, 7, 8, 9]
#binning = array.array('d', [8, 20, 30, 50, 100, 200])

# ===========  prepare the canvas for comparison  ===============
canvas = ROOT.TCanvas("comparison","data",900,1200)
canvas.cd()
# pad1 = ROOT.TPad("plot1","plot1",0.05,0.05,0.97,0.98)
# pad1.SetTopMargin(0.05)
# pad1.SetLeftMargin(0.10)
# pad1.SetBottomMargin(0.05)
# pad1.SetFillColor(0)
# pad1.SetFillStyle(4000)
# pad1.SetFrameFillStyle(0)




# pad1.Draw()

pad1 = ROOT.TPad("plot1","plot1",0.05,0.33,0.95,0.97)
pad2 = ROOT.TPad("plot2","plot2",0.05,0.02,0.95,0.33)
pad1.SetTopMargin(0.05)
pad1.SetLeftMargin(0.15)
pad1.SetBottomMargin(0)
pad2.SetTopMargin(0.05)
pad2.SetLeftMargin(0.15)
pad2.SetBottomMargin(0.31)
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

            
            
            



    
legend = ROOT.TLegend(0.60,0.78,0.95,0.95);
legend.SetFillColor(0);
legend.SetTextSize(0.02);
# ==============================================================
globals()['Observed']=ROOT.TH1D("Observed","Observed",5,8.0,200.0)
globals()['Datadriven']=ROOT.TH1D("Datadriven","Datadriven",5,8.0,200.0)

    
for i,fileKey in enumerate(fileDir1MVA):
    print fileKey
    globals()["dataFile1" + fileKey] = ROOT.TFile(baseDirMVA+fileDir1MVA[i] + "data.root")
    globals()["dataFile2" + fileKey] = ROOT.TFile(baseDirMVA+fileDir2MVA[i] + "data.root")

    globals()["dataHist1" + fileKey] = globals()["dataFile1" + fileKey].Get(histKey)
    globals()["dataHist1" + fileKey].Sumw2()
    globals()["dataHist1" + fileKey].SetStats(0)

    globals()["dataHist2" + fileKey] = globals()["dataFile2" + fileKey].Get(histKey)
    globals()["dataHist2" + fileKey].Sumw2()
    globals()["dataHist2" + fileKey].SetStats(0)


    globals()["fakeEffHist" + fileKey] = fakeEffFile.Get(fakeEffHistMVA[i])

    nBins = globals()["dataHist1" + fileKey].GetNbinsX()
    
    
    for ibin in xrange(nBins):
                
        binContentD = globals()["dataHist2" + fileKey].GetBinContent(ibin+1)
        fakeEffContent = globals()["fakeEffHist" + fileKey].GetBinContent(ibin+1)
        if fakeEffContent==1:
            continue
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
        
        
        
        
    globals()['Observed'].Add(globals()["dataHist1" + fileKey])
    globals()['Datadriven'].Add(globals()["dataHist2" + fileKey])


    globals()['Observed'].GetXaxis().SetTitle("#tau_{h} Pt(GeV)")
    globals()['Observed'].GetYaxis().SetTitle("Events")

      
    #globals()['Datadriven'].SetBinContent(int(fakeEffHistMVA[i].split('e')[-1])+1,Integral_D)
    
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
    #globals()["Datadriven"].SetFillColor(20)
    globals()["Datadriven"].SetMarkerColor(2)
    globals()["Datadriven"].SetMarkerSize(1)
    globals()["Datadriven"].SetLineWidth(3)
    

    pad2.cd()
    globals()["ratiohist"]=globals()['Observed'].Clone()
    globals()["ratiohist"].Divide(globals()["Datadriven"])
    globals()["ratiohist"].GetYaxis().SetTitleSize(0.05)
    globals()["ratiohist"].GetYaxis().SetNdivisions(510)
    globals()['ratiohist'].GetYaxis().SetTitle("Observed/Datadriven")
    globals()["ratiohist"].GetYaxis().SetTitleOffset(0.9)
    globals()["ratiohist"].GetXaxis().SetTitleOffset(0.9)
    globals()["ratiohist"].GetYaxis().SetLabelSize(0.05)
    globals()["ratiohist"].GetXaxis().SetTitleSize(0.05)
    globals()["ratiohist"].GetXaxis().SetLabelSize(0.05)
    globals()["ratiohist"].Fit("pol1")
    globals()["ratiohist"].Draw("same")

pad1.cd()
globals()["Observed" ].GetYaxis().SetRangeUser(0, 300)  

legend.AddEntry(globals()["Observed"], "Observed", "elp")
legend.AddEntry(globals()["Datadriven"], "Datadriven", "l")

globals()["Datadriven"].Draw("hist e")
globals()["Observed"].Draw("elp same") 

label1.Draw("same")
label2.Draw("same")
label3.Draw("same")
legend.Draw("same")

ROOT.gPad.Update()
ROOT.gPad.RedrawAxis()

pad2.cd()
ROOT.gPad.RedrawAxis()

canvas.SaveAs("../data/plots_sidebandValidation/" + histKey + "teth_fakerateUncertainty_combine_New_AdjEle_MVA_AllDM_p1" + ".png")  
    
