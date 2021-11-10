# **Streamlined DAM Analysis**

### **DAM**: **D**rosophila **A**ctivity **M**onitor

---

Refer to the Read_me.md and Instructions.md in each pacakge for more information.

## Packages

- DAM_blips_package
- DAM_streamline_package

## Steps

1. Download the repository to your working directory on Secretariat

   - Option A: Download _with_ git: `git clone git@github.com:ypan23-1876660/DAM.git`

   - Option B: Download _without_ `git`: `svn checkout https://github.com/ypan23-1876660/DAM`

2. Run the DAM_blips_package script: `sbatch blips_shscript.sh`

3. Download the results from (2) and run ShinyR DAM

4. Upload the results from (3) to Secretariat

5. Run the DAM_streamline_package script: `sbatch dam_shscript.sh`

6. Download the results for futher analysis (e.g. SAS)
