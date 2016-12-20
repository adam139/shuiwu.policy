# -*- coding: utf-8 -*-
from plone import api
from Products.CMFCore.utils import getToolByName
import datetime
from shuiwu.baoshui.content.nashuiren import Inashuiren
from shuiwu.baoshui.content.niandu import Iniandu
from shuiwu.baoshui.subscriber import subids


def createChildTree(context):
    "for nashuiren create sub-child-tree"
    #search all nashuiren objects that have not sub object
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Inashuiren.__identifier__}
    bns = pc(query)
    bns = filter(everypathsearchFilter,bns)
    if len(bns) > 5000:
        bns = bns[:4999]    
    finishlist = map(map_build_subtree,bns)
        
def getTargetobj(context,objid):
    "get target nashuiren object that has been created sub tree by object id"
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Inashuiren.__identifier__,'id':objid}
    bns = pc(query)
    return bns[0].getObject()
        
def mapf(brain):
    "copy & paster sub tree for the brain"

    target = brain.getObject()
    source = getTargetobj(target,"43062519700816052X01")       
    for subid,subtype,title,num in subids:
        subobj = source[subid]
        api.content.copy(source=subobj, target=target)

def map_build_subtree(brain):
    "create new niandu subtree"
    obj = brain.getObject()
    target = api.content.create(
#     id = datetime.datetime.today().strftime("%Y"),
    id = '2017',
    type='shuiwu.baoshui.niandu',
    title=u'%s年度记录' % id,
    container=obj)
    status = obj.status
    description = obj.description
    shuiguanyuan = obj.shuiguanyuan
    init_tags = []
    if status != "":
        group = tagroup[0].encode("utf-8")
        tag = "%s-%s" %(group,status)
        init_tags.append(tag)
    if description != "":
        group = tagroup[1].encode("utf-8")
        tag = "%s-%s" %(group,description)
        init_tags.append(tag)
    if shuiguanyuan != "":
        group = tagroup[2].encode("utf-8")
        tag = "%s-%s" %(group,shuiguanyuan)
        init_tags.append(tag)
    subjects = yuedu_subjects + jidu_subjects + ling_subjects + init_tags   
    obj.setSubject(tuple(subjects))                        
    obj.reindexObject()
   # Put the tasks into the queue as a tuple
    for subid,title in subids:
        title = title.encode('utf-8')
        type="shuiwu.baoshui.%s" % subid
        directory = api.content.create(type=type,id=subid,title=title,container=target)    

def pathsearchFilter(brain):
    "search the specify brain, path of the brain,if the path has sub-object,return True" 
    context = brain.getObject()
    pc = getToolByName(context, "portal_catalog")
    query = {"path":"/".join(context.getPhysicalPath())}
    bns = pc(query)
    if len(bns) <= 1:
        return True
    else:
        return False

def everypathsearchFilter(brain):
    "search the specify brain, path of the brain,if the path has sub-object,return True" 
    context = brain.getObject()
    pc = getToolByName(context, "portal_catalog")
    query = {"path":"/".join(context.getPhysicalPath())}
#     id = datetime.datetime.today().strftime("%Y")
    query['id'] = '2017'
    bns = pc(query)
    if len(bns) < 1:
        return True
    else:
        return False    
def notexistsearchFilter(brain):
    "if not exist niandu object,return True,else return False"
    context = brain.getObject()
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Iniandu.__identifier__}
#     query['object_provides'] = Iniandu.__identifier__
    query["path"] = "/".join(context.getPhysicalPath())
    bns = pc(query)
    if len(bns) < 1:
        return True
    else:
        return False
    
def notmoveFilter(brain):
    "if not exist niandu object,return True,else return False"
    context = brain.getObject()
    bns = api.content.find(context=context,depth=1)
    if len(bns) > 1:
        return True
    else:
        return False
        
def appendNianduContainer(context): 
    "niandu object append to nashuiren container"
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Inashuiren.__identifier__}
    bns = pc(query)

    bns = filter(notmoveFilter,bns)
    if len(bns) > 100:
        bns = bns[:99]    
    finishlist = map(mapc,bns)              

def mapc(brain):
    "new create niandu container and move nashuiren's children to it"

    obj = brain.getObject()
    id = datetime.datetime.today().strftime("%Y")    
#     target = api.content.create(
#     id = id
#     type='shuiwu.baoshui.niandu',
#     title=u'年度记录',
#     container=target)
          
    target = obj[id]   
    subbrains = api.content.find(context=obj,depth=1)

    for subbrain in subbrains:
        if subbrain.id == id: continue
        subobj = subbrain.getObject()
        api.content.move(source=subobj, target=target)        

# reset guishu keshi
model = u'湖南省湘潭高新技术产业开发区地方税务局'.encode('utf-8')
def resetDescription(context):
    "湖南省湘潭高新技术产业开发区地方税务局税源管理三科 change to 税源管理三科"
    
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Inashuiren.__identifier__}
    bns = pc(query)
#     import pdb
#     pdb.set_trace()
    bns = filter(zipFilter,bns)
#     if len(bns) > 5:
#         bns = bns[:4]    
    finishlist = map(mapf,bns)      
        
def zipFilter(brain):
    "if description field  exist '湖南省湘潭高新技术产业开发区地方税务局' ,return True,else return False"
    des = brain.Description
    if isinstance(des, unicode):
        des = des.encode('utf-8')
    if model in des:
        return True
    else:
        return False        

def mapf(brain):
    "replace"

    target = brain.getObject()
    des = target.description
    if isinstance(des, unicode):
        des = des.encode('utf-8')
    newd = des.replace(model,'')
    target.description = newd
    target.reindexObject(idxs=['description'])
  
    
    


