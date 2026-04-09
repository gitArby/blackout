# 🕶️ Operace: Blackout (Data Exfiltration Optimizer)

Tento projekt je nástroj v jazyce Python navržený pro rychlou a optimalizovanou exfiltraci dat ze zabezpečených serverů. Vznikl jako odpověď na časově kritickou situaci, kdy bezpečnostní systém "Cerberus" zahájil trasování připojení s pevným limitem do úplného odpojení.

Skript analyzuje dostupné soubory na serveru a vybírá přesně tu kombinaci, která přinese **největší celkovou hodnotu (Credits)**, aniž by překročila dostupný časový (a tedy datový) limit.

## 🧠 Technické pozadí

Jádrem problému je klasický optimalizační scénář známý jako **Diskrétní problém batohu (0/1 Knapsack Problem)**. 
V našem případě:
* **Batoh (Kapacita):** Maximální objem dat, který lze stáhnout (Rychlost sítě × Časový limit).
* **Předměty:** Soubory na serveru.
* **Váha předmětu:** Velikost souboru (v MB).
* **Hodnota předmětu:** Hodnota souboru (Credits).

Algoritmus využívá **dynamické programování**, které (na rozdíl od "hladového algoritmu") zaručuje nalezení absolutně nejlepší možné kombinace budováním rozhodovací matice.

## 🚀 Vlastnosti

* **Robustní parser dat:** Zvládne přečíst a vyčistit surové výpisy ze serverových logů (včetně nestandardního formátování a systémových tagů).
* **100% Přesnost:** Využívá matici dynamického programování pro nalezení matematického maxima zisku.
* **Zpětné trasování:** Z matice zpětně zrekonstruuje přesný seznam souborů, které je nutné stáhnout.
* **Přehledný report:** Vygeneruje detailní výstup o exfiltrovaných datech, spotřebovaném čase a celkovém zisku.

## ⚙️ Konfigurace a parametry

Výchozí parametry spojení jsou nastaveny přímo ve skriptu:
* **Rychlost stahování:** `20 MB/s`
* **Časový limit:** `300 sekund` (5 minut)
* *Celková datová kapacita činí 6000 MB.*
