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
        return True, relevant_links
    else:
        return False, relevant_links
    
def main():
    links = ['1','2','3','4','5','6','7','8','9','10']
    result, relevant_links = process_feedback(links)
    print(result)

if __name__ == "__main__":
    main()












