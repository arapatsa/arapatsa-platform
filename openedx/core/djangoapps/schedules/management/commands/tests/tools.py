import datetime

from edx_ace.utils.date import serialize
from mock import patch
import pytz

from courseware.models import DynamicUpgradeDeadlineConfiguration
from openedx.core.djangolib.testing.utils import CacheIsolationTestCase, FilteredQueryCountMixin
from openedx.core.djangoapps.site_configuration.tests.factories import SiteConfigurationFactory, SiteFactory
from openedx.core.djangoapps.schedules import tasks
from openedx.core.djangoapps.schedules.tests.factories import ScheduleConfigFactory



class ScheduleBaseEmailTestBase(FilteredQueryCountMixin, CacheIsolationTestCase):

    __test__ = False

    ENABLED_CACHES = ['default']

    def setUp(self):
        super(ScheduleBaseEmailTestBase, self).setUp()

        site = SiteFactory.create()
        self.site_config = SiteConfigurationFactory.create(site=site)
        ScheduleConfigFactory.create(site=self.site_config.site)

        DynamicUpgradeDeadlineConfiguration.objects.create(enabled=True)

    def test_command_task_binding(self):
        self.assertEqual(self.tested_command.async_send_task, self.tested_task)

    def test_handle(self):
        with patch.object(self.tested_command, 'async_send_task') as mock_send:
            test_day = datetime.datetime(2017, 8, 1, tzinfo=pytz.UTC)
            self.tested_command().handle(date='2017-08-01', site_domain_name=self.site_config.site.domain)

            for offset in self.expected_offsets:
                mock_send.enqueue.assert_any_call(
                    self.site_config.site,
                    test_day,
                    offset,
                    None
                )

    @patch.object(tasks, 'ace')
    def test_resolver_send(self, mock_ace):
        current_day = datetime.datetime(2017, 8, 1, tzinfo=pytz.UTC)
        offset = self.expected_offsets[0]
        target_day = current_day + datetime.timedelta(days=offset)

        with patch.object(self.tested_task, 'apply_async') as mock_apply_async:
            self.tested_task.enqueue(self.site_config.site, current_day, offset)
            mock_apply_async.assert_any_call(
                (self.site_config.site.id, serialize(target_day), offset, 0, None),
                retry=False,
            )
            mock_apply_async.assert_any_call(
                (self.site_config.site.id, serialize(target_day), offset, self.tested_task.num_bins - 1, None),
                retry=False,
            )
            self.assertFalse(mock_ace.send.called)
