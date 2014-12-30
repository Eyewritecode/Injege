#This script fetches articles from igihe.com and analyze them


import urllib2 as ul
import os
import sys
import io
import re
import argparse
from bs4 import BeautifulSoup as bs




parser = argparse.ArgumentParser()
parser.add_argument('--start','-s', action = 'store', type=int , required = True, help = 'The article id number to start with(going down)')
parser.add_argument('--num', '-n',action ='store', default = 10, type =int, help = 'The number of articles to download. Default = 10')


#Visiting a given page

def go_to_page(link) :

	resp = ul.urlopen(link)
	contents = resp.read()
	return contents

#Scraping results from a given igihe page
def scrap_results(contents,counters):
	
	Features = {}
	soup = bs(contents)
	soup_counter = bs(counters)

                           
	#Features of the article
	
	#Summary = soup.p.i.text #Summary of the article
	Title = soup.title.text[:(len(soup.title.text)-13)]#The title of the article
	Features['Title'] = Title
	Date = soup.find_all(class_ = "gh_inarticledetails")[0].text
	Features['Date'] = Date
	Hour = soup.find_all(class_ = "gh_inarticledetails")[1].text[:5]
	Features['Time'] = Hour
	Author = soup.find_all(class_ = "gh_tab_articledetails_author")[0].text
	Features['Author'] = Author
	#Content = soup.find_all(class_ = "gh_articlecontent")[0].text[73:]
	#Related_links_list =[ip_ad+rel.get('href') for rel in soup.find_all(class_ = "gh_news_hometitle")]


	#Retrieving the number of views and the number of comments.
	Visits_Counter = 0
	Comments_Counter = 0
	
	for link in soup_counter.body.find_all('a', style = re.compile("views")):
		Visits_Counter= Visits_Counter +  int(link.text[9:])
	for link in soup_counter.body.find_all('a', style = re.compile("comment")):
		Comments_Counter = Comments_Counter + int(link.text[10:])
	
	Features['Comments_count'] = Comments_Counter
	Features['Visits_count'] = Visits_Counter
	return Features


def main():
	args = parser.parse_args()
	
	Number_of_articles_needed = args.num 
	id_art = args.start

	Limit = id_art-Number_of_articles_needed
	
	ip_ad = "http://142-4-9-39.unifiedlayer.com/"

	output_file = "igihe_"+str(id_art)+"_"+str(Limit) +".txt"

	Not_working = [] #Error links

	print "Starting ...\n"

	with open(output_file,"w") as outfile:
	
		outfile.write( "{:<15}\t{:<20}\t{:<9}\t{:<6}\t{:<6}\t{:<9}\tTitle\n\n".format("Article_ID","Author","Date","Hour", "NViews", "NComments",))

		while id_art > Limit:
		
			print "Fetching: Igihe.com article whose ID is", str(id_art) ,"..."
			article_link = ip_ad+str(id_art)
			format_counter = ip_ad + "/trafficcounter.php?id_article="
			
			try:
				contents = go_to_page(article_link)
				counters = go_to_page(format_counter + str(id_art))
				
				#Getting features and putting them into the file
				print "Features extraction..."
				try:
					Features = scrap_results(contents,counters)
					#Overwriting the file
					Author = Features['Author'].encode('utf8')
					Date = Features['Date'].encode('utf8')
					Hour = Features['Time'].encode('utf8')
					Title = Features['Title'].encode('utf8')
					Visits = str(Features['Visits_count']).encode('utf8')
					Comments = str(Features['Comments_count']).encode('utf8')
					
					outfile.write( "{:<15}\t{:<20}\t{:<9}\t{:<6}\t{:<6}\t{:<9}\t{}\n".format(str(id_art).encode('utf8'), Author, Date, Hour, Visits, Comments,Title)) 

				except Exception:
					Not_working.append(id_art)
					print "No features"
				
			except ul.HTTPError, error:
				#contents = error.read()
				Not_working.append(id_art)
			except ul.URLError:
				Not_working.append(id_art)
			except ul.HTTPException, e:
				Not_working.append(id_art)
			except Exception:
				Not_working.append(id_art)
				
			id_art = id_art - 1
			print "Done."

	#print "These are not working: ",  ' '.join([str(item) for item in Not_working])
	print "Number of broken links : ", len(Not_working)




if __name__ == "__main__" :
	main()
