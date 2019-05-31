#Perception: Mapping and Patrolling

**Tasks to achieve**

1. Map the Race World
2. Edit raceworld to include a line and follow as a loop.
3. Create launch file includes front_laser and front_flea3 options and follows line without stopping.
4. Use rosbag to record /laserscan and /tf topics
5. Play the line-following sequence back while running gmapping
6. Compare new map to random produced map

### Team

>Sam Kysar(Team Lead)

>Om Kukunuru

>Kalpesh Kuber

## To clone and run project

***You may need to source the main ros setup.bash initially***

***1)*** Assumes ROS Indigo and Gazebo 2, clone repository [HERE](https://bitbucket.org/ee5531sp2018/optical-illusions/commits/all)

***2)*** open new terminal

***3)*** type: ```cd <path to local repository>/optical-illusions/workspace/``` replacing <path to local repository> with the path to local repository

***4)*** type: ```ls``` verify only local folder is src, if not remove all but src

***5)*** type: ```catkin_make```

***6)*** type: ```source devel/setup.bash```

***7)*** open new terminal

***8)*** type: ```cd <path to local repository>/optical-illusions/workspace/```       replacing <path to local repository> with the path to local repository

***9)*** type: ```source devel/setup.bash```

***10)*** type: ```roslaunch lab4_pkg lab4.launch config:=<desired launch>``` In first terminal replacing ```<desired launch>``` with desired launch from below options

***```For active recording```***

***11)*** type: ```roslaunch jackal_viz view_robot.launch config:=gmapping``` In second terminal to view map building in rviz

***12)*** type: ```rosrun map_server map_saver -f <map_name>``` To save map in separate terminal.

***```For post recording```***

***13)*** Follow steps at this [Link](http://wiki.ros.org/slam_gmapping/Tutorials/MappingFromLoggedData#record)


##Launch options

To run the launch file:

***for only laser scan***

```roslaunch lab4_pkg lab4.launch config:=front_laser```

***for only flea3 camera***

```roslaunch lab4_pkg lab4.launch config:=front_flea3```

***for both, recomended!***

```roslaunch lab4_pkg lab4.launch config:=laserCam```


***Note:*** If during the launch of lab4.launch file any red shows up in terminal Gazebo may have launched erroneously, therefore hit ctrl c to kill the process and retry steps 10-12 as needed. Gazebo has some problems at times launching also repeat if Gazebo shows only black on the screen.

***Note:*** Second note, the model parameter is set to start driving after 20 seconds giving the operator time to launch rviz with gmapping. This parameter is in the lab4.launch file.

## Maps created by running wall following and then line following with Rosbag playback

***Wall following map***
![wall_follow.png](https://bitbucket.org/repo/XXGzyex/images/1891317769-wall_follow.png)

***Line following map***
![line_map.png](https://bitbucket.org/repo/XXGzyex/images/3554166669-line_map.png)

## Control Strategy for Motion Control

PID control was implemented on the robot in order to limit the jerk motion of the robot. In the first image is shown the setup as rqt_graph to display the location of the PID with respect to the control system. In order to tune the robot ```rosrun rqt_reconfigure rqt_reconfigure``` was ran and tuned with a very impulsed input fed to the system as shown in below image. The PID was implemented to have one PID buffer the angular velocity and the other to buffer the linear acceleration. Image below shows tuning of linear control.

***PID rqt_graph location***
![Graph.png](https://bitbucket.org/repo/XXGzyex/images/4126613797-Graph.png)

***PID tuning***
![pid_controller.png](https://bitbucket.org/repo/XXGzyex/images/2836173380-pid_controller.png)
