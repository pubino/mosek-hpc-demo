# MOSEK HPC License Verification & Demo

This repository provides a minimal, self-contained template for postdocs and graduate researchers to verify and demo a personal/academic **MOSEK** license across compute nodes in an HPC cluster.

By using the files in this repository, you can confirm that your license is validated correctly and that jobs run successfully across multiple cluster nodes.

## 1. Prerequisites

1. An active HPC account.
2. A valid personal or academic MOSEK license file (`mosek.lic`). 
   * *If you do not have one, you can request an Academic License from [MOSEK's website](https://www.mosek.com/products/academic-licenses/).*

## 2. Setup

1. Copy your license file to the default `~/mosek/mosek.lic`.  Alternatively, configure the environment variable `export MSK_LICENSE_FILE=/path/to/your/mosek.lic` in your environment or SLURM script.
2. Clone this repo
```
  git clone https://github.com/pubino/mosek-hpc-demo.git
```
4. Run the verification
```
  cd mosek-hpc-demo
  sbatch job.slurm
```

## 3. Verification

Once completed, a file named `mosek_<JOBID>.out` will appear in the directory. Inspect the output:

```bash
cat mosek_*.out
```

Expected output showing successful execution on two distinct compute nodes:

```text
Starting Mosek license verification across cluster nodes...
=========================================
       MOSEK LICENSE VERIFICATION        
=========================================
Hostname:       abc.xyz
Python:         3.11.7
Mosek version:  10.1.28
MSK_LICENSE_FILE: [NOT SET] (Using default path)
Checking default path: /home/netid/mosek/mosek.lic
License file exists at default path: Yes
Verification solve result: x = 0.50, y = 0.50
MOSEK license is successfully validated on this node!
=========================================
=========================================
       MOSEK LICENSE VERIFICATION        
=========================================
Hostname:       zyx.cba
Python:         3.11.7
Mosek version:  10.1.28
MSK_LICENSE_FILE: [NOT SET] (Using default path)
Checking default path: /home/netid/mosek/mosek.lic
License file exists at default path: Yes
Verification solve result: x = 0.50, y = 0.50
MOSEK license is successfully validated on this node!
=========================================
```

## Repository Contents

* [solve.py](file:///Users/bino/Downloads/mosek-demo/solve.py) - Minimal Python script solving a small LP with the MOSEK Fusion API and printing verification details.
* [job.slurm](file:///Users/bino/Downloads/mosek-demo/job.slurm) - Slurm batch script configured for Della.
* [test_solve.py](file:///Users/bino/Downloads/mosek-demo/test_solve.py) - Mocked test suite.
* [Dockerfile](file:///Users/bino/Downloads/mosek-demo/Dockerfile) - Dockerized testing container environment.
* [LICENSE.md](file:///Users/bino/Downloads/mosek-demo/LICENSE.md) - MIT License.
