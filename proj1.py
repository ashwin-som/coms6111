#just some pseudocode/ideas for part 4: 
import numpy as np 
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from googleapiclient.discovery import build
import pprint
#print(sw_nltk)
import urllib.request  # the lib that handles the url stuff
from sklearn.feature_extraction.text import TfidfVectorizer #used to make document vectors 
from sklearn.metrics.pairwise import cosine_similarity
'''
Represent query as weighted tf-idf vector
● Represent documents as weighted tf-idf vectors
● Compute cosine similarity score for query vector
and each document vector
● Rank documents with respect to query by score
● Return the top K (e.g., K = 10) documents to
user
44

'''



def link_to_text(target_url):
    data = urllib.request.urlopen(target_url) # it's a file like object and works just like a file
    return_str = ""
    for line in data: # files are iterable
        return_str += line
    return return_str


def text_vectors(text):
    ''' given a text, generate the vectors for the documents'''
    #stop words 
    sw_nltk = stopwords.words('english')
    stop_set = stop(sw_nltk)
    #clean up text 

    #covert to tokens 
    text = word_tokenize(text)

    #remove stop words 
    good_text = "" #not positive if this was done properly 
    for word in text:
        if word not in stop_set:
            good_text += word
            good_text += " "


    vectorizer = TfidfVectorizer()
    mat = vectorizer.fit_transform(good_text) #td-idf vectors 
    cosine_similarity(query_vector, tfidf_matrix)
    #extract most relevant column 
    id = cosine_similarities.argmax()
    important_vec = mat[id]

    return important_vec


#not sure what to set og_query_weight, related_weight, unrelated_weights to? think this may need to be a part we figure out 
#not exactly sure what og_query_vector will be? 
#also given new query vector - how do we get the exact words? 
def rocchios(og_query_vector, related_links,unrelated_links,og_query_weight, related_weight, unrelated_weight):
    #og_query_vector = og_query_vector.split(' ')
    #how to generate the vector for a document 
    related_vectors = []
    for link in related_links:
        #convert to text 
        text = link_to_text(link)
        #convert to vector 
        vector = text_vector(text)
        related_vectors.append(vector)
    related_vectors = np.array(related_vectors)

    unrelated_vectors = []
    for link2 in unrelated_links:
        #convert to text 
        text2 = link_to_text(link2)
        #convert to vector 
        vector2 = text_vector(text2)
        unrelated_vectors.append(vector2)
    unrelated_vectors = np.array(unrelated_vectors)

    #get sums of vectors
    r_sum = np.sum(related_vectors)
    ur_sum = np.sum(unrelated_vectors)
    og_sum = np.sum(np.array(og_query_vector)) #not sure on this part 

    #og_query_vec = 
    #related_doc_vec = 

    #generate related_doc_vec_sum 


    new_vector = og_query_weight*og_query_vec + (related_weight/(len(related_links)))*r_sum - (unrelated_weight/(len(unrelated_links)))*ur_sum
    
    return new_vector #new the new query vector - not sure how to get words from it 



def process_feedback(links):
    count = 0
    relevant_links, irrelevant_links= [], []
    for i in range(len(links)):
        print('Document #: ',i)
        print(links[i])
        answer = input('Is the document above relevant to your search query? (Y/N): ')
        if answer.lower()=='y':
            relevant_links.append(links[i])
            count+=1
        else:
            irrelevant_links.append(links[i])
    print('The current precision level out of 10 is: ',count)
    if count>=9:
        return True, relevant_links, irrelevant_links
    else:
        return False, relevant_links, irrelevant_links


def scrape_web(query):
    service = build(
        "customsearch", "v1", developerKey="AIzaSyC0vz_nYIczwBwNupqMrNhmBm4dQbX5Pbw"
    )

    res = (
        service.cse()
        .list(
            q=query,
            cx="7260228cc892a415a",
        )
        .execute()
    )
    pprint.pprint(res)
    links = []
    for result in res['items']:
        links.append(result.get('link'))
        print(result.get('link'))
    return links

def main():
    inp = input('What would you like to search for?')
    while True:
        links = scrape_web(inp)
        result, relevant_links,irrelevant_links = process_feedback(links)
        if result:
            exit()
        new_search_input = rocchios(input,relevant_links, irrelevant_links,0.3,0.4,0.3)
        inp = new_search_input.split(' ')
    
    result, relevant_links = process_feedback(links)
    print(result)

if __name__ == "__main__":
    main()












