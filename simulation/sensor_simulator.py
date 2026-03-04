import random
from simulation.traffic_generator import TrafficGenerator


class SensorSimulator:
    """
    Simulates IoT traffic sensors placed at different lanes/junctions.
    Each sensor reads traffic data from the generator and emits
    a network-like message.
    """

    def __init__(self, dataset_path):

        self.generator = TrafficGenerator(dataset_path)

        # Simulated sensor nodes (like network devices)
        self.sensors = {
            1: "North Lane Sensor",
            2: "East Lane Sensor",
            3: "South Lane Sensor",
            4: "West Lane Sensor"
        }

    def read_sensor(self):

        # Get next traffic data point
        data = self.generator.get_next_data()

        junction = data["junction"]
        vehicles = data["vehicle_count"]

        # Simulate average speed
        speed = random.randint(20, 60)

        sensor_message = {
            "sensor_id": junction,
            "sensor_name": self.sensors.get(junction, "Unknown Sensor"),
            "vehicle_count": vehicles,
            "avg_speed": speed,
            "timestamp": data["timestamp"]
        }

        return sensor_message

    def read_all_sensors(self):
        messages = []

        for sensor_id, sensor_name in self.sensors.items():
            data = self.generator.get_next_data()

            vehicles = data["vehicle_count"]

            speed = random.randint(20, 60)

            msg = {
                "sensor_id": sensor_id,
                "sensor_name": sensor_name,
                "vehicle_count": vehicles,
                "avg_speed": speed,
                "timestamp": data["timestamp"]
            }

            messages.append(msg)

        return messages