import os
import gym
import torch
import numpy as np
import imageio
import wandb
import gymnasium as gym
import gym_lowcostrobot  # Import the low-cost robot environments
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import BaseCallback


class WandbCallback(BaseCallback):
    def __init__(self, verbose=0):
        super(WandbCallback, self).__init__(verbose)

    def _on_step(self) -> bool:
        # Log metrics to W&B at every step
        wandb.log({
            "reward": self.locals.get("rewards", 0),
            "length": self.num_timesteps
        })
        return True


def record_video(model, env, num_episodes=50, video_dir='./video', fps=30):
    """
    Enregistre les vidéos de simulations pour un modèle entraîné.
    
    Args:
        model: Le modèle RL entraîné.
        env: L'environnement Gym.
        num_episodes: Nombre d'épisodes à enregistrer.
        video_dir: Répertoire pour enregistrer les vidéos.
        fps: Frames par seconde pour les vidéos.
    """
    os.makedirs(video_dir, exist_ok=True)

    for episode in range(num_episodes):
        obs = env.reset()[0]  # Compatible avec gym version récente
        done = False
        frames = []
        total_reward = 0

        while not done:
            action, _ = model.predict(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            frame = env.render()
            if frame is not None:
                frames.append(frame)

            total_reward += reward

        video_path = os.path.join(video_dir, f'episode_{episode}.mp4')
        imageio.mimsave(video_path, frames, fps=fps)
        print(
            f"Episode {episode} enregistré : {video_path} - Récompense totale : {total_reward}")

        # Log video to W&B
        wandb.log({
            f"video/episode_{episode}": wandb.Video(video_path, fps=fps, format="mp4"),
            f"reward/episode_{episode}": total_reward
        })


def train_ppo_model(env_id="PickPlaceCube-v0", total_timesteps=700000):
    """
    Entraîne un modèle PPO sur un environnement donné.

    Args:
        env_id: Identifiant de l'environnement Gym.
        total_timesteps: Nombre total de pas pour l'entraînement.

    Returns:
        Le modèle entraîné.
    """
    # Initialiser W&B
    wandb.init(project="rl_pickplace", name="ppo_training", config={
        "env_id": env_id,
        "total_timesteps": total_timesteps,
        "learning_rate": 3e-4,
        "n_steps": 2048,
        "batch_size": 64,
        "n_epochs": 10,
        "gamma": 0.99,
        "gae_lambda": 0.95,
        "clip_range": 0.2
    })

    # Configuration du dispositif
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"CUDA disponible: {torch.cuda.is_available()}")

    # Création de l'environnement vectorisé
    env = DummyVecEnv([lambda: gym.make(env_id)])

    # Initialisation du modèle PPO
    model = PPO(
        policy='MultiInputPolicy',
        env=env,
        verbose=1,
        device=device,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        vf_coef=0.5,
        ent_coef=0.01
    )

    # Entraînement du modèle
    print("Début de l'entraînement...")
    model.learn(total_timesteps=total_timesteps, callback=WandbCallback())
    print("Entraînement terminé.")

    # Évaluation du modèle
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
    print(f"Récompense moyenne : {mean_reward:.2f} +/- {std_reward:.2f}")

    # Log des métriques finales
    wandb.log({"mean_reward": mean_reward, "std_reward": std_reward})

    # Sauvegarde du modèle
    model_path = f"{env_id}_ppo_model"
    model.save(model_path)
    print(f"Modèle sauvegardé à : {model_path}")

    # Charger les artefacts W&B
    wandb.save(model_path)

    return model


def main():
    """
    Point d'entrée principal pour entraîner, évaluer et enregistrer des vidéos du modèle.
    """
    # Entraînement du modèle
    trained_model = train_ppo_model()

    # Création d'un nouvel environnement pour l'évaluation
    eval_env = gym.make("PickPlaceCube-v0", render_mode='rgb_array')

    # Enregistrement des vidéos
    print("Enregistrement des vidéos...")
    record_video(trained_model, eval_env)

    eval_env.close()
    print("Programme terminé.")


if __name__ == "__main__":
    main()
