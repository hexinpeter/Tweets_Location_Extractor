# The following code is modified by Xin He from the code written by Steve Hanov, 2011
# The original code from Steve Hanov is available at http://stevehanov.ca/blog/index.php?id=114

from trie import Trie

def search( trie, word, maxCost ):
    """The search function returns a dict, with the distances as the keys and the 
    sets of corresponding distinct tweetIDs as the values.
    An empty dict will be returned if no suitable tweetIDs is found"""

    # build first row
    currentRow = range( len(word) + 1 )

    results = {}

    # recursively search each branch of the trie
    for letter in trie.branches():
        searchRecursive( trie.next_branch(letter), letter, word, currentRow, 
            results, maxCost )

    return results

# This recursive helper is used by the search function above. It assumes that
# the previousRow has been filled in already.
def searchRecursive( node, letter, word, previousRow, results, maxCost ):

    columns = len( word ) + 1
    currentRow = [ previousRow[0] + 1 ]

    # Build one row for the letter, with a column for each letter in the target
    # word, plus one for the empty string at column 0
    for column in xrange( 1, columns ):

        insertCost = currentRow[column - 1] + 1
        deleteCost = previousRow[column] + 1

        if word[column - 1] != letter:
            replaceCost = previousRow[ column - 1 ] + 1
        else:                
            replaceCost = previousRow[ column - 1 ]

        currentRow.append( min( insertCost, deleteCost, replaceCost ) )

    # if the last entry in the row indicates the optimal cost is less than the
    # maximum cost, and there is a word in this trie node, then add it.
    if currentRow[-1] <= maxCost and node.value_valid:
        try:
            results[currentRow[-1]] = results[currentRow[-1]].union(node.value)
        except KeyError:
            results[currentRow[-1]] = node.value
        #results.append( (node.value, currentRow[-1] ) )

    # if any entries in the row are less than the maximum cost, then 
    # recursively search each branch of the trie
    if min( currentRow ) <= maxCost:
        for letter in node.branches():
            searchRecursive( node.next_branch(letter), letter, word, currentRow, 
                results, maxCost )


# this function is specifically made for the output provided in the main function
def process_search_result(output, allowed_errors):
    """process the search results gotten from different words from the location name, 
    to find the intersection sets""" 
    num_words = len(output)
    result = []
    for dist in output[0].keys():
        result.append([dist, output[0][dist], 1])

    for index in range(1, num_words):
        current_len = len(result)
        for part in result[:current_len]:
            for key in output[index].keys():
                new_key = key + part[0]
                new_set = output[index][key].intersection(part[1])
                if (new_key <= allowed_errors) and (len(new_set) != 0):
                    result.append([new_key, new_set, part[2]+1])
    # cleaning up the result list 
    to_be_removed = []
    num_removed = 0
    storage_index = {}
    for index in range(len(result)):
        if result[index][2] != num_words:
            to_be_removed.append(index)
        else:
            dist = result[index][0]
            id_set = result[index][1]
            if dist not in storage_index.keys():
                storage_index[dist] = index
            else:
                store_index = storage_index[dist]
                result[store_index][1] = result[store_index][1].union(id_set)
                to_be_removed.append(index)
    for index in to_be_removed:
        result.pop(index - num_removed)
        num_removed += 1
    return sorted(result, key=lambda dlist: dlist[0])
