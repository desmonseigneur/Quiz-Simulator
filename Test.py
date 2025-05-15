from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.mapview import MapView

class MapViewApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        # Set the map to Silang, Cavite
        mapview = MapView(zoom=15, lat=14.2307, lon=120.9752)  # Silang, Cavite coordinates
        layout.add_widget(mapview)
        return layout

if __name__ == '__main__':
    MapViewApp().run()