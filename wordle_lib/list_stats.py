import string
import matplotlib.pyplot as plt
import json

def get_word_scores(wordlist, ltr_freq, orderedlist=False):
  # ltr_freq is dict of ltr : freq
  word_scores = {word : 0 for word in wordlist}
  
  for word in wordlist:
    for ltr in set(word):     # set() removes duplicate letters
                              # Consider how to handle score when a letter is
                              # known and we wish to test a duplicate
      word_scores[word] += ltr_freq[ltr]
  if orderedlist:
    return sorted(word_scores, key=word_scores.get, reverse=True)
  else:
    return word_scores

def get_ltr_freq(wordlist):
  ltr_freq = {ltr : 0 for ltr in string.ascii_lowercase}
  for word in wordlist:
    for ltr in set(word):  # set() takes out duplicate letters
      ltr_freq[ltr] += 1
  return ltr_freq

if __name__ == "__main__":
  with open("word_list", 'r') as f:
    wordlist = f.read().split()
  
  # This method gives each letter a rating, then reconstructs a rating
  # for each word. Another method may be to begin by giving each word
  # a rating (based on how many other words share a letter in common).
  # Additional considerations: how many other words share letters in same
  # spot? (and is this better or worse?) What if some letters are already
  # known, how should this effect a revised word score?
  # A rating based on how much we learn from the guess? Should depend on
  # what words remain in the list. e.g., (eliminated words) * (remaining words)
  # ^or /? or average words eliminated (based on population of possible solutions)
  ltr_freq = get_ltr_freq(wordlist)
  
  print(ltr_freq)
  
  ordered_freq = sorted(ltr_freq, key=ltr_freq.get, reverse=True)
  ordered_freq = {ltr : ltr_freq[ltr] for ltr in ordered_freq}
  
  print(ordered_freq)
  
  # Consider not only the letters that appear in the most words, but whether
  # some letters frequently show up in the same words. We may learn more by
  # guessing letters that both occur frequently but in different words.
  
  # Ways to assess goodness of a guess:
  # - sum of frequencies
  # - sum of distinct frequencies (each letter key's value should be a list
  # of words?)
  
  # TODO give each word a score, print top 10 words
  
  word_scores = get_word_scores(wordlist, ltr_freq)
  ordered_scores = sorted(word_scores, key=word_scores.get, reverse=True)
  #ordered_scores_dict = {word : word_scores[word] for word in ordered_scores}
  print({word : word_scores[word] for word in ordered_scores[:10]})
  print(word_scores['weary'], ordered_scores.index('weary'),word_scores['yearn'],word_scores['steer'])
  salet = 0
  for ltr in "salet":
    salet += ltr_freq[ltr]
  print(salet)
  if 0:  # Print words with duplicate letters
    dups = 0
    for w in wordlist:
      if len(set(w)) != 5:
        dups += 1
        #print(w)
    print(dups)
  if 0:  # Print json of word list
    print(json.dumps({word : word_scores[word] for word in ordered_scores},indent=2))
  if 0:  # Print word list to csv
    with open("words.csv",'w') as f:
      f.write("word,rating\n")
      for word in word_scores:
        f.write(word + "," + str(word_scores[word]) + '\n')
  
  #ltrs = [ltr for ltr in ordered_freq]
  #freq = [ordered_freq[ltr] for ltr in ltrs]
  # TODO add second y-axis for percentage
  if 0:  # Graph letter frequencies
    padding = 1.05
    ymax = max(ordered_freq.values())
    fig, ax1 = plt.subplots()
    ax1.bar(ordered_freq.keys(),ordered_freq.values())
    ax1.set_ylim(0, ymax * padding)
    ax1.set_ylabel("Number of Words")
    nwords = len(wordlist)
    ax2 = ax1.twinx()
    # need to set ylim on both axs to make them match
    ax2.set_ylim(0, ymax / nwords * 100 * padding)
    ax2.set_ylabel("Percentage out of Possible Solutions")
    ax2.set_yticklabels([f'{x:.0f}%' for x in ax2.get_yticks()])
    # List is ordered we can index instead of using min/max funcs
    #plt.bar(ordered_freq.keys(),ordered_freq.values())
    plt.title("Amount of Words Containing Each Letter")
    plt.show()
