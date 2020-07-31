#slouch_detector/app.py

import logging
import time
import edgeiq
import os
import json
import simpleaudio as sa
from posture import CheckPosture
from draw import *

"""
Modifies realtime_pose_estimator to detect whether a person is exhibiting
improper posture of any kind.

Proper posture functions are defined in the 'CheckPosture' class and imported.

A custom .wav file is used to remind the user when they are not sitting up straight.
The audio file is specified in a configuration file (config.json), along with a
'scale' factor, which is used to make the posture calculations more or less stringent.
A larger scale factor (>1) makes the calculation less stringent (allows for less straight
posture).
"""
CONFIG_FILE = "config.json"
SCALE = "scale"
AUDIO_CLIP = "audio_clip"

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
    audio_clip = sa.WaveObject.from_wave_file(config.get(AUDIO_CLIP))

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

                    # update the instance key_points to check the posture
                    posture.set_key_points(pose.key_points)

                    # play a reminder if you are not sitting up straight
                    correct_posture = posture.correct_posture()
                    if not correct_posture:
                        text.append(posture.build_message())
                        draw_points(posture.get_data(), frame)


                    streamer.send_data(results.draw_poses(frame), text)
                    fps.update()

                    if not correct_posture:
                        sound_play = audio_clip.play()
                        sound_play.wait_done()

                if streamer.check_exit():
                    break
    finally:
        fps.stop()
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))

        print("Program Ending")


if __name__ == "__main__":
    main()
