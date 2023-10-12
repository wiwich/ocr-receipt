# Receipt OCR

## Should to know 
- **Invoices** and **Receipts** have different purpose: invoices is issued before the payment whereas receipts is issued after the payment [1]

## Receipt components
- Company business information: name, address, and phone number
- Sale date and time
- Transaction Number
- Product or service description 
- Cost
- Tax (if required)

## Data Extraction

## Receipt OCR
### [20231011] Asprise receipt
Use 'Asprise receipt OCR' (Accurate Real-time Receipt OCR: http://asprise.com/receipt-ocr-data-capture-api/extract-text-reader-scanner-index.html) [2] This API has a rate limit of 500 requests within one day per IP address.

**Post Request**
The post request to the receipt OCR API in Python.
```
# View complete code at: https://github.com/Asprise/receipt-ocr/tree/main/python-receipt-ocr
import requests

print("=== Python Receipt OCR Demo - Need help? Email support@asprise.com ===")

receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt' # Receipt OCR API endpoint
imageFile = "receipt.jpg" # // Modify this to use your own file if necessary
r = requests.post(receiptOcrEndpoint, data = { \
  'api_key': 'TEST',        # Use 'TEST' for testing purpose \
  'recognizer': 'auto',       # can be 'US', 'CA', 'JP', 'SG' or 'auto' \
  'ref_no': 'ocr_python_123', # optional caller provided ref code \
  }, \
  files = {"file": open(imageFile, "rb")})

print(r.text) # result in JSON
```

**Request Parameters**
  *api_key* (string, required)
  *recognizer* (string, required)
  *file* (file, required)
  *ref_no (string, optional)
  *mapping_rule_set* (string, optional)

**Receipt Object**
Receipt object properties include: 
- `merchant_name` Name of the merchant
- `merchant_address` Address of the merchant
- `merchant_phone` Phone number
- `merchant_website` Website if any
- `merchant_tax_reg_no` Tax registration number
- `merchant_company_reg_no` Company registration number
- `merchant_logo` URL of the merchant logo image
- `region` Region or area
- `mall` Mall
etc.
Preperties of a line item object:
- `amount` Amount of the line item
- `description` Description
- `flags` Text after amount indicating tax status
- `qty` Quantity
- `remarks` Remarks
- `unitPrice` Unit price

*API can detect more than one receipt*








**References**
 [1] https://parsio.io/blog/extract-data-from-pdf-receipt/#:~:text=Receipts%20Data%20Extraction%20With%20the%20Zonal%20OCR&text=OCR%20scans%20an%20image%20of,the%20data%20from%20these%20fields.
 [2] http://asprise.com/ocr/api/docs/html/receipt-ocr.html
