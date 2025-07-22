"""
This program has you input the parameters of your experiment and
will then store the data with the appropriate headline in the
selected repository. The program will save points in the following
manner:

Output_Voltage  Readback  DMM_Readback  Counts

Use the program data_analysis to read your results

link for the DMM manual: https://www.keysight.com/ca/en/assets/9018-03876/service-manuals/9018-03876.pdf?success=true
link for the SR400 manual: https://thinksrs.com/downloads/pdfs/manuals/SR400m.pdf

Developed by Mathias Roman (2022) and Aryan Prasad (2023) for Laser Applications @ TRIUMF.
"""

####################################################################################################################

from __future__ import absolute_import, division, print_function

import unicodecsv as csv
from datetime import datetime, date
import time
import socket
import serial
import os
from decimal import Decimal
from ctypes import *
import multiprocessing
import threading
import queue

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from builtins import *
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.ttk import Combobox

# from mcculw import ul
# from mcculw.device_info import DaqDeviceInfo
# from mcculw.ul import ULError

# EPICS pvapy
from pvaccess import *

try:
    from ui_examples_util import UIExample, show_ul_error, validate_float_entry, validate_positive_int_entry
except ImportError:
    from .ui_examples_util import UIExample, show_ul_error, validate_float_entry, validate_positive_int_entry

font = {'family': 'normal', 'weight': 'normal', 'size': 12}


class CLS_Scan(UIExample):

    def __init__(self, master, giver, scan_on, epics_queue):
        # connects to the DAQ and outputs 0V
        super(CLS_Scan, self).__init__(master)
        use_device_detection = True
        # self.board_num = 0
        self.scan_running = False
        self.scan_paused = False
        self.ao_set = 0.0
        self.giver = giver
        self.scanning = scan_on

        # epics value queue
        self.epicsQueue = epics_queue

        # epics channel access for freq, power
        #self.epics_freq = Channel('ISOL-CLS:LSR-WM:GetFreq', CA)
        #self.epics_power = Channel('ISOL-CLS:LSR-WM:GetPower', CA)
        self.epics_value = Channel('WM:GetMeas')
        slef.epics_dmm = Channel('ISOL-CLS:DMM')
        # Trigger variable
        # self.trigQueue = trig_queue
        # self.triggering = trig_on

        # creates the UI if proper conditions are met
        # try:
            # if use_device_detection:
                # self.configure_first_detected_device()

            # self.device_info = DaqDeviceInfo(self.board_num)
            # self.ctr_info = self.device_info.get_ctr_info()
            # self.ao_info = self.device_info.get_ao_info()
            # if self.ctr_info.is_supported:
            #     if self.device_info.supports_analog_input:
            #         self.ai_info = self.device_info.get_ai_info()
            #         if self.ao_info.is_supported and self.ao_info.supports_v_out:
            #             self.create_widgets()
            #         else:
            #             self.create_unsupported_widgets()
            #     else:
            #         self.create_unsupported_widgets()
            # else:
            #     self.create_unsupported_widgets()

        self.create_widgets()

        self.giver.put("GUI Created!")
            # self.trigQueue.put(self.board_num)

        # except ULError:
            # self.create_unsupported_widgets(True)

    #########################################################################

    def scan(self):
        cycle = int(self.scan_cycle_value) + 1
        progress_value = 0
        self.start_time = time.time()  # Record the start time

        # loop for the number of cycles
        for j in range(1, cycle):
            if j > 1:
                # informs the plot process of cycles
                self.giver.put(j)
            if self.scan_running:
                self.ao_set = self.scan_start
                # ul.v_out(self.board_num, self.channel_ao, self.ao_range, self.ao_set)
                command = "CLS:SetVolt"
                voltage = self.scan_start
                message = f"{command} {voltage}\r\n"
                client_socket.send(message.encode())

                self.cycle_status_label["text"] = "Current cycle #:     " + str(j)

                # Determine the condition for the while loop
                if self.scan_start == self.scan_stop:
                    # When start and stop are equal, we need at least one iteration
                    condition = True
                elif self.scan_start > self.scan_stop:
                    condition = (self.ao_set >= (self.scan_stop - 1E-6))
                else:
                    condition = (self.ao_set <= (self.scan_stop + 1E-6))

                # if self.MCA4_status == 1:
                #     # Start a scan for the MCA4
                #     # erase the data to prepare for the next set
                #     string = 'erase'
                #     string = string.encode('utf-8')
                #     self.mca4DLL.RunCmd(0, string)
                #     # starts the acquisition
                #     string = 'start'
                #     string = string.encode('utf-8')
                #     self.mca4DLL.RunCmd(0, string)
                #     time.sleep(2)

                trigger = self.trig_mode

                # loop for the steps
                while condition and self.scan_running:
                    # Set AO voltage
                    # ul.v_out(self.board_num, self.channel_ao, self.ao_range, self.ao_set)
                    command = "CLS:SetVolt"
                    voltage = self.ao_set
                    message = f"{command} {voltage}\r\n"
                    client_socket.send(message.encode())
                    # if self.MCA4_status == 1:
                    #     ul.v_out(self.board_num, 1, self.ao_range, 5)
                    #     '''opens the gate for the laser pulses'''

                    # Reset counters at the start of dwell time
                    # if self.DAQ_status == 1:
                    #     ul.c_clear(self.board_num, self.channel_ct)
                    message = "CLS:SetClear\r\n"
                    client_socket.send(message.encode())

                    # if self.SR400_status == 1:
                    #     # Reset and start the SR400
                    #     self.SR400.write(b'CR\n')
                    #     self.SR400.write(b'CS\n')

                    # Start time for dwell period
                    dwell_start_time = time.time()

                    # Sleep for the dwell time
                    time.sleep(self.scan_dwell_time / 1000.0)  # Convert ms to seconds

                    # if self.MCA4_status == 1:
                    #     ul.v_out(self.board_num, 1, self.ao_range, 0)
                    #     '''closes the gate for the laser pulses'''

                    # Read counts after dwell time
                    value_ct = 0  # Initialize counts
                 
#                    if self.DAQ_status == 1:
#                        value_ct += ul.c_in_32(self.board_num, self.channel_ct)
                     message = "CLS:GetCount\r\n"
                     value_ct += client_socket.send(message.encode())
#                    if self.SR400_status == 1:
                        # Read counts from the SR400
#                        self.SR400.write(b'QA\n')
#                        countA = int(self.SR400.read(size=100).decode("ascii").strip())
##                        self.SR400.write(b'QB\n')
#                        countB = int(self.SR400.read(size=100).decode("ascii").strip())
#                        value_ct += (countA + countB)

                    # Get a voltage value from the DAQ
#                    if self.ai_info.resolution <= 16:
                        # Use the a_in method for devices with a resolution <= 16
                        # Convert the raw value to engineering units
#                        eng_units_value = self.ai_to_eng_units(
#                            ul.a_in(self.board_num, self.channel_ai, self.ai_range),
#                            self.ai_range, self.ai_info.resolution)

#                    else:
                        # Use the a_in_32 method for devices with a resolution > 16
                        # Convert the raw value to engineering units
#                        eng_units_value = self.ai_to_eng_units(
#                            ul.a_in_32(self.board_num, self.channel_ai, self.ai_range), self.ai_range,
#                            self.ai_info.resolution)
                    eng_units_value = self.epics_dmm.get()

                    # Get a value from the DMM if the box was checked
#                    if self.DMM_status == 1:
#                        self.DMM.sendall(b'MEAS:VOLT:DC? 10,0.0001\r\n')
#                        time.sleep(0.05)
#                        DMM_response = self.DMM.recv(1000).decode().strip()
#                        try:
#                            DMM_readback = float(DMM_response)
#                            self.DMM_readback_value["text"] = '{:.3f}'.format(DMM_readback)
#                        except ValueError:
#                            print("DMM reading error occurred at voltage " + str(self.ao_set) + " of cycle " + str(
#                                j) + ".")
#                            DMM_readback = 0
#                    else:
#                        DMM_readback = 0
                    
                    self.value_ct["text"] = str(value_ct)  # display counts
                    self.eng_value["text"] = '{:.3f}'.format(eng_units_value)  # display AI value
                    self.data_ao_value["text"] = '{:.3f}'.format(self.ao_set)  # display current step
                    # Calculate elapsed time
                    current_time = time.time() - self.start_time

                    # Update EPICS pva value
                    self.epicsQueue.put(value_ct)
                    # freq_value = dict(self.epics_freq.get('field(value)'))['value']
                    # power_value = dict(self.epics_power.get('field(value)'))['value']
                    freq_value = dict(self.epics_value.get())['freq']
                    power_value = dict(self.epics_value.get())['power']

                    # self.pv['value'] = int(value_ct)
                    
                    #bitin = ul.d_bit_in(self.board_num, 1, 7)
                    #print("DI :", bitin)

                    # Saves the data
                    data = [self.ao_set, eng_units_value, DMM_readback, value_ct, current_time, freq_value, power_value]

                    self.update()

                    if not self.scan_paused:
                        if self.scan_running:
                            try:
                                with open(self.dir_path, 'ab') as csv_file:
                                    writer = csv.writer(csv_file, delimiter='\t')
                                    writer.writerow(data)
                            except ULError as e:
                                show_ul_error(e)

                        # updates the while loop's condition (type casting required for exact arithmetic)
                        if self.scan_start != self.scan_stop:
                            self.ao_set = Decimal(str(self.ao_set)) + Decimal(str(self.scan_step_size))
                            if self.scan_start > self.scan_stop:
                                condition = self.ao_set >= (self.scan_stop - 1E-6)
                            else:
                                condition = self.ao_set <= (self.scan_stop + 1E-6)
                        else:
                            # If start == stop, we only want one iteration
                            condition = False

                        # updates the progress bar
                        progress_value += self.progress_step
                        if self.pb["value"] <= 100:
                            self.pb["value"] = progress_value

                        # sends the data to the plotting process
                        self.giver.put(data)

                    self.update()

                try:
                    with open(self.dir_path, 'ab') as csv_file:
                        writer = csv.writer(csv_file, delimiter='\t')
                        writer.writerow(['*', '*', '*', '*', '*', '*'])
                except ULError as e:
                    show_ul_error(e)

                if self.MCA4_status == 1:
                    string = 'halt'
                    string = string.encode('utf-8')
                    self.mca4DLL.RunCmd(0, string)

        # makes the progress bar full
        self.pb["value"] = 100
        csv_file.close()

        self.giver.put("Done")

        self.stop_scan()

    #########################################################################

    def stop_scan(self):
        # turn the scanning status off
        self.scanning.clear()
        # informs the plot process to clear the queue and plot the totality of the data
        self.giver.put(None)
        if self.pause_scan_button:
            self.resume_scan()
        # enables the modification of parameters
        # self.range_ai_combobox['state'] = 'readonly'
        # self.range_ao_combobox['state'] = 'readonly'
        # self.channel_ao_entry['state'] = 'normal'
        # self.channel_ai_entry['state'] = 'normal'
        # self.channel_ct_entry['state'] = 'normal'
        self.start_scan_button["text"] = "Start scan"
        self.start_scan_button["command"] = self.scan_manager
        self.scan_start_entry['state'] = 'normal'
        self.scan_stop_entry['state'] = 'normal'
        self.scan_cycle_entry['state'] = 'normal'
        self.scan_step_size_entry['state'] = 'normal'
        self.scan_dwell_time_entry['state'] = 'normal'
        self.scan_status_label["text"] = "Not scanning"
        self.scan_status_label["fg"] = "red"
        self.mass_entry['state'] = 'normal'
        self.element_entry['state'] = 'normal'
        self.wavenumber_entry['state'] = 'normal'
        self.beam_energy_entry['state'] = 'normal'
        self.collinear_combobox['state'] = 'readonly'
        # self.headline['state'] = 'normal'
        self.change_button['state'] = 'normal'
        self.dir_entry['state'] = 'normal'
        self.file_entry['state'] = 'normal'
        # self.DMM_checkbox["state"] = "normal"
        # self.SR400_checkbox["state"] = "normal"
        # self.DAQ_checkbox["state"] = "normal"
        # self.MCA4_checkbox['state'] = 'normal'
        self.new_outfile_checkbox['state'] = 'normal'

        self.trigdelay_entry['state'] = 'normal'
        self.trigmode_checkbox['state'] = 'normal'
        self.trigfreq_entry['state'] = 'normal'
        self.trigwidth_entry['state'] = 'normal'


        # Sets the output voltage back to 0
        # ul.v_out(self.board_num, self.channel_ao, self.ao_range, 0)
        # self.data_ao_value["text"] = '{:.3f}'.format(0)
        # self.eng_value["text"] = '{:.3f}'.format(0)
        # self.DMM_readback_value["text"] = '{:.3f}'.format(0)

        # closes connection to exterior device
        # if self.DMM_status == 1:
        #     try:
        #         self.DMM.close()
        #     except Exception:
        #         self.DMM_status = 0
        # if self.SR400_status == 1:
        #     try:
        #         self.SR400.close()
        #     except Exception:
        #         self.SR400_status = 0
        self.scan_running = False
        self.update()

    def hard_stop_scan(self):
        self.loop_checkbox.deselect()
        self.stop_scan()

    #########################################################################

    def start_scan(self):
        # gets the value of necessary parameters
        # self.channel_ai = self.get_channel_num_ai()
        # self.ai_range = self.get_ai_range()
        # self.channel_ct = self.get_channel_num_ct()
        # self.channel_ao = self.get_channel_num_ao()
        # self.ao_range = self.get_ao_range()
        self.scan_start = self.get_scan_start_value()
        self.scan_stop = self.get_scan_stop_value()
        self.scan_step_size = self.get_scan_step_size_value()
        self.scan_dwell_time = self.get_scan_dwell_time_value()
        self.scan_cycle_value = self.get_scan_cycle_value()
        self.mass = self.get_mass_value()
        self.wavenumber = self.get_wavenumber_value()
        self.beam_energy = self.get_beam_energy_value()
        # self.DAQ_status = self.get_DAQ()
        # self.DMM_status = self.get_DMM()
        # self.SR400_status = self.get_SR400()
        # self.MCA4_status = self.get_MCA4()

        self.trig_delay = self.get_trig_delay_value()
        self.trig_mode = self.get_trig_mode()
        self.trig_freq = self.get_trig_freq_value()
        self.trig_width = self.get_trig_width_value()

        # Verifies if the inputs are valid
        if self.scan_start > 10 or self.scan_start < -10 or self.scan_stop > 10 or self.scan_stop < -10:
            messagebox.showerror("Invalid Range", "Voltages must be kept in [-10 V, 10 V].")
            return
        if self.mass == 0:
            messagebox.showerror("Invalid Isotope", "The isotope you entered (mass number and element) was not found.")
            return
        if self.scan_start != self.scan_stop:
            if self.scan_start + self.scan_step_size > 10 or self.scan_start - self.scan_step_size < -10:
                messagebox.showerror("Invalid Input", "Step size is too large!")
                return
            if self.scan_step_size == 0:
                messagebox.showerror("Invalid Input", "Step size must be greater than zero.")
                return
        else:
            # When start equals stop, we allow step size of zero
            self.scan_step_size = 0
        if self.DAQ_status == 0 and self.SR400_status == 0:
            messagebox.showerror("Invalid Input", "Please select at least one counter.")
            return
        # scan can only begin if there are no parameter errors
        self.scanning.set()

        # prevents modification of parameters mid-scan
        self.range_ai_combobox['state'] = 'disabled'
        self.range_ao_combobox['state'] = 'disabled'
        self.channel_ao_entry['state'] = 'disabled'
        self.channel_ai_entry['state'] = 'disabled'
        self.channel_ct_entry['state'] = 'disabled'

        self.start_scan_button["text"] = "Stop scan"
        self.start_scan_button["command"] = self.hard_stop_scan
        self.scan_running = True
        self.scan_status_label["text"] = "Scanning"
        self.scan_status_label["fg"] = "green"

        self.scan_start_entry['state'] = 'disabled'
        self.scan_stop_entry['state'] = 'disabled'
        self.scan_cycle_entry['state'] = 'disabled'
        self.scan_step_size_entry['state'] = 'disabled'
        self.scan_dwell_time_entry['state'] = 'disabled'
        self.mass_entry['state'] = 'disabled'
        self.element_entry['state'] = 'disabled'
        self.wavenumber_entry['state'] = 'disabled'
        self.beam_energy_entry['state'] = 'disabled'
        self.collinear_combobox['state'] = 'disabled'
        # self.headline['state'] = 'disabled'
        self.change_button['state'] = 'disabled'
        self.dir_entry['state'] = 'disabled'
        self.file_entry['state'] = 'disabled'
        self.DMM_checkbox["state"] = "disabled"
        self.SR400_checkbox["state"] = "disabled"
        self.DAQ_checkbox["state"] = "disabled"
        self.MCA4_checkbox['state'] = 'disabled'
        self.new_outfile_checkbox['state'] = 'disabled'

        self.trigdelay_entry['state'] = 'disabled'
        self.trigmode_checkbox['state'] = 'disabled'
        self.trigfreq_entry['state'] = 'disabled'
        self.trigwidth_entry['state'] = 'disabled'
          
        # makes sure the steps are in the right direction
        if self.scan_start != self.scan_stop:
            if self.scan_start > self.scan_stop and self.scan_step_size > 0:
                self.scan_step_size = -1.0 * self.scan_step_size
            elif self.scan_start < self.scan_stop and self.scan_step_size < 0:
                self.scan_step_size = -1.0 * self.scan_step_size

        # resets the progress bar and set its step size
        self.pb["value"] = 0
        if self.scan_start != self.scan_stop:
            self.number_step = abs((self.scan_stop - self.scan_start) * self.scan_cycle_value / self.scan_step_size)
        else:
            # When start equals stop, we have one step per cycle
            self.number_step = self.scan_cycle_value
        self.progress_step = 100 / self.number_step

        self.dir_path = self.dir_entry.get() + '/' + self.file_entry.get()
        if self.var_newout.get():
            now = datetime.now()
            self.dir_path += ' ' + now.strftime("%H{0}%M{0}%S").format(*'\uA789')

        # opens connections with exterior devices
        if self.DMM_status == 1:
            try:
                # opens the connection with the DMM
                host = "169.254.114.102"  # To find the IP address, see DMM manual
                port = 5024  # The DMM always uses port 5024
                self.DMM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.DMM.connect((host, port))
                # sets the input impedance to auto (resulting in High Z for normal voltage ranges)
                # self.DMM.sendall(b'SENT: VOLT:IMP:AUTO ON \r\n')
            except Exception:
                self.DMM_status = 0
                self.DMM_checkbox.deselect()
                messagebox.showerror("Error", "Connection with the DMM has failed")
                self.stop_scan()

        if self.SR400_status == 1:
            try:
                # opens the connection with the SR400 and sends the command for the setup
                # list of all the commands to send for setup
                """
                equivalence table:
                A=0
                B=1
                T=2
                """
                cmd = []

                # sets the step duration to the dwell_time
                cmd.append("CP2," + str(self.scan_dwell_time * 1E4))

                # sets the discriminator level for input A and B
                cmd.append("DL0,-0.075;DL1,-0.075")

                # opens the serial connection (change com port)
                self.SR400 = serial.Serial(port='COM4', baudrate=9600)
                self.SR400.setDTR(True)

                # sends all the command for the setup
                for x in cmd:
                    x = bytes(x, "ascii") + b'\n'
                    self.SR400.write(x)
            except Exception:
                self.SR400_status = 0
                self.SR400_checkbox.deselect()
                messagebox.showerror("Error", "Connection with the SR400 has failed")
                self.stop_scan()

        if self.MCA4_status == 1:
            string = 'cycles=' + str(int(self.number_step + 0.1))
            string = string.encode('utf-8')
            self.mca4DLL.RunCmd(0, string)

            self.period = 0.1  # corresponds to 100us in ms

            string = 'swpreset=' + str(self.scan_dwell_time / self.period)
            string = string.encode('utf-8')
            self.mca4DLL.RunCmd(0, string)

        # writes the headline of the csv file
        time_now = datetime.now()
        # headline = self.get_headline()
        lin = self.collinear_combobox.get()
        mass = "Mass: " + str(self.mass)
        isotope = 'Isotope: ' + str(self.element) + str(self.mass_number)
        wavenumber = "Wavenumber: " + str(self.wavenumber) + " cm\u207B\u00B9"
        beam_energy = "Beam energy: " + str(self.beam_energy) + " eV"
        scan_start = "Scan Start: " + str(self.scan_start) + " V"
        scan_stop = "Scan Stop: " + str(self.scan_stop) + " V"
        scan_step_size = "Scan Step Size: " + str(self.scan_step_size) + " V"
        scan_dwell_time = "Scan Dwell time: " + str(self.scan_dwell_time) + " ms"

        try:
            with open(self.dir_path, 'ab') as csv_file:
                writer = csv.writer(csv_file, encoding='utf-8', delimiter='\t')
                # writer.writerow([time_now, isotope, mass, wavenumber, beam_energy, lin, headline])
                writer.writerow([time_now, isotope, mass, wavenumber, beam_energy, lin])
                writer.writerow([scan_start, scan_stop, scan_step_size, scan_dwell_time])
                writer.writerow(['AOut (V)', 'AIn (V)', 'DMM Read (V)', 'Ion/Photon Count', 'Time (s)', 'Frequency(THz)', 'Power(mW)'])
        except ULError as e:
            show_ul_error(e)
        self.update()
        self.scan()

    def scan_manager(self):
        while True:
            self.start_scan()
            if not self.var_loop.get():
                break

    #########################################################################

    # functions used in the start, scan and stop functions
    @staticmethod
    def ai_to_eng_units(raw_value, ai_range, resolution):
        full_scale_volts = ai_range.range_max - ai_range.range_min
        full_scale_count = (2 ** resolution) - 1
        return ((full_scale_volts / full_scale_count) * raw_value
                + ai_range.range_min)

    def get_scan_start_value(self):
        try:
            return float(self.scan_start_entry.get())
        except ValueError:
            return 0

    def get_scan_stop_value(self):
        try:
            return float(self.scan_stop_entry.get())
        except ValueError:
            return 0

    def get_scan_step_size_value(self):
        try:
            value = self.scan_step_size_entry.get()
            y = ""
            for x in value:
                if x == " ":
                    break
                y += x
            return float(y)
        except ValueError:
            return 0

    def get_scan_dwell_time_value(self):
        try:
            return int(self.scan_dwell_time_entry.get())
        except ValueError:
            return 0

    def get_scan_cycle_value(self):
        try:
            return int(self.scan_cycle_entry.get())
        except ValueError:
            return 0

    def get_headline(self):
        try:
            return str(self.headline.get())
        except ValueError:
            return ""

    def get_mass_value(self):
        try:
            m = str(self.mass_entry.get())
            n = str(self.element_entry.get())
            file = open('isotope.csv', 'rb')
            rows = []
            csvreader = csv.reader(file, encoding='utf-8')
            for row in csvreader:
                rows.append(row)
            for row in rows:
                if row[0] == m:
                    if row[1] == n:
                        self.element = row[1]
                        self.mass_number = row[0]
                        return float(row[2])
            return 0
        except Exception:
            return 0

    def get_wavenumber_value(self):
        try:
            return float(self.wavenumber_entry.get())
        except ValueError:
            return 0

    def get_beam_energy_value(self):
        try:
            return float(self.beam_energy_entry.get())
        except ValueError:
            return 0

    def get_channel_num_ai(self):
        if self.ai_info.num_chans == 1:
            return 0
        try:
            return int(self.channel_ai_entry.get())
        except ValueError:
            return 0

    def get_channel_num_ao(self):
        if self.ao_info.num_chans == 1:
            return 0
        try:
            return int(self.channel_ao_entry.get())
        except ValueError:
            return 0

    def get_channel_num_ct(self):
        if self.ctr_info.num_chans == 1:
            return self.ctr_info.chan_info[0].channel_num
        try:
            return int(self.channel_ct_entry.get())
        except ValueError:
            return 0

    def get_ai_range(self):
        selected_index = self.range_ai_combobox.current()
        return self.ai_info.supported_ranges[selected_index]

    def get_ao_range(self):
        selected_index = self.range_ao_combobox.current()
        return self.ao_info.supported_ranges[selected_index]

    def get_scan_start(self):
        if self.ai_info.num_chans == 1:
            return 0
        try:
            return int(self.channel_ai_entry.get())
        except ValueError:
            return 0

    def get_DMM(self):
        try:
            return self.var_DMM.get()
        except ValueError:
            return 0

    def get_DAQ(self):
        try:
            return self.var_DAQ.get()
        except ValueError:
            return 0

    def get_SR400(self):
        try:
            return self.var_SR400.get()
        except ValueError:
            return 0

    def get_MCA4(self):
        try:
            return self.var_MCA4.get()
        except ValueError:
            return 0

    def get_trig_delay_value(self):
        try:
            return float(self.trigdelay_entry.get())
        except ValueError:
            return 0

    def get_trig_mode(self):
        try:
            return self.var_trigmode.get()
        except ValueError:
            return 0

    def get_trig_freq_value(self):
        try:
            return float(self.trigfreq_entry.get())
        except ValueError:
            return 0

    def get_trig_width_value(self):
        try:
            return float(self.trigwidth_entry.get())
        except ValueError:
            return 0
    #########################################################################

    def pause_scan(self):
        if self.scan_running:
            self.scan_paused = True
            self.giver.put("Paused")
            self.scan_status_label["text"] = "Scan is paused"
            self.scan_status_label["fg"] = "red"

            self.pause_scan_button["text"] = "Resume scan"
            self.pause_scan_button["command"] = self.resume_scan
        else:
            messagebox.showerror("Error", "No scan is running")

    def resume_scan(self):
        if self.scan_running:
            self.scan_paused = False
            self.giver.put("Resumed")
            self.scan_status_label["text"] = "Scanning"
            self.scan_status_label["fg"] = "green"

            self.pause_scan_button["text"] = "Pause scan"
            self.pause_scan_button["command"] = self.pause_scan

    #########################################################################

    def validate_channel_ai_entry(self, p):
        if p == '':
            return True
        try:
            value = int(p)
            if value < 0 or value > self.ai_info.num_chans - 1:
                return False
        except ValueError:
            return False

        return True

    def validate_channel_ct_entry(self, p):
        if p == '':
            return True
        try:
            value = int(p)
            if value < 0 or value > self.ctr_info.num_chans - 1:
                return False
        except ValueError:
            return False

        return True

    def validate_channel_ao_entry(self, p):
        if p == '':
            return True
        try:
            value = int(p)
            if value < 0 or value > self.ao_info.num_chans - 1:
                return False
        except ValueError:
            return False

        return True

    @staticmethod
    def validate_string(p):
        """Determines whether a string (intended to represent an atomic element) is a number or not
        by catching an exception thrown when attempting to convert to a float
        """
        if p == '':
            return True
        try:
            value = float(p)
            return False
        except ValueError:
            return True

    def switch_DAQ(self):
        self.DAQ_checkbox.deselect()

    def switch_SR400(self):
        self.SR400_checkbox.deselect()

    def activate_MCA4(self):
        try:
            self.MCA4_status = self.get_MCA4()
            if self.MCA4_status == 1:
                self.mca4DLL = CDLL('dmca4')
                self.mca4DLL.RunCmd.argtypes = [c_int, c_char_p]
                self.mca4DLL.RunCmd.restype = c_int
                # opens the connection with the MCA4 and sends the commands for the setup
                cmd = []

                # sets the mode to multichannel scaling with multiple cycles
                cmd.append('mcsmode=5')

                # sets the dwelltime to 30ns
                '''self.bin_size=self.get_bin_size()'''
                self.bin_size = 3
                cmd.append('dwellunit=0')
                cmd.append('dwelltime=' + str(self.bin_size))

                # sets the saving parameters
                cmd.append('mpafmt=csv')
                cmd.append('savedata=1')
                cmd.append('[MCS1]')
                cmd.append('mpaname=' + self.name + '_MCA')
                cmd.append('autoinc=1')

                # sets the mode to sweep preset
                cmd.append('pr_ena=4')

                # sets the range and ROI presets
                cmd.append('[MCS1]')
                '''self.range=self.get_range()'''
                self.range = 2048  # the period for one cycle must be shorter than that of the laser pulses
                cmd.append('range=' + str(self.range))

                for string in cmd:
                    string = string.encode('utf-8')
                    self.mca4DLL.RunCmd(0, string)
                    time.sleep(0.1)
        except Exception:
            self.MCA4_status = 0
            self.MCA4_checkbox.deselect()
            messagebox.showerror("Error", "Connection with the MCA4 has failed")
            self.stop_scan()

    #########################################################################

    def change_dir(self):
        indir = filedialog.askdirectory(parent=self, initialdir=os.getcwd(), title='Input Folder')
        indir = str(indir)
        if indir == "":
            return
        dir_path = os.path.dirname(indir)
        self.dir_entry.delete(0, 'end')
        self.dir_entry.insert(0, dir_path)

    #########################################################################

    def create_widgets(self):
        """Create the tkinter UI"""

        self.option_add("*Font", "Helvetica 10")

        # Top band

        device_frame = tk.Frame(self, relief='sunken', borderwidth=3)
        device_frame.pack(anchor=tk.NW, fill=tk.X, padx=3, pady=4)

        self.device_label = tk.Label(device_frame, fg="red")
        self.device_label.grid(row=0, column=0, padx=3, pady=4)
        # # self.device_label.pack(fill=tk.NONE, anchor=tk.NW)
        # self.device_label["text"] = ('MCC Board Number ' + str(self.board_num)
        #                              + "    " + self.device_info.product_name
        #                              + " (" + self.device_info.unique_id + ")     AI resolution: "
        #                              + str(self.ai_info.resolution) +
        #                              "      AO resolution: " + str(self.ao_info.resolution))
        self.device_label["text"] = ('FPGA Board IP: 192.168.150.215')

        # quit button
        quit_button = tk.Button(device_frame)
        quit_button["text"] = "Quit Program"
        quit_button["command"] = self.master.destroy
        quit_button.grid(row=0, column=3, padx=20, pady=4)

        ##################################################################

        # Device and channel selection

        channel_frame = tk.Frame(self, relief='sunken', borderwidth=3)
        channel_frame.pack(anchor=tk.NW, padx=3, pady=5)

        # channel_vcmd_ao = self.register(self.validate_channel_ao_entry)
        # self.ao_set = 0

        # if self.ao_info.num_chans > 1:
            # channel_ao_entry_label = tk.Label(channel_frame)
            # channel_ao_entry_label["text"] = "MCC Analog Output Ch #:"
            # channel_ao_entry_label.grid(row=0, column=0, sticky=tk.W, padx=3, pady=10)

            # self.channel_ao_entry = tk.Spinbox(
            #     channel_frame, from_=0, to=max(self.ao_info.num_chans - 1, 0),
            #     validate='key', validatecommand=(channel_vcmd_ao, '%P'), width=3)
            # self.channel_ao_entry.grid(row=0, column=1, sticky=tk.E)

        # range_ao_label = tk.Label(channel_frame)
        # range_ao_label["text"] = "Range:"
        # range_ao_label.grid(row=1, column=0, sticky=tk.W)

        # self.range_ao_combobox = Combobox(channel_frame, width=12)
        # self.range_ao_combobox["state"] = "readonly"
        # self.range_ao_combobox["values"] = [
        #     x.name for x in self.ao_info.supported_ranges]
        # self.range_ao_combobox.current(0)  # choose default value of 0, +-10V
        # self.range_ao_combobox.grid(row=1, column=1, sticky=tk.E, padx=3, pady=6)

        # channel_vcmd_ai = self.register(self.validate_channel_ai_entry)
        # if self.ai_info.num_chans > 1:
        #     channel_ai_entry_label = tk.Label(channel_frame)
        #     channel_ai_entry_label["text"] = "MCC Analog Input Ch #:   "
        #     channel_ai_entry_label.grid(row=3, column=0, sticky=tk.W, padx=3, pady=3)

        #     self.channel_ai_entry = tk.Spinbox(channel_frame, from_=0, to=max(self.ai_info.num_chans - 1, 0),
        #                                        validate='key', validatecommand=(channel_vcmd_ai, '%P'), width=3)
        #     self.channel_ai_entry.grid(row=3, column=1, sticky=tk.E, padx=3, pady=3)

        # range_ai_label = tk.Label(channel_frame)
        # range_ai_label["text"] = "Range:"
        # range_ai_label.grid(row=4, column=0, sticky=tk.W, padx=3, pady=3)

        # self.range_ai_combobox = Combobox(channel_frame, width=12)
        # self.range_ai_combobox["state"] = "readonly"
        # self.range_ai_combobox["values"] = [
        #     x.name for x in self.ai_info.supported_ranges]
        # self.range_ai_combobox.current(1)  # choose default value of 1, +-10V
        # self.range_ai_combobox.grid(row=4, column=1, sticky=tk.E, padx=3, pady=3)

        # channel_vcmd_ct = self.register(self.validate_channel_ct_entry)

        # if self.ctr_info.num_chans > 1:
        #     channel_ct_entry_label = tk.Label(channel_frame)
        #     channel_ct_entry_label["text"] = "Counter Ch #:"
        #     channel_ct_entry_label.grid(
        #         row=7, column=0, sticky=tk.W, padx=3, pady=3)

        #     chan_info_list = self.ctr_info.chan_info
        #     first_chan = chan_info_list[0].channel_num
        #     last_chan = first_chan
        #     for chan_info in chan_info_list:
        #         if chan_info.channel_num >= last_chan:
        #             last_chan = chan_info.channel_num
        #         else:
        #             break
        #     self.channel_ct_entry = tk.Spinbox(
        #         channel_frame, from_=first_chan, to=last_chan,
        #         validate='key', validatecommand=(channel_vcmd_ct, '%P'), width=3)
        #     self.channel_ct_entry.grid(row=7, column=0, sticky=tk.E, padx=3, pady=3)

        # # DMM checkbox
        # self.var_DMM = tk.IntVar()
        # self.DMM_checkbox = tk.Checkbutton(channel_frame, text='Enable DMM', var=self.var_DMM, onvalue=1, offvalue=0)
        # self.DMM_checkbox.grid(row=5, column=1, sticky=tk.W, padx=3, pady=3)

        # # DAQ checkbox
        # self.var_DAQ = tk.IntVar()
        # self.DAQ_checkbox = tk.Checkbutton(channel_frame, text='Enable DAQ', var=self.var_DAQ, onvalue=1, offvalue=0,
        #                                    command=self.switch_SR400)
        # self.DAQ_checkbox.grid(row=7, column=1, sticky=tk.W, padx=3, pady=3)
        # self.DAQ_checkbox.select()

        # # SR400 checkbox
        # self.var_SR400 = tk.IntVar()
        # self.SR400_checkbox = tk.Checkbutton(channel_frame, text='Enable SR400', var=self.var_SR400, onvalue=1,
        #                                      offvalue=0, command=self.switch_DAQ)
        # self.SR400_checkbox.grid(row=8, column=1, sticky=tk.W, padx=3, pady=3)

        # # MCA4 checkbox
        # self.var_MCA4 = tk.IntVar()
        # self.MCA4_checkbox = tk.Checkbutton(channel_frame, text='Enable MCA4', var=self.var_MCA4, onvalue=1, offvalue=0,
        #                                     command=self.activate_MCA4)
        # self.MCA4_checkbox.grid(row=9, column=1, sticky=tk.W, padx=3, pady=3)

        ##################################################################

        # Channels feedback

        # # label of the Voltage output
        # data_ao_value_label = tk.Label(channel_frame)
        # data_ao_value_label["text"] = "Output (V):                  "
        # data_ao_value_label.grid(row=0, column=2, padx=20, pady=10, sticky=tk.W)
        # # Voltage output setting
        # self.data_ao_value = tk.Label(channel_frame, width=10)
        # self.data_ao_value.grid(row=0, column=2, sticky=tk.E, padx=10, pady=3)
        # self.data_ao_value["text"] = '{:.3f}'.format(0)

        # # precision of AO with chosen range
        # # label of the AO precision
        # AO_precision_label = tk.Label(channel_frame, fg="red")
        # AO_precision_label["text"] = "AO precision for \u00B110V:                    "
        # AO_precision_label.grid(row=1, column=2, padx=20, pady=10, sticky=tk.W)
        # # AI precision display
        # self.AO_precision = tk.Label(channel_frame, width=10, fg="red")
        # self.AO_precision.grid(row=1, column=2, padx=10, pady=10, sticky=tk.E)
        # self.AO_precision["text"] = '{:.4f}'.format(
        #     20 / ((2 ** self.ao_info.resolution) - 1))  # display input value, initial

        # # label of the Voltage readback
        # eng_value_left_label = tk.Label(channel_frame)
        # eng_value_left_label["text"] = "Readback (V):                 "
        # eng_value_left_label.grid(row=3, column=2, padx=20, pady=10, sticky=tk.W)
        # # Voltage readback
        # self.eng_value = tk.Label(channel_frame, width=10)
        # self.eng_value.grid(row=3, column=2, padx=10, pady=10, sticky=tk.E)
        # self.eng_value["text"] = '{:.4f}'.format(0)  # display input value, initial

        # # precision of AI with chosen range
        # # label of the AI precision
        # AI_precision_label = tk.Label(channel_frame, fg="red")
        # AI_precision_label["text"] = "AI precision for \u00B110V:                    "
        # AI_precision_label.grid(row=4, column=2, padx=20, pady=10, sticky=tk.W)
        # # AI precision display
        # self.AI_precision = tk.Label(channel_frame, width=10, fg="red")
        # self.AI_precision.grid(row=4, column=2, padx=10, pady=10, sticky=tk.E)
        # # self.AI_precision["text"] = '{:.4f}'.format(self.on_select_ai_combobox())
        # self.AI_precision["text"] = '{:.4f}'.format(
        #     20 / ((2 ** self.ai_info.resolution) - 1))  # display input value, initial

        # # DMM label
        # DMM_label = tk.Label(channel_frame)
        # DMM_label["text"] = "DMM Settings:"
        # DMM_label.grid(row=5, column=0, padx=3, pady=10, sticky=tk.W)
        # # DMM readback
        # self.DMM_readback_label = tk.Label(channel_frame)
        # self.DMM_readback_label["text"] = "Readback (V):"
        # self.DMM_readback_label.grid(row=5, column=2, padx=20, pady=10, sticky=tk.W)
        # # DMM readback value
        # self.DMM_readback_value = tk.Label(channel_frame, width=10)
        # self.DMM_readback_value.grid(row=5, column=2, padx=10, pady=10, sticky=tk.E)
        # self.DMM_readback_value["text"] = '{:.4f}'.format(0)

        # # label of the counter
        # value_ct_left_label = tk.Label(channel_frame)
        # value_ct_left_label["text"] = "Ion/Photon Count:"
        # value_ct_left_label.grid(row=7, column=2, padx=20, pady=10, sticky=tk.W)
        # # counter value
        # self.value_ct = tk.Label(channel_frame, width=10)
        # self.value_ct.grid(row=7, column=2, sticky=tk.E, padx=10, pady=3)
        # self.value_ct["text"] = "0"  # display Counter value, initial

        # # DAQ label
        # DAQ_label = tk.Label(channel_frame)
        # DAQ_label["text"] = "MCC counter Ch #:"
        # DAQ_label.grid(row=7, column=0, padx=3, pady=10, sticky=tk.W)

        # # SR400 label
        # SR400_label = tk.Label(channel_frame)
        # SR400_label["text"] = "SR400 Settings:"
        # SR400_label.grid(row=8, column=0, padx=3, pady=10, sticky=tk.W)
        # # SR400 readback
        # self.SR400_readback_label = tk.Label(channel_frame)
        # self.SR400_readback_label["text"] = "Ion/Photon Count:"
        # self.SR400_readback_label.grid(row=8, column=2, padx=20, pady=10, sticky=tk.W)
        # # SR400 readback value
        # self.SR400_readback_value = tk.Label(channel_frame, width=10)
        # self.SR400_readback_value.grid(row=8, column=2, padx=10, pady=10, sticky=tk.E)
        # self.SR400_readback_value["text"] = '0'

        # # MCA4 label
        # MCA4_label = tk.Label(channel_frame)
        # MCA4_label["text"] = "MCA4 Settings:"
        # MCA4_label.grid(row=9, column=0, padx=3, pady=10, sticky=tk.W)

        # sep1 = tk.Label(channel_frame)
        # sep1["text"] = "---------------------------------------------------------------------------------------------"
        # sep1.grid(row=2, column=0, columnspan=3, padx=0, pady=0)

        # sep2 = tk.Label(channel_frame)
        # sep2["text"] = "----------------------------------------------------------------------------------------------"
        # sep2.grid(row=6, column=0, columnspan=3, padx=0, pady=0)

        # tk.Canvas(channel_frame, width=5, height=450, bg='#ECECEC').grid(column=3, row=0, rowspan=10)

        ##################################################################

        # Modifiable parameters

        # register to prevent invalid entry
        scan_start_value = self.register(validate_float_entry)
        scan_stop_value = self.register(validate_float_entry)
        scan_dwell_time_value = self.register(validate_positive_int_entry)
        scan_cycle_value = self.register(validate_positive_int_entry)
        scan_mass_value = self.register(validate_positive_int_entry)
        scan_wavenumber_value = self.register(validate_float_entry)
        scan_beam_energy_value = self.register(validate_float_entry)
        scan_step_size_value = self.register(validate_float_entry)
        scan_element_value = self.register(self.validate_string)

        scan_trigdelay_value = self.register(validate_float_entry)
        scan_trigfreq_value = self.register(validate_float_entry)
        scan_trigwidth_value = self.register(validate_float_entry)

        #   start label
        start_label = tk.Label(channel_frame)
        start_label["text"] = "Start (V):                  "
        start_label.grid(row=0, column=4, padx=20, pady=10, sticky=tk.W)
        #  set value of start point
        self.scan_start_entry = tk.Entry(
            channel_frame, validate='key', validatecommand=(scan_start_value, '%P'), width=7)
        self.scan_start_entry.grid(row=0, column=4, sticky=tk.E, padx=10, pady=3)
        self.scan_start_entry.insert(0, '{:.3f}'.format(0.00))

        #   stop label
        stop_label = tk.Label(channel_frame)
        stop_label["text"] = "Stop (V):                  "
        stop_label.grid(row=0, column=5, padx=20, pady=10, sticky=tk.W)
        #  set value of stop point
        self.scan_stop_entry = tk.Entry(
            channel_frame, validate='key', validatecommand=(scan_stop_value, '%P'), width=7)
        self.scan_stop_entry.grid(row=0, column=5, sticky=tk.E, padx=10, pady=3)
        self.scan_stop_entry.insert(0, '{:.3f}'.format(3.00))

        #   cycle label
        cycle_label = tk.Label(channel_frame)
        cycle_label["text"] = "Cycle #:         "
        cycle_label.grid(row=0, column=6, padx=10, pady=10, sticky=tk.W)
        #  set value of cycle
        self.scan_cycle_entry = tk.Entry(channel_frame, validate='key', validatecommand=(scan_cycle_value, '%P'), width=7)
        self.scan_cycle_entry.grid(row=0, column=6, sticky=tk.E, padx=10, pady=3)
        self.scan_cycle_entry.insert(0, "1")

        #   cycle status label
        self.cycle_status_label = tk.Label(channel_frame, bg="white", fg='blue', font=('Helvetica', 10))
        self.cycle_status_label["text"] = "Current cycle #:         " + "0"  # initial
        self.cycle_status_label.grid(row=1, column=6, padx=10, pady=3, sticky=tk.W)

        #   step size label
        step_size_label = tk.Label(channel_frame)
        step_size_label["text"] = "Step size (V):                  "
        step_size_label.grid(row=1, column=4, padx=20, pady=10, sticky=tk.W)
        #  value of step_size Combobox
        self.scan_step_size_entry = tk.Entry(
            channel_frame, validate='key', validatecommand=(scan_step_size_value, '%P'), width=7)
        self.scan_step_size_entry.grid(row=1, column=4, sticky=tk.E, padx=10, pady=3)
        self.scan_step_size_entry.insert(0, '{:.3f}'.format(0.001))

        #   dwell time label
        dwell_time_label = tk.Label(channel_frame)
        dwell_time_label["text"] = "Dwell time (ms):                  "
        dwell_time_label.grid(row=1, column=5, padx=20, pady=10, sticky=tk.W)
        #  set value of dwell time
        self.scan_dwell_time_entry = tk.Entry(
            channel_frame, validate='key', validatecommand=(scan_dwell_time_value, '%P'), width=7)
        self.scan_dwell_time_entry.grid(row=1, column=5, sticky=tk.E, padx=10, pady=3)
        self.scan_dwell_time_entry.insert(0, '100')

        # mass label
        self.mass_label = tk.Label(channel_frame)
        self.mass_label["text"] = "Mass Number:                  "
        self.mass_label.grid(row=2, column=4, padx=20, pady=10, sticky=tk.W)

        # set mass
        self.mass_entry = tk.Entry(
            channel_frame, validate='key', validatecommand=(scan_mass_value, '%P'), width=7)
        self.mass_entry.grid(row=2, column=4, padx=10, pady=10, sticky=tk.E)
        self.mass_entry.insert(0, '23')

        # element label
        self.element_label = tk.Label(channel_frame)
        self.element_label["text"] = "Element:"
        self.element_label.grid(row=2, column=5, padx=20, pady=10, sticky=tk.W)

        # set element
        self.element_entry = tk.Entry(
            channel_frame, validate='key', validatecommand=(scan_element_value, '%P'), width=7)
        self.element_entry.grid(row=2, column=5, padx=10, pady=10, sticky=tk.E)
        self.element_entry.insert(0, 'Na')

        # wavenumber label
        self.wavenumber_label = tk.Label(channel_frame)
        self.wavenumber_label["text"] = "Wavenumber (cm\u207B\u00B9):         "
        self.wavenumber_label.grid(row=2, column=6, padx=10, pady=10, sticky=tk.W)

        # set wavenumber
        self.wavenumber_entry = tk.Entry(
            channel_frame, validate='key', validatecommand=(scan_wavenumber_value, '%P'), width=7)
        self.wavenumber_entry.grid(row=2, column=6, padx=10, pady=10, sticky=tk.E)
        self.wavenumber_entry.insert(0, '{:.4f}'.format(0))

        # beam energy label
        self.beam_energy_label = tk.Label(channel_frame)
        self.beam_energy_label["text"] = "Beam energy (eV):"
        self.beam_energy_label.grid(row=3, column=4, padx=20, pady=10, sticky=tk.W)

        # set beam energy
        self.beam_energy_entry = tk.Entry(
            channel_frame, validate='key', validatecommand=(scan_beam_energy_value, '%P'), width=7)
        self.beam_energy_entry.grid(row=3, column=4, padx=10, pady=10, sticky=tk.E)
        self.beam_energy_entry.insert(0, '{:.3f}'.format(19930))

        # Collinear or anti-collinear combobox
        self.collinear_combobox = Combobox(channel_frame)
        self.collinear_combobox["state"] = "readonly"
        self.collinear_combobox["values"] = ["Collinear", "Anticollinear"]
        self.collinear_combobox.current(1)
        self.collinear_combobox.grid(row=3, column=5, sticky=tk.W, padx=20, pady=6)

        # Headline label
        # self.headline_label = tk.Label(channel_frame)
        # self.headline_label["text"] = "Headline of the data file:"
        # self.headline_label.grid(row=4, column=4, padx=20, pady=10, sticky=tk.W)

        # Trigger Label
        self.trigmode_label = tk.Label(channel_frame)
        self.trigmode_label["text"] = "Trigger Mode:"
        self.trigmode_label.grid(row=4, column=4, padx=20, pady=10, sticky=tk.W)

        # Trigger Delay
        self.trigdelay_label = tk.Label(channel_frame)
        self.trigdelay_label["text"] = "Trigger Delay(ms):"
        self.trigdelay_label.grid(row=3, column=6, padx=20, pady=10, sticky=tk.W)

        self.trigdelay_entry = tk.Entry(channel_frame, validate='key', validatecommand=(scan_trigdelay_value, '%P'), width=7)
        self.trigdelay_entry.grid(row=3, column=6, padx=10, pady=10, sticky=tk.E)
        self.trigdelay_entry.insert(0, '0')

        # Trigger Checkbox
        self.var_trigmode = tk.IntVar()
        self.trigmode_checkbox = tk.Checkbutton(channel_frame, text='Enable Trig', var=self.var_trigmode, onvalue=1, offvalue=0)
        self.trigmode_checkbox.grid(row=4, column=4, sticky=tk.E, padx=10, pady=3)
        # self.trigmode_checkbox.select()

        # Trigger Freq
        self.trigfreq_label = tk.Label(channel_frame)
        self.trigfreq_label["text"] = "Trigger Freq(Hz):"
        self.trigfreq_label.grid(row=4, column=5, padx=20, pady=10, sticky=tk.W)

        self.trigfreq_entry = tk.Entry(channel_frame, validate='key', validatecommand=(scan_trigfreq_value, '%P'), width=7)
        self.trigfreq_entry.grid(row=4, column=5, padx=10, pady=10, sticky=tk.E)
        self.trigfreq_entry.insert(0, '1')

        # Trigger Width
        self.trigwidth_label = tk.Label(channel_frame)
        self.trigwidth_label["text"] = "Trigger Width(ms):"
        self.trigwidth_label.grid(row=4, column=6, padx=20, pady=10, sticky=tk.W)

        self.trigwidth_entry = tk.Entry(channel_frame, validate='key', validatecommand=(scan_trigwidth_value, '%P'), width=7)
        self.trigwidth_entry.grid(row=4, column=6, padx=10, pady=10, sticky=tk.E)
        self.trigwidth_entry.insert(0, '100')

        # set headline
        # self.headline = tk.Entry(
        #     channel_frame, validate='key', validatecommand=True, width=50)
        # self.headline.grid(row=4, column=5, padx=0, pady=10, sticky=tk.W, columnspan=2)

        # start/stop scan button
        self.start_scan_button = tk.Button(channel_frame)
        self.start_scan_button["text"] = "Start scan"
        self.start_scan_button["command"] = self.scan_manager
        self.start_scan_button.grid(row=5, column=4, sticky=tk.W, padx=20, pady=3)

        # provides option to run the scan in a loop
        self.var_loop = tk.IntVar()
        self.loop_checkbox = tk.Checkbutton(channel_frame, text='Run indefinitely',
                                            var=self.var_loop, onvalue=1, offvalue=0)
        self.loop_checkbox.grid(row=5, column=4, sticky=tk.W, padx=(100, 20), pady=3)

        # pause scan button
        self.pause_scan_button = tk.Button(channel_frame)
        self.pause_scan_button["text"] = "Pause scan"
        self.pause_scan_button["command"] = self.pause_scan
        self.pause_scan_button.grid(row=5, column=5, sticky=tk.W, padx=0, pady=3)

        #   scan status label
        self.scan_status_label = tk.Label(channel_frame, bg="white", fg='red', font=('Helvetica', 15))
        self.scan_status_label["text"] = "Not scanning"
        self.scan_status_label.grid(row=5, column=6, sticky=tk.W, padx=20, pady=3)

        # progress bar label
        self.progress_bar_label = tk.Label(channel_frame)
        self.progress_bar_label["text"] = "Progress of the scan:"
        self.progress_bar_label.grid(row=6, column=4, padx=20, pady=10, sticky=tk.W)

        # progress bar
        self.pb = ttk.Progressbar(
            channel_frame,
            orient='horizontal',
            mode='determinate',
            length=370
        )
        self.pb.grid(row=6, column=5, padx=0, pady=10, sticky=tk.W, columnspan=2)

        sep2 = tk.Label(channel_frame)
        sep2[
            "text"] = "----------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        sep2.grid(row=7, column=4, columnspan=3, padx=0, pady=0)

        # file saving
        tk.Label(channel_frame, text="Data directory:    ").grid(row=8, column=4, sticky=tk.W, padx=20)
        self.dir_entry = tk.Entry(channel_frame, width=40)
        # makes a subfolder to put the run logs into
        if not os.path.exists(os.getcwd() + "\\Runs"):
            os.makedirs(os.getcwd() + "\\Runs")
        self.dir_entry.insert(0, os.getcwd() + "\\Runs")
        self.dir_entry.grid(row=8, column=4, padx=(11, 0), pady=2, sticky=tk.E, columnspan=2)

        # opens menu for selecting a directory
        self.change_button = tk.Button(channel_frame, width=10)
        self.change_button["text"] = "Change"
        self.change_button["command"] = self.change_dir
        self.change_button.grid(row=8, column=6, padx=10, pady=2)

        # defines a default name for the file
        self.name = str(date.today()) + " Run"

        tk.Label(channel_frame, text="Data file name:   ").grid(row=9, column=4, sticky=tk.W, padx=20)
        self.file_entry = tk.Entry(channel_frame, width=40)
        self.file_entry.insert(0, self.name)
        self.file_entry.grid(row=9, column=4, padx=0, pady=2, sticky=tk.E, columnspan=2)

        # provides option to log data to new time-stamped file
        self.var_newout = tk.IntVar()
        self.new_outfile_checkbox = tk.Checkbutton(channel_frame, text='Use single-run timestamped file',
                                                   var=self.var_newout, onvalue=1, offvalue=0)
        self.new_outfile_checkbox.grid(row=9, column=6, sticky=tk.W, padx=12, pady=3)
        self.new_outfile_checkbox.select()


class CLS_Plot(UIExample):
    def __init__(self, master, receiver, scan_on):
        super(CLS_Plot, self).__init__(master)
        self.receiver = receiver
        self.scanning = scan_on
        self.data_list = [[], [], [], [], []]  # Include an extra list for time data

        # creates plotting GUI upon receiving confirmation of creation of main GUI
        receiver.get()
        self.create_widgets()

    #########################################################################

    def get_axis_data(self, series):
        """Translates the name of the data series selected in a combobox to its numeric representation (place in the
        data list), which is used for plotting
        """
        try:
            if series == 'x':
                data = self.x_axis_combobox.get()
            elif series == 'y':
                data = self.y_axis_combobox.get()
            else:
                raise ValueError('If you are seeing this, something very wrong has happened.')

            if data == 'Time (s)':
                return 4  # Index for time data
            elif data == 'Analog Output (V)':
                return 0
            elif data == 'Analog Input (V)':
                return 1
            elif data == 'DMM Reading (V)':
                return 2
            elif data == 'Ion/Photon Count':
                return 3  # Index for counts
            else:
                raise ValueError('Invalid data series selected.')
        except ValueError:
            return 0

    def set_labels(self):
        self.x_axis = self.get_axis_data('x')
        self.y_axis = self.get_axis_data('y')
        try:
            plt.xlabel(self.x_axis_combobox.get())
            plt.ylabel(self.y_axis_combobox.get())
        except ValueError:
            return 0

    def plot_data(self, point):
        """Plots through blitting: adding a single point without redrawing the entire figure (as the slow ax.plot()
        does). Adjusts axes when data is beyond current limits."""
        x_min, x_max, y_min, y_max = plt.axis()
        # heuristic adjustment levels (cast to float to deal with Decimal type of Analog Output)
        if point[self.x_axis] >= x_max:
            plt.xlim(x_min, 1.1 * float(point[self.x_axis]))
        elif point[self.x_axis] <= x_min:
            plt.xlim(float(point[self.x_axis]) - .1 * abs(float(point[self.x_axis])), x_max)
        if point[self.y_axis] >= y_max:
            plt.ylim(y_min, 1.1 * float(point[self.y_axis]))
        elif point[self.y_axis] <= y_min:
            plt.ylim(float(point[self.y_axis]) - .1 * abs(float(point[self.y_axis])), y_max)
        # adds current data set (including new point) to the plot
        self.scatter.set_data(self.data_list[self.x_axis], self.data_list[self.y_axis])

    def plot_cleanup(self):
        # gathers any remaining data from the pipe once a scan has finished
        while not self.receiver.empty():
            data = self.receiver.get()
            # break if a scan stop signal (None) is received as any data that follows should be plotted in the main loop
            if type(data) != list:
                break
            for i in range(5):  # Adjust range to include time data
                self.data_list[i].append(data[i])
        # final plot covering the entire scan
        plt.ion()

        if self.scatter is None:
            self.scatter, = self.ax.plot(self.data_list[self.x_axis], self.data_list[self.y_axis], marker='o', color='r', linestyle='')
        else:
            try:
                # sets axis limits slightly beyond extrema of the entire dataset
                plt.xlim(float(min(self.data_list[self.x_axis])) - .1 * abs(float(min(self.data_list[self.x_axis]))), 1.1 * float(max(self.data_list[self.x_axis])))
                plt.ylim(float(min(self.data_list[self.y_axis])) - .1 * abs(float(min(self.data_list[self.y_axis]))), 1.1 * float(max(self.data_list[self.y_axis])))
                # adds dataset to the plot
                self.scatter.set_data(self.data_list[self.x_axis], self.data_list[self.y_axis])
            except ValueError:
                print("There was an error in generating the final plot. Have you been holding the window?")
        plt.ioff()
        self.update()

    def plot_loop(self):
        # executes the plot loop while the scan is in progress
        while self.scanning.is_set():
            # waits a maximum of one second for data to be received
            try:
                data = self.receiver.get(timeout=10)
            except queue.Empty:
                print("The queue is empty.")
                # data = None

            if type(data) == list:
                # appends to list and plots
                for i in range(5):  # Adjust range to include time data
                    self.data_list[i].append(data[i])
                if not self.var_plot_post_scan.get():
                    plt.ion()
                    # creates a scatter list if none exists, specifying the design of the plotted points
                    if self.scatter is None:
                        self.scatter, = self.ax.plot(data[self.x_axis], data[self.y_axis], marker='o', color='r', linestyle='')
                    else:
                        self.plot_data(data)
                    plt.ioff()
                    self.update()
            # waits for the resume or scan stop signal to enter the queue after the scan is paused
            elif data == "Paused":
                signal = self.receiver.get()
                if signal is None:
                    break
            # breaks when a scan is complete
            elif data == "Done":
                break
            # breaks when a scan is complete or the queue is empty
            # elif data is None:
                # break
            # should only occur at the start of cycles, where breaking is not required but cleanup plotting is helpful
            else:
                self.plot_cleanup()

        # cleans up and plots outstanding data following a scan event
        self.plot_cleanup()

    # combobox event binding passes two parameters to the function, but the second one is irrelevant
    def clear_plot(self, event=0):
        plt.ion()
        self.ax.clear()
        # clears the extant data
        self.scatter = None
        self.data_list = [[], [], [], [], []]  # Reset data_list with time data
        self.set_labels()
        self.ax.grid()
        plt.ioff()

    def create_widgets(self):
        self.option_add("*Font", "Helvetica 10")
        # create the window
        plot_frame = tk.Frame(self, relief='flat', borderwidth=3)
        plot_frame.pack(anchor=tk.NW, fill=tk.X, padx=3, pady=4)
        # clear plot button
        self.clear_plot_button = tk.Button(plot_frame)
        self.clear_plot_button["text"] = "Clear plot"
        self.clear_plot_button["command"] = self.clear_plot
        self.clear_plot_button.grid(row=0, column=0, padx=3, pady=3)

        # x-axis data selection
        self.x_axis_select_label = tk.Label(plot_frame)
        self.x_axis_select_label["text"] = "X-axis Data:"
        self.x_axis_select_label.grid(row=0, column=1, padx=(20, 5), pady=10, sticky=tk.W)

        self.x_axis_combobox = Combobox(plot_frame)
        self.x_axis_combobox["state"] = "readonly"
        self.x_axis_combobox["values"] = ["Time (s)", "Analog Input (V)", "Analog Output (V)", "DMM Reading (V)",
                                          "Ion/Photon Count"]
        self.x_axis_combobox.current(0)
        self.x_axis_combobox.grid(row=0, column=2, padx=0, pady=6, sticky=tk.W)
        self.x_axis_combobox.bind("<<ComboboxSelected>>", self.clear_plot)

        # y-axis data selection
        self.y_axis_select_label = tk.Label(plot_frame)
        self.y_axis_select_label["text"] = "Y-axis Data:"
        self.y_axis_select_label.grid(row=0, column=3, padx=(20, 5), pady=10, sticky=tk.W)

        self.y_axis_combobox = Combobox(plot_frame)
        self.y_axis_combobox["state"] = "readonly"
        self.y_axis_combobox["values"] = ["Time (s)", "Analog Input (V)", "Analog Output (V)", "DMM Reading (V)",
                                          "Ion/Photon Count"]
        self.y_axis_combobox.current(4)  # Default to "Counts"
        self.y_axis_combobox.grid(row=0, column=4, padx=0, pady=6, sticky=tk.W)
        self.y_axis_combobox.bind("<<ComboboxSelected>>", self.clear_plot)

        # provides option to clear plot after a completed scan
        self.var_clear_post_scan = tk.IntVar()
        self.clear_post_scan_checkbox = tk.Checkbutton(plot_frame, text='Clear before new scan',
                                                       var=self.var_clear_post_scan, onvalue=1, offvalue=0)
        self.clear_post_scan_checkbox.grid(row=0, column=5, sticky=tk.W, padx=30, pady=3)
        self.clear_post_scan_checkbox.select()


        # provides option to prevent plotting until scan complete
        self.var_plot_post_scan = tk.IntVar()
        self.plot_post_scan_checkbox = tk.Checkbutton(plot_frame, text='Performance: plot after scan complete',
                                                      var=self.var_plot_post_scan, onvalue=1, offvalue=0)
        self.plot_post_scan_checkbox.grid(row=0, column=6, sticky=tk.W, padx=0, pady=3)

        # creates the figure, axes, limits, and placeholder for a special list to hold the scatter of points
        self.fig = plt.figure(figsize=(9, 6))
        self.ax = plt.subplot(111)
        self.scatter = None
        self.ax.set_facecolor('#DEDEDE')
        self.ax.grid()

        self.set_labels()
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()

        # run the plot loop on a separate thread to allow GUI to remain interactive while waiting for scan start
        threading.Thread(target=self.plot_manager).start()
        self.update()

    def plot_manager(self):
        while True:
            # waits for a scan to begin
            self.scanning.wait()
            # updates plot ahead of new scan
            if self.var_clear_post_scan.get():
                self.clear_plot()
            else:
                self.set_labels()
            self.plot_loop()


def cls_trigger(queue, event):
    # while not queue.empty():
        # time.sleep(1)

    board_num = 0
    # configure_first_detected_device()
    # device_info = DaqDeviceInfo(board_num)
    # value = ul.d_bit_in(0, 1, 7)
    # print(value)
    # device_info = queue.get()
    # trigger_on = event
    print(board_num)

    # while True:
    #     value = ul.d_bit_in(0, 1, 7)
    #     print(value)

    #     if value:
    #         trigger_on.set()
    #     else:
    #         trigger_on.clear()
    #########################################################################

    #########################################################################

def cls_epics(equeue, e):
    # EPICS variable
    pv = PvObject({'value': INT})
    pvaServer = PvaServer('DAQ:COUNT', pv)

    while True:
        try:
            pv['value'] = int(equeue.get(block=False))
        except queue.Empty:
            pass

        time.sleep(0.1)

    # while True:
    #     print(queue.empty())
    #     if not queue.empty():
    #         pv['value'] = int(queue.get())

    #     time.sleep(0.1)

def data_gen(comm, event, equeue):
    CLS_Scan(master=tk.Tk(), giver=comm, scan_on=event, epics_queue=equeue).mainloop()

def plot_gen(comm, event):
    CLS_Plot(master=tk.Tk(), receiver=comm, scan_on=event).mainloop()

# starts the program by creating two GUIs under different processes
if __name__ == "__main__":
    # first pipe can only receive, second can only send
    queue = multiprocessing.Queue()
    
    # trigger queue to get board number for trigger process
    tqueue = multiprocessing.Queue()

    # epics queue 
    equeue = multiprocessing.Queue()

    # creates an event to inform the plot process of the scan status
    e = multiprocessing.Event()

    # creates an event to inform external input to trigger scan
    te = multiprocessing.Event()

    # creates and starts processes that create the two GUIs
    data_process = multiprocessing.Process(target=data_gen, args=(queue, e, equeue))
    plot_process = multiprocessing.Process(target=plot_gen, args=(queue, e))

    epics_process = multiprocessing.Process(target=cls_epics, args=(equeue, e))
    # trigger_process = multiprocessing.Process(target=cls_trigger, args=(tqueue, te))

    data_process.start()
    plot_process.start()

    epics_process.start()
    # trigger_process.start()

    # stalls the execution of the main process until the data process has finished so the plot process can be cleaned up
    data_process.join()
    plot_process.terminate()

    epics_process.terminate()
    # trigger_process.terminate()
