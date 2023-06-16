import logging

from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import requests
from buttons import sura_markup, main_markup, oyatinfo, main_menu
from states import SuralarInfo, Botqw

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode='html')
dp = Dispatcher(bot=bot, storage=MemoryStorage())



@dp.message_handler(text='🔼 Asosiy Menyu', state='*')
@dp.message_handler(commands=['start'], state='*')
async def do_start(message: types.Message, state: FSMContext):
  await state.finish()
  full_name = message.from_user.full_name
  await message.answer(f"Assalomu alaykum {full_name}, xush kelibsiz!", reply_markup=main_markup)

@dp.message_handler(text='⬅️ Orqaga', state=SuralarInfo.oyat)
@dp.message_handler(text='Oyatlar')
async def do_Oyatlar(message: types.Message, state: FSMContext):
  await state.finish()
  await message.answer("Oʻzingizga kerakli suraning raqamini kiriting, nomini yozing yoki tugmalardan foydalaning", reply_markup=sura_markup)
  await SuralarInfo.sura.set()

@dp.message_handler(state=SuralarInfo.sura)
async def get_sura(message: types.Message, state: FSMContext):
    r = requests.get("https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/info.json").json()
    sura_name = message.text.split('.')
    sura_name = str(sura_name[-1])
    chapter = ''
    for sura in r['chapters']:
        if sura['name'] == sura_name:
            chapter += str(sura['chapter'])
            await state.update_data({"sura_name":sura_name})
    
    r2 = requests.get("https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu.json").json()

    verse_len = []
    for i in r2['quran']:
       if i['chapter'] == int(chapter):
          verse_len.append(i['verse'])
    
    await message.answer(f"{sura_name} surasi {verse_len[-1]} ta oyatdan iborat!\nO'qimoqchi bo'lgan oyatingizning raqamini kiriting:\n\nSuraning barcha oyatlarni o'qish uchun 1-{verse_len[-1]} deb xabar jo'nating")
    
    await state.update_data(data={"verse_len":verse_len})
    await state.update_data({"chapter": int(chapter)})

    await SuralarInfo.next()

@dp.message_handler(state=SuralarInfo.oyat)
async def do_oyat(message: types.Message, state: FSMContext):
   data = await state.get_data()
   sura_name = data["sura_name"]
   verse_len = data["verse_len"]
   chapter = data['chapter']

   try: 
    if '-' in str(message.text):
        text = message.text.split('-') 
        if int(text[0]) < int(text[-1]) and int(text[-1]) <= int(verse_len[-1]) > int(text[0]):
            r = requests.get("https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu.json").json()
            
            start = int(text[0])
            stop = int(text[-1])
            for i in range(start, stop + 1):
              for it in r['quran']:
                  if it['chapter'] == chapter:
                    if it['verse'] == int(i):
                        sms = f'<b>{sura_name} surasi {i}-oyat</b>\n\n'
                        sms += f"{it['text']}"
                        await message.answer(sms, reply_markup=oyatinfo)
        else:
          await message.answer("Nato'g'ri kiritdingiz")

    elif ',' in str(message.text):
        text = message.text.split(',')
        r = requests.get("https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu.json").json()
        for t in text:
          if int(t) <= int(verse_len[-1]):
              for i in r['quran']:
                if i['chapter'] == chapter:
                  if i['verse'] == int(t):
                    sms = f'<b>{sura_name} surasi {t}-oyat</b>\n\n'
                    sms += f"{i['text']}"
                    await message.answer(sms, reply_markup=oyatinfo)   

    else:
        if int(message.text) <= int(verse_len[-1]):
          r = requests.get("https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu.json").json()
          for i in r['quran']:
            if i['chapter'] == chapter:
              if i['verse'] == int(message.text):
                sms = f'<b>{sura_name} surasi {message.text}-oyat</b>\n\n'
                sms += f"{i['text']}"
                await message.answer(sms, reply_markup=oyatinfo)
        else:
          await message.answer(f"Suraning barcha oyatlarni o'qish uchun 1-{verse_len[-1]} deb xabar jo'nating!")
   except:
      await message.answer("Nato'g'ri kiritdingiz")


@dp.message_handler(text='⬅️ Orqaga', state=SuralarInfo.sura)
@dp.message_handler(text='⬅️ Orqaga', state=SuralarInfo.oyat)
@dp.message_handler(text='Oyatlar')
async def do_Oyatlar(message: types.Message, state: FSMContext):
  await state.finish()
  await message.answer("Oʻzingizga kerakli suraning raqamini kiriting, nomini yozing yoki tugmalardan foydalaning", reply_markup=sura_markup)
  await SuralarInfo.sura.set()


@dp.message_handler(state=SuralarInfo.sura)
async def get_sura(message: types.Message, state: FSMContext):
    r = requests.get("https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/info.json").json()
    sura_name = message.text.split('.')
    sura_name = str(sura_name[-1])
    chapter = ''
    for sura in r['chapters']:
        if sura['name'] == sura_name:
            chapter += str(sura['chapter'])
            await state.update_data({"sura_name":sura_name})
    
    r2 = requests.get("https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu.json").json()

    verse_len = []
    for i in r2['quran']:
       if i['chapter'] == int(chapter):
          verse_len.append(i['verse'])
    
    await message.answer(f"{sura_name} surasi {verse_len[-1]} ta oyatdan iborat\n\no'qimoqchi bo'lgan oyatingizning raqamini kiriting\n\nyoki ko'proq oyat o'qimoqchi bo'lsangiz oyatlarni quyidagi ko'rinishda kiriting\n\n➡️  2,5,12,13 ....\n\nYoki\n\n➡️  1-5 ko'rinishida xabar jo'nating\n\nSuraning barcha oyatlarni o'qish uchun 1-{verse_len[-1]} deb xabar jo'nating", reply_markup=oyatinfo)
    
    await state.update_data(data={"verse_len":verse_len})
    await state.update_data({"chapter": int(chapter)})

    await SuralarInfo.next()

@dp.message_handler(state=SuralarInfo.oyat)
async def do_oyat(message: types.Message, state: FSMContext):
   data = await state.get_data()
   sura_name = data["sura_name"]
   verse_len = data["verse_len"]
   chapter = data['chapter']

   try: 
    if '-' in str(message.text):
        text = message.text.split('-') 
        if int(text[0]) < int(text[-1]) and int(text[-1]) <= int(verse_len[-1]) > int(text[0]):
            r = requests.get("https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu.json").json()
            
            start = int(text[0])
            stop = int(text[-1])
            for i in range(start, stop + 1):
              for it in r['quran']:
                  if it['chapter'] == chapter:
                    if it['verse'] == int(i):
                        sms = f'<b>{sura_name} surasi {i}-oyat</b>\n\n'
                        sms += f"{it['text']}"
                        await message.answer(sms, reply_markup=oyatinfo)
        else:
          await message.answer("Nato'g'ri kiritdingiz")

    elif ',' in str(message.text):
        text = message.text.split(',')
        r = requests.get("https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu.json").json()
        for t in text:
          if int(t) <= int(verse_len[-1]):
              for i in r['quran']:
                if i['chapter'] == chapter:
                  if i['verse'] == int(t):
                    sms = f'<b>{sura_name} surasi {t}-oyat</b>\n\n'
                    sms += f"{i['text']}"
                    await message.answer(sms, reply_markup=oyatinfo)   

    else:
        if int(message.text) <= int(verse_len[-1]):
          r = requests.get("https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu.json").json()
          for i in r['quran']:
            if i['chapter'] == chapter:
              if i['verse'] == int(message.text):
                sms = f'<b>{sura_name} surasi {message.text}-oyat</b>\n\n'
                sms += f"{i['text']}"
                await message.answer(sms, reply_markup=oyatinfo)
        else:
          await message.answer(f"Suraning barcha oyatlarni o'qish uchun 1-{verse_len[-1]} deb xabar jo'nating!")
   except:
      await message.answer("Nato'g'ri kiritdingiz") 


    
@dp.message_handler(text="Fikr bildirish✍️", state='*')
async def get_qw(message: types.Message, state: FSMContext):
  await state.finish()
  await message.answer("Assalomu alaykum. Fikringizni yozib qoldiring. Adminga xabaringiz yuboriladi.", reply_markup=main_menu)
  await Botqw.fikir.set()

@dp.message_handler(state=Botqw.fikir)
async def get_fikir(message: types.Message):
   await message.answer("Xabar yuborildi", reply_markup=main_markup)

@dp.message_handler(state='*')
async def to_setting(message: types.Message, state: FSMContext):
  await message.answer("Kechirasiz, bu bo'lim hali ishlamayapti!", reply_markup=main_markup)
    

    




if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)