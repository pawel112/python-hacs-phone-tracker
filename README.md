# Phone Tracker

Integracja HACS do wykrywania urządzenia (telefonu) w sieci lokalnej przez ping.

## Funkcje
- Encja `binary_sensor` o nazwie **Połączono** — `Connected` / `Disconnected`
- Pingowanie co 30 sekund
- Atrybut `ostatnio_widziany` — timestamp ostatniego wykrycia
- Ikona zmienia się zależnie od stanu (wifi / wifi-off)

## Instalacja przez HACS
1. HACS → Integracje → ⋮ → Repozytoria niestandardowe
2. Wklej URL repo → Kategoria: **Integracja** → Dodaj
3. Zainstaluj **Phone Tracker** → Uruchom ponownie HA
4. **Ustawienia → Urządzenia i usługi → Dodaj integrację → Phone Tracker**
5. Wpisz nazwę urządzenia i adres IP

## Ważne
Ustaw **stały IP** telefonu w routerze (rezerwacja DHCP po MAC-u), inaczej IP może się zmienić po restarcie telefonu.
