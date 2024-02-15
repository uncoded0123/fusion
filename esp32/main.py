import time, connect, send_recieve, servo

while True:
    if send_recieve.recieve() == 'detected':
        servo.s_on('on')
        send_recieve.send('off')
    time.sleep(0.2)
