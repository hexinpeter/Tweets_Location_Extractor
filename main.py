import os.path
import sys
from time import time

from trie import Trie
from dis_search import search, process_search_result
from extract import extract_location, extract_tweet, output_name


start = time()

# print the usage of this programme
print "*" * 80
print 'For each address in the location file, this programme aims to find the ' \
'tweetIDs of all the tweets (among the tweets stored in the tweets file) that ' \
'mentions the address name. Whenever a tweet contains words whose combined global ' \
'edit distance are smaller or equal to the maximum_allowed_distance from the address name, its tweetID ' \
'will be recorded and displayed.'
print ""
if len(sys.argv) != 4:
	print "Usage: python main.py tweets_file_name location_file_name max_allowed_distance"
	print "e.g. python main.py training_set_tweets_small.txt US_small.txt 1"
	sys.exit()

# get values from the command line
allowed_errors = int(sys.argv[3])
tweets_file_name = sys.argv[1]
location_file_name = sys.argv[2]

# extraction, two new files will be created (if not already) to contain the processed data
processed_tweets_file_name = output_name(tweets_file_name)
processed_location_file_name = output_name(location_file_name)
if not os.path.isfile(processed_tweets_file_name):
	extract_tweet(tweets_file_name)
if not os.path.isfile(processed_location_file_name):
	extract_location(location_file_name)

# build a tweets Trie
tweets_f = open(processed_tweets_file_name, "r")
tweet_trie = Trie()
for line in tweets_f:
	id_sec = True
	tweet_id = ""
	tweet_content = ""

	for char in line:
		if char == ',':
			id_sec = False
		if id_sec:
			tweet_id += char
		if not id_sec:
			tweet_content += char

	if not tweet_id.isdigit():
		continue

	tweet_id = int(tweet_id)
	tweet_content = tweet_content.strip(',').split()

	for word in tweet_content:
		tweet_trie[word] = tweet_id


# print the output header
print "tweets file: %s" %(tweets_file_name)
print "location file: %s" %(location_file_name)
print "maximum distance: %d" %(allowed_errors)
print "*" * 80
print ""


# process the location query 
location_f = open(processed_location_file_name, "r")
for line in location_f:
	location = line.split()
	results = []
	for index in range(len(location)):
		output = search(tweet_trie, location[index], allowed_errors)
		results.append(output)
	results = process_search_result(results, allowed_errors)
	# report the search results for each query
	for word in location:
		print word.capitalize(),
	print ":"
	if len(results) == 0:
		print "    ",
		print "no required tweetIDs are found"
	for result in results:
		print "    ",
		print "with the distance of %d:" %(result[0])
		print "      ",
		for tweet_id in result[1]:
			print "%s" % (tweet_id),
		print ""
	print ""

end = time()
print "\nTime used: %.2f s" % (end - start)












