#!/usr/bin/env python3

import sys, os, json, colorama
from colorama import Fore

def displayHelp():
    print("""
===============================""" + 
Fore.CYAN + """
SuperBackLogger v0.9 (22/12/2017)""" +
Fore.YELLOW + """
    -   by Ben Cook""" +
Fore.WHITE + """
	
A script to help you log all your gaming/movie/TV/music/reading endeavours.
	
    Usage:

        list                                    -   Lists all the backlogs in backlogs.json.

        create <backlog name> [item]            -   Create a new backlog with the given name. Supply an optional item to find the specific status of that item.
        check <backlog name>                    -   Displays the backlog and the status of each item.

        add <backlog name> <item> [status]      -   Adds a new item to a backlog. Allows an optional custom status definition, otherwise defaults to [NOT DONE]
        update <backlog name> <item> [status]   -   Updates an item to a new status. If the optional custom status isn't provided, it just increments it to the
                                                    next level, up to [DONE]. A custom status can't be incremented and a new custom one must be provided in order
                                                    to replace it.

        delete <backlog name>                   -   Deletes an entire backlog.
        remove <backlog name> <item>            -   Removes an item from the backlog.
        
        reset <backlog name>                    -   Sets all items on list to [NOT DONE].


    FOLLOWING FUNCTIONS MAY BE TEMPORARY AND INTEGRATED IN TO 'UPDATE' LATER:
        
        notdone <backlog name> <item>           -   Marks an item as [NOT DONE].
        inprogress <backlog name> <item>        -   Marks an item as [IN PROGRESS].
        done <backlog name> <item>              -   Marks an item as [DONE].


===============================
""")

def displayError():
    print("""
That's not how you use that command! Please use --help to get more information on using SuperBackLogger.
""")

argc = len(sys.argv)
backlogInfoFile = 'backlogs.json'
backlogDirectory = 'backlogs/'

statusType = {
    0 : ("[CUSTOM]", Fore.MAGENTA),
    1 : ("[NOT DONE]", Fore.RED),
    2 : ("[IN PROGRESS]", Fore.YELLOW),
    3 : ("[DONE]", Fore.GREEN)
        }

def backlogInfoFileError():
    print('\nUnable to access backlog list! Possible error in: ' + backLogInfoFile + '\n')
def backlogFileError(fileLocation):
    print('\nUnable to access: ' + fileLocation + ', file may not exist!\n')
def ensureWorking():
    if not os.path.isdir(backlogDirectory):
        os.mkdir(backlogDirectory);
    if not os.path.isfile(backlogInfoFile):
        with open(backlogInfoFile, 'w') as jsonFile:
            json.dump({}, jsonFile)

def getBacklogLocation(backlogName):
    try:
        with open(backlogInfoFile, 'r') as jsonFile:
            backlogList = json.load(jsonFile)
            if backlogName not in backlogList:
                print('\n' + Fore.CYAN + backlogName + Fore.WHITE + ' does not exist!\n')
                return False
            else:
                backlogLocation = backlogList[backlogName]
                return backlogLocation
    except:
        backlogInfoFileError()
        return False




def createBacklog(newBacklogName):
    try:
        with open(backlogInfoFile, 'r') as jsonFile:
            backlogList = json.load(jsonFile)
            if newBacklogName in backlogList:
                oResponse = input('\nA backlog with that name already exists!\nWould you like to replace it? (y/n): ')
                while oResponse.lower() not in ('yes', 'no', 'y', 'n'):
                    oResponse = input('\nInvalid response! Must be \'y\' or \'n\': ')
                if oResponse.lower() in ('yes', 'y'):
                    print('\nOkay, overwriting!')
                else:
                    print('\nBacklog has not been created.')
                    return
    except:
        backlogInfoFileError()
        return
    
    newBacklogFile = backlogDirectory + newBacklogName + '.json'

    with open(newBacklogFile, 'w') as jsonFile:
        newJsonData = {
            'name' : newBacklogName,
            'content' : {}
            }
        json.dump(newJsonData, jsonFile)
    
    try:
        with open(backlogInfoFile, 'r+') as jsonFile:
            backlogList = json.load(jsonFile);
            backlogList[newBacklogName] = newBacklogFile;
                    
            jsonFile.seek(0)
            json.dump(backlogList, jsonFile)
            jsonFile.truncate()
    except:
        backlogInfoFileError()
        return

    print('\n' + newBacklogName + ' backlog created successfully!')





def checkBacklog(backlogName):
    pickItem = False
    if argc > 3:
        pickItem = sys.argv[3]

    backlogLocation = getBacklogLocation(backlogName)
    if not backlogLocation:
        return

    try:
        with open(backlogLocation, 'r') as jsonFile:
            backlogInfo = json.load(jsonFile)
            print('\n\t' + Fore.CYAN + '____' + backlogInfo['name'] + ' Backlog____\n')

            if len(backlogInfo['content']) > 0:

                if pickItem:
                    if pickItem in backlogInfo['content']:
                        colour = Fore.MAGENTA
                        status = backlogInfo['content'][pickItem]
                        statusText = status
                        if status in statusType:
                            statusText = statusType[status][0]
                            colour = statusType[status][1]
                        print(('\t' + Fore.YELLOW + '{0:<25}' + colour + '{1:<10}').format(pickItem, statusText))
                    else:
                        print('\t' + Fore.YELLOW + pickItem + Fore.WHITE + ' is not in this backlog!')
                    return


                for name, status in backlogInfo['content'].items():
                    colour = Fore.MAGENTA
                    statusText = status;
                    if status in statusType:
                        statusText = statusType[status][0]
                        colour = statusType[status][1]

                    print(('\t' + Fore.YELLOW + '{0:<25}' + colour + '{1:<10}').format(name, statusText))
            else:
                print('\t' + Fore.WHITE + 'Backlog is empty!\n')
    except:
        backlogFileError(backlogLocation)


def addToBacklog():
    backlogName = sys.argv[2]
    newItem = sys.argv[3]
    newStatus = 1
    if argc > 4:
        newStatus = '[' + sys.argv[4] + ']'

    backlogLocation = getBacklogLocation(backlogName)
    if not backlogLocation:
        return
    
    try:
        with open(backlogLocation, 'r+') as jsonFile:
            backlogInfo = json.load(jsonFile)

            if newItem in backlogInfo['content']:
                oResponse = input('\nThat item already exists in this backlog!\nWould you like to replace it? (y/n): ')
                while oResponse.lower() not in ('yes', 'no', 'y', 'n'):
                    oResponse = input('\nInvalid response! Must be \'y\' or \'n\': ')
                if oResponse.lower() in ('yes', 'y'):
                    print('\nOkay, overwriting!')
                else:
                    print('\nItem has not been added.')
                    return

            backlogInfo['content'][newItem] = newStatus

            jsonFile.seek(0)
            json.dump(backlogInfo, jsonFile)
            jsonFile.truncate()

            print('\n' + Fore.YELLOW + newItem + Fore.WHITE + ' has been added to ' + Fore.CYAN + backlogName)
    except:
        backlogFileError(backlogLocation)

def updateBacklog():
    backlogName = sys.argv[2]
    itemToUpdate = sys.argv[3]
    newStatus = False
    if argc > 4:
        newStatus = '[' + sys.argv[4] + ']'

    backlogLocation = getBacklogLocation(backlogName)
    if not backlogLocation:
        return

    try:
        with open(backlogLocation, 'r+') as jsonFile:
            backlogInfo = json.load(jsonFile)
            
            if itemToUpdate not in backlogInfo['content']:
                print('\n' + Fore.YELLOW + itemToUpdate + Fore.WHITE + ' isn\'t in ' + Fore.CYAN + backlogName + Fore.WHITE + '!')
                return
            if newStatus:
                backlogInfo['content'][itemToUpdate] = newStatus
            elif backlogInfo['content'][itemToUpdate] in (1, 2, 3):
                backlogInfo['content'][itemToUpdate] = min(backlogInfo['content'][itemToUpdate]+1, 3)
            else:
                print('\nA custom status can only be replaced by another custom status! (at least, until I update this feature...)')
                return

            jsonFile.seek(0)
            json.dump(backlogInfo, jsonFile)
            jsonFile.truncate()

            print('\n' + Fore.YELLOW + itemToUpdate + Fore.WHITE + ' has been updated!')
    except:
        backlogFileError(backlogLocation)


def markItemDone():
    backlogName = sys.argv[2]
    itemToUpdate = sys.argv[3]

    backlogLocation = getBacklogLocation(backlogName)
    if not backlogLocation:
        return

    try:
        with open(backlogLocation, 'r+') as jsonFile:
            backlogInfo = json.load(jsonFile)
            
            if itemToUpdate not in backlogInfo['content']:
                print('\n' + Fore.YELLOW + itemToUpdate + Fore.WHITE + ' isn\'t in ' + Fore.CYAN + backlogName + Fore.WHITE + '!')
                return
            
            backlogInfo['content'][itemToUpdate] = 3

            jsonFile.seek(0)
            json.dump(backlogInfo, jsonFile)
            jsonFile.truncate()

            print('\n' + Fore.YELLOW + itemToUpdate + Fore.WHITE + ' has been marked as ' + Fore.GREEN + '[DONE]' + Fore.WHITE + '!')
    except:
        backlogFileError(backlogLocation)

def markItemNotDone():
    backlogName = sys.argv[2]
    itemToUpdate = sys.argv[3]

    backlogLocation = getBacklogLocation(backlogName)
    if not backlogLocation:
        return

    try:
        with open(backlogLocation, 'r+') as jsonFile:
            backlogInfo = json.load(jsonFile)
            
            if itemToUpdate not in backlogInfo['content']:
                print('\n' + Fore.YELLOW + itemToUpdate + Fore.WHITE + ' isn\'t in ' + Fore.CYAN + backlogName + Fore.WHITE + '!')
                return
            
            backlogInfo['content'][itemToUpdate] = 1

            jsonFile.seek(0)
            json.dump(backlogInfo, jsonFile)
            jsonFile.truncate()

            print('\n' + Fore.YELLOW + itemToUpdate + Fore.WHITE + ' has been marked as ' + Fore.RED + '[NOT DONE]' + Fore.WHITE + '!')
    except:
        backlogFileError(backlogLocation)


def markItemInProgress():
    backlogName = sys.argv[2]
    itemToUpdate = sys.argv[3]

    backlogLocation = getBacklogLocation(backlogName)
    if not backlogLocation:
        return

    try:
        with open(backlogLocation, 'r+') as jsonFile:
            backlogInfo = json.load(jsonFile)
            
            if itemToUpdate not in backlogInfo['content']:
                print('\n' + Fore.YELLOW + itemToUpdate + Fore.WHITE + ' isn\'t in ' + Fore.CYAN + backlogName + Fore.WHITE + '!')
                return
            
            backlogInfo['content'][itemToUpdate] = 2

            jsonFile.seek(0)
            json.dump(backlogInfo, jsonFile)
            jsonFile.truncate()

            print('\n' + Fore.YELLOW + itemToUpdate + Fore.WHITE + ' has been marked as ' + Fore.YELLOW + '[IN PROGRESS]' + Fore.WHITE + '!')
    except:
        backlogFileError(backlogLocation)

def removeItem():
    backlogName = sys.argv[2]
    itemToDelete = sys.argv[3]

    backlogLocation = getBacklogLocation(backlogName)
    if not backlogLocation:
        return

    try:
        with open(backlogLocation, 'r+') as jsonFile:
            backlogInfo = json.load(jsonFile)
            
            if itemToDelete not in backlogInfo['content']:
                print('\n' + Fore.YELLOW + itemToDelete + Fore.WHITE + ' isn\'t in ' + Fore.CYAN + backlogName + Fore.WHITE + '!')
                return

            backlogInfo['content'].pop(itemToDelete, None)
            
            jsonFile.seek(0)
            json.dump(backlogInfo, jsonFile)
            jsonFile.truncate()
            
            print('\n' + Fore.YELLOW + itemToDelete + Fore.WHITE + ' has been removed from ' + Fore.CYAN + backlogName + Fore.WHITE + '!')
    except:
        backlogFileError(backlogLocation)

def deleteBacklog(backlogName):
    backlogLocation = getBacklogLocation(backlogName)
    if not backlogLocation:
        return

    oResponse = input('\nOnce you delete a backlog, you can\'t get it back!\nAre you sure you want to delete it? (y/n): ')
    while oResponse.lower() not in ('yes', 'no', 'y', 'n'):
        oResponse = input('\nInvalid response! Must be \'y\' or \'n\': ')
    if oResponse.lower() in ('yes', 'y'):
        print('\nOkay, deleting!')
    else:
        print('\nBacklog has not been deleted.')
        return
    
    os.remove(backlogLocation)
    print('\nBacklog deleted!')

    try:
        with open(backlogInfoFile, 'r+') as jsonFile:
            backlogList = json.load(jsonFile)
            backlogList.pop(backlogName, None)
                    
            jsonFile.seek(0)
            json.dump(backlogList, jsonFile)
            jsonFile.truncate()
    except:
        backlogInfoFileError()
        return;

def listBacklogs():
    try:
        with open(backlogInfoFile, 'r') as jsonFile:
            backlogList = json.load(jsonFile)
            
            print(Fore.BLUE + '\t____Backlogs____\n')
            
            if len(backlogList) > 0:
                for name, location in backlogList.items():
                    print('\t' + Fore.CYAN + name)
            else:
                print('\t' + Fore.WHITE + 'You have no backlogs!')

    except:
        backlogInfoFileError()
        return;
    

def resetBacklog(backlogName):
    backlogLocation = getBacklogLocation(backlogName)
    if not backlogLocation:
        return

    oResponse = input('\nBy resetting your backlog, all your progress will be reset to ' + Fore.RED + '[NOT DONE]' + Fore.WHITE + '!\nAre you sure you want to reset it? (y/n): ')
    while oResponse.lower() not in ('yes', 'no', 'y', 'n'):
        oResponse = input('\nInvalid response! Must be \'y\' or \'n\': ')
    if oResponse.lower() in ('yes', 'y'):
        print('\nOkay, resetting!')
    else:
        print('\nBacklog has not been reset.')
        return

    try:
        with open(backlogLocation, 'r+') as jsonFile:
            backlogInfo = json.load(jsonFile)
            
            for key, value in backlogInfo['content'].items():
                backlogInfo['content'][key] = 1
            
            jsonFile.seek(0)
            json.dump(backlogInfo, jsonFile)
            jsonFile.truncate()
            
            print('\nAll items in ' + Fore.CYAN + backlogName + Fore.WHITE + ' have been reset to ' + Fore.RED + '[NOT DONE]' + Fore.WHITE + '.')
    except:
        backlogFileError(backlogLocation)





def handleCommands():
    if sys.argv[1].lower() in ('-h', '--h', '-help', '--help'):
        displayHelp()
    elif sys.argv[1] == 'list':
        listBacklogs()
    elif argc > 2:
        if sys.argv[1] == 'create':
            createBacklog(sys.argv[2])
        elif sys.argv[1] == 'check':
            checkBacklog(sys.argv[2])
        elif sys.argv[1] == 'delete':
            deleteBacklog(sys.argv[2])
        elif sys.argv[1] == 'reset':
            resetBacklog(sys.argv[2])
        elif argc > 3:
            if sys.argv[1] == 'add':
                addToBacklog()
            elif sys.argv[1] == 'update':
                updateBacklog()
            elif sys.argv[1] == 'done':
                markItemDone()
            elif sys.argv[1] == 'notdone':
                markItemNotDone()
            elif sys.argv[1] == 'inprogress':
                markItemInProgress()
            elif sys.argv[1] == 'remove':
                removeItem()
            else:
                displayError()
        else:
            displayError()
    else:
        displayError()



ensureWorking()

if argc > 1:
    handleCommands()
else:
    displayHelp()
