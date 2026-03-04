class SignalController:
    """
    Controls traffic signal timings based on congestion level
    and predicted traffic.
    """

    def __init__(self):

        # Default signal timings in seconds
        self.default_green = 30
        self.medium_green = 45
        self.high_green = 60

    def decide_signal_time(self, congestion_level, predicted_traffic=None):

        decision = {}

        if congestion_level == "High":
            green_time = self.high_green

        elif congestion_level == "Medium":
            green_time = self.medium_green

        else:
            green_time = self.default_green

        decision["green_signal_time"] = green_time
        decision["congestion_level"] = congestion_level
        decision["predicted_traffic"] = predicted_traffic

        return decision

    def lane_signal_plan(self, lanes, congestion_level):

        """
        Assign signal timings to each lane
        """

        signal_plan = {}

        for lane in lanes:

            if congestion_level == "High":
                signal_plan[lane] = 60

            elif congestion_level == "Medium":
                signal_plan[lane] = 45

            else:
                signal_plan[lane] = 30

        return signal_plan