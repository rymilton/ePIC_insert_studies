#!/bin/bash

# Input simulation parameters
particle="e-"
beam_energy=1
num_events=1000
theta=3.459 # in degrees

# Output file names
info_string="${particle}_${beam_energy}GeV_theta_${theta}deg"
hepmcfile="gen_${info_string}.hepmc"

# Generating hepmc file
root -l -b -q "gen_particles.cxx(\
${num_events},\
\"${hepmcfile}\",\
\"${particle}\",\
${theta_min},\
${theta_max},\
${phi_min},\
${phi_max},\
${beam_energy})"
