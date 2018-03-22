import pyb
import gc
from array import array

class Photometry():

    def __init__(self, mode='GCaMP/iso', buffer_size=256, analog_in_1='X5', analog_in_2='X6',
                 digital_in_1='X1', digital_in_2='X2', digital_out_1='X12', digital_out_2='X11'):
        assert mode in ['GCaMP/RFP', 'GCaMP/iso'], \
            "Invalid mode. Mode can be 'GCaMP/RFP' or 'GCaMP/iso'."
        self.mode = mode
        if mode == 'GCaMP/RFP': # 2 channel GFP/RFP acquisition mode.
            self.sampling_rate = 1000    # Hz.
            self.oversampling_rate = 3e5 # Hz.
        elif mode == 'GCaMP/iso': # GCaMP and isosbestic recorded on same channel using time division multiplexing.
            self.sampling_rate = 168        # Hz.
            self.oversampling_rate = 64e3   # Hz.
        self.buffer_size = buffer_size
        self.ADC1 = pyb.ADC(analog_in_1)
        self.ADC2 = pyb.ADC(analog_in_2)
        self.DI1 = pyb.Pin(digital_in_1, pyb.Pin.IN, pyb.Pin.PULL_DOWN)
        self.DI2 = pyb.Pin(digital_in_2, pyb.Pin.IN, pyb.Pin.PULL_DOWN)
        self.DO1 = pyb.Pin(digital_out_1, pyb.Pin.OUT, value=False)
        self.DO2 = pyb.Pin(digital_out_2, pyb.Pin.OUT, value=False)
        self.ovs_buffer = array('H',[0]*64) # Oversampling buffer
        self.ovs_timer = pyb.Timer(2)       # Oversampling timer.
        self.sampling_timer = pyb.Timer(3)
        self.sample_buffers = (array('H',[0]*(buffer_size+2)), array('H',[0]*(buffer_size+2)))
        self.buffer_data_mv = (memoryview(self.sample_buffers[0])[:-2], 
                               memoryview(self.sample_buffers[1])[:-2])
        self.usb_serial = pyb.USB_VCP()

    def start(self):
        #Start acquisition.
        self.write_buffer = 0 # Buffer to write data to.
        self.send_buffer  = 1 # Buffer to send data from.
        self.write_index  = 0 # Buffer index to write new data to. 
        self.buffer_ready = False # Set to True when full buffer is ready to send.
        self.ovs_timer.init(freq=self.oversampling_rate)
        if self.mode == 'GCaMP/RFP':
            self.sampling_timer.init(freq=self.sampling_rate)
            self.sampling_timer.callback(self.gcamp_rfp_ISR)
        elif self.mode == 'GCaMP/iso':
            self.sampling_timer.init(freq=self.sampling_rate*2)
            self.sampling_timer.callback(self.gcamp_iso_ISR)
        gc.disable()

    def stop(self):
        # Stop aquisition
        self.sampling_timer.deinit()
        self.ovs_timer.deinit()
        gc.enable()

    @micropython.native
    def gcamp_rfp_ISR(self, t):
        # Interrupt service routine for GCamp/RFP acquisition mode.
        # Reads a sample from ADCs 1 and 2 sequentially, along with the two digital inputs.
        self.ADC1.read_timed(self.ovs_buffer, self.ovs_timer)
        self.sample_buffers[self.write_buffer][self.write_index] = sum(self.ovs_buffer) >> 3
        if self.DI1.value(): # Store digital input signal in highest bit of sample.
            self.sample_buffers[self.write_buffer][self.write_index] += 0x8000
        self.write_index += 1
        self.ADC2.read_timed(self.ovs_buffer, self.ovs_timer)
        self.sample_buffers[self.write_buffer][self.write_index] = sum(self.ovs_buffer) >> 3
        if self.DI2.value(): 
            self.sample_buffers[self.write_buffer][self.write_index] += 0x8000
        # Update write index and switch buffers if full.
        self.write_index = (self.write_index + 1) % self.buffer_size
        if self.write_index == 0: # Buffer full, switch buffers.
            self.write_buffer = 1 - self.write_buffer
            self.send_buffer  = 1 - self.send_buffer
            self.buffer_ready = True

    @micropython.native
    def gcamp_iso_ISR(self, t):
        # Interrupt service routine for 2 channel GCamp / isosbestic acquisition mode.
        if self.write_index % 2: # Odd samples are isosbestic illumination.
            self.DO2.value(True) # Turn on 405nm illumination.
        else:                    # Even samples are blue illumination.
            self.DO1.value(True) # Turn on 470nm illumination.
        pyb.udelay(350)          # Wait before reading ADC (us).
        # Acquire sample and store in buffer.
        self.ADC1.read_timed(self.ovs_buffer, self.ovs_timer)
        self.sample_buffers[self.write_buffer][self.write_index] = sum(self.ovs_buffer) >> 3
        if self.write_index % 2:
            self.DO2.value(False) # Turn off 405nm illumination.
            if self.DI2.value():  # Store digital input signal in highest bit of sample.
                self.sample_buffers[self.write_buffer][self.write_index] += 0x8000
        else:
            self.DO1.value(False) # Turn on 470nm illumination.
            if self.DI1.value(): # Store digital input signal in highest bit of sample.
                self.sample_buffers[self.write_buffer][self.write_index] += 0x8000
        # Update write index and switch buffers if full.
        self.write_index = (self.write_index + 1) % self.buffer_size
        if self.write_index == 0: # Buffer full, switch buffers.
            self.write_buffer = 1 - self.write_buffer
            self.send_buffer  = 1 - self.send_buffer
            self.buffer_ready = True

    @micropython.native
    def _send_buffer(self):
        # Send full buffer to host computer. Format of the serial chunks sent to the computer: 
        # buffer[:-2] = data, buffer[-2] = checksum, buffer[-1] = 0.
        self.sample_buffers[self.send_buffer][-2] = sum(self.buffer_data_mv[self.send_buffer]) # Checksum
        self.usb_serial.send(self.sample_buffers[self.send_buffer])
        self.buffer_ready = False

    def run(self):
        # Start acquisition, stream data to computer, wait for ctrl+c over serial to stop. 
        self.start()
        try:
            while True:
                if self.buffer_ready:
                    self._send_buffer()
        except KeyboardInterrupt:
            self.stop()