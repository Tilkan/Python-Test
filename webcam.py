colors = visualize.random_colors(len(class_names))

gentle_grey = (45, 65, 79)
white = (255, 255, 255)

OPTIMIZE_CAM = False
SHOW_FPS = False
SHOW_FPS_WO_COUNTER = True # faster
PROCESS_IMG = True


if OPTIMIZE_CAM:
    vs = WebcamVideoStream(src=0).start()
else:
    vs = cv2.VideoCapture(0)

if SHOW_FPS:
    fps_caption = "FPS: 0"
    fps_counter = 0
    start_time = time.time()

SCREEN_NAME = 'Mask RCNN LIVE'
cv2.namedWindow(SCREEN_NAME, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(SCREEN_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    # Capture frame-by-frame
    if OPTIMIZE_CAM:
        frame = vs.read()
    else:
        grabbed, frame = vs.read()
        if not grabbed:
            break
    
    if SHOW_FPS_WO_COUNTER:
        start_time = time.time() # start time of the loop

    if PROCESS_IMG:    
        results = model.detect([frame])
        r = results[0]

        # Run detection
        masked_image = visualize.display_instances_10fps(frame, r['rois'], r['masks'], 
            r['class_ids'], class_names, r['scores'], colors=colors, real_time=True)
        
    if PROCESS_IMG:
        s = masked_image
    else:
        s = frame
    # print("Image shape: {1}x{0}".format(s.shape[0], s.shape[1]))

    width = s.shape[1]
    height = s.shape[0]
    top_left_corner = (width-120, height-20)
    bott_right_corner = (width, height)
    top_left_corner_cvtext = (width-80, height-5)

    if SHOW_FPS:
        fps_counter+=1
        if (time.time() - start_time) > 5 : # every 5 second
            fps_caption = "FPS: {:.0f}".format(fps_counter / (time.time() - start_time))
            # print(fps_caption)
            fps_counter = 0
            start_time = time.time()
        ret, baseline = cv2.getTextSize(fps_caption, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(s, (width - ret[0], height - ret[1] - baseline), bott_right_corner, gentle_grey, -1)
        cv2.putText(s,fps_caption, (width - ret[0], height - baseline), cv2.FONT_HERSHEY_SIMPLEX, 0.5, white, lineType=cv2.LINE_AA)

    if SHOW_FPS_WO_COUNTER:
        # Display the resulting frame
        fps_caption = "FPS: {:.0f}".format(1.0 / (time.time() - start_time))
        # print("FPS: ", 1.0 / (time.time() - start_time))
        
        # Put the rectangle and text on the bottom left corner
        ret, baseline = cv2.getTextSize(fps_caption, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(s, (width - ret[0], height - ret[1] - baseline), bott_right_corner, gentle_grey, -1)
        cv2.putText(s, fps_caption, (width - ret[0], height - baseline),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, white, 1, lineType=cv2.LINE_AA)

    
    s = cv2.resize(s,(1920,1080))
    cv2.imshow(SCREEN_NAME, s)
    cv2.waitKey(1)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    
# When everything done, release the capture
if OPTIMIZE_CAM:
    vs.stop()
else:
    vs.release()
cv2.destroyAllWindows()
