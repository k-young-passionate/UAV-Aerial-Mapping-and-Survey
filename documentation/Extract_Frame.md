## How to extract frame from video

### MacOS
- Use `ffmpeg`
```
brew install ffmpeg
```
- extract frame from video
```
ffmpeg -i /path/my/video /path/my/output-%04d.jpg
```

- hide banner option
```
ffmpeg -i /path/my/video /path/my/output-%04d.jpg -hide_banner
```

- extract frame count what you want from video

```
ffmpeg -i /path/my/video -vf fps='seconds you want' /path/my/output-%04d.jpg
```
* output one image every ten minutes
    ```
    ffmpeg -i /path/my/video -vf fps=1/600 /path/my/output-%04d.jpg
    ```
* Output one image for every I-frame :
    ```
    ffmpeg -i a.mp4 -vf "select='eq(pict_type, PICT_TYPE_I)'" -vsync vfr font/output-%04d.jpg
    ```