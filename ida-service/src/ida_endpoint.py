import camunda_external_task
import entities_extractor
import intelligent_document_service
import logging
import os
import requests
import urllib.request

PROCESS_ENGINE_URL = "http://camunda:8080/engine-rest"

def create_file_path(dest_folder, file_name):
    '''
    Creates a destination folder if not exists, and returns the full file path (including file name). 
    
    Args:
        dest_folder (str): path of the destination folder
        file_name (str): the file_name
    
    Returns:
        path : the path of the newly created path including file name
    '''
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    file_path = os.path.join(dest_folder, file_name)
    return file_path

def get_invoice_file(url, processInstanceId):
    '''
    Gets the invoice file from the process as bytes and saves it locally as a temporary file.

    Args:
        url (str): The url of camunda to connect to
            processInstanceId (String): the id of the process instance the external task is connected to

    Returns:
        file_path : the path of the newly created file
    '''
    response = requests.get(url + "/process-instance/"+processInstanceId+"/variables/invoice_document/data")

    file_path = create_file_path("../data", "invoice.pdf")

    with open(file_path, 'w+b') as f:
        invoice_byte_arr = response.content
        binary_format = bytearray(invoice_byte_arr)
        f.write(binary_format)

    return file_path
   
def extract_data_from_file_to_dict(file_path):
    """
    Calls intelligent document recognition service and extracts the recognized entities to a dictionary.
    
    Args:
        file_path: the full path of the file to analyze
    
    Returns: 
        extracted_values_dict: a dictionary containing the extracted values. 
            Currently: {type: (String), firstname: (String), lastname: (String), date: (string), costs: (string)}
    """
    ida_client = intelligent_document_service.IntelligentDocumentAnalyzer(file_path)
    results_output_path = ida_client.run()
    
    extracted_values_dict = entities_extractor.EntitiesExtractor(results_output_path).extract()
    return extracted_values_dict

def main():
    logging.info("Intelligent Document Analysis is running")
    while(True):
        camunda_client= camunda_external_task.client(PROCESS_ENGINE_URL, "ida_task")
        camunda_client.subscribe(topic = "IDA")

        file_path = get_invoice_file(PROCESS_ENGINE_URL, camunda_client.processInstanceId)
        
        extracted_values_dict = extract_data_from_file_to_dict(file_path)
        
        camunda_client.complete(**extracted_values_dict)
        
        logging.info("WorkerId: {} of process instance id: {} completed".format(camunda_client.workerid, camunda_client.processInstanceId))
    return 
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()