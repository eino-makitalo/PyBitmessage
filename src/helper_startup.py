import shared
import ConfigParser
import sys
import os
import locale
import random
import string

from namecoin import ensureNamecoinOptions

storeConfigFilesInSameDirectoryAsProgramByDefault = False  # The user may de-select Portable Mode in the settings if they want the config files to stay in the application data folder.

def loadConfig():
    if shared.appdata:
        shared.config.read(shared.appdata + 'keys.dat')
        #shared.appdata must have been specified as a startup option.
        try:
            shared.config.get('bitmessagesettings', 'settingsversion')
            print 'Loading config files from directory specified on startup: ' + shared.appdata
            needToCreateKeysFile = False
        except:
            needToCreateKeysFile = True

    else:
        shared.config.read('keys.dat')
        try:
            shared.config.get('bitmessagesettings', 'settingsversion')
            print 'Loading config files from same directory as program.'
            needToCreateKeysFile = False
            shared.appdata = ''
        except:
            # Could not load the keys.dat file in the program directory. Perhaps it
            # is in the appdata directory.
            shared.appdata = shared.lookupAppdataFolder()
            shared.config.read(shared.appdata + 'keys.dat')
            try:
                shared.config.get('bitmessagesettings', 'settingsversion')
                print 'Loading existing config files from', shared.appdata
                needToCreateKeysFile = False
            except:
                needToCreateKeysFile = True

    if needToCreateKeysFile:
        # This appears to be the first time running the program; there is
        # no config file (or it cannot be accessed). Create config file.
        shared.config.add_section('bitmessagesettings')
        shared.config.set('bitmessagesettings', 'settingsversion', '8')
        shared.config.set('bitmessagesettings', 'port', '8444')
        shared.config.set(
            'bitmessagesettings', 'timeformat', '%%a, %%d %%b %%Y  %%I:%%M %%p')
        shared.config.set('bitmessagesettings', 'blackwhitelist', 'black')
        shared.config.set('bitmessagesettings', 'startonlogon', 'false')
        if 'linux' in sys.platform:
            shared.config.set(
                'bitmessagesettings', 'minimizetotray', 'false')
                              # This isn't implimented yet and when True on
                              # Ubuntu causes Bitmessage to disappear while
                              # running when minimized.
        else:
            shared.config.set(
                'bitmessagesettings', 'minimizetotray', 'true')
        shared.config.set(
            'bitmessagesettings', 'showtraynotifications', 'true')
        shared.config.set('bitmessagesettings', 'startintray', 'false')
        shared.config.set('bitmessagesettings', 'socksproxytype', 'none')
        shared.config.set(
            'bitmessagesettings', 'sockshostname', 'localhost')
        shared.config.set('bitmessagesettings', 'socksport', '9050')
        shared.config.set(
            'bitmessagesettings', 'socksauthentication', 'false')
        shared.config.set(
            'bitmessagesettings', 'sockslisten', 'false')
        shared.config.set('bitmessagesettings', 'socksusername', '')
        shared.config.set('bitmessagesettings', 'sockspassword', '')
        shared.config.set('bitmessagesettings', 'keysencrypted', 'false')
        shared.config.set(
            'bitmessagesettings', 'messagesencrypted', 'false')
        shared.config.set('bitmessagesettings', 'defaultnoncetrialsperbyte', str(
            shared.networkDefaultProofOfWorkNonceTrialsPerByte * 2))
        shared.config.set('bitmessagesettings', 'defaultpayloadlengthextrabytes', str(
            shared.networkDefaultPayloadLengthExtraBytes))
        shared.config.set('bitmessagesettings', 'minimizeonclose', 'false')
        shared.config.set(
            'bitmessagesettings', 'maxacceptablenoncetrialsperbyte', '0')
        shared.config.set(
            'bitmessagesettings', 'maxacceptablepayloadlengthextrabytes', '0')
        shared.config.set('bitmessagesettings', 'dontconnect', 'true')
        shared.config.set('bitmessagesettings', 'userlocale', 'system')
        shared.config.set('bitmessagesettings', 'useidenticons', 'True')
        shared.config.set('bitmessagesettings', 'identiconsuffix', ''.join(random.choice("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz") for x in range(12))) # a twelve character pseudo-password to salt the identicons
        
         #start:UI setting to stop trying to send messages after X days/months
        shared.config.set(
            'bitmessagesettings', 'stopresendingafterxdays', '')
        shared.config.set(
            'bitmessagesettings', 'stopresendingafterxmonths', '')
        #shared.config.set(
        #    'bitmessagesettings', 'timeperiod', '-1')
        #end

        # Are you hoping to add a new option to the keys.dat file? You're in
        # the right place for adding it to users who install the software for
        # the first time. But you must also add it to the keys.dat file of
        # existing users. To do that, search the class_sqlThread.py file for the
        # text: "right above this line!"

        ensureNamecoinOptions()

        if storeConfigFilesInSameDirectoryAsProgramByDefault:
            # Just use the same directory as the program and forget about
            # the appdata folder
            shared.appdata = ''
            print 'Creating new config files in same directory as program.'
        else:
            print 'Creating new config files in', shared.appdata
            if not os.path.exists(shared.appdata):
                os.makedirs(shared.appdata)
        if not sys.platform.startswith('win'):
            os.umask(0o077)
        with open(shared.appdata + 'keys.dat', 'wb') as configfile:
            shared.config.write(configfile)
