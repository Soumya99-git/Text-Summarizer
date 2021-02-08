import speech_recognition as sr
import moviepy.editor as mp
from pytube import YouTube
import os
import subprocess
from multiprocessing import Process
import feedback_analysis
from pydub import AudioSegment
import text_summariztion

def video_to_audio(vid_path,dest_path):
    video = mp.VideoFileClip(vid_path)
    video.audio.write_audiofile(dest_path)
    video.close()
    return dest_path

def mp3_to_wav(fname):
    os.chdir(r"C:\Users\Soumya Chatterjee\Desktop\INFRAMIND\PROJECT\uploads")
    sound = AudioSegment.from_mp3(fname)
    os.remove(fname)
    fname=fname[:-3]+"wav"
    sound.export(fname,format="wav")

    return fname

def you_to_video(url):
    YouTube(url).streams.get_by_resolution("720p").download()
    
def you_to_audio(url):
    os.chdir(r"c:\Users\Soumya Chatterjee\Desktop\INFRAMIND\PROJECT\uploads")
    for i in os.listdir():
        os.remove(i)
    
    mp4 = YouTube(url).streams.get_highest_resolution().download()
    mp3 = mp4.split(".mp4",1)[0] +".mp3"
    video_to_audio(mp4,mp3)
    os.remove(mp4)
    return os.path.join(r"c:\Users\Soumya Chatterjee\Desktop\INFRAMIND\PROJECT\uploads",mp3)    
    
def spliter_audio_text(fname,flag):            #if flag = 1 then to text summarization from audio else if flag = 0 then audio or video to feedback analysis

    os.chdir(r"C:\Users\Soumya Chatterjee\Desktop\INFRAMIND\PROJECT\uploads")
    for i in os.listdir():
        if i == fname:
            continue
        else:
            os.remove(i)
    

    if fname[-3:]=="mp3":
        fname = mp3_to_wav(fname)

    elif fname[-3:]=="mp4":
        dest_path = fname[:-3]+"wav"
        fname = video_to_audio(fname,dest_path)
    
    print(fname)
 
    command = "ffmpeg -i "+fname+" -f segment -segment_time 30 -c copy %03d.wav"
    subprocess.call(command,shell=True)
    files = []
    for filename in os.listdir('.'):
        if len(filename)==7:
            files.append(filename)
    files.sort()
    print(files)
    count = 0
    txt = [] 
    for filename in files:
        with open(filename,'rb') as fp:
            r = sr.Recognizer()
            audio = sr.AudioFile(fp)
            with audio as source:
                audio_file = r.record(source)
        try:
            result = r.recognize_google(audio_file,language="en_In")
            txt.append(result)
            count += 1
            print(count)
            os.remove(filename)

        except:
            count += 1
            print("error ")
            os.remove(filename)
            continue
    if flag==1:
        res = fname[:-3]+"txt"
        with open(res,"a") as fp:
            fp.writelines(txt)
        npath =  os.path.join(r"c:\Users\Soumya Chatterjee\Desktop\INFRAMIND\PROJECT\uploads",res)
        r_path = text_summariztion.summarization(npath)
        return r_path

    elif flag==0:
        string = ""
        for i in txt:
            string+=i
        return feedback_analysis.feedback(string),string

    

#if __name__=="__main__":
#    print(spliter_audio_text("WIN_20210128_20_37_33_Pro.mp4",0))
    