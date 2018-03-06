respeaker v2入手
===============

>如果respeaker v2上运行的系统是2018年之前的，先升级到最新的系统吧。如果还对老系统情有独钟，可以查看history_doc.md

### 入坑
1. 使用 `screen /dev/ttyACM0 115200` 或 putty 通过USB OTG虚拟串口登录respeaker v2的 Debian 系统，用户名和密码都是respeaker

   将respeaker v2带OTG标签的USB口连接上电脑，会出现一个虚拟的串口

2. 用Network Manager命令行工具nmtui联网 `sudo nmtui`
3. 安装支持Amazon Alexa Voice Service和百度DuerOS的 avs 库，并检测录音和放音

   ```
   pip install avs      # alexa-audio-check, alexa-auth, dueros-auth, alexa-tap and alexa will be installed at ~/.local/bin
   ~/.local/bin/alexa-audio-check       # it calculates recording audio RMS and plays alarm
   ```

4. 用`ip addr`获取设备IP地址，用VNC登录系统，VNC地址是IP，默认端口号5900，VNC客户端推荐使用 [VNC Viewer for Google Chrome](https://chrome.google.com/webstore/detail/vnc%C2%AE-viewer-for-google-ch/iabmpiboiopbgfabjmgeedhcmjenhbla?hl=en)
5. 在VNC远程桌面中打开terminal，运行`~/.local/bin/alexa-auth`获取Alexa授权（或运行`dueros-auth`使用百度DuerOS）
6. 运行`~/.local/bin/alexa-tap`，log输出on_ready之后，即可按Enter开始语音对话
7. 运行snowboy版hands-free alexa
   ```
   sudo apt update
   sudo apt install libatlas-base-dev                # required by snowboy
   pip install --no-deps snowboy*.whl          # install pre-build snowboy
   pip install webrtc_audio_processing*.whl
   pip install voice-engine
   python ns_kws_alexa.py
   ```
8. 加灯效
   ```
   pip install pixel-ring
   python ns_kws_alexa_with_light.py
   ```



