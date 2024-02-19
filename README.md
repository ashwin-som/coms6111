Names/UNIs:
Ashwin Somasundaram, as7116
Claire Dawson, cd3417

Files:
proj1.py - main driver file, contains all code functionality and driver function
README.md - this file explaining project
testing.txt = testing transcript output of

How to Run Program:
call the following in the terminal:
python proj1.py AIzaSyC0vz_nYIczwBwNupqMrNhmBm4dQbX5Pbw 7260228cc892a415a precision query_word

Internal Design:
The main chunk of this project is in the proj1.tar.gz file, which executes most of the project. The different functions in the code are:
generate_new_input() - this function takes in the current input query words, relevant links, and unrelevant links, and will output and updated query string of words. It does this by vectorizing the documents in the links, and running Rocchio's algorithm. The strategy implemented adds only one word to the original query string.
process_feedback() - this function takes in all links produced from the Google API along with goal precision. Within the function, it asks for the users feedback on each document (relevant or not). It then cateogrizes the links into two list of relevant or not relevant. It calculates the current precision of the query. Depending on what that precision is and the number of relevant links, it will return a decision (if new queries should be generated or not). False indicates the program should keep running and call generate_new_input() to produce more query words, while True indicates the program can halt because the precision goal has been met, no relevant queries were produced, or there were less than 10 links produced from Google.
scrape_web() - this function takes in the query string, the Google Custom Search Engine JSON API Key, and the Engine Id, to get Google's top 10 links from that query string. It returns these 10 links.
main() - this is the driver function - it takes in the intitial query string, precision, the Google Custom Search Engine JSON API Key, and the Engine Id from command line arguments. It then prints these basic parameters, and calles scrape_web, process_feedback(), and generate_new_input() until an end state is reached.


Query-Modification:
We used Rocchio's algorithm to add new words to the query. Using the 10 links given, we read in the snippets from each of them and utilize sklearn's TfidfVectorizer() to vectorize the words according to tfidf scores. We remove any stop words and numbers from the text snippets before doing this. Once the TfidfVectorizer is created, we fit it to meet the size of the query string (which gets converted to an array of keywords), and create our related and unrelated vectors from that. Then we call the algorithm to get the centroids of each of the three components (original query vector, related vectors, and unrelated vectors). We toyed around with coefficinet values for each of the 3 weights and ultimately chose .9, .6, and .1 for final values of original query vector, related vectors, and unrelated vectors respectfully. Once the algorithm runs, we take the top word produced (according to tfidf score) and add it to the query string. We tested out adding 1 and 2 and even an implementation where depending on how high the frequency was between the top two, we decided whether to include both or just the top one. Essentially, if the frequencies were very close together we would add both, but if it was a big dropoff we would add just the top word. Ultimately, though, we found just adding one word still tended to work best, so we decided to just take the top word.

Packages included:
numpy - pip install numpy (might be pip3)
sklearn - pip install scikit-learn (might be pip3)
google api client - pip3 install --upgrade google-api-python-client
sys, heapq - should be part of standard python library

Google Custom Search Engine JSON API Key: AIzaSyC0vz_nYIczwBwNupqMrNhmBm4dQbX5Pbw
Engine ID: 7260228cc892a415a
