import os
import ffmpeg

def DurationCrop(floc,nfloc,start,duration):
    os.system(f"ffmpeg -ss {start} -i {floc} -t {duration} {nfloc}")
    return True
def video_to_video_note(floc, nfloc):
    probe = ffmpeg.probe(floc)
    for stream in probe["streams"]:
        if stream["codec_type"]=="video":
            w = stream['width']
            h = stream['height']
            l = stream['duration']
    if float(l)>60:
        return 'toolong'
    s = min(w,h)
    if w>h:
        x=(w-h)//2
        y=0
    if w==h:
        x=0
        y=0
    if w<h:
        x=0
        y=(h-w)//2
    os.system(f"ffmpeg -y -i {floc} -vf crop={s}:{s}:{x}:{y},scale=384:384,setsar=1:1 {nfloc}")
    return True