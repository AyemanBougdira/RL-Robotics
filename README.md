# Instructions d'installation et de configuration pour RLrobotics

## Étape 1 : Installation des dépendances

Exécutez les commandes suivantes dans votre terminal pour créer un environnement Conda et installer les bibliothèques nécessaires :

```bash
conda create -y -n RLrobotics python=3.10
conda activate RLrobotics

pip install git+https://github.com/perezjln/gym-lowcostrobot.git
pip install gym stable-baselines3
pip install rl_zoo3
pip install imageio[ffmpeg]
pip install imageio[pyav]
```

## ValueError: XML Error: Schema violation: unrecognized attribute: 'convexhull'

L'erreur unrecognized attribute: 'convexhull' aprés l'execution du script validationenv.py provient du fichier XML de configuration. Voici les étapes pour localiser et modifier ce fichier.

### Localisation du fichier XML (executer test.py  pour trouver le chemin)

```bash
import gym_lowcostrobot
import os

# Affiche le chemin du package
print(os.path.dirname(gym_lowcostrobot.__file__))
```

le résultat est le suivant:

```bash
C:\Anaconda3\envs\RLrobotics\lib\site-packages\gym_lowcostrobot
```


Pour corriger l'erreur, remplacez le contenu du fichier pick_place_cube.xml par le texte suivant (changer la dernier ligne par votre chemin)! :

 

```bash
@'
<mujoco model="low_cost_robot scene">
    <compiler angle="radian" autolimits="true"/>
    <!-- The timestep has a big influence on the contacts stability -->
    <option cone="elliptic" impratio="10" timestep="0.005" gravity="0 0 -9.81"/>
    <include file="follower.xml"/>
    <statistic center="0 0 0.1" extent="0.6"/>
    <visual>
        <headlight diffuse="0.6 0.6 0.6" ambient="0.3 0.3 0.3" specular="0 0 0"/>
        <rgba haze="0.15 0.25 0.35 1"/>
        <global azimuth="150" elevation="-20" offheight="640"/>
    </visual>
    <asset>
        <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0 0 0" width="512" height="3072"/>
        <texture type="2d" name="groundplane" builtin="checker" mark="edge" rgb1="0.2 0.3 0.4" rgb2="0.1 0.2 0.3"
            markrgb="0.8 0.8 0.8" width="300" height="300"/>
        <material name="groundplane" texture="groundplane" texuniform="true" texrepeat="5 5" reflectance="0.2"/>
    </asset>
    <worldbody>
        <light pos="0 0 3" dir="0 0 -1" directional="false"/>
        <geom name="floor" size="0 0 0.05" type="plane" material="groundplane" pos="0 0 0" friction="0.1"/>
        <body name="cube" pos="0.0 0.2 0.01">
            <freejoint name="red_box_joint"/>
            <inertial pos="0 0 0" mass="10" diaginertia="0.00016667 0.00016667 0.00016667"/>
            <geom friction="0.5" condim="4" pos="0 0 0" size="0.015 0.015 0.015" type="box" name="red_box" rgba="0.5 0 0 1" priority="1"/>
        </body>
        <camera name="camera_front" pos="0.049 0.5 0.225" xyaxes="-0.998 0.056 -0.000 -0.019 -0.335 0.942"/>
        <camera name="camera_top" pos="0 0.1 0.6" euler="0 0 0" mode="fixed"/>
        <camera name="camera_vizu" pos="-0.1 0.6 0.3" quat="-0.15 -0.1 0.6 1"/>
        <geom name="target_region" type="cylinder" pos=".06 .135 0.005" size="0.035 0.01" rgba="0 0 1 0.3" contype="0" conaffinity="0" />
    </worldbody>
</mujoco>
'@ | Set-Content "C:\Anaconda3\envs\RLrobotics\lib\site-packages\gym_lowcostrobot\assets\low_cost_robot_6dof\pick_place_cube.xml"
```