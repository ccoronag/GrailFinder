from EbayFetch import Ebay, EbayAuthTokenError

ebay = Ebay()
try:
    ebay_results = ebay.fetch_result("shirt")
except EbayAuthTokenError as e:
    # The token was invalid
    ebay_results = ebay.fetch_result("shirt")

if not ebay_results:
    exit()

for item in ebay_results:
    print(item)