# Scraper for Amazon price tracking. Uses BeautifulSoup4 library.

Requirements need to be installed separately. Installed in venv (See tutorials in youtube) and venv path specific in pythonshell node. /data is the nodered root directly in my case. 

pip install Beautifulsoup4
pip install requests

The nodered flow is to invoke the py script (using pythonshell node) in a layman friendly manner and provide the amazon URL as input. 

Once the script is executed and the product price details are output by the script, the next node filter and convert to json.

The function node formats the product and price to send the price to influxdb for visualization.

The price compare node compares price against a price set by you for the product and if the price is below the set price, the product details along with price are set to a telegram bot which is part of a telegram group so that users receive the price alert immediately.

Users can click the url and purchase the product if they like the price.

The trigger frequency for the script can be set in the inject node along with the product url. Amazon can identify scripts polling their websites and block IP's of user that poll too often, so better to maintain a 20-30 min frequency.

The same flow can be replicated to track multiple products. need to change url in inject node. Measurement name in influxdb and price in compare node.




