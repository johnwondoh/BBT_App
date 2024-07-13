import boto3
import pandas as pd
import json
from decimal import Decimal
import uuid

#
# print(table)
# print(response["ResponseMetadata"]["HTTPStatusCode"])

def changeDateFormat(date_val):
    arr = date_val.split('/')
    return '-'.join([arr[2], arr[1], arr[0]])


print(changeDateFormat('29/7/2023'))

revenue_df = pd.read_csv('../BBT_Asset.csv')


# revenue_df['Date'] = revenue_df['Date'].apply(lambda x: changeDateFormat(x))
revenue_df['ID'] = [uuid.uuid4().hex for _ in range(len(revenue_df.index))]
revenue_df['Created_By'] = [None for _ in range(len(revenue_df.index))]
# revenue_df['Exchange_Rate'] = [None for _ in range(len(revenue_df.index))]

print(revenue_df.head())

#  ---- DyanamoDB stuff --------------
# __TableName__ = 'Asset'
# #
# DB = boto3.resource('dynamodb', region_name='ap-southeast-2')
# table = DB.Table(__TableName__)
#
# for index, row in revenue_df.iterrows():
#     put_item = json.loads(row.to_json(), parse_float=Decimal)
#     print(put_item)
#     res = table.put_item(
#         Item=put_item
#     )
#     print(res)
#     print(put_item)




# response = table.put_item(
#     Item={
#         "ID": "sfadfadf"
#     }
# )



