import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Données d'Ebbinghaus (converties en jours)
t_data = np.array([0.01389, 0.04167, 0.375, 1, 2, 6])  # Temps en jours (20 min, 1 h, 9 h, 1 j, 2 j, 6 j)
R_data = np.array([58.2, 44.2, 35.8, 33.7, 27.8, 25.4])  # Rétention en %

# Fonction pour modéliser la courbe de l'oubli (exponentielle avec asymptote)
def forgetting_curve(t, R_inf, R0_minus_R_inf, k):
    return R_inf + R0_minus_R_inf * np.exp(-k * t)

# Ajustement du modèle aux données
popt, _ = curve_fit(forgetting_curve, t_data, R_data, bounds=(0, [100, 100, 10]))
R_inf_opt, R0_minus_R_inf_opt, k_opt = popt
R0_opt = R_inf_opt + R0_minus_R_inf_opt

print("Paramètres optimisés :")
print(f"R_inf = {R_inf_opt:.2f} %, R0 = {R0_opt:.2f} %, k = {k_opt:.4f}")

# Fonction pour calculer la rétention avec révisions
def retention_with_revisions(t_values, revision_times, R_inf, k0, alpha):
    retention_values = np.zeros_like(t_values)
    n_revisions = 1  # Commence à 1 pour l'apprentissage initial
    k_n = k0
    t_last_revision = 0.0
    idx_revision = 0

    for i, t in enumerate(t_values):
        # Vérifier si une révision a eu lieu
        while idx_revision < len(revision_times) and revision_times[idx_revision] <= t:
            t_last_revision = revision_times[idx_revision]
            n_revisions += 1
            k_n = k0 * n_revisions ** (-alpha)
            idx_revision += 1
            # Remettre la rétention à 100% au moment de la révision
            retention_values[i] = 100.0
            continue

        # Temps écoulé depuis la dernière révision
        delta_t = t - t_last_revision
        # Calcul de la rétention
        R_t = R_inf + (100.0 - R_inf) * np.exp(-k_n * delta_t)
        retention_values[i] = R_t

    return retention_values

# Paramètres du modèle
R_inf_model = R_inf_opt
k0_model = k_opt
alpha_model = 0.9  # Ajuster en fonction des données ou de la littérature

# Plage de temps pour le tracé (jusqu'à 5 jours)
t_values = np.linspace(0, 5, 1000)

# Scénarios de révision
revision_scenarios = [
    {'label': 'Sans Révision', 'times': []},
    {'label': 'Révision à 20 min', 'times': [0.01389]},
    {'label': 'Révisions à 20 min et Jour 1', 'times': [0.01389, 1]},
    {'label': 'Révisions à 20 min, Jour 1 et Jour 3', 'times': [0.01389, 1, 3]}
]

# Génération et sauvegarde des graphiques
for i in range(4):
    plt.figure(figsize=(12, 8))

    # Tracer les courbes jusqu'au scénario actuel
    for j in range(i + 1):
        label = revision_scenarios[j]['label']
        times = revision_scenarios[j]['times']
        R_t = retention_with_revisions(t_values, times, R_inf_model, k0_model, alpha_model)
        plt.plot(t_values, R_t, label=label)

    # Personnalisation du graphique
    plt.title('Courbe de l\'oubli avec révisions', fontsize=16)
    plt.xlabel('Temps (jours)', fontsize=14)
    plt.ylabel('Rétention (%)', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.xlim(0, 5)
    plt.ylim(15, 105)

    # Sauvegarde du graphique
    plt.savefig(f'courbe_oubli_revision_{i+1}.png', dpi=300)
    plt.close()

print("Les graphiques ont été générés et sauvegardés sous les noms 'courbe_oubli_revision_1.png' à 'courbe_oubli_revision_4.png'.")
