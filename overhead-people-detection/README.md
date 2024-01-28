# Overhead people detection using drones

During disasters, it is crucial to pay attention to people who may be stuck in rooftops or inaccessible areas. Autonomous drones equipped with overhead people detection capabilities can greatly aid in rescue efforts and potentially save more lives. Here are some benefits of using autonomous drones for overhead people detection:

- **Efficiency**: Drones can cover large areas quickly, providing a faster response time compared to traditional search and rescue methods.

- **Safety**: By using drones, rescue teams can avoid putting themselves in potentially dangerous situations, reducing the risk to human lives.

- **Accuracy**: Drones equipped with advanced sensors and computer vision algorithms can accurately detect and count the number of people in a given area.

- **Location tracking**: The overhead detection capabilities of drones allow for precise location tracking of individuals, enabling rescue teams to reach them more effectively.

- **Real-time data**: Drones can provide real-time data and live video feeds, allowing rescue teams to make informed decisions and prioritize their efforts.


# Usage

## 1. Install dependencies

```
pip install -r requirements.txt
```

## 2. Run the demo

```
python example.py
```
The count of people detected is displayed on the terminal along with the location coordinates.

#### or

```
streamlit run app.py
```
The count of people detected is displayed on the screen along with the location coordinates.


- Both of these connects automatically to the webcam and starts detecting people, once every 2 seconds, and displays the resulting frame separately.

- If different video source is connected, it automatically picks the other video source.

- Modify variable in cv2.VideoCapture('variable') to change the video source.


# Future Scope

- The model can be trained on a larger dataset to improve the accuracy of the model.

- Food and medicine delivery can be integrated with the drones to provide immediate relief to the people in need.

