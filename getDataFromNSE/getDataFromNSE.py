import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup 
import bs4
import csv
import datetime, timedelta
import time
import os
from fuzzywuzzy import fuzz

class data:

	# def __init__(indexName,full_data=None,start_date=None,end_date=None,indextype=None):
	# 	self.indexName = indexName
	# 	self.full_data = full_data
	# 	self.start_date = start_date
	# 	self.end_date = end_date
	# 	self.indextype = in


	def returns(self,indexName,full_data=None,start_date=None,end_date=None,indextype=None):
		self.indexName = indexName
		self.indextype = indextype

		
		##Setting by default to be historical	

		result=[];
		if(full_data ==None or full_data=="No"):
			x=datetime.datetime.strptime(start_date,"%d-%m-%Y")
			y=datetime.datetime.strptime(end_date,"%d-%m-%Y")

			if(x>y):
				raise ValueError("Starting date is greater than end date.")

			# Checking for proper IndexName and suggesting closest alternative.
			flag=0;
			for i in range(len(arr)):
				if(arr[i]==indexName or values[i]==indexName):
					indexName = arr[i]
					print(indexName)
					flag=1

			maxi = 0
			maxVal = values[0];

			indexName = indexName.replace(" ","%20")
			# print("HAAA")
			#Downloading Data
			result = pd.DataFrame()
			while(True):
					if((y-x).days<365):
						try:
							# print(1)
							fromdate= x.strftime("%d-%m-%Y")
							# print(fromdate)
							todate=y.strftime("%d-%m-%Y")
							url = first + '?indexType='+(indexName)+ '&fromDate='+ fromdate + '&toDate='+ todate;			
							headers = {
								"Host": "www1.nseindia.com",
								"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0",
								"Accept": "*/*",
								"Accept-Language": "en-US,en;q=0.5",
								"Accept-Encoding": "gzip, deflate, br",
								"X-Requested-With": "XMLHttpRequest",
								"Referer": "https://www1.nseindia.com/products/content/equities/equities/eq_security.htm",
								"Access-Control-Allow-Origin" : "*",
								"Access-Control-Allow-Methods" : "GET,POST,PUT,DELETE,OPTIONS",
								"Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With",
								'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'
							}
							response = requests.get(url, timeout=240,headers=headers)
							page_content = BeautifulSoup(response.content, "html.parser")

							a=page_content.find(id="csvContentDiv").get_text();
							a = a.replace(':',", \n")


							with open("data.csv", "w") as f:
								f.write(a)

							df = pd.read_csv("data.csv")
							df.set_index("Date",inplace=True)
							df = df[::-1]
							result = pd.concat([result,df])
							break;

						except AttributeError:
							break

					if ((y-x).days > 365 ):
						try:
							# print(0)
							todate= y.strftime("%d-%m-%Y")
							fromdate = ( y - datetime.timedelta(days=364) ).strftime("%d-%m-%Y")
							inter =  y - datetime.timedelta(days=364) 
							# print(todate)
							url = first + '?indexType='+(indexName)+ '&fromDate='+ fromdate + '&toDate='+ todate;			
							headers = {
								"Host": "www1.nseindia.com",
								"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0",
								"Accept": "*/*",
								"Accept-Language": "en-US,en;q=0.5",
								"Accept-Encoding": "gzip, deflate, br",
								"X-Requested-With": "XMLHttpRequest",
								"Referer": "https://www1.nseindia.com/products/content/equities/equities/eq_security.htm",
								"Access-Control-Allow-Origin" : "*",
								"Access-Control-Allow-Methods" : "GET,POST,PUT,DELETE,OPTIONS",
								"Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With",
								'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'
							}

							response = requests.get(url, timeout=10,headers=headers)
							page_content = BeautifulSoup(response.content, "html.parser")

							a=page_content.find(id="csvContentDiv").get_text();
							a = a.replace(':',", \n")
							# print(a)


							with open("data.csv", "w") as f:
								f.write(a)

							df = pd.read_csv("data.csv")
							df.set_index("Date",inplace=True)
							df = df[::-1]
							result = pd.concat([result,df])
							y = ( inter - datetime.timedelta(days=1) )

						except AttributeError:
							break;

			
		elif(full_data =="Yes" or full_data=="yes"):
			
				# Checking for proper IndexName and suggesting closest alternative.
				flag=0;
				for i in range(len(arr)):
					if(arr[i]==indexName or values[i]==indexName):
						indexName = arr[i]
						print(indexName)
						flag=1

				maxi = 0
				maxVal = values[0];
				for compare in values:
					str1 = indexName
					str2 = compare

					Ratio = fuzz.ratio(str1.lower(),str2.lower())
					if(Ratio>maxi):
						maxVal = compare
						maxi = Ratio

				if(flag==0):
					raise ValueError("Check Index name. Try {} as index name".format(maxVal))

				x=datetime.datetime.now()
				y=datetime.datetime.now() - datetime.timedelta(days=364)

				result = pd.DataFrame()
				i=0;
				while(True):
					try:
						print("Stage ",i)
						todate=x.strftime("%d-%m-%Y")
						fromdate= y.strftime("%d-%m-%Y")

						url = first + '?indexType='+(indexName)+ '&fromDate='+ fromdate + '&toDate='+ todate;			
						headers = {
								"Host": "www1.nseindia.com",
								"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0",
								"Accept": "*/*",
								"Accept-Language": "en-US,en;q=0.5",
								"Accept-Encoding": "gzip, deflate, br",
								"X-Requested-With": "XMLHttpRequest",
								"Referer": "https://www1.nseindia.com/products/content/equities/equities/eq_security.htm",
								"Access-Control-Allow-Origin" : "*",
								"Access-Control-Allow-Methods" : "GET,POST,PUT,DELETE,OPTIONS",
								"Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With",
								'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'
						}
						response = requests.get(url, timeout=10,headers=headers)
						page_content = BeautifulSoup(response.content, "html.parser")

						a=page_content.find(id="csvContentDiv").get_text();
						a = a.replace(':',", \n")

						with open("data.csv", "w") as f:
							f.write(a)

						df = pd.read_csv("data.csv")
						df.set_index("Date",inplace=True)
						df = df[::-1]
						result = pd.concat([result,df])

						x = y - datetime.timedelta(days=1)
						y = x - datetime.timedelta(days=364)
						i=i+1
					except AttributeError:
						# print("YES")
						break;
		try:
			os.remove("data.csv")
		except(OSError):
			pass


		return result;

	def returnsToCSV(self,data,link=None):
		try:
			if(link==None):
				data.to_csv(self.indexName+".csv")
				print("Data stored as csv in the name {}.csv".format(self.indexName))
			else:
				data.to_csv(link+"/{}.csv".format(self.indexName))
				print("Data stored as csv in the name {}.csv".format(self.indexName))

		except (AttributeError):
			print("Check data")


	def returnsToCSVStocks(self,data,link=None):
		try:
			if(link==None):
				data.to_csv(self.stockSymbol+".csv")
				print("Data stored as csv in the name {}.csv".format(self.stockSymbol))

			else:
				data.to_csv(link+"/{}.csv".format(self.stockSymbol))
				print("Data stored as csv in the name {}.csv".format(self.stockSymbol))

		except (AttributeError):
			print("Check data")


	def returnsForStocks(self,stockSymbol,full_data=None,start_date=None,end_date=None):
		values = ['20MICRONS', '21STCENMGM', '3IINFOTECH', '3MINDIA', '3PLAND', '5PAISA', '63MOONS', '8KMILES', 'A2ZINFRA', 'AARTIDRUGS', 'AARTIIND', 'AARVEEDEN', 'AAVAS', 'ABAN', 'ABB', 'ABBOTINDIA', 'ABCAPITAL', 'ABFRL', 'ABMINTLTD', 'ACC', 'ACCELYA', 'ACE', 'ADANIENT', 'ADANIGAS', 'ADANIGREEN', 'ADANIPORTS', 'ADANIPOWER', 'ADANITRANS', 'ADFFOODS', 'ADHUNIK', 'ADHUNIKIND', 'ADLABS', 'ADORWELD', 'ADROITINFO', 'ADSL', 'ADVANIHOTR', 'ADVENZYMES', 'AEGISCHEM', 'AFFLE', 'AGARIND', 'AGCNET', 'AGRITECH', 'AGROPHOS', 'AHLEAST', 'AHLUCONT', 'AHLWEST', 'AIAENG', 'AIONJSW', 'AIRAN', 'AJANTPHARM', 'AJMERA', 'AKASH', 'AKSHARCHEM', 'AKSHOPTFBR', 'AKZOINDIA', 'ALANKIT', 'ALBERTDAVD', 'ALBK', 'ALCHEM', 'ALEMBICLTD', 'ALICON', 'ALKALI', 'ALKEM', 'ALKYLAMINE', 'ALLCARGO', 'ALLSEC', 'ALMONDZ', 'ALOKTEXT', 'ALPA', 'ALPHAGEO', 'ALPSINDUS', 'AMARAJABAT', 'AMBER', 'AMBIKCO', 'AMBUJACEM', 'AMDIND', 'AMJLAND', 'AMRUTANJAN', 'ANANTRAJ', 'ANDHRABANK', 'ANDHRACEMT', 'ANDHRSUGAR', 'ANIKINDS', 'ANKITMETAL', 'ANSALAPI', 'ANSALHSG', 'ANTGRAPHIC', 'ANUP', 'APARINDS', 'APCL', 'APCOTEXIND', 'APEX', 'APLAPOLLO', 'APLLTD', 'APOLLO', 'APOLLOHOSP', 'APOLLOTYRE', 'APOLSINHOT', 'APTECHT', 'ARCHIDPLY', 'ARCHIES', 'ARCOTECH', 'ARENTERP', 'ARIES', 'ARIHANT', 'ARIHANTSUP', 'ARMANFIN', 'AROGRANITE', 'ARROWGREEN', 'ARROWTEX', 'ARSHIYA', 'ARSSINFRA', 'ARVIND', 'ARVINDFASN', 'ARVSMART', 'ASAHIINDIA', 'ASAHISONG', 'ASAL', 'ASHAPURMIN', 'ASHIANA', 'ASHIMASYN', 'ASHOKA', 'ASHOKLEY', 'ASIANHOTNR', 'ASIANPAINT', 'ASIANTILES', 'ASPINWALL', 'ASSAMCO', 'ASTEC', 'ASTERDM', 'ASTRAL', 'ASTRAMICRO', 'ASTRAZEN', 'ASTRON', 'ATFL', 'ATLANTA', 'ATLASCYCLE', 'ATUL', 'ATULAUTO', 'AUBANK', 'AURIONPRO', 'AUROPHARMA', 'AUSOMENT', 'AUTOAXLES', 'AUTOIND', 'AUTOLITIND', 'AVADHSUGAR', 'AVANTIFEED', 'AVTNPL', 'AXISBANK', 'AXISCADES', 'AYMSYNTEX', 'BAGFILMS', 'BAJAJ-AUTO', 'BAJAJCON', 'BAJAJELEC', 'BAJAJFINSV', 'BAJAJHIND', 'BAJAJHLDNG', 'BAJFINANCE', 'BALAJITELE', 'BALAMINES', 'BALAXI', 'BALKRISHNA', 'BALKRISIND', 'BALLARPUR', 'BALMLAWRIE', 'BALPHARMA', 'BALRAMCHIN', 'BANARBEADS', 'BANARISUG', 'BANCOINDIA', 'BANDHANBNK', 'BANG', 'BANKBARODA', 'BANKINDIA', 'BANSWRAS', 'BARTRONICS', 'BASF', 'BASML', 'BATAINDIA', 'BAYERCROP', 'BBL', 'BBTC', 'BCG', 'BCP', 'BDL', 'BEARDSELL', 'BEDMUTHA', 'BEL', 'BEML', 'BEPL', 'BERGEPAINT', 'BFINVEST', 'BFUTILITIE', 'BGLOBAL', 'BGRENERGY', 'BHAGERIA', 'BHAGYANGR', 'BHAGYAPROP', 'BHANDARI', 'BHARATFORG', 'BHARATGEAR', 'BHARATRAS', 'BHARATWIRE', 'BHARTIARTL', 'BHEL', 'BIGBLOC', 'BIL', 'BILENERGY', 'BINANIIND', 'BINDALAGRO', 'BIOCON', 'BIOFILCHEM', 'BIRLACABLE', 'BIRLACORPN', 'BIRLAMONEY', 'BKMINDST', 'BLBLIMITED', 'BLISSGVS', 'BLKASHYAP', 'BLS', 'BLUEBLENDS', 'BLUECOAST', 'BLUEDART', 'BLUESTARCO', 'BODALCHEM', 'BOMDYEING', 'BOROSIL', 'BOSCHLTD', 'BPCL', 'BPL', 'BRFL', 'BRIGADE', 'BRITANNIA', 'BRNL', 'BROOKS', 'BSE', 'BSELINFRA', 'BSL', 'BSOFT', 'BURNPUR', 'BUTTERFLY', 'BVCL', 'BYKE', 'CADILAHC', 'CALSOFT', 'CAMLINFINE', 'CANBK', 'CANDC', 'CANFINHOME', 'CANTABIL', 'CAPACITE', 'CAPLIPOINT', 'CAPTRUST', 'CARBORUNIV', 'CAREERP', 'CARERATING', 'CASTEXTECH', 'CASTROLIND', 'CCHHL', 'CCL', 'CDSL', 'CEATLTD', 'CEBBCO', 'CELEBRITY', 'CELESTIAL', 'CENTENKA', 'CENTEXT', 'CENTRALBK', 'CENTRUM', 'CENTUM', 'CENTURYPLY', 'CENTURYTEX', 'CERA', 'CEREBRAINT', 'CESC', 'CESCVENT', 'CGCL', 'CGPOWER', 'CHALET', 'CHAMBLFERT', 'CHEMFAB', 'CHENNPETRO', 'CHOLAFIN', 'CHOLAHLDNG', 'CHROMATIC', 'CIGNITITEC', 'CIMMCO', 'CINELINE', 'CINEVISTA', 'CIPLA', 'CKFSL', 'CLEDUCATE', 'CLNINDIA', 'CMICABLES', 'CNOVAPETRO', 'COALINDIA', 'COCHINSHIP', 'COFFEEDAY', 'COLPAL', 'COMPINFO', 'COMPUSOFT', 'CONCOR', 'CONFIPET', 'CONSOFINVT', 'CONTROLPR', 'CORALFINAC', 'CORDSCABLE', 'COROMANDEL', 'CORPBANK', 'COSMOFILMS', 'COUNCODOS', 'COX&KINGS', 'CREATIVE', 'CREATIVEYE', 'CREDITACC', 'CREST', 'CRISIL', 'CROMPTON', 'CTE', 'CUB', 'CUBEXTUB', 'CUMMINSIND', 'CUPID', 'CURATECH', 'CYBERMEDIA', 'CYBERTECH', 'CYIENT', 'DAAWAT', 'DABUR', 'DALBHARAT', 'DALMIASUG', 'DAMODARIND', 'DATAMATICS', 'DBCORP', 'DBL', 'DBREALTY', 'DBSTOCKBRO', 'DCAL', 'DCBBANK', 'DCM', 'DCMFINSERV', 'DCMNVL', 'DCMSHRIRAM', 'DCW', 'DECCANCE', 'DEEPAKFERT', 'DEEPAKNTR', 'DEEPIND', 'DELTACORP', 'DELTAMAGNT', 'DEN', 'DENORA', 'DFMFOODS', 'DGCONTENT', 'DHAMPURSUG', 'DHANBANK', 'DHANUKA', 'DHARSUGAR', 'DHFL', 'DHUNINV', 'DIAMONDYD', 'DIAPOWER', 'DICIND', 'DIGISPICE', 'DIGJAMLTD', 'DISHTV', 'DIVISLAB', 'DIXON', 'DLF', 'DLINKINDIA', 'DMART', 'DNAMEDIA', 'DOLAT', 'DOLLAR', 'DOLPHINOFF', 'DONEAR', 'DPSCLTD', 'DQE', 'DREDGECORP', 'DRREDDY', 'DSSL', 'DTIL', 'DUCON', 'DVL', 'DWARKESH', 'DYNAMATECH', 'DYNPRO', 'EASTSILK', 'EASUNREYRL', 'ECLERX', 'EDELWEISS', 'EDL', 'EDUCOMP', 'EICHERMOT', 'EIDPARRY', 'EIHAHOTELS', 'EIHOTEL', 'EIMCOELECO', 'EKC', 'ELECON', 'ELECTCAST', 'ELECTHERM', 'ELGIEQUIP', 'ELGIRUBCO', 'EMAMILTD', 'EMAMIPAP', 'EMAMIREAL', 'EMCO', 'EMKAY', 'EMMBI', 'ENDURANCE', 'ENERGYDEV', 'ENGINERSIN', 'ENIL', 'EON', 'EQUITAS', 'ERIS', 'EROSMEDIA', 'ESABINDIA', 'ESCORTS', 'ESSARSHPNG', 'ESSELPACK', 'ESTER', 'EUROCERA', 'EUROMULTI', 'EUROTEXIND', 'EVEREADY', 'EVERESTIND', 'EXCEL', 'EXCELINDUS', 'EXIDEIND', 'EXPLEOSOL', 'FACT', 'FAIRCHEM', 'FCL', 'FCONSUMER', 'FCSSOFT', 'FDC', 'FEDERALBNK', 'FEL', 'FELDVR', 'FIEMIND', 'FILATEX', 'FINCABLES', 'FINEORG', 'FINPIPE', 'FLEXITUFF', 'FLFL', 'FLUOROCHEM', 'FMGOETZE', 'FMNL', 'FORCEMOT', 'FORTIS', 'FOSECOIND', 'FRETAIL', 'FSC', 'FSL', 'GABRIEL', 'GAEL', 'GAIL', 'GAL', 'GALAXYSURF', 'GALLANTT', 'GALLISPAT', 'GAMMNINFRA', 'GANDHITUBE', 'GANECOS', 'GANESHHOUC', 'GANGESSECU', 'GANGOTRI', 'GARDENSILK', 'GARFIBRES', 'GATI', 'GAYAHWS', 'GAYAPROJ', 'GDL', 'GEECEE', 'GENESYS', 'GENUSPAPER', 'GENUSPOWER', 'GEOJITFSL', 'GEPIL', 'GESHIP', 'GET&D', 'GFLLIMITED', 'GFSTEELS', 'GHCL', 'GICHSGFIN', 'GICRE', 'GILLANDERS', 'GILLETTE', 'GINNIFILA', 'GIPCL', 'GISOLUTION', 'GKWLIMITED', 'GLAXO', 'GLENMARK', 'GLFL', 'GLOBALVECT', 'GLOBOFFS', 'GLOBUSSPR', 'GMBREW', 'GMDCLTD', 'GMMPFAUDLR', 'GMRINFRA', 'GNA', 'GNFC', 'GOACARBON', 'GOCLCORP', 'GODFRYPHLP', 'GODREJAGRO', 'GODREJCP', 'GODREJIND', 'GODREJPROP', 'GOENKA', 'GOKEX', 'GOKUL', 'GOKULAGRO', 'GOLDENTOBC', 'GOLDIAM', 'GOLDTECH', 'GOODLUCK', 'GPIL', 'GPPL', 'GPTINFRA', 'GRANULES', 'GRAPHITE', 'GRASIM', 'GRAVITA', 'GREAVESCOT', 'GREENLAM', 'GREENPANEL', 'GREENPLY', 'GREENPOWER', 'GRINDWELL', 'GROBTEA', 'GRPLTD', 'GRSE', 'GSCLCEMENT', 'GSFC', 'GSKCONS', 'GSPL', 'GSS', 'GTL', 'GTLINFRA', 'GTNIND', 'GTNTEX', 'GTPL', 'GUFICBIO', 'GUJALKALI', 'GUJAPOLLO', 'GUJGASLTD', 'GUJRAFFIA', 'GULFOILLUB', 'GULFPETRO', 'GULPOLY', 'GVKPIL', 'HAL', 'HARITASEAT', 'HARRMALAYA', 'HATHWAY', 'HATSUN', 'HAVELLS', 'HAVISHA', 'HBLPOWER', 'HBSL', 'HCC', 'HCG', 'HCL-INSYS', 'HCLTECH', 'HDFC', 'HDFCAMC', 'HDFCBANK', 'HDFCLIFE', 'HDIL', 'HEG', 'HEIDELBERG', 'HERCULES', 'HERITGFOOD', 'HEROMOTOCO', 'HESTERBIO', 'HEXATRADEX', 'HEXAWARE', 'HFCL', 'HGINFRA', 'HGS', 'HIGHGROUND', 'HIKAL', 'HIL', 'HILTON', 'HIMATSEIDE', 'HINDALCO', 'HINDCOMPOS', 'HINDCOPPER', 'HINDMOTORS', 'HINDNATGLS', 'HINDOILEXP', 'HINDPETRO', 'HINDSYNTEX', 'HINDUJAVEN', 'HINDUNILVR', 'HINDZINC', 'HIRECT', 'HISARMETAL', 'HITECH', 'HITECHCORP', 'HITECHGEAR', 'HMT', 'HMVL', 'HNDFDS', 'HONAUT', 'HONDAPOWER', 'HOTELEELA', 'HOTELRUGBY', 'HOVS', 'HPL', 'HSCL', 'HSIL', 'HTMEDIA', 'HUBTOWN', 'HUDCO', 'IBREALEST', 'IBULHSGFIN', 'IBULISL', 'IBVENTURES', 'ICICIBANK', 'ICICIGI', 'ICICIPRULI', 'ICIL', 'ICRA', 'IDBI', 'IDEA', 'IDFC', 'IDFCFIRSTB', 'IEX', 'IFBAGRO', 'IFBIND', 'IFCI', 'IFGLEXPOR', 'IGARASHI', 'IGL', 'IGPL', 'IIFL', 'IIFLSEC', 'IIFLWAM', 'IITL', 'IL&FSENGG', 'IL&FSTRANS', 'IMFA', 'IMPAL', 'IMPEXFERRO', 'INDBANK', 'INDHOTEL', 'INDIACEM', 'INDIAGLYCO', 'INDIAMART', 'INDIANB', 'INDIANCARD', 'INDIANHUME', 'INDIGO', 'INDLMETER', 'INDNIPPON', 'INDOCO', 'INDORAMA', 'INDOSOLAR', 'INDOSTAR', 'INDOTECH', 'INDOTHAI', 'INDOWIND', 'INDRAMEDCO', 'INDSWFTLAB', 'INDSWFTLTD', 'INDTERRAIN', 'INDUSINDBK', 'INEOSSTYRO', 'INFIBEAM', 'INFOBEAN', 'INFRATEL', 'INFY', 'INGERRAND', 'INOXLEISUR', 'INOXWIND', 'INSECTICID', 'INSPIRISYS', 'INTEGRA', 'INTELLECT', 'INTENTECH', 'INVENTURE', 'IOB', 'IOC', 'IOLCP', 'IPAPPM', 'IPCALAB', 'IRB', 'IRCON', 'IRCTC', 'ISEC', 'ISFT', 'ISMTLTD', 'ITC', 'ITDC', 'ITDCEM', 'ITI', 'IVC', 'IVP', 'IVRCLINFRA', 'IZMO', 'J&KBANK', 'JAGRAN', 'JAGSNPHARM', 'JAIBALAJI', 'JAICORPLTD', 'JAIHINDPRO', 'JAINSTUDIO', 'JAMNAAUTO', 'JAYAGROGN', 'JAYBARMARU', 'JAYNECOIND', 'JAYSREETEA', 'JBCHEPHARM', 'JBFIND', 'JBMA', 'JCHAC', 'JETAIRWAYS', 'JHS', 'JIKIND', 'JINDALPHOT', 'JINDALPOLY', 'JINDALSAW', 'JINDALSTEL', 'JINDCOT', 'JINDRILL', 'JINDWORLD', 'JISLDVREQS', 'JISLJALEQS', 'JITFINFRA', 'JIYAECO', 'JKCEMENT', 'JKIL', 'JKLAKSHMI', 'JKPAPER', 'JKTYRE', 'JMA', 'JMCPROJECT', 'JMFINANCIL', 'JMTAUTOLTD', 'JOCIL', 'JPASSOCIAT', 'JPINFRATEC', 'JPOLYINVST', 'JPPOWER', 'JSL', 'JSLHISAR', 'JSWENERGY', 'JSWHL', 'JSWSTEEL', 'JTEKTINDIA', 'JUBILANT', 'JUBLFOOD', 'JUBLINDS', 'JUMPNET', 'JUSTDIAL', 'JVLAGRO', 'JYOTHYLAB', 'KABRAEXTRU', 'KAJARIACER', 'KAKATCEM', 'KALPATPOWR', 'KALYANI', 'KALYANIFRG', 'KAMATHOTEL', 'KAMDHENU', 'KANANIIND', 'KANORICHEM', 'KANSAINER', 'KARDA', 'KARMAENG', 'KARURVYSYA', 'KAUSHALYA', 'KAVVERITEL', 'KAYA', 'KCP', 'KCPSUGIND', 'KDDL', 'KEC', 'KECL', 'KEI', 'KELLTONTEC', 'KENNAMET', 'KERNEX', 'KESARENT', 'KESORAMIND', 'KEYFINSERV', 'KGL', 'KHADIM', 'KHAITANLTD', 'KHANDSE', 'KICL', 'KILITCH', 'KINGFA', 'KIOCL', 'KIRIINDUS', 'KIRLOSBROS', 'KIRLOSENG', 'KIRLOSIND', 'KITEX', 'KKCL', 'KMSUGAR', 'KNRCON', 'KOHINOOR', 'KOKUYOCMLN', 'KOLTEPATIL', 'KOPRAN', 'KOTAKBANK', 'KOTARISUG', 'KOTHARIPET', 'KOTHARIPRO', 'KPITTECH', 'KPRMILL', 'KRBL', 'KREBSBIO', 'KRIDHANINF', 'KRISHANA', 'KSB', 'KSCL', 'KSERASERA', 'KSK', 'KSL', 'KTIL', 'KTKBANK', 'KUANTUM', 'KWALITY', 'L&TFH', 'LAKPRE', 'LAKSHVILAS', 'LALPATHLAB', 'LAMBODHARA', 'LAOPALA', 'LASA', 'LAURUSLABS', 'LAXMIMACH', 'LEMONTREE', 'LFIC', 'LGBBROSLTD', 'LGBFORGE', 'LIBAS', 'LIBAS', 'LIBERTSHOE', 'LICHSGFIN', 'LINCOLN', 'LINCPEN', 'LINDEINDIA', 'LOKESHMACH', 'LOTUSEYE', 'LOVABLE', 'LPDC', 'LSIL', 'LT', 'LTI', 'LTTS', 'LUMAXIND', 'LUMAXTECH', 'LUPIN', 'LUXIND', 'LYKALABS', 'LYPSAGEMS', 'M&M', 'M&MFIN', 'MAANALU', 'MADHAV', 'MADHUCON', 'MADRASFERT', 'MAGADSUGAR', 'MAGMA', 'MAGNUM', 'MAHABANK', 'MAHAPEXLTD', 'MAHASTEEL', 'MAHESHWARI', 'MAHINDCIE', 'MAHLIFE', 'MAHLOG', 'MAHSCOOTER', 'MAHSEAMLES', 'MAITHANALL', 'MAJESCO', 'MALUPAPER', 'MANAKALUCO', 'MANAKCOAT', 'MANAKSIA', 'MANAKSTEEL', 'MANALIPETC', 'MANAPPURAM', 'MANGALAM', 'MANGCHEFER', 'MANGLMCEM', 'MANGTIMBER', 'MANINDS', 'MANINFRA', 'MANPASAND', 'MANUGRAPH', 'MARALOVER', 'MARATHON', 'MARICO', 'MARKSANS', 'MARUTI', 'MASFIN', 'MASKINVEST', 'MASTEK', 'MATRIMONY', 'MAWANASUG', 'MAXINDIA', 'MAXVIL', 'MAYURUNIQ', 'MAZDA', 'MBAPL', 'MBECL', 'MBLINFRA', 'MCDHOLDING', 'MCDOWELL-N', 'MCLEODRUSS', 'MCX', 'MEGASOFT', 'MEGH', 'MELSTAR', 'MENONBE', 'MEP', 'MERCATOR', 'METALFORGE', 'METKORE', 'METROPOLIS', 'MFSL', 'MGL', 'MHRIL', 'MIC', 'MIDHANI', 'MINDACORP', 'MINDAIND', 'MINDTECK', 'MINDTREE', 'MIRCELECTR', 'MIRZAINT', 'MMFL', 'MMTC', 'MODIRUBBER', 'MOHITIND', 'MOHOTAIND', 'MOIL', 'MOLDTECH', 'MOLDTKPAC', 'MONTECARLO', 'MORARJEE', 'MOREPENLAB', 'MOTHERSUMI', 'MOTILALOFS', 'MOTOGENFIN', 'MPHASIS', 'MPSLTD', 'MRF', 'MRO-TEK', 'MRPL', 'MSPL', 'MSTCLTD', 'MTEDUCARE', 'MTNL', 'MUKANDENGG', 'MUKANDLTD', 'MUKTAARTS', 'MUNJALAU', 'MUNJALSHOW', 'MURUDCERA', 'MUTHOOTCAP', 'MUTHOOTFIN', 'MVL', 'NACLIND', 'NAGAFERT', 'NAGAROIL', 'NAGREEKCAP', 'NAGREEKEXP', 'NAHARCAP', 'NAHARINDUS', 'NAHARPOLY', 'NAHARSPING', 'NATCOPHARM', 'NATHBIOGEN', 'NATIONALUM', 'NATNLSTEEL', 'NAUKRI', 'NAVINFLUOR', 'NAVKARCORP', 'NAVNETEDUL', 'NBCC', 'NBIFIN', 'NBVENTURES', 'NCC', 'NCLIND', 'NDGL', 'NDL', 'NDTV', 'NECCLTD', 'NECLIFE', 'NELCAST', 'NELCO', 'NEOGEN', 'NESCO', 'NESTLEIND', 'NETWORK18', 'NEULANDLAB', 'NEWGEN', 'NEXTMEDIA', 'NFL', 'NH', 'NHPC', 'NIACL', 'NIBL', 'NIITLTD', 'NIITTECH', 'NILAINFRA', 'NILASPACES', 'NILKAMAL', 'NIPPOBATRY', 'NIRAJISPAT', 'NITCO', 'NITESHEST', 'NITINFIRE', 'NITINSPIN', 'NKIND', 'NLCINDIA', 'NMDC', 'NOCIL', 'NOIDATOLL', 'NORBTEAEXP', 'NRAIL', 'NRBBEARING', 'NSIL', 'NTL', 'NTPC', 'NUCLEUS', 'OAL', 'OBEROIRLTY', 'OCCL', 'OFSS', 'OIL', 'OILCOUNTUB', 'OISL', 'OLECTRA', 'OMAXAUTO', 'OMAXE', 'OMKARCHEM', 'OMMETALS', 'ONELIFECAP', 'ONEPOINT', 'ONGC', 'ONMOBILE', 'ONWARDTEC', 'OPTIEMUS', 'OPTOCIRCUI', 'ORBTEXP', 'ORICONENT', 'ORIENTABRA', 'ORIENTALTL', 'ORIENTBANK', 'ORIENTBELL', 'ORIENTCEM', 'ORIENTELEC', 'ORIENTHOT', 'ORIENTLTD', 'ORIENTPPR', 'ORIENTREF', 'ORISSAMINE', 'ORTEL', 'ORTINLABSS', 'OSWALAGRO', 'PAEL', 'PAGEIND', 'PAISALO', 'PALASHSECU', 'PALREDTEC', 'PANACEABIO', 'PANAMAPET', 'PAPERPROD', 'PARABDRUGS', 'PARACABLES', 'PARAGMILK', 'PARSVNATH', 'PATELENG', 'PATINTLOG', 'PATSPINLTD', 'PCJEWELLER', 'PDMJEPAPER', 'PDPL', 'PDSMFL', 'PEARLPOLY', 'PEL', 'PENIND', 'PENINLAND', 'PERSISTENT', 'PETRONENGG', 'PETRONET', 'PFC', 'PFIZER', 'PFOCUS', 'PFS', 'PGEL', 'PGHH', 'PGHL', 'PGIL', 'PHILIPCARB', 'PHOENIXLTD', 'PIDILITIND', 'PIIND', 'PILANIINVS', 'PILITA', 'PIONDIST', 'PIONEEREMB', 'PIRPHYTO', 'PITTIENG', 'PKTEA', 'PLASTIBLEN', 'PNB', 'PNBGILTS', 'PNBHOUSING', 'PNC', 'PNCINFRA', 'PODDARHOUS', 'PODDARMENT', 'POKARNA', 'POLYCAB', 'POLYMED', 'POLYPLEX', 'PONNIERODE', 'POWERGRID', 'POWERMECH', 'PPAP', 'PPL', 'PRABHAT', 'PRADIP', 'PRAENG', 'PRAJIND', 'PRAKASH', 'PRAKASHSTL', 'PRAXIS', 'PRECAM', 'PRECOT', 'PRECWIRE', 'PREMEXPLN', 'PREMIER', 'PREMIERPOL', 'PRESSMN', 'PRESTIGE', 'PRICOLLTD', 'PRIMESECU', 'PROSEED', 'PROVOGE', 'PROZONINTU', 'PRSMJOHNSN', 'PSB', 'PSL', 'PSPPROJECT', 'PTC', 'PTL', 'PUNJABCHEM', 'PUNJLLOYD', 'PURVA', 'PVR', 'QUESS', 'QUICKHEAL', 'RADAAN', 'RADICO', 'RADIOCITY', 'RAIN', 'RAJESHEXPO', 'RAJRAYON', 'RAJSREESUG', 'RAJTV', 'RAJVIR', 'RALLIS', 'RAMANEWS', 'RAMASTEEL', 'RAMCOCEM', 'RAMCOIND', 'RAMCOSYS', 'RAMKY', 'RANASUG', 'RANEENGINE', 'RANEHOLDIN', 'RATNAMANI', 'RAYMOND', 'RBL', 'RBLBANK', 'RCF', 'RCOM', 'RECLTD', 'REDINGTON', 'REFEX', 'REGENCERAM', 'RELAXO', 'RELCAPITAL', 'RELIANCE', 'RELIGARE', 'RELINFRA', 'REMSONSIND', 'RENUKA', 'REPCOHOME', 'REPRO', 'RESPONIND', 'REVATHI', 'RGL', 'RHFL', 'RICOAUTO', 'RIIL', 'RITES', 'RKDL', 'RKFORGE', 'RMCL', 'RML', 'RNAM', 'RNAVAL', 'ROHITFERRO', 'ROHLTD', 'ROLLT', 'ROLTA', 'ROSSELLIND', 'RPGLIFE', 'RPOWER', 'RPPINFRA', 'RSSOFTWARE', 'RSWM', 'RSYSTEMS', 'RTNINFRA', 'RTNPOWER', 'RUBYMILLS', 'RUCHINFRA', 'RUCHIRA', 'RUCHISOYA', 'RUPA', 'RUSHIL', 'RVNL', 'SABEVENTS', 'SABTN', 'SADBHAV', 'SADBHIN', 'SAFARI', 'SAGARDEEP', 'SAGCEM', 'SAIL', 'SAKAR', 'SAKHTISUG', 'SAKSOFT', 'SAKUMA', 'SALASAR', 'SALONA', 'SALSTEEL', 'SALZERELEC', 'SAMBHAAV', 'SANCO', 'SANDESH', 'SANDHAR', 'SANGAMIND', 'SANGHIIND', 'SANGHVIFOR', 'SANGHVIMOV', 'SANGINITA', 'SANOFI', 'SANWARIA', 'SARDAEN', 'SAREGAMA', 'SARLAPOLY', 'SASKEN', 'SASTASUNDR', 'SATHAISPAT', 'SATIA', 'SATIN', 'SBILIFE', 'SBIN', 'SCAPDVR', 'SCHAEFFLER', 'SCHAND', 'SCHNEIDER', 'SCI', 'SDBL', 'SEAMECLTD', 'SELAN', 'SELMCL', 'SEPOWER', 'SEQUENT', 'SESHAPAPER', 'SETCO', 'SETUINFRA', 'SEYAIND', 'SFL', 'SGL', 'SHAHALLOYS', 'SHAKTIPUMP', 'SHALBY', 'SHALPAINTS', 'SHANKARA', 'SHANTIGEAR', 'SHARDACROP', 'SHARDAMOTR', 'SHEMAROO', 'SHILPAMED', 'SHIRPUR-G', 'SHIVAMAUTO', 'SHIVAMILLS', 'SHIVATEX', 'SHK', 'SHOPERSTOP', 'SHREDIGCEM', 'SHREECEM', 'SHREEPUSHK', 'SHREERAMA', 'SHRENIK', 'SHREYANIND', 'SHREYAS', 'SHRIPISTON', 'SHRIRAMCIT', 'SHRIRAMEPC', 'SHYAMCENT', 'SHYAMTEL', 'SICAGEN', 'SICAL', 'SIEMENS', 'SIGIND', 'SIL', 'SILINV', 'SIMBHALS', 'SIMPLEXINF', 'SINTEX', 'SIRCA', 'SIS', 'SITINET', 'SIYSIL', 'SJVN', 'SKFINDIA', 'SKIL', 'SKIPPER', 'SKMEGGPROD', 'SMARTLINK', 'SMLISUZU', 'SMPL', 'SMSLIFE', 'SMSPHARMA', 'SNOWMAN', 'SOBHA', 'SOLARA', 'SOLARINDS', 'SOMANYCERA', 'SOMATEX', 'SOMICONVEY', 'SONATSOFTW', 'SORILINFRA', 'SOTL', 'SOUTHBANK', 'SOUTHWEST', 'SPAL', 'SPANDANA', 'SPARC', 'SPCENET', 'SPECIALITY', 'SPENCERS', 'SPENTEX', 'SPIC', 'SPICEJET', 'SPLIL', 'SPMLINFRA', 'SPTL', 'SPYL', 'SREEL', 'SREINFRA', 'SRF', 'SRHHYPOLTD', 'SRIPIPES', 'SRSLTD', 'SRTRANSFIN', 'SSWL', 'STAMPEDE', 'STAR', 'STARCEMENT', 'STARPAPER', 'STCINDIA', 'STEELCITY', 'STEELXIND', 'STEL', 'STERTOOLS', 'STINDIA', 'STRTECH', 'SUBCAPCITY', 'SUBEX', 'SUBROS', 'SUDARSCHEM', 'SUJANAUNI', 'SUMEETINDS', 'SUMIT', 'SUMMITSEC', 'SUNCLAYLTD', 'SUNDARAM', 'SUNDARMFIN', 'SUNDARMHLD', 'SUNDRMBRAK', 'SUNDRMFAST', 'SUNFLAG', 'SUNPHARMA', 'SUNTECK', 'SUNTV', 'SUPERHOUSE', 'SUPERSPIN', 'SUPPETRO', 'SUPRAJIT', 'SUPREMEIND', 'SUPREMEINF', 'SURANASOL', 'SURANAT&P', 'SURYALAXMI', 'SURYAROSNI', 'SUTLEJTEX', 'SUVEN', 'SUZLON', 'SWANENERGY', 'SWARAJENG', 'SWELECTES', 'SWSOLAR', 'SYMPHONY', 'SYNCOM', 'SYNDIBANK', 'SYNGENE', 'TAINWALCHM', 'TAJGVK', 'TAKE', 'TALBROAUTO', 'TALWALKARS', 'TALWGYM', 'TANLA', 'TANTIACONS', 'TARAPUR', 'TARMAT', 'TASTYBITE', 'TATACHEM', 'TATACOFFEE', 'TATACOMM', 'TATAELXSI', 'TATAGLOBAL', 'TATAINVEST', 'TATAMETALI', 'TATAMOTORS', 'TATAMTRDVR', 'TATAPOWER', 'TATASTEEL', 'TATASTLBSL', 'TATASTLLP', 'TBZ', 'TCI', 'TCIDEVELOP', 'TCIEXP', 'TCIFINANCE', 'TCNSBRANDS', 'TCPLPACK', 'TCS', 'TDPOWERSYS', 'TEAMLEASE', 'TECHIN', 'TECHM', 'TECHNOE', 'TECHNOFAB', 'TEJASNET', 'TERASOFT', 'TEXINFRA', 'TEXMOPIPES', 'TEXRAIL', 'TEXRAIL', 'TFCILTD', 'TFL', 'TGBHOTELS', 'TGBHOTELS', 'THANGAMAYL', 'THEINVEST', 'THEMISMED', 'THERMAX', 'THIRUSUGAR', 'THOMASCOOK', 'THOMASCOTT', 'THYROCARE', 'TI', 'TIDEWATER', 'TIIL', 'TIINDIA', 'TIJARIA', 'TIL', 'TIMESGTY', 'TIMETECHNO', 'TIMKEN', 'TINPLATE', 'TIPSINDLTD', 'TIRUMALCHM', 'TITAN', 'TMRVL', 'TNPETRO', 'TNPL', 'TNTELE', 'TOKYOPLAST', 'TORNTPHARM', 'TORNTPOWER', 'TPLPLASTEH', 'TREEHOUSE', 'TREJHARA', 'TRENT', 'TRF', 'TRIDENT', 'TRIGYN', 'TRIL', 'TRITURBINE', 'TRIVENI', 'TTKHLTCARE', 'TTKPRESTIG', 'TTL', 'TTML', 'TV18BRDCST', 'TVSELECT', 'TVSMOTOR', 'TVSSRICHAK', 'TVTODAY', 'TVVISION', 'TWL', 'UBL', 'UCALFUEL', 'UCOBANK', 'UFLEX', 'UFO', 'UGARSUGAR', 'UJAAS', 'UJJIVAN', 'ULTRACEMCO', 'UMANGDAIRY', 'UMESLTD', 'UNICHEMLAB', 'UNIENTER', 'UNIONBANK', 'UNIPLY', 'UNITECH', 'UNITEDBNK', 'UNITEDTEA', 'UNITY', 'UNIVCABLES', 'UPL', 'URJA', 'USHAMART', 'UTTAMSTL', 'UTTAMSUGAR', 'UVSL', 'V2RETAIL', 'VADILALIND', 'VAIBHAVGBL', 'VAKRANGEE', 'VARDHACRLC', 'VARDMNPOLY', 'VARROC', 'VASCONEQ', 'VASWANI', 'VBL', 'VEDL', 'VENKEYS', 'VENUSREM', 'VESUVIUS', 'VETO', 'VGUARD', 'VHL', 'VICEROY', 'VIDEOIND', 'VIDHIING', 'VIJIFIN', 'VIKASECO', 'VIKASMCORP', 'VIKASPROP', 'VIKASWSP', 'VIMALOIL', 'VIMTALABS', 'VINATIORGA', 'VINDHYATEL', 'VINYLINDIA', 'VIPCLOTHNG', 'VIPIND', 'VIPULLTD', 'VISAKAIND', 'VISASTEEL', 'VISESHINFO', 'VISHAL', 'VISHNU', 'VISHWARAJ', 'VIVIDHA', 'VIVIMEDLAB', 'VLSFINANCE', 'VMART', 'VOLTAMP', 'VOLTAS', 'VRLLOG', 'VSSL', 'VSTIND', 'VSTTILLERS', 'VTL', 'WABAG', 'WABCOINDIA', 'WALCHANNAG', 'WANBURY', 'WATERBASE', 'WEBELSOLAR', 'WEIZFOREX', 'WEIZMANIND', 'WELCORP', 'WELENT', 'WELINV', 'WELSPUNIND', 'WENDT', 'WESTLIFE', 'WHEELS', 'WHIRLPOOL', 'WILLAMAGOR', 'WINDMACHIN', 'WINSOME', 'WIPL', 'WIPRO', 'WOCKPHARMA', 'WONDERLA', 'WSI', 'WSTCSTPAPR', 'XCHANGING', 'XELPMOC', 'XLENERGY', 'XPROINDIA', 'YESBANK', 'ZEEL', 'ZEELEARN', 'ZEEMEDIA', 'ZENITHBIR', 'ZENITHEXPO', 'ZENSARTECH', 'ZENTEC', 'ZICOM', 'ZODIACLOTH', 'ZODJRDMKJ', 'ZOTA', 'ZUARI', 'ZUARIGLOB', 'ZYDUSWELL']

		self.stockSymbol = stockSymbol;
		headers = {
		"Host": "www1.nseindia.com",
		"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0",
		"Accept": "*/*",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate, br",
		"X-Requested-With": "XMLHttpRequest",
		"Referer": "https://www1.nseindia.com/products/content/equities/equities/eq_security.htm",
		"Access-Control-Allow-Origin" : "*",
		"Access-Control-Allow-Methods" : "GET,POST,PUT,DELETE,OPTIONS",
		"Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With",
		'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'
		}

		first = 'https://www1.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp'
		result=[];
		# session = requests.Session()
		urlpost = "https://www1.nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol="
		data = {"symbol":stockSymbol}
		response = requests.post(urlpost,data=data,headers=headers)
		page_content = BeautifulSoup(response.content, "html.parser")
		symbolCount = (str(page_content))
		# print(symbolCount)
		print(stockSymbol)
		if(full_data ==None or full_data=="No"):

				x=datetime.datetime.strptime(start_date,"%d-%m-%Y")
				y=datetime.datetime.strptime(end_date,"%d-%m-%Y")

				if(x>y):
					raise ValueError("Starting date is greater than end date.")

				#Checking for proper StockSymbol and suggesting necessary changes.
				maxi = 0
				maxVal = values[0];
				for compare in values:
					str1 = stockSymbol
					str2 = compare

					Ratio = fuzz.ratio(str1.lower(),str2.lower())
					if(Ratio>maxi):
						maxVal = compare
						maxi = Ratio

				if stockSymbol not in values:
					raise ValueError("Check the Stock symbol. Try {} as stock symbol.".format(maxVal))

				result = pd.DataFrame()
				while(True):
					if((y-x).days<365):
						try:
							# print(1)
							fromdate= x.strftime("%d-%m-%Y")
							# print(fromdate)
							todate=y.strftime("%d-%m-%Y")

							url = first + '?symbol='+(stockSymbol)+ '&segmentLink=3&symbolCount'+ symbolCount+ "&series=EQ&dateRange=+&fromDate="+fromdate+"&toDate="+todate+"&dataType=PRICEVOLUMEDELIVERABLE"			
							
							response = requests.get(url,headers=headers)
							page_content = BeautifulSoup(response.content, "html.parser")
							# print(page_content)
							a=page_content.find(id="csvContentDiv").get_text();
							a = a.replace(':',", \n")


							with open("data.csv", "w") as f:
								f.write(a)

							df = pd.read_csv("data.csv")
							df.set_index("Date",inplace=True)
							df = df[::-1]
							result = pd.concat([result,df])
							break;

						except AttributeError:
							break

					if ((y-x).days > 365 ):
						try:
							# print(0)
							todate= y.strftime("%d-%m-%Y")
							fromdate = ( y - datetime.timedelta(days=364) ).strftime("%d-%m-%Y")
							inter =  y - datetime.timedelta(days=364) 
							# print(todate)
							url = first + '?symbol='+(stockSymbol)+ '&segmentLink=3&symbolCount'+ symbolCount+ "&series=EQ&dateRange=+&fromDate="+fromdate+"&toDate="+todate+"&dataType=PRICEVOLUMEDELIVERABLE"			
												
							response = requests.get(url, timeout=240,headers=headers)
							page_content = BeautifulSoup(response.content, "html.parser")
							# print(page_content)

							a=page_content.find(id="csvContentDiv").get_text();
							# print(a)
							a = a.replace(':',", \n")


							with open("data.csv", "w") as f:
								f.write(a)

							df = pd.read_csv("data.csv")
							df.set_index("Date",inplace=True)
							df = df[::-1]
							result = pd.concat([result,df])
							y = ( inter - datetime.timedelta(days=1) )

						except AttributeError:
							break;

			
		elif(full_data =="Yes" or full_data=="yes"):
				# print("YES")
				x=datetime.datetime.now()
				y=datetime.datetime.now() - datetime.timedelta(days=364)

				maxi = 0
				maxVal = values[0];
				for compare in values:
					str1 = stockSymbol
					str2 = compare

					Ratio = fuzz.ratio(str1.lower(),str2.lower())
					if(Ratio>maxi):
						maxVal = compare
						maxi = Ratio

				if stockSymbol not in values:
					raise ValueError("Check the Stock symbol.Try {} as stock symbol".format(maxVal))
				result = pd.DataFrame()
				i=0;
				while(True):
					try:
						print("Stage ",i)
						todate=x.strftime("%d-%m-%Y")
						fromdate= y.strftime("%d-%m-%Y")

						url = first + '?symbol='+(stockSymbol)+ '&segmentLink=3&symbolCount'+ symbolCount+ "&series=EQ&dateRange=+&fromDate="+fromdate+"&toDate="+todate+"&dataType=PRICEVOLUMEDELIVERABLE"			
								

						response = requests.get(url, timeout=240,headers=headers)
						page_content = BeautifulSoup(response.content, "html.parser")
						a=page_content.find(id="csvContentDiv").get_text();
						a = a.replace(':',", \n")

						with open("data.csv", "w") as f:
							f.write(a)

						df = pd.read_csv("data.csv")
						df.set_index("Date",inplace=True)
						df = df[::-1]
						result = pd.concat([result,df])

						x = y - datetime.timedelta(days=1)
						y = x - datetime.timedelta(days=364)
						i=i+1

					except AttributeError:
						break;
		try:
			os.remove("data.csv")
		except(OSError):
			pass


		return result;
