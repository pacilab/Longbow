# Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B Shannon 2015.
#
# This file is part of the Longbow software which was developed as part of
# the HECBioSim project (http://www.hecbiosim.ac.uk/).
#
# HECBioSim facilitates and supports high-end computing within the
# UK biomolecular simulation community on resources such as Archer.
#
# Longbow is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Longbow is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Longbow.  If not, see <http://www.gnu.org/licenses/>.

"""."""

import logging                                                  # IMPORTANT
import math
import os
import corelibs.exceptions as ex
import corelibs.shellwrappers as shellwrappers


# -----------------------------------------------------------------------------
# Boiler plate for logging.

LOGGER = logging.getLogger("Longbow")                           # IMPORTANT

# -----------------------------------------------------------------------------
# For schedulers a unique string to identify the scheduler should go here.
# Sometimes "env | grep -i 'something specific'" will suffice.

QUERY_STRING = "which sbatch"                        # IMPORTANT

# -----------------------------------------------------------------------------
# Delete method (not currently used).


def delete(host, jobid):                                        # IMPORTANT

    """Method for deleting job."""

    LOGGER.info("Deleting the job with id: %s", jobid)
    try:
        shellout = shellwrappers.sendtossh(host, ["scancel " + jobid])

    except ex.SSHError:
        raise ex.JobdeleteError("  Unable to delete job.")

    LOGGER.info("Deleted successfully")

    return shellout[0]


# -----------------------------------------------------------------------------
# Prepare method

def prepare(hosts, jobname, jobs):                             # IMPORTANT

    """Create the SLURM jobfile ready for submitting jobs"""

    LOGGER.info("Creating submit file for job: %s", jobname)

    # Open file for SLURM script.
    slurmfile = os.path.join(jobs[jobname]["localworkdir"], "submit.slurm")
    jobfile = open(slurmfile, "w+")

    # Write the SLURM script
    jobfile.write("#!/bin/bash --login\n")

    # Job name (if supplied)
    if jobname is not "":
        jobfile.write("#SBATCH -J " + jobname + "\n")

    # Queue to submit to (if supplied)
    if jobs[jobname]["queue"] is not "":
        jobfile.write("#SBATCH -p " + jobs[jobname]["queue"] + "\n")

    resource = jobs[jobname]["resource"]

    # Account to charge (if supplied)
    if hosts[resource]["account"] is not "":
        # if no accountflag is provided use the default
        if hosts[resource]["accountflag"] is "":
            jobfile.write("#SBATCH -A " + hosts[resource]["account"] + "\n")

        else:
            jobfile.write("#SBATCH " +
                          hosts[resource]["accountflag"] +
                          " " + hosts[resource]["account"] + "\n")

    cores = hosts[resource]["cores"]
    cpn = hosts[resource]["corespernode"]

    # Specify the total number of mpi tasks required
    jobfile.write("#SBATCH -n " + cores + "\n")

    # If user has specified corespernode for under utilisation then
    # set the total nodes (-N) parameter.
    if cpn is not "":
        nodes = float(cores) / float(cpn)

        # Make sure nodes is rounded up to the next highest integer
        nodes = str(int(math.ceil(nodes)))
        jobfile.write("#SBATCH -N " + nodes + "\n")

    # Walltime for job
    jobfile.write("#SBATCH -t " + jobs[jobname]["maxtime"] + ":00\n")

    if int(jobs[jobname]["batch"]) > 1:
        jobfile.write("#SBATCH --array=1-" + jobs[jobname]["batch"] + "\n")

    # Load up modules if required.
    if jobs[jobname]["modules"] is not "":
        for module in jobs[jobname]["modules"].split(","):
            module.replace(" ", "")
            jobfile.write("module load %s\n\n" % module)

    # Handler that is used for job submission.
    mpirun = hosts[resource]["handler"]

    # Single jobs only need one run command.
    if int(jobs[jobname]["batch"]) == 1:
        jobfile.write(mpirun + " " + jobs[jobname]["commandline"] + "\n")

    # Ensemble jobs need a loop.
    elif int(jobs[jobname]["batch"]) > 1:
        jobfile.write("basedir = `pwd`"
                      "cd $basedir/rep${SLURM_ARRAY_TASK_ID}/\n" +
                      mpirun + " " + jobs[jobname]["commandline"] +
                      " &\n"
                      "wait\n")

    # Close the file
    jobfile.close()

    # Append submitfile to list of files ready for staging.
    jobs[jobname]["filelist"].extend(["submit.slurm"])            # IMPORTANT
    jobs[jobname]["subfile"] = "submit.slurm"                     # IMPORTANT


# -----------------------------------------------------------------------------
# Status method

def status(host, jobid):                                        # IMPORTANT

    """Method for querying job."""

    state = ""

    try:
        shellout = shellwrappers.sendtossh(host, ["squeue -u " + host["user"] +
                                                  "| grep " + jobid])

        stat = shellout[0].split()

        if stat[4] == "CA":
            state = "Cancelled"

        elif stat[4] == "CD":
            state = "Completed"

        elif stat[4] == "CF":
            state = "Configuring"

        elif stat[4] == "CG":
            state = "Completing"

        elif stat[4] == "F":
            state = "Failed"

        elif stat[4] == "NF":
            state = "Node failure"

        elif stat[4] == "PD":
            state = "Pending"

        elif stat[4] == "PR":
            state = "Preempted"

        elif stat[4] == "R":
            state = "Running"

        elif stat[4] == "S":
            state = "Suspended"

        elif stat[4] == "TO":
            state = "Timed out"

    except ex.SSHError:
        state = "Finished"

    return state

# -----------------------------------------------------------------------------
# Submit method


def submit(host, jobname, jobs):                                # IMPORTANT

    """Method for submitting job."""

    path = os.path.join(host["remoteworkdir"], jobname)

    # Change into the working directory and submit the job.
    cmd = ["cd " + path + "\n" + "sbatch " + jobs[jobname]["subfile"] +
           "| tail -1 | awk '{print $4}'"]

    # Process the submit
    try:
        shellout = shellwrappers.sendtossh(host, cmd)[0]

    except ex.SSHError:
        raise ex.JobsubmitError("  Something went wrong when submitting.")

    output = shellout.rstrip("\r\n")

    LOGGER.info("Job: %s submitted with id: %s", jobname, output)

    jobs[jobname]["jobid"] = output                             # IMPORTANT