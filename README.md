# Posture Corrector with Pose Estimation Example App
This app uses pose estimation to help users correct their posture by alerting them with a custom audio file when they
are slouching, leaning, or tilting their head down. As an extra bonus, this branch includes some image markup, to show
the offending posture, as well as a custom wav file for a personalized reminder to sit up straight.
A **scale** variable is used to adjust the keypoints measurements for different individuals, accounting for greater or
smaller natural distances between keypoints used to detect poor posture.

## Requirements
To run this app, you will need an alwaysAI account. Please register at https://alwaysai.co/auth?register=true

## Setup
Easy start up guides can be found following registration. Please see the docs page for more information: https://alwaysai.co/docs/getting_started/introduction.html

### Models
The pose estimation model used is the 'alwaysai/human-pose' model, and more details can be found at https://alwaysai.co/model-catalog?model=alwaysai/human-pose


You can alter the code to used different detection and classification models: https://alwaysai.co/docs/application_development/changing_the_model.html


## Troubleshooting
If you are having trouble connecting to your edge device, use the CLI configure command to reset the device.
Please see the following page for more details: https://alwaysai.co/docs/reference/cli_commands.html

You can also post questions and comments on our Discord Community at: https://discord.gg/R2uM36U