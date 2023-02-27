# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import sys
import os 
import shutil 
from shutil import copyfile, copytree
import re
import glob
import json


def namespace(element):
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''

def readFile( path ):
	strFile = ''
	with open( path, 'r') as f:
		strFile = f.read()
	return strFile

def removeXMLNodes( itemPath, nodes ):
	fileChanged = False

	xml_tree = readFile( itemPath )
	parser = ET.XMLParser( encoding='UTF-8' )
	ET.register_namespace( '', 'http://soap.sforce.com/2006/04/metadata' )
	root = ET.fromstring( xml_tree, parser = parser )
	fileChanged = False
	for node in nodes:
		for parentNode in root.findall( createPath( root.tag, str( node[ 'parentNode' ] ) ) ):
			metadataNode = parentNode.find(  createPath( root.tag, str( node[ 'childNode' ] ) ) ).text
			if metadataNode in node[ 'values' ]:
				root.remove( parentNode )
				fileChanged = True

	if fileChanged:
		et = ET.ElementTree( root )
		et.write( itemPath, encoding = 'UTF-8', xml_declaration = True )

def createPath( parentElementTag, elementName ):
	path = './'
	if '{http://soap.sforce.com/2006/04/metadata}' in parentElementTag:
		path += '{http://soap.sforce.com/2006/04/metadata}' + elementName
	else:
		path = './' + elementName
	return path

def copyFileIsValid(src, des, filename):
    print (src.decode("utf-8"))
    print (des.decode("utf-8"))

    if not os.path.exists(src):
        print('Warning: Arquivo ' + filename + ' nao existe no repositorio')
    else:
        copyfile(src,des)

def copyFolderIsValid(src, des,filename):
    if not os.path.exists(src):
        print('Warning: Arquivo "' + filename + '" nao existe no repositorio!')
    else:
        copytree(src,des)
    
def getExtensionStaticResource(contentType):
    
    data = [
        ['image/png','png'],
        ['application/json','json'],
        ['application/javascript','js'],
        ['text/javascript','js'],
        ['image/jpeg','jpeg'], 
        ['text/plain','txt'], 
        ['image/svg+xml','svg'],
        ['text/css','css'],
        ['application/x-zip-compressed','folder'],
        ['application/zip','folder'],
        ['text/csv','csv']
    ]
    
    extension = ''
    
    for loop in data:
        if(loop[0] == contentType):
            extension = loop[1]
    return extension            

def getfile(type, member, files, actualStatus):
    
    configs = {
        'AuthProvider': [['authproviders','authprovider']],
        'CustomApplication': [['applications','app']],
        'AppMenu': [['appMenus','appMenu']],
        'ApprovalProcess': [['approvalProcesses','approvalProcess']],
        'AssignmentRules': [['assignmentRules','assignmentRules']],
        'AutoResponseRules': [['autoResponseRules','autoResponseRules']],
        'ApexClass': [['classes','cls'],['classes', 'cls-meta.xml']],
        'Community': [['communities','community']],
        'ApexComponent': [['components','component'], ['components', 'component-meta.xml']],
        'CustomApplicationComponent': [['customApplicationComponents','customApplicationComponent']],
        'CustomNotificationType': [['notificationtypes','notiftype']],
        'DataCategoryGroup': [['datacategorygroups','datacategorygroup']],
        'EntitlementProcess': [['entitlementProcesses','entitlementProcess']],
        'EscalationRules': [['escalationRules','escalationRules']],
        'ExperienceBundle': [['experiences','site']],
        'NetworkBranding': [['networkBranding','networkBranding-meta.xml'], ['networkBranding','networkBranding']],
        'Fields': [['customFields']],
        'Flow': [['flows','flow']],
        'Group': [['groups','group']],
        'HomePageComponent': [['homePageComponents','homePageComponent']],
        'HomePageLayout': [['homePageLayouts','homePageLayout']],
        'CustomLabel' : [['labels', 'labels']],
        'CustomLabels': [['labels','labels']],
        'ProfileSessionSetting' : [['profileSessionSettings', 'profileSessionSetting']],
        'ProfilePasswordPolicy' : [['profilePasswordPolicies', 'profilePasswordPolicy']],
        'Layout': [['layouts','layout']],
        'PlatformCachePartition':[['cachePartitions','cachePartition']],
        'Letterhead': [['letterhead','letter']],
        'LiveChatAgentConfig': [['liveChatAgentConfigs','liveChatAgentConfig']],
        'LiveChatButton': [['liveChatButtons','liveChatButton']],
        'LiveChatDeployment': [['liveChatDeployments','liveChatDeployment']],
        'MilestoneType': [['milestoneTypes','milestoneType']],
        'Network': [['networks','network']],
        'CustomObject': [['objects','object']],
        'CustomObjectTranslation': [['objectTranslations','objectTranslation']],
        'ApexPage': [['pages','page'], ['pages', 'page-meta.xml']],
        'PathAssistant': [['pathAssistants','pathAssistant']],
        'PermissionSet': [['permissionsets','permissionset']],
        'PermissionSetGroup': [['permissionsetgroups','permissionsetgroup']],
        'Profile': [['profiles', 'profile']],
        'Queue': [['queues','queue']],
        'QuickAction': [['quickActions','quickAction']],
        'RemoteSiteSetting': [['remoteSiteSettings','remoteSite']],
        'ReportType': [['reportTypes','reportType']],
        'Role': [['roles','role']],
        'Skill': [['skills','skill']],
        'Settings': [['settings','settings']],
        'SiteDotCom': [['siteDotComSites','site'], ['siteDotComSites', 'site-meta.xml']],
        'CustomSite': [['sites','site']],
        'StaticResource': [['staticresources', 'resource-meta.xml']],
        'CustomTab': [['tabs','tab']],
        'CustomMetadata': [['customMetadata','md']],
        'ApexTrigger': [['triggers','trigger'],['triggers','trigger-meta.xml']],
        'CustomPageWebLink': [['weblinks','weblink']],
        'Workflow': [['workflows','workflow']],
        'WorkflowAlert': [['workflows', 'workflow']],
        'WorkflowFieldUpdate': [['workflows', 'workflow']],
        'WorkflowTask': [['workflows', 'workflow']],
        'WorkflowRule': [['workflows', 'workflow']],
        'WebLink': [['webLinks', 'webLink'], ['webLinks', 'webLink-meta.xml']],
        'RemoteSiteSettings': [['remoteSiteSettings', 'remoteSite']],
        'Report': [['reports', 'report-meta.xml']],
        'Dashboard': [['dashboards', 'dashboard-meta.xml']],
        'Document': [['documents', '-meta.xml']],
        'EmailTemplate': [['email', 'email'], ['email', 'email-meta.xml']],
        'SharingCriteriaRule': [['sharingRules', 'sharingRules']],
        'SharingRules': [['sharingRules', 'sharingRules']],
        'GlobalPicklist': [['globalPicklists', 'globalPicklist']],
        'FlowDefinition': [['flowDefinitions', 'flowDefinition']],
        'FlexiPage': [['flexipages', 'flexipage']],
        'PlatformEventSubscriberConfig': [['platformEventSubscriberConfigs', 'platformEventSubscriberConfig']],
        'AuraDefinitionBundle': [['aura']],
        'ConnectedApp': [['connectedApps', 'connectedApp']],
        'GlobalValueSet': [['globalValueSets', 'globalValueSet']],
        'StandardValueSet': [['standardValueSets', 'standardValueSet']],
        'SharingSet': [['sharingSets', 'sharingSet']],
        'NavigationMenu': [['navigationMenus', 'navigationMenu']],
        'CallCenter': [['callCenters', 'callCenter']],
        'CustomPermission': [['customPermissions', 'customPermission']],
        'NamedCredential': [['namedCredentials', 'namedCredential']],
        'MatchingRule': [['matchingRules', 'matchingRule']],
        'DuplicateRule': [['duplicateRules', 'duplicateRule']],
        'ContentAsset': [['contentassets', 'asset'], ['contentassets', 'asset-meta.xml']],
        'WaveApplication': [['wave', 'wapp']],
        'WaveDashboard': [['wave', 'wdash']],
        'WaveDataflow': [['wave', 'wdf']],
        'WaveDataset': [['wave', 'wds']],
        'CspTrustedSite': [['cspTrustedSites', 'cspTrustedSite']],
        'QueueRoutingConfig':[['queueRoutingConfigs','queueRoutingConfig']], 
        'LightningComponentBundle':[['lwc']],
        'CustomField':[['fields','field-meta.xml']],
        'Index':[['indexes','indexe-meta.xml']],
        'BusinessProcess':[['businessProcesses','businessProcess-meta.xml']],
        'RecordType':[['recordTypes','recordType-meta.xml']],
        'ListView':[['listViews','listView-meta.xml']], 
        'Bot':[['bots','bot-meta.xml']], 
        'CompactLayout':[['compactLayouts', 'compactLayout-meta.xml']],
        'ValidationRule':[['validationRules', 'validationRule-meta.xml']],
        'FieldSet':[['fieldSets', 'fieldSet-meta.xml']],
        'RecordActionDeployment':[['recordActionDeployments', 'deployment']],
        'LightningMessageChannel':[['messageChannels', 'messageChannel']],
        'EmailServicesFunction' : [['emailservices','xml-meta.xml']],
        'Translations' : [['translations','translation']],
        'ManagedTopics' : [['managedTopics','managedTopics']],
        'DelegateGroup' : [['delegateGroups','delegateGroup']],
        'SharingReason' : [['sharingReasons','sharingReason-meta.xml']]
    }
  
    if(type == 'LightningComponentBundle' or type == 'AuraDefinitionBundle' or type == 'CustomObjectTranslation'): 
      
      for config in configs[type]:
        foldersrc = config[0]
        newpath = os.path.join(sys.argv[2], foldersrc)
        
        if not os.path.exists(newpath):
          os.makedirs(newpath)
        
        if not os.path.exists(os.path.join(sys.argv[2], foldersrc, member)):
            src = os.path.join(sys.argv[3], foldersrc, member)
            des = os.path.join(sys.argv[2], foldersrc, member)
            copyFolderIsValid(src,des,foldersrc + '/' + member)
    
    elif(type == "Index" or type =="CustomField" or type == "WebLink" or type == "ListView" or type == "RecordType"  or type == "CompactLayout" or type == "ValidationRule" or type == "FieldSet" or type == "BusinessProcess" or type == "SharingReason"):
        
        for config in configs[type]:
            foldersrc = config[0]
            extension = config[1]
            newpath = os.path.join(sys.argv[2], "objects/"+str(member.split(".")[0]), foldersrc)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            src = os.path.join(sys.argv[3], "objects/"+str(member.split(".")[0]), foldersrc, member.split(".")[1]+ "." + extension)
            des = os.path.join(sys.argv[2], "objects/"+str(member.split(".")[0]), foldersrc, member.split(".")[1] + "." + extension)
            copyFileIsValid(src,des, member.split(".")[1])
    
    elif(type == "Bot"): 
        
        for config in configs[type]:
            foldersrc = config[0]
            extension = config[1]
            newpath = os.path.join(sys.argv[2],"bots/" +str(member.split(".")[0]))
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            src = os.path.join(sys.argv[3], foldersrc, str(member.split(".")[0]) ,str(member.split(".")[0]) + "." + extension)
            des = os.path.join(sys.argv[2], foldersrc, str(member.split(".")[0]) ,str(member.split(".")[0]) + "." + extension)
            copyFileIsValid(src,des, member.split(".")[0])
            if (len(member.split(".")) == 1 ):
                raise Exception('E necessario mandar a versao do Bot')
            # get Bot Version
            src = os.path.join(sys.argv[3], foldersrc, str(member.split(".")[0]) ,str(member.split(".")[1]) + ".botVersion-meta.xml")
            des = os.path.join(sys.argv[2], foldersrc, str(member.split(".")[0]) ,str(member.split(".")[1]) + ".botVersion-meta.xml")
            copyFileIsValid(src,des, member.split(".")[0])    
    elif(type == "Workflow" or type == "WorkflowAlert" or type == "WorkflowFieldUpdate" or type == "WorkflowTask" or type == "WorkflowRule" ):
        
        for config in configs[type]:
            foldersrc = config[0]
            extension = config[1]
            newpath = os.path.join(sys.argv[2], foldersrc)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            src = os.path.join(sys.argv[3], foldersrc, str(member.split(".")[0]) + "." + extension  + "-meta.xml")
            des = os.path.join(sys.argv[2], foldersrc, str(member.split(".")[0]) + "." + extension  + "-meta.xml")
            copyFileIsValid(src,des, str(member.split(".")[0]))
    
    elif(type =="CustomObject"):
        
        for config in configs[type]:
            foldersrc = config[0]
            extension = config[1]
            newpath = os.path.join(sys.argv[2], "objects/" + member)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            src = os.path.join(sys.argv[3], "objects/", member, member + "." + extension + "-meta.xml")
            des = os.path.join(sys.argv[2], "objects/", member, member + "." + extension + "-meta.xml")
            copyFileIsValid(src,des, member)
            
    elif(type=='Profile' or type == 'PermissionSet'):
        
        for config in configs[type]:
            foldersrc = config[0]
            extension = config[1]
            newpath = os.path.join(sys.argv[2], foldersrc)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            src = os.path.join(sys.argv[3], foldersrc, member + "." + extension + "-meta.xml")
            des = os.path.join(sys.argv[2], foldersrc, member + "." + extension + "-meta.xml")
            copyFileIsValid(src,des, member)
            itens = json.loads( readFile( sys.argv[3] + '/../../../pipeline-tools/config/manifest/config/tags.json' ) )
            
            for item in itens[ 'itens' ]:
                nodes = item[ 'nodes' ]
                if( str( item['type'] ) == type):
                    removeXMLNodes(des, nodes)
            
    elif(type=='ConnectedApp'):
        
        for config in configs[type]:
            foldersrc = config[0]
            extension = config[1]
            newpath = os.path.join(sys.argv[2], foldersrc)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            xmlProfile = ET.parse(os.path.join(sys.argv[3],foldersrc, member + "." + extension + "-meta.xml"))
            rootProfile = xmlProfile.getroot()
            for child in rootProfile:
                if "oauthConfig" in str(child.tag):
                    for m in child:
                        if(m.text == 'Full'):
                            messageErro = type + " " + member + " : Nao permitido conceder o acesso full ao Connect App"
                            raise Exception(messageErro)
            src = os.path.join(sys.argv[3], foldersrc, member + "." + extension + "-meta.xml")
            des = os.path.join(sys.argv[2], foldersrc, member + "." + extension + "-meta.xml")
            copyFileIsValid(src,des, member) 
            
    elif(type=='ApexClass' or type=='ApexTrigger' or type == 'ApexPage' or  type == 'NetworkBranding' or type == 'ContentAsset'):
        
        for config in configs[type]:
            foldersrc = config[0]
            extension = config[1]
            newpath = os.path.join(sys.argv[2], foldersrc)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            src = os.path.join(sys.argv[3], foldersrc,  str(member) + '.' + str(extension))
            des = os.path.join(sys.argv[2], foldersrc,  str(member) + '.' + str(extension))
            copyFileIsValid(src,des, member)
    
    elif(type == "EmailTemplate"):    
        for config in configs[type]:
            foldersrc = config[0]
            extension = config[1]
            newpath = os.path.join(sys.argv[2], foldersrc)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
       
        if(member.find("/") > 0):
            
            folder = str(member.split("/")[0])
            
            if not os.path.exists(sys.argv[2] + '/' + foldersrc + '/' + folder):
                os.makedirs(sys.argv[2] + '/' + foldersrc + '/' + folder)
            
            for config in configs[type]:
                foldersrc = config[0]
                extension = config[1]
                src = os.path.join(sys.argv[3],foldersrc, member + "." + extension)
                des = os.path.join(sys.argv[2],foldersrc, member + "." + extension)
                copyFileIsValid(src,des, member)
        else:
            
            src = os.path.join(sys.argv[3],foldersrc, member + '.emailFolder-meta.xml')
            des = os.path.join(sys.argv[2],foldersrc, member + '.emailFolder-meta.xml')
            copyFileIsValid(src,des, member)
    
    elif(type == "Dashboard"):
        
        for config in configs[type]:
            foldersrc = config[0]
            extension = config[1]
            newpath = os.path.join(sys.argv[2], foldersrc)
            
            if not os.path.exists(newpath):
                os.makedirs(newpath)
       
        if(member.find("/") > 0):
            
            folder = str(member.split("/")[0])
            
            if not os.path.exists(sys.argv[2] + '/' + foldersrc + '/' + folder):
                os.makedirs(sys.argv[2] + '/' + foldersrc + '/' + folder)
                
                src = os.path.join(sys.argv[3],foldersrc, folder + ".dashboardFolder-meta.xml")
                des = os.path.join(sys.argv[2],foldersrc, folder + ".dashboardFolder-meta.xml")
                copyFileIsValid(src,des, member)   

            for config in configs[type]:
                foldersrc = config[0]
                extension = config[1]
                src = os.path.join(sys.argv[3],foldersrc, member + "." + extension)
                des = os.path.join(sys.argv[2],foldersrc, member + "." + extension)
                copyFileIsValid(src,des, member)   
                
    elif(type == "Report"):
        
        for config in configs[type]:
            foldersrc = config[0]
            extension = config[1]
            newpath = os.path.join(sys.argv[2], foldersrc)
            
            if not os.path.exists(newpath):
                os.makedirs(newpath)
       
        if(member.find("/") > 0):
            
            folder = str(member.split("/")[0])
            
            if not os.path.exists(sys.argv[2] + '/' + foldersrc + '/' + folder):
                os.makedirs(sys.argv[2] + '/' + foldersrc + '/' + folder)
                
                src = os.path.join(sys.argv[3],foldersrc, folder + ".reportFolder-meta.xml")
                des = os.path.join(sys.argv[2],foldersrc, folder + ".reportFolder-meta.xml")
                copyFileIsValid(src,des, member)   

            for config in configs[type]:
                foldersrc = config[0]
                extension = config[1]
                src = os.path.join(sys.argv[3],foldersrc, member + "." + extension)
                des = os.path.join(sys.argv[2],foldersrc, member + "." + extension)
                copyFileIsValid(src,des, member)    
            
            
    elif(type=='StaticResource'):
        
        for config in configs[type]:
            foldersrc = config[0]
            extension = config[1]
            newpath = os.path.join(sys.argv[2], foldersrc)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            xmlResource = ET.parse(os.path.join(sys.argv[3],foldersrc, member + "." + extension ))
            rootResource = xmlResource.getroot()
            
            staticResourceExtension = ''
            
            for child in rootResource:
                if "contentType" in str(child.tag):
                    staticResourceExtension = getExtensionStaticResource(child.text)
                    
                    if(staticResourceExtension == 'folder'):
                    
                        src = os.path.join(sys.argv[3], foldersrc, member)
                        des = os.path.join(sys.argv[2], foldersrc, member)
                        if not os.path.exists(des):
                            copyFolderIsValid(src,des, member)
                    
                    else:
                        
                        src = os.path.join(sys.argv[3], foldersrc, member + "." + staticResourceExtension)
                        des = os.path.join(sys.argv[2], foldersrc, member + "." + staticResourceExtension)
                        copyFileIsValid(src,des, member)
            
            src = os.path.join(sys.argv[3], foldersrc, member + "." + extension)
            des = os.path.join(sys.argv[2], foldersrc, member + "." + extension)
            copyFileIsValid(src,des, member)
    
    elif(type == 'ExperienceBundle'):
        
        for config in configs[type]:
            foldersrc = config[0]
            extension = config[1]
            newpath = os.path.join(sys.argv[2], foldersrc)
            
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            
        folder = str(member.split("/")[0])
       
        if not os.path.exists(sys.argv[2] + '/' + foldersrc + '/' + folder):
            src = os.path.join(sys.argv[3],foldersrc, folder)
            des = os.path.join(sys.argv[2],foldersrc, folder)
            copyFolderIsValid(src,des,foldersrc + '/' + member)
            
        for config in configs[type]:
            foldersrc = config[0]
            extension = config[1]
            src = os.path.join(sys.argv[3],foldersrc, member + "." + extension + '-meta.xml')
            des = os.path.join(sys.argv[2],foldersrc, member + "." + extension + '-meta.xml')
            copyFileIsValid(src,des, member)   
    else:
      
      for config in configs[type]:
        
        foldersrc = config[0]
        extension = config[1]
        newpath = os.path.join(sys.argv[2], foldersrc)
    
        if not os.path.exists(newpath):
          os.makedirs(newpath)
    
        src = os.path.join(sys.argv[3], foldersrc, member.decode("utf-8") + "." + extension + "-meta.xml")
        des = os.path.join(sys.argv[2], foldersrc, member.decode("utf-8") + "." + extension + "-meta.xml")
        copyFileIsValid(src,des, member)
    
    return files

def initProcess(xml):
    root = xml.getroot()
    workspace = sys.argv[2]
    newpath =  sys.argv[2]
    space = namespace(root)
    files = [] 

    if not os.path.exists(newpath):
        os.makedirs(newpath)
    for child in root: 
        if(child.tag == str(space + "types")):
            name = child.find(str(space + "name")).text
            for member in child:
                if(member.tag == str(space + "members")):
                    files = getfile(name, member.text, files, '')
    print('Montagem Finalizada')

path = sys.argv[1] + "packages"
print (path)
if not os.path.exists(path):
    print('\n\nNenhum Arquivo PACKAGE.XML foi encontrado\n\n')
    sys.exit(1)
    
for file in os.listdir(path):
      print('Package.xml: ' + file)
      xml = ET.parse(os.path.join(path, file))
      initProcess(xml)


