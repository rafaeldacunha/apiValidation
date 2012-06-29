#!/usr/bin/env python
# -*- coding: latin-1 -*-
'''
Created on 26/06/2012

@author: rafael.cunha
'''

print "ola3"

import sys
import StringIO
import lxml

from lxml import etree
from StringIO import StringIO
import os, sys

# Construct XML relevant to the XML schema we're validating against. By altering the string, adding/removing elements
# we can force different errors to occur when validating.
xml = StringIO('''<?xml version="1.0" encoding="iso-8859-1"?>
    <channels xmlns:TerraTVUtils="TerraTV:Util">
        <channel>
        <id><![CDATA[4845]]></id>
        <title><![CDATA[Diversão]]></title>
        <ad_channel><![CDATA[]]></ad_channel>
        <ad_frequency><![CDATA[0]]></ad_frequency>
        <adserver><![CDATA[no]]></adserver>
        </channel>
    </channels>
''')

# Clear any previous errors
lxml.etree.clear_error_log()

try:
    # Get the XML schema to validate against
    #schema = lxml.etree.XMLSchema(file = 'http://xmlgw.companieshouse.gov.uk/v2-1/schema/CompanyData-v2-2.xsd')
    schema = lxml.etree.XMLSchema(file = 'http://localhost/getCategories.xsd')
    
    # Parse string of XML
    xml_doc = lxml.etree.parse(xml)
    # Validate parsed XML against schema returning a readable message on failure
    schema.assertValid(xml_doc)
    # Validate parsed XML against schema returning boolean value indicating success/failure
    print 'schema.validate() returns "%s".' % schema.validate(xml_doc)

except lxml.etree.XMLSchemaParseError, xspe:
    # Something wrong with the schema (getting from URL/parsing)
    print "XMLSchemaParseError occurred!"
    print xspe

except lxml.etree.XMLSyntaxError, xse:
    # XML not well formed
    print "XMLSyntaxError occurred!"
    print xse
    
except lxml.etree.DocumentInvalid, di:
    # XML failed to validate against schema
    print "DocumentInvalid occurred!"

    error = schema.error_log.last_error
    if error:
        # All the error properties (from libxml2) describing what went wrong
        print 'domain_name: ' + error.domain_name
        print 'domain: ' + str(error.domain)
        print 'filename: ' + error.filename # '<string>' cos var is a string of xml
        print 'level: ' + str(error.level)
        print 'level_name: ' + error.level_name # an integer
        print 'line: ' + str(error.line) # a unicode string that identifies the line where the error occurred.
        print 'message: ' + error.message # a unicode string that lists the message.
        print 'type: ' + str(error.type) # an integer
        print 'type_name: ' + error.type_name