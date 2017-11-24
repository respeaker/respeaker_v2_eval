respeaker v2 评估板入坑指南
=========================

### 简易指南
使用仓库里面的配置文件和预编译包快速上手：

1. 使用 `screen /dev/ttyACM0 115200` 或 `minicom -D /dev/ttyACM0 -b 115200` 通过串口登录系统
2. 用Network Manager命令行工具nmtui联网 `sudo nmtui`
3. 下载此仓库，更新配置，设置python虚拟环境，安装软件包
   ```
   su respeaker                           # 切换到respeaker用户，如果已经是respeaker用户，跳过这一步
   cd                                     # 切换到respeaker用户主目录/home/respeaker
   pwd                                    # 确保在/home/respeaker目录
   git clone https://github.com/respeaker/respeaker_v2_eval.git
   cd respeaker_v2
   sudo cp asound.conf /etc/                       # 配置ALSA
   sudo cp pulse/default.pa /etc/pulse/            # 配置pulseaudio
   cp pulse/client.conf ~/.config/pulse/
   pulseaudio -k && pulseaudio -D                  # 重启pulseaudio，不要使用root运行
   sudo cp etc/apt/apt.conf.d/02proxy /etc/apt/apt.conf.d/    # 如果不在SEEED局域网，跳过这一步，这是设置apt缓存代理，加速apt下载
   sudo apt install python-virtualenv
   python -m virtualenv --system-site-packages ~/env          # 创建python虚拟环境
   source ~/env/bin/activate                                  # 激活python虚拟环境
   pip install ./webrtc*.whl
   pip install ./snowboy*.whl
   sudo apt install libatlas-base-dev                         # 安装snowboy依赖包atlas
   pip install avs
   pip install voice-engine
   sudo apt-get install gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly python-gi python-gst gir1.2-gstreamer-1.0
   ./set_alsa_mixer.sh                                        # 设置 alsa 音量
   sudo ip addr                                               # 获取IP地址
   ```
4. 用VNC登录系统，VNC地址是IP加端口号5901，比如`192.168.9.9:5901`，VNC客户端推荐使用 [VNC Viewer for Google Chrome](https://chrome.google.com/webstore/detail/vnc%C2%AE-viewer-for-google-ch/iabmpiboiopbgfabjmgeedhcmjenhbla?hl=en)
5. 在VNC远程桌面中打开terminal，运行`alexa-auth`获取Alexa授权（或运行`dueros-auth`使用百度dueros）
6. 切回到之前配置好python虚拟环境运行`alexa-tap`，即可按Enter开始语音对话
   ```
   source ~/env/bin/activate
   alexa-tap
   ```
7. 运行snowboy版alexa，代码在alexa目录
   ```
   python ns_kws_doa_alexa.py
   ```
8. 加灯效，由于读写SPI需要root权限，所以先切到root用户
   ```
   sudo su
   /home/respeaker/respeaker_v2_eval/enable_pixels.sh # 拉低 pixels 使能引脚
   cp /home/respeaker/.avs.json /root/.avs.json       # 拷贝respeaker用户的alexa配置文件给root用户
   source /home/respeaker/env/bin/activate            # 激活之前配置好的python虚拟环境
   python ns_kws_doa_alexa_with_light.py
   ```

### Hard way
1. 使用 `screen /dev/ttyACM0 115200` 或 `minicom -D /dev/ttyACM0 -b 115200` 通过串口登录系统
2. 用Network Manager命令行工具nmtui联网 `sudo nmtui`
3. （可选）为tmux设置locales，运行`sudo dpkg-reconfigure locales`，选择en_US.UTF-8
4. 设置ALSA，添加配置文件`/etc/asound.conf`
   ```
   pcm.!default {
       type asym
       playback.pcm "dmixed"
       capture.pcm "plughw:0,0"
   }

   pcm.dmixed {
       type dmix
       slave.pcm "hw:0,2"
       ipc_key 123456
   }
   ```
5. 修复一个PulseAudio配置问题，修改`/etc/pulse/default.pa`，禁用module-udev-detect和module-detect，静态加载alsa sink和source，修改之后用respeaker用户重启pulseaudio，运行`pulseaudio -k || pulseaudio -D`
   ```
   ### Load audio drivers statically                                                                                                       
   ### (it's probably better to not load these drivers manually, but instead
   ### use module-udev-detect -- see below -- for doing this automatically) 
   load-module module-alsa-sink device=hw:0,2   
   load-module module-alsa-source device=hw:0,0            
   #load-module module-oss device="/dev/dsp" sink_name=output source_name=input  
   #load-module module-oss-mmap device="/dev/dsp" sink_name=output source_name=input 
   #load-module module-null-sink           
   #load-module module-pipe-sink           
                                                                                                                                        
   ### Automatically load driver modules depending on the hardware available      
   #.ifexists module-udev-detect.so        
   #load-module module-udev-detect   
   #.else                  
   ### Use the static hardware detection module (for systems that lack udev support)    
   #load-module module-detect    
   #.endif
   ```
6. （可选，仅在SEEED局域网可用）使用apt缓存
   ```
   echo "Acquire::http { Proxy \"http://192.168.4.48:3142\"; };" | sudo tee  /etc/apt/apt.conf.d/02proxy
   ```
7. 通过`sudo ip addr`或`sudo ifconfig`获取设备IP地址，用VNC登录系统，VNC地址是IP加端口号5901，比如`192.168.9.9:5901`，VNC客户端推荐使用 [VNC Viewer for Google Chrome](https://chrome.google.com/webstore/detail/vnc%C2%AE-viewer-for-google-ch/iabmpiboiopbgfabjmgeedhcmjenhbla?hl=en)
8. （可选）使用virtualenv建立一个虚拟的python环境 
   ```
   sudo apt update && sudo apt install python-virtualenv
   python -m virtualenv --with-site-packages ~/env
   source ~/env/bin/activate
   ```
9. 安装 avs 库 `pip install avs`
10. 获取alexa或dueros的授权，在VNC中（因为需要在网页登录Amazon或百度），打开terminal，运行alexa-auth 或 dueros-auth，在弹出的浏览器网页登录
11. 运行 alexa，然后可以按Enter键开始语音交互
12. 用Pulseaudio录8通道音频有问题，先关掉Pulseaudio

    ```
    su repseaker
    echo “autospawn = no" > ~/.config/pulse/client.conf
    pulseaudio -k
    ```
