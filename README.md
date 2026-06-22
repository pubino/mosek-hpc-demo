# MOSEK on Princeton Della HPC: License Verification & Demo

This repository provides a minimal, self-contained template for postdocs and graduate researchers to verify and demo a personal/academic **MOSEK** license across compute nodes on Princeton Research Computing's **Della** cluster (or any other Princeton cluster running Slurm, e.g., Adroit, Tiger).

By using the files in this repository, you can confirm that your license is validated correctly and that jobs run successfully across multiple cluster nodes.

---

## 1. Prerequisites

1. An active Princeton HPC account (Della access).
2. A valid personal or academic MOSEK license file (`mosek.lic`). 
   * *If you do not have one, you can request an Academic License from [MOSEK's website](https://www.mosek.com/products/academic-licenses/).*

---

## 2. Setup

### A. Copy your License to Della

MOSEK looks for the license file in a default directory `~/mosek/mosek.lic`. 

From your local machine, create the directory on Della (if it doesn't exist) and transfer your license file using `scp` (replace `netid` with your Princeton NetID):

```bash
# Create the mosek directory on Della
ssh netid@della.princeton.edu "mkdir -p ~/mosek"

# Transfer the license file
scp mosek.lic netid@della.princeton.edu:~/mosek/mosek.lic
```

*Note: Alternatively, if you wish to store the license file elsewhere, you must configure the environment variable `export MSK_LICENSE_FILE=/path/to/your/mosek.lic` in your environment or SLURM script.*

### B. Clone this Repository on Della

SSH into Della and clone this repository:

```bash
ssh netid@della.princeton.edu
git clone https://github.com/pubino/mosek-hpc-demo.git
cd mosek-hpc-demo
```

---

## 3. Run Verification on the Cluster

Submit the verification job to the Slurm scheduler:

```bash
sbatch job.slurm
```

### How it Works Under the Hood
1. **Modules**: The script automatically purges conflicting environments and loads Princeton's standard Anaconda environment (`anaconda3/2024.6`).
2. **Auto-Install**: It checks if the Python `mosek` package is present, and if not, automatically installs it into your user space (`pip install --user mosek`).
3. **Multi-Node Verification**: The job script requests **2 nodes** (`--nodes=2`) and uses `srun` to execute `solve.py` simultaneously on all allocated compute nodes. This verifies that your personal license file resolves correctly across distributed nodes.

### Monitoring and Output

Check the job status using `squeue`:

```bash
squeue -u $USER
```

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
Hostname:       della-r3c1n4
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
Hostname:       della-r3c1n5
Python:         3.11.7
Mosek version:  10.1.28
MSK_LICENSE_FILE: [NOT SET] (Using default path)
Checking default path: /home/netid/mosek/mosek.lic
License file exists at default path: Yes
Verification solve result: x = 0.50, y = 0.50
MOSEK license is successfully validated on this node!
=========================================
```

---

## 4. Local Development & Testing

To ensure the scripts are robust and verify local changes without access to the HPC cluster or a MOSEK license, you can run the mock-based unit tests inside a Docker container:

```bash
# Build the test image
docker build -t mosek-demo-test .

# Run the test suite
docker run --rm mosek-demo-test
```

---

## Repository Contents

* [solve.py](file:///Users/bino/Downloads/mosek-demo/solve.py) - Minimal Python script solving a small LP with the MOSEK Fusion API and printing verification details.
* [job.slurm](file:///Users/bino/Downloads/mosek-demo/job.slurm) - Slurm batch script configured for Della.
* [test_solve.py](file:///Users/bino/Downloads/mosek-demo/test_solve.py) - Mocked test suite.
* [Dockerfile](file:///Users/bino/Downloads/mosek-demo/Dockerfile) - Dockerized testing container environment.
* [LICENSE.md](file:///Users/bino/Downloads/mosek-demo/LICENSE.md) - MIT License.

---

## License

This project is licensed under the MIT License - see the [LICENSE.md](file:///Users/bino/Downloads/mosek-demo/LICENSE.md) file for details.
