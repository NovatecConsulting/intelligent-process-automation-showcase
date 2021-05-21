import boto3
import json
import logging
import os
from os import path
import pandas as pd
import PyPDF2
import uuid

class IntelligentDocumentAnalyzer:
    """Implements all logic to execute Named Entity Recognition on a document."""
   
    COMPREHEND_OUTPUT = "comprehend_output"
    PYPDF2_OUTPUT = "raw_text_output"
    DATA = "data"
    
    def __init__(self, file_path):
        super().__init__()
        logging.basicConfig(level=logging.INFO)
        self.file_path = file_path
        self.file_basename = os.path.basename(self.file_path)


    def pdf_to_text(self, ida_job_id):
        """
        Converts a pdf to raw text.
        
        Args:
            ida_job_id (str): the unique id of the analysis job that called the function

        Returns: 
            raw_text_file_path (str): the full path were the raw text file is saved
        """   
        raw_text_output_dir_name = os.path.join(self.PYPDF2_OUTPUT, ida_job_id)
        text_output_name = self.file_basename.replace('.pdf', '.txt')
        
        if not path.exists(raw_text_output_dir_name):
                    os.makedirs(raw_text_output_dir_name)

        raw_text_file_path = os.path.join(raw_text_output_dir_name, text_output_name)
        
        with open(self.file_path,'rb') as pdfFileObj, open(raw_text_file_path, "w") as raw_text_file:
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            pageObj = pdfReader.getPage(0)     
            text = pageObj.extractText()

            raw_text_file.write(text)
            raw_text_file.close()

        logging.info('Job Id:{} converted file {} to raw text in path'.format(ida_job_id,raw_text_file_path, self.file_path))             
        
        return raw_text_file_path


    def comprehend_and_save(self, ida_job_id, raw_text_file_path):
        """
        Does Named Entity Recognition on the raw text file.
        
        Args:
            ida_job_id (str): the unique id of the analysis job that called the function
            raw_text_file_path (str): the full path to read the raw text file from

        Returns: 
            entities_file_path (str): the full path were the entities file is saved
        """   
        comprehend_output_dir_name = os.path.join(self.COMPREHEND_OUTPUT, ida_job_id)
        
        entities_file_path = os.path.join(comprehend_output_dir_name,"output.json")

        if not path.exists(comprehend_output_dir_name):
            os.makedirs(comprehend_output_dir_name)
            
        with open(raw_text_file_path, 'r') as raw_text_file, open(entities_file_path, "w") as entities_file:
            text = raw_text_file.read()
                
            client = boto3.client('comprehend')
            response = client.detect_entities(LanguageCode= "de", Text =  text)
            
            json.dump(response, entities_file)

        logging.info('Job Id:{} extracted entities from file {} in path: {}'.format(ida_job_id,raw_text_file_path, entities_file_path))             

        return entities_file_path

    def run(self):
        """
        Implements the end-to-end process for entity recognition in a document.
        """  
        ida_job_id = str(uuid.uuid4())
        data_folder = os.path.join(self.DATA, ida_job_id)

        raw_text_file_path = self.pdf_to_text(ida_job_id)

        entities_file_path = self.comprehend_and_save(ida_job_id, raw_text_file_path)

        return entities_file_path
