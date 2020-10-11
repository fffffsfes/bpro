
import numpy as np
import pyaudio
import RPi.GPIO as GPIO
import keyboard
import time 

NOTE_MIN = 20      
NOTE_MAX = 200       
FSAMP = 16000     
FRAME_SIZE = 1024   
FRAMES_PER_FFT = 3 
out1 = 7  #A
out2 = 12 #B
out3 = 11 #A/
out4 = 13 #B/
 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)

SAMPLES_PER_FFT = FRAME_SIZE*FRAMES_PER_FFT
FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT

NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()

def freq_to_number(f): return 69 + 12*np.log2(f/440.0)
def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)
def note_name(n): return NOTE_NAMES[n % 12] + str(n/12 - 1)
def note_to_fftbin(n): return number_to_freq(n)/FREQ_STEP
def motor_clock() :
     GPIO.output(out1,GPIO.LOW)
     GPIO.output(out2,GPIO.LOW)
     GPIO.output(out3,GPIO.LOW)
     GPIO.output(out4,GPIO.LOW)
     time.sleep(0.01)
      
     GPIO.output(out1,GPIO.LOW)
     GPIO.output(out2,GPIO.LOW)
     GPIO.output(out3,GPIO.LOW)
     GPIO.output(out4,GPIO.HIGH)
     time.sleep(0.01)
      
     GPIO.output(out1,GPIO.LOW)
     GPIO.output(out2,GPIO.LOW)
     GPIO.output(out3,GPIO.HIGH)
     GPIO.output(out4,GPIO.HIGH)
     time.sleep(0.01)
      
     GPIO.output(out1,GPIO.LOW)
     GPIO.output(out2,GPIO.LOW)
     GPIO.output(out3,GPIO.HIGH)
     GPIO.output(out4,GPIO.LOW)
     time.sleep(0.01)
      
     GPIO.output(out1,GPIO.LOW)
     GPIO.output(out2,GPIO.HIGH)
     GPIO.output(out3,GPIO.HIGH)
     GPIO.output(out4,GPIO.LOW)
     time.sleep(0.01)
      
     GPIO.output(out1,GPIO.LOW)
     GPIO.output(out2,GPIO.HIGH)
     GPIO.output(out3,GPIO.LOW)
     GPIO.output(out4,GPIO.LOW)
     time.sleep(0.01)
      
     GPIO.output(out1,GPIO.HIGH)
     GPIO.output(out2,GPIO.HIGH)
     GPIO.output(out3,GPIO.LOW)
     GPIO.output(out4,GPIO.LOW)
     time.sleep(0.01)
      
     GPIO.output(out1,GPIO.HIGH)
     GPIO.output(out2,GPIO.LOW)
     GPIO.output(out3,GPIO.LOW)
     GPIO.output(out4,GPIO.LOW)
     time.sleep(0.01)
      
     GPIO.output(out1,GPIO.HIGH)
     GPIO.output(out2,GPIO.LOW)
     GPIO.output(out3,GPIO.LOW)
     GPIO.output(out4,GPIO.HIGH)
     time.sleep(0.01)

def motor_ccw() :
    GPIO.output(out1,GPIO.LOW)
    GPIO.output(out2,GPIO.LOW)
    GPIO.output(out3,GPIO.LOW)
    GPIO.output(out4,GPIO.LOW)
    time.sleep(0.01)   
      
    GPIO.output(out1,GPIO.HIGH)
    GPIO.output(out2,GPIO.LOW)
    GPIO.output(out3,GPIO.LOW)
    GPIO.output(out4,GPIO.LOW)
    time.sleep(0.01)                        
              
    GPIO.output(out1,GPIO.HIGH)
    GPIO.output(out2,GPIO.HIGH)
    GPIO.output(out3,GPIO.LOW)
    GPIO.output(out4,GPIO.LOW)
    time.sleep(0.01)
                 
    GPIO.output(out1,GPIO.LOW)
    GPIO.output(out2,GPIO.HIGH)
    GPIO.output(out3,GPIO.LOW)
    GPIO.output(out4,GPIO.LOW)
    time.sleep(0.01)
                 
    GPIO.output(out1,GPIO.LOW)
    GPIO.output(out2,GPIO.HIGH)
    GPIO.output(out3,GPIO.HIGH)
    GPIO.output(out4,GPIO.LOW)
    time.sleep(0.01)
                 
    GPIO.output(out1,GPIO.LOW)
    GPIO.output(out2,GPIO.LOW)
    GPIO.output(out3,GPIO.HIGH)
    GPIO.output(out4,GPIO.LOW)
    time.sleep(0.01)
           
    GPIO.output(out1,GPIO.LOW)
    GPIO.output(out2,GPIO.LOW)
    GPIO.output(out3,GPIO.HIGH)
    GPIO.output(out4,GPIO.HIGH)
    time.sleep(0.01)
                 
    GPIO.output(out1,GPIO.LOW)
    GPIO.output(out2,GPIO.LOW)
    GPIO.output(out3,GPIO.LOW)
    GPIO.output(out4,GPIO.HIGH)
    time.sleep(0.01)
                 
    GPIO.output(out1,GPIO.HIGH)
    GPIO.output(out2,GPIO.LOW)
    GPIO.output(out3,GPIO.LOW)
    GPIO.output(out4,GPIO.HIGH)
    time.sleep(0.01)
    

imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))

buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
num_frames = 0


stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                channels=1,
                                rate=FSAMP,
                                input=True,
                                frames_per_buffer=FRAME_SIZE)

stream.start_stream()


window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))


print ('sampling at',FSAMP, 'Hz with max resolution of', FREQ_STEP, 'Hz')


try:
    while stream.is_active():
    
       
        buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
        buf[-FRAME_SIZE:] = np.frombuffer(stream.read(FRAME_SIZE), np.int16)

       
        fft = np.fft.rfft(buf * window)

        
        freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP

        
        if freq > 450 :
            motor_ccw()
            print ('높음')
        elif freq < 430 :
            motor_clock()
            print ('낮음')
        elif 430 <= freq <= 450 :
            print('완료')

except KeyboardInterrupt:
    GPIO.cleanup()
    stream.stop_stream()
    stream.close()
