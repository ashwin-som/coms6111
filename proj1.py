import numpy as np 
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import TfidfVectorizer 
import heapq
import sys


def generate_new_input(input,related_res,unrelated_res):

    documents = []
    for i in related_res:
        documents.append(i)
    for i in unrelated_res:
        documents.append(i)

    V = TfidfVectorizer(stop_words='english',token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b')
    V.fit_transform(documents)

    input_vector = V.transform([input])
    related_list = []
    for i in related_res:
        related_list.append(V.transform([i]))
    related_vectors = np.array(related_list)
    unrelated_list = []
    for i in unrelated_res:
        unrelated_list.append(V.transform([i]))
    unrelated_vectors = np.array(unrelated_list)

    a,b,c = 0.9,0.6,0.1
    
    new_input_vector_big = a*input_vector+(b*np.sum(related_vectors)/len(related_list))-(c*np.sum(unrelated_vectors)/len(unrelated_list))
    new_input_array = new_input_vector_big.toarray()[0]
    word_heap = []
    heapq.heapify(word_heap)
    for word in V.vocabulary_:
        weight = new_input_array[V.vocabulary_[word]]
        heapq.heappush(word_heap,(-weight,word))
    
    top_2_words = []
    input_words = V.inverse_transform(input_vector)[0]
    
    while len(word_heap)!=0:
        _,word = heapq.heappop(word_heap)
        if word in input_words:
            continue
        else:
            top_2_words.append(word)
            if len(top_2_words)==1:
                break
    
    resulting_input = input
    for i in top_2_words:
        resulting_input+=' '+i
    
    return resulting_input

def process_feedback(links, precision):
    total_count = len(links)
    if total_count < 10: 
        return True, "Program ended. Not enough links produced",links, links
    count = 0
    relevant_links, irrelevant_links= [], []
    for i in range(len(links)):
        print('Document #: ',i+1)
        print('Link: ',links[i].get('link'))
        print('Snippet: ',links[i].get('snippet'))
        
        answer = input('Is the document above relevant to your search query? (Y/N): ')
        while True:
            if answer.lower()=='y':
                snippet = links[i].get('snippet')
                if not snippet:
                    snippet = ""
                relevant_links.append(snippet)
                count+=1
                break
            elif answer.lower()=='n':
                snippet = links[i].get('snippet')
                if not snippet:
                    snippet = ""
                irrelevant_links.append(snippet)
                break
            else: #tell user they need to answer again 
                answer = input('Oops, not a valid response! Is the document above relevant to your search query? (Y/N): ')

    prec_val = float(count)/float(total_count)
    print("")
    print('The current precision level is: ',prec_val)
    if prec_val >=precision:
        return True, "Success! Desired precision reached!",relevant_links, irrelevant_links
    elif count==0:
        return True, "Program ended. No more relevant links",relevant_links, irrelevant_links
    else:
        return False, "keep going",relevant_links, irrelevant_links


def scrape_web(query, key, id):
    service = build(
        "customsearch", "v1", developerKey=key
    )

    res = (
        service.cse()
        .list(
            q=query,
            cx=id,
        )
        .execute()
    )
    
    links = []
    for result in res['items']:
        links.append(result)
    return links

def main():
    #/home/gkaraman/run <google api key> <google engine id> <precision> <query>
    #key = "AIzaSyC0vz_nYIczwBwNupqMrNhmBm4dQbX5Pbw"
    #id = "7260228cc892a415a"
    i = 1 
    google_api = sys.argv[0+i]
    google_engine = sys.argv[1+i]
    key = google_api
    id = google_engine
    precision = float(sys.argv[2+i])
    inp_list = sys.argv[3+i:]
    inp = ""
    for i in inp_list:
        inp += i + ' '
    
    print("")
    print("Paramters: ")
    print("Client Key = " + str(key))
    print("Engine Key = " + str(id))
    print("Desired Precision = " + str(precision))
    print("Query = " + str(inp))
    print("")
    if inp == '' or inp == ' ':
        print("error, no queries given")
        return
    

    while True:
        links = scrape_web(inp,key, id)
        result, output_text, relevant_links,irrelevant_links = process_feedback(links, precision)
        if result:
            print(output_text)
            exit()
        
        inp = generate_new_input(inp,relevant_links,irrelevant_links)
        print("Current Query = " + str(inp))
        print("")

if __name__ == "__main__":
    main()













