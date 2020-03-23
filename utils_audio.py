from gtts import gTTS 
import librosa    
import pysndfile
from pydub import AudioSegment


def text_to_speech(text, file='tts.mp3', language='en', slow=False, convert_to_wav=False, target_sample_rate=None):
    speech = gTTS(text=text, lang=language, slow=slow)
    speech.save(file)
    if convert_to_wav:
        wav_file = file.replace('.mp3', '.wav')
        sound = AudioSegment.from_mp3(file)
        sound.export(wav_file, format="wav")
        
        if target_sample_rate is not None: 
            data, s = librosa.load(wav_file, sr=target_sample_rate)
            # librosa.output.write_wav(wav_file, data, sr=target_sample_rate)
            pysndfile.sndio.write(wav_file, data, rate=target_sample_rate, format='wav', enc='pcm16')


def create_mellotron_input_from_lyrics_lines(lyrics, speaker_id, path='/app/jupyter'):
    lyrics_lines = lyrics.strip().split('\n')
    
    for idx, line in enumerate(lyrics_lines):
        text_to_speech(line, file=f'tts_{idx:02d}.mp3', convert_to_wav=True, target_sample_rate=22050)
    
    files = []
    with open('mellotron/data/examples_filelist.txt', 'wt') as f:
        for idx, line in enumerate(lyrics_lines):
            files.append(f"tts_{idx:02d}.wav")
            f.write(f"{path}/{files[-1]}|{line}|{speaker_id}\n")
    
    return files
