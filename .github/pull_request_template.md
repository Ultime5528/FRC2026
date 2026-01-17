# Description
<!--- Fais un résumé de ce que tu as ajouté. -->
Closes #TODO. 

### Vérifications générales
- [ ] Code en anglais
- [ ] Noms de fichier en lettres minuscules et sans espace
- [ ] Noms de classe en `PascalCase`
- [ ] Noms de fonction en `camelCase`
- [ ] Noms de variables en `snake_case`
- [ ] Noms de fonction débutent par un verbe d'action (get, set, move, start,
  stop...)
- Ports
  - [ ] se trouvent dans `ports.py`
  - [ ] respectent la convention `subsystem_composante_precision` (p. ex. 
    `shooter_motor_left`)
- [ ] Chaque `autoproperty` respecte la convention `type_precision` (p.ex. 
  `speed_slow`, `height_max`, `distance_max`)
- [ ] Tests unitaires pour maintenir ou augmenter la couverture
- [ ] Chaque dossier est un module (contient `__init__.py`)

### Command
- [ ] Nom débute par un verbe d'action
- [ ] Ajoutée sur le Dashboard
- [ ] Ses paramètres sont dans des `autoproperty`
- [ ] Si pertinent (calculs), implémente `initSendable` pour afficher toute 
  information pertinente sur son état

### Subsystem
- [ ] Hérite de la classe `ultime.Subsystem` (et non `commands2.
Subsystem`)
- [ ] Ses composantes ont été liées au sous-système par `self.addChild()`
- [ ] Ses paramètres sont dans des `autoproperty`
- [ ] Implémente `initSendable` pour afficher toute information pertinente 
  sur son état
- [ ] Instancié et ajouté sur le Dashboard

