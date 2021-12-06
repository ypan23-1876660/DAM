#!/bin/bash
rm ../data/.gitkeep; mkdir -p ../output/{error,output_csv,preview} | sbatch ./blips_shscript.sh
