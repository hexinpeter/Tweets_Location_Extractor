Please drag the tweets file and the location file into the same directory as where the codes are.

The programme will generate two text files, which are the processed tweet and location files, in the current directory. The returned result will be printed on the stdout. You may append command ‘> file_name.txt’ behind the below mentioned command to transfer the output to file_name.txt  

Run the code as
>>> python main.py tweets_file_name location_file_name max_allowed_distance
e.g. 
>>> python main.py training_set_tweets_small.txt US_small.txt 1


The programme runtime is shown below
  
Working on the training_set_tweets_small.txt and US_small.txt:
	with max_allowed_distance=0, it takes 5.95s
	with max_allowed_distance=1, it takes 97.26s
	with max_allowed_distance=2, it takes 478.68s

Working on the training_set_tweets.txt:
	each location query takes 90s if the max_allowed_distance=1

