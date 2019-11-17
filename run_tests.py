# -*- coding: utf-8 -*-
import sys
import unittest

from tests import CloudFileAccessTest, CloudFolderTest, OperationsTest

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(CloudFolderTest),
        unittest.makeSuite(CloudFileAccessTest),
        unittest.makeSuite(OperationsTest),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
