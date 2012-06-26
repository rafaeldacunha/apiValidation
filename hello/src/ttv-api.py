'''
Created on 26/03/2012

@author: rafael.cunha
'''
import httplib, base64, urllib
import hashlib, md5
from time import gmtime, localtime, strftime
import xml.parsers.expat
from xml.dom.minidom import parse, parseString
from lxml import etree
import StringIO  

hostBr = 'api.terratv.terra.com.br'
hashPass = 'p9bUt6ab'
ttvCall = "/demo/GetCategories.aspx"
parameters = "country=br&firstResult=1"

timestamp = strftime("%d%m%Y%S%M%H", gmtime())
ip = '200.176.1.253'
h1 = timestamp + ip
print h1;
h1 = base64.b64encode(h1)
print h1;

h2 = hashPass + '://' + hostBr + ttvCall + '?' + parameters + '&h1=' + h1
print h2

m = hashlib.md5()
m.update(h2)
h2 = m.digest()
print 'h2 md5:' + h2

h2 = base64.b64encode(h2)
print 'h2 md5 base64: ' + h2

ttvCall = ttvCall + "?" + parameters + "&h1=" + urllib.quote_plus(h1) + "&h2=" + urllib.quote_plus(h2)
print "ttvCall=" + ttvCall

conn = httplib.HTTPConnection(hostBr)
conn.request("GET", ttvCall)
r1 = conn.getresponse()
data1 = r1.read()
print 'HTTP Response:' + str(r1.status)
print data1

# XML Parse method 1
# 3 handler functions
def start_element(name, attrs):
    print 'Start element:', name, attrs
def end_element(name):
    print 'End element:', name
def char_data(data):
    print 'Character data:', repr(data)

p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data

p.Parse(data1)

# XML Parse method 2 - DOM
canais = []
dom = xml.dom.minidom.parseString(data1)
lista = dom.getElementsByTagName("title")
for node2 in lista:
    for node3 in node2.childNodes:
        print node3.nodeType
        print node3.data
        canais.append(node3.data)
print canais
#print canais[0]

# read config file
def read_ttvapi_config(configFile):
    #f = open('config.xml', 'r')
    f = open(configFile, 'r')
    configData = f.read()
    print 'systems to be tested: '
    return configData

configData = read_ttvapi_config('config.xml')
print "--->" + configData

#try:
dom1 = xml.dom.minidom.parseString(configData)
lista = dom1.getElementsByTagName("system")
for node2 in lista:
    print 'system=' + node2.getAttribute('name')
    print 'secret=' + node2.getAttribute('secret') 
    print 'url=' + node2.getAttribute('url')
#        print node2.childNodes
#        node3 = node2.firstChild
    for node3 in node2.childNodes:
       if (node3.nodeType==1) and node3.hasAttributes():
           print 'tem atributos'
           print 'nodeName=' + node3.nodeName
           print 'description=' + node3.getAttribute('description')
           expectedTag= node3.getAttribute('expectedTag')
           expectedTagValue= node3.getAttribute('expectedTagValue')
           expectedTagAttribute = node3.getAttribute('expectedTagAttribute')
           expectedTagAttributeValue = node3.getAttribute('expectedTagAttributeValue')
           print 'expectedTag=' + expectedTag
           print 'expectedTagValue=' + expectedTagValue
           print 'expectedTagAttribute=' + expectedTagAttribute
           print 'expectedTagAttributeValue=' + expectedTagAttributeValue
    
    
    if len(expectedTag) > 0 :
        lista = dom.getElementsByTagName(expectedTag)
        if len(lista) > 0:
            print "-- PASSED. Expected tag found: " + expectedTag
            
            if len(expectedTagValue)>0:
                for node2 in lista:
                    for node3 in node2.childNodes:
                        print node3.data.lower() + " ; type=" + str(node3.nodeType)
                        if (node3.nodeType==4) and (node3.data.lower() == expectedTagValue):
                            print "-- PASSED. Expected value for tag found: " + expectedTagValue
            else:
                print "-- PASSED. No TagValue required for: " + expectedTag 
                
            if len(expectedTagAttribute)>0:
                for node2 in lista:
                    print "node2Type=" + str(node2.nodeType)
                    print "node2Name=" + str(node2.nodeName)
                    if (node2.nodeType==1) and node2.hasAttributes():
                        print 'tem atributos'
                        expectedTag= node3.getAttribute(expectedTagAttribute)
                        #if len(expectedTagAttributeValue)>0:
                    else:
                        print "-- FAIL. No such attribute found: " + expectedTagAttribute + " for tag=" + expectedTag
     
    print '-- XSD validation'
    xsdF = open('getCategories.xsd', 'r')
    xsdData = xsdF.read()
    print 'xsd data:' + xsdData
    
    xmlF = open('getCategories.xml', 'r')
    xmlData = xmlF.read()

    #val = parseAndValidate("getCategories.xml", xsdFile="getCategories.xsd")
    #print '-- val=' + val    


#f = StringIO('<a><b></b></a>')
fl = StringIO.StringIO()
fl.write(xsdData)
xmlschema_doc = etree.parse(fl)

#xmlschema_doc = etree.parse(f)
#xmlschema = etree.XMLSchema(xmlschema_doc)    
    #parseAndValidateString(data1, xsdData, **kw)
#except xml.parsers.expat.ExpatError:
    #print 'Bad, bad XML! No donut for you'
#except:
    #print 'Bad, bad XML! No donut for you 2'
    
