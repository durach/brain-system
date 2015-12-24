import serial
import platform
import glob

class interfaceKEUSB24R():
    buf = ''
    timeout = 0.1
    port_number = 0
    port = False
    lamps = (1, 2, 3, 4)
    relay_states = (0, 1)
    line_count = 16
    relay_count = 4
    io_out_direction = 0
    io_in_direction = 1
    io_directions = (0, 1)

    def __init__(self):
        self.scan()

    def scan(self):

        portnames = self.get_port_names()
        for portname in portnames:
            try:
                self.port = serial.Serial(portname, timeout=self.timeout)
                print "Opened %s" % portname
                self.send_command('$KE')
                answer = self.read_answer()
                if answer == '#OK':
                    self.port_number = portname
                    return True
                else:
                    print "Can't open %s" % portname
                    self.port.close()
            except serial.SerialException:
                pass


        return False

    def is_initialized(self):
        return self.port_number != 0

    def readline(self):
        timeout = 1
        tries = 0
        while 1:
            char = self.port.read(1)
            if char != '':
                tries = 0
                self.buf += char
                pos = self.buf.find('\n')
                if pos >= 0:
                    line, self.buf = self.buf[:pos + 1], self.buf[pos + 1:]
                    return line
            tries += 1
            if tries * self.timeout > timeout:
                break
        line, self.buf = self.buf, ''
        return line

    def send_command(self, text):
        cmd = "%s\r\n" % text
        # print "Sending: '%s'" % text
        self.port.write(cmd)

    def read_answer(self):
        text = self.readline().strip()
        # print "Answer: '%s'" % text
        return text

    def relay_switch(self, relay_no, state):
        if (relay_no in self.lamps) and (state in self.relay_states):
            self.send_command('$KE,REL,%d,%d' % (relay_no, state))
            self.read_answer()

    def relay_turn_on(self, relay_no):
        self.relay_switch(relay_no, 1)

    def relay_turn_off(self, relay_no):
        self.relay_switch(relay_no, 0)

    def config_io(self, in_lines):
        for input in range(1, self.line_count + 1):
            if input in in_lines:
                direction = self.io_in_direction
            else:
                direction = self.io_out_direction

            self.io_set_direction(input, direction)

    def io_set_direction(self, line, direction):
        if (direction in self.io_directions) and (1 <= line <= self.line_count):
            self.send_command('$KE,IO,SET,%d,%d' % (line, direction))
            self.read_answer()

    def get_inputs_state(self):
        self.send_command('$KE,RD,ALL')
        self.read_answer()

    def get_port_names(self):
        platform_name = platform.system()
        if platform_name == "Darwin" or platform_name == "Linux":
            return glob.glob("/dev/tty.usbmodem*")
        elif platform_name == "Windows":
            return range(6, 20)
        else:
            raise Exception("Not supported platform")
