from audio2numpy import open_audio
import sounddevice as sd
import os

from pynput.keyboard import Key, Listener


class Sound:
    def __init__(self, _title):
        self.title = _title

    def setSignal(self, _signal):
        self.signal = _signal

    def setMetaData(self, _duration, _sampling_rate):
        self.duration_true = _duration
        self.duration_min = int(_duration/60)
        self.duration_sec = int(_duration%60)
        self.duration_str = '{}:{}'.format(self.duration_min, self.duration_sec)

        self.sampling_rate = _sampling_rate


    def getSignal(self):
        return self.signal

    def getTitle(self):
        return self.title

    def getDuration(self):
        return self.duration_true


    def getDurationStr(self):
        return self.duration_str

    def getSamplingRate(self):
        return self.sampling_rate


class DataManager:
    def __init__(self):
        self.title_list = []
        self.sound_dict = {}

    def loadFile(self, _title, _path):
        signal, sampling_rate = open_audio(_path)
        
        self.title_list.append(_title)

        duration = len(signal)/sampling_rate

        sound = Sound(_title)
        sound.setSignal(signal)
        sound.setMetaData(duration, sampling_rate)
        
        self.sound_dict[_title] = sound

    def load(self, _dir):
        for file in os.listdir(_dir):
            if file.endswith(".mp3") or file.endswith(".wav"):
                title = file.split('.')[0]
                path = os.path.join(_dir, file)
                
                self.loadFile(title, path)
        

    def getFiles(self):
        pass

    def get(self, _title):
        return self.sound_dict[_title]

    def getTitles(self):
        return self.title_list

    



class App:
    def __init__(self):
        self.data_mgr = DataManager()
        self.file_dir = '.\\Sounds'
        sd.default.samplerate = 48000
        sd.default.device = 'CABLE Input (VB-Audio Virtual C, MME'

        self.k = KeyInput(self)

    def play(self, _title):

        self.stop()

        sound = self.data_mgr.get(_title)
        signal = sound.getSignal()
        
        sd.default.samplerate = sound.getSamplingRate()
        sd.play(signal)

        

        return sound.getDuration()

    def quit(self):
        self.stop()
        self.k.listener.stop()
    
    def stop(self):
        sd.stop()


    def setDirectory(self, _dir):
        self.file_dir = _dir

    def load(self):
        self.data_mgr.load(self.file_dir)
    

    def getTitles(self):
        return self.data_mgr.getTitles()





class KeyInput:
    def __init__(self, app):
        self.app = app
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def start(self):
        
        self.listener.join()
##        with Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
##            self.listener.join()

    def on_press(self, key):
        if isinstance(key, Key):
            key_id = key.name
        else:
            key_id = key.vk

        
        self.action(key_id)

    def on_release(self, key):
        if isinstance(key, Key):
            key_id = key.name
        else:
            key_id = key.vk


          
        

    def action(self, key_id):
        if key_id == 103:
            self.app.play('HIIII')

        elif key_id == 104:
            self.app.play('BYE')











