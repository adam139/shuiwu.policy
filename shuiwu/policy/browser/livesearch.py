# -*- coding: utf-8 -*-
from shuiwu.baoshui.content.nashuiku import Inashuiku
from shuiwu.baoshui.content.nashuiren import Inashuiren
from Products.CMFPlone.browser.search import MULTISPACE,BAD_CHARS,quote_chars
from Products.CMFPlone.browser.search import AjaxSearch
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFPlone.browser.navtree import getNavigationRoot
from Products.ZCTextIndex.ParseTree import ParseError
from ZTUtils import make_query
from plone.app.contentlisting.interfaces import IContentListing
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from zope.publisher.browser import BrowserView

import json

_ = MessageFactory('plone')


class NashuirenAjaxSearch(AjaxSearch):
    
    def getPathQuery(self): 
        """返回 纳税人库目录查询条件
        """
        query = {'path':self.getDBFolder()}               
        return query         
        
# roll table output
    def getDBFolder(self):
        
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({'object_provides':Inashuiku.__identifier__})
        path = brains[0].getPath()
        return path
    
    def filter_query(self, query):
        request = self.request
        text = query.get('SearchableText', None)
        if text is None:
            text = request.form.get('SearchableText', '')
        if not text:
            # Without text, must provide a meaningful non-empty search
            return

        #nashuiren_searchable_query = {}
        nquery = self.getPathQuery()
        if text:
            nquery['SearchableText'] = self.munge_search_term(text)
        nquery['object_provides'] = Inashuiren.__identifier__
        return nquery





