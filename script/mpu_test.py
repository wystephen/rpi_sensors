import smbus
import sched, time
import binascii
from threading import Timer, Thread, Event
from struct import *
import ctypes
from math import acos

import sched, time
import binascii
from struct import *




def mpu9250_data_get_and_write():
    # global t_a_g

    # keep AKM pointer on continue measuring
    i2c.write_byte_data(0x0c, 0x0a, 0x16)
    # get MPU9250 smbus block data
    # xyz_g_offset = i2c.read_i2c_block_data(addr, 0x13, 6)
    xyz_a_out = i2c.read_i2c_block_data(addr, 0x3B, 6)
    print("xyz_a_out" + str(list2word(xyz_a_out, calc_accelerator_value)))
    # print("xyz_a_out_org#:"+str(xyz_a_out))

    xyz_g_out = i2c.read_i2c_block_data(addr, 0x43, 6)
    print("xyz_g_out" + str(list2word(xyz_g_out, calc_gyro_value)))
    # xyz_a_offset = i2c.read_i2c_block_data(addr, 0x77, 6)

    # get AK8963 smb#us data (by pass-through way)
    xyz_mag = i2c.read_i2c_block_data(0x0c, 0x00, 6)
    # print("xyz_mag"+str(list2word(xyz_mag)))
    xyz_mag_adj = i2c.read_i2c_block_data(0x0c, 0x10, 3)
    i2c.write_byte_data(0x0c,0x0a,0x01)
    print("xyz_mag:",xyz_mag)
    print("xyz mag_adj:",xyz_mag_adj)
    #print("xyzmag:",str(list2word(xyz_mag_adj,calc_gyro_value)))


def list2word(data_list=[], callback=''):
    data = data_list[:]
    if not len(data):
        return [];

    result = []
    for i in range(3):
        high_byte = data.pop(0)
        low_byte = data.pop(0)
        result.append(callback(float(ctypes.c_int16(((high_byte << 8) | low_byte)).value)))

    return result


def calc_accelerator_value(value):
    return round(value / 16.4)


def calc_gyro_value(value):
    return round(value / 131)


def clear_i2c_and_close_file():
    i2c.write_byte_data(addr, 0x6A, 0x07)


# solution 1: while true
def while_true_method():
    # max_count = raw_input("Enter how many count you want.")
    max_count = 100;
    if max_count < 1: max_count = 1000
    print "Data Counts: " + str(max_count)

    max_count = int(max_count)
    count = 1

    print ""
    print "MPU9250 9axis DATA Recording..."
    while True:
        # if count <= max_count:
        mpu9250_data_get_and_write()
        count += 1
        time.sleep(0.5)
        # else:
        pass
    # break;

if __name__ == '__main__':
    i2c = smbus.SMBus(1)
    addr = 0x68
    t0 = time.time()


    # ====== initial zone ======
    try:
        device_id = i2c.read_byte_data(addr, 0x75)
        print "Device ID:" + str(hex(device_id))
        print "MPU9250 I2C Connected."
        print ""
    except:
        print "Connect failed"
        print ""
    i2c.write_byte_data(0x68, 0x6a, 0x00)
    time.sleep(0.05);
    i2c.write_byte_data(0x68, 0x37, 0x02)
    time.sleep(0.05)
    i2c.write_byte_data(0x0c, 0x0a, 0x11) # 0110 continuous measurement mode 2

    # set frequence for accelerator
    i2c.write_byte_data(0x68, 29, 9)

    #print " after write"


    # enable fifo and dmp
    # i2c.write_byte_data(0x68 , 106 , 32+64);

    # ====== intial done ======

    while_true_method();
