from dotenv import load_dotenv
import os
"""
Підписи осей радарних графіків окремо для лекторів і практиків
УВАГА послідовність підписів має збігатись з послідовністю індексів відповідей
"""
radar_l=["Якість подачі\nлекційного матеріалу","Актуальність лекційного\nматеріалу",
         "Достатність та\nнаповненість\nлекційного\nматеріалу","Дотримання РСО","Об'єктивність оцінювання",
         "Якість і\nзручність комунікації","Ввічливість","Пунктуальність"]
radar_p=["Дотримання РСО","Об'єктивність\nоцінювання","Якість і зручність\nкомунікації",
         "Ввічливість","Пунктуальність","Зручність здачі робіт"]
"""
Підписи осей гістограм. З урахуванням поточного формату не бажано для назв графіків форматувати текст, аби він перевищував з строки
"""
y_hist="Кількість\nголосів"
hist_11_name="Оцінка власних знаннь після\nвивчення дисципліни"
hist_12_name="Здатність викладача із порозумінням\nставитись до проблем студентів"
"""
Вибірка питаннь формату 1_5 для гістограм і радарних графіків, 
максимальна відмітка використовується в парсері результатів і не застосовується під час
побудови графіків, зміна максимальної відмітки може призвести до неправильного графічного 
відображення даних
"""
l_ans_mask={"radar":[1,2,3,4,5,6,7,8],"hist":[11,12]}
p_ans_mask={"radar":[4,5,6,7,8,14],"hist":[11,12]}
max_mark=5
#current directory, used for creation of results
cur_dir=os.getcwd()
#debug state if True generate results only for "fbme" faculty
debug=True

def ch_cr(path):
    """
    Check is directory exist
    Create directory by folow path if dont
    """
    if not os.path.isdir(path):
        os.makedirs(path)

load_dotenv()

#Database connection variables see README to get structure of .env file

host=os.getenv("HOST")
port=os.getenv("PORT")
db_name=os.getenv("DB_NAME")
user=os.getenv("USER")
password=os.getenv("PASS")
