
from torch.utils.data import Dataset, DataLoader
import os
import gym
import torch
import numpy as np
import imageio
import wandb
import gymnasium as gym
import gym_lowcostrobot  # Import the low-cost robot environments
from stable_baselines3 import PPO

from Behavior_cloning import train_bc_model
from DataSet import ImitationDataset
from CollecteData import collect_demonstrations

def main_imitation():
    # Charger l'environnement
    env_id = "PickPlaceCube-v0"
    env = gym.make(env_id)
    # Charger un modèle expert
    expert_model = PPO.load("PickPlaceCube-v0_ppo_model")

    # Collecte des démonstrations
    demonstrations = collect_demonstrations(
        env, expert_model, num_episodes=100)

    # Création du dataset
    dataset = ImitationDataset(demonstrations)
    input_dim = env.observation_space.shape[0]
    output_dim = env.action_space.n

    # Entraînement du modèle BC
    bc_model = train_bc_model(dataset, input_dim, output_dim)

    # Évaluation du modèle
    evaluate_bc_model(bc_model, env)


def evaluate_bc_model(model, env, num_episodes=10):
    """
    Évalue le modèle BC dans l'environnement.
    
    Args:
        model: Modèle BC entraîné.
        env: Environnement Gym.
        num_episodes: Nombre d'épisodes d'évaluation.
    """
    total_rewards = []

    for episode in range(num_episodes):
        obs = env.reset()[0]
        done = False
        total_reward = 0

        while not done:
            obs_tensor = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)
            action = model(obs_tensor).argmax().item()
            obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            total_reward += reward

        total_rewards.append(total_reward)
        print(f"Episode {episode + 1}/{num_episodes} - Reward: {total_reward}")

    print(f"Reward moyen: {np.mean(total_rewards):.2f}")


if __name__ == "__main__":
    main_imitation()
