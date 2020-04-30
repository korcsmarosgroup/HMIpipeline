# HMI pipeline

**What do you need for the pipeline**

- docker (version = 3.4.0)

**How can you run the pipeline in a docker environment**

First of all, you need an installed, enabled and active docker on your machine.
Second you have to download the github repository from github:

`https://github.com/korcsmarosgroup/HMIpipeline`

After that you only need to run the `hmipipeline.sh` bash script. This will automatically 
build the docker image, run it in a container and enter into it as well.
If everything is good, you should get something like this:

`root@248342fef37e:/home/hmipipeline#`

After that, you can use all of the scripts which are inside the pipeline:

1 Domain-domain interactions (DDI)

- You need to run the following commands:<br>
`cd pipeline/1.DDI/`<br>
`python3 DDIbasedPPIprediction.py`

2 Domain-motif interactions (DMI)

- You need to run the following commands:<br>
`cd pipeline/2.DMI/`<br>
`python3 DMI.py`

3 Structural filtering

- You need to run the following commands:<br>
`cd pipeline/3.Structural_filtering/structural_filtering/`<br>
`python3 src/structural_filtering_prediction.py --hmi_prediction resources/MPDMIresult.tsv --resources resources/ --results results/`

4 TIEDIE

- You need to run the following commands:<br>
`cd pipeline/4.tiedie_with_dmi_results/examples/TieDIE_results_DDI/`<br>
`make`<br>
or<br>
`cd pipeline/4.tiedie_with_dmi_results/examples/TieDIE_results_DMI/`<br>
`make`<br>

If you are done with everything, just quit from the container with the following command: `Ctrl+d`
