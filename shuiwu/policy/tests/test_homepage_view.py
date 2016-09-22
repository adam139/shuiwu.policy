#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
 
from shuiwu.policy.testing import FunctionalTesting
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest

import os
from shuiwu.baoshui.tests.test_contents import InitContents

class TestView(InitContents):
    
    layer = FunctionalTesting

    
    def test_homepage_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal.absolute_url() + '/@@index.html'        

        browser.open(obj)
 
        outstr = u"nashuiren1"
        
        self.assertTrue(outstr in browser.contents)          
        
   