# Moodul 04a: Andurite liidestamine

> **Järeleaitamine** — see repo on mõeldud tudengitele, kes teevad ülesande hiljem.
> Täpsem õppematerjal on Moodle'is: **Moodul 04: Andurite liidestamine**.

---

## Samm 1 — Forki see repo

1. Mine selle repo lehele GitHubis
2. Kliki paremal ülal nuppu **Fork**
3. Vali oma GitHub konto
4. Kliki **Create fork**

Sinu isiklik koopia tekib:
```
https://github.com/SINU-KASUTAJANIMI/TRO013-04a-Andurid-jarel
```

---

## Samm 2 — Klooni konteinerisse

Ava noVNC terminal (`http://SERVER_IP:33000+N`) ja käivita:

```bash
cd /workspace/ros2_ws/src
git clone https://github.com/SINU-KASUTAJANIMI/TRO013-04a-Andurid-jarel.git
cd TRO013-04a-Andurid-jarel
```

---

## Samm 3 — Tee ülesanded

Kaks ülesannet, mõlemad kasutavad Webots simulatsiooni.

### Ülesanne 1: Raja andur (`raja_andur.py`)

Kirjuta ROS2 sõlm, mis jagab lidari 360° vaate 5 sektoriks ja trükib kauguste tabeli:

```
=== Raja andurid ===
Vasak sein:    0.45 m  [LÄHEDAL]
Ette-vasak:    1.23 m  [OK]
Otse ette:     2.87 m  [OK]
Ette-parem:    1.15 m  [OK]
Parem sein:    0.52 m  [LÄHEDAL]
===================
```

Märgised: `[LÄHEDAL]` < 0.5 m, `[HOIATUS]` < 1.0 m, `[OK]` ≥ 1.0 m

**Faili asukoht repos on sinu valida** — hindamine otsib `raja_andur.py` nimega faili.

### Ülesanne 2: Marsruut (`marsruut.py`)

Kirjuta olekumasin, mis sõidab L-kujulise teekonna odomeetria põhjal:

```
1. Edasi 1.0 m  →  2. Pööre 90°  →  3. Edasi 1.0 m  →  4. Pööre 90°  →  VALMIS
```

Olekud: `OLEK_EDASI_1`, `OLEK_POORDE_1`, `OLEK_EDASI_2`, `OLEK_POORDE_2`, `OLEK_VALMIS`

**Faili asukoht repos on sinu valida** — hindamine otsib `marsruut.py` nimega faili.

**Käivitamine:**
```bash
source /opt/mobros_ws/install/setup.bash
ros2 launch yahboom_webots webots.launch.py    # Terminal 1
ros2 run raja_andur raja_andur                  # Terminal 2 (ülesanne 1)
ros2 run marsruut marsruut                      # Terminal 2 (ülesanne 2)
```

---

## Samm 4 — Commit ja push

```bash
cd /workspace/ros2_ws/src/TRO013-04a-Andurid-jarel
git add .
git commit -m "Moodul 04a: raja_andur ja marsruut"
git push
```

> Git küsib parool — kasuta GitHubi **Personal Access Token**:
> GitHub → Settings → Developer settings → Personal access tokens → Generate new token (scopes: `repo`)

---

## Samm 5 — Vaata hindamistulemusi

Pärast push-i käivitub automaatne hindamine (~1-2 min).

**Vaata tulemusi:** oma repo → **Actions** → viimane töö

Hindamine otsib `raja_andur.py` ja `marsruut.py` faile **kõikidest kaustadest** ja kontrollib:

| Test | Punktid |
|------|---------|
| `raja_andur.py` eksisteerib | 5 p |
| `raja_andur.py` süntaks korrektne | 5 p |
| `sektori_min()` implementeeritud | 15 p |
| 5 sektori kaugused arvutatud (mitte stub) | 15 p |
| Tabel trükitakse aktiivses koodis | 10 p |
| `marsruut.py` eksisteerib | 5 p |
| `marsruut.py` süntaks korrektne | 5 p |
| `control_loop()` olekumasin implementeeritud | 10 p |
| Kõik 4 olekut implementeeritud | 15 p |
| `OLEK_VALMIS` kasutatud | 5 p |
