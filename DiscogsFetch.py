import urllib.request
import socket
import json
import urllib.parse
from dotenv import load_dotenv
import os

class Discogs():
    def __init__(self):
        load_dotenv()
        self.apikey = os.getenv("DISCOGS_KEY")
        self.secret = os.getenv("DISCOGS_SECRET")
        self.auth = f"key={self.apikey}&secret={self.secret}"
        self.headers = {
                "User-Agent": "GrailFinder/0.1 (ccoronag@uci.edu)"
            }

    def send_request(self, url):
        '''
        searches the Discogs API with the given user query.
        returns:
            result of the query as a json file
            None if fialed
        '''
        response_json = None
        try:
            print(f"CALLING: {url}")
            request = urllib.request.Request(url, headers=self.headers)
            server_response = urllib.request.urlopen(request)
            response_data = server_response.read()
            server_response.close()
            response_json = json.loads(response_data)
            print(f"CALL TO {url} COMPLETED")
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

        return response_json

    def fetch_result(self, query, search_by = "release_title", format = "album", media_type = "Vinyl", attempt = "1"):
        query = urllib.parse.quote(query)
        url = f"https://api.discogs.com/database/search?type=master&query={query}&per_page=1&page=1&{self.auth}"
        response_json = self.send_request(url)
        # print(response_json)
        if response_json != None: result_id = response_json["results"][0]["id"]
        else: return

        resource_url = response_json["results"][0]["resource_url"]
        artist = self.send_request(f"{resource_url}?{self.auth}")["artists"][0]["name"]

        url2 = f"https://api.discogs.com/masters/{result_id}/versions?format={media_type}&sort=released&sort_order=asc&page={attempt}&per_page=13;m&{self.auth}"
        master_result_json = self.send_request(url2)
        results = master_result_json["versions"]

        fetched_results = []
        count = 0
        for result in results:
            individual_search_url = f"https://api.discogs.com/marketplace/stats/{result["id"]}?{self.auth}"
            release_result_json = self.send_request(individual_search_url)
            if not release_result_json:
                continue
            address = f"https://www.discogs.com/release/{result["id"]}"



            price = release_result_json.get("lowest_price")
            if price: price = price.get("value")
            if not price:
                continue
            fetched_results.append({"address": address, 
                                      "thumb": result.get("thumb"), 
                                      "title": result.get("title"), 
                                      "artist": artist,
                                      "released": result.get("released"), 
                                      "format": result.get("format"), 
                                      "lowest_price": price})
            count += 1

        return fetched_results
    
    def fetch_picks(self):
        with open("weekly_picks.json") as f:
            picks = json.load(f)
        
        picks_data = []
        for master_id in picks["master_ids"]:
            url = f"https://api.discogs.com/masters/{master_id}?{self.auth}"
            result = self.send_request(url)
            # print(result)
            picks_data.append({
                "address": f"https://www.discogs.com/master/{master_id}",
                "thumb": self.check_img_quality(result.get("images")),
                "title": result.get("title"),
                "artist": result.get("artists")[0]["name"],
                "released": result.get("year"),
                "lowest_price": result.get("lowest_price")
            })
        
        return picks_data

    def check_img_quality(self, images: dict) :
        for image in images:
            if image.get("type") == "primary":
                return image.get("uri")

        return None
        