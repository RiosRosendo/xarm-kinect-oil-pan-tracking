# xArm + Kinect v2 Oil Pan Tracking

## Project Overview

ROS2 3D perception pipeline for industrial oil pan tracking and manipulation using collaborative robotic arm (xArm) and RGB-D sensor (Kinect v2).

### Key Features
- **3D Perception**: Real-time point cloud processing with Open3D
- **Pose Estimation**: Iterative Closest Point (ICP) alignment with CAD models
- **Robotic Control**: xArm trajectory planning and execution
- **High Precision**: 2.8 cm accuracy at 450 ms latency

---

## Performance Metrics
| Metric | Value |
|--------|-------|
| Positioning Accuracy | 2.8 cm |
| Latency | 450 ms |
| Point Cloud Rate | 30 Hz |
| Frame Resolution | 512×424 (Kinect v2) |

---

## Tech Stack

### Core
- **ROS2** (Middleware)
- **Kinect v2** (RGB-D Camera)
- **xArm** (Collaborative Robot Arm)

### Perception & Processing
- **Open3D** (Point Cloud Filtering & Alignment)
- **PCL** (Point Cloud Library)
- **ICP Algorithm** (Pose Estimation)

### Development
- **Python 3.x**
- **C++ (ROS2 Nodes)**

---

## Prerequisites

- Ubuntu 20.04+ with ROS2 Humble
- xArm SDK (≥1.0.0)
- libfreenect2 (Kinect v2 Driver)
- Open3D Python bindings
- PCL with ROS2 bindings

---

## Installation

```bash
# Clone the repository
git clone https://github.com/RiosRosendo/xarm-kinect-oil-pan-tracking.git
cd xarm-kinect-oil-pan-tracking

# Install dependencies
sudo apt install ros-humble-perception-pcl ros-humble-xarm-ros2
pip install open3d numpy opencv-python

# Build the ROS2 workspace
colcon build --symlink-install
source install/setup.bash
```

---

## Usage

### Launch the Pipeline
```bash
ros2 launch xarm_perception oil_pan_tracking.launch.py
```

### Run Tracking Node
```bash
ros2 run xarm_perception tracking_node
```

### View Point Cloud
```bash
ros2 run rviz2 rviz2 -d config/perception.rviz
```

---

## Architecture

```
Kinect v2 (RGB-D) 
    ↓
Point Cloud Preprocessing (Downsample, Filter)
    ↓
ICP Alignment (vs. CAD Model)
    ↓
Pose Estimation
    ↓
xArm Trajectory Planning
    ↓
Robotic Manipulation
```

---

## Contributors
- **Rosendo De Los Rios** - Perception pipeline, integration, testing & optimization
- **Jordan Palafox** - Initial ROS2 setup & xArm control framework

---

## Papers & References
- See `/docs` folder for technical documentation and research papers

---

## License
MIT License - See LICENSE file for details

---

## Contact
📧 Email: delosriosrosendo@gmail.com  
🔗 GitHub: [@RiosRosendo](https://github.com/RiosRosendo)  
🔗 LinkedIn: [delosriosrosendo](https://linkedin.com/in/delosriosrosendo)
