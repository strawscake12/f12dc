# -*-coding: utf-8 -*-

from DinnAPI.linepy import *
from DinnAPI.akad.ttypes import Message
from DinnAPI.akad.ttypes import ContentType as Type
from DinnAPI.akad.ttypes import ChatRoomAnnouncementContents
from gtts import gTTS
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from googletrans import Translator
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, six, ast, pytz, urllib, urllib3, urllib.parse, traceback, atexit

client = LINE("Eu6O2Eq7XpIDPWVwwHG8.T/0Vn2E9Xul8wJjjACMpIa.C0kvjqmPQU4npoGZNrjndzZf34X40aCAuRbYjwVzRnI=")
#client = LINE("")
clientMid = client.profile.mid
clientProfile = client.getProfile()
clientSettings = client.getSettings()
clientPoll = OEPoll(client)
botStart = time.time()

msg_dict = {}

settings = {
    "userAgent": ['Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'],
    "autoAdd": False,
    "autoJoin": False,
    "autoLeave": False,
    "autoRead": False,
    "autoRespon": False,
    "autoJoinTicket": False,
    "checkContact": False,
    "checkPost": False,
    "checkSticker": False,
    "changePictureProfile": False,
    "Welcome": False,
    "wcMsg":False,
    "leaveMessage":False,
    "Addimage":False,
    "changeGroupPicture": [],
    "keyCommand": "",
    "myProfile": {
        "displayName": "",
        "coverId": "",
        "pictureStatus": "",
        "statusMessage": ""
    },
    "mimic": {
        "copy": False,
        "status": False,
        "target": {}
    },
    "setKey": False,
    "unsendMessage": False
}

read = {
    "ROM": {},
    "readPoint": {},
    "readMember": {},
    "readTime": {}
}

list_language = {
    "list_textToSpeech": {
        "id": "Indonesia",
        "af" : "Afrikaans",
        "sq" : "Albanian",
        "ar" : "Arabic",
        "hy" : "Armenian",
        "bn" : "Bengali",
        "ca" : "Catalan",
        "zh" : "Chinese",
        "zh-cn" : "Chinese (Mandarin/China)",
        "zh-tw" : "Chinese (Mandarin/Taiwan)",
        "zh-yue" : "Chinese (Cantonese)",
        "hr" : "Croatian",
        "cs" : "Czech",
        "da" : "Danish",
        "nl" : "Dutch",
        "en" : "English",
        "en-au" : "English (Australia)",
        "en-uk" : "English (United Kingdom)",
        "en-us" : "English (United States)",
        "eo" : "Esperanto",
        "fi" : "Finnish",
        "fr" : "French",
        "de" : "German",
        "el" : "Greek",
        "hi" : "Hindi",
        "hu" : "Hungarian",
        "is" : "Icelandic",
        "id" : "Indonesian",
        "it" : "Italian",
        "ja" : "Japanese",
        "km" : "Khmer (Cambodian)",
        "ko" : "Korean",
        "la" : "Latin",
        "lv" : "Latvian",
        "mk" : "Macedonian",
        "no" : "Norwegian",
        "pl" : "Polish",
        "pt" : "Portuguese",
        "ro" : "Romanian",
        "ru" : "Russian",
        "sr" : "Serbian",
        "si" : "Sinhala",
        "sk" : "Slovak",
        "es" : "Spanish",
        "es-es" : "Spanish (Spain)",
        "es-us" : "Spanish (United States)",
        "sw" : "Swahili",
        "sv" : "Swedish",
        "ta" : "Tamil",
        "th" : "Thai",
        "tr" : "Turkish",
        "uk" : "Ukrainian",
        "vi" : "Vietnamese",
        "cy" : "Welsh"
    },
    "list_translate": {    
        "af": "afrikaans",
        "sq": "albanian",
        "am": "amharic",
        "ar": "arabic",
        "hy": "armenian",
        "az": "azerbaijani",
        "eu": "basque",
        "be": "belarusian",
        "bn": "bengali",
        "bs": "bosnian",
        "bg": "bulgarian",
        "ca": "catalan",
        "ceb": "cebuano",
        "ny": "chichewa",
        "zh-cn": "chinese (simplified)",
        "zh-tw": "chinese (traditional)",
        "co": "corsican",
        "hr": "croatian",
        "cs": "czech",
        "da": "danish",
        "nl": "dutch",
        "en": "english",
        "eo": "esperanto",
        "et": "estonian",
        "tl": "filipino",
        "fi": "finnish",
        "fr": "french",
        "fy": "frisian",
        "gl": "galician",
        "ka": "georgian",
        "de": "german",
        "el": "greek",
        "gu": "gujarati",
        "ht": "haitian creole",
        "ha": "hausa",
        "haw": "hawaiian",
        "iw": "hebrew",
        "hi": "hindi",
        "hmn": "hmong",
        "hu": "hungarian",
        "is": "icelandic",
        "ig": "igbo",
        "id": "indonesian",
        "ga": "irish",
        "it": "italian",
        "ja": "japanese",
        "jw": "javanese",
        "kn": "kannada",
        "kk": "kazakh",
        "km": "khmer",
        "ko": "korean",
        "ku": "kurdish (kurmanji)",
        "ky": "kyrgyz",
        "lo": "lao",
        "la": "latin",
        "lv": "latvian",
        "lt": "lithuanian",
        "lb": "luxembourgish",
        "mk": "macedonian",
        "mg": "malagasy",
        "ms": "malay",
        "ml": "malayalam",
        "mt": "maltese",
        "mi": "maori",
        "mr": "marathi",
        "mn": "mongolian",
        "my": "myanmar (burmese)",
        "ne": "nepali",
        "no": "norwegian",
        "ps": "pashto",
        "fa": "persian",
        "pl": "polish",
        "pt": "portuguese",
        "pa": "punjabi",
        "ro": "romanian",
        "ru": "russian",
        "sm": "samoan",
        "gd": "scots gaelic",
        "sr": "serbian",
        "st": "sesotho",
        "sn": "shona",
        "sd": "sindhi",
        "si": "sinhala",
        "sk": "slovak",
        "sl": "slovenian",
        "so": "somali",
        "es": "spanish",
        "su": "sundanese",
        "sw": "swahili",
        "sv": "swedish",
        "tg": "tajik",
        "ta": "tamil",
        "te": "telugu",
        "th": "thai",
        "tr": "turkish",
        "uk": "ukrainian",
        "ur": "urdu",
        "uz": "uzbek",
        "vi": "vietnamese",
        "cy": "welsh",
        "xh": "xhosa",
        "yi": "yiddish",
        "yo": "yoruba",
        "zu": "zulu",
        "fil": "Filipino",
        "he": "Hebrew"
    }
}

try:
    with open("Log_data.json","r",encoding="utf_8_sig") as f:
        msg_dict = json.loads(f.read())
except:
    print("Couldn't read Log data")
    
settings["myProfile"]["displayName"] = clientProfile.displayName
settings["myProfile"]["statusMessage"] = clientProfile.statusMessage
settings["myProfile"]["pictureStatus"] = clientProfile.pictureStatus
coverId = client.getProfileDetail()["result"]["objectId"]
settings["myProfile"]["coverId"] = coverId




#Dont sell it fcking bitch *Akhirnya bisa bhs inggris
def changeVideoAndPictureProfile(pict, vids):
    try:
        files = {'file': open(vids, 'rb')}
        obs_params = client.genOBSParams({'oid': clientMid, 'ver': '2.0', 'type': 'video', 'cat': 'vp.mp4', 'name': 'Hello_World.mp4'})
        data = {'params': obs_params}
        r_vp = client.server.postContent('{}/talk/vp/upload.nhn'.format(str(client.server.LINE_OBS_DOMAIN)), data=data, files=files)
        if r_vp.status_code != 201:
            return "Failed update profile"
        client.updateProfilePicture(pict, 'vp')
        return "Success update profile"
    except Exception as e:
        raise Exception("Error change video and picture profile %s"%str(e))
def restartBot():
    print ("[ INFO ] BOT RESTART")
    python = sys.executable
    os.execl(python, python, *sys.argv)

def sendLineMusic(to):
    contentMetadata = {
        'countryCode': 'ID',
        'i-installUrl': "http://line.me/ti/p/{}".format(client.getUserTicket().id), 
        'a-packageName': 'com.spotify.music',
        'linkUri': "http://line.me/ti/p/{}".format(client.getUserTicket().id), 
        'type': 'mt',
        'previewUrl':"http://dl.profile.line-cdn.net/{}".format(client.profile.pictureStatus),
        'a-linkUri': "http://line.me/ti/p/{}".format(client.getUserTicket().id), 
        'text': client.profile.displayName,
        'id': 'mt000000000a6b79f9',
        'subText': client.profile.statusMessage
    }
    return client.sendMessage(to, 'Dinn~', contentMetadata, 19)

    
def logError(text):
    client.log("[ ERROR ] {}".format(str(text)))
    tz = pytz.timezone("Asia/Jakarta")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow,"(%H:%M)")
    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime('%A')
    bln = inihari.strftime('%m')
    for i in range(len(day)):
        if hr == day[i]: hasil = hari[i]
    for k in range(0, len(bulan)):
        if bln == str(k): bln = bulan[k-1]
    time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime('%d')), str(bln), str(inihari.strftime('%Y')), str(inihari.strftime('%H:%M:%S')))
    with open("logError.txt","a") as error:
        error.write("\n[ {} ] {}".format(str(time), text))

def cTime_to_datetime(unixtime):
    return datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))
def dt_to_str(dt):
    return dt.strftime('%H:%M:%S')

def delete_log():
    ndt = datetime.now()
    for data in msg_dict:
        if (datetime.utcnow() - cTime_to_datetime(msg_dict[data]["createdTime"])) > timedelta(1):
            if "path" in msg_dict[data]:
                client.deleteFile(msg_dict[data]["path"])
            del msg_dict[data]
            
def sendMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@zeroxyuuki "
    if mids == []:
        raise Exception("Invalid mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mids")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
        textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    client.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)

def command(text):
    pesan = text.lower()
    if settings["setKey"] == True:
        if pesan.startswith(settings["keyCommand"]):
            cmd = pesan.replace(settings["keyCommand"],"")
        else:
            cmd = "Undefined command"
    else:
        cmd = text.lower()
    return cmd
    
def helpmessage():
    if settings['setKey'] == True:
        key = settings['keyCommand']
    else:
        key = ''
    helpMessage =   "╔══[ Help Message ]" + "\n" + \
                    "╠ " + "「 Self Bot By Dinn」" + "\n" + \
                    "╠ " + key + "Help" + "\n" + \
                    "╠ " + key + "Translate" + "\n" + \
                    "╠ " + key + "TTS" + "\n" + \
                    "╠ " + key + "Restart" + "\n" + \
                    "╠ " + key + "Runtime" + "\n" + \
                    "╠ " + key + "Sp" + "\n" + \
                    "╠ " + key + "Status" + "\n" + \
                    "╠══[ Self Help ]" + "\n" + \
                    "╠ " + key + "About" + "\n" + \
                    "╠ " + key + "Errorlog" + "\n" + \
                    "╠ " + key + "Resetlog" + "\n" + \
                    "╠ " + key + "Myself" + "\n" + \
                    "╠ " + key + "Settings" + "\n" + \
                    "╠ " + key + "Group" + "\n" + \
                    "╠ " + key + "Media" + "\n" + \
                    "╠══[ Key Set ]" + "\n" + \
                    "╠ SetKey:" + "\n" + \
                    "╠ MyKey" + "\n" + \
                    "╠ KeyMode 「On/Off」" + "\n" + \
                    "╚══[ Jangan Typo ] "
    return helpMessage

def helpmyself():
    if settings['setKey'] == True:
        key = settings['keyCommand']
    else:
      key = ''
    helpMySelf =    "╔═══[Self Command] +" "\n" + \
                    "╠ " + key + "CName:「TEXT」" + "\n" + \
                    "╠ " + key + "CBio:「TEXT」" + "\n" + \
                    "╠ " + key + "Me" + "\n" + \
                    "╠ " + key + "MyMid" + "\n" + \
                    "╠ " + key + "MyName" + "\n" + \
                    "╠ " + key + "MyBio" + "\n" + \
                    "╠ " + key + "MyPicture" + "\n" + \
                    "╠ " + key + "MyVideoProfile" + "\n" + \
                    "╠ " + key + "MyCover" + "\n" + \
                    "╠ " + key + "CuriContact 「Mention」" + "\n" + \
                    "╠ " + key + "StealMid 「Mention」" + "\n" + \
                    "╠ " + key + "StealName 「Mention」" + "\n" + \
                    "╠ " + key + "StealBio 「Mention」" + "\n" + \
                    "╠ " + key + "StealPicture 「Mention」" + "\n" + \
                    "╠ " + key + "CuriVideoProfil 「Mention」" + "\n" + \
                    "╠ " + key + "CuriCover 「Mention」" + "\n" + \
                    "╠ " + key + "Copy 「Mention」" + "\n" + \
                    "╠ " + key + "Restore" + "\n" + \
                    "╚══[ Support: Team Child Bot ]" + "\n" + \
                    "╔══[ Special Command Self ] " + "\n" + \
                    "╠ " + key + "Gcast 「TEXT」" + "\n" + \
                    "╠ " + key + "Annag 「TEXT」" + "\n" + \
                    "╠ " + key + "Dinnkawai" + "\n" + \
                    "╠ " + key + "CPP 「Ganti Pp」" + "\n" + \
                    "╚══[ ~Support: Dinn]"
    return helpMySelf

def helpsettings():
    if settings['setKey'] == True:
        key = settings['keyCommand']
    else:
        key = ''
    helpSettings =  "╔══[ Settings Command ]" + "\n" + \
                    "╠ " + key + "AutoAdd「On/Off」" + "\n" + \
                    "╠ " + key + "AutoJoin「On/Off」" + "\n" + \
                    "╠ " + key + "AutoJoinTicket「On/Off」" + "\n" + \
                    "╠ " + key + "AutoLeave「On/Off」" + "\n" + \
                    "╠ " + key + "AutoRead「On/Off」" + "\n" + \
                    "╠ " + key + "AutoRespon「On/Off」" + "\n" + \
                    "╠ " + key + "CekContact「On/Off」" + "\n" + \
                    "╠ " + key + "CekPost「On/Off」" + "\n" + \
                    "╠ " + key + "CekSticker「On/Off」" + "\n" + \
                    "╠ " + key + "UnsendChat「On/Off」" + "\n" + \
                    "╚══[ ᵀᴱᴬᴹ ᶜᴴᴵᴸᴰ ᴮᴼᵀ ]"
    return helpSettings
def helpgroup():
    if settings['setKey'] == True:
        key = settings['keyCommand']
    else:
        key = ''
    helpGroup =     "╔══[ Group Command ]" + "\n" + \
                    "╠ " + key + "Gcr" + "\n" + \
                    "╠ " + key + "GId" + "\n" + \
                    "╠ " + key + "GName" + "\n" + \
                    "╠ " + key + "GPict" + "\n" + \
                    "╠ " + key + "Url" + "\n" + \
                    "╠ " + key + "Url 「On/Off」" + "\n" + \
                    "╠ " + key + "GList" + "\n" + \
                    "╠ " + key + "Memlist" + "\n" + \
                    "╠ " + key + "GInfo" + "\n" + \
                    "╠ " + key + "CGP" + "\n" + \
                    "╠ " + key + "Tagall" + "\n" + \
                    "╠ " + key + "Setspamcall: 「Num」" + "\n" + \
                    "╠ " + key + "Spamcall " + "\n" + \
                    "╠ " + key + "Announce" + "\n" + \
                    "╠ " + key + "Delannounce" + "\n" + \
                    "╠ " + key + "Kick 「Mention」" + "\n" + \
                    "╠ " + key + "Mimicadd 「Mention」" + "\n" + \
                    "╠ " + key + "Mimicdel 「Mention」" + "\n" + \
                    "╠ " + key + "MimicList" + "\n" + \
                    "╚══[ ᵀᴱᴬᴹ ᶜᴴᴵᴸᴰ ᴮᴼᵀ ]"

    return helpGroup

def helpmedia():
    if settings['setKey'] == True:
        key = settings['keyCommand']
    else:
        key = ''
    helpMedia =  "╔══[ Media Command ]" + "\n" + \
                 "╠ " + key + "Addpict " + "\n" + \
                 "╠ " + key + "Anime 「Judul」 " + "\n" + \
                 "╠ " + key + "Quotes" + "\n" + \
                 "╠ " + key + "Murottal" + "\n" + \
                 "╠ " + key + "1cak" + "\n" + \
                 "╠ " + key + "CekDate 「Date」" + "\n" + \
                 "╠ " + key + "CekWebsite 「URL」" + "\n" + \
                 "╠ " + key + "CekPraytime 「Location」" + "\n" + \
                 "╠ " + key + "CekWeather 「Location」" + "\n" + \
                 "╠ " + key + "CekLocation 「Location」" + "\n" + \
                 "╠ " + key + "InstaInfo 「UserName」" + "\n" + \
                 "╠ " + key + "InstaPost 「UserName」|「Number」" + "\n" + \
                 "╠ " + key + "InstaStory 「UserName」|「Number」" + "\n" + \
                 "╠ " + key + "SearchYoutube「Judul」" + "\n" + \
                 "╠ " + key + "SearchMusic 「Judul」" + "\n" + \
                 "╠ " + key + "SearchLyric 「Judul」" + "\n" + \
                 "╠ " + key + "SearchImage 「Judul」" + "\n" + \
                 "╚══[ ᵀᴱᴬᴹ ᶜᴴᴵᴸᴰ ᴮᴼᵀ ]"
    return helpMedia

def helptexttospeech():
    if settings['setKey'] == True:
        key = settings['keyCommand']
    else:
        key = ''
    helpTextToSpeech =  "╔══[ Help TextToSpeech ]" + "\n" + \
                        "╠ " + key + "af : Afrikaans" + "\n" + \
                        "╠ " + key + "sq : Albanian" + "\n" + \
                        "╠ " + key + "ar : Arabic" + "\n" + \
                        "╠ " + key + "hy : Armenian" + "\n" + \
                        "╠ " + key + "bn : Bengali" + "\n" + \
                        "╠ " + key + "ca : Catalan" + "\n" + \
                        "╠ " + key + "zh : Chinese" + "\n" + \
                        "╠ " + key + "zhcn : Chinese (Mandarin/China)" + "\n" + \
                        "╠ " + key + "zhtw : Chinese (Mandarin/Taiwan)" + "\n" + \
                        "╠ " + key + "zhyue : Chinese (Cantonese)" + "\n" + \
                        "╠ " + key + "hr : Croatian" + "\n" + \
                        "╠ " + key + "cs : Czech" + "\n" + \
                        "╠ " + key + "da : Danish" + "\n" + \
                        "╠ " + key + "nl : Dutch" + "\n" + \
                        "╠ " + key + "en : English" + "\n" + \
                        "╠ " + key + "enau : English (Australia)" + "\n" + \
                        "╠ " + key + "enuk : English (United Kingdom)" + "\n" + \
                        "╠ " + key + "enus : English (United States)" + "\n" + \
                        "╠ " + key + "eo : Esperanto" + "\n" + \
                        "╠ " + key + "fi : Finnish" + "\n" + \
                        "╠ " + key + "fr : French" + "\n" + \
                        "╠ " + key + "de : German" + "\n" + \
                        "╠ " + key + "el : Greek" + "\n" + \
                        "╠ " + key + "hi : Hindi" + "\n" + \
                        "╠ " + key + "hu : Hungarian" + "\n" + \
                        "╠ " + key + "is : Icelandic" + "\n" + \
                        "╠ " + key + "id : Indonesian" + "\n" + \
                        "╠ " + key + "it : Italian" + "\n" + \
                        "╠ " + key + "ja : Japanese" + "\n" + \
                        "╠ " + key + "km : Khmer (Cambodian)" + "\n" + \
                        "╠ " + key + "ko : Korean" + "\n" + \
                        "╠ " + key + "la : Latin" + "\n" + \
                        "╠ " + key + "lv : Latvian" + "\n" + \
                        "╠ " + key + "mk : Macedonian" + "\n" + \
                        "╠ " + key + "no : Norwegian" + "\n" + \
                        "╠ " + key + "pl : Polish" + "\n" + \
                        "╠ " + key + "pt : Portuguese" + "\n" + \
                        "╠ " + key + "ro : Romanian" + "\n" + \
                        "╠ " + key + "ru : Russian" + "\n" + \
                        "╠ " + key + "sr : Serbian" + "\n" + \
                        "╠ " + key + "si : Sinhala" + "\n" + \
                        "╠ " + key + "sk : Slovak" + "\n" + \
                        "╠ " + key + "es : Spanish" + "\n" + \
                        "╠ " + key + "eses : Spanish (Spain)" + "\n" + \
                        "╠ " + key + "esus : Spanish (United States)" + "\n" + \
                        "╠ " + key + "sw : Swahili" + "\n" + \
                        "╠ " + key + "sv : Swedish" + "\n" + \
                        "╠ " + key + "ta : Tamil" + "\n" + \
                        "╠ " + key + "th : Thai" + "\n" + \
                        "╠ " + key + "tr : Turkish" + "\n" + \
                        "╠ " + key + "uk : Ukrainian" + "\n" + \
                        "╠ " + key + "vi : Vietnamese" + "\n" + \
                        "╠ " + key + "cy : Welsh" + "\n" + \
                        "╚══[ Jangan Typo ]" + "\n" + "\n\n" + \
                        "Contoh : " + key + "say-id Magic"
    return helpTextToSpeech

def helptranslate():
    if settings['setKey'] == True:
        key = settings['keyCommand']
    else:
        key = ''
    helpTranslate = "╔══[ Help Translate ]" + "\n" + \
                    "╠ " + key + "af : afrikaans" + "\n" + \
                    "╠ " + key + "sq : albanian" + "\n" + \
                    "╠ " + key + "am : amharic" + "\n" + \
                    "╠ " + key + "ar : arabic" + "\n" + \
                    "╠ " + key + "hy : armenian" + "\n" + \
                    "╠ " + key + "az : azerbaijani" + "\n" + \
                    "╠ " + key + "eu : basque" + "\n" + \
                    "╠ " + key + "be : belarusian" + "\n" + \
                    "╠ " + key + "bn : bengali" + "\n" + \
                    "╠ " + key + "bs : bosnian" + "\n" + \
                    "╠ " + key + "bg : bulgarian" + "\n" + \
                    "╠ " + key + "ca : catalan" + "\n" + \
                    "╠ " + key + "ceb : cebuano" + "\n" + \
                    "╠ " + key + "ny : chichewa" + "\n" + \
                    "╠ " + key + "zhcn : chinese (simplified)" + "\n" + \
                    "╠ " + key + "zhtw : chinese (traditional)" + "\n" + \
                    "╠ " + key + "co : corsican" + "\n" + \
                    "╠ " + key + "hr : croatian" + "\n" + \
                    "╠ " + key + "cs : czech" + "\n" + \
                    "╠ " + key + "da : danish" + "\n" + \
                    "╠ " + key + "nl : dutch" + "\n" + \
                    "╠ " + key + "en : english" + "\n" + \
                    "╠ " + key + "eo : esperanto" + "\n" + \
                    "╠ " + key + "et : estonian" + "\n" + \
                    "╠ " + key + "tl : filipino" + "\n" + \
                    "╠ " + key + "fi : finnish" + "\n" + \
                    "╠ " + key + "fr : french" + "\n" + \
                    "╠ " + key + "fy : frisian" + "\n" + \
                    "╠ " + key + "gl : galician" + "\n" + \
                    "╠ " + key + "ka : georgian" + "\n" + \
                    "╠ " + key + "de : german" + "\n" + \
                    "╠ " + key + "el : greek" + "\n" + \
                    "╠ " + key + "gu : gujarati" + "\n" + \
                    "╠ " + key + "ht : haitian creole" + "\n" + \
                    "╠ " + key + "ha : hausa" + "\n" + \
                    "╠ " + key + "haw : hawaiian" + "\n" + \
                    "╠ " + key + "iw : hebrew" + "\n" + \
                    "╠ " + key + "hi : hindi" + "\n" + \
                    "╠ " + key + "hmn : hmong" + "\n" + \
                    "╠ " + key + "hu : hungarian" + "\n" + \
                    "╠ " + key + "is : icelandic" + "\n" + \
                    "╠ " + key + "ig : igbo" + "\n" + \
                    "╠ " + key + "id : indonesian" + "\n" + \
                    "╠ " + key + "ga : irish" + "\n" + \
                    "╠ " + key + "it : italian" + "\n" + \
                    "╠ " + key + "ja : japanese" + "\n" + \
                    "╠ " + key + "jw : javanese" + "\n" + \
                    "╠ " + key + "kn : kannada" + "\n" + \
                    "╠ " + key + "kk : kazakh" + "\n" + \
                    "╠ " + key + "km : khmer" + "\n" + \
                    "╠ " + key + "ko : korean" + "\n" + \
                    "╠ " + key + "ku : kurdish (kurmanji)" + "\n" + \
                    "╠ " + key + "ky : kyrgyz" + "\n" + \
                    "╠ " + key + "lo : lao" + "\n" + \
                    "╠ " + key + "la : latin" + "\n" + \
                    "╠ " + key + "lv : latvian" + "\n" + \
                    "╠ " + key + "lt : lithuanian" + "\n" + \
                    "╠ " + key + "lb : luxembourgish" + "\n" + \
                    "╠ " + key + "mk : macedonian" + "\n" + \
                    "╠ " + key + "mg : malagasy" + "\n" + \
                    "╠ " + key + "ms : malay" + "\n" + \
                    "╠ " + key + "ml : malayalam" + "\n" + \
                    "╠ " + key + "mt : maltese" + "\n" + \
                    "╠ " + key + "mi : maori" + "\n" + \
                    "╠ " + key + "mr : marathi" + "\n" + \
                    "╠ " + key + "mn : mongolian" + "\n" + \
                    "╠ " + key + "my : myanmar (burmese)" + "\n" + \
                    "╠ " + key + "ne : nepali" + "\n" + \
                    "╠ " + key + "no : norwegian" + "\n" + \
                    "╠ " + key + "ps : pashto" + "\n" + \
                    "╠ " + key + "fa : persian" + "\n" + \
                    "╠ " + key + "pl : polish" + "\n" + \
                    "╠ " + key + "pt : portuguese" + "\n" + \
                    "╠ " + key + "pa : punjabi" + "\n" + \
                    "╠ " + key + "ro : romanian" + "\n" + \
                    "╠ " + key + "ru : russian" + "\n" + \
                    "╠ " + key + "sm : samoan" + "\n" + \
                    "╠ " + key + "gd : scots gaelic" + "\n" + \
                    "╠ " + key + "sr : serbian" + "\n" + \
                    "╠ " + key + "st : sesotho" + "\n" + \
                    "╠ " + key + "sn : shona" + "\n" + \
                    "╠ " + key + "sd : sindhi" + "\n" + \
                    "╠ " + key + "si : sinhala" + "\n" + \
                    "╠ " + key + "sk : slovak" + "\n" + \
                    "╠ " + key + "sl : slovenian" + "\n" + \
                    "╠ " + key + "so : somali" + "\n" + \
                    "╠ " + key + "es : spanish" + "\n" + \
                    "╠ " + key + "su : sundanese" + "\n" + \
                    "╠ " + key + "sw : swahili" + "\n" + \
                    "╠ " + key + "sv : swedish" + "\n" + \
                    "╠ " + key + "tg : tajik" + "\n" + \
                    "╠ " + key + "ta : tamil" + "\n" + \
                    "╠ " + key + "te : telugu" + "\n" + \
                    "╠ " + key + "th : thai" + "\n" + \
                    "╠ " + key + "tr : turkish" + "\n" + \
                    "╠ " + key + "uk : ukrainian" + "\n" + \
                    "╠ " + key + "ur : urdu" + "\n" + \
                    "╠ " + key + "uz : uzbek" + "\n" + \
                    "╠ " + key + "vi : vietnamese" + "\n" + \
                    "╠ " + key + "cy : welsh" + "\n" + \
                    "╠ " + key + "xh : xhosa" + "\n" + \
                    "╠ " + key + "yi : yiddish" + "\n" + \
                    "╠ " + key + "yo : yoruba" + "\n" + \
                    "╠ " + key + "zu : zulu" + "\n" + \
                    "╠ " + key + "fil : Filipino" + "\n" + \
                    "╠ " + key + "he : Hebrew" + "\n" + \
                    "╚══[ Jangan Typo ]" + "\n" + "\n\n" + \
                    "Contoh : " + key + "tr-id Imagination"
    return helpTranslate

def clientBot(op):
    try:
        if op.type == 0:
            print ("[ 0 ] END OF OPERATION")
            return

        if op.type == 5:
            print ("[ 5 ] NOTIFIED ADD CONTACT")
            if settings["autoAdd"] == True:
                client.findAndAddContactsByMid(op.param1)
            sendMention(op.param1, "Haii @!, Makasih ya udah add :3", [op.param1])
            client.sendSticker(op.param1, '1149071','6076185')

        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE INTO GROUP")
            if clientMid in op.param3:
                if settings["autoJoin"] == True:
                    client.acceptGroupInvitation(op.param1)
                sendMention(op.param1, "Halo @!, Makasih udah invite ke grup :3", [op.param1])
                client.sendSticker(op.param1, '1856523','26613706')

        if op.type == 15 and set["leaveMessage"] == True:
                client.sendContact(op.param1)
                sendMention(op.param1, "Goodbye @!, See you next time ea ", [op.param2])
                client.sendSticker(op.param1,'1856523','26613711')

        if op.type == 17:
            print ("[ 17 ] NOTIFIED ACCEPT GROUP INVITATION")
            group = client.getGroup(op.param1)
            contact = client.getContact(op.param2)
            if settings["Welcome"] == True:
                sendMention(op.param1, op.param2, "「 Auto Tag 」\n•", "\n{}".format(str(settings["wcMsg"])))
            arg = " Group Name : {}".format(str(group.name))
            arg += "\n User Join : {}".format(str(contact.displayName))
            print (arg)

        if op.type in [22, 24]:
            print ("[ 22 And 24 ] NOTIFIED INVITE INTO ROOM & NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
                sendMention(op.param1, "Oi asw @!,ngapain invite gw")
                client.leaveRoom(op.param1)

        if op.type == 25:
            try:
                print ("[ 26 ] SEND MESSAGE")
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                setKey = settings["keyCommand"].title()
                if settings["setKey"] == False:
                    setKey = ''
                if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                    if msg.toType == 0:
                        if sender != client.profile.mid:
                            to = sender
                        else:
                            to = receiver
                    elif msg.toType == 1:
                        to = receiver
                    elif msg.toType == 2:
                        to = receiver
                    if msg.contentType == 0:
                        if text is None:
                            return
                        else:
                            cmd = command(text)
                            if cmd == "help":
                                name = " 「Help Message」 "
                                link = "http://line.me/ti/p/dthVjYx_R9"
                                icon = "http://dl.profile.line-cdn.net/0hYLDdOyhrBmN5HSso3Hp5NEVYCA4OMwArAShPUQkeD1FSKkdmEClNAF9KClcEL0IwTXxBV1QUD1pd"
                                text = helpMessage = helpmessage()
                                client.sendMessageWithRi(to, text, name, link, icon)
                                helpMessage = helpmessage()
                            elif cmd == "myself":
                                name = " 「 Self Command 」"
                                link = "http://line.me/ti/p/dthVjYx_R9"
                                icon = "http://dl.profile.line-cdn.net/0hYLDdOyhrBmN5HSso3Hp5NEVYCA4OMwArAShPUQkeD1FSKkdmEClNAF9KClcEL0IwTXxBV1QUD1pd"
                                text = helpMyself = helpmyself()
                                client.sendMessageWithRi(to, text, name, link, icon)
                                helpMySelf = helpmyself()
                            elif cmd == "settings":
                                name = " 「 Settings Command 」"
                                link = "http://line.me/ti/p/dthVjYx_R9"
                                icon = "http://dl.profile.line-cdn.net/0hYLDdOyhrBmN5HSso3Hp5NEVYCA4OMwArAShPUQkeD1FSKkdmEClNAF9KClcEL0IwTXxBV1QUD1pd"
                                text = helpSettings = helpsettings()
                                client.sendMessageWithRi(to, text, name, link, icon)
                                helpSettings = helpsettings()
                            elif cmd == "group":
                                name = " 「 Group Command 」"
                                link = "http://line.me/ti/p/dthVjYx_R9"
                                icon = "http://dl.profile.line-cdn.net/0hYLDdOyhrBmN5HSso3Hp5NEVYCA4OMwArAShPUQkeD1FSKkdmEClNAF9KClcEL0IwTXxBV1QUD1pd"
                                text = helpGroup = helpgroup()
                                client.sendMessageWithRi(to, text, name, link, icon)
                                helpGroup = helpgroup()
                            elif cmd == "media":
                                name = " 「 Media Command 」"
                                link = "http://line.me/ti/p/dthVjYx_R9"
                                icon = "http://dl.profile.line-cdn.net/0hYLDdOyhrBmN5HSso3Hp5NEVYCA4OMwArAShPUQkeD1FSKkdmEClNAF9KClcEL0IwTXxBV1QUD1pd"
                                text = helpMedia = helpmedia()
                                client.sendMessageWithRi(to, text, name, link, icon)
                                helpMedia = helpmedia()
                            elif cmd == "tts":
                                name = " 「 TextToSpeech 」"
                                link = "http://line.me/ti/p/dthVjYx_R9"
                                icon = "http://dl.profile.line-cdn.net/0hYLDdOyhrBmN5HSso3Hp5NEVYCA4OMwArAShPUQkeD1FSKkdmEClNAF9KClcEL0IwTXxBV1QUD1pd"
                                text = helpTextToSpeech = helptexttospeech()
                                client.sendMessage(to, str(helpTextToSpeech))
                            elif cmd == "translate":
                                name = " 「 Translate Command 」"
                                link = "http://line.me/ti/p/dthVjYx_R9"
                                icon = "http://dl.profile.line-cdn.net/0hYLDdfiDBBmN5HSskXF55NEVYCA4OMwArAShPUQkeD1FSKkdmEClNAF9KClcEL0IwTXxBV1QUD1pd"
                                text = helpTranslate = helptranslate()
                                client.sendMessage(to, str(helpTranslate))
                            elif cmd.startswith("setkey:"):
                                sep = text.split(" ")
                                key = text.replace(sep[0] + " ","")
                                if " " in key:
                                    client.sendMessage(to, "Key tidak bisa menggunakan spasi")
                                else:
                                    settings["keyCommand"] = str(key).lower()
                                    client.sendMessage(to, "Key Diubah Menjadi {}"+str(key).lower(), {'AGENT_NAME': '「 RunTime 」 >_<', 'AGENT_LINK': 'https://line.me/ti/p/IpWxNL4Lbz','AGENT_ICON': "http://dl.profile.line-cdn.net/"})
                            elif cmd == "sp":
                                start = time.time()
                                client.sendMessage(to, "Benchmarking...")
                                elapsed_time = time.time() - start
                                client.sendMessage(to, "[ Speed ]\n{} Second".format(str(elapsed_time)), {'AGENT_NAME': '「 Speed 」 >_<', 'AGENT_LINK': 'http://line.me/ti/p/dthVjYx_R9','AGENT_ICON': "http://dl.profile.line-cdn.net/0hYLDdfiDBBmN5HSskXF55NEVYCA4OMwArAShPUQkeD1FSKkdmEClNAF9KClcEL0IwTXxBV1QUD1pd"})
                            elif cmd == "runtime":
                                timeNow = time.time()
                                runtime = timeNow - botStart
                                runtime = format_timespan(runtime)
                                client.sendMessage(to, "Bot Sudah Berjalan Selama "+str(runtime), {'AGENT_NAME': '「 RunTime 」 >_<', 'AGENT_LINK': 'http://line.me/ti/p/dthVjYx_R9','AGENT ICON': "http://dl.profile.line-cdn.net/0hYLDdfiDBBmN5HSskXF55NEVYCA4OMwArAShPUQkeD1FSKkdmEClNAF9KClcEL0IwTXxBV1QUD1pd"})
                            elif cmd == "restart":
                                client.sendMessage(to, "Berhasil merestart Bot")
                                restartBot()
# Pembatas Script #
                            elif cmd == "autoadd on":
                                settings["autoAdd"] = True
                                client.sendMessage(to, "Berhasil mengaktifkan auto add")
                            elif cmd == "autoadd off":
                                settings["autoAdd"] = False
                                client.sendMessage(to, "Berhasil menonaktifkan auto add")
                            elif cmd == "autojoin on":
                                settings["autoJoin"] = True
                                client.sendMessage(to, "Berhasil mengaktifkan auto join")
                            elif cmd == "autojoin off":
                                settings["autoJoin"] = False
                                client.sendMessage(to, "Berhasil menonaktifkan auto join")
                            elif cmd == "autoleave on":
                                settings["autoLeave"] = True
                                client.sendMessage(to, "Berhasil mengaktifkan auto leave")
                            elif cmd == "autoleave off":
                                settings["autoLeave"] = False
                                client.sendMessage(to, "Berhasil menonaktifkan auto leave")
                            elif cmd == "autorespon on":
                                settings["autoRespon"] = True
                                client.sendMessage(to, "Berhasil mengaktifkan auto respon")
                            elif cmd == "autorespon off":
                                settings["autoRespon"] = False
                                client.sendMessage(to, "Berhasil menonaktifkan auto respon")
                            elif cmd == "autoread on":
                                settings["autoRead"] = True
                                client.sendMessage(to, "Berhasil mengaktifkan auto read")
                            elif cmd == "autoread off":
                                settings["autoRead"] = False
                                client.sendMessage(to, "Berhasil menonaktifkan auto read")
                            elif cmd == "autojointicket on":
                                settings["autoJoinTicket"] = True
                                client.sendMessage(to, "Berhasil mengaktifkan auto join by ticket")
                            elif cmd == "autoJoinTicket off":
                                settings["autoJoin"] = False
                                client.sendMessage(to, "Berhasil menonaktifkan auto join by ticket")
                            elif cmd == "cekcontact on":
                                settings["checkContact"] = True
                                client.sendMessage(to, "Berhasil mengaktifkan check details contact")
                            elif cmd == "cekcontact off":
                                settings["checkContact"] = False
                                client.sendMessage(to, "Berhasil menonaktifkan check details contact")
                            elif cmd == "cekpost on":
                                settings["checkPost"] = True
                                client.sendMessage(to, "Berhasil mengaktifkan check details post")
                            elif cmd == "cekpost off":
                                settings["checkPost"] = False
                                client.sendMessage(to, "Berhasil menonaktifkan check details post")
                            elif cmd == "ceksticker on":
                                settings["checkSticker"] = True
                                client.sendMessage(to, "Berhasil mengaktifkan check details sticker")
                            elif cmd == "ceksticker off":
                                settings["checkSticker"] = False
                                client.sendMessage(to, "Berhasil menonaktifkan check details sticker")
                            elif cmd == "unsendchat on":
                                settings["unsendMessage"] = True
                                client.sendMessage(to, "Berhasil mengaktifkan unsend message")
                            elif cmd == "unsendchat off":
                                settings["unsendMessage"] = False
                                client.sendMessage(to, "Berhasil menonaktifkan unsend message")
                            elif cmd == "welcome on":
                                settings["welcomeMessage"] = True
                                client.sendMessage(to, "Berhasil Mengatifkan Sambutan")
                            elif cmd == "welcome off":
                                settings["welcomeMessage"] = False
                                client.sendMessage(tp, "Berhasil Menonatifkan Sambutan")
                            elif cmd == "status":
                                try:
                                    ret_ = "╔══[ Status ]"
                                    if settings["autoAdd"] == True: ret_ += "\n╠══[ ON ] Auto Add"
                                    else: ret_ += "\n╠══[ OFF ] Auto Add"
                                    if settings["autoJoin"] == True: ret_ += "\n╠══[ ON ] Auto Join"
                                    else: ret_ += "\n╠══[ OFF ] Auto Join"
                                    if settings["autoLeave"] == True: ret_ += "\n╠══[ ON ] Auto Leave Room"
                                    else: ret_ += "\n╠══[ OFF ] Auto Leave Room"
                                    if settings["autoJoinTicket"] == True: ret_ += "\n╠══[ ON ] Auto Join Ticket"
                                    else: ret_ += "\n╠══[ OFF ] Auto Join Ticket"
                                    if settings["autoRead"] == True: ret_ += "\n╠══[ ON ] Auto Read"
                                    else: ret_ += "\n╠══[ OFF ] Auto Read"
                                    if settings["autoRespon"] == True: ret_ += "\n╠══[ ON ] Detect Mention"
                                    else: ret_ += "\n╠══[ OFF ] Detect Mention"
                                    if settings["checkContact"] == True: ret_ += "\n╠══[ ON ] Check Contact"
                                    else: ret_ += "\n╠══[ OFF ] Check Contact"
                                    if settings["checkPost"] == True: ret_ += "\n╠══[ ON ] Check Post"
                                    else: ret_ += "\n╠══[ OFF ] Check Post"
                                    if settings["checkSticker"] == True: ret_ += "\n╠══[ ON ] Check Sticker"
                                    else: ret_ += "\n╠══[ OFF ] Check Sticker"
                                    if settings["setKey"] == True: ret_ += "\n╠══[ ON ] Set Key"
                                    else: ret_ += "\n╠══[ OFF ] Set Key"
                                    if settings["unsendMessage"] == True: ret_ += "\n╠══[ ON ] Unsend Message"
                                    else: ret_ += "\n╠══[ OFF ] Unsend Message"
                                    ret_ += "\n╚══[ Status ]"
                                    client.sendMessage(to, str(ret_))
                                except Exception as e:
                                    client.sendMessage(msg.to, str(e))
# Pembatas Script #
                            elif cmd == "crash":
                                client.sendContact(to, "u1f41296217e740650e0448b96851a3e2',")
                            elif cmd.startswith("cname:"):
                                sep = text.split(" ")
                                string = text.replace(sep[0] + " ","")
                                if len(string) <= 20:
                                    profile = client.getProfile()
                                    profile.displayName = string
                                    client.updateProfile(profile)
                                    client.sendMessage(to,"Berhasil mengganti display name menjadi{}".format(str(string)))
                            elif cmd.startswith("cbio:"):
                                sep = text.split(" ")
                                string = text.replace(sep[0] + " ","")
                                if len(string) <= 500:
                                    profile = client.getProfile()
                                    profile.statusMessage = string
                                    client.updateProfile(profile)
                                    client.sendMessage(to,"Berhasil mengganti status message menjadi{}".format(str(string)))
                            elif cmd.startswith("welcomemessage: "):
                                sep = text.split(" ")
                                msg = text.replace(sep[0] + " ","")
                                settings["wcMsg"] = msg + ""
                                client.sendMessage(to, "[ Message ]\nBerhasil mengubah Welcome Message ke : 「"+msg+"」")
       #                              CLOSE                                 # 
















       #                               CLOSE                                     #
                            elif cmd == "me":
                                sendMention(to, "@!", [sender])
                                client.sendContact(to, sender)
                                sendLineMusic(to)
                            elif cmd == "mymid":
                                client.sendMessage(to, "[ MID ]\n{}".format(sender))
                            elif cmd == "myname":
                                contact = client.getContact(sender)
                                client.sendMessage(to, "[ Display Name ]\n{}".format(contact.displayName))
                            elif cmd == "mybio":
                                contact = client.getContact(sender)
                                client.sendMessage(to, "[ Status Message ]\n{}".format(contact.statusMessage))
                            elif cmd == "mypicture":
                                contact = client.getContact(sender)
                                client.sendMessage(to,"http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
                            elif cmd == "myvideoprofile":
                                contact = client.getContact(sender)
                                client.sendVideoWithURL(to,"http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
                            elif cmd == "mycover":
                                channel = client.getProfileCoverURL(sender)
                                path = str(channel)
                                client.sendImageWithURL(to, path)
                            elif cmd.startswith("copy "):
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        contact = client.getContact(ls)
                                        client.cloneContactProfile(ls)
                                        client.sendMessage(to, "Berhasil mengclone profile {}".format(contact.displayName))
                            elif cmd == "restore":
                                try:
                                    clientProfile = client.getProfile()
                                    clientProfile.displayName = str(settings["myProfile"]["displayName"])
                                    clientProfile.statusMessage = str(settings["myProfile"]["statusMessage"])
                                    clientProfile.pictureStatus = str(settings["myProfile"]["pictureStatus"])
                                    client.updateProfileAttribute(8, clientProfile.pictureStatus)
                                    client.updateProfile(clientProfile)
                                    coverId = str(settings["myProfile"]["coverId"])
                                    client.updateProfileCoverById(coverId)
                                    client.sendMessage(to, "Berhasil restore profile tunggu beberapa saat sampai profile berubah")
                                except Exception as e:
                                    client.sendMessage(to, "Gagal restore profile")
                                    logError(error)
                            elif cmd == "backup me":
                                try:
                                    profile = client.getProfile()
                                    settings["myProfile"]["displayName"] = str(profile.displayName)
                                    settings["myProfile"]["statusMessage"] = str(profile.statusMessage)
                                    settings["myProfile"]["pictureStatus"] = str(profile.pictureStatus)
                                    coverId = client.getProfileDetail()["result"]["objectId"]
                                    settings["myProfile"]["coverId"] = str(coverId)
                                    client.sendMessage(to, "Berhasil backup profile")
                                except Exception as e:
                                    client.sendMessage(to, "Gagal backup profile")
                                    logError(error)
                            elif cmd.startswith("stealmid "):
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    ret_ = "[ Mid User ]"
                                    for ls in lists:
                                        ret_ += "\n{}".format(str(ls))
                                    client.sendMessage(to, str(ret_))
                            elif cmd.startswith("stealdn "):
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        contact = client.getContact(ls)
                                        client.sendMessage(to, "[ Display Name ]\n{}".format(str(contact.displayName)))
                            elif cmd.startswith("stealbio "):
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        contact = client.getContact(ls)
                                        client.sendMessage(to, "[ Status Message ]\n{}".format(str(contact.statusMessage)))
                            elif cmd.startswith("stealpp "):
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        contact = client.getContact(ls)
                                        path = "http://dl.profile.line.naver.jp/{}".format(contact.pictureStatus)
                                        client.sendImageWithURL(to, str(path))
                            elif cmd.startswith("stealpv "):
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        contact = client.getContact(ls)
                                        path = "http://dl.profile.line.naver.jp/{}/vp".format(contact.pictureStatus)
                                        client.sendVideoWithURL(to, str(path))
                            elif cmd.startswith("stealcover "):
                                if client != None:
                                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                                        names = re.findall(r'@(\w+)', text)
                                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                        mentionees = mention['MENTIONEES']
                                        lists = []
                                        for mention in mentionees:
                                            if mention["M"] not in lists:
                                                lists.append(mention["M"])
                                        for ls in lists:
                                            channel = client.getProfileCoverURL(ls)
                                            path = str(channel)
                                            client.sendImageWithURL(to, str(path))
# Pembatas Script #
                            elif cmd == 'gcr':
                                group = client.getGroup(to)
                                GS = group.creator.mid
                                client.sendContact(to, GS)
                            elif cmd == 'gid':
                                gid = client.getGroup(to)
                                client.sendMessage(to, "[ID Group : ]\n" + gid.id)
                            elif cmd == 'gpict':
                                group = client.getGroup(to)
                                path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                                client.sendImageWithURL(to, path)
                            elif cmd == 'gname':
                                gid = client.getGroup(to)
                                client.sendMessage(to, "[Nama Group : ]\n" + gid.name)
                            elif cmd == 'url':
                                if msg.toType == 2:
                                    group = client.getGroup(to)
                                    if group.preventedJoinByTicket == False:
                                        ticket = client.reissueGroupTicket(to)
                                        client.sendMessage(to, "[ Group Ticket ]\nhttps://line.me/R/ti/g/{}".format(str(ticket)))
                                    else:
                                        client.sendMessage(to, "Grup qr tidak terbuka silahkan buka terlebih dahulu dengan perintah {}openqr".format(str(settings["keyCommand"])))
                            elif cmd == 'url on':
                                if msg.toType == 2:
                                    group = client.getGroup(to)
                                    if group.preventedJoinByTicket == False:
                                        client.sendMessage(to, "Grup qr sudah terbuka")
                                    else:
                                        group.preventedJoinByTicket = False
                                        client.updateGroup(group)
                                        client.sendMessage(to, "Berhasil membuka grup qr")
                            elif cmd == 'url off':
                                if msg.toType == 2:
                                    group = client.getGroup(to)
                                    if group.preventedJoinByTicket == True:
                                        client.sendMessage(to, "Grup qr sudah tertutup")
                                    else:
                                        group.preventedJoinByTicket = True
                                        client.updateGroup(group)
                                        client.sendMessage(to, "Berhasil menutup grup qr")
                            elif cmd == 'ginfo':
                                group = client.getGroup(to)
                                try:
                                    gCreator = group.creator.displayName
                                except:
                                    gCreator = "Tidak ditemukan"
                                if group.invitee is None:
                                    gPending = "0"
                                else:
                                    gPending = str(len(group.invitee))
                                if group.preventedJoinByTicket == True:
                                    gQr = "Tertutup"
                                    gTicket = "Tidak ada"
                                else:
                                    gQr = "Terbuka"
                                    gTicket = "https://line.me/R/ti/g/{}".format(str(client.reissueGroupTicket(group.id)))
                                path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                                ret_ = "╔══[ Group Info ]"
                                ret_ += "\n╠ Nama Group : {}".format(str(group.name))
                                ret_ += "\n╠ ID Group : {}".format(group.id)
                                ret_ += "\n╠ Pembuat : {}".format(str(gCreator))
                                ret_ += "\n╠ Jumlah Member : {}".format(str(len(group.members)))
                                ret_ += "\n╠ Jumlah Pending : {}".format(gPending)
                                ret_ += "\n╠ Group Qr : {}".format(gQr)
                                ret_ += "\n╠ Group Ticket : {}".format(gTicket)
                                ret_ += "\n╚══[ Finish ]"
                                client.sendMessage(to, str(ret_))
                                client.sendImageWithURL(to, path)
                            elif cmd == 'memlist':
                                if msg.toType == 2:
                                    group = client.getGroup(to)
                                    ret_ = "╔══[ Member List ]"
                                    no = 0 + 1
                                    for mem in group.members:
                                        ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
                                        no += 1
                                    ret_ += "\n╚══[ Total {} ]".format(str(len(group.members)))
                                    client.sendMessage(to, str(ret_))
                            elif cmd == 'glist':
                                    groups = client.groups
                                    ret_ = "╔══[ Group List ]"
                                    no = 0 + 1
                                    for gid in groups:
                                        group = client.getGroup(gid)
                                        ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                                        no += 1
                                    ret_ += "\n╚══[ Total {} Groups ]".format(str(len(groups)))
                                    client.sendMessage(to, str(ret_))
# Pembatas Script #
                            elif cmd == "errorlog":
                              with open('logError.txt', 'r') as e:
                                  error = e.read()
                              client.sendMessage(to, str(error))
                            elif cmd == "resetlog":
                              with open("logError.txt","w") as error:
                                  error.write("")
                              client.sendMessage(to, "[ Error Log ]\nBerhasil Mereset Log Error")
                            elif cmd.startswith("bc "):
                                sep = text.split(" ")
                                txt = text.replace(sep[0] + " ","")
                                yan = client.getGroupIdsJoined()
                                groups = client.groups
                                for group in yan:
                                    client.sendMessage(group, "[ BroadCast ]\n"+txt, {'AGENT_NAME': '「 Broadcasted 」 >_<', 'AGENT_LINK': "http://line.me/ti/p/dthVjYx_R9",'AGENT_ICON': "http://dl.profile.line-cdn.net/0hYLDdfiDBBmN5HSskXF55NEVYCA4OMwArAShPUQkeD1FSKkdmEClNAF9KClcEL0IwTXxBV1QUD1pd"})
                                client.sendMessage(to, "Berhasil broadcast ke {} group".format(str(len(groups))))
                            elif cmd == "cvp":
                                 pict = client.downloadFileURL("http://dl.profile.line-cdn.net/0hYLDdfiDBBmN5HSskXF55NEVYCA4OMwArAShPUQkeD1FSKkdmEClNAF9KClcEL0IwTXxBV1QUD1pd")
                                 vids = client.downloadFileURL("https://r2---sn-uigxxi0ujipnvo-hxne.googlevideo.com/videoplayback?source=youtube&signature=0DE382C98FBBEE2BF4BBE6957AA0CA6977CA729D.01483EF189213C9ABE56DF94F4A9ACB0DD55ECC9&mime=video%2Fmp4&dur=232.454&fvip=2&pl=24&id=o-AHJzmTndeCjbIE5rVnE2hE2kvWa9-M7p6oWPioG2Pk9I&sparams=dur,ei,expire,id,initcwndbps,ip,ipbits,itag,lmt,mime,mip,mm,mn,ms,mv,pl,ratebypass,requiressl,source&itag=22&requiressl=yes&key=cms1&ip=5.9.80.28&expire=1528852551&ratebypass=yes&ipbits=0&c=WEB&ei=5xsgW8fzMIv01wLPlZ_ICw&lmt=1528727162187348&title=%E3%80%8CAMV%E3%80%8DAnime%20Mix-%20Crucial%20Fracture&cms_redirect=yes&mip=116.206.30.54&mm=31&mn=sn-uigxxi0ujipnvo-hxne&ms=au&mt=1528830830&mv=m")
                                 changeVideoAndPictureProfile(pict, vids)
                                 client.sendMessage(to, "[ Succes Njink ]", {'AGENT_NAME': '「 ChangeDual Mamank 」 >_<', 'AGENT_LINK': 'https://line.me/ti/p/IpWxNL4Lbz','AGENT_ICON': "http://dl.profile.line-cdn.net/0hp3PA-YBrLxxtOAJbd81QS1F9IXEaFilUFVgzKEpqd3kSCz8fUgo3LxhvJCtICD9MBA5iekE6JCQU"})
                            elif cmd == "dinnkawai":
                                pict = client.downloadFileURL("http://dl.profile.line-cdn.net/0hYLDdOyhrBmN5HSso3Hp5NEVYCA4OMwArAShPUQkeD1FSKkdmEClNAF9KClcEL0IwTXxBV1QUD1pd")
                                vids = client.downloadFileURL("https://sv69.onlinevideoconverter.com/download?file=h7a0e4j9g6a0d3b1")
                                changeVideoAndPictureProfile(pict, vids)
                                client.sendMessage(to, "[ Succes Changedual ]", {'AGENT_NAME': '「 Changedual >_< 」', 'AGENT_LINK': 'http://line.me/ti/p/dthVjYx_R9','AGENT_ICON': "http://dl.profile.line-cdn.net/0hYLDdfiDBBmN5HSskXF55NEVYCA4OMwArAShPUQkeD1FSKkdmEClNAF9KClcEL0IwTXxBV1QUD1pd"})

                            elif cmd == "delannounce":
                                a = client.getChatRoomAnnouncements(to)
                                anu = []
                                for b in a:
                                    c = b.announcementSeq
                                    anu.append(c)
                                    client.removeChatRoomAnnouncement(to, c)
                                client.sendMessage(to, "「 Announcement 」\nSucces Removing Announce")
                            elif cmd.startswith("announce "):
                                sep = text.split(" ")
                                a = text.replace(sep[0] + " ","")
                                z = client.getGroupIdsJoined()
                                b = client.getContact(sender)
                                c = ChatRoomAnnouncementContents()
                                c.displayFields = 5
                                c.text = a
                                c.link = "line://ti/p/~dinn_din"
                                c.thumbnail = "http://dl.profile.line-cdn.net/0hYLDdfiDBBmN5HSskXF55NEVYCA4OMwArAShPUQkeD1FSKkdmEClNAF9KClcEL0IwTXxBV1QUD1pd"
                                try:
                                    client.createChatRoomAnnouncement(to, 1, c)
                                    client.sendMessage(to, "[ Announcement ]\n Succes Announce".format(str(b)))
                                except Exception as e:
                                   client.sendMessage(to, str(e))


                            elif cmd.startswith("kick "):
                                clientMID = client.profile.mid
                                targets = []
                                key = eval(msg.contentMetadata["MENTION"])
                                key["MENTIONEES"] [0] ["M"]
                                for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                                for target in targets:
                                    try:
                                        client.kickoutFromGroup(to,[target])
                                        time.sleep(1)
                                    except Exception as e:
                                        client.sendMessage(to, str(e))
                            elif cmd.startswith("ulti"):
                                clientMID = client.profile.mid
                                targets = []
                                key = eval(msg.contentMetadata["MENTION"])
                                key["MENTIONEES"] [0] ["M"]
                                for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                                for target in targets:
                                    try:
                                        client.kickoutFromGroup(to,[target])
                                        client.findAndAddContactByMid(to, [target])
                                        client.inviteIntoGroup(to, [target])
                                        client.cancelGroupInvitation(to, [target])
                                        time.sleep(1)
                                    except Exception as e:
                                        client.sendMessage(to, str(e))
                            elif text.lower() == 'about':
                                try:
                                    arr = []
                                    saya ="ub7ed2f3767bdc542fc5a324969c98f88"
                                    creator = client.getContact(saya)
                                    ret_ = "╔══[ About SelfBot ]"
                                    ret_ += "\n╠Thanks For HelloWorld"
                                    ret_ += "\n╠This SelfBot Premium"
                                    ret_ += "\n╠Creator: Dinn"
                                    ret_ += "\n╠Self Bot By Dinn"
                                    ret_ += "\n╚══[ Contact Me : http://line.me/ti/p/dthVjYx_R9 ]"
                                    client.sendMessage(to, str(ret_))
                                    sendLineMusic(to)
                                except Exception as e:
                                    client.sendMessage(msg.to, str(e))
                            elif cmd == "megu":
                                pict = client.downloadFileURL("http://dl.profile.line-cdn.net/0hp3PA1zFVLxxtOAJns49QS1F9IXEaFilUFVgzKEpqd3kSCz8fUgo3LxhvJCtICD9MBA5iekE6JCQU")
                                vids = client.downloadFileURL("")
                                changeVideoAndPictureProfile(pict, vids)
                            elif cmd.startswith("addpict "):
                                sep = text.split(" ")
                                apl = text.replace(sep[0] + " ","")
                                settings["Images"][apl.lower()] = "Alldata/%s.jpg" % apl
                                settings["Img"] = "%s" % apl
                                settings["Addimage"] = True
                                client.sendMessage(to, "[ Image ]\nType: AddPicture\nStatus: Kirim Gambarnya")

                            elif cmd.startswith("setspamcall: "):
                                sep = text.split(":")
                                strnum = text.replace(sep[0] + ":","")
                                num = int(strnum)
                                settings["limit"] = num
                                client.sendMessage(msg.to,"Total Spamcall Diubah Menjadi " +strnum)
                            elif cmd == "spamcall":
                                if msg.toType == 2:
                                    group = client.getGroup(to)
                                    members = [mem.mid for mem in group.members]
                                    jmlh = int(settings["limit"])
                                    client.sendMessage(msg.to, "Berhasil mengundang {} undangan Call Grup".format(str(settings["limit"])))
                                    if jmlh <= 1000:
                                        for x in range(jmlh):
                                            try:
                                                client.acquireGroupCallRoute(to)
                                                client.inviteIntoGroupCall(to, contactIds=members)
                                            except Exception as e:
                                                client.sendMessage(msg.to,str(e))
                                    else:
                                        client.sendMessage(msg.to,"Jumlah melebihi batas")
# SC SI RIAN~ :V
                            elif cmd == "1cak":
                                r=requests.get("http://api-1cak.herokuapp.com/random")
                                data=r.text
                                data=json.loads(data)
                                hasil = "[ 1Cak ]\n"
                                hasil += "\nId : " +str(data["id"])
                                hasil += "\nTitle : " + str(data["title"])
                                hasil += "\nLink : " + str(data["url"])
                                hasil += "\nVotes : " + str(data["votes"])
                                hasil += "\nNsfw : " + str(data["nsfw"])
                                client.sendMessage(to, str(hasil))

                            elif cmd.startswith("imagetext "):
                                sep = text.split(" ")
                                textnya = text.replace(sep[0] + " ","")
                                ogtu = "http://chart.apis.google.com/chart?chs=480x80&cht=p3&chtt=" + textnya + "&chts=FFFFFF,70&chf=bg,s,000000"
                                client.sendImageWithURL(to, ogtu)

                            elif text.lower() == 'flist':
                                contactlist = client.getAllContactIds()
                                kontak = client.getContacts(contactlist)
                                num=1
                                msgs="[List Friend]"
                                for ids in kontak:
                                    msgs+="\n[%i] %s" % (num, ids.displayName)
                                    num=(num+1)
                                woo+="\n[List Friend]\n\nTotal Friend : %i" % len(kontak)
                                client.sendMessage(to, woo)

                            elif text.lower() == 'blist':
                                contactlist = client.getBlockedContactIds()
                                kontak = client.getContacts(contactlist)
                                num=1
                                msgs="[ Block Friends ]"
                                for ids in kontak:
                                    msgs+="\n[%i] %s" % (num, ids.displayName)
                                    num=(num+1)
                                msgs+="\n[ Block Friends ]\n\nBlock Friend : %i" % len(kontak)
                                client.sendMessage(to, msgs)







                            elif cmd.startswith("annag "):
                                sep = text.split(" ")
                                a = text.replace(sep[0] + " ","")
                                group = client.groups
                                anu = client.reissueUserTicket()
                                b = ChatRoomAnnouncementContents()
                                b.displayFields = 5
                                b.text = a
                                b.link = "line.me/ti/p/~dinn_din"
                                for groups in group:
                                    anu = client.getGroup(groups)
                                    b.thumbnail = "http://dl.profile.line-cdn.net/"+str(anu.pictureStatus)
                                    client.createChatRoomAnnouncement(groups, 1, b)
                                client.sendMessage(to, "[ Announcement ]\nSudah Announce Ke Semua Group"+str(a))
                            elif cmd == "quotes":
                                try:
                                    respon = requests.get("https://talaikis.com/api/quotes/random")
                                    data = respon.text
                                    data = json.loads(data)
                                    ret_ = "[ Random Quotes ]\n"
                                    ret_ += "\nWriter : {}".format(str(data["author"]))
                                    ret_ += "\nCategory : {}".format(str(data["cat"]))
                                    ret_ += "\nQuote :\n{}".format(str(data["quote"]))
                                    client.sendMessage(to, str(ret_))
                                except Exception as e:
                                    client.sendMessage(to, str(e))

                            elif cmd.startswith("anime "):
                                try:
                                    sep = text.split(" ")
                                    anim = sep[1]
                                    r = requests.get("https://initiate.host/search/{}".format(str(anim)))
                                    data = r.text
                                    data = json.loads(data)
                                    a = data["result"][0]
                                    nama = a["name"]
                                    episode = a["episode"]
                                    tipe = a["type"]
                                    score = a["score"]
                                    url = a["url"]
                                    gambar = a["image_url"]
                                    ret_ = "[ Search Anime ]\n"
                                    ret_ += "\nTittle : {}".format(str(nama))
                                    ret_ += "\nEpisodes : {} ({} eps)".format(str(tipe), str(episode))
                                    ret_ += "\nScore :{}".format(str(score))
                                    ret_ += "\nUrl : {}".format(str(url))
                                    client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "Anime not found!")

                            elif cmd.startswith("kemiripan "):
                                rq=requests.get("https://botfamily.faith/api/kemiripan/?apikey=beta&q=")
                                data = json.loads(rq.text)
                                data["result"]["desc"]
                                data["result"]["img"]
                                hasil = "[ Kemiripan ]\n"
                                hasil += "\nName : "+str(data["result"]["desc"])
                                hasil += "\nImage : "+str(data["result"]["img"])
                                client.sendMessage(to, str(hasil))
                                client.sendMessage(to, data["result"]["img"])









                            elif cmd.startswith("murrotal"):
                                try:
                                    sep = text.split(" ")
                                    ayat = text.replace(sep[0] + " ","")
                                    path = "http://islamcdn.com/quran/media/audio/ayah/ar.alafasy/" + ayat
                                    client.sendAudioWithURL(to, path)
                                except Exception as error:
                                    client.sendMessage(to, "error\n" + str(error))
                                    logError(error)

                            elif cmd.startswith("window "):
                                dinn = requests.get("http://leert.corrykalam.gq/fwindow.php?text="+str(msg.text.replace(msg.text.split(' ')[0]+' ','')))
                                data = dinn.json()
                                client.sendImageWithURL(to, data["image"])

                            elif cmd.startswith("graffiti "):
                                ano = requests.get("http://leert.corrykalam.gq/graffiti.php?text="+str(msg.text.replace(msg.text.split(' ')[0]+' ','')))
                                data = ano.json()
                                client.sendImageWithURL(to, data["image"])

                            elif cmd.startswith("cookies "):
                                nee = requests.get("http://leert.corrykalam.gq/wcookies.php?text="+str(msg.text.replace(msg.text.split(' ')[0]+' ','')))
                                data = nee.json()
                                client.sendImageWithURL(to, data["image"])

                            elif cmd.startswith("sletters "):
                                shh = requests.get("http://leert.corrykalam.gq/sletters.php?text="+str(msg.text.replace(msg.text.split(' ')[0]+' ','')))
                                data = shh.json()
                                client.sendImageWithURL(to, data["image"])

                            elif 'sticker:' in msg.text.lower():
                                try:
                                    query = msg.text.replace("sticker:", "")
                                    query = int(query)
                                    if type(query) == int:
                                        client.sendImageWithURL(receiver, 'https://stickershop.line-scdn.net/stickershop/v1/product/'+str(query)+'/ANDROID/main.png')
                                        client.sendMessage(receiver, 'https://line.me/S/sticker/'+str(query))
                                    else:
                                        client.sendText(receiver, 'gunakan key sticker angka bukan huruf')
                                except Exception as e:
                                    client.sendMessage(receiver, str(e))

                            elif text.lower() == 'removechat':
                               client.removeAllMessages(op.param2)
                               client.sendMessage(to, "Done Remove Chat")

                            elif cmd == "mywaifu":
                                req = rq.get("https://api.moepoe.tech/waifu/?apikey=beta")
                                data = json.loads(req.text)
                                nama = data["result"]["name"]
                                gambar = data["result"]["image"]
                                alasan = data["result"]["reason"]
                                hasil = "[ Random Waifu ]\n"
                                hasil += "\nName : {} ".format(str(nama))
                                hasil += "\nImage : {} ".format(str(gambar))
                                hasil += "\nReason : {} ".format(str(alasan))
                                client.sendMessage(to, str(hasil))

                            elif cmd.startswith('ls'):
                                a = subprocess.getoutput(cmd[1])
                                client.sendMessage(to, a)

                            elif cmd.startswith("addpict "):
                                sep = text.split(" ")
                                apl = text.replace(sep[0] + " ","")
                                settings["Images"][apl.lower()] = "Alldata/%s.jpg" % apl
                                settings["Img"] = "%s" % apl
                                settings["Addimage"] = True
                                client.sendMessage(to, "[ Image ]\nType: Add Picture\nStatus: Kirim Gambarnya")



















                            elif cmd == "manga":
                                yan3 = requests.get("https://apiz.eater.host/manga/list")
                                yan2 = yan3.text
                                yan = json.loads (yan2)
                                ma= yan['result']['judul']
                                ayan3 = yan['result']['link']
                                ayan2 = requests.get (ayan3)
                                ayan = ayan2.text
                                rian = "[ Manga ]\n"
                                rian += "\nJudul : ".format(str(ma))
                                rian += "\nLink : ".format(str(ayan3))
                                client.sendMessage(to, str(rian))

                            elif cmd.startswith("streamanime"):
                                separate = msg.text.split(" ")
                                text = msg.text.replace(separate[0] + " ","")
                                aris = text.split("-")
                                search = aris[0]
                                with requests.session() as web:
                                    web.headers["User-Agent"] = random.choice(settings["userAgent"])
                                    result = web.get("https://api.moepoe.tech/anistream/newpost/?apikey=beta".format(search))
                                    njing = result.text
                                    data = json.loads(njing)
                                    if len(aris) == 1:
                                        num = 0
                                        ret_ = "╭──Result Anime"
                                        for anime in data["result"]:
                                            num += 1
                                            ret_ +="\n│ {}. {}".format(str(num), str(anime["title"]))
                                        ret_ +="\n╰──Total {} anime  ".format(str(len(data["result"])))
                                        ret_ +="\n\nUntuk Streaming, silahkan gunakan command:\nstreamanime-ãNumbã"
                                    elif len(aris) == 2:
                                        num = int(aris[1])
                                        if num <= len(data["result"]):
                                            anime = data["result"][num - 1]
                                            result = requests.get("https://api.moepoe.tech/anistream/dl/?apikey=beta&url={}".format(str(anime["url"])))
                                            data = result.text
                                            data = json.loads(data)
                                            if data["result"] != []:
                                                ret_ = "ã Title Anime ã"
                                                ret_ += "\n{}".format(str(anime["title"]))
                                                link = "{}".format(str(data["result"]["thumbnail"]))
                                                urlstream = "{}".format(str(data["result"]["url"]))
                                                client.sendImageWithURL(to, link)
                                                client.sendMessage(to, str(ret_), {'AGENT_ICON': 'http://dl.profile.line-cdn.net/0hYLDdw8JsBmN5HSsnyqZ5NEVYCA4OMwArAShPUQkeD1FSKkdmEClNAF9KClcEL0IwTXxBV1QUD1pd', 'AGENT_LINK': "{}".format(str(data["result"]["url"])), 'AGENT_NAME': "Tap Here For Stream Or Download"})

                            elif cmd.startswith("nekopoi"):
                                separate = msg.text.split(" ")
                                text = msg.text.replace(separate[0] + " ","")
                                aris = text.split("-")
                                search = aris[0]
                                with requests.session() as web:
                                    web.headers["User-Agent"] = random.choice(settings["userAgent"])
                                    result = web.get("https://api.moepoe.tech/nekopoi/newpost/?apikey=beta")
                                    data = result.text
                                    data = json.loads(data)
                                    if len(aris) == 1:
                                        num = 0
                                        ret_ = "╭──「 Result 」"
                                        for anime in data["result"]:
                                            num += 1
                                            ret_ +="\n│ {}. {}".format(str(num), str(anime["title"]))
                                        ret_ +="\n╰──「 Total {} 」".format(str(len(data["result"])))
                                        ret_ +="\n\nUntuk detail, silahkan gunakan command:\nnekopoi-「Numb」"
                                        client.sendMessage(to, str(ret_))
                                    elif len(aris) == 2:
                                        num = int(aris[1])
                                        if num <= len(data["result"]):
                                            anime = data["result"][num - 1]
                                            result = requests.get("https://api.moepoe.tech/nekopoi/dl/?apikey=beta&url={}".format(str(anime["url"])))
                                            data = result.text
                                            data = json.loads(data)
                                            if data["result"] != []:
                                                num = 0
                                                results = data["result"][0]
                                                ret_ = "「 Title 」"
                                                for results in data["result"]:
                                                    num += 1
                                                    ret_ += "\n\n{}. {}".format(str(num), str(results["host"]))
                                                    ret_ += "\n{}".format(str(results["url"]))
                                                ret_ +="\n\n「 Untuk Jomblo, Jangan Lupa Sediain Tissue 」"
                                                client.sendMessage(to, str(ret_), {'AGENT_ICON': 'https://ih0.redbubble.net/image.351322758.0680/flat,800x800,075,f.jpg', 'AGENT_LINK': "{}".format(str(anime["url"])), 'AGENT_NAME': "Klik Disini Untuk Melihat Langsung Di Browser"})

                            elif text.lower() == 'token win10':
                                req = requests.get(url = 'https://api.eater.host/WIN10')
                                a = req.text
                                b = json.loads(a)
                                tknop = codecs.open("tkn.json","r","utf-8")
                                tkn = json.load(tknop)
                                tkn['{}'.format(msg._from)] = []
                                tkn['{}'.format(msg._from)].append({
                                    'qr': b['result'][0]['linkqr'],
                                    'tkn': b['result'][0]['linktkn']
                                    })
                                qrz = b['result'][0]['linkqr']
                                client.sendMessage(msg.to, '{}'.format(qrz))
                                with open('tkn.json', 'w') as outfile:
                                    json.dump(tkn, outfile)

                            elif text.lower() == 'token done':
                                tknop= codecs.open("tkn.json","r","utf-8")
                                tkn = json.load(tknop)
                                a = tkn['{}'.format(msg._from)][0]['tkn']
                                req = requests.get(url = '{}'.format(a))
                                b = req.text
                                client.sendMessage(msg.to, '{}'.format(b))

                            elif cmd.startswith("inviteid "):
                                text = cmd.replace("inviteid ", "")
                                sep = text.split(" ")
                                idnya = text.replace(sep[0] + " ", text)
                                conn = client.findContactsByUserid(idnya)
                                client.findAndAddContactsByMid(conn.mid)
                                client.inviteIntoGroup(msg.to,[conn.mid])
                                group = client.getGroup(msg.to)
                                xname = client.getContact(conn.mid)
                                zx = ""
                                zxc = ""
                                zx2 = []
                                xpesan = '「 Invited from Id 」\nName '
                                khie = str(xname.displayName)
                                pesan = ''
                                pesan2 = pesan+"@a\n"
                                xlen = str(len(zxc)+len(xpesan))
                                xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                                zx = {'S':xlen, 'E':xlen2, 'M':xname.mid}
                                zx2.append(zx)
                                zxc += pesan2
                                text = xpesan+ zxc + "To group " + str(group.name) +""
                                client.sendMessage(receiver, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)





















#BATAS EAAA1!1!

                            elif cmd == "cpp":
                                settings["changePictureProfile"] = True
                                client.sendMessage(to, "Silahkan kirim gambarnya")
                            elif cmd == "cgp":
                                if msg.toType == 2:
                                    if to not in settings["changeGroupPicture"]:
                                        settings["changeGroupPicture"].append(to)
                                    client.sendMessage(to, "Silahkan kirim gambarnya")
                            elif cmd == 'tagall':
                                group = client.getGroup(msg.to)
                                nama = [contact.mid for contact in group.members]
                                k = len(nama)//100
                                for a in range(k+1):
                                    txt = u''
                                    s=0
                                    b=[]
                                    for i in group.members[a*100 : (a+1)*100]:
                                        b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                                        s += 7
                                        txt += u'@Zero \n'
                                    client.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                                    client.sendMessage(to, "Total {} Mention".format(str(len(nama))))

                            elif cmd == "sider on":
                                tz = pytz.timezone("Asia/Jakarta")
                                timeNow = datetime.now(tz=tz)
                                day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                                hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                                bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]: hasil = hari[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k): bln = bulan[k-1]
                                readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                                if receiver in read['readPoint']:
                                    try:
                                        del read['readPoint'][receiver]
                                        del read['readMember'][receiver]
                                        del read['readTime'][receiver]
                                    except:
                                        pass
                                    read['readPoint'][receiver] = msg_id
                                    read['readMember'][receiver] = ""
                                    read['readTime'][receiver] = readTime
                                    read['ROM'][receiver] = {}
                                    client.sendMessage(receiver,"Sider telah diaktifkan")
                                else:
                                    try:
                                        del read['readPoint'][receiver]
                                        del read['readMember'][receiver]
                                        del read['readTime'][receiver]
                                    except:
                                        pass
                                    read['readPoint'][receiver] = msg_id
                                    read['readMember'][receiver] = ""
                                    read['readTime'][receiver] = readTime
                                    read['ROM'][receiver] = {}
                                    client.sendMessage(receiver,"Set reading point : \n" + readTime)
                            elif cmd == "sider off":
                                tz = pytz.timezone("Asia/Makassar")
                                timeNow = datetime.now(tz=tz)
                                day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                                hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                                bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]: hasil = hari[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k): bln = bulan[k-1]
                                readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                                if receiver not in read['readPoint']:
                                    client.sendMessage(receiver,"Sider telah dinonaktifkan")
                                else:
                                    try:
                                        del read['readPoint'][receiver]
                                        del read['readMember'][receiver]
                                        del read['readTime'][receiver]
                                    except:
                                        pass
                                    client.sendMessage(receiver,"Delete reading point : \n" + readTime)
        
                            elif cmd == "sider reset":
                                tz = pytz.timezone("Asia/Makassar")
                                timeNow = datetime.now(tz=tz)
                                day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                                hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                                bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]: hasil = hari[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k): bln = bulan[k-1]
                                readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                                if msg.to in read["readPoint"]:
                                    try:
                                        del read["readPoint"][msg.to]
                                        del read["readMember"][msg.to]
                                        del read["readTime"][msg.to]
                                        del read["ROM"][msg.to]
                                    except:
                                        pass
                                    read['readPoint'][receiver] = msg_id
                                    read['readMember'][receiver] = ""
                                    read['readTime'][receiver] = readTime
                                    read['ROM'][receiver] = {}
                                    client.sendMessage(msg.to, "Reset reading point : \n" + readTime)
                                else:
                                    client.sendMessage(msg.to, "Sider belum diaktifkan ngapain di reset?")
                                    
                            elif cmd == "sider":
                                tz = pytz.timezone("Asia/Makassar")
                                timeNow = datetime.now(tz=tz)
                                day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                                hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                                bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]: hasil = hari[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k): bln = bulan[k-1]
                                readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                                if receiver in read['readPoint']:
                                    if read["ROM"][receiver].items() == []:
                                        client.sendMessage(receiver,"Tidak Ada Sider")
                                    else:
                                        chiya = []
                                        for rom in read["ROM"][receiver].items():
                                            chiya.append(rom[1])
                                        cmem = client.getContacts(chiya) 
                                        zx = ""
                                        zxc = ""
                                        zx2 = []
                                        xpesan = '[R E A D E R ]\n'
                                    for x in range(len(cmem)):
                                        xname = str(cmem[x].displayName)
                                        pesan = ''
                                        pesan2 = pesan+"@c\n"
                                        xlen = str(len(zxc)+len(xpesan))
                                        xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                                        zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                                        zx2.append(zx)
                                        zxc += pesan2
                                    text = xpesan+ zxc + "\n" + readTime
                                    try:
                                        client.sendMessage(receiver, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                                    except Exception as error:
                                        print (error)
                                    pass
                                else:
                                    client.sendMessage(receiver,"Sider belum diaktifkan")
                            elif cmd.startswith("mimicadd"):
                                targets = []
                                key = eval(msg.contentMetadata["MENTION"])
                                key["MENTIONEES"][0]["M"]
                                for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                                for target in targets:
                                    try:
                                        settings["mimic"]["target"][target] = True
                                        client.sendMessage(msg.to,"Target ditambahkan!")
                                        break
                                    except:
                                        client.sendMessage(msg.to,"Gagal menambahkan target")
                                        break
                            elif cmd.startswith("mimicdel"):
                                targets = []
                                key = eval(msg.contentMetadata["MENTION"])
                                key["MENTIONEES"][0]["M"]
                                for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                                for target in targets:
                                    try:
                                        del settings["mimic"]["target"][target]
                                        client.sendMessage(msg.to,"Target dihapuskan!")
                                        break
                                    except:
                                        client.sendMessage(msg.to,"Gagal menghapus target")
                                        break
                                    
                            elif cmd == "mimiclist":
                                if settings["mimic"]["target"] == {}:
                                    client.sendMessage(msg.to,"Tidak Ada Target")
                                else:
                                    mc = "╔══[ Mimic List ]"
                                    for mi_d in settings["mimic"]["target"]:
                                        mc += "\n╠ "+client.getContact(mi_d).displayName
                                    mc += "\n╚══[ Finish ]"
                                    client.sendMessage(msg.to,mc)
                                
                            elif cmd.startswith("mimic"):
                                sep = text.split(" ")
                                mic = text.replace(sep[0] + " ","")
                                if mic == "on":
                                    if settings["mimic"]["status"] == False:
                                        settings["mimic"]["status"] = True
                                        client.sendMessage(msg.to,"Reply Message on")
                                elif mic == "off":
                                    if settings["mimic"]["status"] == True:
                                        settings["mimic"]["status"] = False
                                        client.sendMessage(msg.to,"Reply Message off")
# Pembatas Script #   
                            elif cmd.startswith("cekwebsite"):
                                try:
                                    sep = text.split(" ")
                                    query = text.replace(sep[0] + " ","")
                                    r = requests.get("http://rahandiapi.herokuapp.com/sswebAPI?key=betakey&link={}".format(urllib.parse.quote(query)))
                                    data = r.text
                                    data = json.loads(data)
                                    client.sendImageWithURL(to, data["result"])
                                except Exception as error:
                                    logError(error)
                            elif cmd.startswith("cekdate"):
                                try:
                                    sep = msg.text.split(" ")
                                    tanggal = msg.text.replace(sep[0] + " ","")
                                    r = requests.get('https://script.google.com/macros/exec?service=AKfycbw7gKzP-WYV2F5mc9RaR7yE3Ve1yN91Tjs91hp_jHSE02dSv9w&nama=ervan&tanggal='+tanggal)
                                    data=r.text
                                    data=json.loads(data)
                                    ret_ = "[ D A T E ]"
                                    ret_ += "\nDate Of Birth : {}".format(str(data["data"]["lahir"]))
                                    ret_ += "\nAge : {}".format(str(data["data"]["usia"]))
                                    ret_ += "\nBirthday : {}".format(str(data["data"]["ultah"]))
                                    ret_ += "\nZodiak : {}".format(str(data["data"]["zodiak"]))
                                    client.sendMessage(to, str(ret_))
                                except Exception as error:
                                    logError(error)
                            elif cmd.startswith("cekpraytime "):
                                separate = msg.text.split(" ")
                                location = msg.text.replace(separate[0] + " ","")
                                r = requests.get("http://api.corrykalam.net/apisholat.php?lokasi={}".format(location))
                                data = r.text
                                data = json.loads(data)
                                tz = pytz.timezone("Asia/Makassar")
                                timeNow = datetime.now(tz=tz)
                                if data[1] != "Subuh : " and data[2] != "Dzuhur : " and data[3] != "Ashar : " and data[4] != "Maghrib : " and data[5] != "Isya : ":
                                    ret_ = "╔══[ Jadwal Sholat Sekitar " + data[0] + " ]"
                                    ret_ += "\n╠ Tanggal : " + datetime.strftime(timeNow,'%Y-%m-%d')
                                    ret_ += "\n╠ Jam : " + datetime.strftime(timeNow,'%H:%M:%S')
                                    ret_ += "\n╠ " + data[1]
                                    ret_ += "\n╠ " + data[2]
                                    ret_ += "\n╠ " + data[3]
                                    ret_ += "\n╠ " + data[4]
                                    ret_ += "\n╠ " + data[5]
                                    ret_ += "\n╚══[ Success ]"
                                    client.sendMessage(msg.to, str(ret_))
                            elif cmd.startswith("cekweather "):
                                try:
                                    sep = text.split(" ")
                                    location = text.replace(sep[0] + " ","")
                                    r = requests.get("http://api.corrykalam.net/apicuaca.php?kota={}".format(location))
                                    data = r.text
                                    data = json.loads(data)
                                    tz = pytz.timezone("Asia/Makassar")
                                    timeNow = datetime.now(tz=tz)
                                    if "result" not in data:
                                        ret_ = "╔══[ Weather Status ]"
                                        ret_ += "\n╠ Location : " + data[0].replace("Temperatur di kota ","")
                                        ret_ += "\n╠ Suhu : " + data[1].replace("Suhu : ","") + "°C"
                                        ret_ += "\n╠ Kelembaban : " + data[2].replace("Kelembaban : ","") + "%"
                                        ret_ += "\n╠ Tekanan udara : " + data[3].replace("Tekanan udara : ","") + "HPa"
                                        ret_ += "\n╠ Kecepatan angin : " + data[4].replace("Kecepatan angin : ","") + "m/s"
                                        ret_ += "\n╠══[ Time Status ]"
                                        ret_ += "\n╠ Tanggal : " + datetime.strftime(timeNow,'%Y-%m-%d')
                                        ret_ += "\n╠ Jam : " + datetime.strftime(timeNow,'%H:%M:%S') + " WIB"
                                        ret_ += "\n╚══[ Success ]"
                                        client.sendMessage(to, str(ret_))
                                except Exception as error:
                                    logError(error)
                            elif cmd.startswith("ceklocation "):
                                try:
                                    sep = text.split(" ")
                                    location = text.replace(sep[0] + " ","")
                                    r = requests.get("http://api.corrykalam.net/apiloc.php?lokasi={}".format(location))
                                    data = r.text
                                    data = json.loads(data)
                                    if data[0] != "" and data[1] != "" and data[2] != "":
                                        link = "https://www.google.co.id/maps/@{},{},15z".format(str(data[1]), str(data[2]))
                                        ret_ = "╔══[ Location Status ]"
                                        ret_ += "\n╠ Location : " + data[0]
                                        ret_ += "\n╠ Google Maps : " + link
                                        ret_ += "\n╚══[ Success ]"
                                        client.sendMessage(to, str(ret_))
                                except Exception as error:
                                    logError(error)
                            elif cmd.startswith("instainfo"):
                                try:
                                    sep = text.split(" ")
                                    search = text.replace(sep[0] + " ","")
                                    r = requests.get("https://www.instagram.com/{}/?__a=1".format(search))
                                    data = r.text
                                    data = json.loads(data)
                                    if data != []:
                                        ret_ = "╔══[ Profile Instagram ]"
                                        ret_ += "\n╠ Nama : {}".format(str(data["graphql"]["user"]["full_name"]))
                                        ret_ += "\n╠ Username : {}".format(str(data["graphql"]["user"]["username"]))
                                        ret_ += "\n╠ Bio : {}".format(str(data["graphql"]["user"]["biography"]))
                                        ret_ += "\n╠ Pengikut : {}".format(str(data["graphql"]["user"]["edge_followed_by"]["count"]))
                                        ret_ += "\n╠ Diikuti : {}".format(str(data["graphql"]["user"]["edge_follow"]["count"]))
                                        if data["graphql"]["user"]["is_verified"] == True:
                                            ret_ += "\n╠ Verifikasi : Sudah"
                                        else:
                                            ret_ += "\n╠ Verifikasi : Belum"
                                        if data["graphql"]["user"]["is_private"] == True:
                                            ret_ += "\n╠ Akun Pribadi : Iya"
                                        else:
                                            ret_ += "\n╠ Akun Pribadi : Tidak"
                                        ret_ += "\n╠ Total Post : {}".format(str(data["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]))
                                        ret_ += "\n╚══[ https://www.instagram.com/{} ]".format(search)
                                        path = data["graphql"]["user"]["profile_pic_url_hd"]
                                        client.sendImageWithURL(to, str(path))
                                        client.sendMessage(to, str(ret_))
                                except Exception as error:
                                    logError(error)
                            elif cmd.startswith("instapost"):
                                try:
                                    sep = text.split(" ")
                                    text = text.replace(sep[0] + " ","")   
                                    cond = text.split("|")
                                    username = cond[0]
                                    no = cond[1] 
                                    r = requests.get("http://rahandiapi.herokuapp.com/instapost/{}/{}?key=betakey".format(str(username), str(no)))
                                    data = r.text
                                    data = json.loads(data)
                                    if data["find"] == True:
                                        if data["media"]["mediatype"] == 1:
                                            client.sendImageWithURL(msg.to, str(data["media"]["url"]))
                                        if data["media"]["mediatype"] == 2:
                                            client.sendVideoWithURL(msg.to, str(data["media"]["url"]))
                                        ret_ = "╔══[ Info Post ]"
                                        ret_ += "\n╠ Jumlah Like : {}".format(str(data["media"]["like_count"]))
                                        ret_ += "\n╠ Jumlah Comment : {}".format(str(data["media"]["comment_count"]))
                                        ret_ += "\n╚══[ Caption ]\n{}".format(str(data["media"]["caption"]))
                                        client.sendMessage(to, str(ret_))
                                except Exception as error:
                                    logError(error)
                            elif cmd.startswith("instastory"):
                                try:
                                    sep = text.split(" ")
                                    text = text.replace(sep[0] + " ","")
                                    cond = text.split("|")
                                    search = str(cond[0])
                                    if len(cond) == 2:
                                        r = requests.get("http://rahandiapi.herokuapp.com/instastory/{}?key=betakey".format(search))
                                        data = r.text
                                        data = json.loads(data)
                                        if data["url"] != []:
                                            num = int(cond[1])
                                            if num <= len(data["url"]):
                                                search = data["url"][num - 1]
                                                if search["tipe"] == 1:
                                                    client.sendImageWithURL(to, str(search["link"]))
                                                if search["tipe"] == 2:
                                                    client.sendVideoWithURL(to, str(search["link"]))
                                except Exception as error:
                                    logError(error)
                                    
                            elif cmd.startswith("say-"):
                                sep = text.split("-")
                                sep = sep[1].split(" ")
                                lang = sep[0]
                                say = text.replace("say-" + lang + " ","")
                                if lang not in list_language["list_textToSpeech"]:
                                    return client.sendMessage(to, "Language not found")
                                tts = gTTS(text=say, lang=lang)
                                tts.save("hasil.mp3")
                                client.sendAudio(to,"hasil.mp3")
                                
                            elif cmd.startswith("cariimage"):
                                try:
                                    separate = msg.text.split(" ")
                                    search = msg.text.replace(separate[0] + " ","")
                                    r = requests.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(search))
                                    data = r.text
                                    data = json.loads(data)
                                    if data["result"] != []:
                                        items = data["result"]
                                        path = random.choice(items)
                                        a = items.index(path)
                                        b = len(items)
                                        client.sendImageWithURL(to, str(path))
                                except Exception as error:
                                    logError(error)
                            elif cmd.startswith("carimusic "):
                                sep = msg.text.split(" ")
                                query = msg.text.replace(sep[0] + " ","")
                                cond = query.split("|")
                                search = str(cond[0])
                                result = requests.get("http://api.ntcorp.us/joox/search?q={}".format(str(search)))
                                data = result.text
                                data = json.loads(data)
                                if len(cond) == 1:
                                    num = 0
                                    ret_ = "╔══[ Result Music ]"
                                    for music in data["result"]:
                                        num += 1
                                        ret_ += "\n╠ {}. {}".format(str(num), str(music["single"]))
                                    ret_ += "\n╚══[ Total {} Music ]".format(str(len(data["result"])))
                                    ret_ += "\n\nUntuk Melihat Details Music, silahkan gunakan command {}SearchMusic {}|「number」".format(str(setKey), str(search))
                                    client.sendMessage(to, str(ret_))
                                elif len(cond) == 2:
                                    num = int(cond[1])
                                    if num <= len(data["result"]):
                                        music = data["result"][num - 1]
                                        result = requests.get("http://api.ntcorp.us/joox/song_info?sid={}".format(str(music["sid"])))
                                        data = result.text
                                        data = json.loads(data)
                                        if data["result"] != []:
                                            ret_ = "╔══[ Music ]"
                                            ret_ += "\n╠ Title : {}".format(str(data["result"]["song"]))
                                            ret_ += "\n╠ Album : {}".format(str(data["result"]["album"]))
                                            ret_ += "\n╠ Size : {}".format(str(data["result"]["size"]))
                                            ret_ += "\n╠ Link : {}".format(str(data["result"]["mp3"][0]))
                                            ret_ += "\n╚══[ Finish ]"
                                            client.sendImageWithURL(to, str(data["result"]["img"]))
                                            client.sendMessage(to, str(ret_))
                                            client.sendAudioWithURL(to, str(data["result"]["mp3"][0]))
                            elif cmd.startswith("carilyric"):
                                sep = msg.text.split(" ")
                                query = msg.text.replace(sep[0] + " ","")
                                cond = query.split("|")
                                search = cond[0]
                                api = requests.get("http://api.secold.com/joox/cari/{}".format(str(search)))
                                data = api.text
                                data = json.loads(data)
                                if len(cond) == 1:
                                    num = 0
                                    ret_ = "╔══[ Result Lyric ]"
                                    for lyric in data["results"]:
                                        num += 1
                                        ret_ += "\n╠ {}. {}".format(str(num), str(lyric["single"]))
                                    ret_ += "\n╚══[ Total {} Music ]".format(str(len(data["results"])))
                                    ret_ += "\n\nUntuk Melihat Details Lyric, silahkan gunakan command {}SearchLyric {}|「number」".format(str(setKey), str(search))
                                    client.sendMessage(to, str(ret_))
                                elif len(cond) == 2:
                                    num = int(cond[1])
                                    if num <= len(data["results"]):
                                        lyric = data["results"][num - 1]
                                        api = requests.get("http://api.secold.com/joox/sid/{}".format(str(lyric["songid"])))
                                        data = api.text
                                        data = json.loads(data)
                                        lyrics = data["results"]["lyric"]
                                        lyric = lyrics.replace('ti:','Title - ')
                                        lyric = lyric.replace('ar:','Artist - ')
                                        lyric = lyric.replace('al:','Album - ')
                                        removeString = "[1234567890.:]"
                                        for char in removeString:
                                            lyric = lyric.replace(char,'')
                                        client.sendMessage(msg.to, str(lyric))
                            elif cmd.startswith("cariyoutube"):
                                sep = text.split(" ")
                                search = text.replace(sep[0] + " ","")
                                params = {"search_query": search}
                                r = requests.get("https://www.youtube.com/results", params = params)
                                soup = BeautifulSoup(r.content, "html5lib")
                                ret_ = "╔══[ Youtube Result ]"
                                datas = []
                                for data in soup.select(".yt-lockup-title > a[title]"):
                                    if "&lists" not in data["href"]:
                                        datas.append(data)
                                for data in datas:
                                    ret_ += "\n╠══[ {} ]".format(str(data["title"]))
                                    ret_ += "\n╠ https://www.youtube.com{}".format(str(data["href"]))
                                ret_ += "\n╚══[ Total {} ]".format(len(datas))
                                client.sendMessage(to, str(ret_))
                            elif cmd.startswith("tr-"):
                                sep = text.split("-")
                                sep = sep[1].split(" ")
                                lang = sep[0]
                                say = text.replace("tr-" + lang + " ","")
                                if lang not in list_language["list_translate"]:
                                    return client.sendMessage(to, "Language not found")
                                translator = Translator()
                                hasil = translator.translate(say, dest=lang)
                                A = hasil.text
                                client.sendMessage(to, str(A))
# Pembatas Script #

                            elif cmd.startswith ('invitegroupcall '):
                                           if msg.toType == 2:
                                              sep = text.split(" ")
                                              strnum = text.replace(sep[0] + " ","")
                                              num = int(strnum)
                                              client.sendMessage(to, "Berhasil mengundang kedalam telponan group")
                                              for var in range(0,num):
                                                  group = client.getGroup(to)
                                                  members = [mem.mid for mem in group.members]
                                                  client.acquireGroupCallRoute(to)
                                                  client.inviteIntoGroupCall(to, contactIds=members)
# Pembatas Script #
                        if text.lower() == "mykey":
                            client.sendMessage(to, "KeyCommand Saat ini adalah [ {} ]".format(str(settings["keyCommand"])))
                        elif text.lower() == "setkey on":
                            settings["setKey"] = True
                            client.sendMessage(to, "Berhasil mengaktifkan setkey")
                        elif text.lower() == "setkey off":
                            settings["setKey"] = False
                            client.sendMessage(to, "Berhasil menonaktifkan setkey")
                        elif text.lower() == "kickall":
                             for kick in [ mem.mid for mem in
                        client.getGroup(receiver)]:
                               if kick != client.profile.mid:
                                 client.kickoutFromGroup(receiver,[kick])
                        elif cmd == "my ticket":
                            client.sendMessage(to, '[ Your Ticket ]\nhttp://line.me/ti/p/{}'.format(client.getUserTicket().id))
# Pembatas Script #
                    elif msg.contentType == 1:
                        if settings["changePictureProfile"] == True:
                            path = client.downloadObjectMsg(msg_id)
                            settings["changePictureProfile"] = False
                            client.updateProfilePicture(path)
                            client.sendMessage(to, "Berhasil mengubah foto profile")
                        if msg.toType == 2:
                            if to in settings["changeGroupPicture"]:
                                path = client.downloadObjectMsg(msg_id)
                                settings["changeGroupPicture"].remove(to)
                                client.updateGroupPicture(to, path)
                                client.sendMessage(to, "Berhasil mengubah foto group")
                    elif msg.contentType == 7:
                        if settings["checkSticker"] == True:
                            stk_id = msg.contentMetadata['STKID']
                            stk_ver = msg.contentMetadata['STKVER']
                            pkg_id = msg.contentMetadata['STKPKGID']
                            ret_ = "╔══[ Sticker Info ]"
                            ret_ += "\n╠ STICKER ID : {}".format(stk_id)
                            ret_ += "\n╠ STICKER PACKAGES ID : {}".format(pkg_id)
                            ret_ += "\n╠ STICKER VERSION : {}".format(stk_ver)
                            ret_ += "\n╠ STICKER URL : line://shop/detail/{}".format(pkg_id)
                            ret_ += "\n╚══[ Finish ]"
                            client.sendMessage(to, str(ret_))
                    elif msg.contentType == 13:
                        if settings["checkContact"] == True:
                            try:
                                contact = client.getContact(msg.contentMetadata["mid"])
                                if client != None:
                                    cover = client.getProfileCoverURL(msg.contentMetadata["mid"])
                                else:
                                    cover = "Tidak dapat masuk di line channel"
                                path = "http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus))
                                try:
                                    client.sendImageWithURL(to, str(path))
                                except:
                                    pass
                                ret_ = "╔══[ Details Contact ]"
                                ret_ += "\n╠ Nama : {}".format(str(contact.displayName))
                                ret_ += "\n╠ MID : {}".format(str(msg.contentMetadata["mid"]))
                                ret_ += "\n╠ Bio : {}".format(str(contact.statusMessage))
                                ret_ += "\n╠ Gambar Profile : http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus))
                                ret_ += "\n╠ Gambar Cover : {}".format(str(cover))
                                ret_ += "\n╚══[ Finish ]"
                                client.sendMessage(to, str(ret_))
                            except:
                                client.sendMessage(to, "Kontak tidak valid")
                    elif msg.contentType == 16:
                        if settings["checkPost"] == True:
                            try:
                                ret_ = "╔══[ Details Post ]"
                                if msg.contentMetadata["serviceType"] == "GB":
                                    contact = client.getContact(sender)
                                    auth = "\n╠ Penulis : {}".format(str(contact.displayName))
                                else:
                                    auth = "\n╠ Penulis : {}".format(str(msg.contentMetadata["serviceName"]))
                                purl = "\n╠ URL : {}".format(str(msg.contentMetadata["postEndUrl"]).replace("line://","https://line.me/R/"))
                                ret_ += auth
                                ret_ += purl
                                if "mediaOid" in msg.contentMetadata:
                                    object_ = msg.contentMetadata["mediaOid"].replace("svc=myhome|sid=h|","")
                                    if msg.contentMetadata["mediaType"] == "V":
                                        if msg.contentMetadata["serviceType"] == "GB":
                                            ourl = "\n╠ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
                                            murl = "\n╠ Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(msg.contentMetadata["mediaOid"]))
                                        else:
                                            ourl = "\n╠ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
                                            murl = "\n╠ Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(object_))
                                        ret_ += murl
                                    else:
                                        if msg.contentMetadata["serviceType"] == "GB":
                                            ourl = "\n╠ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
                                        else:
                                            ourl = "\n╠ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
                                    ret_ += ourl
                                if "stickerId" in msg.contentMetadata:
                                    stck = "\n╠ Stiker : https://line.me/R/shop/detail/{}".format(str(msg.contentMetadata["packageId"]))
                                    ret_ += stck
                                if "text" in msg.contentMetadata:
                                    text = "\n╠ Tulisan : {}".format(str(msg.contentMetadata["text"]))
                                    ret_ += text
                                ret_ += "\n╚══[ Finish ]"
                                client.sendMessage(to, str(ret_))
                            except:
                                client.sendMessage(to, "Post tidak valid")
            except Exception as error:
                logError(error)
                traceback.print_tb(error.__traceback__)
                
        if op.type == 26:
            try:
                print ("[ 26 ] RECIEVE MESSAGE")
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                    if msg.toType == 0:
                        if sender != client.profile.mid:
                            to = sender
                        else:
                            to = receiver
                    elif msg.toType == 1:
                        to = receiver
                    elif msg.toType == 2:
                        to = receiver
                    if settings["autoRead"] == True:
                        client.sendChatChecked(to, msg_id)
                    if to in read["readPoint"]:
                        if sender not in read["ROM"][to]:
                            read["ROM"][to][sender] = True
                    if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
                        text = msg.text
                        if text is not None:
                            client.sendMessage(msg.to,text)
                    if settings["unsendMessage"] == True:
                        try:
                            msg = op.message
                            if msg.toType == 0:
                                client.log("[{} : {}]".format(str(msg._from), str(msg.text)))
                            else:
                                client.log("[{} : {}]".format(str(msg.to), str(msg.text)))
                                msg_dict[msg.id] = {"text": msg.text, "from": msg._from, "createdTime": msg.createdTime, "contentType": msg.contentType, "contentMetadata": msg.contentMetadata}
                        except Exception as error:
                            logError(error)
                    if msg.contentType == 1:
                       if settings["unsendMessage"] == True:
                           try:
                              path = client.downloadObjectMsg(msg_id, saveAs="client.png")
                              msg_dict[msg.id] = {"from":msg._from,"image":path,"createdTime": msg.createdTime}
                              with open("Log_data.json", "w") as fp:
                                json.dump(msg_dict, fp, sort_keys=True, indent=4)
                           except Exception as e:
                             print (e)
                     if msg.contentType == 2:
                       if settings["unsendMessage"] == True:
                           try:
                              path = client.downloadObjectMsg(msg_id, saveAs="rian.mp4")
                              msg_dict[msg.id] = {"from": msg._from,"video":path,"createdTime": msg.createdTime}
                              with open("Log_data.json", "w") as fp:
                                json.dump(msg_dict, fp, sort_keys=True, indent=4)
                            except Exception as e:
                              print (e)
                    if msg.contentType == 7:
                       if settings["unsendMessage"] == True:
                           try:
                              sticker = msg.contentMetadata["STKID"]
                              link = "http://dl.stickershop.line.naver.jp/stickershop/v1/sticker/{}/android/sticker.png".format(sticker)
                              msg_dict[msg.id] = {"from":msg._from,"sticker":link,"createdTime": msg.createdTime}
                              with open("Log_data.json", "w") as fp:
                                json.dump(msg_dict, fp, sort_keys=True, indent=4)
                           except Exception as e:
                             print (e)
                    if msg.contentType == 0:
                        if text is None:
                            return
                        if "/ti/g/" in msg.text.lower():
                            if settings["autoJoinTicket"] == True:
                                link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
                                links = link_re.findall(text)
                                n_links = []
                                for l in links:
                                    if l not in n_links:
                                        n_links.append(l)
                                for ticket_id in n_links:
                                    group = client.findGroupByTicket(ticket_id)
                                    client.acceptGroupInvitationByTicket(group.id,ticket_id)
                                    client.sendMessage(to, "Berhasil masuk ke group %s" % str(group.name))
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if clientMid in mention["M"]:
                                    if settings["autoRespon"] == True:
                                        sendMention(sender, "Oi Asw @!,jangan main tag tag", [sender])
                                    break
            except Exception as error:
                logError(error)
                traceback.print_tb(error.__traceback__)
        if op.type == 65:
            print ("[ 65 ] NOTIFIED DESTROY MESSAGE")
            if settings["unsendMessage"] == True:
                try:
                    at = op.param1
                    msg_id = op.param2
                    if msg_id in msg_dict:
                        if msg_dict[msg_id]["from"]:
                            contact = client.getContact(msg_dict[msg_id]["from"])
                            if contact.displayNameOverridden != None:
                                name_ = contact.displayNameOverridden
                            else:
                              if "text" in msg_dict[msg_id]:
                                name_ = contact.displayName
                                ret_ = "「 Unsend Message >_< 」"
                                ret_ += "\n\n「 Sender 」 : {} @!".format(str(contact.displayName),str(contact.mid))
                                ret_ += "\n\n「 Waktu 」 : {}".format(str(dt_to_str(cTime_to_datetime(msg_dict[msg_id]["createdTime"]))))
                                ret_ += "\n\n「 Type 」 : Text "
                                ret_ += "\n\n「 Text 」 : {}".format(str(msg_dict[msg_id]["text"]))
                                client.sendMessage(at, str(ret_), {'AGENT_NAME': 'Unsend Message Ea','AGENT_LINK': 'http://line.me/ti/p/wP927WeNFA','AGENT_ICON': "http://dl.profile.line-cdn.net{}".format(str(contact.picturePath))})
                                client.sendSticker(at, '1482011','17822843')
                                del msg_dict[msg_id]
                              else:
                                if "sticker" in msg_dict[msg_id]:
                                  name_ = contact.displayName
                                  ret_ = "「 Unsend Message >_< 」"
                                  ret_ += "\n\n「 Sender 」 : {} ".format(str(contact.displayName))
                                  ret_ += "\n\n「 Waktu 」 : {}".format(str(dt_to_str(cTime_to_datetime(msg_dict[msg_id]["createdTime"]))))
                                  ret_ += "\n\n「 Link Sticker 」 : {} ".format(str(msg_dict[msg_id]["sticker"]))
                                  ret_ += "\n\n「 Type 」 : Sticker"
                                  client.sendMessage(at, str(ret_), {'AGENT_NAME': 'Unsend Message Ea','AGENT_LINK': 'http://line.me/ti/p/wP927WeNFA','AGENT_ICON': "http://dl.profile.line-cdn.net{}".format(str(contact.picturePath))})
                                  client.sendImageWithURL(at, msg_dict[msg_id]["sticker"])
                                  del msg_dict[msg_id]
                                else:
                                  if "image" in msg_dict[msg_id]:
                                    name_ = contact.displayName
                                    ret_ = "「 Unsend Message >_< 」"
                                    ret_ += "\n\n「 Sender 」 : {} ".format(str(contact.displayName))
                                    ret_ += "\n\n「 Waktu 」: {}".format(str(dt_to_str(cTime_to_datetime(msg_dict[msg_id]["createdTime"]))))
                                    ret_ += "\n\n「 Link Image 」 : Not Found ."
                                    ret_ += "\n\n「 Type 」 : Image"
                                    client.sendMessage(at, str(ret_), {'AGENT_NAME': 'Unsend Message Ea','AGENT_LINK': 'http://line.me/ti/p/wP927WeNFA','AGENT_ICON': "http://dl.profile.line-cdn.net{}".format(str(contact.picturePath))})
                                    client.sendImage(at, "client.png")
                                    del msg_dict[msg_id]
                                  else:
                                    if "video" in msg_dict[msg_id]:
                                      name_ = contact.displayName
                                      ret_ = "「 Unsend Message >_< 」"
                                      ret_ += "\n\n「 Sender 」 : @!"
                                      ret_ += "\n\n「 Waktu 」: {}".format(str(dt_to_str(cTime_to_datetime(msg_dict[msg_id]["createdTime"]))))
                                      ret_ += "\n\n「 Link Video 」 : Not Found ."
                                      ret_ += "\n\n「 Type 」 : Video"
                                      sendMessage(at, str(ret_), [contact.mid])
                                      client.sendVideo(at, "rian.mp4")
                                      del msg_dict[msg_id]
                        else:
                            client.sendMessage(at,"SentMessage .cancelled,But I didn't have log data.\nSorry > <")
                except Exception as error:
                    logError(error)
                    traceback.print_tb(error.__traceback__)

        if op.type == 55:
            print ("[ 55 ] NOTIFIED READ MESSAGE")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                else:
                   pass
            except Exception as error:
                logError(error)
                traceback.print_tb(error.__traceback__)
    except Exception as error:
        logError(error)
        traceback.print_tb(error.__traceback__)

while True:
    try:
        delete_log()
        ops = clientPoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                clientBot(op)
                clientPoll.setRevision(op.revision)
    except Exception as error:
        logError(error)
        
def atend():
    print("Saving")
    with open("Log_data.json","w",encoding='utf8') as f:
        json.dump(msg_dict, f, ensure_ascii=False, indent=4,separators=(',', ': '))
    print("BYE")
atexit.register(atend)

