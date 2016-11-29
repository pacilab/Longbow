# Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B Shannon 2015.
#
# This file is part of the Longbow software which was developed as part of the
# HECBioSim project (http://www.hecbiosim.ac.uk/).
#
# HECBioSim facilitates and supports high-end computing within the UK
# biomolecular simulation community on resources such as ARCHER.
#
# Longbow is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 2 of the License, or (at your option) any later
# version.
#
# Longbow is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Longbow.  If not, see <http://www.gnu.org/licenses/>.

"""
This test module contains tests for the SGE scheduler plugin.
"""

import os
import Longbow.schedulers.sge as sge


def test_prepare_case1():

    """
    Simple test
    """

    job = {
        "account": "",
        "cluster": "",
        "cores": "24",
        "corespernode": "",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "mpirun",
        "email-address": "",
        "email-flags": "",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "",
        "modules": "amber",
        "queue": "debug",
        "replicates": "1",
        "scripts": "",
        "sge-peflag": "mpi",
        "sge-peoverride": "false",
        "upload-include": "file1, file2"
    }

    sge.prepare(job)

    assert job["subfile"] == "submit.sge"
    assert job["upload-include"] == "file1, file2, submit.sge"
    assert open("/tmp/submit.sge", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "Tests/standards/sge_submitfiles/testcase1.txt"), "rb").read()


def test_prepare_case2():

    """
    Test replicates
    """

    job = {
        "account": "",
        "cluster": "",
        "cores": "24",
        "corespernode": "",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "mpirun",
        "email-address": "",
        "email-flags": "",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "",
        "modules": "amber",
        "queue": "debug",
        "replicates": "5",
        "scripts": "",
        "sge-peflag": "mpi",
        "sge-peoverride": "false",
        "upload-include": "file1, file2"
    }

    sge.prepare(job)

    assert open("/tmp/submit.sge", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "Tests/standards/sge_submitfiles/testcase2.txt"), "rb").read()


def test_prepare_case3():

    """
    Test account parameter
    """

    job = {
        "account": "accno1234",
        "accountflag": "",
        "cluster": "",
        "cores": "24",
        "corespernode": "",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "mpirun",
        "email-address": "",
        "email-flags": "",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "",
        "modules": "amber",
        "queue": "debug",
        "replicates": "1",
        "scripts": "",
        "sge-peflag": "mpi",
        "sge-peoverride": "false",
        "upload-include": "file1, file2"
    }

    sge.prepare(job)

    assert open("/tmp/submit.sge", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "Tests/standards/sge_submitfiles/testcase3.txt"), "rb").read()


def test_prepare_case4():

    """
    Test account parameter
    """

    job = {
        "account": "accno1234",
        "accountflag": "-P",
        "cluster": "",
        "cores": "24",
        "corespernode": "",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "mpirun",
        "email-address": "",
        "email-flags": "",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "",
        "modules": "amber",
        "queue": "debug",
        "replicates": "1",
        "scripts": "",
        "sge-peflag": "mpi",
        "sge-peoverride": "false",
        "upload-include": "file1, file2"
    }

    sge.prepare(job)

    assert open("/tmp/submit.sge", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "Tests/standards/sge_submitfiles/testcase4.txt"), "rb").read()


def test_prepare_case5():

    """
    Test email parameters
    """

    job = {
        "account": "",
        "accountflag": "",
        "cluster": "",
        "cores": "24",
        "corespernode": "",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "mpirun",
        "email-address": "test.email@server.com",
        "email-flags": "bn",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "",
        "modules": "amber",
        "queue": "debug",
        "replicates": "1",
        "scripts": "",
        "sge-peflag": "mpi",
        "sge-peoverride": "false",
        "upload-include": "file1, file2"
    }

    sge.prepare(job)

    assert open("/tmp/submit.sge", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "Tests/standards/sge_submitfiles/testcase5.txt"), "rb").read()


def test_prepare_case6():

    """
    Test script parameters
    """

    job = {
        "account": "",
        "accountflag": "",
        "cluster": "",
        "cores": "24",
        "corespernode": "",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "mpirun",
        "email-address": "",
        "email-flags": "",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "",
        "modules": "amber",
        "queue": "debug",
        "replicates": "1",
        "scripts": "ls /dir, cd /dir",
        "sge-peflag": "mpi",
        "sge-peoverride": "false",
        "upload-include": "file1, file2"
    }

    sge.prepare(job)

    assert open("/tmp/submit.sge", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "Tests/standards/sge_submitfiles/testcase6.txt"), "rb").read()


def test_prepare_case7():

    """
    Test single core parameter for GPU
    """

    job = {
        "account": "",
        "accountflag": "",
        "cluster": "",
        "cores": "1",
        "corespernode": "",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "mpiexec",
        "email-address": "",
        "email-flags": "",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "",
        "modules": "amber",
        "queue": "debug",
        "replicates": "1",
        "scripts": "",
        "sge-peflag": "mpi",
        "sge-peoverride": "false",
        "upload-include": "file1, file2"
    }

    sge.prepare(job)

    assert open("/tmp/submit.sge", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "Tests/standards/sge_submitfiles/testcase7.txt"), "rb").read()
