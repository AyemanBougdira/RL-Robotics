def collect_demonstrations(env, model, num_episodes=100):
    """
    Collecte des trajectoires pour former un dataset d'imitation.
    
    Args:
        env: Environnement Gym.
        model: Modèle RL ou un expert humain.
        num_episodes: Nombre d'épisodes à collecter.

    Returns:
        Une liste de trajectoires contenant des états et des actions.
    """
    demonstrations = []

    for episode in range(num_episodes):
        obs = env.reset()[0]  # Compatible gym moderne
        done = False
        episode_data = {"states": [], "actions": []}

        while not done:
            action, _ = model.predict(obs)  # Prédiction de l'expert
            episode_data["states"].append(obs)
            episode_data["actions"].append(action)

            obs, _, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

        demonstrations.append(episode_data)
        print(f"Trajectoire {episode + 1}/{num_episodes} collectée.")

    return demonstrations
