from dependencies import *
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical # type: ignore
from keras.models import Sequential # type: ignore
from keras.layers import LSTM, Dense # type: ignore
from keras.callbacks import TensorBoard # type: ignore

# Map actions to numerical labels
label_map = {label: num for num, label in enumerate(actions)}

# Initialize sequences and labels
sequences, labels = [], []

# Loop through actions and sequences to load data
for action in actions:
    for sequence in range(no_sequences):
        window = []
        for frame_num in range(sequence_length):
            res = np.load(os.path.join(DATA_PATH, action, str(sequence), "{}.npy".format(frame_num)), allow_pickle=True)
            
            # Ensure that the shape of each keypoint set is consistent (63 = 21 landmarks * 3 coordinates)
            if res.shape != (63,):
                print(f"Error: Shape mismatch in {action} sequence {sequence} frame {frame_num}. Expected shape (63,), got {res.shape}.")
                continue  # Skip this frame if there's a shape mismatch
            
            window.append(res)
        
        # Ensure that each sequence has exactly 30 frames (trim or pad if necessary)
        if len(window) == sequence_length:
            sequences.append(window)
            labels.append(label_map[action])
        else:
            print(f"Skipping sequence {sequence} for action {action} due to incorrect length: {len(window)}")

# Convert sequences and labels to NumPy arrays
X = np.array(sequences)
y = to_categorical(labels).astype(int)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

# Set up TensorBoard for logging
log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)

# Build the LSTM model
model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30, 63)))  # 30 frames, 63 keypoints
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

# Compile the model
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=200, callbacks=[tb_callback])

# Print model summary
model.summary()

# Save the model architecture to a JSON file
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

# Save the trained model
model.save('model.h5')
