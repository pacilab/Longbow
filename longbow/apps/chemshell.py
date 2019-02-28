# BSD 3-Clause License
#
# Copyright (c) 2017, Science and Technology Facilities Council and
# The University of Nottingham
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""This is the Chemshell plugin module.

This plugin is relatively simple in the fact that adding new executables is as
simple as modifying the EXECDATA structure below. See the documentation at
http://www.hecbiosim.ac.uk/longbow-devdocs for more information.
"""

import logging
import re
import longbow.exceptions as exceptions
import longbow.shellwrappers as shellwrappers


EXECDATA = {
    "chemsh": {
        "subexecutables": [],
        "requiredfiles": ["<"]
    }
}

LOG = logging.getLogger("longbow.apps.chemshell")


def rsyncuploadhook(jobs, job):
    '''Override the default rsync upload parameters to null so that rsync
    basically transfers all files'''

    jobs[job]["upload-include"] = ""
    jobs[job]["upload-exclude"] = "log, *.log"


def submitscripthook(job):
    '''
    This hook will replace the generation of a submit script. Since Chemshell
    calls the scheduler by itself, we will defer this functionality to
    Chemshell itself.
    '''

    LOG.info("For job {0} - Chemshell is being used so skip creation of "
             "submit file.".format(job["jobname"]))


def submithook(job):
    '''
    This hook will SSH into the HPC machine, change into the job directory then
    run Chemshell which in turn will submit a job. It will grab the jobid from
    chemshell.
    '''

    LOG.info("Chemshell plugin some of the native functionality of Longbow.")

    args = job["executableargs"]
    newargs = ""

    if "--submit" not in args:

        newargs = " --submit"

    if "--account" not in args and "-A" not in args and job["account"] != "":

        newargs = newargs + " --account " + job["account"]

    if "--queue" not in args and "-q" not in args and job["queue"] != "":

        newargs = newargs + " --queue " + job["queue"]

    job["executableargs"] = args + newargs

    LOG.info("For job '%s' - execution string: %s", job["jobname"],
             job["executableargs"])

    # Change into the working directory and submit the job.
    cmd = ["cd " + job["destdir"] + "\n", job["executableargs"]]

    shellout = shellwrappers.sendtossh(job, cmd)

    # Find job id.
    try:

        # Split the shell output down to a list of lines.
        lines = shellout[0].split('\n')

        # Find line with keyword "submitted".
        for line in lines:

            if "submitted" in line:

                jobidline = line
                break

        jobid = re.search(r'\d+', jobidline).group()

    except AttributeError:

        raise exceptions.JobsubmitError(
            "Could not detect the job id during submission, this means that "
            "either the submission failed in an unexpected way, or that "
            "Longbow could not understand the returned information.")

    # Put jobid into the job dictionary.
    job["jobid"] = jobid
