#!/usr/bin/env python

#http://docs.ros.org/api/rosbag_storage/html/c++/
import rosbag
from binascii import hexlify
import rospy

## LOAD BAG DATA
#bag = rosbag.Bag('/home/karl/wheele_bags/wheele_add_compass_GPS_freeze_02Feb2018/2018-02-02-17-54-48.bag')
#bag = rosbag.Bag('/home/karl/wheele_bags/wheele_more_speed_03Feb2018/2018-02-03-17-42-00.bag')

## Get bag file(s) from current directory where this is run
#import glob
#files = glob.glob("*.bag")
import fnmatch
import os
files = []
for root, dirnames, filenames in os.walk('.'):
    for filename in fnmatch.filter(filenames, '*.bag'):
        files.append(os.path.join(root, filename))

for f in files:
    print f
    bag = rosbag.Bag(f)
    
    node_names_list = ['ublox','m8n']
    
    for node_name in node_names_list:
    
        print('fix')
        csv_fix_name = f[0:-4] + '_' + node_name + '_fix.csv'
        csv_fix = open(csv_fix_name,'w')
        csv_fix.write('bagTime,frameTime,status,lat,lon,covar0,covar4\n')
      
        for k, (topic, msg, t) in enumerate(bag.read_messages('/' + node_name + '/fix')):
            if(k==0):
                t0 = t
                
            csv_fix.write('%.9f,%.9f,%d,%.9f,%.9f,%.3f,%.3f\n'
              % ((t-t0).to_sec(), (msg.header.stamp-t0).to_sec(), msg.status.status,
                  msg.latitude, msg.longitude, msg.position_covariance[0], msg.position_covariance[4] ))
        csv_fix.close()
        
        print('gps_vel')
        csv_gps_vel_name = f[0:-4] + '_' + node_name + '_gps_vel.csv'
        csv_gps_vel = open(csv_gps_vel_name,'w')
        csv_gps_vel.write('bagTime,frameTime,vx,vy\n')
      
        for k, (topic, msg, t) in enumerate(bag.read_messages('/' + node_name + '/fix_velocity')):            
            csv_gps_vel.write('%.9f,%.9f,%.3f,%.3f\n'
              % ((t-t0).to_sec(), (msg.header.stamp-t0).to_sec(), msg.twist.twist.linear.x, msg.twist.twist.linear.y) )
        csv_gps_vel.close()
        
        print('gps_relpose')
        csv_gps_vel_name = f[0:-4] + '_' + node_name + '_gps_relpose.csv'
        csv_gps_vel = open(csv_gps_vel_name,'w')
        csv_gps_vel.write('bagTime,relE,relN\n')
      
        for k, (topic, msg, t) in enumerate(bag.read_messages('/' + node_name + '/navrelposned')):            
            csv_gps_vel.write('%.9f,%.3f,%.3f\n'
              % ((t-t0).to_sec(), msg.relPosE/100.0, msg.relPosN/100.0) )
        csv_gps_vel.close()
        
    bag.close()
