import serial

import serial.tools.list_ports

import tkinter

window=tkinter.Tk()
window.geometry("150x50")
window.resizable(False, False)


# 사용 가능한 시리얼 포트 정보 가져오기

ports = serial.tools.list_ports.comports()
str=[]
i=0
for p in ports:
    if 'FT232R USB UART' in p.description:
        ser = serial.Serial(p.device, 38400)  # 아두이노와 시리얼 통신 연결
        break

while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode().strip()
        if 'C' in data:
            id = data
            str.append(id)
            i+=1
            if i ==2:
                print(str[0])
                print(str[1])
                print()
                # GUI 측정한 온도 값 디스플레이
                label=tkinter.Label(window, text=str[0]+"\n"+str[1],width=0, height=0)
                label.grid(row=0,column=0) 
                window.update()
                i=0
                str.clear()
                label.destroy()

