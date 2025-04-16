import pyrealsense2 as rs
import numpy as np
import cv2
import math
from pupil_apriltags import Detector
import collections

C_H = 1.5  # Height of the camera above the ground (meters)
C_T = math.radians(30)  # Tilt angle in radians (e.g., 30 degrees)
TOL_W = 0.5 
TOL_D = 0.25
TOL_R = .05 # in meters
TOL_THETA = 3 # in degrees
THRESHOLD = 60

smoothed_distance = None
smoothed_pixel = None
distance_buffer = collections.deque(maxlen=6)
pixel_buffer = collections.deque(maxlen=6)

def update_temporal_smoothing(new_distance, new_pixel):
    # Add the new measurement to the buffers
    global smoothed_distance, smoothed_pixel, distance_buffer,pixel_buffer
    distance_buffer.append(new_distance)
    pixel_buffer.append(np.array(new_pixel, dtype=np.float32))
    
    # Compute the average (or weighted average) of the buffers
    smoothed_distance = np.mean(distance_buffer)
    smoothed_pixel = np.mean(pixel_buffer, axis=0)
    
    return smoothed_distance, smoothed_pixel

def wall(depth_frame):
    global smoothed_distance, smoothed_pixel
    alpha = 0.8  # Smoothing factor; adjust as needed (0 < alpha < 1)
    KERNEL_SIZE = 7  # Adjust for sensitivity
    kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)

    if not depth_frame:
        return -1

    # Convert depth frame to NumPy array
    depth_image = np.asanyarray(depth_frame.get_data())

    height, width = depth_image.shape

    top_half_image = depth_image[:height//4, :]

    valid_depths = top_half_image[top_half_image > 0]

    if valid_depths.size > 0:
        lowest_depth_value = np.min(valid_depths)
    else:
        lowest_depth_value = np.nan  # No valid depth data

    print(f"{lowest_depth_value}")

    if lowest_depth_value == np.nan:
        return -2 # for if the frame is bad

    if lowest_depth_value < TOL_W:
        return -3 # getting too close to wall
    
    if lowest_depth_value < TOL_D:
        return -4# too close to wall

    # Ignore zero depth values (invalid points)
    depth_image = np.where(depth_image == 0, np.nan, depth_image)

    # Apply dilation (max depth in region)
    max_depth = cv2.dilate(depth_image, kernel, iterations=1)

    # Apply erosion (min depth in region)
    min_depth = cv2.erode(depth_image, kernel, iterations=1)

    # Compute depth variation
    depth_variation = max_depth - min_depth
    depth_variation = np.nan_to_num(depth_variation)  # Replace NaNs with 0

    target_pixels = np.where(depth_variation > THRESHOLD)
    coordinates = np.column_stack((target_pixels[1], target_pixels[0]))
    translated_coordinates = coordinates 
    translated_coordinates = np.clip(translated_coordinates, 0, np.array([width - 1, height - 1]))
    depths = depth_image[translated_coordinates[:, 1], translated_coordinates[:, 0]]
    depths = np.array(depths).flatten()  # Ensure it's 1D

# Create a boolean mask for valid depth values (non-NaN)
    valid_mask = ~np.isnan(depths)

    if valid_mask.sum() > 0:
        valid_depths = depths[valid_mask]
        valid_coords = translated_coordinates[np.nonzero(valid_mask)[0]]

        # Find index of minimum depth from valid depths
        min_index = np.argmin(valid_depths)
        new_distance = valid_depths[min_index]
        new_pixel = valid_coords[min_index]

        # Apply temporal smoothing:
        smoothed_distance, smoothed_pixel = update_temporal_smoothing(new_distance, new_pixel)

        # Visualization: draw a red circle on a color version of the depth image
    else:
        smoothed_distance = np.nan
        

    return smoothed_distance

class ObjectTracker:
    def __init__(self, r, theta):
        self.r = r
        self.theta = theta

    def __repr__(self):
        return f" r={self.r}, theta={self.theta})"

class ObjectManager:
    def __init__(self):
        self.objects = []

    def __iter__(self):
        return iter(self.objects)

    def add_object(self, r, theta):
        """Add a new object to the list."""
        new_obj = ObjectTracker(r, theta)
        self.objects.append(new_obj)

    def check_object(self, r, theta):
        for obj in global_manager:
            if r - TOL_R < obj.r < r + TOL_R:
                if theta - TOL_THETA < obj.theta < theta + TOL_THETA:
                    return True
        return False

    def clear_all_objects(self):
        self.objects.clear()

    def print_objects(self):
        for count, obj in enumerate(global_manager):
            print(f"Object {count}: {obj}")

global_manager = ObjectManager()

def april(color_frame):

    if color_frame is None:
        print("Error: color_image is None")
        return -1
    detector = Detector(families="tag36h11")

    frame = np.asanyarray(color_frame.get_data())
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    tags = detector.detect(gray)

    if tags == None:
        return -3
    for tag in tags:
        if not -1 < tag.tag_id < 5:
            continue
        else:
            return tag.tag_id
    return -4       # AC - Added fallback state
            
def ground_cords(x, y, depth_frame, intrinsics):
     d = depth_frame.get_distance(x, y)
     point = rs.rs2_deproject_pixel_to_point(intrinsics, [x, y], d)
     X, Y, Z = point
     if d == 0:
        return None
     if Z == 0:  # Avoid division by zero
        return None
     if math.tan(C_T) - (Y / Z) <= 0:
        return None  # Object is too high or camera tilt is incorrect
     
     Z_ground = C_H / (math.tan(C_T) - (Y / Z))
     X_ground = X * (Z_ground / Z)

    # Compute r and theta relative to the ground
     r = math.sqrt(X_ground**2 + Z_ground**2)
     theta = math.atan2(X_ground, Z_ground)  # Angle in radians

     return r, theta
            
def object_detection(depth_frame, color_frame, intrinsics):

    global_manager.clear_all_objects()

    count = 0
        

    if not depth_frame or not color_frame:
            return -2

    # Convert images to numpy arrays
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # -------------------------------
    # Object detection by color
    # -------------------------------
    # Convert BGR to HSV color space for easier color segmentation
    hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

    # Define HSV ranges for the target color.
    # Here we demonstrate for red objects. Adjust these values for your needs.
    lower_purple = np.array([115, 35, 35])  # Lower saturation & value thresholds
    upper_purple = np.array([165, 255, 255])  # Extend the upper range
    # Create masks and combine them
    mask = cv2.inRange(hsv, lower_purple, upper_purple)


    # Optional: Apply some morphological operations to remove noise
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    # -------------------------------
    # Find contours of the detected objects
    # -------------------------------
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if not contours:
            return 0
        area = cv2.contourArea(cnt)
        # Filter out small contours/noise by area threshold (adjust as needed)
        if area < 100:
            continue

        # Get bounding box around the contour
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Compute the centroid of the contour for a better depth measurement
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = x + w // 2, y + h // 2

        result = ground_cords(cx, cy, depth_frame, intrinsics)
        if result == None:
           return -1
        r, theta = result

        if not global_manager.check_object(r, theta):
           global_manager.add_object(r, theta)

    current_manager = global_manager

    return current_manager


def control(wall, object, april_parameter):     # AC - changed name of april parameter to not interfere with function
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # Depth stream
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)  # Color stream

    pipeline.start(config)

    align_to = rs.stream.color
    align = rs.align(align_to)

    profile = pipeline.get_active_profile()
    depth_stream = profile.get_stream(rs.stream.depth)  # Get depth stream profile
    intrinsics = depth_stream.as_video_stream_profile().get_intrinsics()

    count = 0

    wall_r = None
    object_r = None
    april_r = None

    if wall == 1:
       while True:
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        wall_r = wall(depth_frame) 
        count = count + 1
        if wall_r > 0:
            return wall_r
        if count == 10:
            break
        return wall_r


    
    if object == 1:
        while True:
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            object_r = object_detection(depth_frame, color_frame, intrinsics)
            count = count + 1
            if count == 15:
                break
            if object_r == 0:
                #error message'
                break
            if object_r == -1:
                continue

            if object_r == -2:
                continue
                #error message
            else:
                return object_r
        

    if april_parameter == 1:    # AC - changed the name of this as it was trying to call it as a function
        while True:
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()

            april_r = april(color_frame)

            if april_r == -1:
                continue
            if april_r == -2:
                continue
            if april_r == -3:       # AC - changed april to april_r.
                return -1
            if april_r == -4:
                return -1

            if april_r:             # AC - Added this line, because it was returning nonetype
                if -1 < april_r < 5:
                    return april_r

            else:
                count = count + 1
                if count > 20:
                    break
                continue

    pipeline.stop()
    cv2.destroyAllWindows()



            
                