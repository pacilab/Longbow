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

"""This is the dl_poly plugin module.

This plugin is relatively simple in the fact that adding new executables is as
simple as modifying the EXECDATA structure below. See the documentation at
http://www.hecbiosim.ac.uk/longbow-devdocs for more information.
"""

import os
import longbow.exceptions as exceptions

EXECDATA = {
    "DLPOLY.Z": {
        "subexecutables": [],
        "requiredfiles": ["CONFIG", "CONTROL", "FIELD"],
    }
}


def cmdlinevalidator(job):
    """"""
    filelist = []
    requiredfiles = ["CONFIG", "CONTROL", "FIELD"]
    optionalfiles = ["TABLE", "TABEAM", "REFERENCE"]

    for rep in range(1, int(job["replicates"]) + 1):

        if int(job["replicates"]) == 1:

            filepath = job["localworkdir"]

        else:

            repx = str(job["replicate-naming"]) + str(rep)
            filepath = os.path.join(job["localworkdir"], repx)

        # Check for required files and fail if missing.
        for item in requiredfiles:

            if os.path.isfile(os.path.join(filepath, item)):

                filelist.append(item)

            else:

                raise exceptions.RequiredinputError(
                    "In job '{0}' the following file '{1}' as input to the "
                    "application '{2}' is missing"
                    .format(job["jobname"],
                            os.path.join(filepath, item),
                            "DL_POLY"))

        # Check for any optional files.
        for item in optionalfiles:

            if os.path.isfile(os.path.join(filepath, item)):

                filelist.append(item)

    return filelist
