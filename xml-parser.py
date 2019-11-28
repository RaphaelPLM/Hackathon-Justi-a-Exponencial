import xml.dom.minidom as minidom
import csv
from operator import itemgetter

# Default function for extracting data from XML based on tag_name
def extractData(doc, tag_name):
     list_objects = doc.getElementsByTagName(tag_name)
     return list_objects

# Function that prints data based on a tag_name and a field_name. *Currently, not in use
def printDataFromFieldName(tag_name, field_name):
     list_objects = extractData(tag_name)

     for obj in list_objects:
          print(obj.getAttribute(field_name))

# This function navigates through the XML data source, and extract all of it's lawsuits ID's and the related subject codes.
def mapProcessToSubjectCode():
     
     # The first step is to parse data from a XML source.
     doc = minidom.parse('TRF1_G2_20191112_48.xml')

     # Instantiates an empty dictionary, that will be populated with parsed values, in the form {lawsuit_id: [array_of_subject_codes]}.
     dict_processo_assunto = {}

     # Generates a list of all lawsuits
     list_processos = doc.getElementsByTagName("ns2:processo")

     # Navigates through the tags hierarchy of the XML data source. This isn't strictly necessary, but makes the code more legible.
     for processo in list_processos:
          list_dadosBasicos = processo.getElementsByTagName("dadosBasicos")
          
          # Creates a list of subject codes.
          list_codigos = []

          for dadosBasicos in list_dadosBasicos:
               list_assuntos = dadosBasicos.getElementsByTagName("assunto")
               
               processo_num = dadosBasicos.getAttribute("numero")

               for assunto in list_assuntos:
                    list_assuntosLocais = assunto.getElementsByTagName("assuntoLocal")

                    for assunto_local in list_assuntosLocais:
                         cod_pai_nacional = assunto_local.getAttribute("codigoPaiNacional")

                         # This loop will append all subject codes into the array, that will be then associated with a key, in above's dictionary
                         list_codigos.append(cod_pai_nacional)

               # Associates a key with the subject codes array.
               dict_processo_assunto[processo_num] = list_codigos

     # Prints the generated dictionary   
     for registro in dict_processo_assunto:
          print ("PROCESSO: ", registro)
          print ("     CODIGOS: ", dict_processo_assunto[registro])

def readFromCSV():
     with open('ASSUNTO DESCRICAO.csv', newline='') as csvfile:
          reader = csv.DictReader(csvfile)
          for row in reader:
               print(row['Cod_Pai'], row['Assunto_Descricao'])

def main():
          mapProcessToSubjectCode()
          readFromCSV()
          # list_assuntos = processo.getElementsByTagName("assunto")

          # for assunto in list_assuntos:
          #      print('Código do assunto: ', assunto.getAttribute("codigoAssunto"))
     
     #printDataFromFieldName("dadosBasicos", "numero")

main()
