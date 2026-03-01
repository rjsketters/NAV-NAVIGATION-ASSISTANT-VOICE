# 🧠 NAV — Navigation Assistant
### **Voice + Map System**
> A Human-Centered Navigation System with Voice Guidance and Adaptive Map Display.

---

## 🔗 Project Links
* **Devpost Submission:** [View on Devpost](https://devpost.com/software/nav-navigation-assistant-voice)
* **Demo Video:** [Watch the Demo](https://www.youtube.com/watch?v=L5Mc24OEgLU)

---

## 🌟 Inspiration
**NAV** was inspired by the frustration of traditional GPS apps that force a single "optimal" route and ignore driver preference. 

The goal was to create a system that:
* **Respects human decision-making.**
* **Highlights multiple valid paths** at intersections.
* **Provides hands-free voice guidance** that feels like a cooperative co-pilot rather than a rigid instructor.

---

## 🛠 What it Does
NAV is a mission-style navigation assistant that simulates real-world driving logic:
* 📍 **Real-time Simulation:** Uses predefined routes to simulate a navigation experience.
* 🗣️ **Spoken Guidance:** Provides audio prompts at critical decision points.
* 🛣️ **Dynamic Choice:** Visually highlights multiple route options when a choice exists.
* 🔄 **Seamless Adaptation:** Automatically updates and follows the path the driver naturally chooses.
* 📶 **100% Offline:** All logic and rendering are handled locally; no internet connection or APIs required.

---

## ⚙️ How I Built It
Built fully in **Python** using the following stack:

| Component | Library / Logic |
| :--- | :--- |
| **GUI & Maps** | `tkinter` (Canvas rendering) |
| **Voice Engine** | `pyttsx3` |
| **Concurrency** | `threading` & `queue` (for non-blocking speech) |
| **Math Logic** | **Haversine Formula** |

**Distance Calculations (Haversine Formula):**
$$d = 2r \arcsin\left(\sqrt{\sin^2\left(\frac{\phi_2 - \phi_1}{2}\right) + \cos(\phi_1) \cos(\phi_2) \sin^2\left(\frac{\lambda_2 - \lambda_1}{2}\right)}\right)$$

---

## 🏆 Accomplishments
* Successfully demonstrated an **adaptive, human-centered navigation** system.
* Synchronized **hands-free voice guidance** to trigger accurately at decision points.
* Developed a **dynamic route visualization** and custom map interface from scratch.
* Achieved **full local operation** with zero external API dependencies or costs.

## 🚧 Challenges
* **Synchronization:** Aligning real-time map animations with voice prompts without lag.
* **Threading:** Preventing UI freezes while the text-to-speech engine is active.
* **Custom UI:** Rendering a map-style interface using only the basic `Tkinter` canvas.

---

## 🚀 Instructions to Run

1. **Ensure you have Python 3.x installed.**
2. **Install the dependencies:**
   ```bash
   pip install pyttsx3
   ```
3. **Run the application:**
   ```bash
   python main.py
   ```

---

## 👥 Team Members
### Rider University
* **Ronald Fella**
* **RJ Angove**
* **Kyle Powell**
* **Will Crooks**
