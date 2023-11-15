#!/usr/bin/env python
# coding: utf-8


import uproot
import awkward as ak
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches

import vector
vector.register_awkward() #Allows Awkward array records to be interpreted as vectors

#load ROOT file
datadir='/gpfs02/eic/wbzhang/epic/hcal_insert/output/'
# events = uproot.open(f'{datadir}/reco_djangoh_18_275.edm4hep.root:events')
events = uproot.open(f'{datadir}/abconv_djangoh.NC.10x100_evt_reco.root:events')

#To check branches
#events.keys()


# ### **Inclusive Kinematics -- Truth Level**
#Get True Inclusive Kinematics Branches
arrays = events.arrays(['InclusiveKinematicsTruth.x','InclusiveKinematicsTruth.Q2','InclusiveKinematicsTruth.y'])
print("")
print(arrays.type)
print("")

x = arrays['InclusiveKinematicsTruth.x']
Q2 = arrays['InclusiveKinematicsTruth.Q2']
y = arrays['InclusiveKinematicsTruth.y']

#Flatten for later cuts on sum
x_flat = ak.flatten(x)
Q2_flat = ak.flatten(Q2)
y_flat = ak.flatten(y)


# ### **Generated Particles**
#Get MCParticles Branches
arrays = events.arrays(filter_name="MCParticles/*")
print("")
print(arrays.type)
print("")

#Select only final-state generated particles, and exclude secondaries
cut_primary = arrays["MCParticles.generatorStatus"]==1

px = arrays["MCParticles.momentum.x"][cut_primary]
py = arrays["MCParticles.momentum.y"][cut_primary]
pz = arrays["MCParticles.momentum.z"][cut_primary]
mass = arrays["MCParticles.mass"][cut_primary]

particles = vector.zip({
    "px": px,
    "py": py,
    "pz": pz,
    "mass": mass,
})

#For testing
###
pt = np.sqrt(px**2+py**2)
mom = np.sqrt(px**2+py**2+pz**2)
energy = np.sqrt(mom**2+mass**2)
theta = np.arccos(pz/mom)
eta = -1.*np.log( np.tan(theta/2.) )

#Check conservation of energy -- should be ~ 18+275 = 293 GeV
e_sum = (ak.sum(energy,axis=-1))
print("Total energy of final-state particles:")
print(e_sum)
print("")

print("energy comparison:")
print(energy)
print(ak.count(energy,axis=-1))
print(particles.energy)
print(ak.count(particles.energy,axis=-1))
print("")
print("eta comparison:")
print(eta)
print(ak.count(eta,axis=-1))
print(particles.eta)
print(ak.count(particles.eta,axis=-1))
print("")
###

#Rotate particles so that angles are defined relative to proton beam direction
particles_star = particles.rotateY(25./1000.)
print(type(particles))
print(type(particles_star))
energy_star = particles_star.energy #should be same as unrotated
px_star = particles_star.px
py_star = particles_star.py #should be same as unrotated
pz_star = particles_star.pz
eta_star = particles_star.eta
empz_star = energy_star - pz_star

#For testing
###
print("energy comparison:")
print(energy)
print(ak.count(energy,axis=-1))
print(energy_star)
print(ak.count(energy_star,axis=-1))
print("")
print("eta comparison:")
print(eta)
print(ak.count(eta,axis=-1))
print(eta_star)
print(ak.count(eta_star,axis=-1))
print("")
###

#Sums for various eta* cuts
#eta* > 1.0
e1 = energy_star[(eta_star>1)] #should be same as using unrotated energy
e1_sum = ak.sum(e1,axis=-1)
e14 = energy_star[(eta_star>1) & (eta_star<4)] #should be same as using unrotated energy
e14_sum = ak.sum(e14,axis=-1)

px1_sum = ak.sum(px_star[(eta_star>1)],axis=-1)
py1_sum = ak.sum(py_star[(eta_star>1)],axis=-1)
pt1_sum = np.sqrt( px1_sum*px1_sum + py1_sum*py1_sum )

px14_sum = ak.sum(px_star[(eta_star>1) & (eta_star<4)],axis=-1)
py14_sum = ak.sum(py_star[(eta_star>1) & (eta_star<4)],axis=-1)
pt14_sum = np.sqrt( px14_sum*px14_sum + py14_sum*py14_sum )

empz1 = empz_star[(eta_star>1)]
print("Eta* > +1:")
print(empz1)
print(ak.count(empz1,axis=-1))

empz1_sum = ak.sum(empz1,axis=-1)
print(empz1_sum)
print("")

#eta* > 3.0
e3 = energy_star[(eta_star>3)] #should be same as using unrotated energy
e3_sum = (ak.sum(e3,axis=-1))
e34 = energy_star[(eta_star>3) & (eta_star<4)] #should be same as using unrotated energy
e34_sum = ak.sum(e34,axis=-1)

px34_sum = ak.sum(px_star[(eta_star>3) & (eta_star<4)],axis=-1)
py34_sum = ak.sum(py_star[(eta_star>3) & (eta_star<4)],axis=-1)
pt34_sum = np.sqrt( px34_sum*px34_sum + py34_sum*py34_sum )

empz3 = empz_star[(eta_star>3)]
print("Eta* > +3:")
print(empz3)
print(ak.count(empz3,axis=-1))

empz3_sum = ak.sum(empz3,axis=-1)
print(empz3_sum)
print("")

#High-x events: eta* > 1.0 & x > 0.3
empz1_highx = empz1_sum[x_flat>0.3]
pt1_highx = pt1_sum[x_flat>0.3]
y_highx = y_flat[x_flat>0.3]
Q2_highx = Q2_flat[x_flat>0.3]

#Energy fraction
print("Energy fraction:")
print(ak.count(e14_sum))
print(ak.count(e14_sum[e14_sum>0]))
print("")

x_frac = x_flat[e14_sum>0]
e_frac = e34_sum[e14_sum>0] / e14_sum[e14_sum>0]


# ### Calorimeter Reconstruction


#Get Calorimeter Branches
#HCal endcap -- Use merged hits: these integrate over all z cells with same x,y position; merged z position at front face
#HCal insert -- Use merged hits
#Ecal endcap -- Use reconstructed hits: only one energy value per x,y position; z position at front face
#Ecal insert -- Use reconstructed hits

hcal_arrays = events.arrays(['HcalEndcapPMergedHits.energy',
                             'HcalEndcapPMergedHits.position.x',
                             'HcalEndcapPMergedHits.position.y',
                             'HcalEndcapPMergedHits.position.z'])

hcal_insert_arrays = events.arrays(['HcalEndcapPInsertMergedHits.energy',
                                    'HcalEndcapPInsertMergedHits.position.x',
                                    'HcalEndcapPInsertMergedHits.position.y',
                                    'HcalEndcapPInsertMergedHits.position.z'])

ecal_arrays = events.arrays(['EcalEndcapPRecHits.energy',
                             'EcalEndcapPRecHits.position.x',
                             'EcalEndcapPRecHits.position.y',
                             'EcalEndcapPRecHits.position.z'])

ecal_insert_arrays = events.arrays(['EcalEndcapPInsertRecHits.energy',
                                    'EcalEndcapPInsertRecHits.position.x',
                                    'EcalEndcapPInsertRecHits.position.y',
                                    'EcalEndcapPInsertRecHits.position.z'])

print("")
print(hcal_arrays.type)
print(hcal_insert_arrays.type)
print(ecal_arrays.type)
print(ecal_insert_arrays.type)
print("")

#Combine in one set of Awkward arrays (for easier rotation and summing)
cal_energy = ak.concatenate((hcal_arrays['HcalEndcapPMergedHits.energy'],
                             hcal_insert_arrays['HcalEndcapPInsertMergedHits.energy'],
                             ecal_arrays['EcalEndcapPRecHits.energy'],
                             ecal_insert_arrays['EcalEndcapPInsertRecHits.energy']),
                            axis=-1)

cal_posx = ak.concatenate((hcal_arrays['HcalEndcapPMergedHits.position.x'],
                           hcal_insert_arrays['HcalEndcapPInsertMergedHits.position.x'],
                           ecal_arrays['EcalEndcapPRecHits.position.x'],
                           ecal_insert_arrays['EcalEndcapPInsertRecHits.position.x']),
                          axis=-1)

cal_posy = ak.concatenate((hcal_arrays['HcalEndcapPMergedHits.position.y'],
                           hcal_insert_arrays['HcalEndcapPInsertMergedHits.position.y'],
                           ecal_arrays['EcalEndcapPRecHits.position.y'],
                           ecal_insert_arrays['EcalEndcapPInsertRecHits.position.y']),
                          axis=-1)

cal_posz = ak.concatenate((hcal_arrays['HcalEndcapPMergedHits.position.z'],
                           hcal_insert_arrays['HcalEndcapPInsertMergedHits.position.z'],
                           ecal_arrays['EcalEndcapPRecHits.position.z'],
                           ecal_insert_arrays['EcalEndcapPInsertRecHits.position.z']),
                          axis=-1)

#For testing
###
print("Test output:")
print(ak.count(hcal_arrays['HcalEndcapPMergedHits.energy'],axis=-1))
print(ak.count(hcal_insert_arrays['HcalEndcapPInsertMergedHits.energy'],axis=-1))
print(ak.count(ecal_arrays['EcalEndcapPRecHits.energy'],axis=-1))
print(ak.count(ecal_insert_arrays['EcalEndcapPInsertRecHits.energy'],axis=-1))
print(ak.count(cal_energy,axis=-1))
print("")
###

#Create hit position vector and reconstucted momentum vector
cal_pos_vec = vector.zip({
    "x": cal_posx,
    "y": cal_posy,
    "z": cal_posz,
})

cal_pos_unit = cal_pos_vec.unit()
cal_mom_vec = cal_energy*cal_pos_unit

#For testing
###
print("Test output:")
print(type(cal_pos_vec))
print(type(cal_pos_unit))
print(type(cal_mom_vec))

print(cal_pos_vec)
print(cal_pos_unit)
print(cal_energy)
print(cal_mom_vec)
print("")
###

#Rotate hit momentum vectors to be defined relative to proton beam direction
cal_mom_vec_star = cal_mom_vec.rotateY(25./1000.)
cal_energy_star = cal_mom_vec_star.mag #should be same as unrotated
cal_px_star = cal_mom_vec_star.x
cal_py_star = cal_mom_vec_star.y #should be same as unrotated
cal_pz_star = cal_mom_vec_star.z
cal_eta_star = cal_mom_vec_star.eta
cal_empz_star = cal_energy_star - cal_pz_star

#For testing
###
print("Test output:")
print(cal_energy)
print(cal_energy_star)
print(cal_mom_vec.y)
print(cal_py_star)
print(cal_mom_vec.eta)
print(cal_eta_star)
print("")
###

#Total Reconstructed sums for various eta* cuts -- use simple (unweighted) sum
#eta* > 1.0
cal_e1 = cal_energy_star[(cal_eta_star>1)] #should be same as using unrotated energy
cal_e1_sum = ak.sum(cal_e1,axis=-1)
cal_e14 = cal_energy_star[(cal_eta_star>1) & (cal_eta_star<4)] #should be same as using unrotated energy
cal_e14_sum = ak.sum(cal_e14,axis=-1)

cal_empz1 = cal_empz_star[(cal_eta_star>1)]
cal_empz1_sum = ak.sum(cal_empz1,axis=-1)

cal_px1_sum = ak.sum(cal_px_star[(cal_eta_star>1)],axis=-1)
cal_py1_sum = ak.sum(cal_py_star[(cal_eta_star>1)],axis=-1)
cal_pt1_sum = np.sqrt( cal_px1_sum*cal_px1_sum + cal_py1_sum*cal_py1_sum )

cal_px14_sum = ak.sum(cal_px_star[(cal_eta_star>1) & (cal_eta_star<4)],axis=-1)
cal_py14_sum = ak.sum(cal_py_star[(cal_eta_star>1) & (cal_eta_star<4)],axis=-1)
cal_pt14_sum = np.sqrt( cal_px14_sum*cal_px14_sum + cal_py14_sum*cal_py14_sum )

#eta* > 3.0
cal_e3 = cal_energy_star[(cal_eta_star>3)] #should be same as using unrotated energy
cal_e3_sum = ak.sum(cal_e3,axis=-1)
cal_e34 = cal_energy_star[(cal_eta_star>3) & (cal_eta_star<4)] #should be same as using unrotated energy
cal_e34_sum = ak.sum(cal_e34,axis=-1)

cal_empz3 = cal_empz_star[(cal_eta_star>3)]
cal_empz3_sum = ak.sum(cal_empz3,axis=-1)

cal_px34_sum = ak.sum(cal_px_star[(cal_eta_star>3) & (cal_eta_star<4)],axis=-1)
cal_py34_sum = ak.sum(cal_py_star[(cal_eta_star>3) & (cal_eta_star<4)],axis=-1)
cal_pt34_sum = np.sqrt( cal_px34_sum*cal_px34_sum + cal_py34_sum*cal_py34_sum )

#For testing
###
print("Test output:")
print(cal_e1_sum)
print(cal_empz1_sum)
print(cal_empz3_sum)
print("")
###

#High-x events: eta* > 1.0 & x > 0.3
cal_empz1_highx = cal_empz1_sum[x_flat>0.3]
cal_pt1_highx = cal_pt1_sum[x_flat>0.3]

cal_y_highx = cal_empz1_highx / (2.*18.)
cal_yres_highx = 100.*(cal_y_highx-y_highx)/y_highx

cal_Q2_highx = (cal_pt1_highx*cal_pt1_highx) / (1. - cal_y_highx)
cal_Q2res_highx = 100.*(cal_Q2_highx-Q2_highx)/Q2_highx

#For testing
###
print("Test output:")
print(cal_yres_highx)
print("")
###


# ### Repeat Calorimeter Reconstruction -- No Insert

#Combine in one set of Awkward arrays (for easier rotation and summing)
cal_noin_energy = ak.concatenate((hcal_arrays['HcalEndcapPMergedHits.energy'],
                             ecal_arrays['EcalEndcapPRecHits.energy'],),
                            axis=-1)

cal_noin_posx = ak.concatenate((hcal_arrays['HcalEndcapPMergedHits.position.x'],
                           ecal_arrays['EcalEndcapPRecHits.position.x'],),
                          axis=-1)

cal_noin_posy = ak.concatenate((hcal_arrays['HcalEndcapPMergedHits.position.y'],
                           ecal_arrays['EcalEndcapPRecHits.position.y'],),
                          axis=-1)

cal_noin_posz = ak.concatenate((hcal_arrays['HcalEndcapPMergedHits.position.z'],
                           ecal_arrays['EcalEndcapPRecHits.position.z'],),
                          axis=-1)

#Create hit position vector and reconstucted momentum vector
cal_noin_pos_vec = vector.zip({
    "x": cal_noin_posx,
    "y": cal_noin_posy,
    "z": cal_noin_posz,
})

cal_noin_pos_unit = cal_noin_pos_vec.unit()
cal_noin_mom_vec = cal_noin_energy*cal_noin_pos_unit

#Rotate hit momentum vectors to be defined relative to proton beam direction
cal_noin_mom_vec_star = cal_noin_mom_vec.rotateY(25./1000.)
cal_noin_energy_star = cal_noin_mom_vec_star.mag #should be same as unrotated
cal_noin_px_star = cal_noin_mom_vec_star.x
cal_noin_py_star = cal_noin_mom_vec_star.y #should be same as unrotated
cal_noin_pz_star = cal_noin_mom_vec_star.z
cal_noin_eta_star = cal_noin_mom_vec_star.eta
cal_noin_empz_star = cal_noin_energy_star - cal_noin_pz_star

#Total sums for various eta* cuts -- use simple (unweighted) sum
#eta* > 1.0
cal_noin_e1 = cal_noin_energy_star[(cal_noin_eta_star>1)] #should be same as using unrotated energy
cal_noin_e1_sum = ak.sum(cal_noin_e1,axis=-1)
cal_noin_e14 = cal_noin_energy_star[(cal_noin_eta_star>1) & (cal_noin_eta_star<4)] #should be same as using unrotated energy
cal_noin_e14_sum = ak.sum(cal_noin_e14,axis=-1)

cal_noin_empz1 = cal_noin_empz_star[(cal_noin_eta_star>1)]
cal_noin_empz1_sum = ak.sum(cal_noin_empz1,axis=-1)

cal_noin_px1_sum = ak.sum(cal_noin_px_star[(cal_noin_eta_star>1)],axis=-1)
cal_noin_py1_sum = ak.sum(cal_noin_py_star[(cal_noin_eta_star>1)],axis=-1)
cal_noin_pt1_sum = np.sqrt( cal_noin_px1_sum*cal_noin_px1_sum + cal_noin_py1_sum*cal_noin_py1_sum )

cal_noin_px14_sum = ak.sum(cal_noin_px_star[(cal_noin_eta_star>1) & (cal_noin_eta_star<4)],axis=-1)
cal_noin_py14_sum = ak.sum(cal_noin_py_star[(cal_noin_eta_star>1) & (cal_noin_eta_star<4)],axis=-1)
cal_noin_pt14_sum = np.sqrt( cal_noin_px14_sum*cal_noin_px14_sum + cal_noin_py14_sum*cal_noin_py14_sum )

#eta* > 3.0
cal_noin_e3 = cal_noin_energy_star[(cal_noin_eta_star>3)] #should be same as using unrotated energy
cal_noin_e3_sum = ak.sum(cal_noin_e3,axis=-1)
cal_noin_e34 = cal_noin_energy_star[(cal_noin_eta_star>3) & (cal_noin_eta_star<4)] #should be same as using unrotated energy
cal_noin_e34_sum = ak.sum(cal_noin_e34,axis=-1)

cal_noin_empz3 = cal_noin_empz_star[(cal_noin_eta_star>3)]
cal_noin_empz3_sum = ak.sum(cal_noin_empz3,axis=-1)

cal_noin_px34_sum = ak.sum(cal_noin_px_star[(cal_noin_eta_star>3) & (cal_noin_eta_star<4)],axis=-1)
cal_noin_py34_sum = ak.sum(cal_noin_py_star[(cal_noin_eta_star>3) & (cal_noin_eta_star<4)],axis=-1)
cal_noin_pt34_sum = np.sqrt( cal_noin_px34_sum*cal_noin_px34_sum + cal_noin_py34_sum*cal_noin_py34_sum )

#High-x events: eta* > 1.0 & x > 0.3
cal_noin_empz1_highx = cal_noin_empz1_sum[x_flat>0.3]
cal_noin_pt1_highx = cal_noin_pt1_sum[x_flat>0.3]

cal_noin_y_highx = cal_noin_empz1_highx / (2.*18.)
cal_noin_yres_highx = 100.*(cal_noin_y_highx-y_highx)/y_highx

cal_noin_Q2_highx = (cal_noin_pt1_highx*cal_noin_pt1_highx) / (1. - cal_noin_y_highx)
cal_noin_Q2res_highx = 100.*(cal_noin_Q2_highx-Q2_highx)/Q2_highx


# ### Plotting

#Output pdf file
pp1 = PdfPages('pendcap_analysis_djangoh.pdf')

#Plot generated Q2 vs. x
print("Generated Kinematics:")
print("")
x_bins = np.logspace(-3,0,16)
Q2_bins = np.logspace(1,5,21)

#Need to flatten and then convert to numpy array for 2D histogram
counts, xedges, yedges, im = plt.hist2d(np.array(x_flat),
                                        np.array(Q2_flat),
                                        bins=[x_bins,Q2_bins],
                                        norm=mpl.colors.LogNorm(),cmap=plt.cm.jet)
plt.title("Generated Kinematics",fontsize=14)
plt.xlabel("x")
plt.ylabel("$Q^{2} [GeV^2]$")
plt.xscale("log")
plt.yscale("log")

axes = plt.gca()
axes.xaxis.label.set_size(22)
axes.yaxis.label.set_size(22)
axes.tick_params(axis='both',labelsize=14)
axes.spines["left"].set_linewidth(2)
axes.spines["right"].set_linewidth(2)
axes.spines["bottom"].set_linewidth(2)
axes.spines["top"].set_linewidth(2)

plt.colorbar(im)

#Figure Output
fig = plt.gcf()
fig.set_size_inches(18.5/2, 10.5/2)
plt.show()
fig.savefig(pp1, format='pdf')

print("")

#eta* > 1.0
print("Eta* > 1.0:")
print("")
#Plot Total Energy
plt.hist(e1_sum,label="Truth",histtype='step',ec='red',
         lw=3,bins=100,range=[0,300])
plt.hist(cal_e1_sum,label="Reconstructed",histtype='step',ec='blue',
         lw=3,bins=100,range=[0,300])
plt.hist(cal_noin_e1_sum,label="Rec. - No inserts",histtype='step',ec='lime',
         lw=3,bins=100,range=[0,300])
plt.xlabel("Total Energy [GeV]",fontsize=14)
plt.title('$\eta* > 1.0$',fontsize=14)
plt.legend(fontsize=14)

#Figure Output
fig = plt.gcf()
fig.set_size_inches(18.5/2, 10.5/2)
plt.show()
fig.savefig(pp1, format='pdf')

#Plot Total Energy
plt.hist(e14_sum,label="Truth",histtype='step',ec='red',
         lw=3,bins=100,range=[0,250])
plt.hist(cal_e14_sum,label="Reconstructed",histtype='step',ec='blue',
         lw=3,bins=100,range=[0,250])
plt.hist(cal_noin_e14_sum,label="Rec. - No inserts",histtype='step',ec='lime',
         lw=3,bins=100,range=[0,250])
plt.xlabel("Total Energy [GeV]",fontsize=14)
plt.title('$1.0 < \eta* < 4.0$',fontsize=14)
plt.legend(fontsize=14)

#Figure Output
fig = plt.gcf()
fig.set_size_inches(18.5/2, 10.5/2)
plt.show()
fig.savefig(pp1, format='pdf')

#Plot Total Energy -- 2D
counts, xedges, yedges, im = plt.hist2d(np.array(e14_sum),np.array(cal_e14_sum),
                                        bins=(100,100),range=([0,250],[0,250]),
                                        cmap=plt.cm.jet,cmin = 1)
plt.title("$1.0 < \eta* < 4.0$",fontsize=14)
plt.xlabel("Total True Energy [GeV]")
plt.ylabel("Total Rec. Energy [GeV]")

axes = plt.gca()
axes.xaxis.label.set_size(20)
axes.yaxis.label.set_size(20)
axes.tick_params(axis='both',labelsize=14)
axes.spines["left"].set_linewidth(2)
axes.spines["right"].set_linewidth(2)
axes.spines["bottom"].set_linewidth(2)
axes.spines["top"].set_linewidth(2)

plt.colorbar(im)

#Figure Output
fig = plt.gcf()
fig.set_size_inches(18.5/2, 10.5/2)
plt.show()
fig.savefig(pp1, format='pdf')

#Plot Total E-pz
plt.hist(empz1_sum,label="Truth",histtype='step',ec='red',
         lw=3,bins=100,range=[0,8])
plt.hist(cal_empz1_sum,label="Reconstructed",histtype='step',ec='blue',
         lw=3,bins=100,range=[0,8])
plt.hist(cal_noin_empz1_sum,label="Rec. - No inserts",histtype='step',ec='lime',
         lw=3,bins=100,range=[0,8])
plt.xlabel("Total $E - p_{z*}$ [GeV]",fontsize=14)
plt.title('$\eta* > 1.0$',fontsize=14)
plt.legend(fontsize=14)

#Figure Output
fig = plt.gcf()
fig.set_size_inches(18.5/2, 10.5/2)
plt.show()
fig.savefig(pp1, format='pdf')

#Plot total transverse momentum
plt.hist(pt14_sum,label="Truth",histtype='step',ec='red',
         lw=3,bins=100,range=[0,8])
plt.hist(cal_pt14_sum,label="Reconstructed",histtype='step',ec='blue',
         lw=3,bins=100,range=[0,8])
plt.hist(cal_noin_pt14_sum,label="Rec. - No inserts",histtype='step',ec='lime',
         lw=3,bins=100,range=[0,8])
plt.xlabel("Total $P_{T*}$ [GeV/c]",fontsize=14)
plt.title('1.0 < $\eta* < 4.0$',fontsize=14)
plt.legend(fontsize=14)

#Figure Output
fig = plt.gcf()
fig.set_size_inches(18.5/2, 10.5/2)
plt.show()
fig.savefig(pp1, format='pdf')

print("")

#eta* > 3.0
print("Eta* > 3.0:")
print("")
#Plot Total Energy
plt.hist(e3_sum,label="Truth",histtype='step',ec='red',
         lw=3,bins=100,range=[0,300])
plt.hist(cal_e3_sum,label="Reconstructed",histtype='step',ec='blue',
         lw=3,bins=100,range=[0,300])
plt.hist(cal_noin_e3_sum,label="Rec. - No inserts",histtype='step',ec='lime',
         lw=3,bins=100,range=[0,300])
plt.xlabel("Total Energy [GeV]",fontsize=14)
plt.title('$\eta* > 3.0$',fontsize=14)
plt.legend(fontsize=14)

#Figure Output
fig = plt.gcf()
fig.set_size_inches(18.5/2, 10.5/2)
plt.show()
fig.savefig(pp1, format='pdf')

#Plot Total Energy
plt.hist(e34_sum,label="Truth",histtype='step',ec='red',
         lw=3,bins=100,range=[0,80])
plt.hist(cal_e34_sum,label="Reconstructed",histtype='step',ec='blue',
         lw=3,bins=100,range=[0,80])
plt.hist(cal_noin_e34_sum,label="Rec. - No inserts",histtype='step',ec='lime',
         lw=3,bins=100,range=[0,80])
plt.xlabel("Total Energy [GeV]",fontsize=14)
plt.title('$3.0 < \eta* < 4.0$',fontsize=14)
plt.yscale("log")
plt.legend(fontsize=14)

#Figure Output
fig = plt.gcf()
fig.set_size_inches(18.5/2, 10.5/2)
plt.show()
fig.savefig(pp1, format='pdf')

#Plot Total Energy -- 2D
counts, xedges, yedges, im = plt.hist2d(np.array(e34_sum),np.array(cal_e34_sum),
                                        bins=(100,100),range=([0,80],[0,80]),
                                        cmap=plt.cm.jet,norm=mpl.colors.LogNorm())
plt.title("$3.0 < \eta* < 4.0$",fontsize=14)
plt.xlabel("Total True Energy [GeV]")
plt.ylabel("Total Rec. Energy [GeV]")

axes = plt.gca()
axes.xaxis.label.set_size(20)
axes.yaxis.label.set_size(20)
axes.tick_params(axis='both',labelsize=14)
axes.spines["left"].set_linewidth(2)
axes.spines["right"].set_linewidth(2)
axes.spines["bottom"].set_linewidth(2)
axes.spines["top"].set_linewidth(2)

plt.colorbar(im)

#Figure Output
fig = plt.gcf()
fig.set_size_inches(18.5/2, 10.5/2)
plt.show()
fig.savefig(pp1, format='pdf')

#Plot Total E-pz
plt.hist(empz3_sum,label="Truth",histtype='step',ec='red',
         lw=3,bins=100,range=[0,0.6])
plt.hist(cal_empz3_sum,label="Reconstructed",histtype='step',ec='blue',
         lw=3,bins=100,range=[0,0.6])
plt.hist(cal_noin_empz3_sum,label="Rec. - No inserts",histtype='step',ec='lime',
         lw=3,bins=100,range=[0,0.6])
plt.title('$\eta* > 3.0$',fontsize=14)
plt.xlabel("Total $E - p_{z*}$ [GeV]",fontsize=14)
plt.yscale("log")
plt.legend(fontsize=14)

#Figure Output
fig = plt.gcf()
fig.set_size_inches(18.5/2, 10.5/2)
plt.show()
fig.savefig(pp1, format='pdf')

#Plot total transverse momentum
plt.hist(pt34_sum,label="Truth",histtype='step',ec='red',
         lw=3,bins=100,range=[0,2])
plt.hist(cal_pt34_sum,label="Reconstructed",histtype='step',ec='blue',
         lw=3,bins=100,range=[0,2])
plt.hist(cal_noin_pt34_sum,label="Rec. - No inserts",histtype='step',ec='lime',
         lw=3,bins=100,range=[0,2])
plt.xlabel("Total $P_{T*}$ [GeV/c]",fontsize=14)
plt.title('3.0 < $\eta* < 4.0$',fontsize=14)
plt.yscale("log")
plt.legend(fontsize=14)

#Figure Output
fig = plt.gcf()
fig.set_size_inches(18.5/2, 10.5/2)
plt.show()
fig.savefig(pp1, format='pdf')

print("")

#High-x events: eta* > 1.0 & x > 0.3
print("x > 0.3 and Eta* > 1.0:")
print("")

#Plot Total E-pz
plt.hist(empz1_highx,label="Truth",histtype='step',ec='red',
         lw=3,bins=100,range=[0,8])
plt.hist(cal_empz1_highx,label="Reconstructed",histtype='step',ec='blue',
         lw=3,bins=100,range=[0,8])
plt.hist(cal_noin_empz1_highx,label="Rec. - No inserts",histtype='step',ec='lime',
         lw=3,bins=100,range=[0,8])
plt.xlabel("Total $E - p_{z*}$ [GeV]",fontsize=14)
plt.title('$Q^{2} > 100~GeV^{2}$ and $x > 0.3$ and $\eta* > 1.0$',fontsize=14)
plt.legend(fontsize=14)

#Figure Output
fig = plt.gcf()
fig.set_size_inches(18.5/2, 10.5/2)
plt.show()
fig.savefig(pp1, format='pdf')

#Plot total transverse momentum
plt.hist(pt1_highx,label="Truth",histtype='step',ec='red',
         lw=3,bins=100,range=[0,40])
plt.hist(cal_pt1_highx,label="Reconstructed",histtype='step',ec='blue',
         lw=3,bins=100,range=[0,40])
plt.hist(cal_noin_pt1_highx,label="Rec. - No inserts",histtype='step',ec='lime',
         lw=3,bins=100,range=[0,40])
plt.xlabel("Total $P_{T*}$ [GeV/c]",fontsize=14)
plt.title('$Q^{2} > 100~GeV^{2}$ and $x > 0.3$ and $\eta* > 1.0$',fontsize=14)
plt.legend(fontsize=14)

#Figure Output
fig = plt.gcf()
fig.set_size_inches(18.5/2, 10.5/2)
plt.show()
fig.savefig(pp1, format='pdf')

#Plot y resolution
plt.hist(cal_yres_highx ,label="Reconstructed",histtype='step',ec='blue',
         lw=3,bins=100,range=[-100,100])
plt.hist(cal_noin_yres_highx,label="Rec. - No inserts",histtype='step',ec='lime',
         lw=3,bins=100,range=[-100,100])
plt.xlabel("y resolution [%]",fontsize=14)
plt.title('$Q^{2} > 100~GeV^{2}$ and $x > 0.3$',fontsize=14)
plt.legend(fontsize=14)

#Figure Output
fig = plt.gcf()
fig.set_size_inches(18.5/2, 10.5/2)
plt.show()
fig.savefig(pp1, format='pdf')

#Plot Q2 resolution
plt.hist(cal_Q2res_highx ,label="Reconstructed",histtype='step',ec='blue',
         lw=3,bins=100,range=[-100,100])
plt.hist(cal_noin_Q2res_highx,label="Rec. - No inserts",histtype='step',ec='lime',
         lw=3,bins=100,range=[-100,100])
plt.xlabel("$Q^{2}$ resolution [%]",fontsize=14)
plt.title('$Q^{2} > 100~GeV^{2}$ and $x > 0.3$',fontsize=14)
plt.legend(fontsize=14)

#Figure Output
fig = plt.gcf()
fig.set_size_inches(18.5/2, 10.5/2)
plt.show()
fig.savefig(pp1, format='pdf')

#Plot at generator level the fraction of total energy in 1<eta*<4 
#range that is contained in 3<eta*<4 range vs. x
print("Energy Fraction:")
print("")

x_bins = np.logspace(-2.2,0,26)
e_bins = np.linspace(-0.05,1.05,100)

counts, xedges, yedges, im = plt.hist2d(np.array(x_frac),np.array(e_frac),
                                        bins=[x_bins,e_bins],
                                        cmap=plt.cm.jet,norm=mpl.colors.LogNorm())
plt.title("Particles in $1 < \eta* < 4$ range, $Q^{2} > 100~GeV^{2}$",fontsize=14)
plt.xlabel("x")
plt.ylabel("Fraction of energy in $3 < \eta* < 4$")

axes = plt.gca()
axes.xaxis.label.set_size(20)
axes.yaxis.label.set_size(14)
axes.tick_params(axis='both',labelsize=14)
axes.spines["left"].set_linewidth(2)
axes.spines["right"].set_linewidth(2)
axes.spines["bottom"].set_linewidth(2)
axes.spines["top"].set_linewidth(2)
plt.xscale("log")

plt.colorbar(im)

#Figure Output
fig = plt.gcf()
fig.set_size_inches(18.5/2, 10.5/2)
plt.show()
fig.savefig(pp1, format='pdf')

#Close file
pp1.close()
