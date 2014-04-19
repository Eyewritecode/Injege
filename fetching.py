#This script fetches articles from igihe.com and analyze them


import urllib2 as ul
import os
import io
import re
from bs4 import BeautifulSoup as bs


ip_ad = "http://142-4-9-39.unifiedlayer.com/"

format_counter = ip_ad + "/trafficcounter.php?id_article="

Number_of_articles_needed = 10000
id_art = int(input("Where do we start?"))

Limit = id_art-Number_of_articles_needed
#def clean(s):
#   return str(s).encode('utf-8')
output_file = "igihe10k_" + str(id_art) +".txt"

Not_working = [] #Error links

print "Starting ...\n"

with open(output_file,"w") as outfile:
    
    outfile.write( "{:<15}\t{:<20}\t{:<9}\t{:<6}\t{:<6}\t{:<9}\tTitle\n\n".format("Article_ID","Author","Date","Hour", "NViews", "NComments",))

    while id_art > Limit:
        
        print "Fetching: Igihe.com article whose ID is", str(id_art) ,"..."
        
        #Making a BeautifulSoup object
        article_link = ip_ad+str(id_art)

        try:
            resp = ul.urlopen(article_link)
            contents = resp.read()
            
            
            
            
#            if ("igihe" in contents):
            try:
                soup = bs(contents)
                
               
                #Features of the article
                print "Features extraction..."
                #Summary = soup.p.i.text #Summary of the article
               
                Title = soup.title.text[:(len(soup.title.text)-13)]#The title of the article
                Date = soup.find_all(class_ = "gh_inarticledetails")[0].text
                Hour = soup.find_all(class_ = "gh_inarticledetails")[1].text[:5]
                Author = soup.find_all(class_ = "gh_tab_articledetails_author")[0].text
                #Content = soup.find_all(class_ = "gh_articlecontent")[0].text[73:]
                #Related_links_list =[ip_ad+rel.get('href') for rel in soup.find_all(class_ = "gh_news_hometitle")]
                
                
                #Retrieving the number of views and the number of comments.
                print "Comments and Views counting..."
                soup_counter = bs(ul.urlopen(format_counter + str(id_art)).read())
                Visits_Counter = 0
                Comments_Counter = 0
                #    print response.read()
                for link in soup_counter.body.find_all('a', style = re.compile("views")):
                    Visits_Counter= Visits_Counter +  int(link.text[9:])
                for link in soup_counter.body.find_all('a', style = re.compile("comment")):
                    Comments_Counter = Comments_Counter + int(link.text[10:])
                
                #Overwriting the file
                outfile.write("{:<15}\t{:<20}\t{:<9}\t{:<6}\t{:<6}\t{:<9}\t{}\n".format(str(id_art).encode('utf8'),Author.encode('utf8'),Date.encode('utf8'),Hour.encode('utf8'),str(Visits_Counter).encode('utf8'),str(Comments_Counter).encode('utf8'),Title.encode('utf8')))
    
            except Exception:
                Not_working.append(id_art)
    #Error Handling when reading the URL:
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






