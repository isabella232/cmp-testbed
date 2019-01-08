# CMP² - Testbed for recomputable multi-cloud management experiments

CMP² lets you define workflows of actions related to cloud management (e.g. start new virtual machine, delete some files) in multi-cloud environments. It makes use of cloud management platforms (CMP) which are effectively compared concerning performance and resource use. Results are output as text and diagrams.

This testbed is created as research in education linked to the Cloud Accounting and Billing research initiative at Service Prototyping Lab, Zurich University of Applied Sciences, Switzerland. Related to it is a paper entitled «Systematic and recomputable comparison of multi-cloud management platforms», published at CloudCom 2018 (https://doi.org/10.1109/CloudCom2018.2018.00032).

# CMPs and Providers

Currently, CMP² supports local system metrics as well as remote metrics for AWS and Azure. It supports ManageIQ, Cloudbridge, Cloudify, Cloudcheckr, Boto, Libcloud and Mistio as CMPs. Some of them are "CMPs" in a wider sense, more in the form of libraries, but for all remote services (cloud providers and CMPs) that require authentication, CMP² lets you configure the credentials. Additional providers and CMPs can be added easily; see below for instructions.

# Workflows

## Workflow to extend existing driver

Just add methods which are wrapped by timing and tagging tags (resource consumption is optional).

## Workflow to add new driver

In practice, drivers can be located anywhere in Python project, but to keep things in order it is strongly recommended to place them under the corresponding folder like docker_based, docker_compose_based, library_based or website. An evaluation file of a driver should import Decorator class which is aimed to provide decorators for evaluation. Imported decorators should wrap the same as with extension of existing drivers methods which are added. The last step is to add the client to registered clients. It should be added to register.py file into the registered_cilents dictionary. The key name will be the name associated with the client in matrix.yml file and value the client itself.

## Steps to extend testbed to make experiments with file uploading

This is an exemplary description which refers to the comparative work we described in our paper:

First of all existing libcloud was extended by new methods: create\delete aws bucket, upload/download/delete file to the bucket which were warped by tagging, timing and python consumption decorators.
Second step was to create new driver for patform specific library, in this case boto library was choosen. This dirver was populated by the same methods for file uploading as libcloud. Most effort was done in understanding libraries fuctionalities because of lack of documentation especally for libcloud.
Once both drivers contained all needed methods the Boto driver was registered in register.py file.

Finally to run experiments following yml structure was created for each file size:

---
1240_KB:
  repetitions: 50
    output_dir: /home/lexxito/experiments
      cmps: [libcloud, boto_aws]
        providers: [aws]
          pre_experiment:
            bucket:
              - create:
                  - lexx
          post_experiment:
            bucket:
              - delete
          actions:
            file:
              - upload:
                  - /home/ubuntu/test/files/1240_KB
              - download:
                  - /home/ubuntu/test/
              - delete

---

This structre suppose to repeat experiment for 1240 KB file 50 times. Before experimentcreated a bucket with a name lexx, and deleted after all experiments are done. In the deletion it is not neccesary to specify what bucket to delete, while since it is not specified it uses the last one which was actioned. In the experiment itself the file was uploaded, downloaded and deleted. All data for these actions was saved into experiments folder.
Generating simple graphs and latex tables requiered no changes. The code for generating graphs was slighly changed to achieve the same boxplot order and structure as it done in evalutions muli-cloud api work.

Overall the work took 5 hours where the most time was spent in investigation of library finctionality.

Comparing results from previouse work and our results we can conclude that results lead to the same conclusions:

- The performance of multi-cloud differs significantly from platform-specific API
- Libcloud outperformed platform-specific APIs in most tests.

Because of different locations response time for uploading and downloading differs. While In both graphs we can see the same trends for boxplots with growing size of files the dowload time growth linery, also in all experiments in both grapghs  libcloud has bigger response time.

## Data

Experiments_data contains a raw data, where is a name of the folder corresponds to the name of the experiment and each file the combination of provider and action. Each row of the file contains information for every experiment. Each result has the following structure :

{"provider:item:action": {"consumption": {"start": {memory:{}, cpu{}}, "end": {memory:{}, cpu{}}, "time": 1111}}

