# 🐍 Python Basics - Pour Devs Zéro Python

**Lis ça en 5 minutes avant de lancer l'app !**

---

## 1. Python vs Java - Les différences clés

### ❌ Java
```java
public class Greeting {
    public static void main(String[] args) {
        String name = "John";
        System.out.println("Hello " + name);
    }
}

// Compile: javac Greeting.java
// Exécute: java Greeting
```

### ✅ Python (même chose)
```python
name = "John"
print("Hello " + name)

# Exécute directement: python script.py
```

**Différences:**
- ❌ `public class`, `{`, `}`, `;` = Python n'en a pas besoin
- ✅ Python = plus simple et lisible
- ✅ Python = interprété (exécution directe)
- ❌ Java = compilé d'abord

---

## 2. Indentation (TRÈS important!)

### Java (utilise des `{}`)
```java
if (age > 18) {
    System.out.println("Adult");
} else {
    System.out.println("Child");
}
```

### Python (utilise l'indentation!)
```python
if age > 18:
    print("Adult")
else:
    print("Child")
```

⚠️ **ATTENTION**: L'indentation = structure du code en Python!

```python
# BON ✅
if True:
    print("Indenté")
    print("Toujours indenté")

# MAUVAIS ❌
if True:
print("Pas indenté") # ERREUR!
```

---

## 3. Variables (pas besoin de `type`)

### Java
```java
int age = 30;
String name = "Alice";
double salary = 5000.50;
boolean isActive = true;
```

### Python
```python
age = 30              # Nombre entier
name = "Alice"        # Texte (String)
salary = 5000.50      # Nombre décimal
is_active = True      # Booléen (True/False)
```

**Python devine le type automatiquement!** 🎯

---

## 4. Chaînes de caractères (Strings)

### Concaténation
```python
name = "Alice"
print("Hello " + name)           # "Hello Alice"
print(f"Hello {name}")            # "Hello Alice" (plus moderne)
print("Hello {}".format(name))    # "Hello Alice" (ancien style)
```

---

## 5. Listes (comme Array en Java)

### Java
```java
String[] names = {"Alice", "Bob", "Charlie"};
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
System.out.println(names.get(0)); // "Alice"
```

### Python
```python
names = ["Alice", "Bob", "Charlie"]
print(names[0])    # "Alice"
print(names[-1])   # "Charlie" (dernier)

names.append("David")  # Ajoute
names.remove("Bob")    # Retire
```

---

## 6. Dictionnaires (comme HashMap en Java)

### Java
```java
Map<String, String> person = new HashMap<>();
person.put("name", "Alice");
person.put("age", "30");
System.out.println(person.get("name")); // "Alice"
```

### Python
```python
person = {
    "name": "Alice",
    "age": 30
}
print(person["name"])   # "Alice"
print(person.get("age")) # 30
```

---

## 7. Boucles

### Java
```java
for (int i = 0; i < 3; i++) {
    System.out.println(i);
}

for (String name : names) {
    System.out.println(name);
}
```

### Python
```python
for i in range(3):      # 0, 1, 2
    print(i)

for name in names:
    print(name)
```

---

## 8. Conditions

### Java
```java
if (age > 18) {
    System.out.println("Adult");
} else if (age > 13) {
    System.out.println("Teen");
} else {
    System.out.println("Child");
}
```

### Python
```python
if age > 18:
    print("Adult")
elif age > 13:
    print("Teen")
else:
    print("Child")
```

---

## 9. Fonctions (Méthodes)

### Java
```java
public static String greet(String name) {
    return "Hello " + name;
}

String result = greet("Alice");
System.out.println(result);
```

### Python
```python
def greet(name):
    return "Hello " + name

result = greet("Alice")
print(result)
```

**Pas besoin de `public static` !**

---

## 10. Classes (Objets)

### Java
```java
public class Person {
    private String name;
    private int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public String getName() {
        return this.name;
    }
}

Person alice = new Person("Alice", 30);
System.out.println(alice.getName());
```

### Python
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def get_name(self):
        return self.name

alice = Person("Alice", 30)
print(alice.get_name())
```

**Points clés:**
- `class` = pas `public`
- `__init__` = constructeur
- `self` = `this` en Java
- Pas besoin de types

---

## 11. Imports (Comme `import` en Java)

### Java
```java
import java.util.ArrayList;
import com.example.MyClass;
```

### Python
```python
from datetime import datetime
from src.agent import DataAgent
import json
```

---

## 12. Fichiers et JSON

### Lire un fichier
```python
with open("data.json", "r") as f:
    data = json.load(f)
    print(data)
```

### Écrire un fichier
```python
data = {"name": "Alice", "age": 30}
with open("output.json", "w") as f:
    json.dump(data, f)
```

---

## 13. Try/Except (Exception Handling)

### Java
```java
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Error: " + e);
}
```

### Python
```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
```

---

## 14. Modules et Packages

### Structure Python
```
src/
├── agent/
│   ├── __init__.py       ← Rend "agent" un package
│   ├── agent_data.py
│   └── data_loader.py
└── data/
    └── dossiers.json
```

### Importer
```python
# Depuis main.py
from src.agent import DataAgent
from src.agent.data_loader import DataLoader

agent = DataAgent()
```

---

## 15. Virtual Environment (Très important!)

### C'est quoi ?
Un dossier isolé avec toutes les librairies pour ce projet

### Pourquoi ?
Évite les conflits entre projets (comme Maven pour Java)

### Commandes
```bash
# Créer venv
python -m venv venv

# Activer (Windows)
.\venv\Scripts\Activate

# Activer (Linux/Mac)
source venv/bin/activate

# Installer dépendances
pip install -r requirements.txt

# Désactiver
deactivate
```

---

## 🎯 Résumé des différences

| Concept | Java | Python |
|---------|------|--------|
| **Syntaxe** | Verbeux `{}`, `;` | Simple, lisible |
| **Types** | Déclarés | Auto-détectés |
| **Exécution** | Compilé → java | Interprété → python |
| **Boucles** | `for(;;)` | `for in` |
| **Chaînes** | `"string"` | `"string"` ou `f"string"` |
| **Listes** | `ArrayList<>` | `[]` |
| **Dicts** | `HashMap<>` | `{}` |
| **Try/Catch** | `try {} catch` | `try: except:` |
| **Packages** | `package;` | Dossiers + `__init__.py` |

---

## 📝 Cheat Sheet - Commandes courantes

```python
# Affichage
print("Hello")                # Affiche
print(f"Name: {name}")        # Avec variable

# Variables
x = 10
name = "Alice"
is_active = True
items = [1, 2, 3]
person = {"name": "Alice", "age": 30}

# Boucles
for i in range(5):
    print(i)

for item in items:
    print(item)

# Conditions
if x > 5:
    print("Big")
elif x == 5:
    print("Equal")
else:
    print("Small")

# Fonctions
def add(a, b):
    return a + b

result = add(3, 4)

# Classes
class MyClass:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hi {self.name}"

obj = MyClass("Alice")
print(obj.greet())

# Listes
items = [1, 2, 3]
items.append(4)           # Ajoute
items.remove(2)           # Retire
print(len(items))         # Taille
print(items[0])           # Premier
print(items[-1])          # Dernier

# Dictionnaires
person = {"name": "Alice", "age": 30}
print(person["name"])     # Accès
person["email"] = "a@example.com"  # Ajout
```

---

## 🎓 OK, maintenant quoi ?

1. ✅ Tu as lu ce fichier (5 min)
2. ➡️ Ouvre `GETTING_STARTED.md`
3. ➡️ Suis les étapes exactes
4. ➡️ Lance l'app
5. ➡️ Lis le code source (agent_data.py)

**Aucune connaissance Python préalable n'est nécessaire!** 🚀

---

**Version**: 1.0  
**Pour**: Développeurs zéro Python
