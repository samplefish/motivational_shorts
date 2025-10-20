from openai import OpenAI
import moviepy.editor as mp
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from gtts import gTTS

pexels_api_key = os.getenv("pexels_api_key")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

openai_api_key = os.getenv("openai_api_key")
elevenlabs_api_key = os.getenv("elevenlabs_api_key")
pexels_api_key = os.getenv("pexels_api_key")


OpenAI.api_key = openai_api_key

client = OpenAI(api_key=openai_api_key)



client = ElevenLabs(
    api_key=elevenlabs_api_key
)

def create_short(motivational_text):
    print("Script:", motivational_text)


    audio = client.text_to_speech.convert(
        text=motivational_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    with open("output.mp3", "wb") as f:
        for chunk in audio: 
            f.write(chunk)


    folder = "motivational\\stock_footage"
    clips = []


    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".mp4"):
            print('Found file name: '+ filename)
            clip = mp.VideoFileClip(os.path.join(folder, filename))
            clip = clip.resize(height=1280).crop(x_center=clip.w/2, width=720, height=1280)
            clips.append(clip)


    video = mp.concatenate_videoclips(clips, method="compose")
    audio = mp.AudioFileClip("output.mp3")

    if video.duration < audio.duration:
        loops = int(audio.duration // video.duration) + 1
        video = mp.concatenate_videoclips([video] * loops, method="compose")
    video = video.set_duration(audio.duration)

    music = mp.AudioFileClip("motivational/stock_sounds/epic.mp3")
    music = music.volumex(0.05)
    music = music.subclip(0, video.duration)
    audio_mix = mp.CompositeAudioClip([music, audio.volumex(1.0)])

    video = video.set_audio(audio_mix)

    os.environ["IMAGEMAGICK_BINARY"] = r"C:\\Program Files\\ImageMagick-7.1.2-Q16-HDRI\\magick.exe"
    txt = mp.TextClip(motivational_text, fontsize=40, color='white', size=video.size, method="caption")
    txt = txt.set_duration(audio.duration).set_position(("center", "bottom"))
    final = mp.CompositeVideoClip([video, txt])

    final.write_videofile("motivational_short.mp4", fps=24)
