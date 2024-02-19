#just some pseudocode/ideas for part 4: 
import numpy as np 
import nltk
#from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from googleapiclient.discovery import build
import pprint
from bs4 import BeautifulSoup
#print(sw_nltk)
import urllib.request  # the lib that handles the url stuff
import requests
from sklearn.feature_extraction.text import TfidfVectorizer #used to make document vectors 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import heapq
from scipy.sparse import csr_matrix
import sys

nltk.download('stopwords')
nltk.download('punkt')
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
stopwords = ["0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added", "adj", "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against", "ah", "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "ao", "ap", "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar", "are", "aren", "arent", "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "au", "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant", "can't", "cause", "causes", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch", "changes", "ci", "cit", "cj", "cl", "clearly", "cm", "c'mon", "cn", "co", "com", "come", "comes", "con", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn", "couldnt", "couldn't", "course", "cp", "cq", "cr", "cry", "cs", "c's", "ct", "cu", "currently", "cv", "cx", "cy", "cz", "d", "d2", "da", "date", "dc", "dd", "de", "definitely", "describe", "described", "despite", "detail", "df", "di", "did", "didn", "didn't", "different", "dj", "dk", "dl", "do", "does", "doesn", "doesn't", "doing", "don", "done", "don't", "down", "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea", "each", "ec", "ed", "edu", "ee", "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven", "else", "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f", "f2", "fa", "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "first", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings", "gs", "gy", "h", "h2", "h3", "had", "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have", "haven", "haven't", "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hh", "hi", "hid", "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit", "however", "how's", "hr", "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "i'll", "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "interest", "into", "invention", "inward", "io", "ip", "iq", "ir", "is", "isn", "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "iv", "i've", "ix", "iy", "iz", "j", "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "know", "known", "knows", "ko", "l", "l2", "la", "largely", "last", "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "let's", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ll", "ln", "lo", "look", "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mightn't", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n", "n2", "na", "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither", "never", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly", "possible", "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "sf", "shall", "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "should", "shouldn", "shouldn't", "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant", "significantly", "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", "they've", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value", "various", "vd", "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "wa", "want", "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll", "well-b", "went", "were", "we're", "weren", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "who's", "whose", "why", "why's", "wi", "widely", "will", "willing", "wish", "with", "within", "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would", "wouldn", "wouldnt", "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your", "youre", "you're", "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz",]
stop_set = set(stopwords)


def string_generator(string):
    for character in string:
        yield character



def link_to_text(target_url):
    data = urllib.request.urlopen(target_url) # it's a file like object and works just like a file
    link = requests.get(target_url)
    if link.status_code == 200:
        soup = BeautifulSoup(link.content, 'html.parser')
        #get text content from HTML
        text = soup.get_text()
        
        return text
    else:
        # Print an error message if the request failed
        print(f"Error: Failed to fetch URL ({response.status_code})")


    text = data.read()
    return_str = ""
    for line in text: # files are iterable
        return_str += line
    return return_str



def generate_new_input(input,related_res,unrelated_res):

    documents = []
    for i in related_res:
        documents.append(i)
    for i in unrelated_res:
        documents.append(i)

    V = TfidfVectorizer(stop_words='english',token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b')
    V.fit_transform(documents)
    #print('feature names: ',V.get_feature_names_out())
    input_vector = V.transform([input])
    related_list = []
    for i in related_res:
        #print("printing related")
        #print(V.transform([i]))
        related_list.append(V.transform([i]))
    related_vectors = np.array(related_list)
    unrelated_list = []
    for i in unrelated_res:
        #print("printing unrelated")
        #print(V.transform([i]))
        unrelated_list.append(V.transform([i]))
    unrelated_vectors = np.array(unrelated_list)

    a,b,c = 0.9,0.6,0.1
    #print("printing sizes")
    #print(input_vector.shape)
    #print(related_vectors.shape)
    #print(unrelated_vectors.shape)
    new_input_vector_big = a*input_vector+(b*np.sum(related_vectors)/len(related_list))-(c*np.sum(unrelated_vectors)/len(unrelated_list))
    #print("printing new vector")

    #print(new_input_vector_big.shape)

    #temp_arr = new_input_vector_big.toarray()
    #print(temp_arr)
    #sorted_temp = np.sort(temp_arr, axis = 1)
    #new_input_vector_big = csr_matrix(sorted_temp)
    #print(new_input_vector_big)
    #length = new_input_vector_big.shape[1]
    #print(length)
    #new_input_vector = new_input_vector_big[length-3:,:] #extract last two 
    #new_input_vector = new_input_vector_big[:,-1:] #extract last two
    #print(new_input_vector)
    #print(new_input_vector.shape)


    #new_input_words = V.inverse_transform(new_input_vector_big)


    #print("printing new input words")
    #print(new_input_words)
    '''for item in new_input_words:
        for item2 in item:
            input.append(item2)
    print("new input is")
    print(input)'''
    new_input_array = new_input_vector_big.toarray()[0]
    word_heap = []
    heapq.heapify(word_heap)
    for word in V.vocabulary_:
        weight = new_input_array[V.vocabulary_[word]]
        heapq.heappush(word_heap,(-weight,word))
    #print(word_heap)
    top_2_words = []
    input_words = V.inverse_transform(input_vector)[0]
    #print('input words: ',input_words)
    while len(word_heap)!=0:
        _,word = heapq.heappop(word_heap)
        if word in input_words:
            continue
        else:
            top_2_words.append(word)
            if len(top_2_words)==1:
                break
    
    #print(top_2_words)
    #top_2_words.insert(0,input)
    resulting_input = ''
    #for i in input:
        #resulting_input+=i+' '
    resulting_input+=input+' ' 
    for i in top_2_words:
        resulting_input+=i+' '
    #print("current query: " + resulting_input)
    #print(resulting_input)
    return resulting_input

def process_feedback(links, precision):
    total_count = len(links)
    if total_count < 10: 
        return True, "Program ended. Not enough links produced",links, links
    count = 0
    relevant_links, irrelevant_links= [], []
    for i in range(len(links)):
        print('Document #: ',i+1)
        print(links[i].get('link'))
        print(links[i].get('snippet'))
        #answer = ""
        answer = input('Is the document above relevant to your search query? (Y/N): ')
        while True:#answer.lower() != 'y' and answer.lower() != 'n':
            #answer = input('Is the document above relevant to your search query? (Y/N): ')
            if answer.lower()=='y':
                relevant_links.append(links[i].get('snippet'))
                count+=1
                break
            elif answer.lower()=='n':
                irrelevant_links.append(links[i].get('snippet'))
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
    #pprint.pprint(res)
    links = []
    for result in res['items']:
        links.append(result)
        #print(result)
        #print('#1: ',result.get('snippet'))
        #print(' ')
    return links

def main():
    #/home/gkaraman/run <google api key> <google engine id> <precision> <query>
    #key = "AIzaSyC0vz_nYIczwBwNupqMrNhmBm4dQbX5Pbw"
    #id = "7260228cc892a415a"
    i = 0 
    google_api = sys.argv[0+i]
    google_engine = sys.argv[1+i]
    key = google_api
    id = google_engine
    precision = float(sys.argv[2+i])
    inp = sys.argv[3+i]
    #inp = input('What would you like to search for?')
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
    #precision = .9
    while True:
        links = scrape_web(inp,key, id)
        result, output_text, relevant_links,irrelevant_links = process_feedback(links, precision)
        if result:
            print(output_text)
            #print("precision: " + )
            exit()
        #print(inp)
        
        inp = generate_new_input(inp,relevant_links,irrelevant_links)
        print("Current Query = " + str(inp))
        print("")
        #inp_arr = inp_arr.split(' ')
        #break
        #new_search_input = rocchios([inp],relevant_links, irrelevant_links,0.3,0.4,0.3,stop_set)
        #inp = new_search_input.split(' ')
    
    result, output_text,relevant_links, irrelevant_links = process_feedback(links, precision)
    print(result)

if __name__ == "__main__":
    main()











'''
def text_vectors(all_text, stopwords, query_words):
    
    #stop words 
    #sw_nltk = stopwords.words('english')
    #stop_set = set(sw_nltk)
    #clean up text 

    #covert to tokens 
    good_text = []
    for text in all_text:
        text = word_tokenize(text)
        #print(text) #appears to be in sort of a tuple format 
        #remove stop words 
        #good_text = "" #not positive if this was done properly 
        filtered_tokens = [word for word in text if word.isalnum() and word not in stopwords]
        good_text.append(' '.join(filtered_tokens))


    generator = good_text 
    #generator = string_generator(good_text)
    vectorizer = TfidfVectorizer()
    mat = vectorizer.fit_transform(generator) #td-idf vectors 
    #mat = vectorizer.fit(good_text)
    mat_normalized = normalize(mat)
    query_size = len(vectorizer.get_feature_names_out())
    keyword_vector = normalize(vectorizer.transform(query_words).toarray())
    keyword_vector = np.sum(keyword_vector, axis=0, keepdims=True)
    print(query_size)
    query_vector = np.zeros((1, query_size))
    query_vector[:, :keyword_vector.shape[1]] = keyword_vector


    cosine_similarities = cosine_similarity(mat_normalized,query_vector) #not sure on this part 
    #extract most relevant column 
    id = cosine_similarities.argmax()
    important_vec = mat_normalized[id]

    return important_vec


#not sure what to set og_query_weight, related_weight, unrelated_weights to? think this may need to be a part we figure out 
#not exactly sure what og_query_vector will be? 
#also given new query vector - how do we get the exact words? 
def rocchios(og_query_vector, related_links,unrelated_links,og_query_weight, related_weight, unrelated_weight,stopwords):
    #og_query_vector = og_query_vector.split(' ')
    #how to generate the vector for a document 
    related_vectors = []
    all_textsr = [ ]
    counter = 0 
    for link in related_links:
        #convert to text 
        print(counter) #happens on the 3rd article i think 
        counter += 1 
        try:
            text = link_to_text(link)
            all_textsr.append(text)
        except: #convert text to just be the headline? 
        #convert to vector 
            print("we cannot use this related link")
    vector = text_vectors(all_textsr,stopwords,og_query_vector)
    related_vectors.append(vector)
    related_vectors = np.array(related_vectors)

    unrelated_vectors = []
    all_textsu = [ ]
    counter = 0 
    for link in unrelated_links:
        #convert to text 
        print(counter) #happens on the 3rd article i think 
        counter += 1 
        #try:
        text = link_to_text(link)
        all_textsu.append(text)
        #except: #convert text to just be the headline? 
        #convert to vector 
            #print("we cannot use this related link")
    vector2 = text_vectors(all_textsu,stopwords,og_query_vector)
    unrelated_vectors.append(vector2)
    unrelated_vectors = np.array(related_vectors)

    unrelated_vectors = []
    counter2 = 0 
    for link2 in unrelated_links:
        #convert to text 
        print(counter2) #happens on the 3rd article i think 
        counter2 += 1
        try:
            text2 = link_to_text(link2)
            #convert to vector 
            vector2 = text_vectors(text2,stopwords,og_query_vector)
            unrelated_vectors.append(vector2)
        except: 
            print("we cannot use this unrelated link")
    unrelated_vectors = np.array(unrelated_vectors)

    #get sums of vectors
    for i in range(len(related_vectors)):
        print(related_vectors[i].shape)
    #print(related_vectors[3])
    #print(type(related_vectors[3]))
    #print(related_vectors[3])
    r_sum = np.sum(related_vectors)
    ur_sum = np.sum(unrelated_vectors)
    og_sum = np.sum(np.array(og_query_vector)) #not sure on this part 

    related_size = len(related_vectors)
    unrelated_size = len(unrelated_vectors)
    #og_query_vec = 
    #related_doc_vec = 

    #generate related_doc_vec_sum 


    new_vector = og_query_weight*og_query_vec + (related_weight/(related_size))*r_sum - (unrelated_weight/(unrelated_size))*ur_sum
    
    return new_vector #new the new query vector - not sure how to get words from it '''






