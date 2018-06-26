# -*- coding: utf-8 -*- #

from LineAPI.linepy import *
from LineAPI.linepy.call import Call
from LineAPI.akad.ttypes import ChatRoomAnnouncementContents
from LineAPI.akad.ttypes import ChatRoomAnnouncement
from LineAPI.akad.ttypes import Location
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, shutil, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz
import traceback
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

botStart = time.time()

kyuza = LINE('EsOH6HKDbm332BJo8Ofc.skwgztg4SuqUu1exNpTcpa./nn/FPJWQJnkDwkpSfFedJA5NXth7YYtxZqTESPj+Tw=')

contact = kyuza.getProfile()
backup = kyuza.getProfile()
backup.displayName = contact.displayName
backup.statusMessage = contact.statusMessage                        
backup.pictureStatus = contact.pictureStatus
cover = kyuza.getProfileCoverId()

msg_dict = {}
settingsOpen = codecs.open("settingskyu.json","r","utf-8")
readOpen = codecs.open("sider.json","r","utf-8")
read = json.load(readOpen)
oepoll = OEPoll(kyuza)
settings = json.load(settingsOpen)
kyuzaMID = kyuza.profile.mid

## -*- Script Start -*- ##
def mentionMembers(to, mid):
    try:
        group = kyuza.getGroup(to)
        mids = [mem.mid for mem in group.members]
        jml = len(mids)
        arrData = ""
        if mid[0] == mids[0]:
            textx = "[ Mention Members ]\n"
        else:
            textx = ""
        arr = []
        for i in mid:
            no = mids.index(i) + 1
            textx += "{}.)".format(str(no))
            mention = "@kyuza\n"
            slen = str(len(textx))
            elen = str(len(textx) + len(mention) - 1)
            arrData = {'S':slen, 'E':elen, 'M':i}
            arr.append(arrData)
            textx += mention
        if no == jml:
            textx += "\nSucces Mention {} User".format(str(no))
        kyuza.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        logError(error)
        kyuza.sendMessage(to, "[ INFO ] Error :\n" + str(error))
        
def logError(text):
    kyuza.log("[ ERROR ] {}".format(str(text)))
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
    with open("logError1.txt","a") as error:
        error.write("\n[ {} ] {}".format(str(time), text))

def helpsettings():
    if settings['setKey'] == True:
        key = settings['keyCommand']
    else:
        key = ''
    helpSettings = "╔══[ Settings Command ]" + "\n" + \
                  "╠•"+ key + "AutoJoin on/off" + "\n" + \
                  "╠•"+ key + "AutoLeave on/off" + "\n" + \
                  "╠•"+ key + "AutoRespon on/off" + "\n" + \
                  "╠•"+ key + "AutoRead on/off" + "\n" + \
                  "╠•"+ key + "Autoresponpc on/off" + "\n" + \
                  "╠•"+ key + "WelcomeMessage on/off" + "\n" + \
                  "╠•"+ key + "LeaveMessage on/off" + "\n" + \
                  "╠•"+ key + "Autorespon on/off" + "\n" + \
                  "╠•"+ key + "CheckContact on/off" + "\n" + \
                  "╠•"+ key + "CheckShare on/off" + "\n" + \
                  "╠•"+ key + "Detectunsend on/off" + "\n" + \
                  "╠•"+ key + "Sticker on/off" + "\n" + \
                  "╚══[ Kyuza Bot ]"
    return helpSettings

def mygaleri():
    if settings['setKey'] == True:
        key = settings['keyCommand']
    else:
        key = ''
    helpGaleri =  "╔══[ " + key + "  ]" + "\n" + \
                  "╠•"+ key + "Addpict 「text」" + "\n" + \
                  "╠•"+ key + "Delpict 「text」" + "\n" + \
                  "╠•"+ key + "Pictlist"+ "\n" + \
                  "╠•"+ key + "Addvid 「text」" + "\n" + \
                  "╠•"+ key + "Delvid 「text」" + "\n" + \
                  "╠•"+ key + "Vidlist"+ "\n" + \
                  "╠•"+ key + "Addaudio 「text」" + "\n" + \
                  "╠•"+ key + "Delaudio 「text」" + "\n" + \
                  "╠•"+ key + "Audiolist" + "\n" + \
                  "╚══[ Kyuza Bot ]"
    return helpGaleri

def myself():
    if settings["setKey"] == True:
        key = settings['keyCommand']
    else:
        key = ''
    selfMessage =  "╔══[ Myself Command ]" + "\n" + \
                  "╠ "+ key +"Me" + "\n" + \
                  "╠ "+ key +"ChangeName:「text」" + "\n" + \
                  "╠ "+ key +"ChangeBio:「text」" + "\n" + \
                  "╠ "+ key +"Gbroadcast 「text」" + "\n" + \
                  "╠ "+ key +"Fbroadcast 「text」" + "\n" + \
                  "╠ "+ key +"Allbroadcast 「text」" + "\n" + \
                  "╠ "+ key +"MyProfile" + "\n" + \
                  "╠ "+ key +"MyMid" + "\n" + \
                  "╠ "+ key +"MyName" + "\n" + \
                  "╠ "+ key +"MyBio" + "\n" + \
                  "╠ "+ key +"MyPicture" + "\n" + \
                  "╠ "+ key +"MyVideo" + "\n" + \
                  "╠ "+ key +"MyCover" + "\n" + \
                  "╠ "+ key +"GetPofile" + "\n" + \
                  "╠ "+ key +"GetPofile 「mention」" + "\n" + \
                  "╠ "+ key +"GetMid" + "\n" + \
                  "╠ "+ key +"GetMid 「mention」" + "\n" + \
                  "╠ "+ key +"GetName" + "\n" + \
                  "╠ "+ key +"GetName 「mention」" + "\n" + \
                  "╠ "+ key +"GetBio" + "\n" + \
                  "╠ "+ key +"GetBio 「mention」" + "\n" + \
                  "╠ "+ key +"GetPicture" + "\n" + \
                  "╠ "+ key +"GetPicture 「mention」" + "\n" + \
                  "╠ "+ key +"GetVideo" + "\n" + \
                  "╠ "+ key +"GetVideo 「mention」" + "\n" + \
                  "╠ "+ key +"GetCover" + "\n" + \
                  "╠ "+ key +"GetCover 「mention」" + "\n" + \
                  "╠ "+ key +"GetContact" + "\n" + \
                  "╠ "+ key +"GetContact 「mention」" + "\n" + \
                  "╠ "+ key +"MidGetContact 「mid」" + "\n" + \
                  "╠══[ Special Self Command ]" + "\n" + \
                  "╠ "+ key +"Leave" + "\n" + \
                  "╠ "+ key +"ChangeGroupPicture" + "\n" + \
                  "╠•"+ key + "Stickerlist" + "\n" + \
                  "╠•"+ key + "Addsticker 「text」" + "\n" + \
                  "╠•"+ key + "Delsticker 「text」" + "\n" + \
                  "╠•"+ key + "Spamsticker [jmlh] [name]" + "\n" + \
                  "╚══[ Kyuza Bot ]"
    return selfMessage
    
def mygroup():
    if settings["setKey"] == True:
        key = settings['keyCommand']
    else:
        key = ''
    groupMessage = "╔══[ Group Command ]" + "\n" + \
                  "╠ " + key + "GroupInfo" + "\n" + \
                  "╠ " + key + "GroupName" + "\n" + \
                  "╠ " + key + "GroupCreator" + "\n" + \
                  "╠ " + key + "GroupPicture" + "\n" + \
                  "╠ " + key + "GroupId" + "\n" + \
                  "╠ " + key + "GroupTicket" + "\n" + \
                  "╠ " + key + "OpenQr" + "\n" + \
                  "╠ " + key + "CloseQr" + "\n" + \
                  "╠══[ Special Group Command ]" + "\n" + \
                  "╠ " + key + "GetAnnounce" + "\n" + \
                  "╠ " + key + "DelAnnounce" + "\n" + \
                  "╠ " + key + "Announcecam 「text」" + "\n" + \
                  "╠ " + key + "Announcetext 「text」" + "\n" + \
                  "╠ " + key + "Announceblank 「text」" + "\n" + \
                  "╠ " + key + "Announcecam 「text」" + "\n" + \
                  "╠ " + key + "Announceallgroup 「text」" + "\n" + \
                  "╚══[ Kyuza Bot ]"
    return groupMessage
  
def myhelp():
    if settings["setKey"] == True:
        key = settings['keyCommand']
    else:
        key = ''
    helpMessage =  "╔══[ Help Message ]" + "\n" + \
                  "╠ Use ["+ key + "] for prefix\n" + \
                  "╠ "+ key + "Help" + "\n" + \
                  "╠ "+ key + "Myself" + "\n" + \
                  "╠ "+ key + "Galeri" + "\n" + \
                  "╠ "+ key + "Media" + "\n" + \
                  "╠ "+ key + "Group" + "\n" + \
                  "╠══[ Status Command ]" + "\n" + \
                  "╠ "+ key + "Speed" + "\n" + \
                  "╠ "+ key + "Status" + "\n" + \
                  "╠ "+ key + "Errorlog" + "\n" + \
                  "╠ "+ key + "Resetlog" + "\n" + \
                  "╠ "+ key + "Runtime" + "\n" + \
                  "╠══[ Key Command ]" + "\n" + \
                  "╠ "+ key + "Setkey: " + "\n" + \
                  "╠ Mykey" + "\n" + \
                  "╠ Setkey on" + "\n" + \
                  "╠ Setkey off" + "\n" + \
                  "╚══[ Kyuza Bot ]"
    return helpMessage

def sendMention(to, mid, firstmessage, lastmessage):
    try:
        arrData = ""
        text = "%s " %(str(firstmessage))
        arr = []
        mention = "@kyuza"
        slen = str(len(text))
        elen = str(len(text) + len(mention))
        arrData = {'S':slen, 'E':elen, 'M':mid}
        arr.append(arrData)
        text += mention + str(lastmessage)
        kyuza.sendMessage(to, text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        logError(error)
        kyuza.sendMessage(to, "[ INFO ] Error :\n" + str(error))

try:
    with open("Log_data.json","r",encoding="utf_8_sig") as f:
        msg_dict = json.loads(f.read())
except:
    print("Couldn't read Log data")

def backupData():
    try:
        backup = settings
        f = codecs.open('settingskyu.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('sider.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False

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

def lineBot(op):
    try:
        if op.type == 0:
            return

        if op.type == 5:
            print ("[ 5 ] NOTIFIED ADD CONTACT")
            sendMention(op.param1, op.param1, "「 Auto Tag 」\n•", "\nHalo saya adalah Detect Unsend Bot\nSilahkan Invit saya ke group anda >_<")
            arg = "   New Friend : {}".format(str(kyuza.getContact(op.param1).displayName))
            print (arg)
            
        if op.type == 11:
            print ("[ 11 ] NOTIFIED UPDATE GROUP")
            if op.param3 == "1":
                group = kyuza.getGroup(op.param1)
                contact = kyuza.getContact(op.param2)
                arg = "   Changed : Group Name"
                arg += "\n   New Group Name : {}".format(str(group.name))
                arg += "\n   Executor : {}".format(str(contact.displayName))
                print (arg)
            elif op.param3 == "4":
                group = kyuza.getGroup(op.param1)
                contact = kyuza.getContact(op.param2)
                if group.preventedJoinByTicket == False:
                    gQr = "Opened"
                else:
                    gQr = "Closed"
                arg = "   Changed : Group Qr"
                arg += "\n   Group Name : {}".format(str(group.name))
                arg += "\n   New Group Qr Status : {}".format(gQr)
                arg += "\n   Executor : {}".format(str(contact.displayName))
                print (arg)
                     
        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE INTO GROUP")
            group = kyuza.getGroup(op.param1)
            contact = kyuza.getContact(op.param2)
            if kyuzaMID in op.param3:
                kyuza.acceptGroupInvitation(op.param1)
                sendMention(op.param1, op.param2, "「 Auto Tag 」\n•", "\n{}".format(str(settings["autoJoinMsg"])))

            gInviMids = []
            for z in group.invitee:
                if z.mid in op.param3:
                    gInviMids.append(z.mid)
            listContact = ""
            if gInviMids != []:
                for j in gInviMids:
                    name_ = kyuza.getContact(j).displayName
                    listContact += "\n +) {}".format(str(name_))

            arg = " Group Name : {}".format(str(group.name))
            arg += "\n Executor : {}".format(str(contact.displayName))
            arg += "\n List User Invited : {}".format(str(listContact))
            print (arg)
            
        if op.type == 15:
            print ("[ 15 ] NOTIFIED LEAVE GROUP")
            group = kyuza.getGroup(op.param1)
            contact = kyuza.getContact(op.param2)
            if settings["Out"] == True:
            	sendMention(op.param1, op.param2, "「 Auto Tag 」\n•", "\n{}".format(str(settings["outMsg"])))
            arg = "   Group Name : {}".format(str(group.name))
            arg += "\n   User Leave : {}".format(str(contact.displayName))
            print (arg)
            
        if op.type == 17:
            print ("[ 17 ]  NOTIFIED ACCEPT GROUP INVITATION")
            group = kyuza.getGroup(op.param1)
            contact = kyuza.getContact(op.param2)
            if settings["Welcome"] == True:
            	sendMention(op.param1, op.param2, "「 Auto Tag 」\n•", "\n{}".format(str(settings["wcMsg"])))
            arg = "   Group Name : {}".format(str(group.name))
            arg += "\n   User Join : {}".format(str(contact.displayName))
            print (arg)
            
        if op.type == 19:
            print ("[ 19 ] NOTIFIED KICKOUT FROM GROUP")
            group = kyuza.getGroup(op.param1)
            contact = kyuza.getContact(op.param2)
            victim = kyuza.getContact(op.param3)
            arg = "   Group Name : {}".format(str(group.name))
            arg += "\n   Executor : {}".format(str(contact.displayName))
            arg += "\n   Victim : {}".format(str(victim.displayName))
            print (arg)

        if op.type in [22, 24]:
            print ("[ 22 ] NOTIFIED INVITE INTO ROOM [ 24 ] NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
            	sendMention(op.param1, op.param2, "「 Auto Tag 」\n•", "\nGoblok ngapain invite gw")
            	kyuza.leaveRoom(op.param1)
            
        if op.type  == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            setKey = settings["keyCommand"]
            if settings["setKey"] == False:
                setKey = ""
            if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                if msg.toType == 0:
                    if sender != kyuza.profile.mid:
                        to = sender
                    else:
                        to = receiver
                elif msg.toType == 1:
                    to = receiver
                elif msg.toType == 2:
                    to = receiver
                if msg.contentType == 0:
                    if settings["alwayRead"] == True:
                        kyuza.sendChatChecked(to, msg_id)
                    if text is None:
                        return
                    else:
                        cmd = command(text)
                        if cmd == "me":
                            sendMention(to, sender, "「 Auto Tag 」\n•", "")
                            kyuza.sendContact(to, sender)
                            
                        elif cmd == "help":
                            helpMessage = myhelp()
                            kyuza.sendMessage(to, str(helpMessage))
                        elif cmd == "galeri":
                            helpGaleri = mygaleri()
                            kyuza.sendMessage(to, str(helpGaleri))
                        elif cmd == "settings":
                            helpSettings = helpsettings()
                            kyuza.sendMessage(to, str(helpSettings))
                            
                        elif cmd.startswith("setkey: "):
                            sep = text.split(" ")
                            key = text.replace(sep[0] + " ","")
                            if " " in key:
                                kyuza.sendMessage(to, "Key tidak bisa menggunakan spasi")
                            else:
                                settings["keyCommand"] = str(key).lower()
                                kyuza.sendMessage(to, "[ Key ]\nYour new key is: 「{}」".format(str(key).lower()))
                        elif text.lower() == 'clearkey':
                            settings["keyCommand"] = ""
                            kyuza.sendMessage(to, "[ Key ]\nBerhasil menghapus key")
                        elif text.lower() == 'mykey':
                            kyuza.sendMessage(to,"[ Key ]\nYour key is : 「" + str(settings["keyCommand"]) + "」")
                        elif text.lower() == "setkey on":
                            settings["setKey"] = True
                            kyuza.sendMessage(to, "[ Key ]\nBerhasil mengaktifkan setkey")
                        elif text.lower() == "setkey off":
                            settings["setKey"] = False
                            kyuza.sendMessage(to, "「Key」\nBerhasil menon-aktifkan setkey")
                           
                        elif cmd in ["speed","sp"]:
                            start = time.time()
                            kyuza.sendMessage(to, "[ Speed ]\nTesting♪")
                            elapsed_time = time.time() - start
                            kyuza.sendMessage(to, "[ Speed ]\n{}".format(str(elapsed_time)))
                        
                        elif cmd == "runtime":
                            timeNow = time.time()
                            runtime = timeNow - botStart
                            runtime = format_timespan(runtime)
                            kyuza.sendMessage(to, "「 Runtime 」\nRunning in {}".format(str(runtime)))
# Pembatas Script Kyuuu~ #
                        elif cmd.startswith("welcomemessage: "):
                            sep = text.split(" ")
                            msg = text.replace(sep[0] + " ","")
                            settings["wcMsg"] = msg + ""
                            kyuza.sendMessage(to, "[ Message ]\nBerhasil mengubah Welcome Message ke : 「"+msg+"」")
                        elif cmd == "welcomemessage":
                            kyuza.sendMessage(to, "[ Message ]\nWelcome Message : 「{}」".format(str(settings["wcMsg"])))
                        elif cmd == "leavemessage":
                            kyuza.sendMessage(to, "[ Message ]\nLeave Message : 「{}」".format(str(settings["outMsg"])))
                        elif cmd.startswith("leavemessage: "):
                            sep = text.split(" ")
                            msg = text.replace(sep[0] + " ","")
                            settings["outMsg"] = msg + ""
                            kyuza.sendMessage(to, "[ Message ]\nBerhasil mengubah Leave Message ke : 「{}」".format(str(msg)))
                            
                        elif cmd.startswith("autojoinmessage: "):
                            sep = text.split(" ")
                            anu = text.replace(sep[0] + " ","")
                            settings["autoJoinMsg"] = anu
                            kyuza.sendMessage(to, "[ Message ]\nBerhasil mengubah Auto Join Message ke : 「{}」".format(str(settings["autoJoinMsg"])))
                        elif cmd == "autojoinmessage":
                            kyuza.sendMessage(to, "[ Message ]\nAutojoin Message : 「{}」".format(str(settings["autoJoinMsg"])))
                            
                        elif cmd.startswith("autoresponmessage: "):
                            sep = text.split(" ")
                            anu = text.replace(sep[0] + " ","")
                            settings["autoResponMsg"] = anu
                            kyuza.sendMessage(to, "[ Message ]\nBerhasil mengubah Auto Respon Message ke : 「{}」".format(str(settings["autoResponMsg"])))
                        elif cmd == "autoresponmessage":
                            kyuza.sendMessage(to, "[ Message ]\nAutorespon Message : 「{}」".format(str(settings["autoResponMsg"])))
# Pembatas Script Kyuu~ #
                        elif cmd.startswith("gbroadcast "):
                            sep = text.split(" ")
                            txt = text.replace(sep[0] + " ","")
                            kyu = kyuza.getGroup(to)
                            groups = kyuza.groups
                            for group in groups:
                                kyuza.sendMention(group, "[ Broadcast ]\n"+txt)
                            kyuza.sendMessage(to, "Berhasil broadcast ke {} group".format(str(len(groups))))
                        elif cmd.startswith("fbroadcast "):
                            sep = text.split(" ")
                            txt = text.replace(sep[0] + " ","")
                            friends = kyuza.friends
                            for friend in friends:
                                kyuza.sendMessage(friend, "[ Broadcast ]\n{}".format(str(txt)))
                            kyuza.sendMessage(to, "Berhasil broadcast ke {} teman".format(str(len(friends))))
                        elif cmd.startswith("allbroadcast "):
                            sep = text.split(" ")
                            txt = text.replace(sep[0] + " ","")
                            friends = kyuza.friends
                            groups = kyuza.groups
                            for group in groups:
                                kyuza.sendMessage(group, "[ Broadcast ]\n{}".format(str(txt)))
                            kyuza.sendMessage(to, "Berhasil broadcast ke {} group".format(str(len(groups))))
                            for friend in friends:
                                kyuza.sendMessage(friend, "[ Broadcast ]\n{}".format(str(txt)))
                            kyuza.sendMessage(to, "Berhasil broadcast ke {} teman".format(str(len(friends))))
# Pembatas Script Kyuu~ #
                        elif cmd.startswith("addpict "):
                            sep = text.split(" ")
                            apl = text.replace(sep[0] + " ","")
                            settings["Images"][apl.lower()] = "Alldata/%s.jpg" % apl
                            settings["Img"] = "%s" % apl
                            settings["Addimage"] = True
                            kyuza.sendMessage(to, "[ Image ]\nType: Add Picture\nStatus: Kirim Gambarnya")
                        elif cmd == "pictlist":
                            if settings["Images"] == {}:
                                kyuza.sendMessage(to, "[ Image ]\nType: List picture\nStatus: No Picture")
                            else:
                                ret_ = "[ Image ]\nType: List Picture\nTotal {} Picture\n".format(str(len(settings["Images"])))
                                jmlh = 1
                                for listword in settings["Images"]:
                                    ret_ += str(jmlh)+". "+listword+"\n"
                                    jmlh += 1
                                kyuza.sendMessage(to, str(ret_))
                        elif cmd.startswith("delpict "):
                            sep = text.split(" ")
                            xres = text.replace(sep[0] + " ","")
                            if xres in settings["Images"]:
                                del settings["Images"][xres.lower()]
                                path = os.remove("Alldata/%s.jpg" % str(xres))
                                kyuza.sendMessage(to, "[ Image ]\nType: Del Picture\nStatus: Berhasil menghapus gambar : %s" % xres)
                            else:
                                kyuza.sendMessage(to, "[ Image ]\nType: Del Picture\nFile [%s] Tidak ada" % xres)
                        elif msg.text.lower() in settings["Images"]:
                            kyuza.sendImage(to, settings["Images"][msg.text.lower()])
                            
                        elif cmd.startswith("addaudio "):
                            sep = text.split(" ")
                            apl = text.replace(sep[0] + " ","")
                            settings["Audios"][apl.lower()] = "Alldata/%s.m4a" % apl
                            settings["Audio"] = "%s" % apl
                            settings["Addaudio"] = True
                            kyuza.sendMessage(to, "[ Audio ]\nType: Add audio\nStatus: Kirim audionya")

                        elif cmd == "audiolist":
                            if settings["Audios"] == {}:
                                kyuza.sendMessage(to, "[ Audio ]\nType: List audio\nStatus: No Audio")
                            else:
                                ret_ = "[ Audio ]\nType: List audio\nTotal {} Voice\n".format(str(len(settings["Audios"])))
                                jmlh = 1
                                for listword in settings["Audios"]:
                                    ret_ += str(jmlh)+". "+listword+"\n"
                                    jmlh += 1
                                kyuza.sendMessage(to, str(ret_))
                        elif cmd.startswith("delvn "):
                            sep = text.split(" ")
                            xres = text.replace(sep[0] + " ","")
                            if xres in settings["Audios"]:
                                del settings["Audios"][xres.lower()]
                                path = os.remove("Alldata/%s.m4a" % str(xres))
                                kyuza.sendMessage(to, "[ Audio ]\nType: Del audio\nStatus: Berhasil menghapus audio %s" % xres)
                            else:
                                kyuza.sendMessage(to, "[ Audio ]\nType: Del audio\nFile [%s] tidak ada" % xres)
                        elif msg.text.lower() in settings["Audios"]:
                            kyuza.sendAudio(to, settings["Audios"][msg.text.lower()])           
                            
                        elif cmd.startswith("addvid "):
                            sep = text.split(" ")
                            apl = text.replace(sep[0] + " ","")
                            settings["Videos"][apl.lower()] = "Alldata/%s.mp4" % apl
                            settings["Video"] = "%s" % apl
                            settings["Addvideo"] = True
                            kyuza.sendMessage(to, "[ Video ]\nType: Add Video\nStatus: Kirim videonya")
                        elif cmd == "vidlist":
                            if settings["Videos"] == {}:
                                kyuza.sendMessage(to, "[ Video ]\nType: List video\nStatus: No video")
                            else:
                                ret_ = "[ Video ]\nType: List Video\nTotal: {} Video\n".format(str(len(settings["Videos"])))
                                jmlh = 1
                                for listword in settings["Videos"]:
                                    ret_ += str(jmlh)+". "+listword+"\n"
                                    jmlh += 1
                                kyuza.sendMessage(to, str(ret_))
                        elif cmd.startswith("delvid "):
                            sep = text.split(" ")
                            xres = text.replace(sep[0] + " ","")
                            if xres in settings["Videos"]:
                                del settings["Videos"][xres.lower()]
                                path = os.remove("Alldata/%s.mp4" % str(xres))
                                kyuza.sendMessage(to, "[ Video ]\nType: Del Video\nStatus: Berhasil menghapus video %s" % xres)
                            else:
                                kyuza.sendMessage(to, "[ Video ]\nType: Del Video\nFile [%s] tidak ada" % xres)
                        elif msg.text.lower() in settings["Videos"]:
                            kyuza.sendVideo(to, settings["Videos"][msg.text.lower()])           
# Pembatas Script Kyu~ #
                        
                        elif cmd == "detect on":
                            settings["detectUnsend"] = True
                            kyuza.sendMessage(to, "Berhasil mengaktifkan detect unsend")

                        elif cmd == "detect off":
                            settings["detectUnsend"] = False
                            kyuza.sendMessage(to, "Berhasil menon-aktifkan detect unsend")
# Pembatas Script Kyu~ #
                        elif cmd == "mymid":
                                h = kyuza.getContact(lineMID)
                                kyuza.sendMessage(to, "[ Mid ]\n" + sender)
                        elif cmd == "myprofile":
                                contact = kyuza.getContact(sender)
                                cu = kyuza.getProfileCoverURL(sender)
                                path = str(cu)
                                image = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
                                kyuza.sendImageWithURL(msg.to,image)
                                kyuza.sendImageWithURL(msg.to,path)
                                kyuza.sendMessage(to, "[ User Profile ]\nName : {}\nBiography : {}".format(str(contact.displayName), str(contact.statusMessage)))
                        elif cmd == "myname":
                                h = kyuza.getContact(sender)
                                kyuza.sendMessage(to, "[ Name ]\n{}".format(h.displayName))
                        elif cmd == "mybio":
                                h = kyuza.getContact(sender)
                                kyuza.sendMessage(to, "[ Biography ]\n" + h.statusMessage)
                        elif cmd == "mypict":
                                h = kyuza.getContact(sender)
                                kyuza.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + h.pictureStatus)
                        elif cmd == "myvid":
                                h = kyuza.getContact(sender)
                                kyuza.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + h.pictureStatus + "/vp")
                        elif cmd == "mycover":
                                h = kyuza.getContact(sender)
                                cu = kyuza.getProfileCoverURL(sender)          
                                path = str(cu)
                                kyuza.sendImageWithURL(msg.to, path)
                                    
                        elif cmd.startswith("changename: "):
                            separate = msg.text.split(" ")
                            string = msg.text.replace(separate[0] + " ","")
                            if len(string) <= 10000000000:
                                profile = kyuza.getProfile()
                                profile.displayName = string
                                kyuza.updateProfile(profile)
                                kyuza.sendMessage(to,"Succes change name to:  " + string + "")
                        elif cmd.startswith("changebio: "):
                            separate = msg.text.split(" ")
                            string = msg.text.replace(separate[0] + " ","")
                            if len(string) <= 10000000000:
                                profile = kyuza.getProfile()
                                profile.statusMessage = string
                                kyuza.updateProfile(profile)
                                kyuza.sendMessage(msg.to,"Succes change bio to: " + string)
                        
                        elif cmd.startswith("getcontact "):
                        	sep = text.split(" ")
                        	midd = text.replace(sep[0] + " ","")
                        	sendMention(to, midd, "「 Auto Tag 」\n•", "")
                        	kyuza.sendContact(to, midd)
                        	
                        elif cmd.startswith("getmid "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    contact = kyuza.getContact(ls)
                                    kyuza.sendContact(to, ls)
                                    kyuza.sendMessage(to, "「 Mid 」\n{}".format(ls))
                                    
                        elif cmd.startswith("getvideo "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    path = "http://dl.profile.line.naver.jp/" + kyuza.getContact(ls).pictureStatus + "/vp"
                                    kyuza.sendVideoWithURL(to, str(path))
                        elif cmd.startswith("getpicture "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    path = "http://dl.profile.line.naver.jp/" + kyuza.getContact(ls).pictureStatus
                                    kyuza.sendImageWithURL(to, str(path))
                        elif cmd.startswith("getcover "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    path = kyuza.getProfileCoverURL(ls)
                                    path = str(path)
                                    kyuza.sendImageWithURL(to, str(path))
                        elif cmd.startswith("getname "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    contact = kyuza.getContact(ls)
                                    kyuza.sendMessage(to, "[ Name ]\n{}".format(str(contact.displayName)))
                        elif cmd.startswith("getbio "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    contact = kyuza.getContact(ls)
                                    kyuza.sendMessage(to, "[ Biography ]\n{}".format(str(contact.statusMessage)))
                        
                        elif cmd.startswith("clonecontact "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    contact = kyuza.getContact(ls)
                                    kyuza.cloneContactProfile(ls)
                                    sendMention(to, ls, "[ Clone ]\n•", "Status: Succes")
                        elif cmd == "refresh":
                            try:
                                kyuza.updateProfileAttribute(8, backup.pictureStatus)
                                kyuza.updateProfileCoverById(cover)
                                kyuza.updateProfile(backup)
                                sendMention(to, sender, "[ Backup ]\n•", "\nStatus: Succes backup profile")
                            except Exception as e:
                                kyuza.sendMessage(to, str(e))
# Pembatas Script Kyu~ #        
                        elif cmd == "listmovie":
                            r=requests.get("https://api.themoviedb.org/3/movie/now_playing?api_key=d7bc5382814a5e307533d578d5a321f8&language=id&page=1")
                            data=r.text
                            data=json.loads(data)                                
                            if data["results"] != []:
                                no = 0
                                hasil = "[ List Movie ]\n"
                                for film in data["results"]:
                                    no += 1
                                    hasil += "\n" + str(no) + ". " + str(film["title"])
                                hasil += "\n"
                                kyuza.sendMessage(to, str(hasil))
                        elif cmd.startswith("infomovie "):
                            sep = msg.text.split(" ")
                            judul = msg.text.replace(sep[0] + " ","")
                            query = judul.split("|")
                            judul = query[0]
                            tahun = query[1]
                            r=requests.get("https://www.omdbapi.com/?t="+judul+"&y="+tahun+"&plot=full&apikey=4bdd1d70")
                            data=r.text
                            data=json.loads(data)
                            ret_ = "[ Movie ]\n"
                            ret_ += "\nInformasi : " +str(data["Title"])  + " ("+str(data["Year"])+ ")"
                            ret_ += "\n\n " + str(data["Plot"])
                            ret_ += "\nDirector : " + str(data["Director"])
                            ret_ += "\nActors : " + str(data["Actors"])
                            ret_ += "\nRelease : " + str(data["Released"])
                            ret_ += "\nGenre : " + str(data["Genre"])
                            ret_ += "\nDuring : " + str(data["Runtime"])
                            img = data["Poster"]
                            kyuza.sendMessage(to, str(ret_))
                            kyuza.sendImageWithURL(to,str(img))
                            
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
                                ret_ += "\nScore : {}".format(str(score))
                                ret_ += "\nUrl : {}".format(str(url))
                                kyuza.sendMessage(to, str(ret_))
                            except:
                                kyuza.sendMessage(to, "Anime not found!")
                            
                        elif cmd.startswith("searchmanga "):
                            sep = msg.text.split(" ")
                            query = text.replace(sep[0] + " ","")
                            r=requests.get("http://ariapi.herokuapp.com/api/anime/search?q={}".format(str(query)))
                            data=r.text
                            data=json.loads(data)                                                                                                                                                        
                            if data["result"]["manga"] != []:
                                no = 0
                                hasil = "[ Search Manga \\n"
                                for food in data["result"]["manga"]:
                                    no += 1
                                    hasil += "\n" + str(no) + ". " + "Judul: " + str(food["title"]) + "\nLink: " + str(food["link"])
                            kyuza.sendMessage(to, str(hasil))
                            
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
                            kyuza.sendMessage(to, str(hasil))
                        elif cmd == "quote":
                            try:
                                respon = requests.get("https://talaikis.com/api/quotes/random")
                                data = respon.text
                                data = json.loads(data)
                                ret_ = "[ Random Quotes ]\n"
                                ret_ += "\nWriter : {}".format(str(data["author"]))
                                ret_ += "\nCategory : {}".format(str(data["cat"]))
                                ret_ += "\nQuote :\n{}".format(str(data["quote"]))
                                kyuza.sendMessage(to, str(ret_))
                            except Exception as e:
                                kyuza.sendMessage(to, str(e))
# Pembatas Script Kyu~ #          
                        elif cmd == "delannounce":
                            a = kyuza.getChatRoomAnnouncements(to)
                            anu = []
                            for b in a:
                                c = b.announcementSeq
                                anu.append(c)
                                kyuza.removeChatRoomAnnouncement(to, c)
                            kyuza.sendMessage(to, "「 Announcement 」\nSucces del announce")
                              
                        elif cmd == '.':
                                group = kyuza.getGroup(msg.to)
                                nama = [contact.mid for contact in group.members]
                                k = len(nama)//100
                                for a in range(k+1):
                                    ret_ = "[ Mention Members ]\n\n"
                                    no = 1
                                    arr = []
                                    arrData = ""
                                    for i in group.members[a*100 : (a+1)*100]:
                                    	#mentionMembers(to, nama)
                                    	ret_ += "{}.)".format(str(no))
                                    	no += 1
                                    	mention = "@kyuza\n"
                                    	xlen = str(len(ret_))
                                    	xlen2 = str(len(ret_) + len(mention)-1)
                                    	arrData = {'S':xlen, 'E':xlen2, 'M':i.mid}
                                    	arr.append(arrData)
                                    	ret_ += mention
                                    ret_ += "\n[ Total {} Members]".format(str(no-1))
                                    kyuza.sendMessage(to, ret_, contentMetadata ={'MENTION':'{"MENTIONEES":'+json.dumps(arr)+'}'}, contentType=0)
# Pembatas Script Kyuu~ #                      	
                        elif cmd == "getannounce":
                            gett = kyuza.getChatRoomAnnouncements(to)
                            print(gett)
                            for a in gett:
                                aa = kyuza.getContact(a.creatorMid)
                                bb = a.contents
                                cc = bb.link
                                thumb = bb.thumbnail
                                textt = bb.text
                                ret_ = "「 Announce 」\n"
                                ret_ += "\nLink: {}".format(str(cc))
                                ret_ += "\nText: {}".format(str(textt))
                                ret_ += "\nThumbnail: {}".format(str(thumb))
                                ret_ += "\nMaker: {}".format(str(aa.displayName))
                                kyuza.sendMessage(to, str(ret_))

                        elif cmd.startswith("announcetext "):
                            sep = text.split(" ")
                            a = text.replace(sep[0] + " ","")
                            z = kyuza.getGroup(to)
                            anu = kyuza.getContact(sender)
                            c = ChatRoomAnnouncementContents()
                            c.displayFields = 5
                            c.text = a
                            c.link = "line://ti/p/~cen.tod"
                            c.thumbnail = "http://dl.profile.line-cdn.net/{}".format(z.pictureStatus)
                            try:
                                kyuza.createChatRoomAnnouncement(to, 1, c)
                                kyuza.sendMessage(to, "[ Announcement ]\nSucces announce text : {}".format(str(a)))
                            except Exception as e:
                               kyuza.sendMessage(to, str(e))

                        elif cmd.startswith("announcecam "):
                            sep = text.split(" ")
                            a = text.replace(sep[0] + " ","")
                            z = kyuza.getGroup(to)
                            anu = kyuza.getContact(sender)
                            c = ChatRoomAnnouncementContents()
                            c.displayFields = 5
                            c.text = a
                            c.link = "line://nv/camera"
                            c.thumbnail = "http://dl.profile.line-cdn.net/{}".format(anu.pictureStatus)
                            try:
                                kyuza.createChatRoomAnnouncement(to, 1, c)
                                kyuza.sendMessage(to, "[ Announcement ]\nSucces announce")
                            except Exception as e:
                               kyuza.sendMessage(to, str(e))
                               
                        elif cmd.startswith("announceblank "):
                        	sep = text.split(" ")
                        	txt = text.replace(sep[0] + " ","")
                        	contents = ChatRoomAnnouncementContents()
                        	contents.displayFields = 5
                        	contents.text = txt
                        	try:
                        		kyuza.createChatRoomAnnouncement(to, 1, contents)
                        		kyuza.sendMessage(to, "[ Announcement ]\nSucces announce")
                        	except Exception as e:
                        		kyuza.sendMessage(to, str(e))

                        elif cmd.startswith("announceallgroup "):
                            sep = text.split(" ")
                            a = text.replace(sep[0] + " ","")
                            group = kyuza.groups
                           # anu = kyuza.reissueUserTicket()
                            b = ChatRoomAnnouncementContents()
                            b.displayFields = 5
                            b.text = a
                            b.link = "line://ti/p/~cen.tod"
                            for groups in group:
                                anu = kyuza.getGroup(groups)
                                b.thumbnail = "http://dl.profile.line-cdn.net/{}".format(anu.pictureStatus)
                                kyuza.createChatRoomAnnouncement(groups, 1, b)
                            kyuza.sendMessage(to, "[ Announcement ]\nSucces announce {} to all group".format(str(a)))
# Pembatas Script Kyu~ #
                        elif cmd == "errorlog":
                          with open('logError1.txt', 'r') as e:
                              error = e.read()
                          kyuza.sendMessage(to, str(error))
                        elif cmd == "resetlog":
                          with open("logError1.txt","w") as error:
                            error.write("")
                          kyuza.sendMessage(to, "[ Error Log ]\nBerhasil reset errorlog data")
        if op.type  == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            setKey = settings["keyCommand"]
            if settings["setKey"] == False:
                setKey = ""
            if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                if msg.toType == 0:
                    if sender != kyuza.profile.mid:
                        to = sender
                    else:
                        to = receiver
                elif msg.toType == 1:
                    to = receiver
                elif msg.toType == 2:
                    to = receiver
                if msg.contentType == 0:
                    if settings["alwayRead"] == True:
                        kyuza.sendChatChecked(to, msg_id)
                    if text is None:
                        return
                    else:
                        cmd = command(text)
                        if cmd == "help":
                            kyuza.sendMessage(to, "Sorry I don't have, Because i just detect unsend bot >_<")
                if msg.contentType == 0:
                    if settings["detectUnsend"] == True:
                        try:
                            unsendmsg = time.time()
                            msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"waktu":unsendmsg}
                            with open("Log_data.json", "w") as fp:
                                json.dump(msg_dict, fp,  sort_keys=True, indent=4)
                        except Exception as e:
                            print (e)
                if msg.contentType == 1:
                    if settings["detectUnsend"] == True:
                        try:
                            unsendmsg1 = time.time()
                            path = kyuza.downloadObjectMsg(msg_id, saveAs="kyuza.png")
                            msg_dict[msg.id] = {"from":msg._from,"image":path,"waktu":unsendmsg1}
                            with open("Log_data.json", "w") as fp:
                                json.dump(msg_dict, fp,  sort_keys=True, indent=4)
                        except Exception as e:
                            print (e)
                if msg.contentType == 2:
                    if settings["detectUnsend"] == True:
                        try:
                            unsendmsg2 = time.time()
                            path = kyuza.downloadObjectMsg(msg_id, saveAs="kyuza.mp4")
                            msg_dict[msg.id] = {"from":msg._from,"video":path,"waktu":unsendmsg2}
                            with open("Log_data.json", "w") as fp:
                                json.dump(msg_dict, fp,  sort_keys=True, indent=4)
                        except Exception as e:
                            print (e)
                if msg.contentType == 3:
                    if settings["detectUnsend"] == True:
                        try:
                            unsendmsg3 = time.time()
                            path = kyuza.downloadObjectMsg(msg_id, saveAs="kyuza.m4a")
                            msg_dict[msg.id] = {"from":msg._from,"audio":path,"waktu":unsendmsg3}
                            with open("Log_data.json", "w") as fp:
                                json.dump(msg_dict, fp,  sort_keys=True, indent=4)
                        except Exception as e:
                            print (e)
                if msg.contentType == 7:
                    if settings["detectUnsend"] == True:
                        try:
                            unsendmsg7 = time.time()
                            sticker = msg.contentMetadata["STKID"]
                            link = "http://dl.stickershop.line.naver.jp/stickershop/v1/sticker/{}/android/sticker.png".format(sticker)
                            msg_dict[msg.id] = {"from":msg._from,"sticker":link,"waktu":unsendmsg7}
                            with open("Log_data.json", "w") as fp:
                                json.dump(msg_dict, fp,  sort_keys=True, indent=4)
                        except Exception as e:
                            print (e)
                if msg.contentType == 13:
                    if settings["detectUnsend"] == True:
                        try:
                            unsendmsg13 = time.time()
                            mid = msg.contentMetadata["mid"]
                            msg_dict[msg.id] = {"from":msg._from,"mid":mid,"waktu":unsendmsg13}
                            with open("Log_data.json", "w") as fp:
                                json.dump(msg_dict, fp,  sort_keys=True, indent=4)
                        except Exception as e:
                            print (e)

        if op.type == 65:
            if settings["detectUnsend"] == True:
                at = op.param1
                msg_id = op.param2
                if msg_id in msg_dict:
                    ah = time.time()
                    ikkeh = kyuza.getContact(msg_dict[msg_id]["from"])
                    if "text" in msg_dict[msg_id]:
                        waktumsg = ah - msg_dict[msg_id]["waktu"]
                        waktumsg = format_timespan(waktumsg)
                        rat_ = "\n[ Send At ]\n{} ago".format(waktumsg)
                        rat_ += "\n[ Text ]\n{}".format(msg_dict[msg_id]["text"])
                        sendMention(at, ikkeh.mid, "[ Unsend Message ]\n\n[ Maker ]\n•", str(rat_))
                        del msg_dict[msg_id]
                    else:
                        if "image" in msg_dict[msg_id]:
                            waktumsg = ah - msg_dict[msg_id]["waktu"]
                            waktumsg = format_timespan(waktumsg)
                            rat_ = "\n[ Send At ]\n{} ago".format(waktumsg)
                            rat_ += "\n[ Image ]\nBelow"
                            sendMention(at, ikkeh.mid, "[ Unsend Message ]\n\n[ Maker ]\n•", str(rat_))
                            kyuza.sendImage(at, "kyuza.png")
                            del msg_dict[msg_id]
                        else:
                            if "video" in msg_dict[msg_id]:
                                waktumsg = ah - msg_dict[msg_id]["waktu"]
                                waktumsg = format_timespan(waktumsg)
                                rat_ = "\n[ Send At ]\n{} ago".format(waktumsg)
                                rat_ += "\n[ Video ]\nBelow"
                                sendMention(at, ikkeh.mid, "[ Unsend Message ]\n\n[ Maker ]\n•", str(rat_))
                                kyuza.sendVideo(at, "kyuza.mp4")
                                del msg_dict[msg_id]
                            else:
                                if "audio" in msg_dict[msg_id]:
                                    waktumsg = ah - msg_dict[msg_id]["waktu"]
                                    waktumsg = format_timespan(waktumsg)
                                    rat_ = "\n[ Send At ]\n{} ago".format(waktumsg)
                                    rat_ += "\n[ Audio ]\nBelow"
                                    sendMention(at, ikkeh.mid, "[ Unsend Message ]\n\n[ Maker ]\n•", str(rat_))
                                    kyuza.sendAudio(at, "kyuza.m4a")
                                    del msg_dict[msg_id]
                                else:
                                    if "sticker" in msg_dict[msg_id]:
                                        waktumsg = ah - msg_dict[msg_id]["waktu"]
                                        waktumsg = format_timespan(waktumsg)
                                        rat_ = "\n[ Send At ]\n{} ago".format(waktumsg)
                                        rat_ += "\n[ Sticker ]\nBelow"
                                        sendMention(at, ikkeh.mid, "[ Unsend Message ]\n\n[ Maker ]\n•", str(rat_))
                                        kyuza.sendImageWithURL(at, msg_dict[msg_id]["sticker"])
                                        del msg_dict[msg_id]
                                    else:
                                        if "mid" in msg_dict[msg_id]:
                                            waktumsg = ah - msg_dict[msg_id]["waktu"]
                                            waktumsg = format_timespan(waktumsg)
                                            rat_ = "\n[ Send At ]\n{} ago".format(waktumsg)
                                            rat_ += "\n[ Contact ]\nBelow"
                                            sendMention(at, ikkeh.mid, "[ Unsend Message ]\n\n[ Maker ]\n•", str(rat_))
                                            kyuza.sendContact(at, msg_dict[msg_id]["mid"])
                                            del msg_dict[msg_id]
                else:
                    kyuza.sendMessage(at, "Unsend Message Detected\n\nMessage not in log")

    except Exception as error:
        logError(error)
        traceback.print_tb(error.__traceback__)

while True:
    try:
      ops = oepoll.singleTrace(count=50)
      if ops is not None:
          for op in ops:
            lineBot(op)
            oepoll.setRevision(op.revision)
    except Exception as error:
        logError(error)