import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import requests
import io
import time
import threading
import os

# ==========================
# 🔐 1. API Integration
# ==========================

OWM_API_KEY = os.getenv("OWM_API_KEY", "YOUR_OPENWEATHERMAP_API_KEY")
if not OWM_API_KEY or OWM_API_KEY == "YOUR_OPENWEATHERMAP_API_KEY":
    OWM_API_KEY = os.getenv("OWM_API_KEY", "YOUR_OPENWEATHERMAP_API_KEY")


# ==========================
# 📍 4. GPS Integration (via IP for desktop)
# ==========================
def get_geolocation():
    try:
        resp = requests.get("http://ip-api.com/json/")
        data = resp.json()
        if data['status'] == 'success':
            return data['lat'], data['lon'], data['city']
        else:
            raise Exception("Could not fetch geolocation.")
    except Exception as e:
        raise e

# ==========================
# 🌐 1. API Integration (Weather Fetch)
# ==========================
def fetch_weather(lat, lon, units='metric'):
    url = f"https://api.openweathermap.org/data/2.5/onecall"
    params = {
        'lat': lat,
        'lon': lon,
        'exclude': 'minutely,alerts',
        'units': units,
        'appid': OWM_API_KEY
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()

def get_weather_icon(icon_code):
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    resp = requests.get(icon_url)
    resp.raise_for_status()
    img_data = resp.content
    img = Image.open(io.BytesIO(img_data))
    return ImageTk.PhotoImage(img)

# ==========================
# 🌤️ GUI Design & Functionality
# ==========================
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Weather App")
        self.root.geometry("550x750")
        self.root.resizable(False, False)

        self.units = tk.StringVar(value='metric')
        self.create_widgets()

    def create_widgets(self):
        # 🔍 Location Frame
        frame_loc = ttk.Frame(self.root)
        frame_loc.pack(pady=(10,5))

        ttk.Label(frame_loc, text="City: ").grid(row=0, column=0, sticky='w')
        self.city_entry = ttk.Entry(frame_loc, width=30)
        self.city_entry.grid(row=0, column=1, padx=5)

        btn_get = ttk.Button(frame_loc, text="Get Weather", command=self.on_get_weather)
        btn_get.grid(row=0, column=2, padx=5)

        btn_auto = ttk.Button(frame_loc, text="Auto Detect", command=self.on_auto_detect)
        btn_auto.grid(row=1, column=1, pady=5)

        # 🌡️ Unit Selection (7. Unit Conversion)
        frame_units = ttk.Frame(self.root)
        frame_units.pack()
        ttk.Label(frame_units, text="Units: ").pack(side='left')
        ttk.Radiobutton(frame_units, text="Metric (°C, m/s)", variable=self.units, value='metric').pack(side='left')
        ttk.Radiobutton(frame_units, text="Imperial (°F, mph)", variable=self.units, value='imperial').pack(side='left')

        # 🧭 Status Indicator
        self.status_label = ttk.Label(self.root, text="", foreground="blue")
        self.status_label.pack(pady=5)

        ttk.Separator(self.root, orient='horizontal').pack(fill='x', pady=10)

        # 🧊 Current Weather Display
        self.frame_current = ttk.Frame(self.root)
        self.frame_current.pack(pady=10)

        self.icon_label = ttk.Label(self.frame_current)
        self.icon_label.grid(row=0, column=0, rowspan=2, padx=10)

        self.temp_label = ttk.Label(self.frame_current, text="", font=("Helvetica", 24))
        self.temp_label.grid(row=0, column=1, sticky='w')

        self.desc_label = ttk.Label(self.frame_current, text="", font=("Helvetica", 14))
        self.desc_label.grid(row=1, column=1, sticky='w')

        self.wind_label = ttk.Label(self.frame_current, text="", font=("Helvetica", 12))
        self.wind_label.grid(row=2, column=0, columnspan=2, pady=5)

        self.humidity_label = ttk.Label(self.frame_current, text="", font=("Helvetica", 12))
        self.humidity_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.feels_like_label = ttk.Label(self.frame_current, text="", font=("Helvetica", 12))
        self.feels_like_label.grid(row=4, column=0, columnspan=2, pady=5)

        # 🕒 Hourly Forecast
        self.frame_hourly = ttk.LabelFrame(self.root, text="Hourly Forecast")
        self.frame_hourly.pack(fill='x', padx=10, pady=10)

        canvas = tk.Canvas(self.frame_hourly, height=120)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(self.frame_hourly, orient='horizontal', command=canvas.xview)
        scrollbar.pack(side='bottom', fill='x')
        canvas.configure(xscrollcommand=scrollbar.set)

        self.hourly_container = ttk.Frame(canvas)
        canvas.create_window((0,0), window=self.hourly_container, anchor='nw')
        self.hourly_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # 📆 Daily Forecast
        self.frame_daily = ttk.LabelFrame(self.root, text="Daily Forecast")
        self.frame_daily.pack(fill='both', padx=10, pady=10)

    # 🌍 Auto-Detect via IP
    def on_auto_detect(self):
        def task():
            try:
                self.status_label.config(text="Detecting location...")
                lat, lon, city = get_geolocation()
                self.city_entry.delete(0, tk.END)
                self.city_entry.insert(0, city)
                self.fetch_and_display(lat, lon)
            except Exception as e:
                messagebox.showerror("Error", f"Auto detect failed: {e}")
                self.status_label.config(text="Error detecting location.")
        threading.Thread(target=task).start()

    # 🔎 City Search
    def on_get_weather(self):
        city = self.city_entry.get().strip()

        # ✅ 2. User Input Handling
        if not city or len(city) < 2:
            messagebox.showwarning("Input Error", "Please enter a valid city name.")
            return

        def task():
            try:
                self.status_label.config(text="Resolving location...")
                geocode_url = "http://api.openweathermap.org/geo/1.0/direct"
                params = {'q': city, 'limit': 1, 'appid': OWM_API_KEY}
                resp = requests.get(geocode_url, params=params)
                resp.raise_for_status()
                data = resp.json()
                if not data:
                    raise Exception("City not found.")
                lat = data[0]['lat']
                lon = data[0]['lon']
                self.fetch_and_display(lat, lon)
            except Exception as e:
                messagebox.showerror("Error", f"Could not get location: {e}")
                self.status_label.config(text="Failed to resolve city.")
        threading.Thread(target=task).start()

    def fetch_and_display(self, lat, lon):
        try:
            self.status_label.config(text="Fetching weather data...")
            data = fetch_weather(lat, lon, units=self.units.get())
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch weather: {e}")
            self.status_label.config(text="Failed to get weather data.")
            return

        current = data['current']
        temp = current['temp']
        desc = current['weather'][0]['description'].capitalize()
        icon_code = current['weather'][0]['icon']
        wind_speed = current.get('wind_speed', None)
        humidity = current.get('humidity', None)
        feels_like = current.get('feels_like', None)

        icon_img = get_weather_icon(icon_code)
        self.icon_label.image = icon_img
        self.icon_label.configure(image=icon_img)

        unit_temp = "°C" if self.units.get() == 'metric' else "°F"
        unit_speed = "m/s" if self.units.get() == 'metric' else "mph"

        self.temp_label.configure(text=f"{temp:.1f}{unit_temp}")
        self.desc_label.configure(text=desc)
        self.wind_label.configure(text=f"Wind: {wind_speed:.1f} {unit_speed}" if wind_speed else "")
        self.humidity_label.configure(text=f"Humidity: {humidity}%" if humidity else "")
        self.feels_like_label.configure(text=f"Feels like: {feels_like:.1f}{unit_temp}" if feels_like else "")

        # Hourly Forecast
        for widget in self.hourly_container.winfo_children():
            widget.destroy()

        for idx, hour in enumerate(data['hourly'][:12]):
            frame = ttk.Frame(self.hourly_container, borderwidth=1, relief='solid')
            frame.grid(row=0, column=idx, padx=5, pady=5)

            t = time.localtime(hour['dt'])
            hour_str = time.strftime("%I %p", t)
            ttk.Label(frame, text=hour_str).pack()

            ico = get_weather_icon(hour['weather'][0]['icon'])
            lbl = ttk.Label(frame, image=ico)
            lbl.image = ico
            lbl.pack()

            ttk.Label(frame, text=f"{hour['temp']:.1f}{unit_temp}").pack()

        # Daily Forecast
        for widget in self.frame_daily.winfo_children():
            widget.destroy()

        for day in data['daily'][1:8]:  # skip today
            frm = ttk.Frame(self.frame_daily, borderwidth=1, relief='solid', padding=5)
            frm.pack(fill='x', pady=2)

            date_str = time.strftime("%a, %b %d", time.localtime(day['dt']))
            ttk.Label(frm, text=date_str, width=15).pack(side='left')

            ico = get_weather_icon(day['weather'][0]['icon'])
            lbl_i = ttk.Label(frm, image=ico)
            lbl_i.image = ico
            lbl_i.pack(side='left', padx=10)

            min_t = day['temp']['min']
            max_t = day['temp']['max']
            ttk.Label(frm, text=f"{min_t:.1f}/{max_t:.1f}{unit_temp}", width=12).pack(side='left')

            desc_day = day['weather'][0]['description'].capitalize()
            ttk.Label(frm, text=desc_day).pack(side='left', padx=10)

        self.status_label.config(text="Weather data updated.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    app.run()
