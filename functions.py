import re, csv
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

def female_names_generator(filepath):
    with open(filepath) as f:
        female_names = f.read().splitlines()[7:]
    return female_names

def male_names_generator(filepath):
    with open(filepath) as f:
        male_names = f.read().splitlines()[7:]
    return male_names

def movie_titles_generator(filepath):
    df = pd.read_csv(filepath, names=['title', 'url', 'clean_title'])
    return df

def read_script(filepath):
    """Takes a .txt filepath from the IMSDB scraped scripts folder
        and creates a parsed script
        Args:
            filepath : *.txt
        Returns:
            a list of script lines
    """
    with open(filepath) as f:
        script = f.read().splitlines()
    return script

def break_scenes(script):
    """Breaks a script into scenes after identifying headings
        Args:
            script: list of str, a parsed script
        Returns:
            a list of scenes
    """
    headings = sorted([i for i,line in enumerate(script) if ('INT.' in line or 'EXT.' in line)])
    headings.append(len(script))
    scenes = [script[headings[i]+1:headings[i+1]] for i in range(len(headings)-1)]
    return scenes

def extract_characters(script_slice, indent=15):
    """Extracts characters from a full script or a scene
        Args:
            script_slice: list of str, a parsed script (or scene)
            indent : number of spaces before character name
        Returns:
            a list of unique characters
    """
    characters = []
    for line in script_slice:
        if len(line.lstrip()) !=0:
            if len(line)-len(line.lstrip()) > indent and line.lstrip()[0] != '(':
                character = line.strip()
                character = "".join(re.split("\(|\)|\[|\]", character)[::2]).strip()
                characters.append(character)
    return list(set(characters))

def female_count(script_slice, female_names):
    """Counts number of female names in a script
        Args:
            script_slice: list of str, a parsed script (or scene)
            female_names : list of female names
        Returns:
            number of female names in the script slice
    """
    characters = extract_characters(script_slice, indent=15)
    female_count = 0
    for character in characters:
        if character.title() in female_names:
            female_count += 1
    return female_count

def scene_tokenizer(script_slice):
    """Takes a scene and returns all the words present
        Args:
            script_slice: list of str
        Returns:
            a list of unique words
    """
    vectorizer = CountVectorizer(stop_words='english', lowercase=False)
    BOW = vectorizer.fit_transform(script_slice).toarray()
    tokens = vectorizer.get_feature_names()
    characters = extract_characters(script_slice, indent=15)
    for character in characters:
        if character in tokens:
            tokens.remove(character)
    return tokens

def bechdel_test_1(script, female_names):
    """Tests wheter a script passes the First Bechdel Test :
        There are two female names in the script
        Args:
            script: list of str, a parsed script
        Returns:
            Bool : True if the script passes the test, False otherwise
    """
    count = female_count(script, female_names)
    return count > 1

def bechdel_test_2(script, female_names):
    """Tests wheter a script passes the Second Bechdel Test :
        Two female women are talking in a scene
        Args:
            script: list of str, a parsed script
        Returns:
            Bool : True if the script passes the test, False otherwise
    """
    scenes = break_scenes(script)
    for scene in scenes:
        if female_count(scene, female_names) > 1:
            return True
    return False

def bechdel_test_3(script, female_names, male_names):
    """Tests wheter a script passes the Third Bechdel Test :
        Two female women are talking in a scene about something other than a man
        Args:
            script: list of str, a parsed script
        Returns:
            Bool : True if the script passes the test, False otherwise
    """
    scenes = break_scenes(script)
    for scene in scenes:
        test_passed = False
        if female_count(scene, female_names) > 1:
            test_passed = True
            tokens = scene_tokenizer(scene)
            for token in tokens:
                if token in male_names:
                    # we found a male name we should explore another scene'
                    test_passed = False
                    break
            if test_passed:
                # we went through all the tokens without setting test_passed to false
                return test_passed
    # we went through all the scenes without returing True
    return test_passed
