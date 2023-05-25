import shutil
from files_handler_class import Files_handler
import pytest
import os
import csv


@pytest.fixture
def create_directories():
    pathA = "dirs/a"
    pathB = "dirs/b"
    pathC = "dirs/c"

    if not os.path.exists(pathA):
        os.makedirs(pathA)
    if not os.path.exists(pathB):
        os.makedirs(pathB)
    if not os.path.exists(pathC):
        os.makedirs(pathC)
    return pathA, pathB, pathC

@pytest.fixture
def files_handler(create_directories):
    pathA, pathB, pathC = create_directories
    return Files_handler(pathA, pathB, pathC)


# Test Case: Validate the input type of int
def test_is_int(files_handler):
    assert files_handler.is_int(2) == True

# Test Case: Validate the input type of string
def test_is_int_string(files_handler):
    assert files_handler.is_int("abc") == False

# Test Case: Validate the input type of float
def test_is_int_float(files_handler):
    assert files_handler.is_int(0.25) == False


# Test Case: Validate existence of path
def test_check_if_path_exist(files_handler):
    assert files_handler.check_if_path_exist(['dirs/a', 'dirs/b', 'dirs/c']) == True
    assert files_handler.check_if_path_exist(['dirs/a', 'dirs/b', 'dirs/d']) == False


# Test Case: Validate matching values
def test_compare_sets(files_handler):
    set_a = [7, 8, 9]
    set_b = [9, 10, 11]
    assert files_handler.compare_sets(set_a, set_b) == 1

# Test Case: Validate non matching values
def test_compare_sets_without_matches(files_handler):
    set_a = [7, 8, 9]
    set_b = [10, 11, 12]
    assert files_handler.compare_sets(set_a, set_b) == 0

# Test Case: Validate contents of newly created files
def test_min_is_equal_to_one(files_handler):
    min_amount = 1
    expected_content = "1,2,3,4,5,11"
    expected_score = "dirs/a\\1.csv    1"

    files_handler.main(min_amount)
    with open("dirs/c/1.csv") as f:
        contentList = f.readline().strip()

    with open("dirs/c/scores.txt") as f:
        score = f.readline().strip()
    assert contentList == expected_content
    assert score == expected_score


# Test Case: Validate the functionality when min_amount is equal to string.
def test_min_is_equal_to_string(files_handler):
    min_amount = "abc"
    with pytest.raises(Exception):
        files_handler.main(min_amount)


# Test Case: Validate the functionality when min_amount > 1
def test_min_amount_is_bigger_then_two(files_handler):
    min_amount = 2
    files_handler.main(min_amount)
    assert not os.listdir('dirs/c'),  "The scores.txt and 1.csv files should exist because there is a match"


# Test Case: Validate the functionality when min_amount = -1 and the content is not matching between two csv.
def test_min_is_equal_to_minus_one(files_handler):
    min_amount = -1
    csv_a_data = ['1', '2', '3', '4', '5']
    csv_b_data = ['7', '8', '9']
    f = open("dirs/a/1.csv", "w")
    f.truncate()
    f.close()

    f = open("dirs/b/2.csv", "w")
    f.truncate()
    f.close()

    with open('dirs/a/1.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_a_data)

    with open('dirs/b/2.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_b_data)

    files_handler.main(min_amount)
    assert not os.listdir('dirs/c'), "C folder is supposed to be empty"



def test_compare_array_of_objects(files_handler):
    arrayOfObj = [{
        "color": "purple",
        "type": "1",
    },{
        "color": "red",
        "type": "2",
    },{
        "color": "grey",
        "type": "3",
    }]
    arrayOfObjects = [{
        "color": "black",
        "type": "2",
    }, {
        "color": "pink",
        "type": "5",
    }, {
        "color": "grey",
        "type": "6",
    }]
    with pytest.raises(TypeError):
        files_handler.compare_sets(arrayOfObj, arrayOfObjects)

def test_compare_json(files_handler):
    json = {
        "color": "purple",
        "type": "1",
    },{
        "color": "red",
        "type": "2",
    },{
        "color": "grey",
        "type": "3",
    }
    json1 = {
        "color": "black",
        "type": "2",
    }, {
        "color": "pink",
        "type": "5",
    }, {
        "color": "grey",
        "type": "6",
    }
    with pytest.raises(TypeError):
        files_handler.compare_sets(json, json1)


def test_compare_sets_of_string(files_handler):
    set_a = ['a', 'b', 'c']
    set_b = ['d', 'e', 'c']
    assert files_handler.compare_sets(set_a, set_b) == 1

'''
the main method does not actually check if there are any files in the directories.
running this test case will lead to an error to due bad main function implementation.
'''
# Test Case: Validate the functionality when there are no CSV files in pathA.
def test_without_csv_a(files_handler):
    min_amount = 1
    file_path_a = "dirs/a/1.csv"
    os.remove(file_path_a)
    files_handler.main(min_amount)
    with pytest.raises(FileNotFoundError):
        files_handler.main(min_amount)


# Test Case: Validate the functionality when there are no CSV files in pathA or pathB.
def test_without_csv_a_and_csv_b(files_handler):
    min_amount = 1
    file_path_b = "dirs/b/2.csv"
    os.remove(file_path_b)
    files_handler.main(min_amount)
    with pytest.raises(FileNotFoundError):
        files_handler.main(min_amount)


# Test Case: Validate the functionality when there are no folders.
def test_without_dirA_dirB_dirC(files_handler):
    min_amount = 1
    file_path_a = "dirs/a"
    file_path_b = "dirs/b"
    file_path_c = "dirs/c"
    shutil.rmtree(file_path_a)
    shutil.rmtree(file_path_b)
    shutil.rmtree(file_path_c)
    with pytest.raises(FileNotFoundError):
        files_handler.main(min_amount)


# Test Case: Validate the functionality when there are no "dirs" folder.
def test_without_dirs_folder(files_handler):
    min_amount = 1
    file_path_dirs_folder = "dirs"
    shutil.rmtree(file_path_dirs_folder)
    with pytest.raises(FileNotFoundError):
        files_handler.main(min_amount)


'''  
 Test Case: Create a performance test by creating as many files as you can and checking how long it takes to complete 
 iterating over all the files.
'''





