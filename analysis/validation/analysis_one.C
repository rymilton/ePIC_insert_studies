{
    // Define this to wherever your output data is
    TString output_data_dir = "../../output/";

    gStyle->SetOptStat(0);
    gStyle->SetFrameLineWidth(2);
    gStyle->SetLabelSize(0.035,"X");
    gStyle->SetLabelSize(0.035,"Y");
    gStyle->SetLabelOffset(0.01,"X");
    gStyle->SetLabelOffset(0.01,"Y");
    gStyle->SetTitleXSize(0.035);
    gStyle->SetTitleXOffset(1.1);
    gStyle->SetTitleYSize(0.035);
    gStyle->SetTitleYOffset(1.1);

    //Run 1
    TFile *f1 = new TFile(output_data_dir + "output.gen_pi-_1GeV_theta_2.83deg.edm4hep.root");
    TTree *t1 = (TTree*) f1->Get("events");

    TH1 *h1 = new TH1D("h1","#pi^{-} at 1 GeV, #eta* = 3.7",50,-0.25,5);
    h1->GetXaxis()->SetTitle("Scaled total energy deposited in HCal_{Ins.} [GeV]");h1->GetXaxis()->CenterTitle();
    h1->SetLineColor(kBlue);h1->SetLineWidth(2);

    TCanvas *c1 = new TCanvas("c1");
    t1->Draw("Sum$(HcalEndcapPInsertHits.energy)/0.01>>h1");

    TH2 *h1a = new TH2D("h1a","#pi^{-} at 1 GeV, #eta* = 3.7",50,-0.25,5,50,-0.25,5);
    h1a->GetXaxis()->SetTitle("Total energy deposited in ECal_{Ins.} [GeV]");h1a->GetXaxis()->CenterTitle();
    h1a->GetYaxis()->SetTitle("Scaled total energy deposited in HCal_{Ins.} [GeV]");h1a->GetYaxis()->CenterTitle();

    TCanvas *c1a = new TCanvas("c1a");
    t1->Draw("Sum$(HcalEndcapPInsertHits.energy)/0.01:Sum$(EcalEndcapPInsertHits.energy)>>h1a","","col");

    TH2 *h1b = new TH2D("h1b","#pi^{-} at 1 GeV, #eta* = 3.7",100,-0.1,0.1,100,-0.1,0.1);
    h1b->GetXaxis()->SetTitle("Generated P_{x} [GeV/c]");h1b->GetXaxis()->CenterTitle();
    h1b->GetYaxis()->SetTitle("Generated P_{y} [GeV/c]");h1b->GetYaxis()->CenterTitle();

    TCanvas *c1b = new TCanvas("c1b");
    t1->Draw("MCParticles.momentum.y:MCParticles.momentum.x>>h1b","MCParticles.generatorStatus==1","col");

    //Run 2
    TFile *f2 = new TFile(output_data_dir + "output.gen_pi-_1GeV_theta_3.12deg.edm4hep.root");
    TTree *t2 = (TTree*) f2->Get("events");

    TH1 *h2 = new TH1D("h2","#pi^{-} at 1 GeV, #eta* = 3.6",50,-0.25,5);
    h2->GetXaxis()->SetTitle("Scaled total energy deposited in HCal_{Ins.} [GeV]");h2->GetXaxis()->CenterTitle();
    h2->SetLineColor(kBlue);h2->SetLineWidth(2);

    TCanvas *c2 = new TCanvas("c2");
    t2->Draw("Sum$(HcalEndcapPInsertHits.energy)/0.01>>h2");

    TH2 *h2a = new TH2D("h2a","#pi^{-} at 1 GeV, #eta* = 3.6",50,-0.25,5,50,-0.25,5);
    h2a->GetXaxis()->SetTitle("Total energy deposited in ECal_{Ins.} [GeV]");h2a->GetXaxis()->CenterTitle();
    h2a->GetYaxis()->SetTitle("Scaled total energy deposited in HCal_{Ins.} [GeV]");h2a->GetYaxis()->CenterTitle();

    TCanvas *c2a = new TCanvas("c2a");
    t2->Draw("Sum$(HcalEndcapPInsertHits.energy)/0.01:Sum$(EcalEndcapPInsertHits.energy)>>h2a","","col");

    //Run 3
    TFile *f3 = new TFile(output_data_dir + "output.gen_pi-_20GeV_theta_2.83deg.edm4hep.root");
    TTree *t3 = (TTree*) f3->Get("events");

    TH1 *h3 = new TH1D("h3","#pi^{-} at 20 GeV, #eta* = 3.7",50,0,40);
    h3->GetXaxis()->SetTitle("Scaled total energy deposited in Hcal_{Ins.} [GeV]");h3->GetXaxis()->CenterTitle();
    h3->SetLineColor(kBlue);h3->SetLineWidth(2);

    TCanvas *c3 = new TCanvas("c3");
    t3->Draw("Sum$(HcalEndcapPInsertHits.energy)/0.01>>h3");

    TH2 *h3a = new TH2D("h3a","#pi^{-} at 20 GeV, #eta* = 3.7",50,0,40,50,0,40);
    h3a->GetXaxis()->SetTitle("Total energy deposited in ECal_{Ins.} [GeV]");h3a->GetXaxis()->CenterTitle();
    h3a->GetYaxis()->SetTitle("Scaled total energy deposited in HCal_{Ins.} [GeV]");h3a->GetYaxis()->CenterTitle();

    TCanvas *c3a = new TCanvas("c3a");
    t3->Draw("Sum$(HcalEndcapPInsertHits.energy)/0.01:Sum$(EcalEndcapPInsertHits.energy)>>h3a","","col");

    TH1 *h3b = new TH1D("h3b","#pi^{-} at 20 GeV, #eta* = 3.7",50,-0.01,0.1);
    h3b->GetXaxis()->SetTitle("Energy deposited per cell in Hcal_{Ins.} [GeV]");h3b->GetXaxis()->CenterTitle();
    h3b->SetLineColor(kBlue);h3b->SetLineWidth(2);

    TCanvas *c3b = new TCanvas("c3b");
    c3b->SetLogy();
    t3->Draw("HcalEndcapPInsertHits.energy>>h3b");

    //Run 4
    TFile *f4 = new TFile(output_data_dir + "output.gen_pi-_20GeV_theta_3.12deg.edm4hep.root");
    TTree *t4 = (TTree*) f4->Get("events");

    TH1 *h4 = new TH1D("h4","#pi^{-} at 20 GeV, #eta* = 3.6",50,0,40);
    h4->GetXaxis()->SetTitle("Scaled total energy deposited in Hcal_{Ins.} [GeV]");h4->GetXaxis()->CenterTitle();
    h4->SetLineColor(kBlue);h4->SetLineWidth(2);

    TCanvas *c4 = new TCanvas("c4");
    t4->Draw("Sum$(HcalEndcapPInsertHits.energy)/0.01>>h4");

    TH2 *h4a = new TH2D("h4a","#pi^{-} at 20 GeV, #eta* = 3.6",50,0,40,50,0,40);
    h4a->GetXaxis()->SetTitle("Total energy deposited in ECal_{Ins.} [GeV]");h4a->GetXaxis()->CenterTitle();
    h4a->GetYaxis()->SetTitle("Scaled total energy deposited in HCal_{Ins.} [GeV]");h4a->GetYaxis()->CenterTitle();

    TCanvas *c4a = new TCanvas("c4a");
    t4->Draw("Sum$(HcalEndcapPInsertHits.energy)/0.01:Sum$(EcalEndcapPInsertHits.energy)>>h4a","","col");

    //Run 5
    TFile *f5 = new TFile(output_data_dir + "output.gen_pi-_100GeV_theta_2.83deg.edm4hep.root");
    TTree *t5 = (TTree*) f5->Get("events");

    TH1 *h5 = new TH1D("h5","#pi^{-} at 100 GeV, #eta* = 3.7",50,0,150);
    h5->GetXaxis()->SetTitle("Scaled total energy deposited in Hcal_{Ins.} [GeV]");h5->GetXaxis()->CenterTitle();
    h5->SetLineColor(kBlue);h5->SetLineWidth(2);

    TCanvas *c5 = new TCanvas("c5");
    t5->Draw("Sum$(HcalEndcapPInsertHits.energy)/0.01>>h5");

    TH2 *h5a = new TH2D("h5a","#pi^{-} at 100 GeV, #eta* = 3.7",50,0,150,50,0,150);
    h5a->GetXaxis()->SetTitle("Total energy deposited in ECal_{Ins.} [GeV]");h5a->GetXaxis()->CenterTitle();
    h5a->GetYaxis()->SetTitle("Scaled total energy deposited in HCal_{Ins.} [GeV]");h5a->GetYaxis()->CenterTitle();

    TCanvas *c5a = new TCanvas("c5a");
    t5->Draw("Sum$(HcalEndcapPInsertHits.energy)/0.01:Sum$(EcalEndcapPInsertHits.energy)>>h5a","","col");

    //Print to file
    c1->Print("insert_energy.pdf[");
    c1->Print("insert_energy.pdf");
    c1a->Print("insert_energy.pdf");
    c1b->Print("insert_energy.pdf");
    c2->Print("insert_energy.pdf");
    c2a->Print("insert_energy.pdf");
    c3->Print("insert_energy.pdf");
    c3a->Print("insert_energy.pdf");
    c3b->Print("insert_energy.pdf]");
    c4->Print("insert_energy.pdf");
    c4a->Print("insert_energy.pdf");
    c5->Print("insert_energy.pdf");
    c5a->Print("insert_energy.pdf");
    c5a->Print("insert_energy.pdf]");

}
