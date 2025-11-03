import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import threading
import time
import json
import os
from PIL import Image, ImageTk
from game_logic import *

class DetectiveGameGUI:
    def __init__(self, root):
        self.root = root
        self.game_started = False
        self.game_over = False
        self.start_time = None
        self.time_limit = TEMPO_MAX_SEGUNDOS
        
        # Game state variables
        self.culpado_real = None
        self.local_crime = None
        self.item_crime = None
        self.pistas_disponiveis = []
        self.pontuacao_atual = 1000
        self.nome_jogador = ""
        
        # Image variables
        self.images = {}
        self.load_images()
        
        self.setup_window()
        self.create_widgets()
        self.show_main_menu()
        
    def load_images(self):
        """Load all game images"""
        try:
            avatar_mapping = {
                'Silas Stone': 'Silas_Stone_semfundo.png',
                'Engenheira Jade Jenkins': 'Engenheira_Jade_Jenkins_semfundo.png',
                'Piloto Paxton Price': 'Piloto_Piper_Price_semfundo.png',
                'Comandante Victoria Volkova': 'Comandante_Victoria_Volkova_semfundo.png',
                'Dr. Alistair Armstrong': 'Dr._Alistair_Armstrong_semfundo.png',
                'Dr. Elias Erwin': 'Dr._Elias_Erwin_semfundo.png',
                'Chefe Kaelen Knight': 'Chefe_Kaelen_Knight_semfundo.png',
                'A.T.H.E.N.A.': 'IA_semfundo.png'
            }
            
            # Load avatars
            for character, filename in avatar_mapping.items():
                try:
                    path = os.path.join('resources', 'avatares', filename)
                    if os.path.exists(path):
                        img = Image.open(path)
                        img = img.resize((80, 80), Image.Resampling.LANCZOS)
                        self.images[f'avatar_{character}'] = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Error loading avatar {filename}: {e}")
            
            # Load items
            item_mapping = {
                'Seringa Sedativa': 'Seringa_Sedativa.png',
                'Cortador a Plasma': 'Cortador_a_Plasma.png',
                'Unidade de Transmissão LR': 'Unidade_de_Transmissão_LR.png',
                'Chave de Acesso Ômega': 'Chave_de_Acesso_Ômega.png',
                'Vírus de Corrupção': 'Vírus_de_Corrupção.png'
            }
            
            for item, filename in item_mapping.items():
                try:
                    path = os.path.join('resources', 'itens', filename)
                    if os.path.exists(path):
                        img = Image.open(path)
                        img = img.resize((60, 60), Image.Resampling.LANCZOS)
                        self.images[f'item_{item}'] = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Error loading item {filename}: {e}")
            
            # Load locations
            location_mapping = {
                'Engenharia': 'Engenharia_de_Suporta_de_Vida.png',
                'Compartimento de Carga': 'Compartimento_de_Carga.png',
                'Ala Médica': 'Ala_Médica.png',
                'Laboratório de Biociência': 'Laboratório_de_Biociência.png',
                'Ponte de Comando': 'Ponte_de_Comando.png',
                'Dutos de Ventilação': 'Dutos_de_Ventilação.png'
            }
            
            for location, filename in location_mapping.items():
                try:
                    path = os.path.join('resources', 'locais', filename)
                    if os.path.exists(path):
                        img = Image.open(path)
                        img = img.resize((100, 80), Image.Resampling.LANCZOS)
                        self.images[f'location_{location}'] = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Error loading location {filename}: {e}")
                    
        except Exception as e:
            print(f"Error loading images: {e}")
        
    def setup_window(self):
        self.root.title("SABOTAGEM NA ARES-7: AR E SILÊNCIO")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        # Main container
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame for images and info
        left_frame = ttk.Frame(main_container, width=300)
        main_container.add(left_frame, weight=1)
        
        # Right frame for main content
        right_frame = ttk.Frame(main_container)
        main_container.add(right_frame, weight=3)
        
        # === LEFT FRAME SETUP ===
        # Title
        title_label = ttk.Label(left_frame, text="ARES-7", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Timer and Score
        self.timer_label = ttk.Label(left_frame, text="Tempo: 04:00", 
                                   font=('Arial', 12, 'bold'), foreground='blue')
        self.timer_label.pack(pady=5)
        
        self.score_label = ttk.Label(left_frame, text="Pontuação: 1000", 
                                   font=('Arial', 12, 'bold'), foreground='green')
        self.score_label.pack(pady=5)
        
        self.player_label = ttk.Label(left_frame, text="", 
                                    font=('Arial', 10))
        self.player_label.pack(pady=5)
        
        # Current crime info frame
        crime_frame = ttk.LabelFrame(left_frame, text="Investigação Atual", padding="10")
        crime_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.crime_location_label = ttk.Label(crime_frame, text="Local: ---")
        self.crime_location_label.pack()
        
        self.crime_item_label = ttk.Label(crime_frame, text="Item: ---")
        self.crime_item_label.pack()
        
        # Image display frame
        self.image_frame = ttk.LabelFrame(left_frame, text="Evidências Visuais", padding="10")
        self.image_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.current_image_label = ttk.Label(self.image_frame, text="Nenhuma imagem")
        self.current_image_label.pack(expand=True)
        
        # === RIGHT FRAME SETUP ===
        right_main_frame = ttk.Frame(right_frame, padding="10")
        right_main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        main_title_label = ttk.Label(right_main_frame, text="SABOTAGEM NA ARES-7: AR E SILÊNCIO", 
                                   font=('Arial', 18, 'bold'))
        main_title_label.pack(pady=10)
        
        # Main text area (scrollable)
        self.text_area = scrolledtext.ScrolledText(right_main_frame, wrap=tk.WORD, 
                                                  width=70, height=28, 
                                                  font=('Consolas', 10))
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Buttons frame
        button_frame = ttk.Frame(right_main_frame)
        button_frame.pack(pady=10)
        
        self.start_button = ttk.Button(button_frame, text="INICIAR JOGO", 
                                     command=self.start_new_game, width=15)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.clue_button = ttk.Button(button_frame, text="CONSULTAR PISTAS", 
                                    command=self.get_clue, width=20, state='disabled')
        self.clue_button.grid(row=0, column=1, padx=5)
        
        self.accuse_button = ttk.Button(button_frame, text="FAZER ACUSAÇÃO", 
                                      command=self.make_accusation, width=20, state='disabled')
        self.accuse_button.grid(row=0, column=2, padx=5)
        
        self.leaderboard_button = ttk.Button(button_frame, text="VER PLACAR", 
                                           command=self.show_leaderboard, width=15)
        self.leaderboard_button.grid(row=0, column=3, padx=5)
        
        self.restart_button = ttk.Button(button_frame, text="MENU PRINCIPAL", 
                                       command=self.show_main_menu, width=15)
        self.restart_button.grid(row=0, column=4, padx=5)
        
    def display_image(self, image_key, description=""):
        """Display an image in the left panel"""
        if image_key in self.images:
            self.current_image_label.config(image=self.images[image_key], text="")
        else:
            self.current_image_label.config(image="", text=description or "Imagem não encontrada")
            
    def add_text(self, text, newlines=True):
        """Add text to the main text area"""
        self.text_area.insert(tk.END, text)
        if newlines:
            self.text_area.insert(tk.END, "\n\n")
        self.text_area.see(tk.END)
        self.root.update()
        
    def clear_text(self):
        """Clear the text area"""
        self.text_area.delete(1.0, tk.END)
        
    def show_main_menu(self):
        """Show the main menu"""
        self.clear_text()
        self.game_started = False
        self.game_over = False
        
        # Reset UI elements
        self.timer_label.config(text="Tempo: 04:00", foreground='blue')
        self.score_label.config(text="Pontuação: 1000", foreground='green')
        self.player_label.config(text="")
        self.crime_location_label.config(text="Local: ---")
        self.crime_item_label.config(text="Item: ---")
        self.start_button.config(state='normal')
        self.clue_button.config(state='disabled')
        self.accuse_button.config(state='disabled')
        
        # Show A.T.H.E.N.A. image
        self.display_image('avatar_A.T.H.E.N.A.', "A.T.H.E.N.A. - IA da estação")
        
        menu_text = apresentar_contexto() + "\n\n"
        menu_text += "═══════════════════════════════════════════════════════════════\n"
        menu_text += "                           MENU PRINCIPAL\n"
        menu_text += "═══════════════════════════════════════════════════════════════\n\n"
        menu_text += "• INICIAR JOGO - Começar uma nova investigação\n"
        menu_text += "• VER PLACAR - Conferir as melhores pontuações\n"
        menu_text += "• CONSULTAR PISTAS - Disponível durante o jogo (custa tempo e pontos)\n"
        menu_text += "• FAZER ACUSAÇÃO - Sua chance final de salvar a tripulação\n\n"
        menu_text += "SISTEMA DE PONTUAÇÃO:\n"
        menu_text += "- Você começa com 1000 pontos\n"
        menu_text += "- Cada pista custa tempo E pontos\n"
        menu_text += "- Bônus de tempo ao vencer\n"
        menu_text += "- Use a lógica para maximizar sua pontuação!\n\n"
        menu_text += "Clique em 'INICIAR JOGO' quando estiver pronto..."
        
        self.add_text(menu_text)
        
    def start_new_game(self):
        """Start a new game after getting player name"""
        # Get player name
        name = simpledialog.askstring("Nome do Jogador", 
                                     "Digite seu nome de Detetive:",
                                     parent=self.root)
        if not name:
            name = "Detetive Anônimo"
            
        self.nome_jogador = name
        self.player_label.config(text=f"Detetive: {self.nome_jogador}")
        
        self.start_game()
        
    def show_characters(self):
        """Show character information with images"""
        self.add_text(apresentar_personagens())
        
        # Show random character image
        characters = list(PERSONAGENS.keys())
        random_char = characters[0]  # Show first character
        self.display_image(f'avatar_{random_char}', random_char)
        
        self.add_text(apresentar_regras())
            
    def start_game(self):
        """Start the game"""
        if self.game_started:
            return
            
        self.clear_text()
        self.show_characters()
        
        self.culpado_real, self.local_crime, self.item_crime, self.pistas_disponiveis = configurar_partida()
        
        # Update crime info display
        self.crime_location_label.config(text=f"Local: {self.local_crime}")
        self.crime_item_label.config(text=f"Item: {self.item_crime}")
        
        # Show location image
        self.display_image(f'location_{self.local_crime}', self.local_crime)
        
        self.pontuacao_atual = 1000
        self.score_label.config(text=f"Pontuação: {self.pontuacao_atual}")
        
        self.add_text("═" * 60)
        self.add_text("                    INÍCIO DA INVESTIGAÇÃO")
        self.add_text("═" * 60)
        
        game_info = f"""
Boa sorte, Detetive {self.nome_jogador}!

Iniciando investigação... O crime principal está ligado à área '{self.local_crime}' e ao item '{self.item_crime}'.
Restam {len(self.pistas_disponiveis)} pistas para analisar.

Objetivo: Descobrir o sabotador antes que o tempo se esgote!
• Consultar Pistas: Gasta tempo E pontos, mas fornece informações cruciais
• Fazer Acusação: Sua chance final - acertar salva todos, errar é game over
        """
        self.add_text(game_info)
        
        # Start timer
        self.game_started = True
        self.game_over = False
        self.start_time = time.time()
        self.time_limit = TEMPO_MAX_SEGUNDOS
        
        # Enable game buttons
        self.start_button.config(state='disabled')
        self.clue_button.config(state='normal')
        self.accuse_button.config(state='normal')
        
        # Start timer thread
        self.update_timer()
        
    def update_timer(self):
        """Update the timer display"""
        if not self.game_started or self.game_over:
            return
            
        elapsed = time.time() - self.start_time
        remaining = max(0, self.time_limit - elapsed)
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        # Change color based on time left
        if remaining <= 30:
            color = 'red'
            self.timer_label.config(text=f"⚠️ CRÍTICO: {minutes:02d}:{seconds:02d}", foreground=color)
        elif remaining <= 60:
            color = 'orange'
            self.timer_label.config(text=f"⚠️ ATENÇÃO: {minutes:02d}:{seconds:02d}", foreground=color)
        else:
            color = 'blue'
            self.timer_label.config(text=f"Tempo: {minutes:02d}:{seconds:02d}", foreground=color)
        
        if remaining <= 0:
            self.game_over_time()
        else:
            # Schedule next update
            self.root.after(1000, self.update_timer)
            
    def get_clue(self):
        """Get a clue (consulting pistas)"""
        if not self.pistas_disponiveis:
            self.add_text("📋 Todas as pistas disponíveis já foram reveladas!")
            return
        
        tempo_gasto, custo_pontos, self.pistas_disponiveis, clue_text = consultar_pistas(self.pistas_disponiveis)
        
        # Display the clue in GUI
        self.add_text("🔍 NOVA PISTA DESCOBERTA:")
        self.add_text(f"   {clue_text}")
        self.add_text(f"⏱️  Tempo gasto: {tempo_gasto} segundos")
        self.add_text(f"💰 Pontos perdidos: {custo_pontos}")
        
        # Show relevant image based on clue content
        if "item" in clue_text.lower():
            # Try to show item image
            for item in ITENS:
                if item in clue_text:
                    self.display_image(f'item_{item}', item)
                    break
        elif "acesso" in clue_text.lower() or any(local in clue_text for local in LOCAIS):
            # Show location image
            for local in LOCAIS:
                if local in clue_text:
                    self.display_image(f'location_{local}', local)
                    break
        
        # Update time and score
        self.time_limit -= tempo_gasto
        self.pontuacao_atual -= custo_pontos
        if self.pontuacao_atual < 0:
            self.pontuacao_atual = 0
            
        # Update displays
        self.score_label.config(text=f"Pontuação: {self.pontuacao_atual}")
        self.add_text(f"📋 Pistas restantes: {len(self.pistas_disponiveis)}")
        
    def make_accusation(self):
        """Make final accusation with character images"""
        # Create accusation window
        accusation_window = tk.Toplevel(self.root)
        accusation_window.title("FAZER ACUSAÇÃO FINAL")
        accusation_window.geometry("600x750") 
        accusation_window.grab_set() 
        
        # Center the window
        accusation_window.update_idletasks()
        x = (accusation_window.winfo_screenwidth() // 2) - (300)
        y = (accusation_window.winfo_screenheight() // 2) - (375)
        accusation_window.geometry(f"600x750+{x}+{y}")
        
        main_frame = ttk.Frame(accusation_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="ACUSAÇÃO FINAL", 
                font=('Arial', 16, 'bold')).pack(pady=10)
        
        ttk.Label(main_frame, text="Quem você acredita ser o sabotador?", 
                font=('Arial', 12)).pack(pady=10)
        
        # Create scrollable frame for suspects
        canvas = tk.Canvas(main_frame, height=400)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Suspect selection with images
        suspect_var = tk.StringVar()
        suspects = sorted(list(SUSPEITOS))
        
        for i, suspect in enumerate(suspects):
            suspect_frame = ttk.Frame(scrollable_frame)
            suspect_frame.pack(fill=tk.X, pady=5, padx=10)
            
            # Radio button
            radio = ttk.Radiobutton(suspect_frame, text=suspect, variable=suspect_var, 
                                value=suspect, width=30)
            radio.pack(side=tk.LEFT, anchor="w")
            
            # Character image
            if f'avatar_{suspect}' in self.images:
                img_label = ttk.Label(suspect_frame, image=self.images[f'avatar_{suspect}'])
                img_label.pack(side=tk.RIGHT, padx=10)
        
        # Button frame at the bottom
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
    
        def confirm_accusation():
            chosen = suspect_var.get()
            if not chosen:
                messagebox.showwarning("Aviso", "Selecione um suspeito!")
                return
                
            accusation_window.destroy()
            self.resolve_accusation(chosen)
        
        def cancel_accusation():
            accusation_window.destroy()
        
        # Buttons
        ttk.Button(button_frame, text="CONFIRMAR ACUSAÇÃO", 
                command=confirm_accusation, width=20).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(button_frame, text="CANCELAR", 
                command=cancel_accusation, width=15).pack(side=tk.LEFT, padx=10)
        
        # Make sure the window can handle mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", _on_mousewheel)
        
    def resolve_accusation(self, chosen_suspect):
        """Resolve the final accusation using backend logic"""
        self.game_over = True
        
        # Show chosen suspect image
        self.display_image(f'avatar_{chosen_suspect}', chosen_suspect)
        
        tempo_restante = max(0, self.time_limit - (time.time() - self.start_time))
        
        # Use your modified backend function
        jogo_acabou, pontuacao_final, result_text = arriscar_culpado(chosen_suspect, self.culpado_real, 
                                                                   self.pontuacao_atual, tempo_restante)
        
        # Display result in GUI
        self.add_text("=" * 60)
        self.add_text(f"           ACUSAÇÃO FINAL: {chosen_suspect}")
        self.add_text("=" * 60)
        self.add_text(result_text)
        
        # Show real culprit image if wrong
        if chosen_suspect != self.culpado_real:
            self.root.after(3000, lambda: self.display_image(f'avatar_{self.culpado_real}', f"Culpado real: {self.culpado_real}"))
        
        # Save score if > 0
        if pontuacao_final > 0:
            save_result = salvar_pontuacoes(self.nome_jogador, pontuacao_final)
            self.add_text(save_result)
        
        # Update displays
        if pontuacao_final > 0:
            self.timer_label.config(text="MISSÃO CUMPRIDA!", foreground='green')
            self.score_label.config(text=f"Pontuação Final: {pontuacao_final}", foreground='green')
        else:
            self.timer_label.config(text="MISSÃO FALHADA", foreground='red')
            self.score_label.config(text="Pontuação Final: 0", foreground='red')
        
        # Disable game buttons
        self.clue_button.config(state='disabled')
        self.accuse_button.config(state='disabled')
        self.start_button.config(state='normal')
        
    def game_over_time(self):
        """Handle game over due to time"""
        self.game_over = True
        
        # Show real culprit
        self.display_image(f'avatar_{self.culpado_real}', f"Culpado: {self.culpado_real}")
        
        self.add_text("=" * 60)
        self.add_text("         ⏰ TEMPO ESGOTADO - FRACASSO NA MISSÃO!")
        self.add_text("=" * 60)
        
        timeout_text = f"""
O oxigênio esgotou. A tripulação perece no caos da ARES-7.

O culpado era: {self.culpado_real}

Você não conseguiu resolver o mistério a tempo...

PONTUAÇÃO FINAL: 0
        """
        self.add_text(timeout_text)
        
        self.timer_label.config(text="TEMPO ESGOTADO", foreground='red')
        self.score_label.config(text="Pontuação Final: 0", foreground='red')
        
        # Disable game buttons
        self.clue_button.config(state='disabled')
        self.accuse_button.config(state='disabled')
        self.start_button.config(state='normal')
        
    def show_leaderboard(self):
        """Show the leaderboard"""
        self.clear_text()
        
        # Use modified backend function
        leaderboard_text = mostrar_pontuacoes()
        
        self.add_text(leaderboard_text)
        self.add_text("\nClique em 'MENU PRINCIPAL' para voltar...")

if __name__ == "__main__":
    root = tk.Tk()
    game = DetectiveGameGUI(root)
    root.mainloop()