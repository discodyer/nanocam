import cv2
import requests
import numpy as np

# 设置流媒体服务器的URL
stream_url = "http://10.144.77.1:8000/stream"

def fetch_stream(url):
    """ 从指定的URL不断获取JPEG流并转换为OpenCV图像 """
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        bytes = b''
        for chunk in r.iter_content(chunk_size=4096):
            bytes += chunk
            # 在缓存中不断搜索JPEG的结束标记
            while b'\xff\xd8' in bytes and b'\xff\xd9' in bytes:
                start = bytes.find(b'\xff\xd8')
                end = bytes.find(b'\xff\xd9', start) + 2
                jpg = bytes[start:end]
                bytes = bytes[end:]
                img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                if img is not None:
                    cv2.imshow('Frame', img)
                    # 如果按下'q'键则退出循环
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        cv2.destroyAllWindows()
    else:
        print("Failed to connect to the stream.")

if __name__ == "__main__":
    fetch_stream(stream_url)