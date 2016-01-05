# pylint: disable=too-many-public-methods
"""Test for letsencrypt_nginx.configurator."""
import os
import shutil
import unittest

import mock
import OpenSSL

from acme import challenges
from acme import messages

from letsencrypt import achallenges
from letsencrypt import errors

from letsencrypt_nginx.tests import util

class NginxConfiguratorUbuntuTest(util.NginxTest):
    """Test a semi complex vhost configuration."""

    DATA_DIR = "ubuntu_nginx_1_9_3"

    def setUp(self):
        super(NginxConfiguratorUbuntuTest, self).setUp(self.DATA_DIR)

        self.config = util.get_nginx_configurator(
            self.config_path, self.config_dir, self.work_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        shutil.rmtree(self.config_dir)
        shutil.rmtree(self.work_dir)

    def test_choose_vhost_auto_detects_conf_dir(self):
        conf_path = {'new.com': os.path.join(self.DATA_DIR, "sites-enabled/new.com.conf"),
                   'example.com': os.path.join(self.DATA_DIR, "sites-enabled/existing")}

        for name in conf_path:
            vhost = self.config.choose_vhost(name)
            path = os.path.relpath(vhost.filep, self.temp_dir)

            self.assertEqual(set([name]), vhost.names)
            self.assertEqual(conf_path[name], path)

if __name__ == "__main__":
    unittest.main()  # pragma: no cover
