#!/bin/python3
import argparse
from os import path, mkdir, environ
import json
from subprocess import run, PIPE
from time import time

standardHistory = [[], {"notify":True}]
standardBlacklist = [["head", "spotify"], ["body", "example"], ["head", "battery"]]

ogCommand = "notify-send-bin"

homeLocation = ".config/bokbind/"
histFile = "history.json"
blackFile = "blacklisted.json"

# dbus-monitor "interface='org.freedesktop.Notifications'" | grep --line-buffered "member=Notify\|string"


def getArguments():

    timetext = 'dont print the time'


    parent_parser = argparse.ArgumentParser(description='Handle notification history and output', epilog="example: %(prog)s --time notify & %(prog)s store 'Discord' 'Kippster has sent a new message' | Configuration files in ~/" + homeLocation)

    subparsers = parent_parser.add_subparsers(dest='mode', required=True)



    print_parser = subparsers.add_parser('print')
    print_parser.add_argument('-t', '--time', action="store_false", help=timetext)

    notify_parser = subparsers.add_parser('notify')
    notify_parser.add_argument('-t', '--time', action="store_false", help=timetext)

    store_parser = subparsers.add_parser('store')
    store_parser.add_argument('-s', '--silent', action="store_true", help='store but dont notify')
    # store_parser.add_argument('options', help='standard notify-send flags that will be sent through')
    store_parser.add_argument('title', type=str)
    store_parser.add_argument('text', type=str)
    store_parser.add_argument('-p', '--parameters', nargs='*', help="parameters (quote enclosed, without dashes) that will be passed through to notify-send")

    amount_parser = subparsers.add_parser('amount')
    amount_parser.add_argument('-i', '--icon', action="store_true", help='dont print the icon')
    amount_parser.add_argument('-n', '--number', action="store_true", help='show amount number even if 0')

    toggle_parser = subparsers.add_parser('toggle')
    toggle_parser.add_argument('-s', '--silent', action="store_false", help='toggle alerts and notify of it')

    clear_parser = subparsers.add_parser('clear')
    clear_parser.add_argument('-s', '--silent', action="store_true", help='clear but dont notify of it')

    args = parent_parser.parse_args()
    #print(args)
    mode = args.mode
    return mode, args


def getLocation():
    try:
        home = path.expanduser("~") + "/"
    except:
        print(err + "Could not find home folder")
        exit()
    confFolder = home + homeLocation
    return confFolder


def checkFileValidity(file, confFolder):
    if not path.exists(file):
        if not path.exists(confFolder):
            try:
                mkdir(confFolder)
                print("Made directory: " + confFolder)
            except:
                print("Could not create directory: " + confFolder + "\n Check permissions")
                return False
        try:
            if file[-10:] == histFile[-10:]:
                newContent = standardHistory
            elif file[-10:] == blackFile[-10:]:
                newContent = standardBlacklist
            else:
                newContent = standardHistory

            with open(file, "w") as f:
                json.dump(newContent, f)
            print("Made file: " + file)
        except:
            print("Could not create file: " + file)
            return False
    return True


def getJsonFromFile(file, atmpt=0):
    try:
        with open(file, "r") as f:
            contents = json.load(f)
    except:
        print("Could not read/understand file: " + file)
        print("File may be corrupt, attempting rescue")
        if atmpt == 1:
            print("\n[!] Will try to wipe notification history to fix error\n")
        inp = input("Continue? (Y/n)")

        if len(inp) == 0:
            pass
        elif inp[0] in ["n", "N"]:
            exit()
        if atmpt == 1:
            with open(file, "w") as f:
                f.write("")

        if file[-10:] == histFile[-10:]:
            newContent = standardHistory
        elif file[-10:] == blackFile[-10:]:
            newContent = standardBlacklist
        else:
            newContent = standardHistory

        with open(file, "a") as f:
            json.dump(newContent, f)
        contents = getJsonFromFile(file, atmpt+1)
    return contents


def fixTime(stamp):
    diff = int(time() - stamp)
    if diff > 3600:
        answer = str(int(diff/3600)) + " h"
    elif diff > 60:
        answer = str(int(diff/60)) + " m"
    else:
        answer = str(diff) + " s"
    return answer


def writeHistory(history, file):
    try:
        # print(history)
        with open(file, "w") as f:
            json.dump(history, f)
    except:
        print("Could not write to history file")
        return False
    return True


def printNotification(title, text, passParams=None):
    try:
        if not passParams:
            a = run([ogCommand, title, text], stdout=None)
        else:
            params = ""
            for i in passParams:
                params += "--" + i
                if not i == passParams[-1]:
                    params += " "
            a = run([ogCommand, title, text, params], stdout=None)
        # print(a)
        return True
    except:
        return False


def printHistory(history, timeSwitch):
    try:
        text = ""
        for i, notif in enumerate(history[0]):
            spaces = " "
            if timeSwitch:
                text += "[" + fixTime(notif["timestamp"]) + "]" + spaces
            text += notif["head"] + " - " + notif["body"]
            if not i == len(history[0])-1:
                text += "\n"
        if text == "":
            text = "Empty"
        print(text)
        return True
    except:
        return False


def notifyHistory(history, timeSwitch):
    try:
        title = "Notification history"
        body = ""
        for i, notif in enumerate(history[0]):
            spaces = " "
            if timeSwitch:
                body += "[" + fixTime(notif["timestamp"]) + "]" + spaces
            body += notif["head"] + " - " + notif["body"]
            if not i == len(history[0])-1:
                body += "\n"
        if body == "":
            body = "Empty"
        printNotification(title, body)
        return True
    except:
        return False


def amountOfNotifications(history, icons, number):
    space = " "
    num = len(history[0])
    if num == 0 and not number:
        num = ""
        space = ""
    notificationsActive = history[1]["notify"]
    if icons:
        icon = ""
    elif notificationsActive:
        icon = "" + space
    else:
        icon = "" + space
        icon = "" + space
    print(icon + str(num))
    return True


def blacklistedCheck(headtext, bodytext, confFolder):
    blacklistedFile = confFolder + blackFile
    if not checkFileValidity(blacklistedFile, confFolder):
        print("Could not check with blacklist file!")
        return False
    blacklist = getJsonFromFile(blacklistedFile)

    #list = [["head", "Spotify"], ["head", "Battery"], ["body", "gotem"]]

    head = [x.lower() for x in headtext.split()]
    body = [x.lower() for x in bodytext.split()]
    for i in blacklist:
        # print(i)
        if i[0] == "head":
            if i[1].lower() in head:
                return True
        elif i[0] == "body":
            if i[1].lower() in body:
                return True
    return False


def storeNotification(history, passParams, headtext, bodytext, silent, file, confFolder):
    if blacklistedCheck(headtext, bodytext, confFolder):
        if printNotification(headtext, bodytext, passParams):
            return True
    else:
        newNotif = {}
        newNotif["timestamp"] = int(time())
        newNotif["head"] = headtext
        newNotif["body"] = bodytext
        # print(newNotif)
        history[0].append(newNotif)

        if writeHistory(history, file):
            if not silent and history[1]["notify"]:
                printNotification(headtext, bodytext, passParams)
                pass
        else:
            return False
    return True


def toggleNotifications(history, silent, file):
    state = history[1]["notify"]
    if state:
        history[1]["notify"] = not state
        tog = "OFF"
    elif not state:
        history[1]["notify"] = not state
        tog = "ON"
    else:
        print("Something went wrong toggling notifications")
        return False
    if writeHistory(history, file):
        # print(silent, state)
        if not silent or not state:
            printNotification("Notifications", "Notification alert has been turned " + tog)
    else:
        return False
    return True


def clearNotifications(silent, alerts, file):
    history = standardHistory
    if alerts:
        history[1]["notify"] = alerts
    elif not alerts:
        history[1]["notify"] = not alerts
    if writeHistory(history, file):
        if not silent and alerts:
            printNotification("Notifications", "Notification have been cleared")
    else:
        return False
    return True


def switch(mode, history, args, file, confFolder):
    if mode.lower() == "print":
        return printHistory(history, args.time)
    elif mode.lower() == "notify":
        return notifyHistory(history, args.time)
    elif mode.lower() == "store":
        return storeNotification(history, args.parameters, args.title, args.text, args.silent, file, confFolder)
    elif mode.lower() == "amount":
        return amountOfNotifications(history, args.icon, args.number)
    elif mode.lower() == "toggle":
        return toggleNotifications(history, args.silent, file)
    elif mode.lower() == "clear":
        return clearNotifications(args.silent, history[1]["notify"], file)
    else:
        print("Invalid text for option 'mode'")
        # print("Something went wrong with 'mode'.")
        return False


def main(mode=False, args=False):
    if not mode and not args:
        mode, args = getArguments()
        # print(mode)

    confFolder = getLocation()
    file = confFolder + histFile
    if not checkFileValidity(file, confFolder):
        exit()
    history = getJsonFromFile(file)
    return switch(mode, history, args, file, confFolder)

if __name__ == "__main__":
    main()
