#!/usr/bin/env python3

import os
import json
import argparse
import re
import logging
import pandas as pd

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_compute_capability_dataframe():
    """
    Creates and returns a Pandas DataFrame mapping compute capabilities to GPU card names.
    """
    logging.debug("Creating compute capability to card name DataFrame...")
    data = []
    # Compute Capability 12.0
    cards_12_0 = [
        "NVIDIA RTX PRO 6000 Blackwell Workstation Edition", "NVIDIA RTX PRO 6000 Blackwell Max-Q Workstation Edition",
        "NVIDIA RTX PRO 5000 Blackwell", "NVIDIA RTX PRO 4500 Blackwell", "NVIDIA RTX PRO 4000 Blackwell",
        "GeForce RTX 5090", "GeForce RTX 5080", "GeForce RTX 5070 Ti", "GeForce RTX 5070",
        "GeForce RTX 5060 Ti", "GeForce RTX 5060", "NVIDIA RTX PRO 6000 Blackwell Server Edition"
    ]
    for card in cards_12_0: data.append({'compute_capability': 12.0, 'card_name': card})

    # Compute Capability 10.0
    cards_10_0 = ["NVIDIA GB200", "NVIDIA B200"]
    for card in cards_10_0: data.append({'compute_capability': 10.0, 'card_name': card})

    # Compute Capability 9.0
    cards_9_0 = ["NVIDIA GH200", "NVIDIA H200", "NVIDIA H100"]
    for card in cards_9_0: data.append({'compute_capability': 9.0, 'card_name': card})

    # Compute Capability 8.9
    cards_8_9 = [
        "NVIDIA RTX 6000 Ada", "NVIDIA RTX 5000 Ada", "NVIDIA RTX 4500 Ada", "NVIDIA RTX 4000 Ada",
        "NVIDIA RTX 4000 SFF Ada", "NVIDIA RTX 2000 Ada", "GeForce RTX 4090", "GeForce RTX 4080 SUPER",
        "GeForce RTX 4070 Ti", "GeForce RTX 4070", "GeForce RTX 4060 Ti", "GeForce RTX 4060",
        "GeForce RTX 4050", "NVIDIA L4", "NVIDIA L40"
    ]
    for card in cards_8_9: data.append({'compute_capability': 8.9, 'card_name': card})

    # Compute Capability 8.7
    cards_8_7 = ["Jetson AGX Orin", "Jetson Orin NX", "Jetson Orin Nano"]
    for card in cards_8_7: data.append({'compute_capability': 8.7, 'card_name': card})

    # Compute Capability 8.6
    cards_8_6 = [
        "NVIDIA RTX A6000", "NVIDIA RTX A5000", "NVIDIA RTX A4500", "NVIDIA RTX A4000", "NVIDIA RTX A2000",
        "GeForce RTX 3090 Ti", "GeForce RTX 3090", "GeForce RTX 3080 Ti", "GeForce RTX 3080",
        "GeForce RTX 3070 Ti", "GeForce RTX 3070", "GeForce RTX 3060 Ti", "GeForce RTX 3060",
        "GeForce RTX 3050 Ti", "GeForce RTX 3050", "NVIDIA A40", "NVIDIA A10", "NVIDIA A16", "NVIDIA A2"
    ]
    for card in cards_8_6: data.append({'compute_capability': 8.6, 'card_name': card})

    # Compute Capability 8.0
    cards_8_0 = ["NVIDIA A100", "NVIDIA A30"]
    for card in cards_8_0: data.append({'compute_capability': 8.0, 'card_name': card})

    # Compute Capability 7.5
    cards_7_5 = [
        "QUADRO RTX 8000", "QUADRO RTX 6000", "QUADRO RTX 5000", "QUADRO RTX 4000", "QUADRO RTX 3000",
        "QUADRO T2000", "NVIDIA T1200", "NVIDIA T1000", "NVIDIA T600", "NVIDIA T500", "NVIDIA T400",
        "GeForce GTX 1650 Ti", "NVIDIA TITAN RTX", "GeForce RTX 2080 Ti", "GeForce RTX 2080",
        "GeForce RTX 2070", "GeForce RTX 2060", "NVIDIA T4"
    ]
    for card in cards_7_5: data.append({'compute_capability': 7.5, 'card_name': card})

    cards_7_2 = ["Jetson AGX Xavier", "Jetson Xavier NX"]
    for card in cards_7_2: data.append({'compute_capability': 7.2, 'card_name': card})

    cards_7_0 = ["NVIDIA V100", "Quadro GV100", "NVIDIA TITAN V"]
    for card in cards_7_0: data.append({'compute_capability': 7.0, 'card_name': card})

    cards_6_2 = ["Jetson TX2"]
    for card in cards_6_2: data.append({'compute_capability': 6.2, 'card_name': card})

    cards_6_1 = [
        "Tesla P40", "Tesla P4", "Quadro P6000", "Quadro P5200", "Quadro P5000", "Quadro P4200",
        "Quadro P4000", "Quadro P3200", "Quadro P3000", "Quadro P2200", "Quadro P2000", "Quadro P1000",
        "Quadro P620", "Quadro P600", "Quadro P500", "Quadro P400", "P620", "P520", "NVIDIA TITAN Xp",
        "NVIDIA TITAN X", "GeForce GTX 1080 Ti", "GeForce GTX 1080", "GeForce GTX 1070 Ti",
        "GeForce GTX 1070", "GeForce GTX 1060", "GeForce GTX 1050"  
    ]
    for card in cards_6_1: data.append({'compute_capability': 6.1, 'card_name': card})
    
    df = pd.DataFrame(data)
    logging.debug(f"Compute capability DataFrame created with {len(df)} entries.")
    return df

def sm_to_compute_capability(sm_string):
    """
    Converts an 'sm_xx' string (e.g., "sm_75", "sm_90a") to its numeric compute capability.
    Returns None if invalid, or if the capability is > 9.0.
    "sm_90a" maps to 9.0.
    "sm_XX" (e.g. "sm_37") maps to X.Y (e.g. 3.7).
    "sm_XYZ" (e.g. "sm_100") maps to XY.Z (e.g. 10.0), then checks if > 9.0.
    """
    if not isinstance(sm_string, str):
        return None
    
    sm_string_lower = sm_string.strip().lower()

    if sm_string_lower == "sm_90a":
        cc_value = 9.0
    else:
        match = re.match(r"sm_(\d+)", sm_string_lower)
        if not match:
            logging.debug(f"Invalid sm string format: {sm_string}")
            return None
        
        numeric_part_str = match.group(1)
        try:
            if not numeric_part_str: # Should not happen with \d+
                return None
            if len(numeric_part_str) == 1: # e.g., "7" for sm_7 -> 0.7
                cc_value = float(f"0.{numeric_part_str}")
            else: # e.g., "37" -> 3.7, "50" -> 5.0, "120" -> 12.0
                cc_value = float(f"{numeric_part_str[:-1]}.{numeric_part_str[-1]}")
        except ValueError:
            logging.warning(f"Cannot convert numeric part '{numeric_part_str}' of sm string '{sm_string}' to float.")
            return None        
    return cc_value

def discover_pytorch_versions(cache_dir):
    if not os.path.isdir(cache_dir):
        logging.error(f"Cache directory '{cache_dir}' not found for version discovery.")
        return []
    version_extractor_pattern = re.compile(r"^pytorch-([^-]+)-py\d+(\.\d+)*_.*")
    discovered_versions = set()
    logging.info(f"Discovering PyTorch versions in '{cache_dir}'...")
    for item_name in os.listdir(cache_dir):
        item_path = os.path.join(cache_dir, item_name)
        if os.path.isdir(item_path):
            match = version_extractor_pattern.match(item_name)
            if match:
                version = match.group(1)
                discovered_versions.add(version)
                logging.debug(f"  Found potential PyTorch folder: {item_name}, extracted version: {version}")
    if not discovered_versions:
        logging.warning(f"No PyTorch version folders matching the pattern found in '{cache_dir}'.")
        return []
    sorted_versions = sorted(list(discovered_versions))
    logging.info(f"Discovered PyTorch versions: {sorted_versions}")
    return sorted_versions

def collect_architectures_for_specific_version(pytorch_version, cache_dir):
    if not os.path.isdir(cache_dir):
        logging.error(f"Cache directory '{cache_dir}' not found while collecting for version {pytorch_version}.")
        return []
    folder_pattern = re.compile(rf"^pytorch-{re.escape(pytorch_version)}-py\d+(\.\d+)*_.*")
    all_architectures_for_this_version = set()
    logging.debug(f"Scanning '{cache_dir}' for specific PyTorch version '{pytorch_version}'...")
    for item_name in os.listdir(cache_dir):
        item_path = os.path.join(cache_dir, item_name)
        if os.path.isdir(item_path) and folder_pattern.match(item_name):
            logging.debug(f"  Processing matching folder for version {pytorch_version}: {item_name}")
            summary_file_path = os.path.join(item_path, "summary.json")
            if not os.path.isfile(summary_file_path):
                logging.warning(f"    'summary.json' not found in '{item_path}'. Skipping.")
                continue
            try:
                with open(summary_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                architectures_string = data.get("architectures")
                if architectures_string is None:
                    logging.warning(f"    'architectures' key not found in '{summary_file_path}'. Skipping.")
                    continue
                if not isinstance(architectures_string, str):
                    logging.warning(f"    'architectures' in '{summary_file_path}' is not a string (type: {type(architectures_string)}). Expected comma-separated. Skipping.")
                    continue
                parsed_architectures = [arch.strip() for arch in architectures_string.split(',') if arch.strip()]
                if parsed_architectures:
                    all_architectures_for_this_version.update(parsed_architectures)
                    logging.debug(f"    Found sm_architectures from string: {set(parsed_architectures)}")
            except json.JSONDecodeError: logging.error(f"    Error decoding JSON from '{summary_file_path}'. Skipping.")
            except Exception as e: logging.error(f"    An unexpected error occurred processing '{summary_file_path}': {e}. Skipping.")
    return sorted(list(all_architectures_for_this_version))

def get_compatible_cards(sm_architectures_list, cc_dataframe):
    """
    Finds compatible GPU cards for a list of sm_architectures.
    """
    all_compatible_cards = set()
    if not sm_architectures_list:
        return []

    logging.debug(f"  Looking up cards for sm_architectures: {sm_architectures_list}")
    for sm_arch_str in sm_architectures_list:
        cc_val = sm_to_compute_capability(sm_arch_str)
        if cc_val is not None:
            # Pandas DataFrame filtering. Using a small tolerance for float comparison might be robust,
            # but direct equality should work if cc_val is clean.
            # Let's assume direct equality is fine for now, as our cc_val generation is specific.
            matching_cards_df = cc_dataframe[cc_dataframe['compute_capability'] == cc_val]
            if not matching_cards_df.empty:
                cards_found = matching_cards_df['card_name'].tolist()
                logging.debug(f"    For {sm_arch_str} (CC {cc_val:.1f}), found cards: {cards_found}")
                all_compatible_cards.update(cards_found)
            else:
                logging.debug(f"    For {sm_arch_str} (CC {cc_val:.1f}), no matching cards found in DataFrame.")
        # If cc_val is None, it means sm_arch_str was ignored (e.g. >9.0) or invalid.
        # sm_to_compute_capability already logs this at debug level.
            
    return sorted(list(all_compatible_cards))

def main():
    parser = argparse.ArgumentParser(
        description="Discovers PyTorch versions, collects their SM architectures and compatible GPU cards, and saves to JSON files.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--cache-dir", type=str, default="cache", help="Path to the cache directory (default: './cache').")
    parser.add_argument("--output-dir", type=str, default=".", help="Directory for output JSON files (default: './').")
    parser.add_argument("--arch-output-filename", type=str, default="all_pytorch_architectures.json", help="Output filename for SM architectures JSON (default: 'all_pytorch_architectures.json').")
    parser.add_argument("--cards-output-filename", type=str, default="all_pytorch_compatible_cards.json", help="Output filename for compatible cards JSON (default: 'all_pytorch_compatible_cards.json').")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging (DEBUG level).")

    args = parser.parse_args()

    if args.verbose: logging.getLogger().setLevel(logging.DEBUG)
    else: logging.getLogger().setLevel(logging.INFO)

    logging.info("Starting PyTorch architecture and compatible card collection process.")
    logging.info(f"Using cache directory: {os.path.abspath(args.cache_dir)}")
    logging.info(f"Output directory: {os.path.abspath(args.output_dir)}")

    # Create the GPU card DataFrame
    cc_card_df = get_compute_capability_dataframe()

    pytorch_versions = discover_pytorch_versions(args.cache_dir)
    if not pytorch_versions:
        logging.info("No PyTorch versions discovered. Exiting.")
        return

    consolidated_sm_architectures = {}
    consolidated_compatible_cards = {}

    for version in pytorch_versions:
        logging.info(f"Processing PyTorch version: {version}")
        
        # 1. Collect SM architectures
        sm_architectures = collect_architectures_for_specific_version(version, args.cache_dir)
        consolidated_sm_architectures[version] = sm_architectures
        if sm_architectures:
            logging.info(f"  Collected SM architectures for {version}: {sm_architectures}")
        else:
            logging.info(f"  No SM architectures found/extracted for PyTorch version {version}.")

        # 2. Find compatible cards based on these SM architectures
        compatible_cards = get_compatible_cards(sm_architectures, cc_card_df)
        consolidated_compatible_cards[version] = compatible_cards
        if compatible_cards:
            logging.info(f"  Found compatible cards for {version}: {len(compatible_cards)} unique cards.")
            logging.debug(f"  Card list for {version}: {compatible_cards}")
        else:
            logging.info(f"  No compatible cards found for PyTorch version {version} (based on collected SM archs and CC <= 9.0).")

    # Ensure output directory exists
    try:
        os.makedirs(args.output_dir, exist_ok=True)
    except OSError as e:
        logging.error(f"Could not create output directory '{args.output_dir}': {e}. Outputs will be attempted in current directory.")
        # If output_dir fails, subsequent os.path.join might use a relative path from current dir.
    
    # Save SM architectures JSON
    arch_output_filepath = os.path.join(args.output_dir, args.arch_output_filename)
    try:
        with open(arch_output_filepath, 'w', encoding='utf-8') as outfile:
            json.dump(consolidated_sm_architectures, outfile, indent=4)
        logging.info(f"Successfully wrote SM architectures to: {os.path.abspath(arch_output_filepath)}")
    except IOError as e: logging.error(f"Error writing SM architectures file '{arch_output_filepath}': {e}")
    except Exception as e: logging.error(f"Unexpected error writing SM architectures file: {e}")

    # Save compatible cards JSON
    cards_output_filepath = os.path.join(args.output_dir, args.cards_output_filename)
    try:
        with open(cards_output_filepath, 'w', encoding='utf-8') as outfile:
            json.dump(consolidated_compatible_cards, outfile, indent=4)
        logging.info(f"Successfully wrote compatible cards to: {os.path.abspath(cards_output_filepath)}")
    except IOError as e: logging.error(f"Error writing compatible cards file '{cards_output_filepath}': {e}")
    except Exception as e: logging.error(f"Unexpected error writing compatible cards file: {e}")

    # Release date mapping from your table
    pytorch_release_dates = {
        "2.7.0": "04/23/2025",
        "2.6.0": "01/30/2025", 
        "2.5.0": "10/17/2024",
        "2.4.0": "07/24/2024",
        "2.3.0": "04/24/2024",
        "2.2.0": "01/30/2024",
        "2.1.0": "10/04/2023",
        "2.0.0": "03/15/2023",
        "1.13.0": "10/28/2022",
        "1.12.0": "06/28/2022",
        "1.11.0": "02/10/2022",
        "1.10.1": "12/15/2021",
        "1.10.0": "10/21/2021",
        "1.9.1": "09/21/2021",
        "1.9.0": "06/15/2021",
        "1.8.1": "03/25/2021",
        "1.8.0": "03/04/2021",
        "1.7.1": "12/10/2020",
        "1.7.0": "10/27/2020",
        "1.6.0": "07/28/2020",
        "1.5.1": "06/18/2020",
        "1.5.0": "04/21/2020",
        "1.4.0": "01/15/2020",
        "1.3.1": "11/07/2019",
        "1.3.0": "10/22/2019",
        "1.2.0": "08/08/2019",
        "1.1.0": "04/30/2019",
        "1.0.0": "12/07/2018",
        "0.4.1": "07/26/2018",
        "0.4.0": "04/24/2018",
        "0.3.1": "04/03/2018",
        "0.3.0": "01/25/2018"
    }

    # Load your existing JSON file
    with open('all_pytorch_compatible_cards.json', 'r') as f:
        pytorch_cards = json.load(f)

    # Add release dates to matching versions
    for version, cards in pytorch_cards.items():
        if version in pytorch_release_dates:
            # Convert to a dictionary format that includes both architectures and release date
            pytorch_cards[version] = {
                "cards": cards,
                "release_date": pytorch_release_dates[version]
            }

    # Save the updated JSON file
    with open('all_pytorch_compatible_cards.json', 'w') as f:
        json.dump(pytorch_cards, f, indent=2)

    print(f"Updated {len([v for v in pytorch_cards.keys() if v in pytorch_release_dates])} versions with release dates")

if __name__ == "__main__":
    main()
