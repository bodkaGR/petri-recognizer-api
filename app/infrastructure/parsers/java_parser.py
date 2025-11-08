import re

from typing_extensions import override

from app.domain.interfaces.i_parser import IParser
from app.domain.models.models import Place, Transition, Arc, Point
from app.domain.models.petri_model import PetriModel
from app.infrastructure.handlers.file_handler import FileHandler


class JavaParser(IParser):

    @override
    def parse(self, file_path: str) -> PetriModel:
        content = FileHandler.load(file_path)

        place_pattern = re.compile(r'new\s+PetriP\("(?P<name>[^"]+)",\s*(?P<markers>\d+)\)')
        places, transitions, arcs = [], [], []
        for idx, match in enumerate(place_pattern.finditer(content)):
            name = match.group("name")
            markers = int(match.group("markers"))
            place = Place((100 + idx * 60, 200, 20), id=name)
            place.markers = markers
            places.append(place)

        transition_pattern = re.compile(r'new\s+PetriT\("(?P<name>[^"]+)",\s*[\d\.]+')
        for idx, match in enumerate(transition_pattern.finditer(content)):
            name = match.group("name")
            transition = Transition((100 + idx * 60, 400), 40, 10, id=name)
            transitions.append(transition)

        arc_in_pattern = re.compile(r'new\s+ArcIn\(d_P\.get\((?P<p>\d+)\),\s*d_T\.get\((?P<t>\d+)\),\s*(?P<w>\d+)\)')
        arc_out_pattern = re.compile(r'new\s+ArcOut\(d_T\.get\((?P<t>\d+)\),\s*d_P\.get\((?P<p>\d+)\),\s*(?P<w>\d+)\)')

        for match in arc_in_pattern.finditer(content):
            p_idx = int(match.group("p"))
            t_idx = int(match.group("t"))
            w = int(match.group("w"))
            source = places[p_idx]
            target = transitions[t_idx]
            arc = Arc(source, target, Point(source.center.x, source.center.y), Point(target.center.x, target.center.y))
            arc.weight = w
            arcs.append(arc)

        for match in arc_out_pattern.finditer(content):
            t_idx = int(match.group("t"))
            p_idx = int(match.group("p"))
            w = int(match.group("w"))
            source = transitions[t_idx]
            target = places[p_idx]
            arc = Arc(source, target, Point(source.center.x, source.center.y), Point(target.center.x, target.center.y))
            arc.weight = w
            arcs.append(arc)

        model = PetriModel(places=places, transitions=transitions, arcs=arcs)
        return model