# BLE_with_PI3
讓樹莓派3接收BLE裝置資訊的過程記錄

## 安裝樹莓派3的OS(需自備Micro SD卡)

    https://www.raspberrypi.org/downloads/raspbian/

    安裝完之後在SD卡的根目錄新增以下兩個檔案
    
    1.ssh檔案(空白即可)
    2.wpa_supplicant.conf檔案
    並填入以下的資訊
    
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1

    network={
        ssid="附近的wifi名稱"
        psk="wifi的密碼"
        proto=RSN
        key_mgmt=WPA-PSK
        pairwise=CCMP
    }

    等待raspberry pi連上網路後就可以使用ssh來進行控制

## 藍芽的一些設定(HM-10)

    http://www.pondoudou.com/?p=2004
    
    [關於HM-10裝置的詳細內容](http://www.martyncurrey.com/hm-10-bluetooth-4ble-modules/)
