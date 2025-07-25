import rio

class Dashboard(rio.Component):
    """
    The main UI component. This will be the foundation for our web interface.
    It displays a simple set of tabs for the application's features.
    """
    def build(self):
        return rio.Column(
            rio.Text("Dependency Doctor", style="heading1", align_x=0.5),
            rio.Tabs(
                ("Dashboard", self._build_placeholder_page("Welcome to the Dashboard")),
                ("Dependencies", self._build_placeholder_page("Dependency Scanner Page")),
                ("Security", self._build_placeholder_page("Security Analysis Page")),
                ("Updates", self._build_placeholder_page("Dependency Update Page")),
            ),
            spacing=2,
            margin=2,
        )

    def _build_placeholder_page(self, text: str) -> rio.Component:
        """A helper to create a consistent placeholder for pages under development."""
        return rio.Card(
            content=rio.Text(text, align_x=0.5, justify="center"),
            corner_radius=12,
            margin=2,
        ) 