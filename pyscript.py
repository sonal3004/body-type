import cv2
import mediapipe as mp
import numpy as np
import random
import os
import json
from PIL import Image

# Simulate file upload
input_image_path = "C:\\Users\\PC\\Desktop\\body-estimator\\BodyType_Images\\Apple\\Female\\Outfits\\000010.jpg"  # Replace with actual image path
image = cv2.imread(input_image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

result = {}

with mp_pose.Pose(static_image_mode=True) as pose:
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]

        if (left_shoulder.visibility > 0.5 and right_shoulder.visibility > 0.5 and
            left_hip.visibility > 0.5 and right_hip.visibility > 0.5):

            shoulder_width = abs(left_shoulder.x - right_shoulder.x)
            hip_width = abs(left_hip.x - right_hip.x)
            waist_width = (shoulder_width + hip_width) / 2

            shoulder_waist_ratio = shoulder_width / waist_width
            hip_waist_ratio = hip_width / waist_width

            if shoulder_waist_ratio > 1.1 and hip_waist_ratio > 1.1:
                body_type = "Hourglass"
            elif shoulder_width > hip_width and shoulder_waist_ratio > 1.1:
                body_type = "Inverted Triangle"
            elif hip_width > shoulder_width and hip_waist_ratio > 1.1:
                body_type = "Pear"
            elif abs(shoulder_width - hip_width) < 0.05:
                body_type = "Rectangle"
            else:
                body_type = "Unknown"

            gender = "Female"  # Set manually or from user input if needed

            suggestions = {
                "Apple": {
                    "description": "You have a broader upper body and a fuller midsection.",
                    "exercise": ["Focus on cardio exercises like brisk walking and cycling.",
                                 "Strengthen your core with planks and crunches."],
                    "yoga": ["Practice the Bridge Pose to strengthen the spine.",
                             "Include Boat Pose to tone the abdominal muscles."],
                    "outfit": {
                        "Female": "Prefer empire waist dresses, V-neck tops, and flowy tunics with A-line skirts.",
                        "Male": "Choose structured blazers, dark shirts, and relaxed-fit trousers."
                    },
                    "posture": ["Maintain proper spine alignment while sitting.",
                                "Avoid leaning forward postures during walking and standing."]
                },
                "Pear": {
                    "description": "Your hips are wider than your shoulders, giving a pear-shaped figure.",
                    "exercise": ["Strengthen your lower body with lunges and squats.",
                                 "Incorporate cycling to tone your legs."],
                    "yoga": ["Chair Pose (Utkatasana) to build lower body strength.",
                             "Warrior II Pose "],
                    "outfit": {
                        "Female": "Try A-line skirts, darker bottoms, and boat-neck or detailed tops.",
                        "Male": "Wear slim-fit shirts and lighter upper wear with straight pants."
                    },
                    "posture": ["Strengthen glutes and lower back muscles.",
                                "Practice standing tall without slouching."]
                },
                "Hourglass": {
                    "description": "You have balanced shoulders and hips with a well-defined waist.",
                    "exercise": ["Go for full-body workouts like Pilates and strength training.",
                                 "Maintain overall fitness with cardio."],
                    "yoga": ["Cobra Pose to enhance flexibility.",
                             "Triangle Pose to tone the sides."],
                    "outfit": {
                        "Female": "Wear fitted dresses, wrap tops, and high-waist pants to highlight your waist.",
                        "Male": "Prefer fitted blazers, tucked-in shirts, and slim trousers."
                    },
                    "posture": ["Maintain a neutral spine posture.",
                                "Avoid overarching your lower back while sitting."]
                },
                "Rectangle": {
                    "description": "Your body is straight with similar measurements for shoulders, waist, and hips.",
                    "exercise": ["Engage in strength training and core workouts.",
                                 "Add HIIT routines to improve overall muscle tone."],
                    "yoga": ["Camel Pose for opening the chest.",
                             "Bow Pose to strengthen the back."],
                    "outfit": {
                        "Female": "Wear peplum tops, ruffled sleeves, and belted waistlines.",
                        "Male": "Layer clothing with jackets and bomber jackets for a structured look."
                    },
                    "posture": ["Focus on building stronger shoulders and glutes.",
                                "Practice exercises that enhance body definition."]
                },
                "Inverted Triangle": {
                    "description": "You have broad shoulders with narrower hips.",
                    "exercise": ["Focus on lower body strength with squats and glute bridges.",
                                 "Balance proportions with targeted leg workouts."],
                    "yoga": ["Tree Pose to improve balance and focus.",
                             "Downward Dog to lengthen the spine and relieve tension."],
                    "outfit": {
                        "Female": "Opt for flared skirts and wide-leg trousers with simple tops.",
                        "Male": "Wear straight pants and avoid heavy shoulder padding."
                    },
                    "posture": ["Stretch your shoulders regularly.",
                                "Strengthen your core to support better posture."]
                }
            }

            def get_image_paths(body_type, gender, category, count=2):
                folder_path = f"BodyType_Images/{body_type}/{gender}/{category}"
                if os.path.exists(folder_path):
                    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png'))]
                    if len(image_files) >= count:
                        selected_images = random.sample(image_files, count)
                        return [os.path.join(folder_path, img) for img in selected_images]
                return []

            if body_type in suggestions:
                s = suggestions[body_type]
                result = {
                    "body_type": body_type,
                    "gender": gender,
                    "description": s["description"],
                    "exercise": {
                        "tips": s["exercise"],
                        "images": get_image_paths(body_type, gender, "Exercise")
                    },
                    "yoga": {
                        "tips": s["yoga"],
                        "images": get_image_paths(body_type, gender, "Yoga")
                    },
                    "outfit": {
                        "tips": s["outfit"][gender],
                        "images": get_image_paths(body_type, gender, "Outfits")
                    },
                    "posture": s["posture"]
                }

                # Dump to JSON
                result_json = json.dumps(result, indent=4)
                print(result_json)

            else:
                print("❗ No detailed suggestions available for detected body type.")
        else:
            print("🙈 Body not clearly detected. Please use a clearer, front-facing image.")
    else:
        print("😕 No body detected — please upload a full, front-facing image with good lighting.")
