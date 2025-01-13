# Trigger Short Exercise 2024
Trigger short exercise CMS DAS @ CERN, June 2024 ([Indico](https://indico.cern.ch/event/1388937/))

Slides can be found [here](https://docs.google.com/presentation/d/1QEnsiFPUbY2XtM92Q7x1YLCQcJLH7vEjxXImIo_vR5s/edit#slide=id.g2e2500f5b74_0_138)

Please join our Mattermost channel for Q&A ([link](https://mattermost.web.cern.ch/cmsdas24/channels/short-ex-triggers))

## Facilitators
1. Won Jun, Seoul National U. [wjun@cern.ch](mailto:won.jun@cern.ch)
2. Jieun Choi, Hanyang U./IP2I Lyon [ji.eun.choi@cern.ch](mailto:ji.eun.choi@cern.ch)
3. Pedro Fernandez Manteca, Rice U. [pedro.fernandez.manteca@cern.ch](mailto:pedro.fernandez.manteca@cern.ch)

## Setup
Both lxplus8, and lxplus9 can be used, but lxplus8 is recommended (to check pdf files easily)
```    
source /cvmfs/cms.cern.ch/cmsset_default.sh
mkdir CMSDAS2024
cd CMSDAS2024
cmsrel CMSSW_14_0_8
cd CMSSW_14_0_8/src
cmsenv
git clone https://gitlab.cern.ch/cmsdas-cern-2024/short-ex-triggers.git
scram b -j 4
cd short-ex-triggers
```

## Exercise 1
### Measure the MET triggers efficiencies using the Orthogonal method
```
python3 test/MET_Efficiency_NanoAOD.py          # running over full 2023D EGamma0 NanoAOD datasets
root -l --web=off histos_METTrigNanoAOD.root    # check histograms out
python3 test/MET_Efficiency_Plotting.py         # plotting
gio open ./                                     # check plots out, or you can scp pdf files to your machine
```

## Exercise 2
### Measure the SingleMuon triggers efficiencies using the same method
Similar to ex1, you can draw efficiencies vs. pt like (IsoMu24, Mu50, CascadeMu100, HighPtTkMu100, ALL)

Please try to do it with your own codes, you can use codes from ex1.

If you want to draw their efficiencies vs. eta, phi, then you may need to apply pt cut to offline muons (eg. pt > 26 GeV for IsoMu24)

Try it with less input files first.


<details>
    <summary><i>In case you need help, here's our example</i></summary>

```
python3 test/SingleMuon_Efficiency_NanoAOD_answerEx2.py   # running over partial 2023D EGamma0 NanoAOD datasets
root -l --web=off histos_SingleMuTrigNanoAOD.root         # check histograms out
python3 test/SingleMuon_Efficiency_Plotting_answerEx2.py  # plotting
gio open ./                                               # check plots out, or you can scp pdf files to your machine
```
</details>

## Exercise 3
### Measure the SingleMuon (IsoMu24) trigger efficiency using the Tag & Probe method
```
python3 test/SingleMuon_Efficiency_TnP_NanoAOD.py           # running over full 2023Dv2 Muon0 NanoAOD datasets
root -l --web=off histos_SingleMuTrigNanoAOD_TnP.root       # check histograms out
python3 test/SingleMuon_Efficiency_TnP_Plotting_NanoAOD.py  # plotting
gio open ./                                                 # check plots out, or you can scp pdf files to your machine
```

## Exercise 4 (Optional)
### Measure the SingleMuon (Mu50 || CascadeMu100 || HighPtTkMu100) trigger efficiency
The trigger indexes for Mu50, Mu100s are 10, 11. See this [cms-sw](https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/python/triggerObjects_cff.py#L109-L131)

## In case gio doesn't work for you
you can bring the files to your local machine
```
# in your local machine
scp lxplus.cern.ch:<path>/<to>/<my_directory>/*.pdf .
```
or you can open it via cernbox: https://cernbox.cern.ch/
```
cd /eos/user/<initial>/<username>/
mkdir CMSDAS2024
cd -  # working directory used for trigger exercise
cp *.pdf /eos/user/<initial>/<username>/CMSDAS2024
```

## References or useful links
Twiki of Trigger exercise of CMS DAS @ CERN 2023 : [link](https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideCMSDataAnalysisSchoolCERN2023TriggerExercise)

HLT Tutorials in 2024 : [link](https://indico.cern.ch/event/1344500/)

HLT Tutorials in 2023 : [link](https://indico.cern.ch/event/1238936/)

Trigger exercise for the PO & DAS 2023 @ Hamburg : [link](https://gitlab.cern.ch/cms-analysis/cmsdas/dpg/trigger-exercise)
