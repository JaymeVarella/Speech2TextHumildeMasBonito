import speech_recognition
import pyttsx3

import sounddevice as sd
from scipy.io.wavfile import write

try:
    import tkinter as tk
    from tkinter import ttk
except:
    import Tkinter as tk
    from Tkinter import ttk

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

    def recordFromMic(self):
        fs = 44100  # Sample rate
        seconds = 5  # Duration of recording
        self.audio = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write('output.wav', fs, self.audio)
        self.lb_codigo.configure(text="Arquico criado!")

    def transcreverAudio(self):
        while True:
            self.transcricao.insert(tk.END, '.')
            try:
                self.recognizer =  speech_recognition.Recognizer()
                self.audioFile = speech_recognition.AudioFile('output.wav')
                self.transcrito = self.recognizer.recognize_google(self.audioFile)
                self.transcrito = transcrito.lower()
                self.transcricao.insert(tk.END, self.transcrito)
            except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
                continue

class Aplication(Funcs):
    def __init__(self):
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

        self.bt_convMP32WAV = tk.Button(self.frame_1, text="MP3 to WAV", command=self.limpa_tela)
        self.bt_convMP32WAV.place(relx=0.05,rely=0.45, relwidth=0.2, relheight=0.15)

        self.bt_listenMIC = tk.Button(self.frame_1, text="MIC", command=self.recordFromMic)
        self.bt_listenMIC.place(relx=0.3,rely=0.45, relwidth=0.2, relheight=0.15)

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

        self.bt_saveTXT = tk.Button(self.frame_2, bg="#639FAB", text="Salvar em TXT")
        self.bt_saveTXT.place(relx=0.80,rely=0.86, relwidth=0.19, relheight=0.13)

        self.bt_saveclipboard = tk.Button(self.frame_2, bg="#639FAB", text="Salvar na Área de Transferência")
        self.bt_saveclipboard.place(relx=0.60,rely=0.86, relwidth=0.19, relheight=0.13)


    def transcr_area(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3, column=("col1","col2 ","col3","col4"))
        self.listaCli.heading("#0",text="")
        self.listaCli.heading("#1",text="codigo")
        self.listaCli.heading("#2",text="Nome")
        self.listaCli.heading("#3",text="tel")
        self.listaCli.heading("#4",text="cid")
        self.listaCli.column("#0",width=1)
        self.listaCli.column("#1",width=50)
        self.listaCli.column("#2",width=200)
        self.listaCli.column("#3",width=125)
        self.listaCli.column("#4",width=125)
        self.listaCli.place(relx=0.01,rely=0.5,relwidth=0.95,relheight=0.85)

        self.scroollista = tk.Scrollbar(self.frame_2, orient="vertical")
        self.listaCli.configure(yscroll = self.scroollista)
        self.scroollista.place(relx=0.96,rely=0.5,relwidth=0.04,relheight=0.45)


if __name__== '__main__':
    Aplication()
