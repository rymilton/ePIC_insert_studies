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
    TFile *f1 = new TFile(output_data_dir + "eicrecon_out.gen_pi-_1GeV_theta_2.83deg.root");
    TTree *t1 = (TTree*) f1->Get("events");

    TH1 *h1 = new TH1D("h1","#pi^{-} at 1 GeV, #eta* = 3.7",50,-0.25,5);
    h1->GetXaxis()->SetTitle("Total Rec. energy in HCal_{Ins.} [GeV]");h1->GetXaxis()->CenterTitle();
    h1->SetLineColor(kBlue);h1->SetLineWidth(2);

    TCanvas *c1 = new TCanvas("c1");
    t1->Draw("Sum$(HcalEndcapPInsertRecHits.energy)>>h1");

    TH1 *h1a = new TH1D("h1a","#pi^{-} at 1 GeV, #eta* = 3.7",1000,-100,35000);
    h1a->GetXaxis()->SetTitle("ADC amplitude for HCal_{Ins.}");h1a->GetXaxis()->CenterTitle();
    h1a->SetLineColor(kBlue);h1a->SetLineWidth(2);

    TCanvas *c1a = new TCanvas("c1a");
    gPad->SetLogy();
    t1->Draw("HcalEndcapPInsertRawHits.amplitude>>h1a");

    //Run 2
    TFile *f2 = new TFile(output_data_dir + "eicrecon_out.gen_pi-_1GeV_theta_3.12deg.root");
    TTree *t2 = (TTree*) f2->Get("events");

    TH1 *h2 = new TH1D("h2","#pi^{-} at 1 GeV, #eta* = 3.6",50,-0.25,5);
    h2->GetXaxis()->SetTitle("Total Rec. energy in HCal_{Ins.} [GeV]");h2->GetXaxis()->CenterTitle();
    h2->SetLineColor(kBlue);h2->SetLineWidth(2);

    TCanvas *c2 = new TCanvas("c2");
    t2->Draw("Sum$(HcalEndcapPInsertRecHits.energy)>>h2");

    TH1 *h2a = new TH1D("h2a","#pi^{-} at 1 GeV, #eta* = 3.6",1000,-100,35000);
    h2a->GetXaxis()->SetTitle("ADC amplitude for HCal_{Ins.}");h2a->GetXaxis()->CenterTitle();
    h2a->SetLineColor(kBlue);h2a->SetLineWidth(2);

    TCanvas *c2a = new TCanvas("c2a");
    gPad->SetLogy();
    t2->Draw("HcalEndcapPInsertRawHits.amplitude>>h2a");

    //Run 3
    TFile *f3 = new TFile(output_data_dir + "eicrecon_out.gen_pi-_20GeV_theta_2.83deg.root");
    TTree *t3 = (TTree*) f3->Get("events");

    TH1 *h3 = new TH1D("h3","#pi^{-} at 20 GeV, #eta* = 3.7",50,0,40);
    h3->GetXaxis()->SetTitle("Total Rec. energy in HCal_{Ins.} [GeV]");h3->GetXaxis()->CenterTitle();
    h3->SetLineColor(kBlue);h3->SetLineWidth(2);

    TCanvas *c3 = new TCanvas("c3");
    t3->Draw("Sum$(HcalEndcapPInsertRecHits.energy)>>h3");

    TH1 *h3a = new TH1D("h3a","#pi^{-} at 20 GeV, #eta* = 3.7",1000,-100,35000);
    h3a->GetXaxis()->SetTitle("ADC amplitude for HCal_{Ins.}");h3a->GetXaxis()->CenterTitle();
    h3a->SetLineColor(kBlue);h3a->SetLineWidth(2);

    TCanvas *c3a = new TCanvas("c3a");
    gPad->SetLogy();
    t3->Draw("HcalEndcapPInsertRawHits.amplitude>>h3a");

    TH2 *h3b = new TH2D("h3b","#pi^{-} at 20 GeV, #eta* = 3.7",500,-100,15000,500,-2,100);
    h3b->GetXaxis()->SetTitle("ADC amplitude for HCal_{Ins.}");h3b->GetXaxis()->CenterTitle();
    h3b->GetYaxis()->SetTitle("Rec. energy per cell in HCal_{Ins.} [MeV]");h3b->GetYaxis()->CenterTitle();

    TCanvas *c3b = new TCanvas("c3b");
    //We want to show the reconstructed energy in MeV before applying the sampling fraction correction
    //So, divide by 100 and multiply by 1000
    t3->Draw("HcalEndcapPInsertRecHits.energy*10.:HcalEndcapPInsertRawHits.amplitude>>h3b");

    //Run 4
    TFile *f4 = new TFile(output_data_dir + "eicrecon_out.gen_pi-_20GeV_theta_3.12deg.root");
    TTree *t4 = (TTree*) f4->Get("events");

    TH1 *h4 = new TH1D("h4","#pi^{-} at 20 GeV, #eta* = 3.6",50,0,40);
    h4->GetXaxis()->SetTitle("Total Rec. energy in HCal_{Ins.} [GeV]");h4->GetXaxis()->CenterTitle();
    h4->SetLineColor(kBlue);h4->SetLineWidth(2);

    TCanvas *c4 = new TCanvas("c4");
    t4->Draw("Sum$(HcalEndcapPInsertRecHits.energy)>>h4");

    TH1 *h4a = new TH1D("h4a","#pi^{-} at 20 GeV, #eta* = 3.6",1000,-100,35000);
    h4a->GetXaxis()->SetTitle("ADC amplitude for HCal_{Ins.}");h4a->GetXaxis()->CenterTitle();
    h4a->SetLineColor(kBlue);h4a->SetLineWidth(2);

    TCanvas *c4a = new TCanvas("c4a");
    gPad->SetLogy();
    t4->Draw("HcalEndcapPInsertRawHits.amplitude>>h4a");

    //Run 5
    TFile *f5 = new TFile(output_data_dir + "eicrecon_out.gen_pi-_100GeV_theta_2.83deg.root");
    TTree *t5 = (TTree*) f5->Get("events");

    TH1 *h5 = new TH1D("h5","#pi^{-} at 100 GeV, #eta* = 3.7",50,0,150);
    h5->GetXaxis()->SetTitle("Total Rec. energy in HCal_{Ins.} [GeV]");h5->GetXaxis()->CenterTitle();
    h5->SetLineColor(kBlue);h5->SetLineWidth(2);

    TCanvas *c5 = new TCanvas("c5");
    t5->Draw("Sum$(HcalEndcapPInsertRecHits.energy)>>h5");

    TH1 *h5a = new TH1D("h5a","#pi^{-} at 100 GeV, #eta* = 3.7",1000,-100,35000);
    h5a->GetXaxis()->SetTitle("ADC amplitude for HCal_{Ins.}");h5a->GetXaxis()->CenterTitle();
    h5a->SetLineColor(kBlue);h5a->SetLineWidth(2);

    TCanvas *c5a = new TCanvas("c5a");
    gPad->SetLogy();
    t5->Draw("HcalEndcapPInsertRawHits.amplitude>>h5a");

    //Print to file
    c1->Print("insert_energy_rec.pdf[");
    c1->Print("insert_energy_rec.pdf");
    c1a->Print("insert_energy_rec.pdf");
    c2->Print("insert_energy_rec.pdf");
    c2a->Print("insert_energy_rec.pdf");
    c3->Print("insert_energy_rec.pdf");
    c3a->Print("insert_energy_rec.pdf");
    c3b->Print("insert_energy_rec.pdf");
    c4->Print("insert_energy_rec.pdf");
    c4a->Print("insert_energy_rec.pdf");
    c5->Print("insert_energy_rec.pdf");
    c5a->Print("insert_energy_rec.pdf");
    c5a->Print("insert_energy_rec.pdf]");

}
