import requests
from bardapi import Bard
import os
import re

res = requests.get("http://192.168.1.42:5001/api")
data = res.json()
msg = data['msg']

bard = Bard(token=msg)
text = input("ช่วยกรุณาบอกอาการอย่าวงละเอียด: ")
result = bard.get_answer(f"I want you to act as a doctor female and come up with help my illness. My first suggestion request is “Explain the most important way you can help me. The answer should be no more than 20 words. in thai. in this following :{text}")['content']
print(result)
print('-------------------------------------------------------------------------')
a=[]
# Splitting the result into sentences
sentences = result.split('\n')
cleaned_text = str
count = 1
for i in sentences:
    cleaned_text = re.sub(r'\([^)]*\)|\*|\:|\ๆ|[a-zA-Z]', '', i).strip()
    # print(cleaned_text, len(cleaned_text))
    # print('-----------------------------------------------------------------')
    if 'หมอ' in cleaned_text:
        cleaned_text = cleaned_text.replace('หมอ', '')
    if 'แพทย์' in cleaned_text:
        cleaned_text = cleaned_text.replace('แพทย์','')
    if 'หญิง' in cleaned_text:
        cleaned_text = cleaned_text.replace('หญิง','')
    if 'ของ' in cleaned_text:
        cleaned_text = cleaned_text.replace('ของ','')
    if 'คุณ' in cleaned_text:
        cleaned_text = cleaned_text.replace('คุณ','')    
    if 'คือ' in cleaned_text:
        cleaned_text = cleaned_text.replace('คือ','') 
    if 'คุณลูกค้า' in cleaned_text:
        cleaned_text = cleaned_text.replace('คุณลูกค้า','')
    if 'ในฐานะ' in cleaned_text:
        cleaned_text = cleaned_text.replace('ในฐานะ','')
    if 'คุณหมอหญิง' in cleaned_text:
        cleaned_text = cleaned_text.replace('คุณหมอหญิง','')
    if 'คำตอบ' in cleaned_text or 'นอกจาก' in cleaned_text or 'มีประสิทธิภาพ' in cleaned_text or 'ซักประวัติ' in cleaned_text or 'สาเหตุของโรค' in cleaned_text or 'วิธีต่อไปนี้' in cleaned_text or 'คำแนะนำเพิ่มเติม' in cleaned_text or 'ดังนี้' in cleaned_text :
        continue
    # if 'วินิจฉัย' in cleaned_text and 'ตรวจ' in cleaned_text:
    #     continue
    if len(cleaned_text) > 55:
        #print(f"{count}, {cleaned_text}, total = {len(cleaned_text)}")
        a.append(cleaned_text)
        count += 1
print(a[0])
# for sentence in sentences:
#     cleaned_sentence = re.sub(r'\([^)]*\)|\*|\:|\ๆ', '', sentence).strip()
#     words = cleaned_sentence.split()
    
#     # Check if the number of words in the sentence is greater than 20
#     if len(words) > 20:
#         print(cleaned_sentence)
