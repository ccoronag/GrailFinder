import urllib.request
import socket
import json
import base64
from dotenv import load_dotenv
import os


class EbayAPIError(Exception):
    pass

class EbayAuthTokenError(EbayAPIError):
    pass

class Ebay():
    def __init__(self):
        load_dotenv()

        self.appid = os.getenv("EBAY_APPID")
        self.certid = os.getenv("EBAY_SECRET")
        self.credentials = f"{self.appid}:{self.certid}"
        self.encoded = base64.b64encode(self.credentials.encode("utf-8")).decode("utf-8")
        self.token_headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {self.encoded}"
        }
        self.request_body = urllib.parse.urlencode({
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope"
        }).encode("utf-8")
        self.current_token = None
        
    def get_auth_token(self):
        '''
        Ebay's API requires client or user tokens when dealing with it, so before actually calling the api, we retrieve 
        a token from the authorization API.
        '''
        sandbox_url = "https://api.ebay.com/identity/v1/oauth2/token"

        try:
            request = urllib.request.Request(sandbox_url, data=self.request_body, headers=self.token_headers)
            response = urllib.request.urlopen(request)
            token_info = json.loads(response.read().decode("utf-8"))
            response.close()
        except urllib.error.HTTPError as e:
            print('Failed to download contents of URL')
            print('Status code: {}'.format(e.code))
            error_code = e.code
            if (error_code == 404) or (error_code == 503):
                print('This API is currently unavailable')
            return
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.gaierror):
                print('Error connecting to the URL: Check your internet connection')
            else:
                print('Error connecting to the URL')
            return
        except ValueError as val_err:
            print(f'Error processing API response: {val_err}')
            return
        except Exception as err:
            print(f'An unexpected error occurred: {err}')
            return
        return token_info["access_token"]
    
    def fetch_result(self, query, format="Vinyl"):
        if not self.current_token:
            print("Fetching Ebay auth Token...")
            self.current_token = self.get_auth_token()
    
        if format == "Vinyl": cat_id = "176985" 
        else: cat_id = "11233"

        base_url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
        query_params = urllib.parse.urlencode({
            "q": query,
            "limit": 15,
            "category_ids": cat_id
        })

        url = f"{base_url}?{query_params}"

        headers = {
            "Authorization": f"Bearer {self.current_token}",
            "Content-Type": "application/json"
        }
        fetched_results = []
        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            results = json.loads(response.read().decode("utf-8"))
            response.close()
        except urllib.error.HTTPError as e:
            print('Failed to download contents of URL')
            print('Status code: {}'.format(e.code))
            error_code = e.code
            if (error_code == 404) or (error_code == 503):
                print('This API is currently unavailable')
                return []
            elif (error_code == 401):
                print("The eBay auth token has expired")
                self.current_token = self.get_auth_token()
                raise EbayAuthTokenError(f"Current Auth token failed or has expired")
                
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.gaierror):
                print('Error connecting to the URL: Check your internet connection')
            else:
                print('Error connecting to the URL')
            return []
        except ValueError as val_err:
            print(f'Error processing API response: {val_err}')
            return []
        except Exception as err:
            print(f'An unexpected error occurred: {err}')
            return []
        
        
        # print(results)
        if not results:
            return fetched_results
        for item in results.get("itemSummaries", []):
            fetched_results.append({
                "address": item.get("itemWebUrl"), 
                "thumb": item.get("thumbnailImages", [{}])[0].get("imageUrl"), 
                "title": item.get("title"), 
                "price": item.get("price").get("value"), 
                "seller": item.get("seller")})

        return fetched_results