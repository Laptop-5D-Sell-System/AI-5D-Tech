import sys
import unicodedata
import numpy as np 
import math
import connectdb as db
sys.stdout.reconfigure(encoding='utf-8')

# Loại bỏ tiếng việt - dấu câu
def remove_accents(input_str):
    nfkd_str = unicodedata.normalize('NFD', input_str)
    no_accent_str = "".join(ch for ch in nfkd_str if unicodedata.category(ch) != 'Mn')
    return no_accent_str

# Cắt chuỗi thành các chuỗi nhỏ
def CatChuoi(string):
	return remove_accents(string.lower()).split()

# Chuyển đổi thành set các từ không trùng lặp - cat chuoi theo cai gi
def getUniqueWords(stringToUnique):
	arrData = [CatChuoi(pro[f'{stringToUnique}']) for pro in db.data_json]
	unique_words = set(word.strip('.,!@#$%^&*()_') for child in arrData for word in child)
	return list(unique_words)

# Đếm số lần xuất hiện của từ trong chuỗi 
def weightAppear(word, string):
	count = 0 
	for i in CatChuoi(string):
		if word == i:
			count += 1000 #Đánh trọng số cực lớn lên nếu chữ có xuất hiện trong đó
	return count

# Tính xác suất của từ trong description
def probability(word, string, stringToUnique):
	count = weightAppear(word, string)
	lenString = len(CatChuoi(string))
	lenAllWords = math.fabs(len(getUniqueWords(stringToUnique)))
	xs_w_sp = ( count + 1 ) / (lenString + lenAllWords)
	return xs_w_sp
