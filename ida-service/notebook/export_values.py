# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import json
import numpy as np
# %%
with open("C:\\Users\\msk\\Documents\\projects\\poc-ipa\\comprehend_output\\c58266d2-6e91-447a-80a8-a7585c17f25c\\output.json", encoding='utf-8') as entities_file:
    comprehend_output_dict = json.load(entities_file)

data = pd.DataFrame(comprehend_output_dict["Entities"])
data.head()

# %%
extracted_data = {}

# %%
max_organization_score_idx = data.groupby('Type')['Score'].idxmax()["ORGANIZATION"]

ticket_type = data.iloc[max_organization_score_idx]["Text"]

if "DB" in ticket_type:
    extracted_data["type"] = "(116) ö. Fernverkehr (bspw. Fernbus) 19% / 16%  MWST.16"
else:
    extracted_data["type"] = np.nan

extracted_data["type"]

# %%

name_fields = data[(data["Type"] == "PERSON")]
if(name_fields.shape[0] != 0):
    name=""
    for field in name_fields.itertuples():
        print(field)
        name = name + " " +field.Text
        
    names = name.split(" ")[:-1]
    extracted_data["firstname"] = ' '.join(names)
    extracted_data["lastname"] = name.split(" ")[-1]
else:
    extracted_data["firstname"] = np.nan
    extracted_data["lastname"] = np.nan

print("the name is: {}, {}".format(extracted_data["firstname"], extracted_data["lastname"]))


# %%
dates = data[data["Type"] == "DATE"]

if len(extracted_data) >= 2:
    extracted_data["date"] = dates.iloc[0]["Text"] + " - " + dates.iloc[1]["Text"]
else:
    extracted_data["date"] = np.nan
extracted_data["date"]

# %%
quantity_objects_df = data[(data["Type"] == "QUANTITY")]
print(quantity_objects_df)
price_objects_df = quantity_objects_df[quantity_objects_df["Text"].str.contains(",")]
costs_list = price_objects_df["Text"].value_counts().keys().to_list()
if len(costs_list) != 0:
    extracted_data["costs"] = costs_list[0]
else:
    extracted_data["costs"] = np.nan

extracted_data["costs"]

