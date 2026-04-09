import re

def parse_data(file_content):
    """
    Vyčistí a rozparsuje surová data ze serveru.
    Ignoruje zalomení řádků a systémové tagy, aby data byla konzistentní.
    """
    # Odstranění zalomení řádků a případných tagů 
    clean_content = file_content.replace('\n', ' ')
    clean_content = re.sub(r'\', '', clean_content)
    
    # Regulární výraz pro extrakci: Název | Velikost | Hodnota
    pattern = r"\[FILE\]\s+([a-zA-Z0-9_.-]+)\s+\|\s+Size:\s+(\d+)\s+MB\s+\|\s+Val:\s+(\d+)\s+Credits"
    matches = re.findall(pattern, clean_content)
    
    files = []
    for match in matches:
        files.append({
            'name': match[0].strip(),
            'size': int(match[1]),
            'value': int(match[2])
        })
    return files

def execute_blackout(files, max_capacity_mb):
    """
    Vyřeší 0/1 Knapsack problem pomocí dynamického programování.
    """
    n = len(files)
    # Vytvoření DP matice: dp[položka][kapacita]
    dp = [[0 for _ in range(max_capacity_mb + 1)] for _ in range(n + 1)]
    
    # 1. Krok: Vybudování DP matice
    for i in range(1, n + 1):
        file = files[i-1]
        size = file['size']
        value = file['value']
        
        for w in range(1, max_capacity_mb + 1):
            if size <= w:
                # Maximum z: "nevezmu aktuální" vs "vezmu aktuální + zbytek kapacity"
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-size] + value)
            else:
                # Soubor se nevejde, hodnota zůstává stejná jako bez něj
                dp[i][w] = dp[i-1][w]
                
    # 2. Krok: Zpětné trasování (jaké soubory jsme vlastně vybrali)
    max_credits = dp[n][max_capacity_mb]
    w = max_capacity_mb
    selected_files = []
    
    for i in range(n, 0, -1):
        if max_credits <= 0:
            break
        # Pokud hodnota pochází z předchozího řádku, soubor jsme nebrali
        if max_credits == dp[i-1][w]:
            continue
        else:
            # Soubor jsme brali, zaznamenáme ho a odečteme jeho parametry
            file = files[i-1]
            selected_files.append(file)
            max_credits -= file['value']
            w -= file['size']
            
    return selected_files, dp[n][max_capacity_mb]

# --- Spuštění operace ---
if __name__ == "__main__":
    SPEED_MB_S = 20
    TIME_LIMIT_S = 300
    CAPACITY = SPEED_MB_S * TIME_LIMIT_S # 6000 MB
    
    # Načtení dat (zde předpokládáme, že soubor data.txt je ve stejné složce)
    with open('data.txt', 'r', encoding='utf-8') as f:
        raw_data = f.read()
        
    extracted_files = parse_data(raw_data)
    
    print(f"[*] Operace Blackout inicializována...")
    print(f"[*] Detekováno {len(extracted_files)} souborů.")
    print(f"[*] Maximální kapacita pro exfiltraci: {CAPACITY} MB\n")
    
    stolen_files, total_value = execute_blackout(extracted_files, CAPACITY)
    
    # Výstupní report
    total_size = sum(f['size'] for f in stolen_files)
    total_time = total_size / SPEED_MB_S
    
    print("=== REPORT Z EXFILTRACE ===")
    for f in stolen_files:
        print(f"[+] Staženo: {f['name']} ({f['size']} MB, {f['value']} Credits)")
        
    print("===========================")
    print(f"Celková hodnota (Credits):  {total_value}")
    print(f"Celková stažená velikost:   {total_size} MB")
    print(f"Spotřebovaný čas:           {total_time:.1f} s / {TIME_LIMIT_S} s")
    print("===========================")
    print("[*] Odpojení úspěšné. Stopy zahlazeny.")