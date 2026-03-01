#!/usr/bin/env python3
"""Minimal entrypoint for NAV — Navigation Assistant demo.

This file is a small, safe demo so judges can run `python main.py`.
It attempts to use `pyttsx3` if available but falls back to printing.
"""
import time


def speak_demo():
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say("Navigation assistant demo starting.")
        engine.runAndWait()
    except Exception as e:
        print("pyttsx3 not available or failed:", e)


def main():
    print("NAV — Navigation Assistant demo")
    speak_demo()
    time.sleep(0.2)


if __name__ == "__main__":
    main()
import tkinter as tk
import pyttsx3
import threading
import time
import math
import queue

class NAV:
    def __init__(self, root):
        self.root = root
        self.root.title("NAV-FULL NAVIGATION ASSISTANCE VOICE DEMO")
        self.root.geometry("430x932")
        self.root.configure(bg="#020202")

        self.is_moving = False
        self.current_idx = 0
        self.scale = 35000 
        self.history = []
        
        # Mac-Safe Speech Engine
        self.speech_queue = queue.Queue()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170) 
        self.engine.startLoop(False) 
        
        # --- STARTING SEGMENT ---
        self.route_points = [
            (39.7582, -74.1385, 45, "LBI START", "Obey Traffic Laws, Be Alert and Hands-Free Decisions While Driving."),
            (39.6585, -74.2425, 55, "ISLAND INTERSECTION", "Decision Point: Island Intersection.")
        ]

        # --- MISSION DATABASE (The Chain) ---
        self.mission_legs = {
            "four_mile": [
                (39.7500, -74.4500, 60, "RT-72 WEST", "Vectoring to Four Mile Circle via Route 72 West."),
                (39.8912, -74.6064, 50, "FOUR MILE CIRCLE", "Decision Point: Four Mile.")
            ],
            "magnolia_rd": [
                (39.8950, -74.7500, 55, "MAGNOLIA ROAD", "Vectoring via Magnolia Road towards Pemberton Bypass (CR-530) and Route 38. Proceeding to 295 interchange via NJ-38 West."),
                (39.9575, -74.9350, 45, "I-295 & RT-38", "Decision Point: 295 and 38.")
            ],
            "rt38_rt73": [
                (39.9500, -74.9700, 50, "RT-38 WEST", "Vectoring to 38 and 73 junction."),
                (39.9450, -75.0000, 45, "RT-38 & RT-73", "Decision Point: 38 and 73.")
            ],
            "betsy_ross": [
                (39.9700, -75.0400, 55, "RT-90 BRIDGE RD", "Crossing Betsy Ross Bridge. Transitioning to I-95 South."),
                (39.8880, -75.2405, 45, "PHILLY AIRPORT", "Mission Complete. Arrival at PHL Terminal.")
            ]
        }

        self.setup_ui()
        self.process_speech()

    def process_speech(self):
        try:
            self.engine.iterate()
            if not self.speech_queue.empty():
                text = self.speech_queue.get_nowait()
                self.engine.say(text)
        except: pass
        self.root.after(40, self.process_speech)

    def speak(self, text, urgent=False):
        if urgent:
            while not self.speech_queue.empty():
                try: self.speech_queue.get_nowait()
                except: break
        self.speech_queue.put(text)

    def setup_ui(self):
        self.top = tk.Frame(self.root, bg="#050505", height=180)
        self.top.pack(side="top", fill="x")
        self.top.pack_propagate(False)
        tk.Label(self.top, text="PHL TERMINAL LINK", font=("Courier", 11), fg="#00FF41", bg="#050505").pack(pady=(40, 0))
        self.instr_label = tk.Label(self.top, text="READY", font=("Courier", 20, "bold"), fg="white", bg="#050505")
        self.instr_label.pack(pady=5)

        self.canvas = tk.Canvas(self.root, bg="#010801", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.cx, self.cy = 215, 300
        self.car_icon = self.canvas.create_oval(0,0,0,0, fill="#00FF41", outline="white", width=2)

        self.bottom = tk.Frame(self.root, bg="#050505", height=250)
        self.bottom.pack(side="bottom", fill="x")
        self.bottom.pack_propagate(False)
        self.speed_val = tk.Label(self.bottom, text="00", font=("Impact", 80), fg="#00FF41", bg="#050505")
        self.speed_val.place(x=20, y=5)
        self.dist_label = tk.Label(self.bottom, text="NEXT: -- MI", font=("Courier", 12, "bold"), fg="#FFB000", bg="#050505")
        self.dist_label.place(x=210, y=40)
        self.btn = tk.Button(self.bottom, text="START MISSION", bg="#00FF41", fg="black", font=("Courier", 14, "bold"), relief="flat", command=self.toggle)
        self.btn.pack(side="bottom", fill="x", padx=40, pady=40, ipady=15)

        self.choice_overlay = tk.Frame(self.canvas, bg="#020202", highlightbackground="#00FF41", highlightthickness=1)

    def toggle(self):
        if not self.is_moving:
            self.is_moving = True
            self.btn.config(text="ABORT", bg="#222", fg="#FF3131")
            threading.Thread(target=self.loop, daemon=True).start()
        else:
            self.is_moving = False

    def loop(self):
        while self.is_moving and self.current_idx < len(self.route_points) - 1:
            s_node = self.route_points[self.current_idx]
            e_node = self.route_points[self.current_idx + 1]

            self.root.after(0, lambda: self.instr_label.config(text=s_node[3]))
            self.root.after(0, lambda: self.speed_val.config(text=str(s_node[2])))
            
            total_dist = self.calculate_dist(s_node[0], s_node[1], e_node[0], e_node[1])
            self.speak(s_node[4])
            
            angle = math.atan2(e_node[1] - s_node[1], e_node[0] - s_node[0])
            steps = 400 
            announced_markers = set()

            for i in range(steps):
                if not self.is_moving: return
                perc = i / steps
                c_lat = s_node[0] + (e_node[0] - s_node[0]) * perc
                c_lon = s_node[1] + (e_node[1] - s_node[1]) * perc
                rem_miles = total_dist * (1 - perc)

                # HANDSFREE ANNOUNCEMENTS (1 Mile Warning)
                if rem_miles <= 1.0 and "OPT" not in announced_markers:
                    if "ISLAND" in e_node[3]:
                        self.speak("Approaching Surf City. You can take the Boulevard or Central Avenue.", urgent=True)
                    elif "FOUR MILE" in e_node[3]:
                        self.speak("Approaching Four Mile. Route 70 West or Magnolia Road available.", urgent=True)
                    elif "295" in e_node[3]:
                        self.speak("Approaching 38 junction. Proceed to 38 and 73.", urgent=True)
                    elif "38 & 73" in e_node[3]:
                        self.speak("Approaching 73. Vector toward Betsy Ross Bridge.", urgent=True)
                    announced_markers.add("OPT")

                # STANDARD MILE TRIGGERS
                for marker in [5.0, 2.0]:
                    if rem_miles <= marker and marker not in announced_markers:
                        self.speak(f"{marker} miles.")
                        announced_markers.add(marker)

                self.root.after(0, self.update_display, c_lat, c_lon, rem_miles, angle)
                time.sleep(0.04)

            self.current_idx += 1
            
            # CHECK IF WE NEED A DECISION OR JUST KEEP GOING
            if "AIRPORT" not in e_node[3]:
                self.is_moving = False
                self.root.after(0, lambda: self.show_choices(e_node[3]))
                return

        self.speak("Arrival confirmed. Welcome to Philadelphia Airport.")
        self.root.after(0, lambda: self.instr_label.config(text="PHL ARRIVED"))

    def update_display(self, lat, lon, miles, angle):
        self.dist_label.config(text=f"NEXT: {miles:.1f} MI")
        self.render(lat, lon, angle)

    def render(self, lat, lon, angle):
        self.canvas.delete("dyn")
        grid = 60
        off_x, off_y = (lon * self.scale) % grid, (lat * self.scale) % grid
        for i in range(-2, 12):
            x, y = (i * grid) - off_x, (i * grid) + off_y
            self.canvas.create_line(x, 0, x, 800, fill="#333333", tags="dyn")
            self.canvas.create_line(0, y, 430, y, fill="#333333", tags="dyn")
        self.history.append((lat, lon))
        for h_lat, h_lon in self.history[-30:]:
            tx = self.cx + (h_lon - lon) * self.scale
            ty = self.cy - (h_lat - lat) * self.scale
            self.canvas.create_oval(tx-1, ty-1, tx+1, ty+1, fill="#00FF41", outline="", tags="dyn")
            r = 8
            self.canvas.coords(
                self.car_icon,
                self.cx - r,
                self.cy - r,
                self.cx + r,
                self.cy + r
            )

    def calculate_dist(self, lat1, lon1, lat2, lon2):
        R = 3958.8
        dlat, dlon = math.radians(lat2-lat1), math.radians(lon2-lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))

    def show_choices(self, location):
        self.choice_overlay.place(relx=0.5, rely=0.45, anchor="center", width=360)
        for w in self.choice_overlay.winfo_children(): w.destroy()
        tk.Label(self.choice_overlay, text="VECTOR SELECTION", fg="#00FF41", bg="#020202", font=("Courier", 14, "bold")).pack(pady=10)
        
        if "ISLAND" in location:
            options = [("THE BOULEVARD", "four_mile"), ("CENTRAL AVENUE", "four_mile")]
        elif "FOUR MILE" in location:
            options = [("MAGNOLIA ROAD", "magnolia_rd"), ("ROUTE 70 WEST", "magnolia_rd")]
        elif "295" in location:
            options = [("ROUTE 38 & 73", "rt38_rt73")]
        elif "38 & 73" in location:
            options = [("BETSY ROSS BRIDGE", "betsy_ross")]
        else:
            options = [("CONTINUE", "betsy_ross")]

        for txt, leg_key in options:
            tk.Button(self.choice_overlay, text=txt, bg="#111", fg="#00FF41", font=("Courier", 11),
                      command=lambda k=leg_key, t=txt: self.select(k, t)).pack(fill="x", padx=30, pady=8, ipady=12)

    def select(self, leg_key, display_text):
        self.choice_overlay.place_forget()
        next_leg = self.mission_legs.get(leg_key, [])
        self.route_points = self.route_points[:self.current_idx] + next_leg
        self.speak(f"Confirmed {display_text}. Proceeding.", urgent=True)
        self.is_moving = True
        threading.Thread(target=self.loop, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = NAV(root)
    root.mainloop()
