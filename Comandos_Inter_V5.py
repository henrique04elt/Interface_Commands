Subject: [PATCH] Comandos_Inter_V5.py
---
Index: .idea/.gitignore
IDEA additional info:
Subsystem: com.intellij.openapi.diff.impl.patch.CharsetEP
<+>UTF-8
===================================================================
diff --git a/.idea/.gitignore b/.idea/.gitignore
new file mode 100644
--- /dev/null	(revision be73575a99b5a73efb054b4449f3665856561e2f)
+++ b/.idea/.gitignore	(revision be73575a99b5a73efb054b4449f3665856561e2f)
@@ -0,0 +1,3 @@
+# Default ignored files
+/shelf/
+/workspace.xml
Index: .idea/inspectionProfiles/profiles_settings.xml
IDEA additional info:
Subsystem: com.intellij.openapi.diff.impl.patch.CharsetEP
<+>UTF-8
===================================================================
diff --git a/.idea/inspectionProfiles/profiles_settings.xml b/.idea/inspectionProfiles/profiles_settings.xml
new file mode 100644
--- /dev/null	(revision be73575a99b5a73efb054b4449f3665856561e2f)
+++ b/.idea/inspectionProfiles/profiles_settings.xml	(revision be73575a99b5a73efb054b4449f3665856561e2f)
@@ -0,0 +1,6 @@
+<component name="InspectionProjectProfileManager">
+  <settings>
+    <option name="USE_PROJECT_PROFILE" value="false" />
+    <version value="1.0" />
+  </settings>
+</component>
\ No newline at end of file
Index: .idea/misc.xml
IDEA additional info:
Subsystem: com.intellij.openapi.diff.impl.patch.CharsetEP
<+>UTF-8
===================================================================
diff --git a/.idea/misc.xml b/.idea/misc.xml
new file mode 100644
--- /dev/null	(revision be73575a99b5a73efb054b4449f3665856561e2f)
+++ b/.idea/misc.xml	(revision be73575a99b5a73efb054b4449f3665856561e2f)
@@ -0,0 +1,10 @@
+<?xml version="1.0" encoding="UTF-8"?>
+<project version="4">
+  <component name="Black">
+    <option name="sdkName" value="Python 3.12 (pythonProject2)" />
+  </component>
+  <component name="ProjectRootManager" version="2" project-jdk-name="Python 3.12 (pythonProject2)" project-jdk-type="Python SDK" />
+  <component name="PyCharmProfessionalAdvertiser">
+    <option name="shown" value="true" />
+  </component>
+</project>
\ No newline at end of file
Index: .idea/modules.xml
IDEA additional info:
Subsystem: com.intellij.openapi.diff.impl.patch.CharsetEP
<+>UTF-8
===================================================================
diff --git a/.idea/modules.xml b/.idea/modules.xml
new file mode 100644
--- /dev/null	(revision be73575a99b5a73efb054b4449f3665856561e2f)
+++ b/.idea/modules.xml	(revision be73575a99b5a73efb054b4449f3665856561e2f)
@@ -0,0 +1,8 @@
+<?xml version="1.0" encoding="UTF-8"?>
+<project version="4">
+  <component name="ProjectModuleManager">
+    <modules>
+      <module fileurl="file://$PROJECT_DIR$/.idea/pythonProject2.iml" filepath="$PROJECT_DIR$/.idea/pythonProject2.iml" />
+    </modules>
+  </component>
+</project>
\ No newline at end of file
Index: .idea/pythonProject2.iml
IDEA additional info
Subsystem: com.intellij.openapi.diff.impl.patch.CharsetEP
<+>UTF-8
===================================================================
diff --git a/.idea/pythonProject2.iml b/.idea/pythonProject2.iml
new file mode 100644
--- /dev/null	(revision be73575a99b5a73efb054b4449f3665856561e2f)
+++ b/.idea/pythonProject2.iml	(revision be73575a99b5a73efb054b4449f3665856561e2f)
@@ -0,0 +1,10 @@
+<?xml version="1.0" encoding="UTF-8"?>
+<module type="PYTHON_MODULE" version="4">
+  <component name="NewModuleRootManager">
+    <content url="file://$MODULE_DIR$">
+      <excludeFolder url="file://$MODULE_DIR$/.venv" />
+    </content>
+    <orderEntry type="inheritedJdk" />
+    <orderEntry type="sourceFolder" forTests="false" />
+  </component>
+</module>
\ No newline at end of file
Index: .idea/vcs.xml
IDEA additional info:
Subsystem: com.intellij.openapi.diff.impl.patch.CharsetEP
<+>UTF-8
===================================================================
diff --git a/.idea/vcs.xml b/.idea/vcs.xml
new file mode 100644
--- /dev/null	(revision be73575a99b5a73efb054b4449f3665856561e2f)
+++ b/.idea/vcs.xml	(revision be73575a99b5a73efb054b4449f3665856561e2f)
@@ -0,0 +1,6 @@
+<?xml version="1.0" encoding="UTF-8"?>
+<project version="4">
+  <component name="VcsDirectoryMappings">
+    <mapping directory="$PROJECT_DIR$" vcs="Git" />
+  </component>
+</project>
\ No newline at end of file
Index: Comandos_Inter_V4.py
IDEA additional info:
Subsystem: com.intellij.openapi.diff.impl.patch.CharsetEP
<+>UTF-8
===================================================================
diff --git a/Comandos_Inter_V4.py b/Comandos_Inter_V4.py
new file mode 100644
--- /dev/null	(revision be73575a99b5a73efb054b4449f3665856561e2f)
+++ b/Comandos_Inter_V4.py	(revision be73575a99b5a73efb054b4449f3665856561e2f)
@@ -0,0 +1,197 @@
+import tkinter as tk
+from tkinter import ttk
+from PIL import Image, ImageTk
+import socket
+import boe
+from schedule_RMC import criar_janela
+
+class CommandInterface:
+    def __init__(self, master):
+        self.master = master
+        master.title("BOE Command Interface")
+        master.geometry("800x600")
+
+        # Configure estilos e layouts
+        self.style = ttk.Style()
+        self.style.theme_use("clam")
+
+        # Configuração do estilo
+        self.style.configure("TLabelFrame", background="#f7f7f7", font=("Helvetica", 14), relief="solid", borderwidth=1)
+        self.style.configure("TButton", background="#808080", foreground="white", font=("Helvetica", 12), padding=5)
+        self.style.configure("TCombobox", font=("Helvetica", 12))
+        self.style.configure("TLabel", font=("Helvetica", 12))
+        self.style.configure("TText", font=("Helvetica", 12), wrap="word")
+        self.style.configure("Setting.TButton", background="#C0C0C0", foreground="black")
+        self.style.configure("Reading.TButton", background="#C0C0C0", foreground="black")
+        self.style.configure("Rounded.TFrame", background="#f7f7f7", relief="solid", borderwidth=1)
+        self.style.map("Rounded.TFrame", background=[("active", "#e0e0e0")])
+
+        logo_image = Image.open("Eletromidia_logo.png")
+        logo_image = logo_image.resize((100, 100))
+        self.logo = ImageTk.PhotoImage(logo_image)
+
+        self.logo_label = ttk.Label(master, image=self.logo)
+        self.logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
+
+        self.label_frame = ttk.LabelFrame(master, text='Commands', padding=10, style="Rounded.TFrame")
+        self.label_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")
+
+        self.command_type_label = ttk.Label(master, text="Command Type: None", font=("Helvetica", 14))
+        self.command_type_label.grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")
+
+        self.show_setting_button = ttk.Button(self.label_frame, text="Configuration Commands", style="Setting.TButton", command=self.show_setting_commands)
+        self.show_setting_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
+
+        self.show_reading_button = ttk.Button(self.label_frame, text="Reading Commands", style="Reading.TButton", command=self.show_reading_commands)
+        self.show_reading_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
+
+        self.command_variable = tk.StringVar(master)
+        self.command_variable.set('Select a command')
+
+        self.command_menu = ttk.Combobox(self.label_frame, textvariable=self.command_variable, state='readonly', width=40)
+        self.command_menu.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky='ew')
+        self.command_menu.bind('<<ComboboxSelected>>', self.update_display)
+
+        self.code_frame = ttk.LabelFrame(master, text="Code", padding=10, style="Rounded.TFrame", height=100)
+        self.code_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
+
+        self.code_text = tk.Text(self.code_frame, height=3, width=50, font=("Helvetica", 12), bg="#f0f0f0", relief="solid", borderwidth=1)
+        self.code_text.pack(fill=tk.BOTH, expand=True)
+
+        self.ack_frame = ttk.LabelFrame(master, text="ACK", padding=10, style="Rounded.TFrame", height=100)
+        self.ack_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
+
+        self.ack_text = tk.Text(self.ack_frame, height=3, width=50, font=("Helvetica", 12), bg="#f0f0f0", relief="solid", borderwidth=1)
+        self.ack_text.pack(fill=tk.BOTH, expand=True)
+
+        self.relay_frame = ttk.LabelFrame(master, text="Relay Control", padding=10, style="Rounded.TFrame")
+        self.relay_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ne")
+
+        self.schedule_button = ttk.Button(master, text="Configurar Schedule", command=self.abrir_janela_schedule)
+        self.schedule_button.grid(row=0, column=0, columnspan=1, pady=10)
+
+        self.create_relay_buttons()
+        self.relay_status = {i: "OFF" for i in range(6)}
+
+        self.ip_label = ttk.Label(master, text="IP Address:")
+        self.ip_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
+        self.ip_entry = ttk.Entry(master, width=15)
+        self.ip_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
+        self.ip_entry.insert(0, "192.168.0.211")
+
+        self.port_label = ttk.Label(master, text="Port:")
+        self.port_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
+        self.port_entry = ttk.Entry(master, width=15)
+        self.port_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")
+        self.port_entry.insert(0, "55502")
+
+        self.send_button = ttk.Button(master, text="Send Command", command=self.send_tcp_command)
+        self.send_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10)
+
+    def create_relay_buttons(self):
+        for i in range(6):
+            on_button = ttk.Button(self.relay_frame, text=f"Relay {i} ON", width=15, command=lambda i=i: self.send_relay_command(i, True))
+            on_button.grid(row=i, column=0, padx=5, pady=2, sticky="ew")
+
+            off_button = ttk.Button(self.relay_frame, text=f"Relay {i} OFF", width=15, command=lambda i=i: self.send_relay_command(i, False))
+            off_button.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
+
+    def send_relay_command(self, relay, turn_on):
+        command_type = 'ON' if turn_on else 'OFF'
+        command_key = f"Relay - {relay} {command_type}"
+        command_data = boe.comandos['Relay']['Setting'].get(command_key, {})
+
+        code = command_data.get('Send Data', 'Code not available')
+        ack = command_data.get('ACK', 'ACK not available')
+
+        self.code_text.delete("1.0", tk.END)
+        self.code_text.insert(tk.END, code)
+
+        self.ack_text.delete("1.0", tk.END)
+        self.ack_text.insert(tk.END, ack)
+
+    def show_setting_commands(self):
+        self.command_type_label.config(text="Command Type: Setting")
+        self.populate_commands('Setting')
+
+    def abrir_janela_schedule(self):
+        criar_janela()
+
+    def show_reading_commands(self):
+        self.command_type_label.config(text="Command Type: Reading")
+        self.populate_commands('Reading')
+
+    def populate_commands(self, command_type):
+        self.code_text.delete("1.0", tk.END)
+        self.ack_text.delete("1.0", tk.END)
+
+        commands_list = []
+        for category, commands in boe.comandos.items():
+            if command_type in commands:
+                for command in commands[command_type]:
+                    commands_list.append(f"{category} - {command}")
+        self.command_menu['values'] = commands_list
+        if not commands_list:
+            self.command_variable.set('No commands found')
+        else:
+            self.command_variable.set('Select a command')
+
+    def update_display(self, event):
+        selected_command = self.command_variable.get()
+        if ' - ' not in selected_command:
+            return
+
+        category, command = selected_command.split(' - ', 1)
+        command_data = None
+
+        if category in boe.comandos:
+            if 'Setting' in boe.comandos[category] and command in boe.comandos[category]['Setting']:
+                command_data = boe.comandos[category]['Setting'][command]
+            elif 'Reading' in boe.comandos[category] and command in boe.comandos[category]['Reading']:
+                command_data = boe.comandos[category]['Reading'][command]
+
+        if command_data:
+            code = command_data.get('Send Data', 'Code not available')
+            ack = command_data.get('ACK', 'ACK not available')
+        else:
+            code = 'Code not available'
+            ack = 'ACK not available'
+
+        self.code_text.delete("1.0", tk.END)
+        self.code_text.insert(tk.END, code)
+
+        self.ack_text.delete("1.0", tk.END)
+        self.ack_text.insert(tk.END, ack)
+
+    def send_tcp_command(self):
+        ip = self.ip_entry.get()
+        port = self.port_entry.get()
+        command = self.code_text.get("1.0", tk.END).strip()
+
+        if not ip or not port or not command:
+            print("IP, Porta ou Comando não fornecido.")
+            return
+
+        try:
+            port = int(port)
+            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
+                print(f"Conectando a {ip}:{port}")
+                s.connect((ip, port))
+                print(f"Enviando comando: {command}")
+                s.sendall(bytes.fromhex(command))
+                print(f"Comando enviado: {command}")
+                data = s.recv(2048)
+                print(f"Resposta recebida: {data.hex()}")
+                self.ack_text.delete("1.0", tk.END)
+                self.ack_text.insert(tk.END, data.hex())
+        except ValueError as e:
+            print(f"Erro de conversão do comando: {e}")
+        except socket.error as e:
+            print(f"Erro de socket: {e}")
+        except Exception as e:
+            print(f"Erro inesperado: {e}")
+
+if __name__ == "__main__":
+    root = tk.Tk()
+    command_interface = CommandInterface(root)
+    root.mainloop()
Index: Comandos_Inter_V5.py
IDEA additional info:
Subsystem: com.intellij.openapi.diff.impl.patch.CharsetEP
<+>UTF-8
===================================================================
diff --git a/Comandos_Inter_V5.py b/Comandos_Inter_V5.py
new file mode 100644
--- /dev/null	(revision be73575a99b5a73efb054b4449f3665856561e2f)
+++ b/Comandos_Inter_V5.py	(revision be73575a99b5a73efb054b4449f3665856561e2f)
@@ -0,0 +1,71 @@
+import tkinter as tk
+from tkinter import ttk
+import socket
+import threading
+
+class CommandInterface:
+    def __init__(self, master):
+        self.master = master
+        master.title("Command Interface")
+        master.geometry("400x200")
+
+        # Criar os widgets
+        self.create_widgets()
+
+    def create_widgets(self):
+        # Frame para os widgets principais
+        self.main_frame = ttk.Frame(self.master)
+        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
+
+        # Entrada para o endereço IP do servidor
+        self.ip_label = ttk.Label(self.main_frame, text="Server IP:")
+        self.ip_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
+        self.ip_entry = ttk.Entry(self.main_frame, width=20)
+        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)
+
+        # Entrada para a porta do servidor
+        self.port_label = ttk.Label(self.main_frame, text="Server Port:")
+        self.port_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
+        self.port_entry = ttk.Entry(self.main_frame, width=10)
+        self.port_entry.grid(row=1, column=1, padx=5, pady=5)
+
+        # Botão para enviar o comando
+        self.send_button = ttk.Button(self.main_frame, text="Send Command", command=self.send_command)
+        self.send_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")
+
+        # Saída para exibir a resposta do servidor
+        self.response_label = ttk.Label(self.main_frame, text="Response:")
+        self.response_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
+        self.response_text = tk.Text(self.main_frame, height=5, width=40)
+        self.response_text.grid(row=3, column=1, padx=5, pady=5)
+
+    def send_command(self):
+        # Obter o endereço IP e a porta do servidor
+        ip = self.ip_entry.get()
+        port = self.port_entry.get()
+
+        # Iniciar uma nova thread para operação de rede
+        threading.Thread(target=self.send_command_thread, args=(ip, port)).start()
+
+    def send_command_thread(self, ip, port):
+        try:
+            # Criar o socket e se conectar ao servidor
+            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
+                s.connect((ip, int(port)))
+
+                # Enviar o comando específico
+                command = bytes.fromhex('ff 55 04 ad 01 00 00 06')  # Substitua pelo seu comando
+                s.sendall(command)  # Envie o comando
+
+                print("Comando enviado:", command)
+        except Exception as e:
+            # Em caso de erro, exibir uma mensagem de erro
+            self.master.after(0, lambda err=str(e): self.show_error(err))
+
+    def show_error(self, error_message):
+        self.response_text.insert(tk.END, f"Error: {error_message}\n")
+
+if __name__ == "__main__":
+    root = tk.Tk()
+    command_interface = CommandInterface(root)
+    root.mainloop()
