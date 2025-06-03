import time
import osmnx as ox
import folium
from branca.element import Element
from geopy.geocoders import Nominatim
import webbrowser
from datetime import datetime
import networkx as nx

# Catat waktu mulai eksekusi
start_time = time.time()

# Konfigurasi awal OSMnx
ox.settings.log_console = True
ox.settings.use_cache = True
ox.settings.timeout = 300

# Fungsi untuk menghitung estimasi waktu tempuh berdasarkan jarak (meter)
def calculate_travel_times(distance):
    speeds = {
        'jalan_kaki': 1.4,    # ~5 km/jam
        'motor': 8.33,        # ~30 km/jam
        'mobil': 11.11        # ~40 km/jam
    }
    times = {}
    for mode, speed in speeds.items():
        seconds = distance / speed
        mins, secs = divmod(int(seconds), 60)
        times[mode] = f"{mins:02d}:{secs:02d}"
    return times

# Fungsi untuk mengambil atribut edge (misalnya panjang jalan)
def get_route_edge_attributes(G, route, attribute):
    attributes = []
    for u, v in zip(route[:-1], route[1:]):
        if G.has_edge(u, v):
            edge_data = G.get_edge_data(u, v)
            if edge_data:
                first_edge = next(iter(edge_data.values()))
                attributes.append(first_edge.get(attribute, 0))
    return attributes

# Fungsi untuk mengambil waktu sekarang
def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M %a, %d %b")

# Fungsi dummy untuk kemacetan
def get_dummy_congested_edges(G, route_main):
    edge_list = list(zip(route_main[:-1], route_main[1:]))
    n = len(edge_list)
    
    if n < 3:
        return edge_list

    indices = [n // 4, n // 2, 3 * n // 4]
    return [edge_list[i] for i in indices if i < n]

# Algoritma Dijkstra dengan penalti kemacetan
def find_shortest_path_dijkstra(G, start, end, congested_edges=None, penalty_factor=3):
    try:
        G_temp = G.copy()
        if congested_edges:
            for u, v in congested_edges:
                if G_temp.has_edge(u, v):
                    for key in G_temp[u][v]:
                        G_temp[u][v][key]["length"] *= penalty_factor
        route = nx.shortest_path(G_temp, start, end, weight="length")
        edge_lengths = get_route_edge_attributes(G_temp, route, "length")
        distance = sum(edge_lengths)
        return route, distance
    except Exception as e:
        print(f"Error Dijkstra: {e}")
        return None, 0

# Fungsi utama
def main():
    print("Memuat peta Kota Bengkulu...")
    try:
        G = ox.graph_from_place("Bengkulu, Indonesia", network_type='drive', simplify=True)
        G = G.to_undirected()
        print("Peta berhasil dimuat!")
        print(f"Jumlah node: {len(G.nodes())}")
        print(f"Jumlah edge: {len(G.edges())}")
    except Exception as e:
        print(f"Error: {e}")
        return

    print("\n" + "="*40)
    print("BENGKULU NAVIGATOR".center(40))
    print("="*40 + "\n")

    geolocator = Nominatim(user_agent="bengkulu_navigator")

    start_place = input("Tentukan lokasi awal (contoh: Pasar Panorama): ").strip()
    end_place = input("Tentukan lokasi tujuan (contoh: Masjid Raya Baitul Izzah): ").strip()

    def get_coords(place):
        try:
            location = geolocator.geocode(place + ", Bengkulu, Indonesia")
            if location:
                return (location.latitude, location.longitude)
            print(f"Lokasi '{place}' tidak ditemukan!")
            return None
        except Exception as e:
            print(f"Error geocoding {place}: {e}")
            return None

    start_coords = get_coords(start_place)
    end_coords = get_coords(end_place)

    if not start_coords or not end_coords:
        print("Tidak dapat melanjutkan karena lokasi tidak valid!")
        return

    start_node = ox.distance.nearest_nodes(G, start_coords[1], start_coords[0])
    end_node = ox.distance.nearest_nodes(G, end_coords[1], end_coords[0])

    print("\nMenghitung rute terbaik...")
    route_main, distance_main = find_shortest_path_dijkstra(G, start_node, end_node)
    if not route_main or distance_main == 0:
        print("Tidak dapat menemukan rute utama!")
        return

    congested_edges = get_dummy_congested_edges(G, route_main)
    route_alt, distance_alt = find_shortest_path_dijkstra(G, start_node, end_node, congested_edges=congested_edges)
    kemacetan_terdeteksi = route_alt and route_alt != route_main 

    print("Membuat peta interaktif...")
    m = folium.Map(location=start_coords, zoom_start=14, tiles='OpenStreetMap')

    # Fungsi bantu cek edge kemacetan
    def is_congested_edge(u, v, congested_edges):
        return (u, v) in congested_edges or (v, u) in congested_edges

    # Kembali ke indentasi utama
    for u, v in zip(route_main[:-1], route_main[1:]):
        segment_coords = [(G.nodes[u]['y'], G.nodes[u]['x']), (G.nodes[v]['y'], G.nodes[v]['x'])]
        if is_congested_edge(u, v, congested_edges):
            color = '#FF0000'  # merah
        else:
            color = '#4285F4'  # biru
        folium.PolyLine(segment_coords, color=color, weight=6, opacity=0.8).add_to(m)

        # Rute alternatif (jika ada kemacetan)
        if kemacetan_terdeteksi and route_alt:
            route_coords_alt = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route_alt]
            folium.PolyLine(route_coords_alt, color='#FFA500', weight=5, opacity=0.9,
                            tooltip=f"Rute Alternatif: {distance_alt:.0f} meter", dash_array="5,10").add_to(m)

                
         # --- Tambahkan UI peringatan kemacetan di pojok bawah menggunakan branca ---

    warning_html = """
<div style="
    position: fixed;
    bottom: 50px;
    right: 50px;  /* dari left ke right */
    z-index: 9999;
    background-color: #fff3cd;
    padding: 15px;
    border: 2px solid #ffecb5;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    font-size: 14px;
    width: 300px;
">
    <strong style="color:#856404;">⚠️ Peringatan Kemacetan</strong>
    <p>Rute utama melewati jalan yang macet. Rute alternatif ditampilkan (warna oranye).</p>
</div>
"""
    warning_element = Element(warning_html)
    m.get_root().html.add_child(warning_element)

     # Marker peringatan di lokasi awal
    folium.Marker(
        location=start_coords,
        popup=folium.Popup("<b>PERINGATAN KEMACETAN TERDETEKSI!</b><br>Disarankan memilih rute alternatif.", max_width=300),
        icon=folium.Icon(color='red', icon='exclamation-triangle', prefix='fa')
    ).add_to(m)

    print("\n>>> PERINGATAN: Kemacetan terdeteksi pada rute utama. Disarankan menggunakan rute alternatif.")

    # Marker lokasi
    folium.Marker(location=start_coords, popup=f"<b>Start:</b> {start_place}",
                  icon=folium.Icon(color='green', icon='play', prefix='fa')).add_to(m)

    folium.Marker(location=end_coords, popup=f"<b>Tujuan:</b> {end_place}",
                  icon=folium.Icon(color='red', icon='stop', prefix='fa')).add_to(m)

    travel_times = calculate_travel_times(distance_main)
    current_time = get_current_time()

    # Info box HTML di sudut peta
    info_html = f"""
    <div style="position: fixed; bottom: 20px; left: 20px; 
                width: 300px; background: white; padding: 15px;
                border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                z-index: 9999; font-family: 'Segoe UI', Arial, sans-serif;
                border-top: 4px solid #4285F4;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <div style="font-size: 16px; font-weight: bold; color: #4285F4;">BENGKULU Navigator</div>
            <div style="font-size: 12px; color: #666;">{current_time}</div>
        </div>
        <div style="margin-bottom: 15px;">
            <div style="display: flex; margin-bottom: 5px;">
                <div style="width: 8px; height: 8px; background: #0F9D58; border-radius: 50%; margin-top: 5px; margin-right: 8px;"></div>
                <div style="font-size: 14px;"><b>Start:</b> {start_place}</div>
            </div>
            <div style="display: flex;">
                <div style="width: 8px; height: 8px; background: #DB4437; border-radius: 50%; margin-top: 5px; margin-right: 8px;"></div>
                <div style="font-size: 14px;"><b>Tujuan:</b> {end_place}</div>
            </div>
        </div>
        <div style="background: #F5F5F5; padding: 10px; border-radius: 8px; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-size: 14px;">Jarak</span>
                <span style="font-weight: bold; color: #4285F4;">{distance_main:.0f} meter</span>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 13px;">
            <div style="text-align: center; padding: 5px; border-radius: 6px; background: #E6F4EA;">
                <div><b>Jalan Kaki</b><br>{travel_times['jalan_kaki']} menit</div>
            </div>
            <div style="text-align: center; padding: 5px; border-radius: 6px; background: #FFF3E0;">
                <div><b>Motor</b><br>{travel_times['motor']} menit</div>
            </div>
            <div style="text-align: center; padding: 5px; border-radius: 6px; background: #E3F2FD;">
                <div><b>Mobil</b><br>{travel_times['mobil']} menit</div>
            </div>
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(info_html))

    legend_html = """
    <div style="
        position: fixed;
        top: 20px;
        right: 20px;
        z-index:9999;
        background-color:white;
        padding:10px;
        border-radius:8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        font-size:14px;
        line-height: 1.5;
    ">
        <strong>Legenda:</strong><br>
        <span style="color:#FF0000;">■</span> Jalan Macet<br>
        <span style="color:#4285F4;">■</span> Rute Utama Lancar<br>
        <span style="color:#FFA500;">■</span> Rute Alternatif
    </div>
    """
    m.get_root().html.add_child(Element(legend_html))

    # Simpan & buka peta
    map_file = "bengkulu_navigator.html"
    m.save(map_file)
    webbrowser.open(map_file)

    print("\nRute berhasil dihitung dan ditampilkan di browser!")
    print(f"Total waktu eksekusi: {time.time() - start_time:.2f} detik.")

if __name__ == "__main__":
    main()
