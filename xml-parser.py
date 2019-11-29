import xml.dom.minidom as minidom
import csv
from operator import itemgetter
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from gensim.models import LdaModel
from gensim.corpora.dictionary import Dictionary
from gensim.utils import lemmatize, simple_preprocess
from nltk.cluster import KMeansClusterer
from nltk.corpus import stopwords
import nltk
import pyLDAvis.gensim
import warnings

# This function navigates through the XML data source, and extract all of it's lawsuits ID's and the related subject codes.
def mapProcessToSubjectCode(filename):
     # The first step is to parse data from a XML source.
     doc = minidom.parse(filename)

     print("FILENAME ", filename)

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

     return dict_processo_assunto

def count_subject_freqs(dict_processo_assunto):
     assunto = [] 
     counted = {}
     
     for registro in dict_processo_assunto: 
          for registro2 in dict_processo_assunto[registro]: 
               assunto.append(registro2) 
               counted = count_elements(assunto)
     
     print(counted)

     return counted

def remove_stopwords(texts):
    stop_words = nltk.corpus.stopwords.words('portuguese')
    stop_words.extend(['art', 'cf'])

    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def sentences_words_generator(dict):
     list_sentences_words = []
     
     for row in dict:
          for subject_descripton in dict[row]:
               list_words = subject_descripton.split()
               list_sentences_words.append(list_words)

     print(list_sentences_words)
     
     return list_sentences_words

def count_elements(seq) -> dict: 
     hist = {} 
     for i in seq: 
          hist[i] = hist.get(i, 0) + 1 
          
     return hist

def readFromCSV():
     dict_codigo_descricao = {}
     
     with open('DESCRICAO ASSUNTO.csv', newline='') as csvfile:
          reader = csv.DictReader(csvfile)
          for row in reader:
               dict_codigo_descricao[row['Cod_Pai']] = row['Assunto_Descricao']

     for row in dict_codigo_descricao:
          print(row, dict_codigo_descricao[row])

     return dict_codigo_descricao

def getSubjectDescriptionFromCode(dict_processo_assunto, dict_codigo_descricao):
     # Instantiates a new dictionary, in which the key will be the lawsuit ID, and the value will be an array of each subject description
     dict_processo_descricao = {}

     # Iterates through each row of a dictionary
     for row in dict_processo_assunto:
          list_current_lawsuit_subjects = []
          
          # Iterates through each code on the value of a row (tipically an array)
          for subject_code in dict_processo_assunto[row]:
               # Gets the subject description based on its code
               subject_description = dict_codigo_descricao[subject_code]

               list_current_lawsuit_subjects.append(subject_description)

          dict_processo_descricao[row] = list_current_lawsuit_subjects

     print("\n\n\n\DICIONARIO FINAL ")
     for row in dict_processo_descricao:
          print(row, dict_processo_descricao[row])

     return dict_processo_descricao


############### Data training and visualization #################
def generateBarChart(dict_freqs):     
     
     fig = plt.figure(figsize=(16, 9))
     
     plt.bar(range(len(dict_freqs)), list(dict_freqs.values()), align='center')
     plt.xticks(range(len(dict_freqs)), list(dict_freqs.keys()), rotation='vertical')

     fig.savefig('bar_chart.png', dpi = 500)

     plt.show()

def train_lda(training_data):
     dictionary = Dictionary(training_data)
     corpus = [dictionary.doc2bow(sentence) for sentence in training_data]

     model = LdaModel(corpus, num_topics=4)

     visualize_lda(model, corpus, dictionary)

def visualize_lda(model, corpus, dictionary):
     visualization = pyLDAvis.gensim.prepare(model, corpus, dictionary)

     pyLDAvis.save_html(visualization, 'LDA_Visualization.html')
##############################################################

def main():
          
          filename_suffix = ['1', '2', '48']

          filenames = []

          for suffix in filename_suffix:
               filenames.append('TRF1_G2_20191112_' + suffix + '.xml')

          dict_processo_assunto = {}

          for filename in filenames:
               dict_processo_assunto.update(mapProcessToSubjectCode(filename))

          dict_codigo_descricao = readFromCSV()
          dict_processo_descricao = getSubjectDescriptionFromCode(dict_processo_assunto, dict_codigo_descricao)

          dict_assunto_freqs = count_subject_freqs(dict_processo_assunto)

          sentences_words = sentences_words_generator(dict_processo_descricao)

          sentences_words = remove_stopwords(sentences_words)

          generateBarChart(dict_assunto_freqs)

          train_lda(sentences_words)

main()
