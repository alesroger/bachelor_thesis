#!/bin/bash
#SBATCH --job-name=RevenueMaximizer
#SBATCH --array=0-0
#SBATCH -N 1
#SBATCH --cpus-per-task=20
#SBATCH --mem=3
#SBATCH -exclude=minion09
#SBATCH --partition=kraken_slow
#SBATCH --mail-type=NONE
#SBATCH --export=ALL
#SBATCH --output=sSearch.out
#SBATCH --error=sSearch.err
#...commands to be run before jobs starts...
filename=main.py

workingDir=/home/slurm/ehrensperger-${SLURM_JOB_ID}

echo "working directory = "$workingDir

#...copy data from home to work folder
# copy jar
cp ~/$filename $workingDir/
cp -r ~/src $workingDir/
echo "Copying Files "$SLURM_ARRAY_TASK_ID".nt to working directory"$workingDir

#Running the Command

/home/user/ehrensperger/anaconda3/bin/python -u $workingDir/$filename > RevenueMaximizer$SLURM_ARRAY_TASK_ID.txt


echo "Running Job-ID:"$SLURM_ARRAY_TASK_ID 



#Copy Back Data (Backup)

cp $workingDir/GB-Statement-"$SLURM_ARRAY_TASK_ID".nt  ~/ 
