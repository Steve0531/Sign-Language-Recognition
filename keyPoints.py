from dependencies import *
from time import sleep

for action in actions: 
    for sequence in range(no_sequences):
        try: 
            os.makedirs(os.path.join(DATA_PATH, action, str(sequence)))
        except:
            pass

# Set mediapipe model 
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    # Loop through actions
    for action in actions:
        # Loop through sequences aka videos
        for sequence in range(no_sequences):
            # Loop through video length aka sequence length
            for frame_num in range(sequence_length):

                # Read image from disk
                frame = cv2.imread(f'Image/{action}/{sequence}.png')
                
                if frame is None:
                    print(f"Error: Image not found for {action}, sequence {sequence}")
                    continue  # Skip to next sequence

                # Make detections using MediaPipe
                image, results = mediapipe_detection(frame, hands)

                # Draw landmarks
                draw_styled_landmarks(image, results)

                # Display collection info on the frame
                if frame_num == 0:
                    cv2.putText(image, 'STARTING COLLECTION', (120,200), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 4, cv2.LINE_AA)
                    cv2.putText(image, f'Collecting frames for {action} Image Number {sequence}', (15,12), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                    cv2.imshow('OpenCV Feed', image)
                    cv2.waitKey(200)
                else: 
                    cv2.putText(image, f'Collecting frames for {action} Image Number {sequence}', (15,12), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                    cv2.imshow('OpenCV Feed', image)

                # Export keypoints
                keypoints = extract_keypoints(results)
                npy_path = os.path.join(DATA_PATH, action, str(sequence), str(frame_num))
                np.save(npy_path, keypoints)

                # Break on 'q' key
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

    cv2.destroyAllWindows()
