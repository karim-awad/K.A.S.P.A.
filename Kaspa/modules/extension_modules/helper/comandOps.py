def compare_str(a, b):
    if a.lower() == b.lower():
        return True
    return False


def words_2_phrase(words):
    ret = ""
    for word in words:
        ret = ret + " " + word
    return ret


def get_sentences(text, amount):
    words = text.split()
    ret = []
    for word in words:
        ret.append(word)
        tmp = word[::-1] # turn around
        if tmp[0] == ".":
            if len(tmp)> 3:
                amount -= 1
            if amount == 0:
                break
    return words_2_phrase(ret)


def get_text_after(text, key_strings):
    for string in key_strings:  # traverse all keystrings
        if string.lower() in text.lower():  # check if keystring is in text
            ind = text.lower().index(string.lower()) + len(string)  # get end of found keystring
            if text[::-1][0] == "?":
                return text[ind:len(text)-1]
            return text[ind:]
    return None


def filter_string(full_string, string):
    if string.lower() in full_string.lower():  # check if ring is in text
        ind = full_string.lower().index(string.lower()) # get end of found keystring
        ret = full_string[:ind] + full_string[(ind + len(string)):]
        return ret
