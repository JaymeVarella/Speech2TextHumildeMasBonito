import speech_recognition
import pyttsx3

import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment

from scipy.io.wavfile import write

try:
    import tkinter as tk
    from tkinter import ttk, filedialog
except:
    import Tkinter as tk
    from Tkinter import ttk

REC_DURATION = 5
LANGUAGE = "pt-BR"
FILENAME = "output.wav"

COLOR_WINDOWBACKGROUND="#1C5D99"
COLOR_FRAMEBACKGROUND="#BBCDE5"
COLOR_HIGHLIGHT="#222222"
#COLOR_BACKGROUND

root = tk.Tk()

class Funcs():
    def limpa_tela(self):
        self.FileAddress_entry.delete(0, tk.END)
        self.lb_codigo.configure(text='')


    def loadFile(self):
        self.fileAddress = self.FileAddress_entry.get()
        self.lb_codigo.configure(text=self.fileAddress)
        #root = tk.Tk()
        root.withdraw()
        file_name = filedialog.askopenfilename()

    def convertFile(self):
        #root = tk.Tk()
        root.withdraw()
        self.song_path = filedialog.askopenfilename()
        self.song = AudioSegment.from_mp3(self.song_path)
        self.song.export(self.soundFileName, format="wav")
        self.lb_codigo.configure(text=f"Arquivo {self.soundFileName} convertido para .wav!")
        print("Done!")

    def recordFromMic(self):
        fs = 44100  # Sample rate
        seconds = REC_DURATION  # Duration of recording
        self.transcricao.insert(tk.END, "***\n")
        self.audio = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write(self.soundFileName, fs, self.audio)
        data, samplerate = sf.read(self.soundFileName)
        sf.write('sfOutpt.wav', data, samplerate, subtype='PCM_16')
        sf.write('sfOutpt.flac', data, samplerate)
        self.lb_codigo.configure(text=f"Arquivo {self.soundFileName} criado!")

    def transcreverAudio(self):
        self.transcricao.delete('1.0', tk.END)
        while True:
            try:
                self.recognizer =  speech_recognition.Recognizer()
                with speech_recognition.AudioFile('sfOutpt.flac') as self.audioFile:
                    self.audio = self.recognizer.listen(self.audioFile)
                    self.transcrito = self.recognizer.recognize_google(self.audio,language=LANGUAGE)
                    self.transcrito = self.transcrito.lower()
                    self.transcricao.insert(tk.END, self.transcrito)
                    break
                #self.audioFile = speech_recognition.AudioFile('output.wav')
                #self.transcrito = self.recognizer.recognize_google(self.audioFile)
                #self.transcrito = transcrito.lower()
                #self.transcricao.insert(tk.END, self.transcrito)
            except speech_recognition.UnknownValueError:
                self.recognizer = speech_recognition.Recognizer()
                continue
            #endwhile

    def liveTranscript(self):
        self.transcricao.delete('1.0', tk.END)
        self.continueLive = True
        fs = 44100  # Sample rate
        seconds = 5  # Duration of recording
        #self.audio = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        while self.continueLive:
            try:
                self.recognizer =  speech_recognition.Recognizer()
                mic = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
                #self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = self.recognizer.listen(mic)
                text  = self.recognizer.recognize_google(audio)
                text = text.lower()
                self.transcricao.insert(tk.END, text)

            except speech_recognition.UnknownValueError:
                self.recognizer = speech_recognition.Recognizer()
                self.transcricao.insert(tk.END, f'Erro na leitura do audio!')
                continue

    def stopTranscript(self):
        self.continueLive = False

    def saveToClipboard(self):
        try:
            root.clipboard_clear()
            root.clipboard_appent(self.transcricao.get("1.0",tk.END))
            root.update()
        except:
            print("Not working.")

    def save_txt(self):
        text = self.transcricao.get("1.0",'end-1c')
        with open("output.txt","w") as f:
            f.write(text+"\n")


class Aplication(Funcs):
    def __init__(self):
        self.soundFileName = FILENAME

        self.root = root
        self.tela()
        self.campos()
        self.criando_botoes()
        #self.transcr_area()
        root.mainloop()
    def tela(self):
        self.root.title("Reconhecimento de Voz")
        self.root.configure(background=COLOR_WINDOWBACKGROUND)
        self.root.geometry("700x500")
        self.root.resizable(True,True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=400, height=300)
    def campos(self):
        self.frame_1 = tk.Frame(self.root, bd=4, bg=COLOR_FRAMEBACKGROUND, highlightbackground=COLOR_HIGHLIGHT, highlightthickness=3)
        self.frame_2 = tk.Frame(self.root, bd=4, bg=COLOR_FRAMEBACKGROUND, highlightbackground=COLOR_HIGHLIGHT, highlightthickness=3)
        self.frame_1.place(relx = 0.05,rely = 0.05,relwidth = 0.9,relheight = 0.5)
        self.frame_2.place(relx = 0.05,rely = 0.57,relwidth = 0.9,relheight = 0.4)


    def criando_botoes(self):
        #buscar arquivo
        self.lb_frameDados = tk.Label(self.frame_1, text="Programa Humilde Demais", anchor="w", bg=COLOR_FRAMEBACKGROUND)
        self.lb_frameDados.place(relx=0.0,rely=0.0, relwidth = 0.98, relheight = 0.05)

        self.bt_buscar = tk.Button(self.frame_1, text="Carregar", command=self.loadFile)
        self.bt_buscar.place(relx=0.05,rely=0.15, relwidth=0.1, relheight=0.15)

        self.FileAddress_entry = tk.Entry(self.frame_1)
        self.FileAddress_entry.place(relx=0.15,rely=0.15, relwidth=0.65, relheight=0.15)

        self.lb_codigo = tk.Label(self.frame_1, text="Arquivo:", anchor="w", bg=COLOR_FRAMEBACKGROUND)
        self.lb_codigo.place(relx=0.15,rely=0.9, relwidth=0.65, relheight=0.08)

        self.bt_convMP32WAV = tk.Button(self.frame_1, text="MP3 to WAV", command=self.convertFile)
        self.bt_convMP32WAV.place(relx=0.05,rely=0.45, relwidth=0.2, relheight=0.15)

        self.bt_listenMIC = tk.Button(self.frame_1, text="MIC", command=self.recordFromMic)
        self.bt_listenMIC.place(relx=0.3,rely=0.45, relwidth=0.2, relheight=0.15)

        self.bt_listenMICLive = tk.Button(self.frame_1, text="Live MIC", command=self.liveTranscript)
        self.bt_listenMICLive.place(relx=0.55,rely=0.45, relwidth=0.2, relheight=0.15)
        self.bt_stopMICLive = tk.Button(self.frame_1, text="stop", command=self.stopTranscript)
        self.bt_stopMICLive.place(relx=0.75,rely=0.45, relwidth=0.1, relheight=0.15)

        #limpar tudo
        self.bt_limpar = tk.Button(self.frame_1, text="Limpar", command=self.limpa_tela)
        self.bt_limpar.place(relx=0.85,rely=0.15, relwidth=0.1, relheight=0.15)
        #transcrever audio
        self.bt_transcr = tk.Button(self.frame_1, bg="#639FAB", text="Transcrever", command=self.transcreverAudio)
        self.bt_transcr.place(relx=0.35,rely=0.7, relwidth=0.30, relheight=0.15)

        self.lb_transcr = tk.Label(self.frame_2, text="Transcrição do áudio", anchor="w", bg=COLOR_FRAMEBACKGROUND)
        self.lb_transcr.place(relx=0.0,rely=0.0, relwidth=0.5, relheight=0.05)

        self.transcricao = tk.Text(self.frame_2)
        self.transcricao.place(relx=0.01,rely=0.1,relwidth = 0.98, relheight = 0.75)

        self.bt_saveTXT = tk.Button(self.frame_2, bg="#639FAB", text="Salvar em TXT", command=self.save_txt)
        self.bt_saveTXT.place(relx=0.80,rely=0.86, relwidth=0.19, relheight=0.13)

        self.bt_saveclipboard = tk.Button(self.frame_2, bg="#639FAB", text="Salvar na Área de Transferência", command=self.saveToClipboard)
        self.bt_saveclipboard.place(relx=0.50,rely=0.86, relwidth=0.24, relheight=0.13)




if __name__== '__main__':
    Aplication()
