#!/bin/bash
rm ../data/.gitkeep; mkdir -p ../output/{error,output_csv,preview} | sbatch ./dam_shscript.sh
