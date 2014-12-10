"""Unit tests for jujulocal.images"""

import unittest

from mock import patch

from jujulocal.images import (
    parse_cloudimg,
    cloud_images,
)


LXC_CACHE = '/var/cache/lxc'


class ImagesParseCloudimgTest(unittest.TestCase):
    def test_parse(self):
        good = [('ubuntu-14.04-server-cloudimg-amd64-root.tar.gz',
                 'ubuntu', '14.04', 'amd64'),
                ('ubuntu-13.10-server-cloudimg-i386.tar.gz',
                 'ubuntu', '13.10', 'i386'),
                ('ubuntu-12.04-server-cloudimg-ppc64le-root.tar.gz',
                 'ubuntu', '12.04', 'ppc64le'),
                ]
        ugly = [('tmp.dSjGPYEmjo', None, None, None)]

        for t in good:
            self.assertEqual(t[1:], parse_cloudimg(t[0]))

        for t in ugly:
            self.assertEqual(t[1:], parse_cloudimg(t[0]))


class ImagesCloudImagesTest(unittest.TestCase):
    @patch('jujulocal.images.sudo')
    def test_cloud_images(self, ms):
        from datetime import datetime
        fp = ('%s/%s/ubuntu-14.04-server-cloudimg-amd64-root.tar.gz' %
              ('cloud-trusty', LXC_CACHE))
        ms.side_effect = ['cloud-trusty\nsaucy',
                          '1417740800 185796025 %s' % fp,
                          '1417740800 185796025 %s' % fp,
                          ]
        self.assertEqual([{'modified': datetime.fromtimestamp(1417740800),
                           'size': '185796025',
                           'path': fp,
                           'arch': 'amd64',
                           'series': '14.04',
                           'distro': 'ubuntu',
                           }], cloud_images())
