from typing import override

from app.domain.interfaces.i_parser import IParser
from app.domain.models.models import Place, Transition, Arc, Point
from app.domain.models.petri_model import PetriModel
import xml.etree.ElementTree as ET


class PNMLParser(IParser):

    @override
    def parse(self, file_path: str) -> PetriModel:
        tree = ET.parse(file_path)
        root = tree.getroot()

        ns = self._get_namespace(root)

        places, transitions, arcs = [], [], []

        for place_el in self._findall(ns, root, "place"):
            place = self._parse_place(place_el, ns)
            places.append(place)

        for trans_el in self._findall(ns, root, "transition"):
            transition = self._parse_transition(trans_el, ns)
            transitions.append(transition)

        for arc_el in self._findall(ns, root, "arc"):
            arc = self._parse_arc(arc_el, ns, places, transitions)
            arcs.append(arc)

        return PetriModel(places=places, transitions=transitions, arcs=arcs)

    def _findall(self, ns, element, tag):
        if ns:
            return element.findall(f".//{{{ns}}}{tag}")
        return element.findall(f".//{tag}")

    def _get_namespace(self, root):
        """Extracts namespace if exist"""
        if root.tag.startswith("{"):
            return root.tag[1:].split("}")[0]
        return ""

    def _parse_place(self, el, ns):
        graphics = el.find(f".//{{{ns}}}graphics") if ns else el.find(".//graphics")
        position = graphics.find(f".//{{{ns}}}position") if ns else graphics.find(".//position")
        dim = graphics.find(f".//{{{ns}}}dimension") if ns else graphics.find(".//dimension")

        id = el.get("id")
        x = int(position.get("x"))
        y = int(position.get("y"))
        radius = float(dim.get("x")) / 2 if dim is not None else 10

        place = Place((x, y, radius), id=id)
        name_el = el.find(f".//{{{ns}}}name/{{{ns}}}text") if ns else el.find(".//name/text")
        if name_el is not None and name_el.text:
            place.text.append(name_el.text)
        return place

    def _parse_transition(self, el, ns):
        graphics = el.find(f".//{{{ns}}}graphics") if ns else el.find(".//graphics")
        position = graphics.find(f".//{{{ns}}}position") if ns else graphics.find(".//position")
        dim = graphics.find(f".//{{{ns}}}dimension") if ns else graphics.find(".//dimension")

        id = el.get("id")
        x = int(position.get("x"))
        y = int(position.get("y"))

        width = float(dim.get("x"))
        height = float(dim.get("y"))
        transition = Transition((x, y), width, height, id=id)
        return transition

    def _parse_arc(self, el, ns, places, transitions):
        source_id = el.get("source")
        target_id = el.get("target")

        all_nodes = {n.id: n for n in (places + transitions)}

        source = all_nodes.get(source_id)
        target = all_nodes.get(target_id)

        if source is None or target is None:
            # Log and return None to indicate this arc should be skipped by caller
            missing = []
            if source is None:
                missing.append(f"source '{source_id}'")
            if target is None:
                missing.append(f"target '{target_id}'")
            print(f"Skipping arc {el.get('id')} — missing {' and '.join(missing)}")
            return None

        # Try to extract start/end point from graphics if present

        graphics = el.find(f".//{{{ns}}}graphics") if ns else el.find(".//graphics")
        start_point = self._get_point_from_elem(graphics, ns)
        # Some PNML variants store <start> and <end> inside <graphics> or inside <toolinformation> - try heuristics:
        # try explicit child named 'start'/'end'
        if start_point is None:
            start_el = el.find(f".//{{{ns}}}start") if ns else el.find(".//start")
            start_point = self._get_point_from_elem(start_el, ns)

        end_point = None
        if graphics is not None:
            end_point = self._get_point_from_elem(graphics.find(f".//{{{ns}}}end") if ns else graphics.find(".//end"), ns)
        if end_point is None:
            end_el = el.find(f".//{{{ns}}}end") if ns else el.find(".//end")
            end_point = self._get_point_from_elem(end_el, ns)

        # If no explicit points found, fall back to source/target centers (useful for rendering)
        if start_point is None:
            try:
                # If source has center attribute as Place/Transition with .center
                start_point = Point(source.center.x, source.center.y)
            except Exception:
                start_point = None

        if end_point is None:
            try:
                end_point = Point(target.center.x, target.center.y)
            except Exception:
                end_point = None

        # Create Arc object linking the actual node objects
        arc = Arc(source=source, target=target, start_point=start_point, end_point=end_point)

        # inscription / weight
        inscription = el.find(f".//{{{ns}}}inscription/{{{ns}}}text") if ns else el.find(".//inscription/text")
        if inscription is not None and inscription.text:
            try:
                arc.weight = int(inscription.text.strip())
            except Exception:
                # if not an integer, try float then fallback to 1
                try:
                    arc.weight = int(float(inscription.text.strip()))
                except Exception:
                    arc.weight = 1

        return arc

    def _get_point_from_elem(self, parent, ns):
        if parent is None:
            return None
        pos_el = parent.find(f".//{{{ns}}}position") if ns else parent.find(".//position")
        if pos_el is None:
            return None
        try:
            x = float(pos_el.get("x", 0))
            y = float(pos_el.get("y", 0))
            return Point(int(x), int(y))
        except Exception:
            return None
