import cv2
import numpy as np
import time


def get_the_bbox(contrs):
    if  bool(contrs):
        array_of_points = contrs[0]
        for x in contrs[1:]:
            array_of_points = np.vstack((array_of_points,x))
        x = np.min(array_of_points,axis = 0)[0][0]
        y = np.min(array_of_points,axis = 0)[0][1]
        r = np.max(array_of_points,axis=0)[0][0]
        b = np.max(array_of_points,axis=0)[0][1]
        return x,y,r,b
    else:
        return "None"

def motion_detection(source = 0, output = None, fps = 25, sensitivity = 5, show_all_windows = True):
    
    cap = cv2.VideoCapture(source)
   
    
    # Get the Default resolutions
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    
    if output != None:
        codec = cv2.VideoWriter_fourcc(*'DIVX')
        out = cv2.VideoWriter(output, codec, fps, (frame_width,frame_height))
    
    
    ret, first_frame = cap.read()
    
    first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    first_frame = cv2.GaussianBlur(first_frame, (19,21), 0) 
    
    
    while cap.isOpened():
        
        ret, image = cap.read()
        if ret == True:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            gray = cv2.GaussianBlur(gray, (19,21), 0) 
            
            diff = cv2.absdiff(gray, first_frame)
            _,thresh = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)
            
            thresh = cv2.dilate(thresh, None, iterations = sensitivity)
                    
            contoures, hier = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if bool(contoures):
                x,y,r,b = get_the_bbox(contoures)
            
                cv2.rectangle(image, (x,y),(r,b), (0,0,255), 2)
                
                cv2.putText(image, 
                            'Motion Spoted', 
                            (x,y - 3),  
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0,0,255))
            if output != None:
                out.write(image)    
            
            cv2.imshow('Stream', image)
            
            
            if show_all_windows:
                cv2.imshow('Frame', diff)
                
                cv2.imshow('Thresh', thresh)
            
            
            
            
          
            if cv2.waitKey(1) & 0xFF == ord('q'):
              break
            first_frame = gray
            time.sleep(0.05)
        # Break the loop
        else: 
            break
    
    cap.release()
    
    out.release()
    
    cv2.destroyAllWindows()
    
