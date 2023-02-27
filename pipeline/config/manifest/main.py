import xml.etree.ElementTree as ET
import glob
import json
from os.path import dirname, abspath

def readFile( path ):
	strFile = ''
	with open( path, 'r') as f:
		strFile = f.read()
	return strFile

def getfilesPath( item, path ):
	deployPath = '../sfdx-project/force-app/deploy/' 
	print( deployPath )
	return glob.glob( deployPath + str( item[ 'folder' ] ) + '/*.xml' )

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
				if fileChanged == False:
					print( '\n\t' + itemPath + '\n' )
				print( '\t' + str( node[ 'parentNode' ] ) + '/' + str( node[ 'childNode' ] ) + '/' + metadataNode )
				root.remove( parentNode )
				fileChanged = True

	if fileChanged:
		et = ET.ElementTree( root )
		et.write( itemPath, encoding = 'UTF-8', xml_declaration = True )
		print( '\n------------------------------------------------------------------' )

def createPath( parentElementTag, elementName ):
	path = './'
	if '{http://soap.sforce.com/2006/04/metadata}' in parentElementTag:
		path += '{http://soap.sforce.com/2006/04/metadata}' + elementName
	else:
		path = './' + elementName
	return path

def clearFile( path ):
	print( '\nIniciando o script de limpeza dos arquivos\n' )
	
	itens = json.loads( readFile( path + '/manifest/config/tags.json' ) )
	
	for item in itens[ 'itens' ]:
		nodes = item[ 'nodes' ]
		for filePath in getfilesPath( item, path ):
			removeXMLNodes( filePath, nodes )
	
	print( '\nProcesso de limpeza dos arquivos concluido\n' )