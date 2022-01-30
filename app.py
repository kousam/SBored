from audio2numpy import open_audio
import sounddevice as sd
import os



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
        if not os.path.isdir(_dir):
            os.mkdir(_dir)
        
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
        self.file_dir = '.\\sounds'
        sd.default.samplerate = 48000
        sd.default.device = 'CABLE Input (VB-Audio Virtual C, MME'


    def play(self, _title):

        self.stop()

        sound = self.data_mgr.get(_title)
        signal = sound.getSignal()
        
        sd.default.samplerate = sound.getSamplingRate()
        sd.play(signal)

        

        return sound.getDuration()

    def quit(self):
        self.stop()

    
    def stop(self):
        sd.stop()


    def setDirectory(self, _dir):
        self.file_dir = _dir

    def load(self):
        self.data_mgr.load(self.file_dir)
    

    def getTitles(self):
        return self.data_mgr.getTitles()

















