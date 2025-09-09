import os
import numpy as np
import time
from sensor_msgs.msg import PointCloud2, PointField, CompressedImage
from std_msgs.msg import Header
from rclpy.serialization import serialize_message
from mcap.writer import Writer
import cv2
import sys

def definition_pointcloud2(points,width,height,frame_id="camera",stamp=None):
    header= Header()
    header.stamp.sec= int(stamp)
    header.stamp.nanosec= int((stamp-header.stamp.sec)*1e9)
    header.frame_id= frame_id


    fields=[
        PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
        PointField(name='y', offset= 4, datatype=PointField.FLOAT32, count=1),
        PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
        PointField(name='intensidad', offset=12, datatype=PointField.FLOAT32, count=1)
    ]
    datos= points.astype(np.float32).tobytes()

    return PointCloud2(
        header=header,
        height=height,
        width=width,
        fields=fields,
        is_bigendian=False,
        is_dense=True,
        point_step=16,
        row_step=16*width,
        data=datos,
    
    )

def definition_CompressedImage(image_path, frame_id="map", stamp=None):
    header=Header()
    header.stamp.sec= int(stamp)
    header.stamp.nanosec= int((stamp-header.stamp.sec)*1e9)
    header.frame_id= frame_id 
    image= cv2.imread(image_path)
    if image is None:
        raise ValueError(f"no se ha podido leer la imagen {image_path}")
    ret,buffer= cv2.imencode('.png', image)
    if not ret:
        raise ValueError(f"no se ha podido codificar la imagen {image_path}")
    

    return CompressedImage(
        header=header,
        format="png",
        data=buffer.tobytes()
    )

def lectura_pcd(pcd_file):
    with open(pcd_file,'r') as f:
        lines=f.readlines()

    datos={}
    for line in lines:
        if line.startswith('WIDTH'):
            datos('width')=int((line.split()[1]))
        if line.startswith('HEIGHT'):
            datos('height')=int((line.split()[1]))
        if line.strip().startswith('DATA'):
            inicio_datos= lines.index(line)+1
            break
    puntos= np.loadtxt(lines[inicio_datos:])
    return puntos, datos 

def cargar_timestamps(txt_file):
    timestamps={}
    with open(txt_file,'r') as f:
        for line in f:
            index, ts= line.strip().split(",")
            timestamps[int(index)]=float(ts)
    return timestamps

def pcd_images_to_mcap(input_folder,image_folder,output_mcap,timestamp_txt):
    img_files= sorted([f for f in os.listdir(image_folder) if f.endswith(('.png','.jpg','.jpeg'))])
    pcd_files=sorted([f for f in os.listdir(input_folder) if f.endswith('.pcd')])
    timestamps= cargar_timestamps(timestamp_txt)

    if not pcd_files:
        raise ValueError("No se han encontrado archivos .pcd.")
    if not img_files:   
        raise ValueError("No se han encontrado archivos .png")
    
    with open(output_mcap,'wb') as f:
        writer= Writer(f)

        #pcd
        pc2_schema = writer.register_schema(
            name="sensor_msgs/msg/PointCloud2",
            encoding="ros2msg",
            data=b"""
                std_msgs/Header header
                uint32 height
                uint32 width
                sensor_msgs/PointField[] fields
                bool is_bigendian
                uint32 point_step
                uint32 row_step
                uint8[] data
                bool is_dense
                ================================================================================
                MSG: std_msgs/Header
                builtin_interfaces/Time stamp
                string frame_id

                ================================================================================
                MSG: builtin_interfaces/Time
                int32 sec
                uint32 nanosec

                ================================================================================
                MSG: sensor_msgs/PointField
                string name
                uint32 offset
                uint8 datatype
                uint32 count
            """
        )

        pc2_channel = writer.register_channel(
            topic="/pointcloud",
            message_encoding="cdr",
            schema_id=pc2_schema,
            metadata={}
        )

        img_schema = writer.register_schema(
            name="sensor_msgs/msg/CompressedImage",
            encoding="ros2msg",
            data=b"""
                std_msgs/Header header
                string format
                uint8[] data

                ================================================================================
                MSG: std_msgs/Header
                builtin_interfaces/Time stamp
                string frame_id

                ================================================================================
                MSG: builtin_interfaces/Time
                int32 sec
                uint32 nanosec
            """
        )

        img_channel = writer.register_channel(
            topic="/camera/image/compressed",
            message_encoding="cdr",
            schema_id=img_schema,
            matadata={}
        )

        writer.start()

        for i, (pcd_name,image_name) in enumerate(zip(pcd_files,img_files)):
            timestamp= timestamps.get(i)
            
            try:
                pcd_path= os.path.join(input_folder,pcd_name)
                puntos, datos_pcd= lectura_pcd(pcd_path)
                
                pc_msg= definition_pointcloud2(
                    puntos,
                    width=datos_pcd.get("width",puntos.shape[0]),
                    height=datos_pcd.get("height",1),
                    frame_id="map",
                    stamp=timestamp
                )

                img_path= os.path.join(image_folder,image_name)
                img_msg= definition_CompressedImage(img_path, stamp=timestamp)

                timestamp_ns= int(timestamp*1e9)

                writer.add_message(
                    channel_id=pc2_channel,
                    log_time=timestamp_ns,
                    publish_time=timestamp_ns,
                    data=serialize_message(pc_msg)
                )

                writer.add_message(
                    channel_id=img_channel,
                    log_time=timestamp_ns,
                    publish_time=timestamp_ns,
                    data=serialize_message(img_msg)
                )

            except Exception as e:
                print(f"Error al procesar el índice {i}: {e}")

        writer.finish()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Para usar el script: python3 pcd_img_to_mcap <pcd_folder> <image_folder> <output_file.mcap> <timestamps.txt>")
        sys.exit(1)

    input_folder = sys.argv[1]
    image_folder = sys.argv[2]
    output_file = sys.argv[3]
    timestamp_txt = sys.argv[4]

    pcd_images_to_mcap(input_folder, image_folder, output_file, timestamp_txt)





                



        

