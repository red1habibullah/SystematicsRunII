# SystematicsRunII
Calculation of Systematics for HtoAA RunII Analysis

# Introduction for setting up the environment:

$ export SCRAM_ARCH=slc7_amd64_gcc700

$ cmsrel CMSSW_10_2_18

$ cd CMSSW_10_2_18/src

$ cmsenv

$ git cms-init

$ git clone https://github.com/red1habibullah/SystematicsRunII.git

$ scram b clean

$ scram b -j4

# Running the Scripts

To get fakerate uncertainty on different decaymodes run:

$ python calculate_fakeRate_uncertainty_combined.py

To get percentage difference on different decaymodes  in between datadriven estimate (from region D/ validation sideband) and observed (region C / validation region) run:

$ python calculate_fakeRate_uncertainty_combined_percentage.py

Everytime the list of inputfiles in the scripts needs to be changed. The files are to be put in the data/ directory. The input files are usually Data rootfiles from regions C and D , separated by decaymodes.