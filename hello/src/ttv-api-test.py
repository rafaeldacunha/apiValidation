'''
Created on 26/03/2012

@author: rafael.cunha
'''
import httplib, base64, urllib
import hashlib, md5
from time import gmtime, localtime, strftime
import xml.parsers.expat
from xml.dom.minidom import parse, parseString
import minixsv  

####### read config file
def read_ttvapi_config(configFile):
    #f = open('config.xml', 'r')
    f = open(configFile, 'r')
    configData = f.read()
    return configData

####### obtem lista de systems a serem testados
def read_systems_to_test(configData):
    dom1 = xml.dom.minidom.parseString(configData)
    lista = dom1.getElementsByTagName("system")
    ttvsystems = {}
    for node2 in lista:
        systemName= node2.getAttribute('name')
        secret= node2.getAttribute('secret') 
        url= node2.getAttribute('url')
        
        # for each method to be tested for this system, extract method name, parameters and expected values
        methodsToBeTested = {}
        for node3 in node2.childNodes:
           if (node3.nodeType==1) and node3.hasAttributes():
               methodName = node3.getAttribute('name')
               expectedTag= node3.getAttribute('expectedTag')
               expectedTagValue= node3.getAttribute('expectedTagValue')
               expectedTagAttribute = node3.getAttribute('expectedTagAttribute')
               expectedTagAttributeValue = node3.getAttribute('expectedTagAttributeValue')
               methodExpectedReturnValues = {'expectedTag':expectedTag,
                                             'expectedTagValue':expectedTagValue,
                                             'expectedTagAttribute':expectedTagAttribute,
                                             'expectedTagAttributeValue':expectedTagAttributeValue}
               methodsToBeTested[methodName] = methodExpectedReturnValues
               
        ttvsys = {'secret':secret, 'url':url, 'methodsToBeTested':methodsToBeTested}
        ttvsystems[systemName] = ttvsys
    return ttvsystems;

configData = read_ttvapi_config('config.xml')
ttvsystems = read_systems_to_test(configData)

# ttvsystems                 {name:ttvsys}
# ttvsys                     {secret,url,methosToBrTested}
# methodsToBeTested          {name, methodExpectedReturnValues}
# methodExpectedReturnValues {expectedTag, expectedTagValue, expectedTagAttribute, expectedTagAttributeValue}

sistema = ttvsystems['demo']
print 'secret=' + sistema['secret']
metodos = sistema['methodsToBeTested']
methodExpectedReturnValues = metodos['getCategories'] 
methodReturnValues = methodExpectedReturnValues.keys();
print methodReturnValues
print 'expectedTag=' + methodExpectedReturnValues['expectedTag']
systemsList = ttvsystems.keys()
for name in systemsList:
    print "system:" + name

print "-- Validação XSD"

    
