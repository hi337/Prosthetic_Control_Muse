# EEG Prosthetic Control With Muse Headband

1. install required pip packages

   ```
   pip install -r requirements.txt
   ```

2. Open CMD and type the following command into one terminal (make sure bluetooth is on)

   ```
   muselsl stream
   ```

3. Once a Muse Headband is connected, keep the first terminal open.

4. Connect Arduino Uno to computer (script is already uploaded)

5. Connect 4 servos to pins 9, 10, 11, and 12. Heads are already aligned properly.

6. In a new terminal, run the main python file
   ```
   python hand_control.py
   ```
