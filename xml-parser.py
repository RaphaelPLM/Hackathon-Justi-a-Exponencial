import xml.dom.minidom as minidom
import csv

def extractData(doc, tag_name):
     list_objects = doc.getElementsByTagName(tag_name)
     return list_objects

def printDataFromFieldName(tag_name, field_name):
     list_objects = extractData(tag_name)

     for obj in list_objects:
          print(obj.getAttribute(field_name))

def mapProcessToSubjectCode():
     doc = minidom.parse('TRF1_G2_20191112_48.xml')

     dict_processo_assunto = {}

     list_processos = doc.getElementsByTagName("ns2:processo")

     # Get information (process number and subject codes) from XML
     for processo in list_processos:
          list_dadosBasicos = processo.getElementsByTagName("dadosBasicos")
          
          list_codigos = []

          for dadosBasicos in list_dadosBasicos:
               list_assuntos = dadosBasicos.getElementsByTagName("assunto")
               
               processo_num = dadosBasicos.getAttribute("numero")

               for assunto in list_assuntos:
                    list_assuntosLocais = assunto.getElementsByTagName("assuntoLocal")

                    for assunto_local in list_assuntosLocais:
                         cod_pai_nacional = assunto_local.getAttribute("codigoPaiNacional")
                    
                         list_codigos.append(cod_pai_nacional)

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

# @filiperbluz
# similaridade de cossenos