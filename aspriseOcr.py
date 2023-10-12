# Receipt Data Extraction 
# using Accurate Real-time Receipt OCR (asprise)
# --input--
#   > receipt file (file format supported: jpeg, png, pdf, tiff)
# --output--
#   > ocr details
#   > merchant details
#   > item details
# modified by: wiwich
# modified date: 11 Oct 2023

import requests
import json 
import pandas as pd
import time

def getAspriseRequest(ref_no, image):
    url = "https://ocr.asprise.com/api/v1/receipt"

    req = requests.post(url, 
                        data = {
                            'api_key': 'TEST',
                            'recognizer': 'AU',
                            'ref_no': 'ocr_'+ref_no
                        },
                        files = {
                            'file': open(image, 'rb')
                        })
    return req

def getOcrDetailsDataFrame(receipt):
    ocr_header = ['ocr_type', 'request_id', 'ref_no', 'file_name', 'request_received_on', 'success', 'image_width', 'image_height', 'image_rotation', 'recognition_completed_on']
    
    receipt_ocr = pd.DataFrame.from_dict(receipt,orient='index').transpose()
    return receipt_ocr[ocr_header]

def getMdseDetailsDataFrame(receipt, ref_no):
    mdse_header = ['merchant_name', 'merchant_address', 'merchant_phone',
        'merchant_website', 'merchant_tax_reg_no', 'merchant_company_reg_no',
        'region', 'mall', 'country', 'receipt_no', 'date', 'time', 'currency', 'total', 'subtotal', 'tax', 'service_charge', 'tip',
        'payment_method', 'payment_details', 'credit_card_type',
        'credit_card_number', 'ocr_text', 'ocr_confidence', 'width', 'height',
        'avg_char_width', 'avg_line_height', 'conf_amount','source_locations']

    receipt_mdse = pd.DataFrame.from_dict(receipt,orient='index').transpose()
    receipt_mdse_df = receipt_mdse[mdse_header]
    receipt_mdse_df.insert(0,'ref_no','ocr_'+ref_no)
    return receipt_mdse_df

def getItemDetailsDataFrame(receipt_item, ref_no):
    receipt_item_df = pd.DataFrame.from_dict(receipt_item,orient='index').transpose()
    receipt_item_df.insert(0,'ref_no','ocr_'+ref_no)
    return receipt_item_df

def readFile(filename):
    return pd.read_csv(filename, sep='\t')

def writeFile(df, filename):
    last_df = readFile(filename)
    last_df = last_df.append(df)
    last_df = last_df.drop_duplicates()
    last_df.to_csv(filename, sep='\t', index=False)

def getReceiptDetails(image):
    ref_no = str(time.time()) # set reference no of request

    req = getAspriseRequest(ref_no, image) # get request
    receipt = json.loads(req.text) # load json

    # get OCR details
    receipt_ocr_df = getOcrDetailsDataFrame(receipt) 

    for receipt_n in range(len(receipt['receipts'])):
        rec_n = receipt['receipts'][receipt_n]

        # get Merchant details
        if receipt_n == 0:
            receipt_mdse_df = getMdseDetailsDataFrame(rec_n, ref_no)
        else:
            receipt_mdse_df = receipt_mdse_df.append(getMdseDetailsDataFrame(rec_n, ref_no), ignore_index=True)

        # get Item details   
        for item_n in range(len(rec_n.get('items'))):
            receipt_item = rec_n.get('items')[item_n]
            if item_n == 0:
                receipt_item_df = getItemDetailsDataFrame(receipt_item, ref_no)
            else:
                receipt_item_df = receipt_item_df.append(getItemDetailsDataFrame(receipt_item, ref_no), ignore_index=True)
    
    return [receipt_ocr_df, receipt_mdse_df, receipt_item_df]


if __name__ == "__main__":

    file_path = 'C:/Users/wiwich/Desktop/playground/receipt-ocr/'
    # input image
    image = file_path+"receipt-01.jpg"

    # extract receipt
    [receipt_ocr_df, receipt_mdse_df, receipt_item_df] = getReceiptDetails(image)
    
    # export file
    writeFile(receipt_ocr_df,'receipt_ocr.csv')
    writeFile(receipt_mdse_df,'receipt_merchants.csv')
    writeFile(receipt_item_df,'receipt_items.csv')





    


