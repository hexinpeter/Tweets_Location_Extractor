import re

def extract_location(input_file_name):
	us_data = open(input_file_name, "r")
	output_file_name = output_name(input_file_name)
	location = open(output_file_name, "w")

	tab_count = 0
	for line in us_data:
		name = ""
		for char in line:
			if tab_count == 2:
				name += char
			if tab_count > 2:
				break
			if char == '\t':
				tab_count += 1
		tab_count = 0
		name = re.sub(r'\(historical\)', '', name)
		name = name.lower()
		location.write(name + '\n')

	return output_file_name

def extract_tweet(input_file_name):
	tweet_data = open(input_file_name, "r")
	output_file_name = output_name(input_file_name)
	p_tweet = open(output_file_name ,"w")

	tab_count = 0
	separator = 0
	for line in tweet_data:
		for char in line:
			if tab_count > 2:
				break
			if char == '\t':
				tab_count += 1
			#write the tweetID
			if tab_count == 1 and char.isdigit():
				p_tweet.write(char)
			#write the ',' separator between the tweetID and the tweet message
			if tab_count == 2 and not separator:
				p_tweet.write(',')
				separator = 1
			#write the tweet message
			if tab_count == 2:
				text = process_char(char)
				p_tweet.write(text)
		tab_count = 0
		separator = 0
		p_tweet.write('\n')

	return output_file_name

def output_name(input_file_name):
	return "processed_" + input_file_name


def process_char(char):
	if char.isalpha():
		return char.lower()
	else:
		return " "

