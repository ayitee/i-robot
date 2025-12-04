from machine import Pin
import time 

#config
TRIGP = 17
ECHOP = 16
trig = Pin(TRIGP, Pin.OUT)
echo = Pin(ECHOP, Pin.IN)

BTNP = 15
btn = Pin(BTNP, Pin.IN, Pin.PULL_UP)
prev_btn_st = 1

##frequence
SPL_ITVL_MS = 67    #15/s
AVR_ITVL_MS = 250   #3/s

##moy mobile
BUFFRSZ = 7
dist_bffr = []

##record
recording = False
record_start_ticks = None
log_data = []
file_index = 1

def mesurer_dist_cm():

    trig.value(0)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    timeout_us = 30000

    while echo.value() == 0:
        pass   # wait for HIGH
    start = time.ticks_us()

    while echo.value() == 1:
        pass   # wait for LOW
    end = time.ticks_us()
    
    duration = time.ticks_diff(end, start)
    dist_cm = duration / 58.0
    return dist_cm

def save_csv(data):
    
    global file_index

    if not data:
        print("no data to save")
        return
    
    filename = "ultra_log_{03d}.csv".format(file_index)
    file_index += 1

    try:
        with open(filename, "w") as f:
            f.write("time_ms,last_distance_cm,avg_distance_cm\n")
            for t_ms, last_d, avg_d in data:
                if last_d is None:
                    last_d_str = ""
                else:
                    last_d_str = "{:.2f}".format(last_d)
                avg_d_str = "{:.2f}".format(avg_d)
                f.write("{},{},{}\n".format(t_ms, last_d_str, avg_d_str))
        print(">>>data saved at : ",filename)
    except Exception as e:
        print(">>> Error during file creation :", e)



print(""" ____   __  ____  ____   __   __      ____   __  ____    _  _  ____  _  _   __   __    __    __      ____  ____  ____  ____  __  ___   __   __   __  
(  _ \ / _\(_  _)(  _ \ /  \ (  )    (  _ \ /  \(_  _)  ( \/ )(_  _)/ )( \ /  \ /  \  /  \  /  \ ___(    \(_  _)( __ \(  __)(  )/ __) /  \ /  \ /  \ 
 ) __//    \ )(   )   /(  O )/ (_/\   ) _ ((  O ) )(     )  (   )(  ) \/ ((_/ /(  0 )(  0 )(_/ /(___)) D (  )(   (__ ( ) _)  )(( (_ \(_/ /(_/ /(_/ / 
(__)  \_/\_/(__) (__\_) \__/ \____/  (____/ \__/ (__)   (_/\_) (__) \____/ (__) \__/  \__/  (__)    (____/ (__) (____/(__)  (__)\___/ (__) (__) (__) """)
print(2*"=========================================================================================================================================== \n", "\n")
print("ultrasound sensor loadin' up")
time.sleep_us(300000)
print("succefully loaded ! gettin' data")
print("""
     —————————————————————Pin used————————————————————_____
    | comp(ultrasound_sensor), name = TRIG, pin = GP17     |            
    | comp(ultrasound_sensor), name = ECHO, pin = GP16     |
    | comp(external), name = BUTTON, pin = GP15            |
     —————————————————————————————————————————————————_____|
      """)

time.sleep(100000)

last_average_time = time.ticks_ms()

while True:
    loop_start = time.ticks_ms()

    btn_st = btn.value()
    if prev_btn_st == 1 and btn_st== 0:
        
        if not recording:
            recording = True
            record_start_ticks = time.ticks_ms()
            log_data = []
            print(">>> starting recording")
        
        else:
            recording = False
            print(">>> stopping rec, saving data...")
            save_csv(log_data)
            record_start_ticks = None
            print(">>> saved succesfully !")
            log_data = []
    
    prev_btn_st = btn_st

    #measure @ 15Hz
    dist = mesurer_dist_cm

    if dist is not None:
        dist_bffr.append(dist)
        if len(dist_bffr) > BUFFRSZ:
            dist_bffr.pop(0)
    #calc buffer
    now = time.ticks_ms()    
    if time.ticks_diff(now, last_average_time) >= AVR_ITVL_MS:  
        if dist_bffr:
            moyenne = sum(dist_bffr) / len(dist_bffr)

        if dist is not None:
            print(" | [latest_data] = {:.1f} cm | ———— [buffer({} last)] = {:.1f} cm  |"
                  .format(dist, len(dist_bffr), moyenne))
        else:
            print(" | [latest_data] = XXXX-invalid-XXXX | ———— [buffer({} last)] = {:.1f} cm  |"
                  .format(dist, len(dist_bffr), moyenne))
        
        if recording and record_start_ticks is not None:
            elapsed_ms = time.ticks_diff(now, record_start_ticks)
            log_data.append((elapsed_ms, dist, moyenne))
    else:
        print("XXX. no. valid. data.  XXX")
    last_average_time = now

    #respect 15 measure/s
    elapsed = time.ticks_diff(time.ticks_ms(), loop_start)
    reste = SPL_ITVL_MS - elapsed
    if reste > 0:
        time.sleep_ms(reste)