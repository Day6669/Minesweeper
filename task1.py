words = [] # Creates an array 
file = open("./words.txt","r") ## Reads the words text file
lines = file.readlines() ## Gives you a list of words from the file
for line in lines: ## Looks at each word in order to be able to rstrip them
    words.append(line.rstrip()) ## removes "\n" from the right in the file from the word otherwise you will get "word\n"
file.close()

def find_word(word):
    low = 0 ## sets the low point as 0
    high = len(words)-1 ## Sets the index
    while high >= low: ## Creates loop until end and start meet in the middle
        mid = (low + high) // 2
        if word == words[mid]:  ## Check for if the word is at the midpoint
            return mid + 1
        elif word > words[mid]: ## Check for if the word is on the right
            low = mid + 1
        else: ## Check for if the word is on the left
            high = mid - 1
if __name__ == "__main__":
    userWord = input("Enter the word you are looking for: ") ## Function to input the word that the user wants to find
    res = find_word(userWord)
    if res:
        print("Found on the line", res) ## Prints this sentence if the word is found
    else:
        print("The word is not in this Dictionary") ## Otherwise prints this sentence if the word is not found