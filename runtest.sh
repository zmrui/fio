#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /kernel/general/scheduler/sched_fio_benchmark.
#   Description: test desk performance fio
#   Author: Mingrui Zhang <mizhang@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2019 Red Hat, Inc.
#
#   This program is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 2 of
#   the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see http://www.gnu.org/licenses/.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Include Beaker environment
. /usr/bin/rhts-environment.sh || exit 1
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGE="sched_fio_benchmark"
export BASELINE=${BASELINE:-$(uname -r | sed 's/\.'$(uname -m)'//')}
export TARGET=${TARGET:-$(uname -r | sed 's/\.'$(uname -m)'//')}
nvr=$(uname -r | sed 's/\.'$(uname -m)'//')
#BASELINE and TARGET parameters are default to be current kernel nvr
#
#  If not given certain BASELINE and TARGET parameters, this script
#  will only run fio test under current system enviroment.
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Explaination:
#  If only run test (most likely when current task is the
#  initial of all tasks sequence) not provide any parameters,
#  or set BASELINE and TARGET as same
#   For example:
#    Only run test. No set parameters
#    # ./runtest.sh
#
#  If the purpose is run test and compare to previous result
#  then must give nvr as parameter for the object to compare,
#  no matter current task is baseline or target.
#   For example:
#    If current kernel version is 4.18.0-80.el8
#    and tests on 3.10.0-1062.el7 have just finished. Then
#    compare current test with previous result,
#    3.10.0-1062.el7 is baseline, 4.18.0-80.el8 is target.
#    Set BASELINE=3.10.0-1062.el7  , then it would like
#    # BASELINE=3.10.0-1062.el7 ./runtest.sh
#
#    If current kernel version is 3.10.0-1062.el7
#    and tests on 4.18.0-80.el8 have just finished. Then
#    compare current test with previous result,
#    3.10.0-1062.el7 is baseline, 4.18.0-80.el8 is target.
#    Set TARGET=4.18.0-80.el8 , then it would like
#    # TARGET=4.18.0-80.el8 ./runtest.sh

rlJournalStart
    rlPhaseStartTest
        yum install -y fio
	    if rlIsRHEL ">=8";
        then
            rlRun "/usr/libexec/platform-python fio.py" 0 "Run fio test"
        else
            rlRun "python fio.py" 0 "Run fio test"
        fi
        rlLogInfo "Test raw log stored to http://vmcore.usersys.redhat.com/kgqe/scheduler/fio/${HOSTNAME}/${nvr}/fioresult , if succesed."
        rlFileSubmit  "/home/fioresult/output.log" "output.log"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
