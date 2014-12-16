"""Unit tests for jujulocal.suspend"""

import unittest

from mock import patch

from jujulocal.suspend import (
    suspend,
    resume,
)
