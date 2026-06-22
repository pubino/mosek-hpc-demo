#!/bin/bash
#SBATCH --job-name=mosek-verify     # Job name
#SBATCH --output=mosek_%j.out       # Standard output and error log (%j is job ID)
#SBATCH --nodes=2                   # Request 2 nodes to verify it runs across cluster
#SBATCH --ntasks-per-node=1         # 1 task per node
#SBATCH --cpus-per-task=1           # Cores per task
#SBATCH --mem=4G                    # Memory per node
#SBATCH --time=00:05:00             # Time limit hrs:min:sec

# Purge existing modules and load Anaconda
module purge
module load anaconda3/2024.6

# Ensure mosek package is installed in the user/conda environment (if not already present)
python3 -c "import mosek" 2>/dev/null || pip install --user mosek

# Run python script using srun to execute it on all requested nodes in parallel
echo "Starting Mosek license verification across cluster nodes..."
srun python3 solve.py
