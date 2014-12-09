"""Unit tests for jujulocal.helper"""

import errno
import unittest

from mock import patch, MagicMock

from jujulocal.helpers import (
    do,
    sudo,
)


def mock_popen(ret, err=None, retcode=0):
    mPopen = MagicMock()
    mpr = mPopen.return_value
    mpr.communicate.return_value = (ret.encode(), err.encode() if err else None)
    mpr.returncode = retcode

    return mPopen

class HelpersDoTest(unittest.TestCase):
    @patch('jujulocal.helpers.subprocess')
    def test_do(self, ms):
        ms.Popen = mock_popen('user')

        self.assertEqual('user', do(['whoami']))

    @patch('jujulocal.helpers.subprocess')
    def test_do_str(self, ms):
        ms.Popen = mock_popen('user')

        self.assertEqual('user', do('whoami'))

    @patch('jujulocal.helpers.subprocess')
    def test_do_no_cmd(self, ms):
        ms.Popen.side_effect = OSError(errno.ENOENT, 'No such file or directory',
                                       'not-a-cmd')

        self.assertRaises(OSError, do, ['not-a-cmd'])

    @patch('jujulocal.helpers.subprocess')
    def test_do_called_right(self, ms):
        ms.Popen = mock_popen('ubuntu')

        self.assertEqual('ubuntu', do('whoami', env={'HOME': 'heartis'}))
        ms.Popen.assert_called_with(['whoami'], env={'HOME': 'heartis'},
                                    stdout=ms.PIPE, stderr=ms.PIPE)

    @patch('jujulocal.helpers.subprocess')
    def test_do_su(self, ms):
        ms.Popen = mock_popen('root')

        self.assertEqual('root', do('whoami', su=True))
        ms.Popen.assert_called_with(['sudo', 'whoami'], env=None, stdout=ms.PIPE,
                                    stderr=ms.PIPE)

    @patch('jujulocal.helpers.subprocess')
    def test_do_err(self, ms):
        ms.Popen = mock_popen('bzt', 'Failed to run command!', 1)

        self.assertRaises(IOError, do, 'whoami --param?')


class HelpersSudoTest(unittest.TestCase):
    @patch('jujulocal.helpers.do')
    def test_sudo(self, md):
        md.return_value = 'root'

        self.assertEqual('root', sudo('whoami'))
        md.assert_called_with('whoami', env=None, su=True)

    @patch('jujulocal.helpers.do')
    def test_sudo_env(self, md):
        md.return_value = 'root'

        self.assertEqual('root', sudo('whoami', env={'HOME': '127.0.0.1'}))
        md.assert_called_with('whoami', env={'HOME': '127.0.0.1'}, su=True)
