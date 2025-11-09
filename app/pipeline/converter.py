import pickle
import pm4py
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from collections import Counter, defaultdict
from typing import List, Tuple
from app.domain.models.models import Place, Transition, Arc
from app.domain.models.petri_model import PetriModel
from config.path_config import (
    OUTPUT_DIR, TEMPLATES_DIR, VISUALIZATIONS_DIR, PIPELINE_OUTPUT_DIR,
    PLACES_PKL_PATH, TRANSITIONS_PKL_PATH, ARCS_PKL_PATH,
    PLACES_FIXED_PKL_PATH, TRANSITIONS_FIXED_PKL_PATH, ARCS_FIXED_PKL_PATH,
    OUTPUT_PNML_PATH, OUTPUT_PETRIOBJ_PATH, OUTPUT_JSON_PATH, OUTPUT_PNG_PATH, OUTPUT_GV_PATH,
    WORKING_IMAGE_PATH, ensure_directories_exist, get_visualization_path, get_output_file_path
)

def process_elements(places: List[Place], transitions: List[Transition], arcs: List[Arc]) -> Tuple[List[Place], List[Transition], List[Arc]]:
    # Process places to remove those with no connected arcs
    places_to_remove = set()
    for place in places:
        if not any(arc.source == place or arc.target == place for arc in arcs):
            places_to_remove.add(place)
    new_places = [p for p in places if p not in places_to_remove]
    # Remove arcs connected to removed places
    arcs_after_places = [arc for arc in arcs if arc.source not in places_to_remove and arc.target not in places_to_remove]
    
    # Process transitions to remove those with less than two connected arcs
    transitions_to_remove = set()
    arcs_to_remove = set()
    for transition in transitions:
        connected_arcs = [arc for arc in arcs_after_places if arc.source == transition or arc.target == transition]
        if len(connected_arcs) < 2:
            transitions_to_remove.add(transition)
            arcs_to_remove.update(connected_arcs)
    new_transitions = [t for t in transitions if t not in transitions_to_remove]
    arcs_after_transitions = [arc for arc in arcs_after_places if arc not in arcs_to_remove]
    
    # Adjust transitions to have both incoming and outgoing arcs
    for transition in new_transitions:
        connected_arcs = [arc for arc in arcs_after_transitions if arc.source == transition or arc.target == transition]
        outgoing = sum(1 for arc in connected_arcs if arc.source == transition)
        incoming = sum(1 for arc in connected_arcs if arc.target == transition)
        
        if outgoing == 0 and incoming >= 1:
            # Flip one incoming arc to outgoing
            for arc in connected_arcs:
                if arc.target == transition:
                    arc.source, arc.target = arc.target, arc.source
                    break
        elif incoming == 0 and outgoing >= 1:
            # Flip one outgoing arc to incoming
            for arc in connected_arcs:
                if arc.source == transition:
                    arc.source, arc.target = arc.target, arc.source
                    break
    
    return new_places, new_transitions, arcs_after_transitions

def fix_petri_net(places: List[Place], transitions: List[Transition], arcs: List[Arc]) -> PetriModel:
    """Method that checks for all the errors in the petri net, logs the errors and applies fixes, if readily available."""
    ### Remove duplicate ids across places, transitions and arcs
    all_ids = []
    all_ids.extend(place.id for place in places)
    all_ids.extend(transition.id for transition in transitions)
    all_ids.extend(arc.id for arc in arcs)

    id_duplicates = [id for id, count in Counter(all_ids).items() if count > 1]

    for duplicate_id in id_duplicates:
        duplicate_elements = []
        duplicate_elements.extend([place for place in places if place.id == duplicate_id])
        duplicate_elements.extend([transition for transition in transitions if transition.id == duplicate_id])
        duplicate_elements.extend([arc for arc in arcs if arc.id == duplicate_id])
        print(f"Duplicate ID {duplicate_id} found in elements: {duplicate_elements}")

    ### Remove cycles, remove same type connections
    arcs = [arc for arc in arcs if type(arc.source) != type(arc.target)]
    ### Fix weights if any are less than 1
    for arc in arcs:
        if arc.weight < 1:
            print(f"Arc found with weight less than 1: {arc}")
            print("Applying fix to set the weight to 1")
            arc.weight = 1

    ### find arcs in arcs list, that have same source and the same target, and merge them into one arc, with the sum of the weights
    # Group arcs by their source and target
    arc_groups = defaultdict(list)
    for arc in arcs:  # Create a copy of the list to safely modify original
        key = (arc.source.id, arc.target.id)
        arc_groups[key].append(arc)

    # For each group of arcs with same source/target, merge them
    for (source_id, target_id), group in arc_groups.items():
        if len(group) > 1:
            print(f"Found {len(group)} parallel arcs between same source and target: {source_id} -> {target_id}")
            
            total_weight = sum(arc.weight for arc in group)
            
            merged_arc = group[0]
            merged_arc.weight = total_weight
            
            # Remove other arcs from the original list
            for arc in group[1:]:
                if arc in arcs:
                    arcs.remove(arc)


    ### There should be no hanging places, every place must have at least one arc
    ### Every transition must have at least one input and one output arc
    
    # places, transitions, arcs = sanitize_petri_net(places, transitions, arcs)
    places, transitions, arcs = process_elements(places, transitions, arcs)

    print(f"Places amount: {len(places)}")
    print(f"Transitions amount: {len(transitions)}")
    print(f"Arcs amount: {len(arcs)}")

    return PetriModel(places, transitions, arcs)