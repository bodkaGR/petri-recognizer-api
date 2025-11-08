from typing import override

from app.domain.interfaces.i_parser import IParser
from app.domain.models.models import Place, Transition, Arc, Point
from app.domain.models.petri_model import PetriModel
import xml.etree.ElementTree as ET

from app.utils.xml_utils import XMLUtils


class PNMLParser(IParser):

    @override
    def parse(self, file_path: str) -> PetriModel:
        tree = ET.parse(file_path)
        root = tree.getroot()

        ns = XMLUtils.get_namespace(root)

        places, transitions, arcs = [], [], []

        for place_el in XMLUtils.find_all(root, "place", ns):
            place = self._parse_place(place_el, ns)
            places.append(place)

        for trans_el in XMLUtils.find_all(root, "transition", ns):
            transition = self._parse_transition(trans_el, ns)
            transitions.append(transition)

        for arc_el in XMLUtils.find_all(root, "arc", ns):
            arc = self._parse_arc(arc_el, ns, places, transitions)
            arcs.append(arc)

        return PetriModel(places=places, transitions=transitions, arcs=arcs)

    def _parse_place(self, el, ns) -> Place:
        """Parse <place> element into Place object"""
        place_id = el.get("id")
        position = XMLUtils.find(el, "graphics/position", ns)
        coordinates = XMLUtils.find(el, "toolspecific/coordinates", ns)
        markers = XMLUtils.find(el, "initialMarking/text", ns)
        name_el = XMLUtils.find(el, "name/text", ns)

        x = int(position.get("x")) if position is not None else 0
        y = int(position.get("y")) if position is not None else 0
        radius = float(coordinates.get("x")) / 2 if coordinates is not None else 10

        place = Place((x, y, radius), id=place_id)

        if name_el is not None and name_el.text:
            place.text.append(name_el.text.strip())

        if int(markers.text) > 0:
            place.markers += int(markers.text)

        return place

    def _parse_transition(self, el, ns) -> Transition:
        """Parse <transition> element into Transition object"""
        trans_id = el.get("id")
        position = XMLUtils.find(el, "graphics/position", ns)
        coordinates = XMLUtils.find(el, "toolspecific/coordinates", ns)
        name_el = XMLUtils.find(el, "name/text", ns)

        x = int(position.get("x"))
        y = int(position.get("y"))

        width = float(coordinates.get("x"))
        height = float(coordinates.get("y"))

        transition = Transition((x, y), width, height, id=trans_id)

        if name_el is not None and name_el.text:
            transition.text.append(name_el.text.strip())

        return transition

    def _parse_arc(self, el, ns, places, transitions) -> Arc:
        """Parse <arc> element and connect its source and target nodes"""
        source_id = el.get("source")
        target_id = el.get("target")

        # Build lookup map for all nodes
        nodes = {n.id: n for n in (places + transitions)}

        source = nodes.get(source_id)
        target = nodes.get(target_id)

        if not source or not target:
            # Log and return None to indicate this arc should be skipped by caller
            missing = []
            if source is None:
                missing.append(f"source '{source_id}'")
            if target is None:
                missing.append(f"target '{target_id}'")
            print(f"Skipping arc {el.get('id')} — missing {' and '.join(missing)}")
            return None

        start_point = self._get_endpoint(el, ns, "start") or Point(source.center.x, source.center.y)
        end_point = self._get_endpoint(el, ns, "end") or Point(target.center.x, target.center.y)

        # Create Arc object linking the actual node objects
        arc = Arc(source=source, target=target, start_point=start_point, end_point=end_point)
        arc.weight = self._parse_weight(el, ns)
        return arc

    def _get_endpoint(self, el, ns, tag) -> Point | None:
        """Extract endpoint <start>/<end> position from arc element"""
        pos = XMLUtils.find(el, f"{tag}/position", ns)
        if pos is None:
            return None
        try:
            x = float(pos.get("x"))
            y = float(pos.get("y"))
            return Point(x, y)
        except ValueError: # TODO: Add custom exception and handlers
            return None

    def _parse_weight(self, el, ns) -> int:
        """Extract arc weight from <inscription><text>"""
        inscription = XMLUtils.find(el, "inscription/text", ns)
        if inscription is None or not inscription.text:
            return 1
        try:
            return int(inscription.text.strip())
        except ValueError: # TODO: Add custom exception and handlers
            try:
                return int(float(inscription.text.strip()))
            except Exception: # TODO: Add custom exception and handlers
                return 1