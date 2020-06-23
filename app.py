#posture-corrector/app.py

import logging
import time
import edgeiq
import os
import json
from posture import CheckPosture
import numpy as np

"""
Modifies realtime_pose_estimator to detect whether a person is exhibiting
improper posture (as defined in CheckPosture).

Proper posture functions are defined in the 'CheckPosture' class and imported.

This app uses a configuration file (config.json) to configure a
'scale' factor, which is used to make the posture calculations more or less stringent.
A larger scale factor (>1) makes the calculation less stringent (allows for less straight
posture).
"""
CONFIG_FILE = "config.json"
SCALE = "scale"

def load_json(filepath):
    # check that the file exists and return the loaded json data
    if os.path.exists(filepath) == False:
        raise Exception('File at {} does not exist'.format(filepath))

    with open(filepath) as data:
        return json.load(data)

def main():
    # load the configuration data from config.json
    config = load_json(CONFIG_FILE)
    scale = config.get(SCALE)

    pose_estimator = edgeiq.PoseEstimation("alwaysai/human-pose")

    pose_estimator.load(
            engine=edgeiq.Engine.DNN,
            accelerator=edgeiq.Accelerator.CPU)

    print("Loaded model:\n{}\n".format(pose_estimator.model_id))
    print("Engine: {}".format(pose_estimator.engine))
    print("Accelerator: {}\n".format(pose_estimator.accelerator))

    fps = edgeiq.FPS()

    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream, \
                edgeiq.Streamer() as streamer:
            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            posture = CheckPosture(scale)

            # loop detection
            while True:
                frame = video_stream.read()
                results = pose_estimator.estimate(frame)
                # Generate text to display on streamer
                text = ["Model: {}".format(pose_estimator.model_id)]
                text.append(
                        "Inference time: {:1.3f} s".format(results.duration))
                for ind, pose in enumerate(results.poses):
                    text.append("Person {}".format(ind))
                    text.append('-'*10)
                    text.append("Key Points:")

                    # update the instance key_points to check the posture
                    posture.set_key_points(pose.key_points)

                    correct_posture = posture.correct_posture()
                    if not correct_posture:
                        text.append(posture.build_message())
                        
                        # make a sound to alert the user to improper posture
                        print("\a")

                streamer.send_data(results.draw_poses(frame), text)

                fps.update()

                if streamer.check_exit():
                    break
    finally:
        fps.stop()
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))

        print("Program Ending")


if __name__ == "__main__":
    main()
