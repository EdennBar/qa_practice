from files_handler_class import Files_handler


pathA = "dirs/a"
pathB = "dirs/b"
pathC = "dirs/c"
min_amount = 1

files_handler = Files_handler(pathA, pathB, pathC)
files_handler.main(min_amount)

'''
1. Please describe what the function is doing, an example of a test case is attached as well.

The main function compares the contents of CSV files: [setA, setB], calculates the matches integer numbers between lists,
if the max_match is greater than or equal min_amount, it copies the fnameA file content to pathC and updating the scores.txt with max_match.
                  
'''