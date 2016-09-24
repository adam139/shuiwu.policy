# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from zope.lifecycleevent import ObjectModifiedEvent
from plone import api
from plone.app.dexterity.behaviors import constrains
from logging import getLogger
from Products.CMFCore.utils import getToolByName
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
import datetime

logger = getLogger(__name__)

def setupGroups(portal):
    acl_users = getToolByName(portal, 'acl_users')
    if not acl_users.searchGroups(name='Shuiguanyuan'):
        gtool = getToolByName(portal, 'portal_groups')
        gtool.addGroup('Shuiguanyuan', roles=['ShuiguanyuanMember'])
        
STRUCTURE = [
    {
        'type': 'shuiwu.baoshui.nashuiku',
        'title': u'纳税人信息库',
        'id': 'nashuirenku',
        'description': u'纳税人税务申报信息登记库',
        'layout': 'sysajax_listings',
        'children': [

                     {
            'type': 'shuiwu.baoshui.nashuiren',
            'id': 'nashuiren1',            
            'title': u'纳税人1',
            'description': u'一科',            
            'guanlidaima':'888201',
            'shuiguanyuan':'税管员1',
            'danganbianhao':'1001',
            'dengjiriqi':datetime.datetime.today(),
            'layout': 'nashuiren_view',
                      },
                     {
            'type': 'shuiwu.baoshui.nashuiren',
            'id': 'nashuiren3',            
            'title': u'纳税人3',
            'description': u'一科',            
            'guanlidaima':'888203',
            'shuiguanyuan':'税管员3',
            'danganbianhao':'1003',
            'dengjiriqi':datetime.datetime.today(),
            'layout': 'nashuiren_view',
                      },
                     {
            'type': 'shuiwu.baoshui.nashuiren',
            'id': 'nashuiren4',            
            'title': u'纳税人4',
            'description': u'一科',            
            'guanlidaima':'888204',
            'shuiguanyuan':'税管员4',
            'danganbianhao':'1004',
            'dengjiriqi':datetime.datetime.today(),
            'layout': 'nashuiren_view',
                      },
                     {
            'type': 'shuiwu.baoshui.nashuiren',
            'id': 'nashuiren5',            
            'title': u'纳税人5',
            'description': u'一科',            
            'guanlidaima':'888205',
            'shuiguanyuan':'税管员1',
            'danganbianhao':'1005',
            'dengjiriqi':datetime.datetime.today(),
            'layout': 'nashuiren_view',
                      },
                     {
            'type': 'shuiwu.baoshui.nashuiren',
            'id': 'nashuiren9',            
            'title': u'纳税人9',
            'description': u'二科',            
            'guanlidaima':'888209',
            'shuiguanyuan':'税管员2',
            'danganbianhao':'1009',
            'dengjiriqi':datetime.datetime.today(),
            'layout': 'nashuiren_view',
                      }                                                                                                                                                              
                ]
    }
             
]


def isNotCurrentProfile(context):
    return context.readDataFile('shuiwupolicy_marker.txt') is None


def post_install(context):
    """Setuphandler for the profile 'default'
    """
    if isNotCurrentProfile(context):
        return
    # Do something during the installation of this package
#     return
    portal = api.portal.get()
    members = portal.get('events', None)
    if members is not None:
        api.content.delete(members)
    members = portal.get('news', None)
    if members is not None:
        api.content.delete(members)
    members = portal.get('Members', None)
    if members is not None:
       members.exclude_from_nav = True
       members.reindexObject()
   

    for item in STRUCTURE:
        _create_content(item, portal)
#     add group
    setupGroups(portal)

             
                


def content(context):
    """Setuphandler for the profile 'content'
    """
    if context.readDataFile('shuiwupolicy_content_marker.txt') is None:
        return
    pass



def _create_content(item, container):
    new = container.get(item['id'], None)
    if not new:
        new = api.content.create(
            type=item['type'],
            container=container,
            title=item['title'],
            description=item['description'],           
            id=item['id'],
            safe_id=False)
        logger.info('Created item {}'.format(new.absolute_url()))
    if item.get('dengjiriqi', False):
        new.dengjiriqi = item['dengjiriqi']
    if item.get('layout', False):
        new.setLayout(item['layout'])
    if item.get('default-page', False):
        new.setDefaultPage(item['default-page'])
    if item.get('allowed_types', False):
        _constrain(new, item['allowed_types'])
    if item.get('local_roles', False):
        for local_role in item['local_roles']:
            api.group.grant_roles(
                groupname=local_role['group'],
                roles=local_role['roles'],
                obj=new)
    if item.get('publish', False):
        api.content.transition(new, to_state=item.get('state', 'published'))
    new.reindexObject()
    # call recursively for children
    for subitem in item.get('children', []):
        _create_content(subitem, new)


def _constrain(context, allowed_types):
    behavior = ISelectableConstrainTypes(context)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setLocallyAllowedTypes(allowed_types)
    behavior.setImmediatelyAddableTypes(allowed_types)
