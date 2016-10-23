# -*- coding: utf-8 -*-
from plone import api
from Products.CMFCore.utils import getToolByName
from shuiwu.baoshui.content.nashuiren import Inashuiren

subids = [('zichanfuzaibiao1','yuedujilu',u'资产负债表',12),
               ('lirunbiao1','yuedujilu',u'利润表',12),
               ('xianjinliuliangbiao1','yuedujilu',u'现金流量表',12),
               ('chengjianjiaoyudifangfujia','yuedujilu',u'城建、教育、地方教育附加申报表',12),
               ('gerensuodeshui1','yuedujilu',u'个人所得税扣缴表',12),
               ('zhifugongzimingxi1','yuedujilu',u'支付工资明细',12),
               ('yinhuashuianyue1','yuedujilu',u'印花税申报表（按月）',12),
               ('canbaojinshenbaobiao','yuedujilu',u'残保金申报表',12),
               ('gonghuijingfei1','yuedujilu',u'工会经费申报表',12),
               ('shuilijijin1','yuedujilu',u'水利基金申报表（月报）',12),
               ('shebaofei1','yuedujilu',u'社保费申报表',12),
               ('fangchanshui1','yuedujilu',u'房产税申报表（租金收入）',12),
               ('tudizengzhishui1','yuedujilu',u'土地增值税申报表（按月）',12),
               ('anyueqita1','yuedujilu',u'其他1',12),
               ('anyueqita2','yuedujilu',u'其他2',12),
               ('qiyesuodeshuialeiblei','jidujilu',u'企业所得税预缴表（A类、B类）',4),
               ('fangchanshuifangchanyuanzhi1','jidujilu',u'房产税申报表（房产原值）',4),
               ('chengzhentudishiyongshui1','jidujilu',u'城镇土地使用税申报表',4), 
               ('anjiqita1','jidujilu',u'按季其他1',4),
               ('anjiqita2','jidujilu',u'按季其他2',4),
               ('yinhuashuizijinzhangbo1','ancijilu',u'印花税申报表（资金帐薄）',12),
               ('ziyuanshui1','ancijilu',u'资源税申报表',12),
               ('gengdizhanyongshui1','ancijilu',u'耕地占用税申报表',12),
               ('anciqita','ancijilu',u'其他',12)                                                                                                           
               ]
def createChildTree(context):
    "for nashuiren create sub-child-tree"
    #search all nashuiren objects that have not sub object
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":Inashuiren.__identifier__}
    bns = pc(query)
    bns = filter(pathsearchFilter,bns)
    if len(bns) > 100:
        bns = bns[:99]    
    finishlist = map(mapf,bns)
        
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


        
        
    
    
    


