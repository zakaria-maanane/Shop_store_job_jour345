
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Stock")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        
        # Connexion à la base de données
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="store"
            )
            self.cursor = self.conn.cursor()
            print("Connexion à la base de données réussie")
        except Error as e:
            messagebox.showerror("Erreur de connexion", f"Erreur: {e}")
            root.destroy()
            return
        
        # Configurer le style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TEntry', font=('Arial', 10))
        
        # Créer le frame principal
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill='both', expand=True)
        
        # Titre
        title_label = ttk.Label(self.main_frame, text="Gestion de Stock", font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=4, pady=10)
        
        # Créer le tableau des produits
        self.create_product_table()
        
        # Créer les boutons d'action
        self.create_action_buttons()
        
        # Charger les produits
        self.load_products()
        
    def create_product_table(self):
        # Frame pour le tableau
        table_frame = ttk.Frame(self.main_frame)
        table_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
        
        # Créer le treeview
        columns = ('ID', 'Nom', 'Description', 'Prix', 'Quantité', 'Catégorie')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Définir les entêtes
        for col in columns:
            self.tree.heading(col, text=col)
            if col == 'Description':
                self.tree.column(col, width=300)
            elif col in ('ID', 'Prix', 'Quantité'):
                self.tree.column(col, width=80, anchor='center')
            else:
                self.tree.column(col, width=150)
        
        # Ajouter une scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Configurer le double-clic pour éditer
        self.tree.bind("<Double-1>", self.edit_product)
        
        self.tree.pack(fill='both', expand=True)
        
    def create_action_buttons(self):
        # Boutons d'action
        add_btn = ttk.Button(self.main_frame, text="Ajouter un Produit", command=self.add_product)
        add_btn.grid(row=2, column=0, padx=5, pady=10)
        
        delete_btn = ttk.Button(self.main_frame, text="Supprimer un Produit", command=self.delete_product)
        delete_btn.grid(row=2, column=1, padx=5, pady=10)
        
        refresh_btn = ttk.Button(self.main_frame, text="Rafraîchir", command=self.load_products)
        refresh_btn.grid(row=2, column=2, padx=5, pady=10)
        
        chart_btn = ttk.Button(self.main_frame, text="Voir Graphiques", command=self.show_charts)
        chart_btn.grid(row=2, column=3, padx=5, pady=10)
        
        # Configurer le redimensionnement de la grille
        self.main_frame.grid_rowconfigure(1, weight=1)
        for i in range(4):
            self.main_frame.grid_columnconfigure(i, weight=1)
        
    def load_products(self):
        # Effacer les données existantes
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Charger les produits de la base de données
        self.cursor.execute("""
            SELECT p.id, p.name, p.description, p.price, p.quantity, c.name
            FROM product p
            JOIN category c ON p.id_category = c.id
            ORDER BY p.id
        """)
        
        products = self.cursor.fetchall()
        
        # Ajouter les produits au tableau
        for product in products:
            self.tree.insert("", "end", values=(
                product[0],
                product[1],
                product[2],
                f"{product[3]} €",
                product[4],
                product[5]
            ))
    
    def get_categories(self):
        # Récupérer les catégories disponibles
        self.cursor.execute("SELECT id, name FROM category ORDER BY name")
        return {name: id for id, name in self.cursor.fetchall()}
    
    def add_product(self):
        # Créer une fenêtre de dialogue
        dialog = tk.Toplevel(self.root)
        dialog.title("Ajouter un Produit")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Créer les champs de saisie
        ttk.Label(dialog, text="Nom:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Description:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        desc_entry = tk.Text(dialog, width=30, height=5)
        desc_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Prix (€):").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        price_entry = ttk.Entry(dialog, width=40)
        price_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Quantité:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        qty_entry = ttk.Entry(dialog, width=40)
        qty_entry.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Catégorie:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
        
        # Récupérer les catégories
        categories = self.get_categories()
        category_combo = ttk.Combobox(dialog, values=list(categories.keys()), state="readonly", width=38)
        category_combo.grid(row=4, column=1, padx=10, pady=5)
        if categories:
            category_combo.current(0)
        
        # Boutons
        def save_product():
            # Validation des champs
            name = name_entry.get().strip()
            description = desc_entry.get("1.0", tk.END).strip()
            
            try:
                price = int(price_entry.get().strip())
                if price < 0:
                    raise ValueError("Le prix doit être positif")
            except ValueError:
                messagebox.showerror("Erreur", "Le prix doit être un nombre entier positif")
                return
            
            try:
                quantity = int(qty_entry.get().strip())
                if quantity < 0:
                    raise ValueError("La quantité doit être positive")
            except ValueError:
                messagebox.showerror("Erreur", "La quantité doit être un nombre entier positif")
                return
            
            category = category_combo.get()
            if not category:
                messagebox.showerror("Erreur", "Veuillez sélectionner une catégorie")
                return
            
            try:
                # Insérer le produit dans la base de données
                self.cursor.execute("""
                    INSERT INTO product (name, description, price, quantity, id_category) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, description, price, quantity, categories[category]))
                self.conn.commit()
                
                messagebox.showinfo("Succès", "Produit ajouté avec succès")
                dialog.destroy()
                self.load_products()
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout du produit: {e}")
        
        save_btn = ttk.Button(dialog, text="Enregistrer", command=save_product)
        save_btn.grid(row=5, column=0, padx=10, pady=20)
        
        cancel_btn = ttk.Button(dialog, text="Annuler", command=dialog.destroy)
        cancel_btn.grid(row=5, column=1, padx=10, pady=20)
    
    def edit_product(self, event):
        # Récupérer l'élément sélectionné
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        # Récupérer les valeurs
        item = self.tree.item(selected_item[0])
        product_id = item['values'][0]
        
        # Récupérer les informations complètes du produit
        self.cursor.execute("""
            SELECT p.id, p.name, p.description, p.price, p.quantity, p.id_category, c.name
            FROM product p
            JOIN category c ON p.id_category = c.id
            WHERE p.id = %s
        """, (product_id,))
        
        product = self.cursor.fetchone()
        if not product:
            return
        
        # Créer une fenêtre de dialogue
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Modifier le Produit: {product[1]}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Créer les champs de saisie avec les valeurs actuelles
        ttk.Label(dialog, text="Nom:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.insert(0, product[1])
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Description:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        desc_entry = tk.Text(dialog, width=30, height=5)
        desc_entry.insert("1.0", product[2])
        desc_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Prix (€):").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        price_entry = ttk.Entry(dialog, width=40)
        price_entry.insert(0, product[3])
        price_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Quantité:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        qty_entry = ttk.Entry(dialog, width=40)
        qty_entry.insert(0, product[4])
        qty_entry.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Catégorie:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
        
        # Récupérer les catégories
        categories = self.get_categories()
        category_combo = ttk.Combobox(dialog, values=list(categories.keys()), state="readonly", width=38)
        category_combo.grid(row=4, column=1, padx=10, pady=5)
        # Sélectionner la catégorie actuelle
        for i, (cat_name, cat_id) in enumerate(categories.items()):
            if cat_id == product[5]:
                category_combo.current(i)
                break
        
        # Boutons
        def update_product():
            # Validation des champs
            name = name_entry.get().strip()
            description = desc_entry.get("1.0", tk.END).strip()
            
            try:
                price = int(price_entry.get().strip())
                if price < 0:
                    raise ValueError("Le prix doit être positif")
            except ValueError:
                messagebox.showerror("Erreur", "Le prix doit être un nombre entier positif")
                return
            
            try:
                quantity = int(qty_entry.get().strip())
                if quantity < 0:
                    raise ValueError("La quantité doit être positive")
            except ValueError:
                messagebox.showerror("Erreur", "La quantité doit être un nombre entier positif")
                return
            
            category = category_combo.get()
            if not category:
                messagebox.showerror("Erreur", "Veuillez sélectionner une catégorie")
                return
            
            try:
                # Mettre à jour le produit dans la base de données
                self.cursor.execute("""
                    UPDATE product 
                    SET name = %s, description = %s, price = %s, quantity = %s, id_category = %s
                    WHERE id = %s
                """, (name, description, price, quantity, categories[category], product_id))
                self.conn.commit()
                
                messagebox.showinfo("Succès", "Produit mis à jour avec succès")
                dialog.destroy()
                self.load_products()
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la mise à jour du produit: {e}")
        
        save_btn = ttk.Button(dialog, text="Enregistrer", command=update_product)
        save_btn.grid(row=5, column=0, padx=10, pady=20)
        
        cancel_btn = ttk.Button(dialog, text="Annuler", command=dialog.destroy)
        cancel_btn.grid(row=5, column=1, padx=10, pady=20)
    
    def delete_product(self):
        # Récupérer l'élément sélectionné
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un produit à supprimer")
            return
        
        # Récupérer l'ID du produit
        item = self.tree.item(selected_item[0])
        product_id = item['values'][0]
        product_name = item['values'][1]
        
        # Demander confirmation
        confirm = messagebox.askyesno(
            "Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer le produit '{product_name}'?"
        )
        
        if confirm:
            try:
                # Supprimer le produit
                self.cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
                self.conn.commit()
                
                messagebox.showinfo("Succès", "Produit supprimé avec succès")
                self.load_products()
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")
    
    def show_charts(self):
        # Créer une nouvelle fenêtre pour les graphiques
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Statistiques des Produits")
        chart_window.geometry("800x600")
        chart_window.transient(self.root)
        
        # Créer un notebook pour les différents graphiques
        notebook = ttk.Notebook(chart_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Onglet 1: Produits par catégorie
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Produits par Catégorie")
        
        # Onglet 2: Valeur du stock
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Valeur du Stock")
        
        # Créer le graphique des produits par catégorie
        self.cursor.execute("""
            SELECT c.name, COUNT(p.id) as product_count
            FROM category c
            LEFT JOIN product p ON c.id = p.id_category
            GROUP BY c.name
            ORDER BY product_count DESC
        """)
        
        categories_data = self.cursor.fetchall()
        
        if categories_data:
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            
            categories = [cat[0] for cat in categories_data]
            counts = [cat[1] for cat in categories_data]
            
            ax1.bar(categories, counts, color='skyblue')
            ax1.set_title('Nombre de Produits par Catégorie')
            ax1.set_xlabel('Catégorie')
            ax1.set_ylabel('Nombre de Produits')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
            canvas1.draw()
            canvas1.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Créer le graphique de la valeur du stock
        self.cursor.execute("""
            SELECT c.name, SUM(p.price * p.quantity) as stock_value
            FROM category c
            LEFT JOIN product p ON c.id = p.id_category
            GROUP BY c.name
            ORDER BY stock_value DESC
        """)
        
        value_data = self.cursor.fetchall()
        
        if value_data:
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            
            categories = [cat[0] for cat in value_data]
            values = [float(cat[1]) if cat[1] else 0 for cat in value_data]
            
            ax2.pie(values, labels=categories, autopct='%1.1f%%', shadow=True, startangle=90)
            ax2.axis('equal')
            ax2.set_title('Valeur du Stock par Catégorie')
            
            plt.tight_layout()
            
            canvas2 = FigureCanvasTkAgg(fig2, master=tab2)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Bouton pour fermer la fenêtre
        ttk.Button(chart_window, text="Fermer", command=chart_window.destroy).pack(pady=10)
    
    def __del__(self):
        # Fermer la connexion à la base de données
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("Connexion à la base de données fermée")

# Fonction principale
def main():
    root = tk.Tk()
    app = StoreApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()