# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

from twisted.internet import defer
from twisted.trial import unittest

from buildbot.schedulers import timed
from buildbot.test.reactor import TestReactorMixin
from buildbot.test.util import scheduler


class Timed(scheduler.SchedulerMixin, TestReactorMixin, unittest.TestCase):
    OBJECTID = 928754

    @defer.inlineCallbacks
    def setUp(self):
        self.setup_test_reactor()
        yield self.setUpScheduler()

    class Subclass(timed.Timed):
        def getNextBuildTime(self, lastActuation):
            self.got_lastActuation = lastActuation
            return defer.succeed((lastActuation or 1000) + 60)

        def startBuild(self):
            self.started_build = True
            return defer.succeed(None)

    @defer.inlineCallbacks
    def makeScheduler(self, firstBuildDuration=0, **kwargs):
        sched = yield self.attachScheduler(self.Subclass(**kwargs), self.OBJECTID)
        return sched

    # tests

    # note that most of the heavy-lifting for testing this class is handled by
    # the subclasses' tests, as that's the more natural place for it
