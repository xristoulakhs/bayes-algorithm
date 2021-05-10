import os
import csv


my_path = 'C:\\Users\\...'

def stop_words_to_list():
    lst = []
    with open('stop_words.txt', "r") as file:
        lst = file.read().split()
    return lst

# save dictionary as csv file
def save(file, dictionary):
    with open(file, 'w', newline='', encoding='utf8') as csvFile:
        spam_writer = csv.writer(csvFile, delimiter = ',')
        for keys, value in dictionary.items():
            spam_writer.writerow([keys] + [value])

# load csv file as dictionary
def load(file):
    dictionary = {}
    with open(file, mode='r', encoding='utf8') as infile:
        reader = csv.reader(infile)
        for rows in reader:
            # data = ' '.join(rows)
            # print(data)
            # data = data.split(' ')
            dictionary[rows[0]] = float(rows[1])
    return dictionary


def clean(word):
    stopWords = stop_words_to_list()
    word = word.lower()
    word = word.replace('\n', '')
    word = word.replace('.', '')
    word = word.replace(',', '')
    word = word.replace(':', '')
    word = word.replace('?', '')
    word = word.replace('*', '')
    word = word.replace('!', '')
    word = word.replace('"', '')
    word = word.replace('/', '')
    word = word.replace('(', '')
    word = word.replace(')', '')
    word = word.replace('-', '')
    word = word.replace('&', '')
    word = word.replace('<br />','')
    word = word.replace('//>','')
    word = word.replace('/>','')
    word = word.replace('<br','')
    word = word.replace('/><br','')
    word = word.replace('<','')
    word = word.replace('>','')
    word = word.replace('<br>','')
    word = word.replace('<br >','')
    word = word.replace('\\', '')
    text = word.split(' ')
    text = [t for t in text if t not in stopWords]
    return text



def train(myfile):

    path = my_path + '\\train\\' + str(myfile)
    dictionary = {}
    for filename in os.listdir(path):
        with open(os.path.sep.join([path, filename]), encoding="utf8") as f:
            text = f.read()
            text = clean(text)
            for word in text:
                if word in dictionary:
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1

    # print(dictionary)
    fileCount = len(os.listdir(path))
    for word in dictionary.keys():
        dictionary[word] = float(dictionary[word]) / float(fileCount)
    dictionary["fileCount"] = fileCount
    # print(dictionary)
    return dictionary


def bayes(text, dictionary, priory):
    res_of_probability = 1
    for word in text:
        if word in dictionary.keys():
            res_of_probability *= dictionary[word]
        else:
            res_of_probability *= 1/dictionary['fileCount']+len(dictionary)+1
    res_of_probability *= priory
    return res_of_probability

def test(file):
    path = my_path +'\\test\\' +str(file)
    pos_dict = load('pos.csv')
    neg_dict = load('neg.csv')
    sum_pos = 0
    sum_neg = 0
    i= 0
    for filename in os.listdir(path):
        with open(os.path.sep.join([path, filename]), encoding="utf8") as f:
            text = f.read()
            text = clean(text)
            pos_res = bayes(text,pos_dict, 0.5)
            neg_res = bayes(text,neg_dict, 0.5)
            if (pos_res >= neg_res):
                sum_pos += 1
            else:
                sum_neg += 1
    strtext = 'For '+ str(file) +': pos==> '+str(sum_pos)+' and '+' neg==> '+str(sum_neg)
    print(strtext)

if __name__ == '__main__':
    save('pos.csv', train('pos'))
    save('neg.csv', train('neg'))
    test('pos')
    test('neg')



