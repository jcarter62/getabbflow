from abbsavedata import AbbSaveData
from random_word import RandomWords

x = AbbSaveData()

rw = RandomWords()

id = "first id for record"
w1 = rw.get_random_word()
w2 = rw.get_random_word()

obj = {"name": "Jim", "item1": w1, "item2": w2}

x.save_record(id, obj)

print(x)
