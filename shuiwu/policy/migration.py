# -*- coding: utf-8 -*-
from plone import api
from Products.CMFCore.utils import getToolByName
import datetime
from shuiwu.baoshui.content.nashuiren import Inashuiren
from shuiwu.baoshui.content.niandu import Iniandu
from shuiwu.baoshui.subscriber import subids
from shuiwu.baoshui.subscriber import getout,tagroup,yuedu_subjects,jidu_subjects,ling_subjects
## start 內资个体设置默认视图
def nashuiren_set_defaultview(context):
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Inashuiren.__identifier__}
    bns = pc(query)
    bns = filter(nashuiren_is_geti,bns)
    finished = map(setlayout,bns) 
def nashuiren_is_geti(brain):
    "brain is nashuiren brain"
    if brain.regtype ==  getout[0].encode('utf-8'):
        return True
    else:
        return False

def setlayout(brain):
    obj = brain.getObject()
    obj.setLayout("view")
## end 內资个体设置默认视图
def findid_noteq_guanlidaima(context):
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Inashuiren.__identifier__}
    bns = pc(query)
    bns = [bn.id for bn in bns if bns.id != bns.guanlidaima]   

def build_index_nashuiren(context):
    "for nashuiren rebuild indexs"
    #search all nashuiren objects that have not sub object
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Inashuiren.__identifier__}
    bns = pc(query)
    finished = map(rebuild_index,bns)

##start迁移年度记录下面的子对象到纳税人对象（父对象）
def migrateback2nashuiren(context):
    "for nashuiren rebuild indexs"
    #search all nashuiren objects that have not sub object
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Iniandu.__identifier__}
    bns = pc(query)
    finished = map(rebuild_index,bns)

##end 迁移年度记录下面的子对象到纳税人对象（父对象）
## start update empty subject to init subject for nashuiren
def init_subjectfornashuiren(context):
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Inashuiren.__identifier__}
#     query["Subject"] = tuple()
    bns = pc(query)
    bns = filter(nashuiren_is_empty_subject,bns)
    import pdb
    pdb.set_trace()
    finished = map(init_subject,bns) 
def nashuiren_is_empty_subject(brain):
    "brain is nashuiren brain"
    if brain.regtype ==  getout[0].encode('utf-8'):return False
    if len(brain.Subject) < 1:
        return True
    else:
        return False
def init_subject(brain):
    "migrate brain's subject to sub-niandu object"
    obj = brain.getObject()
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
    obj.reindexObject(idxs=["Subject"])
## end update empty subject to init subject for nashuiren    
def migratesubject2niandu(context):
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Inashuiren.__identifier__}
    bns = pc(query)
    bns = filter(niandu_is_empty_subject,bns)
    finished = map(migrate_subject,bns)    
        
def niandu_is_empty_subject(brain):
    "brain is nashuiren brain"
    if len(brain.Subject) > 1:
        return True
    else:
        return False
    
def migrate_subject(brain):
    "migrate brain's subject to sub-niandu object"
    subjects = brain.Subject
    nashuiren = brain.getObject()
    son = nashuiren['2016']
    son.setSubject(tuple(subjects))
    nashuiren.setSubject(tuple())                        
    son.reindexObject(idxs=["Subject"])    

def rebuild_index(brain):
    obj = brain.getObject()
    obj.reindexObject(idxs=["Subject","Title","Description","status","regtype","shuiguanyuan",
                            "caiwufuzeren","caiwufuzerendianhua","banshuiren","banshuirendianhua",
                            "guanlidaima","dengjiriqi"])      

def createChildTree(context):
    "for nashuiren create sub-child-tree"
    #search all nashuiren objects that have not sub object
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Inashuiren.__identifier__}
    bns = pc(query)
    bns = filter(everypathsearchFilter,bns)
    if len(bns) > 2000:
        bns = bns[:1999]     
#     bns = map(map_build_subtree,gen_everypathsearchFilter(bns))   
    finishlist = map(map_build_subtree,bns)
        
def getTargetobj(context,objid):
    "get target nashuiren object that has been created sub tree by object id"
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Inashuiren.__identifier__,'id':objid}
    bns = pc(query)
    return bns[0].getObject()
      
def map_build_subtree(brain):
    "create new niandu subtree"
    obj = brain.getObject()
    id = '2017'
    target = api.content.create(
#     id = datetime.datetime.today().strftime("%Y"),
    id = id,
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
    target.setSubject(tuple(subjects))                        
    target.reindexObject(idxs=["Subject"])
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
def gen_everypathsearchFilter(brains):
    "search the specify brain, path of the brain,if the path has sub-object,return True" 
    for brain in brains:
        context = brain.getObject()
        pc = getToolByName(context, "portal_catalog")
        query = {"path":"/".join(context.getPhysicalPath())}
        #     id = datetime.datetime.today().strftime("%Y")
        query['id'] = '2017'
        bns = pc(query)
        if len(bns) < 1:
            yield context
        else:
            continue 

def everypathsearchFilter(brain):
    "search the specify brain, path of the brain,if the path has sub-object,return True" 
    if brain.regtype ==  getout[0].encode('utf-8'):return False
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
    if brain.regtype ==  getout[0].encode('utf-8'):return False
    context = brain.getObject()
    bns = api.content.find(context=context,depth=1)
    if len(bns) > 1:
        return True
    else:
        return False
 

## start migrate subobj to niandu            
def appendNianduContainer(context): 
    "niandu object append to nashuiren container"
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Inashuiren.__identifier__}
    bns = pc(query)
    bns = filter(notmoveFilter,bns)
    if len(bns) > 1400:
        bns = bns[:699]
    bns = map(mapc,bns)
#     bngenerator = generator_notmoveFilter(bns)    
#     import pdb
#     pdb.set_trace()  
#     for gen in bngenerator:
#         map4obj(gen)

def appendNianduContainer2(context): 
    "niandu object append to nashuiren container"
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Inashuiren.__identifier__}
    bns = pc(query)
    bns = filter(notmoveFilter,bns)
    if len(bns) > 1200:
        bns = bns[700:]
#     bns = map(mapc,filter(notmoveFilter,bns))
    bngenerator = generator_notmoveFilter(bns)    
#     import pdb
#     pdb.set_trace()  
    for gen in bngenerator:
        map4obj(gen)
                     
def generator_notmoveFilter(brains):
    "if not exist niandu object,return True,else return False"
    for brain in brains:
        context = brain.getObject()
        bns = api.content.find(context=context,depth=1)
        if len(bns) > 1:
            yield context
        else:
            continue
def map4obj(obj):
    "new create niandu container and move nashuiren's children to it"    
#     id = datetime.datetime.today().strftime("%Y")
    id = '2016'
    try:
        target = obj[id]
    except:        
        target = api.content.create(
                                    id = id,
                                    type='shuiwu.baoshui.niandu',
                                    title=u'年度记录',
                                    container=obj)          
   
    subbrains = api.content.find(context=obj,depth=1)
    subgenerator = subobj_generator(subbrains,id)
#     import pdb
#     pdb.set_trace()
    for subobj in subgenerator:
        api.content.move(source=subobj, target=target) 
def subobj_generator(brains,id):
    for bn in brains:
        if bn.id == id: continue
        yield bn.getObject()       
    
## end migrate subobj to niandu container


def mapc(brain):
    "new create niandu container and move nashuiren's children to it"

    obj = brain.getObject()
#     id = datetime.datetime.today().strftime("%Y")
    id = '2016'    
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
  
# reset title for niandu
modelid = "%s" % id
def resetTitle(context):
    "湖南省湘潭高新技术产业开发区地方税务局税源管理三科 change to 税源管理三科"
    
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Iniandu.__identifier__}
    bns = pc(query)

    bns = filter(idFilter,bns)
#     if len(bns) > 5:
#         bns = bns[:4]    
    finishlist = map(maptitle,bns)      
        
def idFilter(brain):
    "if title field  exist '<built-in function id>' ,return True,else return False"
    des = brain.Title
    if isinstance(des, unicode):
        des = des.encode('utf-8')
    if modelid in des:
        return True
    else:
        return False        

def maptitle(brain):
    "replace"

    target = brain.getObject()
    des = target.title
    if isinstance(des, unicode):
        des = des.encode('utf-8')
    newd = des.replace(modelid,'')
    target.description = newd
    target.reindexObject(idxs=['Title'])    
    


