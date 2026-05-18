# using string libary allows me to easily remove punctuation as it is in-built in this library.
import string


def clean_text(essay_path):
    # essay_path is the placeholder name of the file I will call in main()
    # 'r' means I am only giving python the permission to read only.
    with open(essay_path, 'r') as essay_file:
 # This will read the content of the file then immediately convert it to lowercase. 
 # it will remove the case sensitivity when we are comparing the words in those essays
        raw_text = essay_file.read().lower()

        #this loops goes into every punctuation mark each time it runs and replaces it witj an empty string.
        # for example: 'brother,' will become 'brother'.

        for punctuation_mark in string.punctuation:
            raw_text = raw_text.replace(punctuation_mark, '')

            # .split() separates the cleaned text at every space to return a list of individual words.
            # this list will be used by all the other functions.

        word_list = raw_text.split()

    return word_list


def find_common_words(essay1_words, essay2_words):
    # the function converts both word lists into sets.
    # the sets will only contain unique words, so duplication will not occur within each set.

    set1 = set(essay1_words)
    set2 = set(essay2_words)

    # .intersection() finds words that appear in both sets.
    # using function over symbol makes the code more readable and easier as it is plain English.

    common_words = set1.intersection(set2)

    # the results dictionary will store each shared word alongside how many times it was repeated in each essay.

    results = {}

    for shared_word in common_words:
        # using the original word lists not the sets is because sets down't allow duplication.
        # the list keeps all occurence which is necessary for counting how many times each shared word appeared.

        results[shared_word] = {
            'essay1_count': essay1_words.count(shared_word),
            'essay2_count': essay2_words.count(shared_word)
        }

    return results


def search_word(user_input, essay1_words, essay2_words):
    # this function receive the user word they want to search for. 
    # added a default function to clean the usr input by converting it into lowercase.

    cleaned_input = user_input.lower().strip(string.punctuation)

    # the codes will count how many times the cleaned user input appears in each essay's word list.

    essay1_count = essay1_words.count(cleaned_input)
    essay2_count = essay2_words.count(cleaned_input)

    #if the word is not found this codes will return False, 
    # otherwise it will return the counts of the word in both essays.

    if essay1_count == 0 and essay2_count == 0:
        return False

    return {
        'essay1': essay1_count,
        'essay2': essay2_count
    }


def plagiarism_score(essay1_words, essay2_words):

    #converts lists to sets to get unique words.
    unique1 = set(essay1_words)
    unique2 = set(essay2_words)
    
    #overlap is a variable name for the words that appear in both essays (intersection of the both sets).
    overlap = unique1.intersection(unique2)

    #union_of_sets is a variable name for all the unique words that appear in either essay (union of the both sets).
    union_of_sets = unique1.union(unique2)

    # Applying the task formula: (shared words / total unique words) * 100
    # if union of sets is empty (which means both essays have no words), we set the score to 0 to avoid division by zero error.
    score = (len(overlap) / len(union_of_sets)) * 100 if union_of_sets else 0

    score = round(score, 2)

    # as the lab says 50% or higher is considered plagiarism, we will use that as the reasoning for our verdict.
    if score >= 50:
        verdict = "Plagiarism Detected"
    else:
        verdict = "Essays are original"

    return {
        'score': score,
        'verdict': verdict,
        'overlap': len(overlap),
        'unique_count': len(union_of_sets)
    }

def main():
    # loads and cleans both essays by calling the clean_text function
    essay1_words = clean_text('essay-1.txt')
    essay2_words = clean_text('essay-2.txt')

    # "-" * 50 prints the dash character 50 times — creates a clean visual separator
    print("-" * 50)
    print("Plagiarism Detection Output")
    print("-" * 50)
    print(f"Essay 1 loaded: {len(essay1_words)} words")
    print(f"Essay 2 loaded: {len(essay2_words)} words")

    print("\n^^^ Finding common words ^^^")
    results = find_common_words(essay1_words, essay2_words)
    print(f"Total common words found: {len(results)}")

    # I sliced the results to show only the first 30 words
    # so the output does not flood the terminal
    for shared_word, counts in list(results.items())[:30]:
        print(f"  '{shared_word}' → Essay1: {counts['essay1_count']} time(s) | Essay2: {counts['essay2_count']} time(s)")

    # results is reassigned here to hold the plagiarism score output
    print("\n^^^ Plagiarism Score ^^^")
    results = plagiarism_score(essay1_words, essay2_words)
    print(f"Words in common: {results['overlap']}")
    print(f"Total unique words: {results['unique_count']}")
    print(f"Plagiarism Score: {results['score']}%")
    print(f"Verdict: {results['verdict']}")

    print("\n^^^ Word Search ^^^")
    user_input = input("Type a word to search across both essays: ")
    search_results = search_word(user_input, essay1_words, essay2_words)

    # 'is False' is more precise than '== False' when checking a boolean
    if search_results is False:
        print(f"The word '{user_input}' was not found in either essay.")
    else:
        # 'essay1' and 'essay2' are the keys returned by search_word()
        print(f"'{user_input}' → Essay1: {search_results['essay1']} time(s) | Essay2: {search_results['essay2']} time(s)")

    print("-" * 50)


# This line starts the whole program
# Without it the functions above are defined but never executed
if __name__ == "__main__":
    main()