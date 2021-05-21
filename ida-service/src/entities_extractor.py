import json
import numpy as np
import pandas as pd

class EntitiesExtractor:
   """Contains all logic to extract relevant information from the recognized entities and save them to a dictionary in the expected format.
   It currently works for DB Tickets.
   """

   def __init__(self, entities_file_path):
        """
        Initializes the EntitiesExtractor, with the output file of NER.
         :param entities_file_path: the file that came as output from the NER Service
        """
        super().__init__()
        self.entities_file_path = entities_file_path
        self.extracted_data = {}
        
        with open(entities_file_path, encoding='utf-8') as entities_file_path:
            comprehend_output_dict = json.load(entities_file_path)
        
        self.data =  pd.DataFrame(comprehend_output_dict["Entities"])
 

   def extract_organization(self):
      """Extracts the organization from the recognized entities file. Currently it only works for DB."""
      
      globals().update(self.__dict__)

      max_organization_score_idx = data.groupby('Type')['Score'].idxmax()["ORGANIZATION"]
      ticket_type = data.iloc[max_organization_score_idx]["Text"]
      if "DB" in ticket_type:
         extracted_data["type"] = "(116) ö. Fernverkehr (bspw. Fernbus) 19% / 16%  MWST.16"
      else:
         extracted_data["type"] = np.nan

   def extract_name(self):
      """Extracts the full name (firstname, lastname) from the recognized entities file."""

      globals().update(self.__dict__)

      name_fields = data[(data["Type"] == "PERSON")]
      if(name_fields.shape[0] != 0):
         name=""
         for field in name_fields.itertuples():
               name = name + " " +field.Text
               
         names = name.split(" ")[:-1]
         extracted_data["firstname"] = ' '.join(names)
         extracted_data["lastname"] = name.split(" ")[-1]
      else:
         extracted_data["firstname"] = np.nan
         extracted_data["lastname"] = np.nan

   def extract_dates(self):
      """Extract the dates of the trip from the receipt. The departure and arrival date will be saved in one string."""
      globals().update(self.__dict__)

      dates = data[data["Type"] == "DATE"]

      if len(extracted_data) >= 2:
        extracted_data["date"] = dates.iloc[0]["Text"] + " - " + dates.iloc[1]["Text"]
      else:
        extracted_data["date"] = np.nan

   def extract_costs(self):
      """Extract the total amound of money paid for the ticket."""
      
      globals().update(self.__dict__)

      quantity_objects_df = data[(data["Type"] == "QUANTITY")]
      price_objects_df = quantity_objects_df[quantity_objects_df["Text"].str.contains(",")]
      costs_list = price_objects_df["Text"].value_counts().keys().to_list()
      if len(costs_list) != 0:
         extracted_data["costs"] = costs_list[0]
      else:
         extracted_data["costs"] = np.nan

   def extract(self):
      """Contains the logic to extract the expected data from the entities file. Returns a dictionary with the extracted values."""
      self.extract_organization()
      self.extract_name()
      self.extract_dates()
      self.extract_costs()

      return self.extracted_data