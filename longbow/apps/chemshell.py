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

EXECDATA = {
    "chemsh.x": {
        "subexecutables": [],
        "requiredfiles": ["<"],
    }
}


def rsyncuploadhook(jobs, job):
    '''Override the default rsync upload parameters to null so that rsync
    basically transfers all files'''

    jobs[job]["upload-include"] = ""
    jobs[job]["upload-exclude"] = "log, *.log"


def scripthook(jobs, job):

    '''Add some lines that will get incorporated into the job submit script
    to save having to introduce a complex dependency chain for plugins.'''

    if jobs[job]["scripts"] == "":

        jobs[job]["scripts"] = "module use ~/.mymodules, module load chemshell"

    else:

        jobs[job]["scripts"] = (jobs[job]["scripts"] + ", module use "
                                "~/.mymodules, module load chemshell")
