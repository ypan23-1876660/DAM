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

   - Option B: Download _without_ git: `svn checkout https://github.com/ypan23-1876660/DAM`

2. Edit the variables in DAM_blips_package blips_shscript.sh

3. Run the DAM_blips_package initiator script: `sbatch blips_initiator.sh`

4. Download the results from (2) and run ShinyR DAM

5. Upload the results from (3) to Secretariat

6. Run the DAM_streamline_package initiator script: `sbatch dam_initiator.sh`

7. Download the results for futher analysis (e.g. SAS)
