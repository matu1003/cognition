import random
from expyriment import design, control, stimuli



# PARAMÈTRES EXPÉRIMENTAUX

ANGLES = [0, 60, 120, 180, 240, 300] # angles de rotation en degrés
VERSIONS = ["normal", "mirror"] # lettre normale vs miroir
REPETITIONS = 3 # nb de répétitions par condition
FIXATION_DURATION = 500 # ms, durée de la croix de fixation
MAX_RESPONSE_DELAY = 3000 # ms, temps max pour répondre
stim = True ## indique si le stimulus est présenté
SOA = 400 # ms, stimulus présenté brièvement

# Nombre total d'essais
TRIALS = []
for angle in ANGLES:
    for version in VERSIONS:
        for _ in range(REPETITIONS):
            TRIALS.append((angle, version))
random.shuffle(TRIALS)
N_TRIALS = len(TRIALS)


# INITIALISATION EXPYRIMENT
exp = design.Experiment(name="Rotation de lettre", text_size=40)
control.set_develop_mode(on=True)
control.initialize(exp)

# Stimuli de base
fixation = stimuli.FixCross(size=(40, 40), colour=(255, 255, 255))
blankscreen = stimuli.BlankScreen()

# On prépare les images pour gagner du temps en présentation
base_stimuli = {
    "normal": stimuli.TextLine("R", text_size=80, text_colour=(255, 255, 255))
}

# Instructions
instructions1 = stimuli.TextScreen(
    "Instructions",
    f"""
Dans cette expérience, une lettre 'R' apparaîtra à l'écran,
plus ou moins inclinée.
Votre tâche est de décider si la lettre est :
    F = version NORMALE
    J = version MIROIR (inversée)

"""
)

instructions2 = stimuli.TextScreen(
    "Instructions (suite)",
    f"""Répondez le plus rapidement ET le plus précisément possible.
Il y aura {N_TRIALS} essais au total.
Appuyez sur la BARRE ESPACE pour commencer."""
)


# Variables sauvegardées
exp.add_data_variable_names([
    'trial', 'angle', 'version', 'respkey', 'correct', 'RT'
])

# -----------------------
# DÉROULEMENT DE L’EXPÉRIENCE
# -----------------------
control.start(skip_ready_screen=True)

# Instructions
instructions1.present()
exp.keyboard.wait_char(' ')  # attendre espace
instructions2.present()
exp.keyboard.wait_char(' ')  # attendre espace

for i_trial, (angle, version) in enumerate(TRIALS, start=1):

    # Écran blanc + petite pause
    blankscreen.present()
    exp.clock.wait(500)

    # Croix de fixation
    fixation.present()
    exp.clock.wait(FIXATION_DURATION)

    # On clone le stimulus de base (pour ne pas le modifier définitivement)
    stim = base_stimuli['normal'].copy()
    if version == "mirror":
        stim.flip([True, False])  # inversion miroir
    stim.rotate(angle)  # rotation mentale à simuler par le sujet

    if stim:
        cue = stimuli.TextLine(f"R {angle} degrés", text_size=80, text_colour=(255, 255, 255))
        cue.present()
        exp.clock.wait(SOA)

    # Présentation du stimulus
    stim.present()

    # Attente de réponse F ou J
    key, rt = exp.keyboard.wait_char(
        ['f', 'j'],
        duration=MAX_RESPONSE_DELAY
    )

    # Détermination de la justesse
    if key is None:
        correct = 0
    else:
        if version == "normal" and key == 'f':
            correct = 1
        elif version == "mirror" and key == 'j':
            correct = 1
        else:
            correct = 0

    # Enregistrement des données
    exp.data.add([i_trial, angle, version, key, correct, rt])

# Fin de l’expérience
control.end()