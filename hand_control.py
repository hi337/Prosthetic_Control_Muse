import numpy as np  # Module that simplifies computations on matrices
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import utils  # Our own utility functions
import serial  # Module for serial communication with Arduino
import time

class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3

# EXPERIMENTAL PARAMETERS
BUFFER_LENGTH = 5
EPOCH_LENGTH = 1
OVERLAP_LENGTH = 0.8
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH
INDEX_CHANNEL = 3

if __name__ == "__main__":

    # Connect to EEG stream
    print('Looking for an EEG stream...')
    streams = resolve_byprop('type', 'EEG', timeout=2)
    if len(streams) == 0:
        raise RuntimeError('Can\'t find EEG stream.')

    print("Start acquiring data")
    inlet = StreamInlet(streams[0], max_chunklen=12)
    eeg_time_correction = inlet.time_correction()
    info = inlet.info()
    fs = int(info.nominal_srate())

    # Initialize buffers
    eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
    filter_state = None
    n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) / SHIFT_LENGTH + 1))
    band_buffer = np.zeros((n_win_test, 4))

    # Initialize serial connection to Arduino
    ser = serial.Serial('COM3', 9600)  # Adjust the COM port based on your setup
    time.sleep(2)  # Give some time for the connection to establish

    print('Press Ctrl-C in the console to break the while loop.')
    allValues = [0]
    try:
        while True:
            value = 0
            # Acquire EEG data
            eeg_data, timestamp = inlet.pull_chunk(timeout=1, max_samples=int(SHIFT_LENGTH * fs))
            ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]

            # Update buffer
            eeg_buffer, filter_state = utils.update_buffer(eeg_buffer, ch_data, notch=True, filter_state=filter_state)

            # Compute band powers
            data_epoch = utils.get_last_data(eeg_buffer, EPOCH_LENGTH * fs)
            band_powers = utils.compute_band_powers(data_epoch, fs)
            band_buffer, _ = utils.update_buffer(band_buffer, np.asarray([band_powers]))
            smooth_band_powers = np.mean(band_buffer, axis=0)
            allValues.append(band_powers[Band.Delta])
            deltaWaves = band_powers[Band.Delta]
            print("Delta: {}".format(deltaWaves))

            # Blink detection logic
            if deltaWaves >= 1 and allValues[-2] <= 1:
                print("Blink detected!")
                ser.write(b'B')  # Send 'B' to Arduino to indicate a blink
            elif deltaWaves >= 1.65 and (deltaWaves - allValues[-2]) >= 0.15:
                print("Blink detected!")
                ser.write(b'B')  # Send 'B' to Arduino to indicate a blink
    except KeyboardInterrupt:
        ser.close()
        print('Closing!')
