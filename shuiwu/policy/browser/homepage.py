#-*- coding: UTF-8 -*-
from five import grok
import json
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Products.CMFCore.interfaces import ISiteRoot

from shuiwu.theme.interfaces import IThemeSpecific
from shuiwu.baoshui.browser.ajax_listing import sysAjaxListingView,ajaxsearch
from shuiwu.baoshui.content.nashuiku import Inashuiku
from shuiwu.baoshui.content.nashuiren import Inashuiren


# grok.templatedir('templates')

class FrontpageView(sysAjaxListingView):
     
      
       
    def getPathQuery(self):
 
        """返回 纳税人库目录
        """
        query = {}
        db = self.getDBFolder()

        query['path'] = "/".join(db.getPhysicalPath())
        return query         
        
# roll table output
    def getDBFolder(self):
        
        brains = self.catalog()({'object_provides':Inashuiku.__identifier__})
        context = brains[0].getObject()
        return context        
        
class search(ajaxsearch):
    
    def render(self):    
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"index.html")        
 # datadic receive front ajax post data       
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          

        tag = datadic['tag'].strip()
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()     

        origquery = searchview.getPathQuery()
        origquery['object_provides'] = Inashuiren.__identifier__
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection                
 #模糊搜索       
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'        

#         if securitykey != 0:
#             origquery['security_level'] = searchview.getSecurityLevel(securitykey)
        if datekey != 0:
            origquery['created'] = self.Datecondition(datekey)           
#         if tasktypekey != 0:
#             origquery['task_type'] = searchview.getTaskType(tasktypekey)

        # remove repeat values 
        tag = tag.split(',')
        tag = set(tag)
        tag = list(tag)
        all = u"所有".encode("utf-8")
        unclass = u"未分类".encode("utf-8")        
# filter contain "u'所有'"
        tag = filter(lambda x: all not in x, tag)
# recover un-category tag (remove:u"未分类-")
        def recovery(value):
            if unclass not in value:return value
            return value.split('-')[1]
            
        tag = map(recovery,tag)        
        if '0' in tag and len(tag) > 1:
            tag.remove('0')
            rule = {"query":tag,"operator":"and"}
            origquery['Subject'] = rule
                      
#totalquery  search all 
        totalquery = origquery.copy()
#origquery provide  batch search        
        origquery['b_size'] = size 
        origquery['b_start'] = start
        # search all                         
        totalbrains = searchview.search_multicondition(totalquery)
        totalnum = len(totalbrains)
        # batch search         
        braindata = searchview.search_multicondition(origquery)
#        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains
#call output function        
        data = self.output(start,size,totalnum, braindata)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)
    
    def output(self,start,size,totalnum,braindata):
        "根据参数total,braindata,返回jason 输出"
        outhtml = ""      

        import datetime
        id = datetime.datetime.today().strftime("%Y")
        for i in braindata:          
            out = """<tr>
                                <td class="col-md-1">%(shibiehao)s</td>
                                <td class="col-md-1"><a href="%(objurl)s">%(title)s</a></td>
                                <td class="col-md-1">%(type)s</td>
                                <td class="col-md-1">%(description)s</td>
                                <td class="col-md-1">%(shuiguanyuan)s</td>
                                <td class="col-md-1">%(danganbianhao)s</td>
                                <td class="col-md-1">%(status)s</td>
                                <td class="col-md-1">%(date)s</td>
                                <td class="col-md-1">%(caiwufuzeren)s</td>
                                <td class="col-md-1">%(caiwufuzerendianhua)s</td>
                                <td class="col-md-1">%(banshuiren)s</td>
                                <td class="col-md-1">%(banshuirendianhua)s</td>                                
                            </tr> """% dict(objurl="%s/%s" % (i.getURL(),id),                                            
                                            title=i.Title,
                                            shibiehao = i.guanlidaima,
                                            type = i.type,
                                            shuiguanyuan = i.shuiguanyuan,
                                            danganbianhao = i.danganbianhao,
                                            status = i.status,
                                            caiwufuzeren = i.caiwufuzeren,
                                            caiwufuzerendianhua = i.caiwufuzerendianhua,
                                            banshuiren = i.banshuiren,
                                            banshuirendianhua = i.banshuirendianhua,
                                            description= i.Description,
                                            date = i.dengjiriqi)           
            outhtml = "%s%s" %(outhtml ,out)

           
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data    
         
class TagSearchView(FrontpageView):
    "统计查询视图"
    
                   
