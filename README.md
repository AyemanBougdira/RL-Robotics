<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Configuration de l'Environnement RL Robotics</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            line-height: 1.6; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        pre { 
            background-color: #f4f4f4; 
            border: 1px solid #ddd; 
            border-radius: 4px; 
            padding: 10px; 
            overflow-x: auto; 
        }
        .error { color: red; }
        .note { color: blue; }
    </style>
</head>
<body>
    <h1>Configuration de l'Environnement RL Robotics</h1>

    <h2>Étapes de Configuration</h2>

    <h3>1. Création de l'Environnement Conda</h3>
    <pre><code>conda create -y -n RLrobotics python=3.10
conda activate RLrobotics</code></pre>

    <h3>2. Installation des Dépendances</h3>
    <pre><code>pip install gym stable-baselines3
pip install rl_zoo3</code></pre>

    <h3>3. Gestion des Erreurs</h3>
    <p class="error">Erreur: attribut 'convexhull' non reconnu</p>

    <h3>4. Modification du Fichier XML</h3>
    <p>Localiser et modifier le fichier <code>pick_place_cube.xml</code>:</p>

    <h4>Trouver l'emplacement du package</h4>
    <pre><code>import gym_lowcostrobot
import os
# Imprimer l'emplacement du package
print(os.path.dirname(gym_lowcostrobot.__file__))</code></pre>

    <h4>Commandes PowerShell pour localiser et modifier le fichier</h4>
    <pre><code>Get-ChildItem -Path C:\Anaconda3\Lib\site-packages\gym_lowcostrobot -Recurse -Filter "pick_place_cube.xml"
type "C:\Anaconda3\envs\RLrobotics\lib\site-packages\gym_lowcostrobot\assets\low_cost_robot_6dof\pick_place_cube.xml"</code></pre>

    <h4>Contenu du Fichier XML à Remplacer</h4>
    <pre><code>&lt;mujoco model="low_cost_robot scene"&gt;
    &lt;compiler angle="radian" autolimits="true"/&gt;
    &lt;!-- Le pas de temps a une grande influence sur la stabilité des contacts --&gt;
    &lt;option cone="elliptic" impratio="10" timestep="0.005" gravity="0 0 -9.81"/&gt;
    &lt;include file="follower.xml"/&gt;
    &lt;statistic center="0 0 0.1" extent="0.6"/&gt;
    &lt;visual&gt;
        &lt;headlight diffuse="0.6 0.6 0.6" ambient="0.3 0.3 0.3" specular="0 0 0"/&gt;
        &lt;rgba haze="0.15 0.25 0.35 1"/&gt;
        &lt;global azimuth="150" elevation="-20" offheight="640"/&gt;
    &lt;/visual&gt;
    &lt;asset&gt;
        &lt;texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0 0 0" width="512" height="3072"/&gt;
        &lt;texture type="2d" name="groundplane" builtin="checker" mark="edge" rgb1="0.2 0.3 0.4" rgb2="0.1 0.2 0.3"
            markrgb="0.8 0.8 0.8" width="300" height="300"/&gt;
        &lt;material name="groundplane" texture="groundplane" texuniform="true" texrepeat="5 5" reflectance="0.2"/&gt;
    &lt;/asset&gt;
    &lt;worldbody&gt;
        &lt;light pos="0 0 3" dir="0 0 -1" directional="false"/&gt;
        &lt;geom name="floor" size="0 0 0.05" type="plane" material="groundplane" pos="0 0 0" friction="0.1"/&gt;
        &lt;body name="cube" pos="0.0 0.2 0.01"&gt;
            &lt;freejoint name="red_box_joint"/&gt;
            &lt;inertial pos="0 0 0" mass="10" diaginertia="0.00016667 0.00016667 0.00016667"/&gt;
            &lt;geom friction="0.5" condim="4" pos="0 0 0" size="0.015 0.015 0.015" type="box" name="red_box" rgba="0.5 0 0 1" priority="1"/&gt;
        &lt;/body&gt;
        &lt;camera name="camera_front" pos="0.049 0.5 0.225" xyaxes="-0.998 0.056 -0.000 -0.019 -0.335 0.942"/&gt;
        &lt;camera name="camera_top" pos="0 0.1 0.6" euler="0 0 0" mode="fixed"/&gt;
        &lt;camera name="camera_vizu" pos="-0.1 0.6 0.3" quat="-0.15 -0.1 0.6 1"/&gt;
        &lt;geom name="target_region" type="cylinder" pos=".06 .135 0.005" size="0.035 0.01" rgba="0 0 1 0.3" contype="0" conaffinity="0" /&gt;
    &lt;/worldbody&gt;
&lt;/mujoco&gt;</code></pre>

    <p class="note">Note: Utilisez la commande PowerShell fournie pour remplacer le contenu du fichier.</p>
</body>
</html>
