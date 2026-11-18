from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

KV = r"""
<SensiRoot>:
    orientation: "vertical"
    padding: "16dp"
    spacing: "9dp"
    canvas.before:
        Color:
            rgba: 0.045, 0.06, 0.10, 1
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: "[b]FREE FIRE INDIA[/b]\\n[color=44E0B8]DEVICE-WISE SENSI[/color]"
        markup: True
        font_size: "23sp"
        size_hint_y: None
        height: "72dp"
    ScrollView:
        do_scroll_x: False
        GridLayout:
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            spacing: "8dp"
            Label:
                text: "Phone aur playing style ki details bharo"
                color: .8, .85, .92, 1
                size_hint_y: None
                height: "30dp"
            Label:
                text: "Phone model"
                halign: "left"
                size_hint_y: None
                height: "22dp"
            TextInput:
                id: phone
                hint_text: "e.g. Moto G45 5G / Samsung A15"
                multiline: False
                size_hint_y: None
                height: "44dp"
            Label:
                text: "RAM"
                halign: "left"
                size_hint_y: None
                height: "22dp"
            Spinner:
                id: ram
                text: "Select RAM"
                values: ["2 GB", "3 GB", "4 GB", "6 GB", "8 GB", "12 GB or more"]
                size_hint_y: None
                height: "44dp"
            Label:
                text: "Screen refresh rate"
                halign: "left"
                size_hint_y: None
                height: "22dp"
            Spinner:
                id: hz
                text: "Select Hz"
                values: ["60 Hz", "90 Hz", "120 Hz", "144 Hz", "165 Hz", "Not sure"]
                size_hint_y: None
                height: "44dp"
            Label:
                text: "Game FPS setting"
                halign: "left"
                size_hint_y: None
                height: "22dp"
            Spinner:
                id: fps
                text: "Select FPS"
                values: ["30 FPS", "40 FPS", "60 FPS", "90 FPS", "120 FPS", "Not sure"]
                size_hint_y: None
                height: "44dp"
            Label:
                text: "Controls / fingers"
                halign: "left"
                size_hint_y: None
                height: "22dp"
            Spinner:
                id: fingers
                text: "Select fingers"
                values: ["2 fingers", "3 fingers", "4 fingers", "5 fingers"]
                size_hint_y: None
                height: "44dp"
            Label:
                text: "Aim style"
                halign: "left"
                size_hint_y: None
                height: "22dp"
            Spinner:
                id: style
                text: "Select style"
                values: ["Balanced", "Drag headshot", "Precise aim", "Close-range rush"]
                size_hint_y: None
                height: "44dp"
            Label:
                text: "Current General sensitivity (optional)"
                halign: "left"
                size_hint_y: None
                height: "22dp"
            TextInput:
                id: current
                hint_text: "0–200; blank if you don't know"
                input_filter: "int"
                multiline: False
                size_hint_y: None
                height: "44dp"
            Button:
                text: "GENERATE MY SENSITIVITY"
                size_hint_y: None
                height: "50dp"
                background_normal: ""
                background_color: .1, .78, .62, 1
                color: .03, .07, .1, 1
                bold: True
                on_release: root.generate(phone.text, ram.text, hz.text, fps.text, fingers.text, style.text, current.text)
            Label:
                text: root.result_text
                markup: True
                text_size: self.width, None
                halign: "left"
                valign: "top"
                size_hint_y: None
                height: self.texture_size[1] + dp(28)
                padding: "12dp", "12dp"
                canvas.before:
                    Color:
                        rgba: .10, .14, .21, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [12,]
"""

class SensiRoot(BoxLayout):
    result_text = StringProperty("[b]Aapki device-wise settings yahan aayengi.[/b]")

    def generate(self, phone, ram, hz, fps, fingers, style, current):
        if not phone.strip() or ram == "Select RAM" or hz == "Select Hz" or fps == "Select FPS" or fingers == "Select fingers" or style == "Select style":
            self.result_text = "[b][color=FFCC66]Phone model aur baaki options select karo.[/color][/b]"
            return

        # A transparent heuristic: these are testable starting presets, not measured/perfect values.
        finger_base = {
            "2 fingers": [180, 172, 158, 140, 85, 130],
            "3 fingers": [176, 168, 154, 138, 85, 130],
            "4 fingers": [172, 165, 150, 135, 82, 128],
            "5 fingers": [170, 162, 148, 132, 80, 125],
        }
        vals = finger_base[fingers][:]

        # A smoother starting point for lower frame-rate settings.
        fps_adjust = {"30 FPS": -8, "40 FPS": -5, "60 FPS": 0,
                      "90 FPS": 2, "120 FPS": 3, "Not sure": 0}
        adjust = fps_adjust[fps]
        vals[0] += adjust
        vals[1] += adjust
        vals[2] += round(adjust / 2)
        vals[3] += round(adjust / 2)

        # High refresh rate does not guarantee that the game runs at that frame rate.
        if hz in ("60 Hz", "Not sure"):
            vals[0] -= 2
            vals[1] -= 2

        # RAM is only a rough context signal; it cannot measure actual touch latency.
        if ram in ("2 GB", "3 GB"):
            vals[0] -= 3
            vals[1] -= 3
            device_note = "Kam RAM par background apps band rakho; stable FPS ko priority do."
        elif ram == "4 GB":
            device_note = "4 GB RAM: gameplay ke dauran FPS stable hai ya nahi, check karo."
        else:
            device_note = "RAM zyada hone se sensitivity automatically better nahi hoti."

        if style == "Drag headshot":
            vals[0] += 8
            vals[1] += 8
        elif style == "Precise aim":
            vals[0] -= 10
            vals[1] -= 10
            vals[2] -= 6
            vals[3] -= 6
        elif style == "Close-range rush":
            vals[0] += 10
            vals[1] += 5

        # Optional anchor: adapt relative to the player's current General setting.
        anchor_note = ""
        if current.strip():
            try:
                c = int(current)
                if not 0 <= c <= 200:
                    raise ValueError
                delta = max(-15, min(15, c - vals[0]))
                vals[0] += delta
                vals[1] += round(delta * 0.7)
                anchor_note = f"Current General setting {c} ko reference banaya; small adjustment kiya."
            except ValueError:
                self.result_text = "[b][color=FFCC66]Current General value 0 se 200 ke beech rakho.[/color][/b]"
                return

        vals = [max(0, min(200, int(v))) for v in vals]
        labels = ["General", "Red Dot", "2x Scope", "4x Scope", "Sniper Scope", "Free Look"]
        lines = [
            "[b][color=44E0B8]YOUR STARTING PRESET[/color][/b]",
            f"Phone: {phone.strip()}",
            f"RAM: {ram} | Screen: {hz} | Game FPS option: {fps}",
            f"Controls: {fingers} | Style: {style}",
            "",
        ]
        lines += [f"[b]{name}:[/b] {value}/200" for name, value in zip(labels, vals)]
        lines += ["", device_note]
        if anchor_note:
            lines.append(anchor_note)
        lines += [
            "",
            "[b]Fine-tune kaise karein:[/b]",
            "Training Ground mein 5 points ke steps se General aur Red Dot adjust karo.",
            "Aim target se aage nikalta hai to thoda kam; target tak nahi pahunchta to thoda badhao.",
            "",
            "[i]Values estimates hain, guaranteed headshots nahi. Game ki current sensitivity scale verify karo.[/i]"
        ]
        self.result_text = "\\n".join(lines)

class SensiApp(App):
    def build(self):
        Builder.load_string(KV)
        return SensiRoot()

if __name__ == "__main__":
    SensiApp().run()
