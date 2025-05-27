import pandas as pd

# Create the compute capability data
data = []

# Compute Capability 12.0
cards_12_0 = [
    "NVIDIA RTX PRO 6000 Blackwell Workstation Edition",
    "NVIDIA RTX PRO 6000 Blackwell Max-Q Workstation Edition",
    "NVIDIA RTX PRO 5000 Blackwell",
    "NVIDIA RTX PRO 4500 Blackwell",
    "NVIDIA RTX PRO 4000 Blackwell",
    "GeForce RTX 5090",
    "GeForce RTX 5080",
    "GeForce RTX 5070 Ti",
    "GeForce RTX 5070",
    "GeForce RTX 5060 Ti",
    "GeForce RTX 5060",
    "NVIDIA RTX PRO 6000 Blackwell Server Edition"
]
for card in cards_12_0:
    data.append({'compute_capability': 12.0, 'card_name': card})

# Compute Capability 10.0
cards_10_0 = [
    "NVIDIA GB200",
    "NVIDIA B200"
]
for card in cards_10_0:
    data.append({'compute_capability': 10.0, 'card_name': card})

# Compute Capability 9.0
cards_9_0 = [
    "NVIDIA GH200",
    "NVIDIA H200",
    "NVIDIA H100"
]
for card in cards_9_0:
    data.append({'compute_capability': 9.0, 'card_name': card})

# Compute Capability 8.9
cards_8_9 = [
    "NVIDIA RTX 6000 Ada",
    "NVIDIA RTX 5000 Ada",
    "NVIDIA RTX 4500 Ada",
    "NVIDIA RTX 4000 Ada",
    "NVIDIA RTX 4000 SFF Ada",
    "NVIDIA RTX 2000 Ada",
    "GeForce RTX 4090",
    "GeForce RTX 4080 SUPER",
    "GeForce RTX 4070 Ti",
    "GeForce RTX 4070",
    "GeForce RTX 4060 Ti",
    "GeForce RTX 4060",
    "GeForce RTX 4050",
    "NVIDIA L4",
    "NVIDIA L40"
]
for card in cards_8_9:
    data.append({'compute_capability': 8.9, 'card_name': card})

# Compute Capability 8.7
cards_8_7 = [
    "Jetson AGX Orin",
    "Jetson Orin NX",
    "Jetson Orin Nano"
]
for card in cards_8_7:
    data.append({'compute_capability': 8.7, 'card_name': card})

# Compute Capability 8.6
cards_8_6 = [
    "NVIDIA RTX A6000",
    "NVIDIA RTX A5000",
    "NVIDIA RTX A4500",
    "NVIDIA RTX A4000",
    "NVIDIA RTX A2000",
    "GeForce RTX 3090 Ti",
    "GeForce RTX 3090",
    "GeForce RTX 3080 Ti",
    "GeForce RTX 3080",
    "GeForce RTX 3070 Ti",
    "GeForce RTX 3070",
    "GeForce RTX 3060 Ti",
    "GeForce RTX 3060",
    "GeForce RTX 3050 Ti",
    "GeForce RTX 3050",
    "NVIDIA A40",
    "NVIDIA A10",
    "NVIDIA A16",
    "NVIDIA A2"
]
for card in cards_8_6:
    data.append({'compute_capability': 8.6, 'card_name': card})

# Compute Capability 8.0
cards_8_0 = [
    "NVIDIA A100",
    "NVIDIA A30"
]
for card in cards_8_0:
    data.append({'compute_capability': 8.0, 'card_name': card})

# Compute Capability 7.5
cards_7_5 = [
    "QUADRO RTX 8000",
    "QUADRO RTX 6000",
    "QUADRO RTX 5000",
    "QUADRO RTX 4000",
    "QUADRO RTX 3000",
    "QUADRO T2000",
    "NVIDIA T1200",
    "NVIDIA T1000",
    "NVIDIA T600",
    "NVIDIA T500",
    "NVIDIA T400",
    "GeForce GTX 1650 Ti",
    "NVIDIA TITAN RTX",
    "GeForce RTX 2080 Ti",
    "GeForce RTX 2080",
    "GeForce RTX 2070",
    "GeForce RTX 2060",
    "NVIDIA T4"
]
for card in cards_7_5:
    data.append({'compute_capability': 7.5, 'card_name': card})

# Create DataFrame
computeCapabilityCardList = pd.DataFrame(data)

# Display the DataFrame
print(f"Total entries: {len(computeCapabilityCardList)}")
print("\nFirst 10 rows:")
print(computeCapabilityCardList.head(10))

print("\nCompute capabilities available:")
print(sorted(computeCapabilityCardList['compute_capability'].unique()))

print("\nCount of cards per compute capability:")
print(computeCapabilityCardList['compute_capability'].value_counts().sort_index())