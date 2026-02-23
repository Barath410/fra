import json
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

# =============================
# Label schema (base labels)
# =============================

BASE_LABELS: List[str] = [
    # Shared / common
    "CLAIMANT_NAME",
    "SPOUSE_NAME",
    "FATHER_MOTHER_NAME",
    "FAMILY_MEMBER_NAME",
    "FAMILY_MEMBER_AGE",
    "DEPENDENT_NAME",
    "TITLE_HOLDER_NAME",
    "COMMUNITY_RIGHT_HOLDER_NAME",
    "GRAM_SABHA_MEMBER_NAME",
    "ADDRESS_FULL",
    "VILLAGE",
    "GRAM_PANCHAYAT",
    "GRAM_SABHA",
    "TEHSIL_TALUKA",
    "DISTRICT",
    "STATE",
    "KHASRA_COMPARTMENT_NUMBER",
    "CATEGORY_SCHEDULED_TRIBE",
    "CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER",
    "LAND_AREA_MEASURE",
    "BOUNDARY_DESCRIPTION",
    "CUSTOMARY_BOUNDARY",
    "COMMUNITY_TYPE_FDST",
    "COMMUNITY_TYPE_OTFD",
    "COMMUNITY_TYPE_SCHEDULED_TRIBE",
    "COMMUNITY_TYPE_OTHER_TFD",
    "COMMUNITY_TYPE_BOTH",
    "EVIDENCE_ITEM",
    "OTHER_TRADITIONAL_RIGHT",
    "OTHER_INFORMATION",
    # Claim Form Type 1 – claim for rights to forest land
    "LAND_EXTENT_HABITATION",
    "LAND_EXTENT_SELF_CULTIVATION",
    "DISPUTED_LAND_DESCRIPTION",
    "EXISTING_PATTAS_LEASES_GRANTS",
    "REHABILITATION_LAND",
    "DISPLACED_FROM_LAND",
    "LAND_EXTENT_FOREST_VILLAGE",
    # Claim Form Type 2 – claim for community rights
    "COMMUNITY_RIGHT_NISTAR",
    "RIGHT_MINOR_FOREST_PRODUCE",
    "COMMUNITY_RIGHT_RESOURCE_USE",
    "COMMUNITY_RIGHT_GRAZING",
    "COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS",
    "COMMUNITY_TENURE_HABITAT",
    "COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK",
    # Claim Form Type 3 – community forest resource
    "BORDERING_VILLAGE",
    "COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST",
    # Title Form Type 1 – individual title
    "TITLE_ADDRESS_FULL",
    "TITLE_LAND_AREA_MEASURE",
    # Title Form Type 2 – community forest rights title
    "COMMUNITY_RIGHT_NATURE",
    "TITLE_CONDITIONS",
]


def build_bio_labels(base_labels: List[str]) -> List[str]:
    labels = ["O"]
    for base in base_labels:
        labels.append(f"B-{base}")
        labels.append(f"I-{base}")
    return labels


LABEL_LIST: List[str] = build_bio_labels(BASE_LABELS)
LABEL2ID: Dict[str, int] = {label: i for i, label in enumerate(LABEL_LIST)}


def bio_ids(base_label: str) -> Tuple[int, int]:
    """Return (B-id, I-id) for a base label."""
    b = LABEL2ID[f"B-{base_label}"]
    i = LABEL2ID[f"I-{base_label}"]
    return b, i


# Map template slot placeholders to base labels
SLOT2LABEL: Dict[str, str] = {
    # Names
    "CLAIMANT_NAME": "CLAIMANT_NAME",
    "SPOUSE_NAME": "SPOUSE_NAME",
    "FATHER_MOTHER_NAME": "FATHER_MOTHER_NAME",
    "FAMILY_MEMBER_NAME": "FAMILY_MEMBER_NAME",
    "FAMILY_MEMBER_AGE": "FAMILY_MEMBER_AGE",
    "DEPENDENT_NAME": "DEPENDENT_NAME",
    "TITLE_HOLDER_NAME": "TITLE_HOLDER_NAME",
    "COMMUNITY_RIGHT_HOLDER_NAME": "COMMUNITY_RIGHT_HOLDER_NAME",
    "GRAM_SABHA_MEMBER_NAME": "GRAM_SABHA_MEMBER_NAME",
    # Locations / address
    "ADDRESS_FULL": "ADDRESS_FULL",
    "TITLE_ADDRESS_FULL": "TITLE_ADDRESS_FULL",
    "VILLAGE": "VILLAGE",
    "GRAM_PANCHAYAT": "GRAM_PANCHAYAT",
    "GRAM_SABHA": "GRAM_SABHA",
    "TEHSIL_TALUKA": "TEHSIL_TALUKA",
    "DISTRICT": "DISTRICT",
    "STATE": "STATE",
    "KHASRA_COMPARTMENT_NUMBER": "KHASRA_COMPARTMENT_NUMBER",
    # Categories / communities
    "CATEGORY_SCHEDULED_TRIBE": "CATEGORY_SCHEDULED_TRIBE",
    "CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER": "CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER",
    "COMMUNITY_TYPE_FDST": "COMMUNITY_TYPE_FDST",
    "COMMUNITY_TYPE_OTFD": "COMMUNITY_TYPE_OTFD",
    "COMMUNITY_TYPE_SCHEDULED_TRIBE": "COMMUNITY_TYPE_SCHEDULED_TRIBE",
    "COMMUNITY_TYPE_OTHER_TFD": "COMMUNITY_TYPE_OTHER_TFD",
    "COMMUNITY_TYPE_BOTH": "COMMUNITY_TYPE_BOTH",
    # Land and boundaries
    "LAND_AREA_MEASURE": "LAND_AREA_MEASURE",
    "TITLE_LAND_AREA_MEASURE": "TITLE_LAND_AREA_MEASURE",
    "BOUNDARY_DESCRIPTION": "BOUNDARY_DESCRIPTION",
    "CUSTOMARY_BOUNDARY": "CUSTOMARY_BOUNDARY",
    "LAND_EXTENT_HABITATION": "LAND_EXTENT_HABITATION",
    "LAND_EXTENT_SELF_CULTIVATION": "LAND_EXTENT_SELF_CULTIVATION",
    "DISPUTED_LAND_DESCRIPTION": "DISPUTED_LAND_DESCRIPTION",
    "EXISTING_PATTAS_LEASES_GRANTS": "EXISTING_PATTAS_LEASES_GRANTS",
    "REHABILITATION_LAND": "REHABILITATION_LAND",
    "DISPLACED_FROM_LAND": "DISPLACED_FROM_LAND",
    "LAND_EXTENT_FOREST_VILLAGE": "LAND_EXTENT_FOREST_VILLAGE",
    # Community rights
    "COMMUNITY_RIGHT_NISTAR": "COMMUNITY_RIGHT_NISTAR",
    "RIGHT_MINOR_FOREST_PRODUCE": "RIGHT_MINOR_FOREST_PRODUCE",
    "COMMUNITY_RIGHT_RESOURCE_USE": "COMMUNITY_RIGHT_RESOURCE_USE",
    "COMMUNITY_RIGHT_GRAZING": "COMMUNITY_RIGHT_GRAZING",
    "COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS": "COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS",
    "COMMUNITY_TENURE_HABITAT": "COMMUNITY_TENURE_HABITAT",
    "COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK": "COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK",
    # Other / evidence
    "BORDERING_VILLAGE": "BORDERING_VILLAGE",
    "COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST": "COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST",
    "COMMUNITY_RIGHT_NATURE": "COMMUNITY_RIGHT_NATURE",
    "TITLE_CONDITIONS": "TITLE_CONDITIONS",
    "EVIDENCE_ITEM": "EVIDENCE_ITEM",
    "OTHER_TRADITIONAL_RIGHT": "OTHER_TRADITIONAL_RIGHT",
    "OTHER_INFORMATION": "OTHER_INFORMATION",
}


# =============================
# Simple synthetic value pools
# (You can extend these lists as needed.)
# =============================

RNG = random.Random(42)


# 1. Names (Claimants, Fathers, Spouses, Dependents)
import random
from typing import Dict, List

RNG = random.Random(42)

# =============================
# UPGRADED SYNTHETIC VALUE POOLS (ALL 5 LANGUAGES)
# =============================

# 1. Names - Massively expanded to prevent model memorization
NAME_POOLS: Dict[str, List[str]] = {
    "hi": [
        "राम कुमार", "सीमा देवी", "अनिल यादव", "गीता सिंह", "सुखराम गौंड", "पार्वती बाई", 
        "लक्ष्मण सिंह", "कमला उइके", "मुकेश भूरिया", "शांति देवी", "रमेश चंद्र", "सुनीता",
        "दिनेश धुर्वे", "मीना कुमारी", "प्रकाश मुंडा", "रेखा", "संतोष प्रधान", "अनीता",
        "राजेश कुमार", "ममता", "शिवराज", "कुसुम देवी", "वीरेंद्र", "संगीता", "मंगल सिंह"
    ],
    "ta": [
        "ராமன்", "லட்சுமி", "குமார்", "சீதா", "முத்துவேல்", "செல்வி", "கந்தசாமி", "பார்வதி", 
        "அருண் குமார்", "மீனா", "சின்னசாமி", "கருப்பண்ணன்", "வேலு", "பழனி", "மாரியம்மாள்", 
        "கிருஷ்ணன்", "ராதா", "சுப்பிரமணி", "கமலா", "ராஜேந்திரன்", "சரஸ்வதி", "தங்கவேல்", 
        "முனியம்மா", "வீராசாமி", "காமாட்சி", "பெரியசாமி", "வள்ளி", "அய்யாக்கண்ணு", "பூங்கொடி"
    ],
    "te": [
        "రామయ్య", "లక్ష్మి", "కుమార్", "సీత", "వెంకటేశ్వర్లు", "సరోజ", "కోటేశ్వరరావు", 
        "వరలక్ష్మి", "శ్రీనివాస్", "అంజమ్మ", "రామారావు", "భవాని", "శివయ్య", "నాగమణి",
        "కృష్ణయ్య", "రమణమ్మ", "వీరభద్రయ్య", "పద్మావతి", "సత్యనారాయణ", "కళావతి", "నర్సింహ",
        "సుశీల", "అప్పారావు", "గౌరమ్మ", "శంకర్"
    ],
    "bn": [
        "রাম দাস", "সীমা দত্ত", "অনীল ঘোষ", "গীতা সরকার", "সুখদেব সর্দার", "পার্বতী মুর্মু", 
        "লক্ষ্মণ টুডু", "মঙ্গলী কিস্কু", "রতন হেমব্রম", "শান্তি সোরেন", "বিকাশ মাহাতো", "অঞ্জলি",
        "দীপক বাউড়ি", "লতিকা", "সুকুমার রায়", "মিনতি", "প্রশান্ত প্রামাণিক", "সুজাতা",
        "নিমাই সর্দার", "বাসন্তী", "তপন মুন্ডা", "প্রতিমা", "শ্যামল", "শিখা", "জগন্নাথ"
    ],
    "or": [
        "ରାମ ନାୟକ", "ସୀମା ଦାସ", "ଅନିଲ ପଟ୍ଟନାୟକ", "ଗୀତା ସ୍ୱାଇଁ", "ଦୁଖୁ ମାଝୀ", "ପଦ୍ମିନୀ ମାଝୀ", 
        "ଲବକାନ୍ତ ଶବର", "ଶାନ୍ତିଲତା ମୁଣ୍ଡା", "ସୁଦର୍ଶନ କିଷାନ", "କମଳା ଜାନି", "ରମେଶ ପ୍ରଧାନ", "ସୁମିତ୍ରା",
        "ପ୍ରକାଶ ଭୋଇ", "ମମତା", "ବିରେନ୍ଦ୍ର ବେହେରା", "ସୁନୀତା", "ଅଶୋକ ନାଏକ", "ରେଖା",
        "ଜଗବନ୍ଧୁ ଗୌଡ", "ଅଞ୍ଜଳି", "କୃଷ୍ଣଚନ୍ଦ୍ର", "ସରସ୍ୱତୀ", "ଭଗବାନ", "ନମିତା", "ଗୋପିନାଥ"
    ]
}

# 2. Geography (Villages)
VILLAGE_POOLS: Dict[str, List[str]] = {
    "hi": ["वनपुर", "हरिटोला", "बैरह", "जामपानी", "टिकरिया", "खमारपाणी", "सीतापुर", "रामनगर", "नयागाँव", "पीपलखेड़ा", "मालपुर", "अंबाटोला"],
    "ta": ["மருதூர்", "காடுகுளம்", "கொட்டப்பட்டி", "மலைகிராமம்", "ஆனைக்கட்டி", "சின்னம்பதி", "பழங்குடிவாடி", "கீழ்க்காடு", "மேலமலை", "தேனூத்து", "சருகுபாறை", "புலியூர்"],
    "te": ["అరణ్యపురం", "గిరిజనపల్లి", "కొత్తపల్లి", "చింతూరు", "భద్రాద్రి", "మంగంపేట", "రామాపురం", "సీతానగరం", "అటవీపాలెం", "కొండపల్లి", "చిన్నూరు", "పెద్దపాడు"],
    "bn": ["বনপুর", "পাহাড়তলী", "শালবনি", "খোয়াঁই", "জামবনি", "বেলপাহাড়ি", "নতুনগ্রাম", "শান্তিপুর", "শ্যামপুর", "রামচন্দ্রপুর", "জঙ্গলমহল", "রাধাপুর"],
    "or": ["ଅରଣ୍ୟପୁର", "ପାହାଡିଆ", "ଝରାବାହାଲି", "ହେରମଲ", "କାଶୀପୁର", "ବିଷମକଟକ", "ରାମପୁର", "ନୂଆଗାଁ", "ଶାନ୍ତିପୁର", "ମାଳିଗୁଡା", "ଟିକିରି", "ଲକ୍ଷ୍ମୀପୁର"]
}

# 3. Geography (Districts)
DISTRICT_POOLS: Dict[str, List[str]] = {
    "hi": ["धार", "गोंडिया", "बालाघाट", "बेतूल", "मंडला", "डिंडोरी", "छिंदवाड़ा", "झाबुआ", "अलीराजपुर", "बस्तर", "दंतेवाड़ा", "सुकमा"],
    "ta": ["திண்டுக்கல்", "விழுப்புரம்", "தர்மபுரி", "கோயம்புத்தூர்", "நீலகிரி", "ஈரோடு", "கிருஷ்ணகிரி", "சேலம்", "திருப்பத்தூர்", "திருவண்ணாமலை", "கள்ளக்குறிச்சி", "தேனி"],
    "te": ["ఆదిలాబాదు", "ఖమ్మం", "భద్రాద్రి కొత్తగూడెం", "ములుగు", "మహబూబాబాద్", "ఆసిఫాబాద్", "వరంగల్", "నిజామాబాద్", "శ్రీకాకుళం", "విశాఖపట్నం", "విజయనగరం", "తూర్పు గోదావరి"],
    "bn": ["পুরুলিয়া", "বাঁকুড়া", "ঝাড়গ্রাম", "পশ্চিম মেদিনীপুর", "আলিপুরদুয়ার", "জলপাইগুড়ি", "দার্জিলিং", "কালিম্পং", "বীরভূম", "দক্ষিণ চব্বিশ পরগনা"],
    "or": ["କଳାହାଣ୍ଡି", "ମୟୂରଭଞ୍ଜ", "ସୁନ୍ଦରଗଡ଼", "କୋରାପୁଟ", "ରାୟଗଡ଼ା", "କନ୍ଧମାଳ", "ଗଜପତି", "ମାଲକାନଗିରି", "ନବରଙ୍ଗପୁର", "କେନ୍ଦୁଝର", "ବଲାଙ୍ଗୀର", "ସମ୍ବଲପୁର"]
}

# 4. State
STATE_POOLS: Dict[str, List[str]] = {
    "hi": ["मध्य प्रदेश", "छत्तीसगढ़", "महाराष्ट्र"],
    "ta": ["தமிழ்நாடு", "கேரளா", "ஆந்திரப் பிரதேசம்"],
    "te": ["తెలంగాణ", "ఆంధ్ర ప్రదేశ్"],
    "bn": ["ত্রিপুরা", "পশ্চিমবঙ্গ", "আসাম"],
    "or": ["ଓଡ଼ିଶା"]
}

# 4.5 Tehsils
TEHSIL_POOLS: Dict[str, List[str]] = {
    "hi": ["तहसील वनखण्ड", "तहसील आदिवासीपुर", "तहसील शाहपुर", "मुलताई तहसील", "भैंसदेही तहसील", "बजाग तहसील", "करंजिया तहसील", "कुसमी तहसील"],
    "ta": ["தாலுகா காட்டூர்", "தாலுகா மலையூர்", "குன்னூர் தாலுகா", "அரூர் தாலுகா", "உடுமலைப்பேட்டை தாலுகா", "பவானி தாலுகா", "சத்தியமங்கலம் தாலுகா", "ஏற்காடு தாலுகா"],
    "te": ["తాలూకా అడవిపేట", "తాలూకా గిరిజనవాడ", "భద్రాచలం తాలూకా", "పాల్వంచ తాలూకా", "పాడేరు తాలూకా", "అరకు తాలూకా", "చింతపల్లి తాలూకా", "రంపచోడవరం తాలూకా"],
    "bn": ["তহসিল জঙ্গলপুর", "তহসিল পাহাড়পুর", "খাতড়া ব্লক", "রানীবাঁধ ব্লক", "বান্দোয়ান ব্লক", "বিনপুর ব্লক", "কুমারগ্রাম ব্লক", "কালচিনি ব্লক"],
    "or": ["ତହସିଲ ଜଙ୍ଗଲପଡା", "ତହସିଲ ପାହାଡପୁର", "ଗୁଣପୁର ତହସିଲ", "ଥୁଆମୂଳ ରାମପୁର ତହସିଲ", "ଲାଞ୍ଜିଗଡ଼ ତହସିଲ", "କୋଟପାଡ଼ ତହସିଲ", "ଜୟପୁର ତହସିଲ", "ଉଦଳା ତହସିଲ"]
}

# 5. Land Records (Khasra/Compartment) - Added varied formats
KHASRA_POOL: Dict[str, List[str]] = {
    "hi": ["खसरा 12/3", "कंपार्टमेंट 45A", "खसरा 78/1", "प्लॉट नं 402", "आरक्षित वन खण्ड 14", "खसरा नंबर 99/2B", "सर्वे 105", "कम्पार्टमेंट C-12", "भूमि क्र. 55", "खसरा 8"],
    "ta": ["கசரா 12/3", "கம்பார்ட்மென்ட் 45A", "கசரா 78/1", "சர்வே எண் 402", "பிரிவு 14", "கசரா 99/2B", "சர்வே எண் 105", "கம்பார்ட்மென்ட் C-12", "நில அளவை எண் 55", "கசரா 8"],
    "te": ["ఖస్రా 12/3", "కంపార్ట్‌మెంట్ 45A", "ఖస్రా 78/1", "సర్వే నంబర్ 402", "కంపార్ట్‌మెంట్ 14", "ఖస్రా నంబర్ 99/2B", "సర్వే 105", "కంపార్ట్‌మెంట్ C-12", "భూమి నంబర్ 55", "ఖస్రా 8"],
    "bn": ["খতিয়ান ১২/৩", "কম্পার্টমেন্ট ৪৫A", "প্লট নং ৪০২", "খতিয়ান ৭৮/১", "সংরক্ষিত ব্লক ১৪", "খতিয়ান ৯৯/২B", "সার্ভে নং ১০৫", "কম্পার্টমেন্ট C-12", "দাগ নং ৫৫", "প্লট ৮"],
    "or": ["ଖାତା ନଂ ୪୫, ପ୍ଲଟ ନଂ ୧୨/୩", "କମ୍ପାର୍ଟମେଣ୍ଟ ୪୫A", "ଖସଡା ୭୮/୧", "ସର୍ଭେ ନମ୍ବର ୪୦୨", "ବ୍ଲକ ନଂ ୧୪", "ଖସଡା ୯୯/୨B", "ସର୍ଭେ ୧୦୫", "କମ୍ପାର୍ଟମେଣ୍ଟ C-12", "ଜମି ନଂ ୫୫", "ଖାତା ନଂ ୮"]
}

# 6. Minor Forest Produce (MFP)
MINOR_FOREST_PRODUCE: Dict[str, List[str]] = {
    "hi": ["तेन्दू पत्ता", "महुआ फूल", "चिरौंजी", "सबई घास", "शहद", "गोंद", "इमली"],
    "ta": ["தேந்து இலை", "மகுவா மலர்", "காட்டுத் தேன்", "காட்டுமூலிகைகள்", "புளி", "நெல்லிக்காய்", "குங்கிலியம்"],
    "te": ["తेंदూ ఆకు", "మహువా పువ్వు", "అడవి తేనె", "అడవి మూలికలు", "చింతపండు", "ఉసిరి", "జిగురు"],
    "bn": ["তendu পাতা", "মহুয়া ফুল", "জংলি মধু", "ঔষধি গাছ", "তেঁতুল", "আমলকি", "ধুনা"],
    "or": ["ତେଣ୍ଡୁ ପତ୍ର", "ମହୁଆ ଫୁଲ", "ଜଙ୍ଗଲୀ ମଧୁ", "ଔଷଧି ଗଛ", "ତେନ୍ତୁଳି", "ଅଁଳା", "ଝୁଣା"]
}

# 7. Area Measurements - Dynamic generator
def get_random_area() -> str:
    """Generates a random float area to prevent model overfitting to specific numbers."""
    return str(round(random.uniform(0.5, 15.0), 2))

AREA_UNITS: Dict[str, List[str]] = {
    "hi": ["हेक्टेयर", "एकड़", "वर्ग फुट", "वर्ग मीटर"],
    "ta": ["ஹெக்டேர்", "ஏக்கர்", "சதுர அடி", "சென்ட்", "சதுர மீட்டர்"],
    "te": ["హెక్టారు", "ఎకరాలు", "చదరపు అడుగులు", "సెంట్లు", "చదరపు మీటర్లు"],
    "bn": ["হেক্টর", "একর", "বর্গফুট", "বর্গমিটার", "শতক"],
    "or": ["ହେକ୍ଟର", "ଏକର", "ବର୍ଗଫୁଟ", "ଡିସିମିଲ", "ବର୍ଗମିଟର"]
}

# 8. Boundary Landmarks
BOUNDARY_LANDMARKS: Dict[str, List[str]] = {
    "hi": ["उत्तर में नाला", "दक्षिण में राजस्व भूमि", "पूर्व में वन मार्ग", "पश्चिम में पहाड़ी", "उत्तर में सागौन का पेड़", "दक्षिण में सार्वजनिक रास्ता", "पूर्व में सरकारी बंजर", "पश्चिम में नदी"],
    "ta": ["வடக்கு: ஓடை", "தெற்கு: வருவாய் நிலம்", "கிழக்கு: காட்டுப் பாதை", "மேற்கு: மலை", "வடக்கு: தேக்கு மரம்", "தெற்கு: பொதுப் பாதை", "கிழக்கு: அரசுப் புறம்போக்கு", "மேற்கு: நதி"],
    "te": ["ఉత్తరం: వాగు", "దక్షిణం: రెవెన్యూ భూమి", "తూర్పు: అటవీ రహదారి", "పడమర: కొండ", "ఉత్తరం: టేకు చెట్టు", "దక్షిణం: పంచాయతీ రోడ్డు", "తూర్పు: ప్రభుత్వ పోరంబోకు", "పడమర: నది"],
    "bn": ["উত্তরে: নালা", "দক্ষিণে: রাজস্ব জমি", "পূর্বে: জঙ্গলের রাস্তা", "পশ্চিমে: পাহাড়", "উত্তরে: সেগুন গাছ", "দক্ষিণে: পঞ্চায়েত রাস্তা", "পূর্বে: খাস জমি", "পশ্চিমে: নদী"],
    "or": ["ଉତ୍ତରେ: ନାଳା", "ଦକ୍ଷିଣେ: ରାଜସ୍ୱ ଜମି", "ପୂର୍ବେ: ଜଙ୍ଗଲ ରାସ୍ତା", "ପଶ୍ଚିମେ: ପାହାଡ଼", "ଉତ୍ତରେ: ଶାଗୁଆନ ଗଛ", "ଦକ୍ଷିଣେ: ପଞ୍ଚାୟତ ରାସ୍ତା", "ପୂର୍ବେ: ସରକାରୀ ପଡିଆ", "ପଶ୍ଚିମେ: ନଦୀ"]
}

# 9. Caste / Category - Removed internal () to fix Regex/Tokenization issues
CASTE_CATEGORIES: Dict[str, List[str]] = {
    "hi": ["अनुसूचित जनजाति ST", "अन्य पारंपरिक वनवासी OTFD", "विशेष रूप से कमजोर जनजातीय समूह PVTG", "वन आश्रित समुदाय"],
    "ta": ["பழங்குடியினர் ST", "பாரம்பரிய வனவாசிகள் OTFD", "PVTG சமூகம்", "வனத்தைச் சார்ந்த பழங்குடியினர்"],
    "te": ["షెడ్యూల్డు తెగలు ST", "పరంపరాగత అటవీ నివాసితులు OTFD", "PVTG సమూహం", "అటవీ ఆధారిత గిరిజనులు"],
    "bn": ["তপশিলি উপজাতি ST", "অন্যান্য ঐতিহ্যগত বনবাসী OTFD", "PVTG সম্প্রদায়", "বন নির্ভরশীল আদিবাসী"],
    "or": ["ଅନୁସୂଚିତ ଜନଜାତି ST", "ଅନ୍ୟାନ୍ୟ ପାରମ୍ପରିକ ବନବାସୀ OTFD", "ପିଭିଟିଜି PVTG ସମ୍ପ୍ରଦାୟ", "ଜଙ୍ଗଲ ନିର୍ଭରଶୀଳ ସମ୍ପ୍ରଦାୟ"]
}

# 10. Evidence Items
EVIDENCE_POOLS: Dict[str, List[str]] = {
    "hi": ["मतदाता पहचान पत्र", "बुजुर्गों का बयान", "वन विभाग की जुर्माना रसीद", "पारंपरिक वंशावली", "राशन कार्ड", "आधार कार्ड", "पुरानी लगान रसीद", "ग्राम सभा का प्रमाण पत्र"],
    "ta": ["வாக்காளர் அடையாள அட்டை", "பெரியோர்களின் வாக்குமூலம்", "வனத்துறை அபராத ரசீது", "பாரம்பரிய வம்சாவளி", "ரேஷன் கார்டு", "ஆதார் அட்டை", "பழைய நில வரி ரசீது", "பஞ்சாயத்து சான்றிதழ்"],
    "te": ["ఓటరు గుర్తింపు కార్డు", "పెద్దల వాంగ్మూలం", "అటవీ శాఖ జరిమానా రసీదు", "వంశవృక్షం", "రేషన్ కార్డు", "ఆధార్ కార్డు", "పాత శిస్తు రసీదు", "గ్రామ సభ ధృవీకరణ పత్రం"],
    "bn": ["ভোটার পরিচয়পত্র", "প্রবীণদের জবানবন্দি", "বন দপ্তরের জরিমানার রসিদ", "বংশতালিকা", "রেশন কার্ড", "আধার কার্ড", "পুরনো খাজনার রসিদ", "গ্রাম সভার শংসাপত্র"],
    "or": ["ଭୋଟର ପରିଚୟ ପତ୍ର", "ବୟସ୍କମାନଙ୍କ ବୟାନ", "ଜଙ୍ଗଲ ବିଭାଗର ଜରିମାନା ରସିଦ", "ବଂଶାବଳୀ", "ରାସନ କାର୍ଡ", "ଆଧାର କାର୍ଡ", "ପୁରୁଣା ଖଜଣା ରସିଦ", "ଗ୍ରାମ ସଭା ପ୍ରମାଣପତ୍ର"]
}

def sample_name(lang: str) -> str:
    return RNG.choice(NAME_POOLS[lang])


def sample_village(lang: str) -> str:
    return RNG.choice(VILLAGE_POOLS[lang])


def sample_district(lang: str) -> str:
    return RNG.choice(DISTRICT_POOLS[lang])


def sample_state(lang: str) -> str:
    return RNG.choice(STATE_POOLS[lang])


def sample_tehsil(lang: str) -> str:
    return RNG.choice(TEHSIL_POOLS[lang])


def sample_minor_forest_produce(lang: str) -> str:
    return RNG.choice(MINOR_FOREST_PRODUCE[lang])


def sample_land_area(lang: str) -> str:
    # Use the new dynamic generator for infinite numeric variety
    value = get_random_area() 
    
    # Randomly choose a localized unit
    unit = RNG.choice(AREA_UNITS[lang])
    
    return f"{value} {unit}"

def sample_boundary_description(lang: str) -> str:
    choices = BOUNDARY_LANDMARKS[lang]
    picked = RNG.sample(choices, k=2)
    return "; ".join(picked)


def sample_khasra(lang: str) -> str:
    return RNG.choice(KHASRA_POOL[lang])


def sample_age() -> str:
    return str(RNG.randint(18, 70))


def sample_address(lang: str) -> str:
    """Construct a simple but realistic full address string for the language."""
    village = sample_village(lang)
    tehsil = sample_tehsil(lang)
    district = sample_district(lang)
    state = sample_state(lang)
    if lang == "hi":
        return f"ग्राम {village}, तहसील {tehsil}, जिला {district}, राज्य {state}"
    if lang == "ta":
        return f"கிராமம் {village}, தாலுகா {tehsil}, மாவட்டம் {district}, மாநிலம் {state}"
    if lang == "te":
        return f"గ్రామం {village}, తాలూకా {tehsil}, జిల్లా {district}, రాష్ట్రం {state}"
    if lang == "bn":
        return f"গ্রাম {village}, তহসিল {tehsil}, জেলা {district}, রাজ্য {state}"
    if lang == "or":
        return f"ଗ୍ରାମ {village}, ତହସିଲ {tehsil}, ଜିଲ୍ଲା {district}, ରାଜ୍ୟ {state}"
    return f"{village}, {tehsil}, {district}, {state}"


def sample_community_type_fdst(lang: str) -> str:
    if lang == "hi":
        return "एफडीएसटी समुदाय"
    if lang == "ta":
        return "எஃப்டிஎஸ்டி சமூக"
    if lang == "te":
        return "ఎఫ్‌డిఎస్టి సముదాయం"
    if lang == "bn":
        return "এফডিএসটি সম্প্রদায়"
    if lang == "or":
        return "ଏଫ୍ଡିଏସ୍ଟି ସମୁଦାୟ"
    return "FDST community"


def sample_community_type_otfd(lang: str) -> str:
    if lang == "hi":
        return "ओटीएफडी समुदाय"
    if lang == "ta":
        return "ஓடிஎஃப்டி சமூக"
    if lang == "te":
        return "ఓటీఎఫ్‌డీ సముదాయం"
    if lang == "bn":
        return "ওটিএফডি সম্প্রদায়"
    if lang == "or":
        return "ଓଟିଏଫ୍ଡି ସମୁଦାୟ"
    return "OTFD community"


# =============================
# Templates per language and document type
# =============================

# doc_type keys
DOC_CLAIM_FOREST_LAND = "claim_forest_land"
DOC_CLAIM_COMMUNITY_RIGHTS = "claim_community_rights"
DOC_CLAIM_COMMUNITY_FOREST_RESOURCE = "claim_community_forest_resource"
DOC_TITLE_UNDER_OCCUPATION = "title_forest_land_under_occupation"
DOC_TITLE_COMMUNITY_FOREST_RIGHTS = "title_community_forest_rights"
DOC_TITLE_COMMUNITY_FOREST_RESOURCES = "title_community_forest_resources"


TEMPLATES: Dict[str, Dict[str, List[str]]] = {
    # Hindi
    "hi": {
        DOC_CLAIM_FOREST_LAND: [
            # Variation 1: Bureaucratic / Form Style (Simulating Form A filled application)
            (
                "प्रपत्र - क [नियम 11(1)(a) देखें]\n"
                "वन भूमि पर अधिकारों के लिए दावा प्रपत्र एवं आवेदक का मूल विवरण।\n"
                "दावेदार का पूरा नाम: {CLAIMANT_NAME}।\n"
                "पिता अथवा माता का नाम: {FATHER_MOTHER_NAME}। जीवनसाथी का नाम: {SPOUSE_NAME}।\n"
                "आवेदक का पूर्ण आवासीय पता: {ADDRESS_FULL} दर्ज किया गया है।\n"
                "यह भूमि {STATE} राज्य के अंतर्गत {DISTRICT} जिले एवं {TEHSIL_TALUKA} तहसील की सीमा में स्थित है।\n"
                "साथ ही, यह {VILLAGE} ग्राम, {GRAM_PANCHAYAT} ग्राम पंचायत तथा {GRAM_SABHA} ग्राम सभा के अधिकार क्षेत्र में आती है।\n\n"

                "दावेदार के परिवार का विवरण एवं वन भूमि पर कब्जे की स्थिति:\n"
                "मेरे परिवार के सदस्य {FAMILY_MEMBER_NAME} (आयु: {FAMILY_MEMBER_AGE} वर्ष) और आश्रित {DEPENDENT_NAME} मेरे साथ निवास करते हैं।\n"
                "हम प्रमाणित करते हैं कि हम {CATEGORY_SCHEDULED_TRIBE} अथवा {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} श्रेणी से संबंधित हैं।\n"
                "आवास के उद्देश्य से हमारे कब्जे वाली वन भूमि का क्षेत्रफल {LAND_EXTENT_HABITATION} है।\n"
                "स्वयं खेती (कृषि) के लिए उपयोग की जा रही भूमि का क्षेत्रफल {LAND_EXTENT_SELF_CULTIVATION} निर्धारित है।\n"
                "वन ग्रामों में स्थित भूमि का क्षेत्रफल {LAND_EXTENT_FOREST_VILLAGE} के रूप में दर्ज किया गया है।\n\n"

                "भूमि से संबंधित अन्य दावे, विवाद एवं संलग्न साक्ष्य:\n"
                "यदि इस भूमि पर कोई विवाद है, तो उसका विवरण: {DISPUTED_LAND_DESCRIPTION}।\n"
                "पूर्व में जारी किए गए पट्टे, लीज या अनुदान का विवरण: {EXISTING_PATTAS_LEASES_GRANTS}।\n"
                "स्वस्थाने पुनर्वास या वैकल्पिक भूमि हेतु दावा की गई भूमि {REHABILITATION_LAND} है।\n"
                "बिना किसी मुआवजे के जिस भूमि से विस्थापित किया गया, उसका विवरण: {DISPLACED_FROM_LAND}।\n"
                "हमारे अन्य पारंपरिक अधिकार {OTHER_TRADITIONAL_RIGHT} हैं और अतिरिक्त सूचना {OTHER_INFORMATION} संलग्न है।\n"
                "इस दावे के समर्थन में साक्ष्य के रूप में {EVIDENCE_ITEM} प्रस्तुत किए जा रहे हैं।"
            ),
            # Variation 2: Narrative / Descriptive Style (Simulating a Gram Sabha resolution narrative)
            (
                "ग्राम सभा के समक्ष प्रस्तुत विस्तृत विवरण एवं वन भूमि पर अधिकार का दावा।\n"
                "मैं, श्री/श्रीमती {CLAIMANT_NAME} (पिता/माता: {FATHER_MOTHER_NAME}, पति/पत्नी: {SPOUSE_NAME}) यह विवरण प्रस्तुत कर रहा हूँ।\n"
                "मेरा स्थायी निवास का पूरा पता {ADDRESS_FULL} है। मैं {STATE} राज्य के {DISTRICT} जिले का निवासी हूँ।\n"
                "मेरा घर {TEHSIL_TALUKA} तहसील के अंतर्गत {VILLAGE} ग्राम में स्थित है।\n"
                "यह क्षेत्र सीधे तौर पर {GRAM_PANCHAYAT} ग्राम पंचायत और {GRAM_SABHA} ग्राम सभा के प्रशासनिक नियंत्रण में आता है।\n\n"

                "हमारा परिवार पीढ़ियों से वनों पर आश्रित है और हम {CATEGORY_SCHEDULED_TRIBE} अथवा {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} समुदाय के पारंपरिक वनवासी हैं।\n"
                "मेरे परिवार में सदस्य {FAMILY_MEMBER_NAME} (आयु {FAMILY_MEMBER_AGE} वर्ष) एवं मुझ पर पूर्णतः आश्रित {DEPENDENT_NAME} शामिल हैं।\n"
                "हम जिस स्थान पर कई पीढ़ियों से निवास कर रहे हैं, उस आवासीय वन भूमि का क्षेत्रफल {LAND_EXTENT_HABITATION} है।\n"
                "हमारे जीवनयापन का मुख्य साधन कृषि है और हमारी स्व-खेती वाली भूमि का क्षेत्रफल {LAND_EXTENT_SELF_CULTIVATION} है।\n"
                "इसके अतिरिक्त, वन ग्राम सीमा के भीतर हमारी जोत का क्षेत्रफल {LAND_EXTENT_FOREST_VILLAGE} मापा गया है।\n\n"

                "इस दावे के संदर्भ में कुछ महत्वपूर्ण वैधानिक तथ्य दर्ज किए जा रहे हैं।\n"
                "भूमि से जुड़े किसी भी विवाद की स्थिति {DISPUTED_LAND_DESCRIPTION} के रूप में स्पष्ट की गई है तथा पुराने पट्टों का विवरण {EXISTING_PATTAS_LEASES_GRANTS} है।\n"
                "हमें पुनर्वास हेतु {REHABILITATION_LAND} भूमि की आवश्यकता है और अतीत में हमें {DISPLACED_FROM_LAND} से बिना मुआवजे के हटाया गया था।\n"
                "हमारे पूर्वजों द्वारा उपयोग किए जाने वाले अन्य पारंपरिक अधिकार {OTHER_TRADITIONAL_RIGHT} आज भी प्रासंगिक हैं।\n"
                "दावे की पुष्टि के लिए मजबूत साक्ष्य {EVIDENCE_ITEM} प्रस्तुत हैं तथा अन्य संबंधित जानकारी {OTHER_INFORMATION} विचारार्थ संलग्न है।"
            ),
            # Variation 3: Formal Letter Style (Simulating a petition to the Sub-Divisional Level Committee)
            (
                "प्रेषक: {CLAIMANT_NAME}, पिता/माता: {FATHER_MOTHER_NAME}, जीवनसाथी: {SPOUSE_NAME}।\n"
                "पता: {ADDRESS_FULL}, ग्राम {VILLAGE}, पंचायत {GRAM_PANCHAYAT}, ग्राम सभा {GRAM_SABHA}।\n"
                "तहसील: {TEHSIL_TALUKA}, जिला: {DISTRICT}, राज्य: {STATE}।\n"
                "विषय: वन अधिकार अधिनियम 2006 के अंतर्गत व्यक्तिगत वन भूमि अधिकार प्रदान करने हेतु आवेदन।\n"
                "महोदय, उपर्युक्त विषय में सविनय निवेदन है कि मैं लंबे समय से वनों में निवास कर रहा हूँ।\n\n"

                "मैं प्रमाणित करता हूँ कि मैं {CATEGORY_SCHEDULED_TRIBE} या {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} श्रेणी का पात्र सदस्य हूँ।\n"
                "मेरे परिवार में {FAMILY_MEMBER_NAME} (उम्र {FAMILY_MEMBER_AGE}) तथा आश्रित {DEPENDENT_NAME} सम्मिलित हैं, जिनका भरण-पोषण इसी भूमि से होता है।\n"
                "वन क्षेत्र के भीतर हमारे मकान एवं आवासीय परिसर का कुल क्षेत्रफल {LAND_EXTENT_HABITATION} है।\n"
                "हमारे द्वारा स्वयं खेती के उपयोग में लाई जा रही कृषि भूमि का क्षेत्रफल {LAND_EXTENT_SELF_CULTIVATION} है।\n"
                "वन ग्रामों में हमारी जोत का क्षेत्रफल {LAND_EXTENT_FOREST_VILLAGE} के रूप में राजस्व रिकॉर्ड में दर्ज होना चाहिए।\n\n"

                "इस भूमि के संबंध में विवादित स्थिति {DISPUTED_LAND_DESCRIPTION} है जिसे सुलझाया जाना आवश्यक है।\n"
                "पूर्व में जारी किए गए लीज या पट्टे {EXISTING_PATTAS_LEASES_GRANTS} की प्रतियां सत्यापन हेतु संलग्न हैं।\n"
                "वैकल्पिक पुनर्वास भूमि {REHABILITATION_LAND} और मुआवजे के बिना विस्थापन वाली भूमि {DISPLACED_FROM_LAND} का संज्ञान भी लिया जाए।\n"
                "कानून द्वारा संरक्षित हमारे अन्य पारंपरिक अधिकार {OTHER_TRADITIONAL_RIGHT} हमें प्रदान किए जाएं।\n"
                "साक्ष्य के तौर पर {EVIDENCE_ITEM} और अतिरिक्त विवरण {OTHER_INFORMATION} आवेदन के साथ नत्थी किए गए हैं।"
            ),
            # Variation 4: Legal / Statutory Declaration Style (Simulating a sworn affidavit)
            (
                "शपथ पत्र एवं वैधानिक दावा प्रकटीकरण (वन अधिकार अधिनियम 2006 के तहत)।\n"
                "मैं, {CLAIMANT_NAME} (पिता/माता: {FATHER_MOTHER_NAME}, वैध जीवनसाथी: {SPOUSE_NAME}), सत्यनिष्ठा से निम्नलिखित घोषणा करता हूँ।\n"
                "मेरा कानूनी और स्थायी पता {ADDRESS_FULL} के रूप में सरकारी दस्तावेजों में पंजीकृत है।\n"
                "दावाकृत भूमि {STATE} राज्य, {DISTRICT} जिले और {TEHSIL_TALUKA} तहसील के क्षेत्राधिकार में स्थित है।\n"
                "यह भूमि पूर्णतः {VILLAGE} राजस्व ग्राम, {GRAM_PANCHAYAT} ग्राम पंचायत तथा {GRAM_SABHA} ग्राम सभा की वैधानिक सीमा के अधीन है।\n\n"

                "धारा 3(1)(a) के तहत भूमि कब्जे एवं सामाजिक श्रेणी की वैधानिक पुष्टि।\n"
                "मैं शपथपूर्वक कहता हूँ कि मैं {CATEGORY_SCHEDULED_TRIBE} अथवा {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} की वैधानिक श्रेणी के अंतर्गत आता हूँ।\n"
                "मेरे कानूनी वारिस {FAMILY_MEMBER_NAME} (आयु {FAMILY_MEMBER_AGE}) और आश्रित {DEPENDENT_NAME} इस दावे के प्रत्यक्ष लाभार्थी हैं।\n"
                "अधिनियम के प्रावधानों के तहत, आवासीय प्रयोजन के लिए कब्जे वाली भूमि का माप {LAND_EXTENT_HABITATION} निर्धारित किया गया है।\n"
                "कृषि उपयोग अथवा स्व-खेती के लिए जोती जा रही भूमि का क्षेत्रफल {LAND_EXTENT_SELF_CULTIVATION} पाया गया है।\n"
                "धारा 3(1)(h) के अनुसार वन ग्रामों में स्थित भूमि की सीमा {LAND_EXTENT_FOREST_VILLAGE} है।\n\n"

                "लंबित वादों, पट्टों और अन्य वैधानिक अधिकारों का प्रकटीकरण।\n"
                "धारा 3(1)(f) के अंतर्गत इस भूमि पर किसी भी प्रकार का विवाद {DISPUTED_LAND_DESCRIPTION} के रूप में घोषित किया जाता है।\n"
                "विगत सरकारों द्वारा निर्गत पट्टे या अनुदान का विवरण: {EXISTING_PATTAS_LEASES_GRANTS}।\n"
                "धारा 3(1)(m) के तहत स्वस्थाने पुनर्वासित भूमि {REHABILITATION_LAND} का विवरण भी प्रस्तुत है।\n"
                "धारा 4(8) के अनुसार बिना किसी उचित मुआवजे के बेदखल की गई भूमि का विवरण {DISPLACED_FROM_LAND} है।\n"
                "धारा 3(1)(l) के तहत अन्य रूढ़िगत अधिकार {OTHER_TRADITIONAL_RIGHT} और कानूनी साक्ष्य {EVIDENCE_ITEM} सहित {OTHER_INFORMATION} इस हलफनामे का अभिन्न अंग हैं।"
            )
        ],

        DOC_CLAIM_COMMUNITY_RIGHTS: [
            # Variation 1: Bureaucratic / Form Style
            (
                "प्रपत्र - ख [नियम 11(1)(a) और (4) देखें]\n"
                "सामुदायिक वन अधिकारों के लिए विधिवत दावा प्रपत्र एवं ग्राम सभा का प्रस्ताव।\n"
                "यह सामूहिक आवेदन {VILLAGE} ग्राम तथा {GRAM_PANCHAYAT} ग्राम पंचायत की ओर से प्रस्तुत किया जा रहा है।\n"
                "इसे {STATE} राज्य, {DISTRICT} जिले, और {TEHSIL_TALUKA} तहसील के अंतर्गत {GRAM_SABHA} ग्राम सभा द्वारा विधिवत पारित किया गया है।\n"
                "हम सभी पारंपरिक वनवासी हैं जो {COMMUNITY_TYPE_FDST} अथवा {COMMUNITY_TYPE_OTFD} समुदाय का प्रतिनिधित्व करते हैं।\n\n"

                "समुदाय द्वारा उपभोग किए जा रहे वन अधिकारों की प्रकृति का विवरण निम्नवत दर्ज है।\n"
                "सामुदायिक उपयोग के लिए निस्तार (Nistar) के अधिकार: {COMMUNITY_RIGHT_NISTAR}।\n"
                "गौण वनोपज (MFP) के संग्रहण और स्वामित्व का अधिकार: {RIGHT_MINOR_FOREST_PRODUCE}।\n"
                "मछली पकड़ने, जल निकायों और अन्य संसाधनों के उपयोग का अधिकार: {COMMUNITY_RIGHT_RESOURCE_USE}।\n"
                "पशुओं को चराने (चराई) से संबंधित अधिकार: {COMMUNITY_RIGHT_GRAZING}।\n"
                "घुमंतू और पशुपालक समुदायों के लिए पारंपरिक संसाधनों तक पहुँच: {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS}।\n\n"

                "विशेष रूप से कमजोर जनजातीय समूहों (PTG) और कृषि-पूर्व समुदायों के लिए पर्यावास (Habitat) अधिकार {COMMUNITY_TENURE_HABITAT} सुनिश्चित किए जाएं।\n"
                "जैव विविधता, बौद्धिक संपदा और पारंपरिक ज्ञान तक पहुँच का अधिकार {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} के रूप में मान्य हो।\n"
                "कानून द्वारा परिभाषित अन्य पारंपरिक अधिकार {OTHER_TRADITIONAL_RIGHT} हमारी आजीविका का मूल आधार हैं।\n"
                "इन सामूहिक दावों को सिद्ध करने हेतु प्रस्तुत साक्ष्य: {EVIDENCE_ITEM}।\n"
                "प्रशासनिक समीक्षा के लिए आवश्यक अतिरिक्त जानकारी {OTHER_INFORMATION} इस प्रपत्र के साथ संलग्न है।"
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "सामुदायिक वनीकरण और पारंपरिक अधिकारों के संरक्षण हेतु ग्राम सभा का सामूहिक आवेदन।\n"
                "हमारी {GRAM_SABHA} ग्राम सभा, {VILLAGE} ग्राम के सभी निवासियों की ओर से यह दावा प्रस्तुत करती है।\n"
                "हमारा क्षेत्र {STATE} राज्य के {DISTRICT} जिले में स्थित {TEHSIL_TALUKA} तहसील और {GRAM_PANCHAYAT} पंचायत के अंतर्गत आता है।\n"
                "हमारा समुदाय सरकारी वर्गीकरण के अनुसार {COMMUNITY_TYPE_FDST} अथवा {COMMUNITY_TYPE_OTFD} के रूप में मान्यता प्राप्त है।\n"
                "हम पीढ़ियों से वनों के साथ सह-अस्तित्व की जीवनशैली का पालन करते आ रहे हैं।\n\n"

                "दैनिक जीवन और आजीविका के लिए हम मुख्य रूप से निम्नलिखित सामुदायिक अधिकारों पर निर्भर हैं।\n"
                "हमारे निस्तार अधिकार स्पष्ट रूप से {COMMUNITY_RIGHT_NISTAR} के रूप में स्थापित हैं।\n"
                "शहद, जड़ी-बूटी जैसी गौण वनोपज प्राप्त करने का अधिकार {RIGHT_MINOR_FOREST_PRODUCE} है।\n"
                "स्थानीय जल निकायों के उपयोग और मछली पकड़ने का अधिकार {COMMUNITY_RIGHT_RESOURCE_USE} है।\n"
                "मवेशियों के लिए चारागाह और चराई का अधिकार {COMMUNITY_RIGHT_GRAZING} के अंतर्गत सुरक्षित है।\n"
                "ऋतु प्रवास करने वाले घुमंतू समुदायों के संसाधन अधिकार {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS} के रूप में प्रदत्त हैं।\n\n"

                "आदिम जनजातियों के प्राचीन पर्यावास (Habitat) को संरक्षित करने वाला अधिकार {COMMUNITY_TENURE_HABITAT} अत्यंत महत्वपूर्ण है।\n"
                "पारंपरिक ज्ञान और स्थानीय जैव विविधता पर हमारा अधिकार {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} के रूप में दावा किया गया है।\n"
                "हमारे पूर्वजों द्वारा उपयोग किए गए अन्य रूढ़िगत अधिकार {OTHER_TRADITIONAL_RIGHT} आज भी जारी हैं।\n"
                "इन अधिकारों की प्रामाणिकता हेतु {EVIDENCE_ITEM} जैसे ऐतिहासिक दस्तावेज़ प्रस्तुत किए गए हैं।\n"
                "विस्तृत विचार-विमर्श के लिए {OTHER_INFORMATION} सहित अन्य तथ्य भी साथ में दिए गए हैं।"
            ),
            # Variation 3: Formal Letter Style
            (
                "विषय: वन अधिकार अधिनियम 2006 के तहत सामुदायिक वन अधिकारों की मान्यता हेतु सामूहिक ज्ञापन।\n"
                "हम {STATE} राज्य, {DISTRICT} जिले और {TEHSIL_TALUKA} तहसील के निवासी हैं।\n"
                "हमारा निवास {VILLAGE} ग्राम तथा {GRAM_PANCHAYAT} पंचायत के अधिकार क्षेत्र में आता है।\n"
                "यह पत्र {GRAM_SABHA} ग्राम सभा की सर्वसम्मति और पूर्ण सहमति से लिखा जा रहा है।\n"
                "हम आदिवासी और पारंपरिक वनवासी हैं जो {COMMUNITY_TYPE_FDST} तथा {COMMUNITY_TYPE_OTFD} समुदाय से संबंध रखते हैं।\n\n"

                "अधिनियम के प्रावधानों के अनुरूप, हम निम्नलिखित सामुदायिक अधिकारों की मांग करते हैं:\n"
                "निस्तार और साझा उपयोग के अधिकार: {COMMUNITY_RIGHT_NISTAR}। गौण वनोपज का अधिकार: {RIGHT_MINOR_FOREST_PRODUCE}।\n"
                "तालाबों और जल संसाधनों के उपयोग का अधिकार: {COMMUNITY_RIGHT_RESOURCE_USE}।\n"
                "पशु चराने का सामुदायिक अधिकार: {COMMUNITY_RIGHT_GRAZING}।\n"
                "घुमंतू समुदायों के लिए चरागाहों तक पहुंच का अधिकार: {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS}।\n\n"

                "हमारे पारंपरिक आवासों का पट्टा {COMMUNITY_TENURE_HABITAT} के रूप में हमें सौंपा जाना चाहिए।\n"
                "हमारे ज्ञान और जैव विविधता पर बौद्धिक अधिकार {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} सुनिश्चित किया जाए।\n"
                "अन्य सभी पारंपरिक अधिकार {OTHER_TRADITIONAL_RIGHT} जो हमारे जीवन से जुड़े हैं, वे भी मान्य हों।\n"
                "इस दावे के समर्थन में ठोस साक्ष्य के रूप में {EVIDENCE_ITEM} संलग्न किए गए हैं।\n"
                "अतिरिक्त जानकारी {OTHER_INFORMATION} प्रशासन के संज्ञान में लाई जा रही है।"
            ),
            # Variation 4: Legal / Statutory Declaration Style
            (
                "सामुदायिक वन अधिकारों (Community Forest Rights) का वैधानिक दावा एवं घोषणा पत्र।\n"
                "यह घोषणा {STATE} राज्य, {DISTRICT} जिले, और {TEHSIL_TALUKA} तहसील के संबंधित अधिकारियों के समक्ष प्रस्तुत की जा रही है।\n"
                "यह दावा {VILLAGE} ग्राम निवासियों की ओर से, {GRAM_PANCHAYAT} ग्राम पंचायत एवं {GRAM_SABHA} ग्राम सभा के वैधानिक प्रस्ताव द्वारा पारित है।\n"
                "वन अधिकार अधिनियम 2006 के तहत इस समुदाय को {COMMUNITY_TYPE_FDST} अथवा {COMMUNITY_TYPE_OTFD} के रूप में कानूनी मान्यता प्राप्त है।\n"
                "इस समुदाय के सामूहिक अधिकारों को विधिपूर्वक पुनर्स्थापित करने हेतु यह प्रलेख तैयार किया गया है।\n\n"

                "धारा 3 के अंतर्गत परिभाषित सामुदायिक उपयोग एवं संसाधनों पर अधिकारों की सूची।\n"
                "धारा 3(1)(b) के तहत निस्तार (Nistar) के वैधानिक अधिकार {COMMUNITY_RIGHT_NISTAR} घोषित किए जाते हैं।\n"
                "धारा 3(1)(c) के तहत गौण वनोपज (MFP) पर स्वामित्व का अधिकार {RIGHT_MINOR_FOREST_PRODUCE} के रूप में मान्य है।\n"
                "जल निकायों और मत्स्य पालन का उपयोग करने का कानूनी अधिकार {COMMUNITY_RIGHT_RESOURCE_USE} निर्धारित है।\n"
                "पारंपरिक चराई अधिकार {COMMUNITY_RIGHT_GRAZING} के रूप में आधिकारिक तौर पर दर्ज हैं।\n"
                "घुमंतू समुदायों की संसाधनों तक वैधानिक पहुंच {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS} सुनिश्चित की गई है।\n\n"

                "जनजातीय पर्यावास अधिकार, बौद्धिक संपदा एवं प्रस्तुत वैधानिक साक्ष्य।\n"
                "पीटीजी (PTG) एवं कृषि-पूर्व समुदायों के लिए पर्यावास (Habitat) का कानूनी अधिकार {COMMUNITY_TENURE_HABITAT} दावा किया जाता है।\n"
                "धारा 3(1)(k) के अनुसार जैव विविधता और पारंपरिक ज्ञान तक पहुंच का अधिकार {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} दर्ज है।\n"
                "कानून द्वारा प्रदत्त अन्य सभी रूढ़िगत अधिकार {OTHER_TRADITIONAL_RIGHT} हमारी सामूहिक विरासत हैं।\n"
                "उपरोक्त वैधानिक दावों को सिद्ध करने हेतु दस्तावेजी साक्ष्य {EVIDENCE_ITEM} संलग्न हैं।\n"
                "विधिक जांच के प्रयोजनार्थ अन्य डेटा {OTHER_INFORMATION} आधिकारिक रूप से प्रस्तुत किया जाता है।"
            )
        ],

        DOC_CLAIM_COMMUNITY_FOREST_RESOURCE: [
            # Variation 1: Bureaucratic / Form Style
            (
                "प्रपत्र - ग [अधिनियम की धारा 3(1)(i) और नियम 11(1) देखें]\n"
                "सामुदायिक वन संसाधनों (CFR) के अधिकारों के लिए दावा प्रपत्र।\n"
                "यह दावा {STATE} राज्य, {DISTRICT} जिले, तथा {TEHSIL_TALUKA} तहसील के क्षेत्राधिकार के अंतर्गत आता है।\n"
                "इसे {GRAM_PANCHAYAT} ग्राम पंचायत के अधीन {VILLAGE} ग्रामवासियों की ओर से प्रस्तुत किया जा रहा है।\n"
                "यह प्रस्ताव {GRAM_SABHA} ग्राम सभा की विधिवत बैठक में सर्वसम्मति से पारित किया गया है।\n\n"

                "इस दावे को प्रस्तुत करने वाले ग्राम सभा के प्रमुख सदस्य {GRAM_SABHA_MEMBER_NAME} हैं।\n"
                "ये सदस्य वैधानिक रूप से {CATEGORY_SCHEDULED_TRIBE} अथवा {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} समुदाय से संबंध रखते हैं।\n"
                "हम जिस वन संसाधन क्षेत्र पर दावा कर रहे हैं उसका खसरा/कम्पार्टमेंट नंबर {KHASRA_COMPARTMENT_NUMBER} है।\n"
                "हमारे वन क्षेत्र की सीमा से लगे हुए सीमावर्ती ग्राम {BORDERING_VILLAGE} हैं।\n"
                "इस क्षेत्र की भौगोलिक सीमाएं {BOUNDARY_DESCRIPTION} के रूप में स्पष्ट रूप से परिभाषित की गई हैं।\n\n"

                "इस भूभाग को हमारा समुदाय पीढ़ियों से संरक्षित और प्रबंधित करता आ रहा है।\n"
                "इसके लिए सामुदायिक वन संसाधन साक्ष्यों की विधिवत सूची {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} संलग्न की गई है।\n"
                "हमारे पारंपरिक उपयोग को सिद्ध करने वाले अन्य साक्ष्य {EVIDENCE_ITEM} के रूप में प्रस्तुत हैं।\n"
                "हम पुष्टि करते हैं कि इस वन संसाधन का स्थायी उपयोग करने का अधिकार ग्राम सभा में निहित है।\n"
                "सक्षम प्राधिकारी से अनुरोध है कि वे इसकी जांच कर सामुदायिक वन संसाधन अधिकार को मान्यता प्रदान करें।"
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "सामुदायिक वन संसाधनों के प्रबंधन और संरक्षण हेतु ग्राम सभा का सामूहिक घोषणा पत्र।\n"
                "हम, {STATE} राज्य के {DISTRICT} जिले में स्थित {TEHSIL_TALUKA} तहसील के निवासी हैं।\n"
                "हमारा {VILLAGE} ग्राम, {GRAM_PANCHAYAT} ग्राम पंचायत के प्रशासनिक ढांचे के अंतर्गत आता है।\n"
                "आज {GRAM_SABHA} ग्राम सभा में एकत्र होकर, हम अपने पारंपरिक वन संसाधन अधिकारों की घोषणा करते हैं।\n"
                "इस सभा का नेतृत्व करने वाले प्रमुख सदस्य {GRAM_SABHA_MEMBER_NAME} हैं।\n\n"

                "हम सभी पारंपरिक वनवासी हैं जो {CATEGORY_SCHEDULED_TRIBE} या {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} समुदाय से आते हैं।\n"
                "हम जिस वन क्षेत्र का प्रबंधन करते हैं, उसका खसरा/कम्पार्टमेंट नंबर {KHASRA_COMPARTMENT_NUMBER} भू-अभिलेखों में दर्ज है।\n"
                "हमारे वन क्षेत्र के चारों ओर स्थित पड़ोसी गाँव {BORDERING_VILLAGE} के रूप में जाने जाते हैं।\n"
                "उत्तर में नदी और दक्षिण में पहाड़ी तक विस्तृत हमारी सीमाओं का विवरण {BOUNDARY_DESCRIPTION} है।\n"
                "इस सीमा के भीतर उपलब्ध सभी संसाधनों के संरक्षण का पूर्ण अधिकार हमारे पास है।\n\n"

                "जैव विविधता को बनाए रखने और वनों को कटाई से बचाने के लिए हम दृढ़ संकल्पित हैं।\n"
                "अपने दावे को मजबूत करने के लिए हमने साक्ष्यों की एक सूची {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} तैयार की है।\n"
                "मौखिक इतिहास और ऐतिहासिक दस्तावेजों को {EVIDENCE_ITEM} के रूप में प्रस्तुत किया गया है।\n"
                "इन प्रमाणों के आधार पर, सामुदायिक वन संसाधन अधिकार (CFR) हमें तुरंत प्रदान किया जाना चाहिए।\n"
                "हम सरकारी अधिकारियों से अनुरोध करते हैं कि वे इस पर शीघ्रता से विचार कर आदेश जारी करें।"
            ),
            # Variation 3: Formal Letter Style
            (
                "विषय: धारा 3(1)(i) के अंतर्गत सामुदायिक वन संसाधनों (CFR) पर अधिकार का दावा।\n"
                "क्षेत्र का विवरण: तहसील {TEHSIL_TALUKA}, जिला {DISTRICT}, राज्य {STATE}।\n"
                "ग्राम: {VILLAGE}, पंचायत: {GRAM_PANCHAYAT}, ग्राम सभा: {GRAM_SABHA}।\n"
                "यह दावा ग्राम सभा सदस्य {GRAM_SABHA_MEMBER_NAME} के नेतृत्व में प्रशासन के समक्ष प्रस्तुत किया जा रहा है।\n"
                "आवेदक मुख्य रूप से {CATEGORY_SCHEDULED_TRIBE} और {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} वर्ग से संबंधित हैं।\n\n"

                "हमारे द्वारा संरक्षित वन क्षेत्र का खसरा या कम्पार्टमेंट नंबर {KHASRA_COMPARTMENT_NUMBER} है।\n"
                "हमारी सीमा से सटे हुए सीमावर्ती गाँव जैसे कि {BORDERING_VILLAGE} इस वन को साझा नहीं करते हैं।\n"
                "हमारे सामुदायिक वन संसाधनों की भौगोलिक सीमाएं {BOUNDARY_DESCRIPTION} के अनुसार नक्शे पर अंकित हैं।\n"
                "इस क्षेत्र के पारिस्थितिक संतुलन को बनाए रखना हमारे समुदाय का प्राथमिक कर्तव्य रहा है।\n"
                "अतः, इन वन संसाधनों के प्रबंधन का पूर्ण अधिकार हमारी ग्राम सभा को दिया जाना चाहिए।\n\n"

                "इस भूमि के साथ हमारे पारंपरिक जुड़ाव को प्रमाणित करने वाले साक्ष्य संकलित किए गए हैं।\n"
                "महत्वपूर्ण दस्तावेजों की सूची {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} आधिकारिक रूप से जमा की जा रही है।\n"
                "अन्य पुख्ता प्रमाणों के रूप में {EVIDENCE_ITEM} दस्तावेज़ भी इस आवेदन के साथ नत्थी हैं।\n"
                "ये सभी साक्ष्य हमारे दावे की वैधता और न्यायसंगतता को पूर्णतः सिद्ध करते हैं।\n"
                "इसके आधार पर हमारी ग्राम सभा के सामुदायिक वन संसाधन अधिकार को सरकारी मान्यता मिलनी चाहिए।"
            ),
            # Variation 4: Legal / Statutory Declaration Style
            (
                "सामुदायिक वन संसाधनों (Community Forest Resource) के दावों की वैधानिक प्रकटीकरण प्रलेख।\n"
                "वन अधिकार अधिनियम 2006, धारा 3(1)(i) के तहत, {STATE} राज्य, {DISTRICT} जिले, {TEHSIL_TALUKA} तहसील के प्राधिकारियों को प्रस्तुत वैधानिक दावा।\n"
                "यह आधिकारिक मांग {VILLAGE} ग्राम के निवासियों की ओर से, {GRAM_PANCHAYAT} ग्राम पंचायत एवं {GRAM_SABHA} ग्राम सभा के माध्यम से प्रस्तुत है।\n"
                "ग्राम सभा के अधिकृत कानूनी प्रतिनिधि {GRAM_SABHA_MEMBER_NAME} इस प्रलेख पर हस्ताक्षर करते हैं।\n"
                "इस दावे में शामिल सदस्य {CATEGORY_SCHEDULED_TRIBE} अथवा {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} नामक विधिक श्रेणी द्वारा संरक्षित हैं।\n\n"

                "दावाकृत वन संसाधन क्षेत्र की भौगोलिक, भूमि मापन एवं सीमा संबंधी वैधानिक प्रविष्टियाँ।\n"
                "दावे के अधीन वन क्षेत्र का वैधानिक खसरा (Khasra) या वन विभाग कम्पार्टमेंट नंबर {KHASRA_COMPARTMENT_NUMBER} राजस्व अभिलेखों में दर्ज है।\n"
                "राजस्व मानचित्र के अनुसार, इस क्षेत्र के साथ सीमा साझा करने वाले अண்டை (पड़ोसी) ग्राम {BORDERING_VILLAGE} हैं।\n"
                "संपूर्ण दावाकृत वन संसाधन क्षेत्र की भौगोलिक एवं स्थलाकृतिक सीमाएं {BOUNDARY_DESCRIPTION} के रूप में अत्यंत स्पष्टता से परिभाषित हैं।\n"
                "इन सीमाओं के भीतर मौजूद वन संसाधनों का स्थायी उपयोग और प्रबंधन करने का रूढ़िगत वैधानिक अधिकार इस समुदाय के पास है।\n"
                "इस क्षेत्र में वन संपदा के पुनरुत्पादन का उत्तरदायित्व और अधिकार कानूनी रूप से ग्राम सभा को सौंपा जाना चाहिए।\n\n"

                "प्रामाणिक साक्ष्यों की प्रस्तुति एवं विधिक दावों की पुष्टि।\n"
                "इस समुदाय के पारंपरिक संबंध को प्रमाणित करने के लिए, साक्ष्यों की आधिकारिक सूची {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} संलग्न है।\n"
                "साथ ही, ग्राम्य रिकॉर्ड और ऐतिहासिक प्रलेखों जैसे अतिरिक्त पुष्टिकर साक्ष्य {EVIDENCE_ITEM} के रूप में प्रस्तुत किए गए हैं।\n"
                "ये सभी प्रलेख अधिनियम के नियम 13 के तहत विधिक साक्ष्य के रूप में स्वीकार्य और मान्य हैं।\n"
                "इन प्रमाणों के आधार पर, संपूर्ण क्षेत्र के संरक्षण और संवर्धन का वैधानिक अधिकार ग्राम सभा को प्रदान किया जाना अनिवार्य है।\n"
                "कानूनी प्रावधानों के अनुसार इस दावे पर शीघ्र समीक्षा कर राजपत्रित आदेश जारी करने का आग्रह किया जाता है।"
            )
        ],

        DOC_TITLE_UNDER_OCCUPATION: [
            # Variation 1: Bureaucratic / Form Style
            (
                "परिशिष्ट - II [नियम 8(h) देखें]\n"
                "कब्जे के अधीन वन भूमि के लिए आधिकारिक अधिकार पत्र / पट्टा।\n"
                "वन भूमि का यह अधिकार पत्र {TITLE_HOLDER_NAME} को राज्य सरकार द्वारा प्रदान किया जाता है।\n"
                "पट्टा धारक के पिता/माता का नाम {FATHER_MOTHER_NAME} तथा जीवनसाथी का नाम {SPOUSE_NAME} है।\n"
                "इन पर आश्रित व्यक्ति {DEPENDENT_NAME} भी इस अधिकार पत्र के संरक्षण के अंतर्गत आते हैं।\n\n"

                "पट्टा धारक का पूर्ण पंजीकृत पता {TITLE_ADDRESS_FULL} है।\n"
                "यह वन भूमि {VILLAGE} ग्राम और {GRAM_PANCHAYAT} ग्राम पंचायत के भौगोलिक क्षेत्र में स्थित है।\n"
                "यह {GRAM_SABHA} ग्राम सभा के क्षेत्राधिकार में, {TEHSIL_TALUKA} तहसील के अंतर्गत आती है।\n"
                "यह जिला {DISTRICT} और राज्य {STATE} के प्रशासनिक नियंत्रण के अधीन है।\n"
                "यह प्रमाणित किया जाता है कि धारक {CATEGORY_SCHEDULED_TRIBE} या {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} वर्ग का पात्र सदस्य है।\n\n"

                "इस दस्तावेज़ द्वारा अधिकार में दी गई वन भूमि का कुल क्षेत्रफल {TITLE_LAND_AREA_MEASURE} है।\n"
                "भूमि रिकॉर्ड में इस भूमि का खसरा या कम्पार्टमेंट नंबर {KHASRA_COMPARTMENT_NUMBER} के रूप में दर्ज है।\n"
                "भूमि की चारों दिशाओं की सीमाएं प्राकृतिक चिन्हों द्वारा {BOUNDARY_DESCRIPTION} के रूप में वर्णित हैं।\n"
                "यह अधिकार वंशानुगत है, परन्तु इसे बेचा या हस्तांतरित नहीं किया जा सकता है।\n"
                "जिला कलेक्टर और प्रभागीय वन अधिकारी के हस्ताक्षर से इसे आधिकारिक रूप से जारी किया गया है।"
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "जनजातीय कार्य मंत्रालय द्वारा जारी व्यक्तिगत वन भूमि अधिकार पत्र (पट्टा)।\n"
                "श्री/श्रीमती {TITLE_HOLDER_NAME} (पिता/माता: {FATHER_MOTHER_NAME}, पति/पत्नी: {SPOUSE_NAME}) को यह पट्टा प्रदान किया जा रहा है।\n"
                "उन पर आश्रित {DEPENDENT_NAME} जैसे परिवार के अन्य सदस्यों का भी इस भूमि पर अधिकार सुरक्षित रहेगा।\n"
                "इनका आवासीय पता {TITLE_ADDRESS_FULL} के रूप में सरकारी रिकॉर्ड में विधिवत दर्ज है।\n"
                "यह क्षेत्र {STATE} राज्य के {DISTRICT} जिले में स्थित {TEHSIL_TALUKA} तहसील के अंतर्गत आता है।\n\n"

                "यह भूखंड {VILLAGE} ग्राम में, {GRAM_PANCHAYAT} पंचायत के अधीन, {GRAM_SABHA} ग्राम सभा के नियंत्रण में है।\n"
                "लाभार्थी को आदिवासी श्रेणी {CATEGORY_SCHEDULED_TRIBE} या पारंपरिक वनवासी {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} के रूप में मान्यता प्राप्त है।\n"
                "सरकार ने कृषि एवं आवास के प्रयोजन हेतु इन्हें {TITLE_LAND_AREA_MEASURE} क्षेत्रफल की भूमि आवंटित की है।\n"
                "राजस्व रिकॉर्ड में उस भूमि का खसरा (Khasra) या मापन संख्या {KHASRA_COMPARTMENT_NUMBER} स्पष्ट रूप से अंकित है।\n"
                "स्थान की सटीक स्थिति और परिधि को {BOUNDARY_DESCRIPTION} के सीमांकन विवरण के माध्यम से प्रलेखित किया गया है।\n\n"

                "यह वन भूमि पट्टा वन अधिकार अधिनियम 2006 के सभी नियमों के अधीन है।\n"
                "धारक को केवल इस भूमि पर खेती करने और पीढ़ी दर पीढ़ी इसका उपभोग करने का अधिकार है।\n"
                "किसी भी परिस्थिति में इस वन भूमि को किसी अन्य व्यक्ति को बेचा या पट्टे पर नहीं दिया जा सकता है।\n"
                "संबंधित विभाग के अधिकारियों द्वारा राज्य सरकार की आधिकारिक मुहर के साथ इसे प्रमाणित किया गया है।\n"
                "यह दस्तावेज़ पट्टा धारक की आजीविका की रक्षा करने वाले कानूनी कवच के रूप में कार्य करेगा।"
            ),
            # Variation 3: Formal Letter Style
            (
                "वन भूमि अधिकार आदेश एवं पट्टा प्रमाणपत्र।\n"
                "अधिकार धारक का नाम: {TITLE_HOLDER_NAME}। माता-पिता का नाम: {FATHER_MOTHER_NAME}। जीवनसाथी: {SPOUSE_NAME}।\n"
                "आश्रित सदस्य: {DEPENDENT_NAME}। धारक की श्रेणी: {CATEGORY_SCHEDULED_TRIBE} / {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER}।\n"
                "पता: {TITLE_ADDRESS_FULL}, ग्राम: {VILLAGE}, पंचायत: {GRAM_PANCHAYAT}, ग्राम सभा: {GRAM_SABHA}।\n"
                "तहसील: {TEHSIL_TALUKA}, जिला: {DISTRICT}, राज्य: {STATE}।\n\n"

                "वन अधिकार अधिनियम 2006 की धारा 4 के अंतर्गत इस भूमि अधिकार को आधिकारिक तौर पर मान्यता दी जाती है।\n"
                "उपर्युक्त लाभार्थी के कब्जे वाली {TITLE_LAND_AREA_MEASURE} क्षेत्रफल की भूमि के लिए पट्टा प्रदान किया जा रहा है।\n"
                "राजस्व विभाग के अभिलेखों के अनुसार, इस भूमि का खसरा नंबर {KHASRA_COMPARTMENT_NUMBER} है।\n"
                "भूमि की सीमाएं {BOUNDARY_DESCRIPTION} के चिह्नों के साथ सटीकता से परिभाषित की गई हैं।\n"
                "सभी जांच और सत्यापन के बाद, जिला स्तरीय समिति (DLC) ने इस भूमि आवंटन को अपनी स्वीकृति दे दी है।\n\n"

                "यह भूमि अधिकार एक वंशानुगत अधिकार के रूप में जारी रहेगा, लेकिन भूमि अहस्तांतरणीय (non-transferable) है।\n"
                "लाभार्थी को सरकार द्वारा समय-समय पर लागू वन संरक्षण नियमों का पालन करना अनिवार्य होगा।\n"
                "इसके माध्यम से, सरकार द्वारा वनवासियों की आर्थिक और सामाजिक सुरक्षा सुनिश्चित की जा रही है।\n"
                "यह प्रमाणपत्र राज्य सरकार के अधिकृत अधिकारियों द्वारा हस्ताक्षरित और मुहरबंद है।\n"
                "यह दस्तावेज़ जारी होने की तिथि से ही विधिक रूप से प्रभाव में आ जाएगा।"
            ),
            # Variation 4: Legal / Statutory Document Style
            (
                "वन भूमि अधिकार अधिनियम 2006 के अंतर्गत वैधानिक पट्टा विलेख (Statutory Title Deed)।\n"
                "राज्य सरकार की विधिक शक्तियों के अधीन, यह अधिकार पत्र {TITLE_HOLDER_NAME} नामक लाभार्थी के पक्ष में वैधानिक रूप से पंजीकृत किया जाता है।\n"
                "अभिलेखों के अनुसार लाभार्थी के पिता/माता का नाम {FATHER_MOTHER_NAME} एवं विधिक जीवनसाथी का नाम {SPOUSE_NAME} सत्यापित किया गया है।\n"
                "लाभार्थी पर पूर्णतः आश्रित विधिक वारिसों {DEPENDENT_NAME} के नाम भी इस विलेख में सम्मिलित किए गए हैं।\n"
                "लाभार्थी का आधिकारिक एवं वैधानिक आवासीय पता {TITLE_ADDRESS_FULL} के रूप में राजस्व तथा वन अभिलेखों में दर्ज है।\n"
                "यह भूखंड {STATE} राज्य, {DISTRICT} जिले, {TEHSIL_TALUKA} तहसील के अंतर्गत {VILLAGE} ग्राम, {GRAM_PANCHAYAT} ग्राम पंचायत एवं {GRAM_SABHA} ग्राम सभा के वैधानिक क्षेत्राधिकार में स्थित है।\n\n"

                "लाभार्थी का विधिक वर्गीकरण, भूमि का मापन एवं भौगोलिक सीमाओं का प्रमाणीकरण।\n"
                "लाभार्थी को अधिनियम के विधिक प्रावधानों के तहत {CATEGORY_SCHEDULED_TRIBE} अथवा {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} श्रेणी का पात्र माना गया है।\n"
                "सरकार द्वारा विधिवत मापन के पश्चात आवंटित वन भूमि का कुल क्षेत्रफल {TITLE_LAND_AREA_MEASURE} घोषित किया गया है।\n"
                "राजस्व और वन अभिलेखों में इस भूमि का विशिष्ट खसरा (Khasra) या कम्पार्टमेंट नंबर {KHASRA_COMPARTMENT_NUMBER} दर्ज किया गया है।\n"
                "इस भूखंड की चारों दिशाओं की भौगोलिक और प्राकृतिक सीमाएं {BOUNDARY_DESCRIPTION} के रूप में अत्यंत स्पष्टता से सीमांकित की गई हैं।\n"
                "यह मापन राजस्व निरीक्षक एवं वन विभाग के सर्वेक्षकों द्वारा प्रत्यक्ष भौतिक सत्यापन के उपरांत किया गया है।\n\n"

                "अधिकार की वैधानिक प्रकृति, प्रतिबंध एवं प्राधिकारियों का प्रमाणीकरण।\n"
                "धारा 4(4) के प्रावधानों के तहत, यह भूमि अधिकार पूर्णतः वंशानुगत है, परन्तु किसी भी दशा में इसे बेचा, हस्तांतरित या गिरवी नहीं रखा जा सकता (non-alienable)।\n"
                "लाभार्थी वन संरक्षण अधिनियमों और पर्यावरण सुरक्षा नियमों के अनुपालन के लिए विधिक रूप से बाध्य होगा।\n"
                "यदि नियमों का उल्लंघन पाया जाता है, तो बिना किसी पूर्व सूचना के राज्य सरकार इस अधिकार को निरस्त करने की पूर्ण शक्ति रखती है।\n"
                "यह वैधानिक पट्टा उप-प्रभागीय (SDLC) तथा जिला स्तरीय (DLC) समितियों के विधिवत अनुमोदन के पश्चात ही निर्गत किया गया है।\n"
                "इसकी वैधानिक पुष्टि हेतु, जिला कलेक्टर (District Collector) तथा प्रभागीय वन अधिकारी (DFO) ने इस पट्टे पर आधिकारिक हस्ताक्षर एवं मुहर अंकित की है।"
            )
        ],

        DOC_TITLE_COMMUNITY_FOREST_RIGHTS: [
            # Variation 1: Bureaucratic / Form Style
            (
                "परिशिष्ट - III [नियम 8(h) देखें]\n"
                "सामुदायिक वन अधिकारों के लिए पट्टा और आधिकारिक अधिकार प्रलेख।\n"
                "यह सामुदायिक वन अधिकार {COMMUNITY_RIGHT_HOLDER_NAME} नामक सामुदायिक इकाई को प्रदान किया जाता है।\n"
                "यह क्षेत्र {STATE} राज्य, {DISTRICT} जिले और {TEHSIL_TALUKA} तहसील के अंतर्गत आता है।\n"
                "यह पट्टा {VILLAGE} ग्राम, {GRAM_PANCHAYAT} ग्राम पंचायत और {GRAM_SABHA} ग्राम सभा की सामूहिक संपत्ति है।\n\n"

                "यह अधिकार प्राप्त करने वाला समुदाय {CATEGORY_SCHEDULED_TRIBE} या {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} के रूप में मान्यता प्राप्त है।\n"
                "समुदाय को प्रदान किए गए अधिकार की प्रकृति {COMMUNITY_RIGHT_NATURE} के रूप में स्पष्ट रूप से परिभाषित की गई है।\n"
                "इस अधिकार का उपयोग करने से जुड़ी कुछ शर्तें हैं, जो इस प्रकार हैं: {TITLE_CONDITIONS}।\n"
                "इस अधिकार के अधीन आने वाले वन क्षेत्र का खसरा/कम्पार्टमेंट नंबर {KHASRA_COMPARTMENT_NUMBER} है।\n"
                "भूमि की सीमाएं {BOUNDARY_DESCRIPTION} जैसे भौगोलिक संदर्भों द्वारा दर्शाई गई हैं।\n\n"

                "इसके अतिरिक्त, इस क्षेत्र की पारंपरिक रूढ़िगत सीमा {CUSTOMARY_BOUNDARY} को भी पारंपरिक रूप से मान्यता प्राप्त है।\n"
                "यह दस्तावेज़ सामुदायिक उपयोग के लिए वन संसाधनों तक पहुंच को वैधानिक मान्यता प्रदान करता है।\n"
                "परंतु, संसाधनों का उपयोग इस प्रकार किया जाना चाहिए कि वन की जैव विविधता को कोई नुकसान न पहुंचे।\n"
                "नियमों का उल्लंघन होने पर सरकार के पास इस अधिकार पर पुनर्विचार करने की शक्ति सुरक्षित है।\n"
                "यह पट्टा जिला स्तरीय प्राधिकारियों द्वारा अनुमोदित और जारी किया गया है।"
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "सामुदायिक वन अधिकार पट्टा एवं ग्राम सभा को वैधानिक अधिकार सौंपने का प्रलेख।\n"
                "सरकार की विधिवत मंजूरी के साथ, यह अधिकार {COMMUNITY_RIGHT_HOLDER_NAME} संस्था/समुदाय को दिया जाता है।\n"
                "यह समुदाय {STATE} राज्य के {DISTRICT} जिले में स्थित {TEHSIL_TALUKA} तहसील में लंबे समय से निवास कर रहा है।\n"
                "इनका निवास क्षेत्र {VILLAGE} ग्राम, {GRAM_PANCHAYAT} पंचायत और {GRAM_SABHA} ग्राम सभा के अंतर्गत समाहित है।\n"
                "इन्हें आधिकारिक रिकॉर्ड में {CATEGORY_SCHEDULED_TRIBE} और {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} श्रेणी के रूप में दर्ज किया गया है।\n\n"

                "इन्हें प्रदान किए गए सामुदायिक अधिकार की सटीक प्रकृति का विवरण {COMMUNITY_RIGHT_NATURE} है।\n"
                "इस सामुदायिक अधिकार के प्रयोग हेतु निर्धारित नियम और शर्तें {TITLE_CONDITIONS} हैं।\n"
                "वन विभाग के अभिलेखों के अनुसार, इस क्षेत्र का खसरा नंबर {KHASRA_COMPARTMENT_NUMBER} अंकित है।\n"
                "इस क्षेत्र की सीमाएं प्राकृतिक चिह्नों का उपयोग करते हुए {BOUNDARY_DESCRIPTION} के रूप में वर्णित की गई हैं।\n"
                "साथ ही, पीढ़ियों से चली आ रही रूढ़िगत सीमा (Customary Boundary) {CUSTOMARY_BOUNDARY} के रूप में पुष्ट की गई है।\n\n"

                "इस दस्तावेज़ के माध्यम से चराई और गौण वनोपज संग्रह के सामुदायिक अधिकार सुरक्षित किए जाते हैं।\n"
                "पर्यावरण और वन क्षेत्र की रक्षा करने का उत्तरदायित्व इसी समुदाय को सौंपा जाता है।\n"
                "अवैध कटाई और शिकार जैसी गैरकानूनी गतिविधियां पूरी तरह से निषिद्ध हैं।\n"
                "यह राज्य सरकार के जनजातीय कल्याण विभाग और राजस्व विभाग की सहमति से जारी किया जाता है।\n"
                "ग्राम सभा को इस दस्तावेज़ को सुरक्षित रखना चाहिए और इसके प्रावधानों को ठीक से लागू करना चाहिए।"
            ),
            # Variation 3: Formal Letter Style
            (
                "सामुदायिक वन अधिकारों को मान्यता देने वाला आधिकारिक अधिकार प्रमाणपत्र।\n"
                "अधिकार प्राप्तकर्ता: {COMMUNITY_RIGHT_HOLDER_NAME}।\n"
                "क्षेत्र: {VILLAGE} ग्राम, {GRAM_PANCHAYAT} पंचायत, {GRAM_SABHA} ग्राम सभा।\n"
                "प्रशासनिक सीमाएँ: तहसील {TEHSIL_TALUKA}, जिला {DISTRICT}, राज्य {STATE}।\n"
                "लाभार्थी श्रेणी: {CATEGORY_SCHEDULED_TRIBE} अथवा {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER}।\n\n"

                "राज्य सरकार द्वारा उपर्युक्त समुदाय को {COMMUNITY_RIGHT_NATURE} की प्रकृति वाले वन अधिकार प्रदान किए जाते हैं।\n"
                "यह अधिकार {TITLE_CONDITIONS} में उल्लिखित प्रतिबंधों और शर्तों के अधीन रहेगा।\n"
                "आवंटित वन भूमि का खसरा या मापन संख्या {KHASRA_COMPARTMENT_NUMBER} निर्धारित है।\n"
                "दस्तावेज़ों में निर्दिष्ट भूमि की सीमाएं {BOUNDARY_DESCRIPTION} चिह्नों द्वारा तय की गई हैं।\n"
                "समुदाय द्वारा पारंपरिक रूप से मानी जाने वाली रूढ़िगत सीमा {CUSTOMARY_BOUNDARY} भी प्रमाणित की जाती है।\n\n"

                "इस अधिकार का प्रयोग केवल ग्राम सभा के सामूहिक प्रबंधन के तहत ही किया जाना चाहिए।\n"
                "वन संसाधनों का उपयोग व्यावसायिक उद्देश्यों के लिए नहीं, बल्कि केवल सामुदायिक आवश्यकताओं के लिए किया जाना चाहिए।\n"
                "ग्राम सभा को सरकारी ऑडिट और निरीक्षण में पूर्ण सहयोग देना अनिवार्य है।\n"
                "यह दस्तावेज़ जिला कलेक्टर और प्रभागीय वन अधिकारी की मुहर के साथ जारी किया जाता है।\n"
                "इसके जारी होने की तिथि से, समुदाय की वन-आधारित आर्थिक स्वतंत्रता सुनिश्चित होती है।"
            ),
            # Variation 4: Legal / Statutory Document Style
            (
                "सामुदायिक वन अधिकारों (CFR) का राजपत्रित वैधानिक विलेख (Statutory Deed) एवं पट्टा।\n"
                "इस आधिकारिक विलेख के माध्यम से, {COMMUNITY_RIGHT_HOLDER_NAME} नामक सामुदायिक इकाई को वन भूमि पर वैधानिक अधिकार प्रदान किए जाते हैं।\n"
                "यह अधिकार {STATE} राज्य, {DISTRICT} जिले एवं {TEHSIL_TALUKA} तहसील के भौगोलिक क्षेत्राधिकार के भीतर प्रदान किया जाता है।\n"
                "वैधानिक रूप से यह क्षेत्र {VILLAGE} ग्राम, {GRAM_PANCHAYAT} ग्राम पंचायत तथा {GRAM_SABHA} ग्राम सभा के प्रशासनिक नियंत्रण में आता है।\n"
                "अधिकार प्राप्त करने वाला यह समुदाय, सरकारी अभिलेखों के अनुसार {CATEGORY_SCHEDULED_TRIBE} अथवा {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} वैधानिक श्रेणी के तहत संरक्षित है।\n"
                "ग्राम सभा के सामूहिक प्रस्ताव तथा जिला स्तरीय समिति (DLC) के अनुमोदन के आधार पर यह प्रलेख वैधानिक रूप से निर्गत किया जा रहा है।\n\n"

                "स्वीकृत सामुदायिक अधिकार की प्रकृति, शर्तें एवं भौगोलिक प्रलेखीकरण।\n"
                "सरकार द्वारा इस समुदाय को आधिकारिक तौर पर प्रदान किए गए अधिकार की प्रकृति {COMMUNITY_RIGHT_NATURE} के रूप में सुस्पष्ट परिभाषित है।\n"
                "इस अधिकार का उपयोग करने हेतु वन विभाग द्वारा लागू की गई वैधानिक शर्तें और प्रतिबंध इस प्रकार हैं: {TITLE_CONDITIONS}।\n"
                "सामुदायिक अधिकारों के अधीन आने वाले वन क्षेत्र का वैधानिक खसरा या मापन संख्या {KHASRA_COMPARTMENT_NUMBER} के रूप में पंजीकृत है।\n"
                "भूमि की सीमाएं, पहाड़ों, नदियों जैसे प्राकृतिक चिह्नों का संदर्भ देते हुए {BOUNDARY_DESCRIPTION} के रूप में प्रलेखित की गई हैं।\n"
                "साथ ही, कई पीढ़ियों से समुदाय द्वारा मान्य रूढ़िगत सीमा (Customary Boundary) {CUSTOMARY_BOUNDARY} वैधानिक रूप से पुष्ट की जाती है।\n\n"

                "समुदाय के वैधानिक दायित्व, प्रतिबंध एवं सरकार का अंतिम अनुमोदन।\n"
                "यह अधिकार प्रमाण पत्र पूर्णतः सामुदायिक उपयोग हेतु है; इसका किसी भी प्रकार का वाणिज्यिक (Commercial) दोहन वर्जित है।\n"
                "पशुओं के चरने और वनोपज संग्रह के साथ-साथ, वन की जैव विविधता को कोई नुकसान न पहुंचे, यह सुनिश्चित करना समुदाय का वैधानिक दायित्व है।\n"
                "यदि अवैध कटाई या राज्य विरोधी गतिविधियों में संलिप्तता पाई जाती है, तो यह अधिकार तत्काल प्रभाव से निरस्त कर दिया जाएगा।\n"
                "जनजातीय कार्य विभाग और वन विभाग दोनों के पूर्ण समन्वय के साथ इस प्रलेख को प्रशासित किया जाएगा।\n"
                "जिला कलेक्टर (DM) और संबंधित वन अधिकारियों की आधिकारिक मुहर और हस्ताक्षर के साथ यह पट्टा राजपत्र में पंजीकृत किया जाता है।"
            )
        ],

        DOC_TITLE_COMMUNITY_FOREST_RESOURCES: [
            # Variation 1: Bureaucratic / Form Style
            (
                "परिशिष्ट - IV [नियम 8(i) देखें]\n"
                "सामुदायिक वन संसाधनों (CFR) के लिए पट्टा और अधिकार पत्र।\n"
                "यह आधिकारिक दस्तावेज़ {STATE} राज्य, {DISTRICT} जिले, {TEHSIL_TALUKA} तहसील के अंतर्गत आने वाले क्षेत्र को प्रदान किया जाता है।\n"
                "इसके अनुसार, {VILLAGE} ग्राम, {GRAM_PANCHAYAT} ग्राम पंचायत और {GRAM_SABHA} ग्राम सभा को सामुदायिक वन संसाधन अधिकार दिया जाता है।\n"
                "यह अधिकार {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} या {COMMUNITY_TYPE_BOTH} समुदायों से संबंधित लोगों के लिए है।\n\n"

                "इस सामुदायिक वन संसाधन अधिकार के अधीन क्षेत्र के खसरा/कम्पार्टमेंट नंबर {KHASRA_COMPARTMENT_NUMBER} हैं।\n"
                "इस क्षेत्र की भौगोलिक स्थिति और सीमाएं {BOUNDARY_DESCRIPTION} के रूप में अत्यंत स्पष्ट रूप से प्रलेखित की गई हैं।\n"
                "साथ ही, सदियों से चली आ रही पारंपरिक रूढ़िगत सीमा {CUSTOMARY_BOUNDARY} को कानूनी रूप से मान्यता प्राप्त है।\n"
                "निर्दिष्ट क्षेत्र के भीतर सभी लघु वनोपजों के प्रबंधन का अधिकार ग्राम सभा को सौंपा गया है।\n"
                "वन विभाग के दिशा-निर्देशों के अनुसार, समुदाय को इन संसाधनों का संरक्षण और स्थायी उपयोग करना होगा।\n\n"

                "यह अधिकार आदिवासियों और अन्य पारंपरिक वनवासियों की आजीविका को बेहतर बनाने के उद्देश्य से दिया जा रहा है।\n"
                "वन संसाधनों के प्रबंधन हेतु समितियां गठित करने का पूरा अधिकार ग्राम सभा को दिया गया है।\n"
                "इन संसाधनों को नुकसान पहुंचाने वाले किसी भी कार्य को कानूनी अपराध माना जाएगा और अधिकार रद्द कर दिए जाएंगे।\n"
                "राज्य सरकार के सक्षम अधिकारियों, जैसे जिला कलेक्टर और वन अधिकारी ने इसे विधिवत अनुमोदित किया है।\n"
                "यह दस्तावेज़ सामुदायिक वन संसाधनों के संरक्षण में एक महत्वपूर्ण मील के पत्थर के रूप में दर्ज किया जा रहा है।"
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "सामुदायिक वन संसाधनों के लिए वैधानिक अधिकार प्रलेख एवं ग्राम सभा को शक्ति हस्तांतरण।\n"
                "सरकार ने {STATE} राज्य के {DISTRICT} जिले की {TEHSIL_TALUKA} तहसील में रहने वाले लोगों की मांग को स्वीकार कर लिया है।\n"
                "इस आधार पर {VILLAGE} ग्राम, {GRAM_PANCHAYAT} पंचायत और {GRAM_SABHA} ग्राम सभा को CFR पट्टा प्रदान किया जाता है।\n"
                "यह अधिकार मान्यता {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} अथवा {COMMUNITY_TYPE_BOTH} समुदायों पर लागू होती है।\n"
                "ये वे समुदाय हैं जो जंगल को देवता मानते हैं और उसे संरक्षित करने की परंपरा रखते हैं।\n\n"

                "सामुदायिक वन संसाधन क्षेत्र के लिए खसरा/कम्पार्टमेंट नंबर {KHASRA_COMPARTMENT_NUMBER} भूमि सर्वेक्षण रिकॉर्ड में उल्लेखित हैं।\n"
                "इस क्षेत्र की सीमाएं, पहाड़ों और नदियों को चिह्नित करते हुए {BOUNDARY_DESCRIPTION} के रूप में परिभाषित की गई हैं।\n"
                "इसके परे हमारी पारंपरिक रूढ़िगत सीमा {CUSTOMARY_BOUNDARY} को भी सरकार द्वारा स्वीकार कर लिया गया है।\n"
                "इस सीमा के भीतर उपलब्ध जलाऊ लकड़ी, शहद और जड़ी-बूटियों का स्वतंत्र रूप से उपयोग करने का अधिकार ग्राम सभा को है।\n"
                "इसके अलावा, वन माफियाओं से जंगल की रक्षा करने की पूरी जिम्मेदारी इसी समुदाय को सौंपी गई है।\n\n"

                "सामुदायिक वन संसाधन अधिकार कानून आदिवासी लोगों के आत्मनिर्णय के अधिकार को सुनिश्चित करता है।\n"
                "जैव विविधता को बनाए रखने के लिए ग्राम सभा को एक उचित प्रबंधन योजना तैयार करनी चाहिए।\n"
                "सरकार और वन विभाग ग्राम सभा की प्रबंधन योजनाओं के लिए केवल तकनीकी सहायता प्रदान करेंगे।\n"
                "यह दस्तावेज़ समुदाय के आर्थिक विकास और जंगल की स्थिरता दोनों को एक साथ सुनिश्चित करेगा।\n"
                "संबंधित अधिकारियों के विधिवत हस्ताक्षर के साथ यह पट्टा आज से प्रभावी हो गया है।"
            ),
            # Variation 3: Formal Letter Style
            (
                "शीर्षक: सामुदायिक वन संसाधनों (CFR) पर अधिकार और पट्टा प्रमाणपत्र।\n"
                "लाभार्थी निकाय: {GRAM_SABHA} ग्राम सभा, {VILLAGE} ग्राम, {GRAM_PANCHAYAT} पंचायत।\n"
                "स्थान: तहसील {TEHSIL_TALUKA}, जिला {DISTRICT}, राज्य {STATE}।\n"
                "समुदाय का वर्गीकरण: {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} अथवा {COMMUNITY_TYPE_BOTH}।\n"
                "विषय: उपर्युक्त ग्राम सभा को सामुदायिक वन संसाधनों के प्रबंधन का आधिकारिक अधिकार प्रदान करना।\n\n"

                "वन अधिकार अधिनियम 2006 के प्रावधानों के आधार पर यह ऐतिहासिक अधिकार प्रदान किया जा रहा है।\n"
                "अधिकार प्राप्त वन क्षेत्र का खसरा या मापन संख्या {KHASRA_COMPARTMENT_NUMBER} स्पष्ट रूप से दर्ज किया गया है।\n"
                "उस क्षेत्र की सीमा को {BOUNDARY_DESCRIPTION} विवरण के माध्यम से भौगोलिक रूप से परिभाषित किया गया है।\n"
                "समुदाय द्वारा पारंपरिक रूप से अनुरक्षित रूढ़िगत सीमा {CUSTOMARY_BOUNDARY} भी इसमें शामिल है।\n"
                "इस सीमा के भीतर सभी प्राकृतिक संसाधनों की रक्षा और उपयोग करने का अधिकार ग्राम सभा का है।\n\n"

                "यह अधिकार किसी भी तरह से व्यक्ति विशेष का नहीं है, यह पूरे समुदाय की साझा संपत्ति है।\n"
                "वन संसाधनों के स्थायी प्रबंधन के लिए ग्राम सभा को एक वन अधिकार समिति बनाकर कार्य करना चाहिए।\n"
                "जंगल की आग जैसी प्राकृतिक आपदाओं से जंगल को बचाना समुदाय का प्राथमिक कर्तव्य है।\n"
                "यह अधिकार राज्य स्तरीय समिति द्वारा समीक्षा और अंतिम स्वीकृति के बाद प्रदान किया जाता है।\n"
                "यह प्रमाणपत्र संबंधित जिला अधिकारियों की मुहर के साथ आधिकारिक तौर पर जारी किया जाता है।"
            ),
            # Variation 4: Legal / Statutory Document Style
            (
                "सामुदायिक वन संसाधनों (Community Forest Resources) का वैधानिक पट्टा एवं सरकार का अधिकार हस्तांतरण प्रलेख।\n"
                "धारा 3(1)(i) के प्रावधानों के अंतर्गत, {STATE} राज्य, {DISTRICT} जिले, {TEHSIL_TALUKA} तहसील के क्षेत्राधिकार में यह विलेख वैधानिक रूप से निष्पादित किया जाता है।\n"
                "तदनुसार, {VILLAGE} ग्राम, {GRAM_PANCHAYAT} ग्राम पंचायत तथा {GRAM_SABHA} ग्राम सभा को सामुदायिक वन संसाधनों के प्रबंधन का पूर्ण वैधानिक अधिकार सौंपा जाता है।\n"
                "यह प्रलेख, {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} अथवा {COMMUNITY_TYPE_BOTH} समुदायों से संबंधित निवासियों की आजीविका को सुरक्षित करने वाला एक विधिक प्रपत्र है।\n"
                "जिला स्तरीय समिति (DLC) के अंतिम विधिक अनुमोदन के पश्चात ही इस अधिकार प्रमाणपत्र को आधिकारिक रूप से प्रकाशित किया जा रहा है।\n"
                "इसके द्वारा, राज्य के स्वामित्व वाले वन संसाधनों की सुरक्षा और प्रबंधन का अधिकार वैधानिक रूप से ग्राम सभा को हस्तांतरित किया जाता है।\n\n"

                "वन संसाधन क्षेत्र के वैधानिक भू-सर्वेक्षण क्रमांक, सीमाएं एवं रूढ़िगत प्रकटीकरण।\n"
                "सामुदायिक प्रबंधन के अधीन वन संसाधन क्षेत्र के खसरा (Khasra) या कम्पार्टमेंट नंबर {KHASRA_COMPARTMENT_NUMBER} भू-सर्वेक्षण अभिलेखों में स्पष्ट रूप से दर्ज किए गए हैं।\n"
                "इस क्षेत्र की भौगोलिक और स्थलाकृतिक सीमाएं {BOUNDARY_DESCRIPTION} के रूप में मानचित्रों द्वारा सरकार द्वारा विधिक रूप से पुष्ट की गई हैं।\n"
                "पड़ोसी ग्रामों और वन विभाग के साथ सीमा साझा करने वाली पारंपरिक रूढ़िगत सीमा (Customary Boundary) {CUSTOMARY_BOUNDARY} आधिकारिक रूप से प्रमाणित की जाती है।\n"
                "इन सीमाओं के भीतर मौजूद गौण वनोपज, जल संसाधनों और वनस्पतियों का उपयोग करने का पूर्ण अधिकार ग्राम सभा को प्रदान किया गया है।\n"
                "सीमा संबंधी किसी भी विवाद से बचने के लिए भूमि सर्वेक्षण विभाग के माध्यम से उचित सीमा-स्तंभ और विधिक चिह्न स्थापित किए गए हैं।\n\n"

                "ग्राम सभा के वैधानिक दायित्व, वन संरक्षण एवं अधिकारियों का अंतिम प्रमाणीकरण।\n"
                "अधिनियम के मूल नियमों को छोड़कर, राज्य सरकार द्वारा इस अधिकार पर कोई अन्य नवीन प्रतिबंध या शर्तें नहीं लगाई गई हैं।\n"
                "तथापि, वन के पारिस्थितिक संतुलन को बनाए रखना और दावानल (Forest Fire) जैसी आपदाओं को रोकना ग्राम सभा का पूर्ण वैधानिक दायित्व होगा।\n"
                "इस प्रयोजन हेतु ग्राम सभा की ओर से 'वन संसाधन संरक्षण समिति' का गठन किया जाना अनिवार्य है, जिसकी रिपोर्ट प्रतिवर्ष सरकार को प्रस्तुत की जाएगी।\n"
                "विधिक रूप से अवैध तरीके से वन संसाधनों का विनाश किए जाने पर, आपराधिक प्रक्रिया संहिता के तहत ग्राम सभा को जवाबदेह ठहराया जाएगा।\n"
                "राज्य सरकार के शीर्ष अधिकारियों—जिला कलेक्टर, प्रभागीय वन अधिकारी (DFO) तथा जनजातीय कल्याण अधिकारी के हस्ताक्षरों से यह पट्टा वैधानिक रूप से प्रभावी हो जाता है।"
            )
        ]
    },
    # Tamil
    "ta": {
        DOC_CLAIM_FOREST_LAND: [
            # Variation 1: Bureaucratic / Form Style (Simulating a filled application form)
            (
                "படிவம் - A [விதி 11(1)(a) பார்க்க]\n"
                "காட்டு நில உரிமைகளுக்கான கோரிக்கை படிவம் மற்றும் விண்ணப்பதாரரின் அடிப்படை விவரங்கள்.\n"
                "விண்ணப்பதாரரின் முழுப் பெயர்: {CLAIMANT_NAME}.\n"
                "தந்தை அல்லது தாயின் பெயர்: {FATHER_MOTHER_NAME}. வாழ்க்கைத் துணையின் பெயர்: {SPOUSE_NAME}.\n"
                "விண்ணப்பதாரரின் முழுமையான முகவரி: {ADDRESS_FULL}.\n"
                "இந்த நிலமானது {STATE} மாநிலம், {DISTRICT} மாவட்டம், {TEHSIL_TALUKA} தாலுகா எல்லைக்கு உட்பட்டது.\n"
                "மேலும், இது {VILLAGE} கிராமம், {GRAM_PANCHAYAT} கிராம பஞ்சாயத்து மற்றும் {GRAM_SABHA} கிராம சபைக்கு உட்பட்ட பகுதியாகும்.\n\n"
                
                "விண்ணப்பதாரரின் குடும்ப விவரங்கள் மற்றும் நில ஆக்கிரமிப்பு விவரங்கள்:\n"
                "எனது குடும்ப உறுப்பினர் {FAMILY_MEMBER_NAME} (வயது: {FAMILY_MEMBER_AGE}), மற்றும் சார்ந்திருக்கும் நபர் {DEPENDENT_NAME} ஆகியோர் என்னுடன் வசிக்கின்றனர்.\n"
                "நாங்கள் {CATEGORY_SCHEDULED_TRIBE} அல்லது {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} வகையைச் சார்ந்தவர்கள்.\n"
                "காட்டுப்பகுதியில் நாங்கள் வசிப்பிடமாகப் பயன்படுத்தும் நிலத்தின் அளவு {LAND_EXTENT_HABITATION} ஆகும்.\n"
                "மேலும், எங்கள் சொந்த விவசாயத்திற்காக உழும் நிலத்தின் அளவு {LAND_EXTENT_SELF_CULTIVATION} என மதிப்பிடப்பட்டுள்ளது.\n"
                "காட்டுக் கிராமங்களில் உள்ள நிலத்தின் அளவு {LAND_EXTENT_FOREST_VILLAGE} எனவும் ஆவணப்படுத்தப்பட்டுள்ளது.\n\n"
                
                "நிலத்தின் மீதான இதர கோரிக்கைகள் மற்றும் ஆதாரங்கள்:\n"
                "இந்த நிலம் தொடர்பாக ஏதேனும் சர்ச்சைகள் இருப்பின் அதன் விவரம்: {DISPUTED_LAND_DESCRIPTION}.\n"
                "ஏற்கனவே நிலுவையில் உள்ள பட்டாக்கள் அல்லது குத்தகைகள்: {EXISTING_PATTAS_LEASES_GRANTS}.\n"
                "மாற்று நிலம் அல்லது மறுவாழ்வுக்காக ஒதுக்கப்பட்ட நிலம் {REHABILITATION_LAND} ஆகும்.\n"
                "முன்பு இழப்பீடு இன்றி வெளியேற்றப்பட்ட நிலத்தின் விவரம்: {DISPLACED_FROM_LAND}.\n"
                "இதர பாரம்பரிய உரிமைகள் ஏதேனும் இருப்பின்: {OTHER_TRADITIONAL_RIGHT}. கூடுதல் தகவல்கள்: {OTHER_INFORMATION}.\n"
                "இக்கோரிக்கையை மெய்ப்பிக்கும் சான்றுகளாக {EVIDENCE_ITEM} ஆவணங்களை இத்துடன் இணைத்துள்ளேன்."
            ),
            # Variation 2: Narrative / Descriptive Style (Simulating a Gram Sabha resolution)
            (
                "கிராம சபையின் முன் சமர்ப்பிக்கப்படும் விரிவான அறிக்கை மற்றும் நில உரிமை கோரிக்கை.\n"
                "திரு/திருமதி {CLAIMANT_NAME} (தந்தை/தாய்: {FATHER_MOTHER_NAME}, கணவன்/மனைவி: {SPOUSE_NAME}) ஆகிய நான் இந்த அறிக்கையைச் சமர்ப்பிக்கிறேன்.\n"
                "எனது நிரந்தர வசிப்பிட முகவரி {ADDRESS_FULL} ஆகும். நான் {STATE} மாநிலத்தின் {DISTRICT} மாவட்டத்தைச் சேர்ந்தவன்.\n"
                "என் வசிப்பிடம் {TEHSIL_TALUKA} தாலுகாவில் உள்ள {VILLAGE} கிராமத்தில் அமைந்துள்ளது.\n"
                "இது {GRAM_PANCHAYAT} கிராம பஞ்சாயத்து மற்றும் {GRAM_SABHA} கிராம சபையின் நேரடி கட்டுப்பாட்டில் வருகிறது.\n\n"

                "எங்கள் குடும்பம் {CATEGORY_SCHEDULED_TRIBE} அல்லது {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} சமூகத்தைச் சேர்ந்த பாரம்பரிய வனவாசிகள் ஆவர்.\n"
                "என் வீட்டில் வசிக்கும் குடும்ப உறுப்பினர் {FAMILY_MEMBER_NAME} என்பவருக்கு வயது {FAMILY_MEMBER_AGE} ஆகிறது.\n"
                "என்னை முழுமையாகச் சார்ந்திருக்கும் {DEPENDENT_NAME} என்பவரும் இக்குடியிருப்பில் வாழ்ந்து வருகிறார்.\n"
                "நாங்கள் தலைமுறை தலைமுறையாக வாழ்ந்து வரும் குடியிருப்பின் நில அளவு {LAND_EXTENT_HABITATION} ஆகும்.\n"
                "எங்கள் வாழ்வாதாரத்திற்காக சொந்தமாக விவசாயம் செய்யும் நிலத்தின் அளவு {LAND_EXTENT_SELF_CULTIVATION}.\n"
                "மேலும், வனக் கிராமங்களுக்குள் நாங்கள் அனுபவிக்கும் நிலப்பரப்பு {LAND_EXTENT_FOREST_VILLAGE} ஆகும்.\n\n"

                "இந்தக் கோரிக்கை தொடர்பாக சில சட்டப்பூர்வமான தகவல்களைப் பதிவு செய்ய விரும்புகிறேன்.\n"
                "நிலம் குறித்த முரண்பாடுகள்: {DISPUTED_LAND_DESCRIPTION}. ஏற்கனவே உள்ள குத்தகை விவரங்கள்: {EXISTING_PATTAS_LEASES_GRANTS}.\n"
                "மறுவாழ்வு அல்லது மாற்று நிலம் கோரும் பகுதி: {REHABILITATION_LAND}. இழப்பீடின்றி இழந்த நிலம்: {DISPLACED_FROM_LAND}.\n"
                "எங்கள் முன்னோர்கள் அனுபவித்த மற்ற பாரம்பரிய உரிமைகள்: {OTHER_TRADITIONAL_RIGHT}.\n"
                "இந்த உரிமைகளை உறுதிப்படுத்த {EVIDENCE_ITEM} போன்ற வலுவான ஆதாரங்களை முன்வைக்கிறேன்.\n"
                "தேவைப்படும் இதர விவரங்கள்: {OTHER_INFORMATION} ஆகியவை அதிகாரிகளின் பார்வைக்குச் சமர்ப்பிக்கப்படுகின்றன."
            ),
            # Variation 3: Formal Letter Style (Simulating a petition to the Sub-Divisional Committee)
            (
                "அனுப்புநர்: {CLAIMANT_NAME}, த/பெ அல்லது தா/பெ {FATHER_MOTHER_NAME}, வாழ்க்கைத்துணை {SPOUSE_NAME}.\n"
                "முகவரி: {ADDRESS_FULL}, {VILLAGE} கிராமம், {GRAM_PANCHAYAT} பஞ்சாயத்து, {GRAM_SABHA} கிராம சபை.\n"
                "தாலுகா: {TEHSIL_TALUKA}, மாவட்டம்: {DISTRICT}, மாநிலம்: {STATE}.\n"
                "பொருள்: வன உரிமைச் சட்டம் 2006-ன் கீழ் தனிநபர் காட்டு நில உரிமை கோருதல் தொடர்பாக.\n"
                "ஐயா/அம்மையீர், நான் மேற்குறிப்பிட்ட முகவரியில் பல ஆண்டுகளாக வசித்து வருகிறேன்.\n\n"

                "நான் {CATEGORY_SCHEDULED_TRIBE} அல்லது {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} சமூகத்தைச் சேர்ந்தவன் என்பதை உறுதிப்படுத்துகிறேன்.\n"
                "எனது குடும்பத்தில் {FAMILY_MEMBER_NAME} (வயது {FAMILY_MEMBER_AGE}) மற்றும் என்னைச் சார்ந்தவர் {DEPENDENT_NAME} ஆகியோர் உள்ளனர்.\n"
                "காட்டுப் பகுதிக்குள் எங்கள் வீடமைந்துள்ள குடியிருப்பின் அளவு {LAND_EXTENT_HABITATION} ஆகும்.\n"
                "நாங்கள் சுயமாகப் பயிரிட்டு விவசாயம் செய்யும் நிலத்தின் பரப்பளவு {LAND_EXTENT_SELF_CULTIVATION} என அளவிடப்பட்டுள்ளது.\n"
                "வனக் கிராம எல்லைக்குள் உள்ள எங்கள் நிலத்தின் அளவு {LAND_EXTENT_FOREST_VILLAGE} என்று பதிவு செய்யப்பட்டுள்ளது.\n\n"

                "இந்த நிலம் தொடர்பாக உள்ள எந்தவொரு சர்ச்சையும் {DISPUTED_LAND_DESCRIPTION} என ஆவணப்படுத்தப்பட்டுள்ளது.\n"
                "பழைய ஆவணங்களான {EXISTING_PATTAS_LEASES_GRANTS} ஆகியவையும் இத்துடன் சரிபார்ப்பிற்காக உள்ளன.\n"
                "மறுவாழ்வு நிலம் {REHABILITATION_LAND} மற்றும் இழப்பீடின்றி கையகப்படுத்தப்பட்ட நிலம் {DISPLACED_FROM_LAND} குறித்தும் கோருகிறேன்.\n"
                "வனச் சட்டத்தின் கீழ் பாதுகாக்கப்படும் இதர பாரம்பரிய உரிமைகள் {OTHER_TRADITIONAL_RIGHT} எங்களுக்கும் பொருந்தும்.\n"
                "இதற்கான ஆதாரமாக {EVIDENCE_ITEM} மற்றும் கூடுதல் தகவலாக {OTHER_INFORMATION} ஆகியவற்றை இணைத்துள்ளேன்."
            ),
            #variation 4
            (
                "உறுதிமொழிப் பத்திரம் மற்றும் சட்டப்பூர்வ உரிமைகோரல் பிரகடனம்.\n"
                "நான், {CLAIMANT_NAME} (தந்தை/தாய்: {FATHER_MOTHER_NAME}, சட்டப்பூர்வத் துணைவர்: {SPOUSE_NAME}) ஆகிய நான், கீழ்க்கண்டவாறு சத்தியப்பிரமாணம் செய்து கொள்கிறேன்.\n"
                "எனது சட்டப்பூர்வமான நிரந்தர முகவரி {ADDRESS_FULL} என ஆவணப்படுத்தப்பட்டுள்ளது.\n"
                "இந்த நிலப்பகுதி {STATE} மாநிலம், {DISTRICT} மாவட்டம், மற்றும் {TEHSIL_TALUKA} தாலுகா அதிகார வரம்பிற்கு உட்பட்டதாகும்.\n"
                "மேலும், இது {VILLAGE} கிராம வருவாய் எல்லைக்குள், {GRAM_PANCHAYAT} கிராம பஞ்சாயத்து மற்றும் {GRAM_SABHA} கிராம சபையின் சட்ட அதிகாரத்திற்கு உட்பட்டது.\n\n"

                "பிரிவு 3(1)(a)-ன் கீழான நில ஆக்கிரமிப்பு மற்றும் சமூக வகைப்பாட்டுக்கான பிரகடனம்.\n"
                "நான் {CATEGORY_SCHEDULED_TRIBE} அல்லது {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} என்ற சட்டப்பூர்வப் பிரிவின் கீழ் வருகிறேன் என்பதைச் சான்றளிக்கிறேன்.\n"
                "எனது சட்டப்பூர்வ வாரிசு மற்றும் குடும்ப உறுப்பினரான {FAMILY_MEMBER_NAME} (வயது {FAMILY_MEMBER_AGE}), மற்றும் சார்ந்திருக்கும் நபரான {DEPENDENT_NAME} ஆகியோர் இந்த உரிமைகோரலின் பயனாளிகள் ஆவர்.\n"
                "சட்டத்தின் விதிகளுக்கு உட்பட்டு, வசிப்பிட நோக்கத்திற்காக ஆக்கிரமிக்கப்பட்டுள்ள நிலத்தின் பரப்பளவு {LAND_EXTENT_HABITATION} ஆக அளவிடப்பட்டுள்ளது.\n"
                "சுய-சாகுபடி அல்லது விவசாயப் பயன்பாட்டிற்கான நிலத்தின் பரப்பளவு {LAND_EXTENT_SELF_CULTIVATION} என நில அளவை செய்யப்பட்டுள்ளது.\n"
                "பிரிவு 3(1)(h)-ன் கீழ் வன கிராமங்களில் அமைந்துள்ள நிலத்தின் அளவு {LAND_EXTENT_FOREST_VILLAGE} என ஆவணங்களில் பதியப்பட்டுள்ளது.\n\n"

                "நிலுவையில் உள்ள தாவாக்கள், குத்தகைகள் மற்றும் இதர சட்ட உரிமைகளுக்கான அறிக்கை.\n"
                "பிரிவு 3(1)(f)-ன் கீழ் இந்த நிலம் தொடர்பான விவாதங்கள் அல்லது வழக்குகள் {DISPUTED_LAND_DESCRIPTION} எனத் தெரிவிக்கப்படுகிறது.\n"
                "முந்தைய அரசுகளால் அல்லது துறைகளால் வழங்கப்பட்ட பட்டாக்கள் அல்லது குத்தகைகளின் விவரம்: {EXISTING_PATTAS_LEASES_GRANTS}.\n"
                "பிரிவு 3(1)(m)-ன் கீழ் கோரப்படும் மாற்று நிலம் அல்லது இடத்திலமைந்த மறுவாழ்வு நிலம் {REHABILITATION_LAND} குறித்த விவரங்களும் சமர்ப்பிக்கப்பட்டுள்ளன.\n"
                "சட்டப்பிரிவு 4(8)-ன் கீழ் எவ்வித இழப்பீடும் இன்றி வெளியேற்றப்பட்ட நிலத்தின் விவரம் {DISPLACED_FROM_LAND} என்பதாகும்.\n"
                "பிரிவு 3(1)(l)-ன் கீழான இதர மரபுவழி உரிமைகள் {OTHER_TRADITIONAL_RIGHT} மற்றும் சட்டப்பூர்வமான சான்றுகள் {EVIDENCE_ITEM}, கூடுதல் தகவல்கள் {OTHER_INFORMATION} ஆகியவை இந்த உறுதிமொழிப் பத்திரத்துடன் இணைக்கப்பட்டுள்ளன."
            )


        ],
        
        DOC_CLAIM_COMMUNITY_RIGHTS: [
            # Variation 1: Bureaucratic / Form Style
            (
                "படிவம் - B [விதி 11(1)(a) மற்றும் (4) பார்க்க]\n"
                "சமூக வன உரிமைகளுக்கான முறையான கோரிக்கை மற்றும் கிராம சபையின் தீர்மானம்.\n"
                "இந்த விண்ணப்பம் {VILLAGE} கிராமம், {GRAM_PANCHAYAT} பஞ்சாயத்து சார்பாக சமர்ப்பிக்கப்படுகிறது.\n"
                "இது {STATE} மாநிலம், {DISTRICT} மாவட்டம், {TEHSIL_TALUKA} தாலுகாவிற்கு உட்பட்ட {GRAM_SABHA} கிராம சபையால் அங்கீகரிக்கப்பட்டுள்ளது.\n"
                "நாங்கள் {COMMUNITY_TYPE_FDST} அல்லது {COMMUNITY_TYPE_OTFD} சமூகத்தைச் சேர்ந்த பாரம்பரிய வனவாசி மக்கள் ஆவோம்.\n\n"

                "சமூகமாக நாங்கள் அனுபவிக்கும் வன உரிமைகளின் தன்மைகள் பின்வருமாறு ஆவணப்படுத்தப்பட்டுள்ளன.\n"
                "சமூக பயன்பாட்டிற்கான நிஸ்தார் உரிமைகள்: {COMMUNITY_RIGHT_NISTAR}.\n"
                "சிறு வனப் பொருட்களைச் சேகரிக்கும் உரிமை: {RIGHT_MINOR_FOREST_PRODUCE}.\n"
                "நீர்நிலைகள் மற்றும் மீன்பிடித்தல் போன்ற வளங்களைப் பயன்படுத்தும் உரிமை: {COMMUNITY_RIGHT_RESOURCE_USE}.\n"
                "கால்நடைகளை மேய்ப்பதற்கான உரிமை: {COMMUNITY_RIGHT_GRAZING}.\n"
                "நாடோடி மற்றும் மேய்ச்சல் சமூகங்களுக்கான பாரம்பரிய வள அணுகல்: {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS}.\n\n"

                "ஆதிவாசி மற்றும் விவசாயத்திற்கு முந்தைய சமூகங்களுக்கான வாழ்விட உரிமைகள் {COMMUNITY_TENURE_HABITAT} என உறுதி செய்யப்படுகிறது.\n"
                "பல்லுயிர் வளம், அறிவுசார் சொத்து மற்றும் பாரம்பரிய அறிவை அணுகும் உரிமை {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} ஆகும்.\n"
                "சட்டத்தின் கீழ் வரையறுக்கப்பட்ட மற்ற பாரம்பரிய உரிமைகள் {OTHER_TRADITIONAL_RIGHT} எங்களது வாழ்வாதாரமாகும்.\n"
                "இந்தக் கோரிக்கைகளை நிரூபிப்பதற்கான முக்கிய ஆதாரங்கள்: {EVIDENCE_ITEM}.\n"
                "பரிசீலனைக்குத் தேவையான இதர தகவல்கள் {OTHER_INFORMATION} என இத்துடன் இணைக்கப்பட்டுள்ளன."
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "சமூகக் காடு வளர்ப்பு மற்றும் பாரம்பரிய உரிமைகளைப் பாதுகாப்பதற்கான கிராம சபையின் கூட்டு விண்ணப்பம்.\n"
                "எங்கள் {GRAM_SABHA} கிராம சபையானது, {VILLAGE} கிராம மக்கள் சார்பாக இந்தக் கோரிக்கையை முன்வைக்கிறது.\n"
                "எங்கள் பகுதி {STATE} மாநிலத்தின் {DISTRICT} மாவட்டத்தில் உள்ள {TEHSIL_TALUKA} தாலுகாவிலும், {GRAM_PANCHAYAT} பஞ்சாயத்திலும் அமைந்துள்ளது.\n"
                "எங்கள் சமூகத்தின் வகைப்பாடு {COMMUNITY_TYPE_FDST} அல்லது {COMMUNITY_TYPE_OTFD} என அரசாங்கத்தால் அங்கீகரிக்கப்பட்டுள்ளது.\n"
                "காட்டு வளங்களோடு ஒன்றிய வாழ்க்கை முறையை நாங்கள் பல தலைமுறைகளாகப் பின்பற்றி வருகிறோம்.\n\n"

                "எங்கள் அன்றாட வாழ்க்கைக்காகவும், வாழ்வாதாரத்திற்காகவும் பல்வேறு உரிமைகளை நாங்கள் சார்ந்திருக்கிறோம்.\n"
                "எங்கள் சமூக நிஸ்தார் உரிமைகள் {COMMUNITY_RIGHT_NISTAR} என தெளிவாக வரையறுக்கப்பட்டுள்ளன.\n"
                "தேன், மூலிகைகள் போன்ற சிறு வனப் பொருட்களைப் பெறுவதற்கான உரிமை {RIGHT_MINOR_FOREST_PRODUCE} ஆகும்.\n"
                "மீன்பிடித்தல் உள்ளிட்ட நீர் ஆதாரங்களைப் பயன்படுத்துவதற்கான உரிமை {COMMUNITY_RIGHT_RESOURCE_USE} ஆகும்.\n"
                "எங்கள் கால்நடைகளுக்கான மேய்ச்சல் உரிமை {COMMUNITY_RIGHT_GRAZING} எனப் பாதுகாக்கப்படுகிறது.\n"
                "இடம்பெயரும் நாடோடி மக்களுக்கான வள அணுகல் உரிமை {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS} என வழங்கப்பட்டுள்ளது.\n\n"

                "ஆதிவாசிகளின் தொன்மையான வாழ்விடங்களைப் பாதுகாக்கும் {COMMUNITY_TENURE_HABITAT} உரிமை எங்களுக்கு மிகவும் அவசியமானது.\n"
                "பாரம்பரிய அறிவு மற்றும் பல்லுயிர் பெருக்கத்தைப் பாதுகாக்கும் உரிமை {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} எனக் கோரப்படுகிறது.\n"
                "எங்கள் முன்னோர்கள் விட்டுச்சென்ற மற்ற பாரம்பரிய உரிமைகள் {OTHER_TRADITIONAL_RIGHT} ஆகத் தொடர்கின்றன.\n"
                "இந்த உரிமைகளை உறுதிசெய்யும் வகையில் {EVIDENCE_ITEM} போன்ற பழமையான ஆவணங்கள் சமர்ப்பிக்கப்பட்டுள்ளன.\n"
                "கூடுதல் பரிசீலனைக்காக {OTHER_INFORMATION} உள்ளிட்ட விவரங்களும் இத்துடன் வழங்கப்பட்டுள்ளன."
            ),
            # Variation 3: Formal Letter Style
            (
                "பொருள்: சமூக வன உரிமைகளை அங்கீகரிப்பதற்கான கூட்டு விண்ணப்பம் சமர்ப்பித்தல்.\n"
                "நாங்கள் {STATE} மாநிலம், {DISTRICT} மாவட்டம், {TEHSIL_TALUKA} தாலுகாவிற்கு உட்பட்ட மக்கள்.\n"
                "எங்கள் வசிப்பிடம் {VILLAGE} கிராமம் மற்றும் {GRAM_PANCHAYAT} பஞ்சாயத்திற்கு உட்பட்டது.\n"
                "இந்தக் கடிதம் {GRAM_SABHA} கிராம சபையின் முழுமையான ஒப்புதலுடன் எழுதப்படுகிறது.\n"
                "நாங்கள் {COMMUNITY_TYPE_FDST} மற்றும் {COMMUNITY_TYPE_OTFD} சமூகத்தைச் சேர்ந்த பழங்குடியினர் ஆவோம்.\n\n"

                "வன உரிமைச் சட்டம் 2006-ன் படி, எங்கள் சமூகத்திற்குப் பின்வரும் உரிமைகள் வழங்கப்பட வேண்டும் எனக் கோருகிறோம்.\n"
                "நிஸ்தார் போன்ற பொது உரிமைகள்: {COMMUNITY_RIGHT_NISTAR}. சிறு வன மகசூல் உரிமை: {RIGHT_MINOR_FOREST_PRODUCE}.\n"
                "வளங்களைப் பயன்படுத்துவதற்கான உரிமை: {COMMUNITY_RIGHT_RESOURCE_USE}.\n"
                "விலங்குகளை மேய்க்கும் உரிமை: {COMMUNITY_RIGHT_GRAZING}.\n"
                "நாடோடி சமூகங்களின் பாரம்பரிய அணுகல் உரிமை: {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS}.\n\n"

                "எங்கள் குடியிருப்புகளுக்கான சமூகப் பதவிக்கால உரிமை {COMMUNITY_TENURE_HABITAT} உறுதி செய்யப்பட வேண்டும்.\n"
                "எங்கள் பல்லுயிர் மற்றும் பாரம்பரிய அறிவுக்கான உரிமை {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} ஆகும்.\n"
                "பிற பாரம்பரிய உரிமைகளான {OTHER_TRADITIONAL_RIGHT} எங்களின் வாழ்வாதாரத்திற்கு அடிப்படையாகும்.\n"
                "இக்கோரிக்கையை ஆதரிக்கும் சான்றுகளாக ஆவணங்கள் {EVIDENCE_ITEM} இணைக்கப்பட்டுள்ளன.\n"
                "மேலும் இதர தகவல்கள் {OTHER_INFORMATION} அதிகாரிகளின் கவனத்திற்குக் கொண்டுவரப்படுகிறது."
            ),
            #variation 4
            (
                "சமூக வன உரிமைகளுக்கான (Community Forest Rights) சட்டப்பூர்வ கோரிக்கை அறிக்கை.\n"
                "{STATE} மாநிலம், {DISTRICT} மாவட்டம், மற்றும் {TEHSIL_TALUKA} தாலுகாவிற்கு உட்பட்ட அதிகார வரம்பில் இந்தக் கோரிக்கை பதிவு செய்யப்படுகிறது.\n"
                "இக்கோரிக்கையானது {VILLAGE} கிராம மக்களின் சார்பில், {GRAM_PANCHAYAT} கிராம பஞ்சாயத்து மற்றும் {GRAM_SABHA} கிராம சபையின் அதிகாரப்பூர்வ தீர்மானத்தின் அடிப்படையில் சமர்ப்பிக்கப்படுகிறது.\n"
                "இந்தச் சமூகமானது வன உரிமைச் சட்டம் 2006-ன் கீழ் {COMMUNITY_TYPE_FDST} அல்லது {COMMUNITY_TYPE_OTFD} எனச் சட்டப்பூர்வமாக வரையறுக்கப்பட்டுள்ளது.\n"
                "இந்தச் சமூகத்தின் ஒட்டுமொத்தப் பாரம்பரிய உரிமைகளை நிலைநாட்டும் வகையில் இந்த ஆவணம் தயார் செய்யப்பட்டுள்ளது.\n\n"

                "பிரிவு 3-ன் கீழ் வரையறுக்கப்பட்ட சமூகப் பயன்பாடு மற்றும் வளங்கள் மீதான உரிமைகளின் பட்டியல்.\n"
                "சட்டப்பிரிவு 3(1)(b)-ன் கீழ் நிஸ்தார் (Nistar) அல்லது அது போன்ற சமூக உரிமைகள் {COMMUNITY_RIGHT_NISTAR} எனப் பிரகடனப்படுத்தப்படுகிறது.\n"
                "பிரிவு 3(1)(c)-ன் கீழ் சிறு வனப் பொருட்களை (MFP) சேகரிக்கும் மற்றும் விற்கும் உரிமை {RIGHT_MINOR_FOREST_PRODUCE} என உறுதி செய்யப்பட்டுள்ளது.\n"
                "நீர்நிலைகள், மீன்பிடித்தல் உள்ளிட்ட வளங்களைப் பயன்படுத்துவதற்கான உரிமை {COMMUNITY_RIGHT_RESOURCE_USE} ஆக வரையறுக்கப்பட்டுள்ளது.\n"
                "கால்நடை மேய்ச்சலுக்கான பாரம்பரிய உரிமை {COMMUNITY_RIGHT_GRAZING} என ஆவணப்படுத்தப்பட்டுள்ளது.\n"
                "நாடோடி மற்றும் மேய்ச்சல் சமூகங்களுக்கான வளங்களுக்கான சட்டப்பூர்வ அணுகல் {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS} என உறுதி செய்யப்படுகிறது.\n\n"

                "பழங்குடியினரின் வாழிட உரிமைகள், அறிவுசார் சொத்துரிமை மற்றும் சமர்ப்பிக்கப்பட்ட சான்றுகள்.\n"
                "குறிப்பாக பாதிக்கப்படக்கூடிய பழங்குடியினர் (PTG) மற்றும் வேளாண்மைக்கு முந்தைய சமூகங்களுக்கான வாழிட உரிமை {COMMUNITY_TENURE_HABITAT} எனக் கோரப்படுகிறது.\n"
                "பிரிவு 3(1)(k)-ன் கீழ் பல்லுயிர் வளம், பாரம்பரிய அறிவு மற்றும் அறிவுசார் சொத்துரிமைக்கான அணுகல் {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} எனப் பதிவு செய்யப்பட்டுள்ளது.\n"
                "அச்சட்டத்தின் கீழ் அங்கீகரிக்கப்பட்ட இதர சமூக மற்றும் பாரம்பரிய உரிமைகள் {OTHER_TRADITIONAL_RIGHT} எங்களின் অবিচ্ছেদ্য உரிமையாகும்.\n"
                "மேற்கண்ட அனைத்துச் சட்டப்பூர்வக் கோரிக்கைகளையும் மெய்ப்பிக்கும் வகையிலான சான்றுகள் {EVIDENCE_ITEM} இத்துடன் இணைக்கப்பட்டுள்ளன.\n"
                "அரசு அதிகாரிகளின் சட்டப்பூர்வ ஆய்வுக்குத் தேவையான இதர தரவுகள் {OTHER_INFORMATION} அதிகாரப்பூர்வமாக முன்வைக்கப்படுகின்றன."
            )
        ],

        DOC_CLAIM_COMMUNITY_FOREST_RESOURCE: [
            # Variation 1: Bureaucratic / Form Style
            (
                "படிவம் - C [சட்டத்தின் பிரிவு 3(1) (i) மற்றும் விதி 11(1) பார்க்க]\n"
                "சமூக வன வளங்களுக்கான (CFR) உரிமைகோரல் படிவம்.\n"
                "இந்தக் கோரிக்கையானது {STATE} மாநிலம், {DISTRICT} மாவட்டம், {TEHSIL_TALUKA} தாலுகாவிற்கு உட்பட்டது.\n"
                "{GRAM_PANCHAYAT} கிராம பஞ்சாயத்தைச் சேர்ந்த {VILLAGE} கிராம மக்களின் சார்பில் இது சமர்ப்பிக்கப்படுகிறது.\n"
                "இந்தத் தீர்மானம் {GRAM_SABHA} கிராம சபையின் கூட்டத்தில் நிறைவேற்றப்பட்டது.\n\n"

                "இந்தக் கோரிக்கையை முன்வைக்கும் கிராம சபையின் முக்கிய உறுப்பினர் {GRAM_SABHA_MEMBER_NAME} ஆவார்.\n"
                "இவர்கள் {CATEGORY_SCHEDULED_TRIBE} அல்லது {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} சமூகத்தைச் சேர்ந்தவர்கள் ஆவர்.\n"
                "நாங்கள் கோரும் வன வளப் பகுதியின் கசரா அல்லது கம்பார்ட்மென்ட் எண் {KHASRA_COMPARTMENT_NUMBER} ஆகும்.\n"
                "எங்கள் வனப் பகுதியை ஒட்டியுள்ள எல்லைக் கிராமங்கள்: {BORDERING_VILLAGE}.\n"
                "இந்தப் பகுதியின் புவியியல் எல்லைகள் {BOUNDARY_DESCRIPTION} எனத் தெளிவாக வரையறுக்கப்பட்டுள்ளன.\n\n"

                "இந்த நிலப்பரப்பை எங்கள் சமூகம் பல தலைமுறைகளாகப் பாதுகாத்து, மீளுருவாக்கம் செய்து வருகிறது.\n"
                "இதற்கான முறையான சமூக வன வள ஆதாரங்களின் பட்டியல் {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} இணைக்கப்பட்டுள்ளது.\n"
                "எங்கள் பாரம்பரியப் பயன்பாட்டை நிரூபிக்கும் இதர சான்றுகள் {EVIDENCE_ITEM} ஆகச் சமர்ப்பிக்கப்பட்டுள்ளன.\n"
                "இந்த வன வளங்களை நிலையான முறையில் பயன்படுத்தும் உரிமை கிராம சபைக்கு உள்ளது என்பதை உறுதிப்படுத்துகிறோம்.\n"
                "உரிய அதிகாரிகள் இதைப் பரிசீலித்து, சமூக வன வள உரிமையை அங்கீகரிக்கக் கேட்டுக்கொள்கிறோம்."
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "சமூக வன வளங்களை நிர்வகிப்பதற்கான கிராம சபையின் கூட்டுப் பிரகடனம்.\n"
                "நாங்கள், {STATE} மாநிலத்தின் {DISTRICT} மாவட்டத்தில் உள்ள {TEHSIL_TALUKA} தாலுகாவில் வசிக்கிறோம்.\n"
                "எங்கள் {VILLAGE} கிராமமானது, {GRAM_PANCHAYAT} கிராம பஞ்சாயத்தின் நிர்வாகத்தின் கீழ் வருகிறது.\n"
                "இன்று {GRAM_SABHA} கிராம சபையில் ஒன்று கூடி, எங்கள் பாரம்பரிய வன வள உரிமைக்கான பிரகடனத்தை வெளியிடுகிறோம்.\n"
                "இந்தக் கூட்டத்தில் முன்னிலை வகிக்கும் உறுப்பினர் {GRAM_SABHA_MEMBER_NAME} ஆவர்.\n\n"

                "நாங்கள் அனைவரும் பழங்குடியினர் வகையான {CATEGORY_SCHEDULED_TRIBE} அல்லது {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} சமூகத்தவர் ஆவோம்.\n"
                "நாங்கள் நிர்வகிக்கும் காட்டுப் பகுதியின் கசரா/கம்பார்ட்மென்ட் எண்கள் {KHASRA_COMPARTMENT_NUMBER} எனப் பதிவு செய்யப்பட்டுள்ளன.\n"
                "எங்கள் வனப்பகுதியைச் சுற்றியுள்ள அண்டை கிராமங்கள் {BORDERING_VILLAGE} என ஆவணப்படுத்தப்பட்டுள்ளன.\n"
                "வடக்கே மலை, தெற்கே ஆறு எனப் பரவியுள்ள எங்கள் நிலத்தின் எல்லைகள் {BOUNDARY_DESCRIPTION} என்று விளக்கப்பட்டுள்ளன.\n"
                "இந்த எல்லைக்குள் உள்ள அனைத்து வளங்களையும் பாதுகாக்கும் உரிமை எங்களுக்கு உண்டு.\n\n"

                "பல்லுயிர் பெருக்கத்தைப் பேணுவதற்கும், காட்டை அழிவில் இருந்து காப்பதற்கும் நாங்கள் உறுதிபூண்டுள்ளோம்.\n"
                "எங்கள் உரிமையை நிலைநாட்டத் தேவையான ஆவணப் பட்டியல் {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} தயாரிக்கப்பட்டுள்ளது.\n"
                "மேலும், வாய்மொழி மற்றும் வரலாற்றுச் சான்றுகளாக {EVIDENCE_ITEM} முன்வைக்கப்படுகின்றன.\n"
                "இந்த ஆதாரங்களின் அடிப்படையில், சமூக வன வள உரிமை (CFR) எங்களுக்கு உடனடியாக வழங்கப்பட வேண்டும்.\n"
                "இதை அரசு அதிகாரிகள் விரைவாகப் பரிசீலித்து ஆணை வெளியிடுமாறு கேட்டுக்கொள்கிறோம்."
            ),
            # Variation 3: Formal Letter Style
            (
                "பொருள்: பிரிவு 3(1)(i)-ன் கீழ் சமூக வன வளங்களுக்கான உரிமை கோருதல்.\n"
                "பகுதி விவரங்கள்: தாலுகா {TEHSIL_TALUKA}, மாவட்டம் {DISTRICT}, மாநிலம் {STATE}.\n"
                "கிராமம்: {VILLAGE}, பஞ்சாயத்து: {GRAM_PANCHAYAT}, கிராம சபை: {GRAM_SABHA}.\n"
                "கிராம சபை உறுப்பினர் {GRAM_SABHA_MEMBER_NAME} அவர்களின் தலைமையில் இந்தக் கோரிக்கை முன்வைக்கப்படுகிறது.\n"
                "விண்ணப்பதாரர்கள் {CATEGORY_SCHEDULED_TRIBE} மற்றும் {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} என்ற பிரிவைச் சேர்ந்தவர்கள்.\n\n"

                "நாங்கள் பாதுகாத்து வரும் காட்டுப் பகுதிக்கான கசரா எண்கள் {KHASRA_COMPARTMENT_NUMBER} ஆகும்.\n"
                "எங்கள் எல்லைக்குட்பட்ட பகுதியைச் சுற்றி {BORDERING_VILLAGE} போன்ற எல்லையோர கிராமங்கள் அமைந்துள்ளன.\n"
                "எங்கள் சமூக வன வளங்களின் நிலவியல் எல்லைகள் {BOUNDARY_DESCRIPTION} எனத் தெளிவாக வரைபடமாகக் குறிக்கப்பட்டுள்ளன.\n"
                "இந்தப் பகுதியின் சுற்றுச்சூழல் சமநிலையைப் பேணுவது எங்கள் சமூகத்தின் தலையாய கடமையாகும்.\n"
                "எனவே, இந்த வன வளங்களை நிர்வகிக்கும் முழு உரிமையும் எங்கள் கிராம சபைக்கு வழங்கப்பட வேண்டும்.\n\n"

                "இந்த நிலத்தின் மீதான எங்கள் பாரம்பரியத் தொடர்பை நிரூபிக்கும் சான்றுகள் தொகுக்கப்பட்டுள்ளன.\n"
                "முக்கிய ஆவணங்களின் பட்டியல் {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} அதிகாரப்பூர்வமாகச் சமர்ப்பிக்கப்படுகிறது.\n"
                "இதர உறுதியான ஆதாரங்களாக {EVIDENCE_ITEM} ஆவணங்களும் இந்த விண்ணப்பத்துடன் இணைக்கப்பட்டுள்ளன.\n"
                "இந்த ஆதாரங்கள் அனைத்தும் எங்கள் கோரிக்கையின் நியாயத்தை உறுதிப்படுத்துகின்றன.\n"
                "இதன் அடிப்படையில் எங்களின் சமூக வன வள உரிமையை அரசு அங்கீகரிக்க வேண்டும்."
            ),
            #variation 4
            (
                "சமூக வன வளங்கள் (Community Forest Resource) மீதான உரிமைகோரலுக்கான சட்டப்பூர்வப் பிரகடனம்.\n"
                "வன உரிமைச் சட்டம் 2006, பிரிவு 3(1)(i)-ன் கீழ், {STATE} மாநிலம், {DISTRICT} மாவட்டம், {TEHSIL_TALUKA} தாலுகா அதிகாரிகளுக்குச் சமர்ப்பிக்கப்படும் ஆவணம்.\n"
                "இந்த அதிகாரப்பூர்வக் கோரிக்கையானது {VILLAGE} கிராம மக்களின் சார்பில், {GRAM_PANCHAYAT} கிராம பஞ்சாயத்து மற்றும் {GRAM_SABHA} கிராம சபை மூலமாக முன்வைக்கப்படுகிறது.\n"
                "சட்டப்பூர்வப் பிரதிநிதியாகச் செயல்படும் கிராம சபை உறுப்பினர் {GRAM_SABHA_MEMBER_NAME} இக்கோரிக்கையில் கையொப்பமிடுகிறார்.\n"
                "இக்கோரிக்கையில் பங்கேற்கும் உறுப்பினர்கள் {CATEGORY_SCHEDULED_TRIBE} அல்லது {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} என்ற சட்டப் பிரிவின் கீழ் பாதுகாக்கப்பட்டவர்கள் ஆவர்.\n\n"

                "கோரப்படும் வன வளப் பகுதியின் புவியியல், நில அளவை மற்றும் எல்லைப்புற ஆவணங்கள்.\n"
                "உரிமை கோரப்படும் வனப்பகுதியின் சட்டப்பூர்வ கசரா (Khasra) அல்லது வனத்துறை கம்பார்ட்மென்ட் எண் {KHASRA_COMPARTMENT_NUMBER} எனப் பதிவேடுகளில் உள்ளது.\n"
                "இந்தப் பகுதியோடு சட்டப்பூர்வமாக எல்லையைப் பகிர்ந்து கொள்ளும் அண்டை கிராமங்கள் {BORDERING_VILLAGE} என வருவாய்த்துறை வரைபடத்தில் சுட்டிக்காட்டப்பட்டுள்ளது.\n"
                "கோரப்படும் ஒட்டுமொத்த வன வளப் பகுதியின் புவியியல் மற்றும் நிலவியல் எல்லைகள் {BOUNDARY_DESCRIPTION} என்று மிகத் துல்லியமாக வரையறுக்கப்பட்டுள்ளன.\n"
                "இந்த எல்லைகளுக்கு உட்பட்ட வன வளங்களை நிலையான முறையில் பயன்படுத்தும் மரபுவழி அதிகாரத்தை இச்சமூகம் பெற்றுள்ளது.\n"
                "இந்தப் பகுதியில் உள்ள வளங்களை மீளுருவாக்கம் செய்யும் பொறுப்பும் அதிகாரமும் கிராம சபையிடம் சட்டப்பூர்வமாக ஒப்படைக்கப்பட வேண்டும்.\n\n"

                "ஆதார ஆவணங்களின் சமர்ப்பணம் மற்றும் சட்டப்பூர்வக் கோரிக்கையின் உறுதிப்படுத்தல்.\n"
                "இச்சமூகத்தின் பாரம்பரியத் தொடர்பை நிரூபிக்கும் வகையில், அதிகாரப்பூர்வ ஆவணங்களின் பட்டியல் {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} இத்துடன் சமர்ப்பிக்கப்பட்டுள்ளது.\n"
                "மேலும், வாய்மொழித் தொன்மங்கள், கிராமப் பதிவேடுகள் போன்ற இதர உறுதிப்படுத்தும் ஆதாரங்கள் {EVIDENCE_ITEM} ஆக இணைக்கப்பட்டுள்ளன.\n"
                "இந்த ஆவணங்கள் அனைத்தும் சட்டத்தின் 13-வது விதியின் கீழ் ஏற்றுக்கொள்ளத்தக்க சான்றுகளாகப் பிரகடனப்படுத்தப்படுகின்றன.\n"
                "இந்த ஆதாரங்களின் அடிப்படையில், இப்பகுதியைப் பாதுகாக்கும் ஒட்டுமொத்த அதிகாரமும் கிராம சபைக்குச் சட்டப்பூர்வமாக வழங்கப்பட வேண்டும்.\n"
                "இக்கோரிக்கையைச் சட்ட விதிகளின்படி விரைவாகப் பரிசீலித்து அரசாணை வெளியிடுமாறு கேட்டுக்கொள்ளப்படுகிறது."
            )
        ],

        DOC_TITLE_UNDER_OCCUPATION: [
            # Variation 1: Bureaucratic / Form Style
            (
                "அனுபந்தம் - II [விதி 8(h) பார்க்க]\n"
                "ஆக்கிரமிப்பின் கீழ் உள்ள காட்டு நிலத்திற்கான அதிகாரப்பூர்வப் பட்டா / உரிமை ஆவணம்.\n"
                "இந்த நில உரிமைக்கான பட்டா {TITLE_HOLDER_NAME} அவர்களுக்கு அரசல் வழங்கப்படுகிறது.\n"
                "பட்டாதாரரின் தந்தை/தாயின் பெயர் {FATHER_MOTHER_NAME} மற்றும் கணவன்/மனைவியின் பெயர் {SPOUSE_NAME} ஆகும்.\n"
                "இவரைச் சார்ந்து வாழும் நபரான {DEPENDENT_NAME} என்பவரும் இந்த உரிமையின் கீழ் பாதுகாக்கப்படுகிறார்.\n\n"

                "பட்டாதாரரின் முழுமையான பதிவு செய்யப்பட்ட முகவரி {TITLE_ADDRESS_FULL} ஆகும்.\n"
                "இந்த நிலம் {VILLAGE} கிராமம் மற்றும் {GRAM_PANCHAYAT} கிராம பஞ்சாயத்திற்கு உட்பட்ட பகுதியாகும்.\n"
                "இது {GRAM_SABHA} கிராம சபையின் எல்லைக்குள், {TEHSIL_TALUKA} தாலுகாவில் அமைந்துள்ளது.\n"
                "இந்த மாவட்டம் {DISTRICT} மற்றும் மாநிலம் {STATE} ஆகியவற்றின் அதிகார வரம்பிற்கு உட்பட்டது.\n"
                "பட்டாதாரர் {CATEGORY_SCHEDULED_TRIBE} அல்லது {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} வகுப்பைச் சேர்ந்தவர் எனச் சான்றளிக்கப்படுகிறது.\n\n"

                "இந்த ஆவணத்தின் மூலம் உரிமையளிக்கப்படும் காட்டு நிலத்தின் மொத்தப் பரப்பளவு {TITLE_LAND_AREA_MEASURE} ஆகும்.\n"
                "நிலத்தின் கசரா அல்லது கம்பார்ட்மென்ட் எண் {KHASRA_COMPARTMENT_NUMBER} என நில ஆவணங்களில் பதிவு செய்யப்பட்டுள்ளது.\n"
                "நிலத்தின் நான்கு புற எல்லைகளும் {BOUNDARY_DESCRIPTION} என்ற புவியியல் அடையாளங்கள் மூலம் விவரிக்கப்பட்டுள்ளன.\n"
                "இந்த உரிமையானது பரம்பரை பரம்பரையாக அனுபவிக்கக்கூடியது, ஆனால் விற்கவோ மாற்றவோ முடியாதது.\n"
                "மாவட்ட ஆட்சியர் மற்றும் மாவட்ட வன அலுவலர் ஆகியோரின் கையொப்பத்துடன் இது அதிகாரப்பூர்வமாக வழங்கப்படுகிறது."
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "பழங்குடியினர் விவகார அமைச்சகத்தால் வழங்கப்படும் தனிநபர் நில உரிமைப் பட்டா.\n"
                "திரு/திருமதி {TITLE_HOLDER_NAME} (தந்தை/தாய்: {FATHER_MOTHER_NAME}, துணைவர்: {SPOUSE_NAME}) என்பவருக்கு இது வழங்கப்படுகிறது.\n"
                "அவரை நம்பி வாழும் {DEPENDENT_NAME} போன்ற குடும்ப உறுப்பினர்களுக்கும் இந்த நிலத்தில் உரிமை உண்டு.\n"
                "இவர்களது வசிப்பிட முகவரி {TITLE_ADDRESS_FULL} என அரசுப் பதிவேடுகளில் முறையாகப் பதிவு செய்யப்பட்டுள்ளது.\n"
                "இது {STATE} மாநிலத்தின் {DISTRICT} மாவட்டத்தில் உள்ள {TEHSIL_TALUKA} தாலுகாவிற்கு உட்பட்டது.\n\n"

                "இந்த இடம் {VILLAGE} கிராமத்தில், {GRAM_PANCHAYAT} பஞ்சாயத்தின் கீழ், {GRAM_SABHA} கிராம சபையின் கட்டுப்பாட்டில் உள்ளது.\n"
                "பயனாளியானவர் பழங்குடியினர் வகையான {CATEGORY_SCHEDULED_TRIBE} அல்லது {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} பிரிவைச் சார்ந்தவர் ஆவார்.\n"
                "அரசாங்கம் இவருக்கு விவசாயம் மற்றும் வசிப்பிடத்திற்காக {TITLE_LAND_AREA_MEASURE} அளவுள்ள நிலத்தை ஒதுக்கியுள்ளது.\n"
                "அந்த நிலத்தின் கசரா (Khasra) அல்லது அளவீட்டு எண் {KHASRA_COMPARTMENT_NUMBER} எனத் தெளிவாகக் குறிப்பிடப்பட்டுள்ளது.\n"
                "இடத்தின் துல்லியமான அமைவிடம், {BOUNDARY_DESCRIPTION} என்ற எல்லை விளக்கத்தின் மூலம் ஆவணப்படுத்தப்பட்டுள்ளது.\n\n"

                "இந்த நில உரிமைப் பட்டாவானது வன உரிமைச் சட்டம் 2006-ன் அனைத்து விதிகளுக்கும் உட்பட்டது.\n"
                "இந்த நிலத்தை உழவு செய்யவும், தலைமுறையாக அனுபவிக்கவும் மட்டுமே அதிகாரம் வழங்கப்பட்டுள்ளது.\n"
                "எக்காரணம் கொண்டும் இந்த வன நிலத்தை வேறு ஒருவருக்கு விற்கவோ, குத்தகைக்கு விடவோ கூடாது.\n"
                "மாநில அரசின் அதிகாரப்பூர்வ முத்திரையுடன் சம்பந்தப்பட்ட துறை அதிகாரிகளால் இது சான்றளிக்கப்படுகிறது.\n"
                "இந்த ஆவணம் பட்டாதாரரின் வாழ்வாதாரத்தைப் பாதுகாக்கும் சட்டப்பூர்வக் கவசமாகச் செயல்படும்."
            ),
            # Variation 3: Formal Letter Style
            (
                "காட்டு நில உரிமை ஆணை மற்றும் பட்டா சான்றிதழ்.\n"
                "உரிமையாளர் பெயர்: {TITLE_HOLDER_NAME}. பெற்றோர் பெயர்: {FATHER_MOTHER_NAME}. துணைவர்: {SPOUSE_NAME}.\n"
                "சார்ந்திருப்போர்: {DEPENDENT_NAME}. உரிமையாளர் வகை: {CATEGORY_SCHEDULED_TRIBE} / {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER}.\n"
                "முகவரி: {TITLE_ADDRESS_FULL}, கிராமம்: {VILLAGE}, பஞ்சாயத்து: {GRAM_PANCHAYAT}, கிராம சபை: {GRAM_SABHA}.\n"
                "தாலுகா: {TEHSIL_TALUKA}, மாவட்டம்: {DISTRICT}, மாநிலம்: {STATE}.\n\n"

                "வன உரிமைச் சட்டம் 2006, பிரிவு 4-ன் கீழ் இந்த நில உரிமை அதிகாரப்பூர்வமாக அங்கீகரிக்கப்படுகிறது.\n"
                "மேற்குறிப்பிட்ட பயனாளியின் அனுபவத்தில் உள்ள {TITLE_LAND_AREA_MEASURE} அளவுள்ள நிலத்திற்குப் பட்டா வழங்கப்படுகிறது.\n"
                "வருவாய்த் துறையின் பதிவேட்டின்படி, இந்த நிலத்தின் கசரா எண் {KHASRA_COMPARTMENT_NUMBER} ஆகும்.\n"
                "நிலத்தின் எல்லைகளானது {BOUNDARY_DESCRIPTION} என்ற அடையாளங்களுடன் துல்லியமாக வரையறுக்கப்பட்டுள்ளன.\n"
                "அனைத்து சரிபார்ப்புகளுக்குப் பிறகும், மாவட்ட அளவிலான குழு இந்த நில ஒதுக்கீட்டிற்கு ஒப்புதல் அளித்துள்ளது.\n\n"

                "இந்த நில உரிமை பரம்பரை உரிமையாகத் தொடரும், எனினும் நிலத்தை அந்நியப்படுத்த இயலாது.\n"
                "அரசாங்கத்தால் அவ்வப்போது விதிக்கப்படும் வனப் பாதுகாப்பு விதிகளுக்குப் பயனாளி கட்டுப்பட வேண்டும்.\n"
                "இதன் மூலம், வனவாசியின் பொருளாதார மற்றும் சமூகப் பாதுகாப்பு அரசால் உறுதி செய்யப்படுகிறது.\n"
                "இது மாநில அரசின் அங்கீகரிக்கப்பட்ட அதிகாரிகளால் கையொப்பமிடப்பட்டு முத்திரையிடப்பட்டுள்ளது.\n"
                "இந்த ஆவணம் வழங்கப்பட்ட நாள் முதல் சட்டப்பூர்வமாக நடைமுறைக்கு வருகிறது."
            ),
            #variation 4
            (
                "காட்டு நில உரிமைச் சட்டம் 2006-ன் கீழ் தனிநபருக்கு வழங்கப்படும் சட்டப்பூர்வப் பட்டா ஆவணம்.\n"
                "மாநில அரசின் சட்ட அதிகாரத்தின்படி, இந்த நில உரிமைக்கான பட்டா {TITLE_HOLDER_NAME} என்ற பயனாளியின் பெயரில் சட்டப்பூர்வமாகப் பதிவு செய்யப்படுகிறது.\n"
                "பயனாளியின் தந்தை/தாயின் பெயர் {FATHER_MOTHER_NAME} மற்றும் சட்டப்பூர்வத் துணைவரின் பெயர் {SPOUSE_NAME} என ஆவணங்களில் உறுதி செய்யப்பட்டுள்ளது.\n"
                "பயனாளியைச் சார்ந்து வாழும் சட்டப்பூர்வ வாரிசுகள் அல்லது சார்ந்திருப்போர் {DEPENDENT_NAME} ஆகியோரின் பெயர்களும் இப்பட்டாவில் இணைக்கப்பட்டுள்ளன.\n"
                "பயனாளியின் அதிகாரப்பூர்வமான வசிப்பிட முகவரி {TITLE_ADDRESS_FULL} என வருவாய்த்துறை மற்றும் வனத்துறைப் பதிவேடுகளில் பதிவு செய்யப்பட்டுள்ளது.\n"
                "இது {STATE} மாநிலம், {DISTRICT} மாவட்டம், {TEHSIL_TALUKA} தாலுகாவிற்கு உட்பட்ட {VILLAGE} கிராமம், {GRAM_PANCHAYAT} கிராம பஞ்சாயத்து மற்றும் {GRAM_SABHA} கிராம சபையின் அதிகார வரம்பிற்கு உட்பட்டதாகும்.\n\n"

                "பயனாளியின் சட்ட வகைப்பாடு, நிலத்தின் அளவீடு மற்றும் நிலவியல் எல்லைகளின் உறுதிப்படுத்தல்.\n"
                "பயனாளி, சட்டத்தின் விதிகளின்படி {CATEGORY_SCHEDULED_TRIBE} அல்லது {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} சமூகத்தைச் சேர்ந்தவர் எனச் சான்றளிக்கப்படுகிறது.\n"
                "அரசாங்கத்தால் அதிகாரப்பூர்வமாக அளவீடு செய்யப்பட்டு ஒதுக்கப்பட்ட காட்டு நிலத்தின் ஒட்டுமொத்தப் பரப்பளவு {TITLE_LAND_AREA_MEASURE} ஆகும்.\n"
                "அரசு நில ஆவணங்களில் இந்த நிலத்திற்கான கசரா (Khasra) அல்லது கம்பார்ட்மென்ட் எண் {KHASRA_COMPARTMENT_NUMBER} எனப் பதியப்பட்டுள்ளது.\n"
                "இந்த நிலத்தின் நான்கு புறமான நிலவியல் மற்றும் இயற்கை எல்லைகள் {BOUNDARY_DESCRIPTION} என்று மிகத் துல்லியமாக வரையறுக்கப்பட்டுள்ளன.\n"
                "இந்த அளவீடுகள் அனைத்தும் அரசு நில அளவையாளர் மற்றும் வனத்துறை அதிகாரிகளால் நேரடியாகச் சரிபார்க்கப்பட்டுள்ளன.\n\n"

                "உரிமையின் சட்டப்பூர்வத் தன்மை, கட்டுப்பாடுகள் மற்றும் அதிகாரிகளின் சான்றளிப்பு.\n"
                "சட்டப்பிரிவு 4(4)-ன் படி, இந்த நில உரிமையானது மரபுவழியாக அனுபவிக்கக்கூடியது, ஆனால் எக்காரணம் கொண்டும் அந்நியப்படுத்தவோ, விற்கவோ, பரிமாற்றம் செய்யவோ முடியாததாகும்.\n"
                "பயனாளி, வனப் பாதுகாப்புச் சட்டங்கள் மற்றும் சுற்றுச்சூழல் பாதுகாப்பு விதிகளுக்கு முழுமையாகக் கட்டுப்பட்டு நடக்க வேண்டும்.\n"
                "விதிமுறைகள் மீறப்பட்டால், எந்த முன்னறிவிப்புமின்றி இந்த உரிமையை ரத்து செய்ய மாநில அரசுக்கு முழு அதிகாரம் உள்ளது.\n"
                "இந்தச் சட்டப்பூர்வப் பட்டாவானது, சப்-டிவிஷனல் மற்றும் மாவட்ட அளவிலான குழுக்களின் முறையான ஒப்புதலுக்குப் பிறகே வழங்கப்படுகிறது.\n"
                "இதற்கான முறையான அங்கீகாரமாக, மாவட்ட ஆட்சியர் மற்றும் கோட்ட வன அலுவலர் ஆகியோர் இப்பட்டாவில் அதிகாரப்பூர்வமாகக் கையொப்பமிட்டுள்ளனர்."
            )
        ],

        DOC_TITLE_COMMUNITY_FOREST_RIGHTS: [
            # Variation 1: Bureaucratic / Form Style
            (
                "அனுபந்தம் - III [விதி 8(h) பார்க்க]\n"
                "சமூக வன உரிமைகளுக்கான பட்டா மற்றும் அதிகாரப்பூர்வ ஆவணம்.\n"
                "இந்த சமூக வன உரிமையானது {COMMUNITY_RIGHT_HOLDER_NAME} என்ற சமூக அமைப்பிற்கு வழங்கப்படுகிறது.\n"
                "இது {STATE} மாநிலம், {DISTRICT} மாவட்டம் மற்றும் {TEHSIL_TALUKA} தாலுகாவிற்கு உட்பட்ட பகுதியாகும்.\n"
                "இப்பட்டா {VILLAGE} கிராமம், {GRAM_PANCHAYAT} கிராம பஞ்சாயத்து மற்றும் {GRAM_SABHA} கிராம சபைக்குச் சொந்தமானது.\n\n"

                "இந்த உரிமையைப் பெறும் சமூகமானது {CATEGORY_SCHEDULED_TRIBE} அல்லது {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} என அங்கீகரிக்கப்பட்டுள்ளது.\n"
                "சமூகத்திற்கு வழங்கப்பட்டுள்ள உரிமையின் தன்மை {COMMUNITY_RIGHT_NATURE} எனத் தெளிவாக வரையறுக்கப்பட்டுள்ளது.\n"
                "இந்த உரிமையை அனுபவிப்பதற்குச் சில நிபந்தனைகள் உள்ளன, அவை: {TITLE_CONDITIONS}.\n"
                "இந்த உரிமைக்கு உட்பட்ட வனப்பகுதியின் கசரா/கம்பார்ட்மென்ட் எண் {KHASRA_COMPARTMENT_NUMBER} ஆகும்.\n"
                "நிலத்தின் எல்லைகள் {BOUNDARY_DESCRIPTION} என்ற புவியியல் குறிப்புகளால் சுட்டிக்காட்டப்பட்டுள்ளன.\n\n"

                "மேலும், இப்பகுதியின் மரபு வழி எல்லைகள் {CUSTOMARY_BOUNDARY} எனப் பாரம்பரியமாக அங்கீகரிக்கப்பட்டுள்ளது.\n"
                "வன வளங்களைச் சமூகப் பயன்பாட்டிற்காகப் பெறுவதற்கு இந்த ஆவணம் சட்டப்பூர்வ அங்கீகாரத்தை அளிக்கிறது.\n"
                "ஆனால், காட்டின் பல்லுயிர் பெருக்கத்திற்கு எவ்வித தீங்கும் ஏற்படாத வகையில் வளங்கள் பயன்படுத்தப்பட வேண்டும்.\n"
                "விதிமுறைகள் மீறப்பட்டால், அரசு இந்த உரிமையை மறுபரிசீலனை செய்ய அதிகாரம் கொண்டுள்ளது.\n"
                "மாவட்ட அளவிலான அதிகாரிகளால் இப்பட்டா அங்கீகரிக்கப்பட்டு வழங்கப்படுகிறது."
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "சமூக வன உரிமைப் பட்டா மற்றும் கிராம சபைக்கான சட்டப்பூர்வ அதிகாரம்.\n"
                "அரசாங்கத்தின் முறையான ஒப்புதலுடன், {COMMUNITY_RIGHT_HOLDER_NAME} அமைப்பிற்கு இந்த உரிமை வழங்கப்படுகிறது.\n"
                "இச்சமூகம் {STATE} மாநிலத்தின் {DISTRICT} மாவட்டத்தில் உள்ள {TEHSIL_TALUKA} தாலுகாவில் நீண்ட காலமாக வசித்து வருகிறது.\n"
                "இவர்களது வசிப்பிடம் {VILLAGE} கிராமம், {GRAM_PANCHAYAT} பஞ்சாயத்து மற்றும் {GRAM_SABHA} கிராம சபை ஆகியவற்றை உள்ளடக்கியது.\n"
                "இவர்கள் {CATEGORY_SCHEDULED_TRIBE} மற்றும் {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} வகையைச் சேர்ந்தவர்களாகப் பதிவு செய்யப்பட்டுள்ளனர்.\n\n"

                "இவர்களுக்கு வழங்கப்பட்டுள்ள சமூக உரிமையின் துல்லியமான தன்மை {COMMUNITY_RIGHT_NATURE} என்று விவரிக்கப்படுகிறது.\n"
                "இந்தச் சமூக உரிமையைச் செயல்படுத்துவதற்கான விதிமுறைகள் மற்றும் நிபந்தனைகள்: {TITLE_CONDITIONS}.\n"
                "வனத்துறையின் ஆவணங்களின்படி, இப்பகுதியின் கசரா எண் {KHASRA_COMPARTMENT_NUMBER} எனப் பதியப்பட்டுள்ளது.\n"
                "இப்பகுதியின் எல்லைகள் இயற்கையான அடையாளங்களைக் கொண்டு {BOUNDARY_DESCRIPTION} என விவரிக்கப்பட்டுள்ளன.\n"
                "மேலும், தலைமுறை தலைமுறையாகப் பின்பற்றப்படும் மரபு வழி எல்லை {CUSTOMARY_BOUNDARY} என உறுதி செய்யப்பட்டுள்ளது.\n\n"

                "இந்த ஆவணத்தின் மூலம் சமூகத்திற்கான மேய்ச்சல் மற்றும் சிறு வனப்பொருள் சேகரிப்பு உரிமைகள் பாதுகாக்கப்படுகின்றன.\n"
                "சுற்றுச்சூழலையும், காட்டின் வனப்பகுதியையும் பாதுகாக்கும் பொறுப்பு இச்சமூகத்தினரிடம் ஒப்படைக்கப்படுகிறது.\n"
                "சட்டத்திற்குப் புறம்பான மரவெட்டல் மற்றும் வேட்டையாடுதல் ஆகியவை முற்றிலும் தடை செய்யப்பட்டுள்ளன.\n"
                "மாநில அரசின் பழங்குடியினர் நலத்துறை மற்றும் வருவாய்த் துறையின் ஒப்புதலோடு இது வெளியிடப்படுகிறது.\n"
                "கிராம சபை இந்த ஆவணத்தைப் பாதுகாத்து, அதன் விதிகளை முறையாகச் செயல்படுத்த வேண்டும்."
            ),
            # Variation 3: Formal Letter Style
            (
                "சமூக வன உரிமைகளை அங்கீகரிக்கும் அதிகாரப்பூர்வ தலைப்புச் சான்றிதழ்.\n"
                "உரிமை பெறுபவர்: {COMMUNITY_RIGHT_HOLDER_NAME}.\n"
                "பகுதி: {VILLAGE} கிராமம், {GRAM_PANCHAYAT} பஞ்சாயத்து, {GRAM_SABHA} கிராம சபை.\n"
                "நிர்வாக எல்லைகள்: தாலுகா {TEHSIL_TALUKA}, மாவட்டம் {DISTRICT}, மாநிலம் {STATE}.\n"
                "பயனாளியின் வகை: {CATEGORY_SCHEDULED_TRIBE} அல்லது {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER}.\n\n"

                "மாநில அரசாங்கம், மேற்கண்ட சமூகத்திற்கு {COMMUNITY_RIGHT_NATURE} என்ற தன்மையிலான வன உரிமைகளை வழங்குகிறது.\n"
                "இந்த உரிமையானது {TITLE_CONDITIONS} என்ற கட்டுப்பாடுகள் மற்றும் நிபந்தனைகளுக்கு உட்பட்டது.\n"
                "ஒதுக்கப்பட்ட காட்டு நிலத்தின் கசரா அல்லது அளவீட்டு எண் {KHASRA_COMPARTMENT_NUMBER} ஆகும்.\n"
                "ஆவணங்களில் குறிப்பிடப்பட்டுள்ளபடி நிலத்தின் எல்லைகள் {BOUNDARY_DESCRIPTION} என்ற அடையாளங்களைக் கொண்டுள்ளன.\n"
                "சமூகத்தால் பாரம்பரியமாகக் கடைப்பிடிக்கப்படும் மரபு வழி எல்லை {CUSTOMARY_BOUNDARY} என்றும் சான்றளிக்கப்படுகிறது.\n\n"

                "இந்த அதிகாரம் கிராம சபையின் கூட்டு நிர்வாகத்தின் கீழ் மட்டுமே செயல்படுத்தப்பட வேண்டும்.\n"
                "காட்டு வளங்களை வணிக நோக்கத்திற்காகப் பயன்படுத்தாமல், சமூகத் தேவைகளுக்காக மட்டுமே பயன்படுத்த வேண்டும்.\n"
                "அரசாங்கத்தின் தணிக்கைகள் மற்றும் ஆய்வுகளுக்கு கிராம சபை முழு ஒத்துழைப்பு வழங்க வேண்டும்.\n"
                "இந்த ஆவணம் மாவட்ட ஆட்சியர் மற்றும் மாவட்ட வனத்துறை அதிகாரியின் முத்திரையுடன் வழங்கப்படுகிறது.\n"
                "இது வழங்கப்பட்ட நாள் முதல், சமூகத்தின் காடு சார்ந்த பொருளாதார சுதந்திரம் உறுதி செய்யப்படுகிறது."
            ),
            #variation 4
            (
                "சமூக வன உரிமைகளுக்கான (CFR) அரசிதழ் பதிவு பெற்ற சட்டப்பூர்வ ஆவணம் மற்றும் பட்டா.\n"
                "இந்த அதிகாரப்பூர்வ ஆவணத்தின் மூலம், {COMMUNITY_RIGHT_HOLDER_NAME} என்ற சமூக அமைப்பிற்கு வன நிலத்தின் மீதான சட்டப்பூர்வ உரிமைகள் வழங்கப்படுகின்றன.\n"
                "இந்த உரிமையானது {STATE} மாநிலம், {DISTRICT} மாவட்டம் மற்றும் {TEHSIL_TALUKA} தாலுகாவிற்கு உட்பட்ட புவியியல் அதிகார வரம்பிற்குள் வழங்கப்படுகிறது.\n"
                "சட்டப்பூர்வமாக இது {VILLAGE} கிராமம், {GRAM_PANCHAYAT} கிராம பஞ்சாயத்து மற்றும் {GRAM_SABHA} கிராம சபையின் நிர்வாகக் கட்டுப்பாட்டிற்கு உட்பட்டதாகும்.\n"
                "இந்த உரிமையைப் பெறும் சமூகம், அரசாங்கப் பதிவேடுகளின்படி {CATEGORY_SCHEDULED_TRIBE} அல்லது {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} என்ற சட்டப் பிரிவின் கீழ் பாதுகாக்கப்படுகிறது.\n"
                "கிராம சபையின் கூட்டுத் தீர்மானம் மற்றும் மாவட்ட அளவிலான குழுவின் ஒப்புதலின் அடிப்படையில் இந்த ஆவணம் சட்டப்பூர்வமாக வெளியிடப்படுகிறது.\n\n"

                "அங்கீகரிக்கப்பட்ட சமூக உரிமையின் தன்மை, நிபந்தனைகள் மற்றும் நிலவியல் ஆவணப்படுத்தல்.\n"
                "இந்தச் சமூகத்திற்கு அரசால் அதிகாரப்பூர்வமாக வழங்கப்பட்டுள்ள உரிமையின் தன்மை {COMMUNITY_RIGHT_NATURE} எனத் தெளிவாக வரையறுக்கப்பட்டுள்ளது.\n"
                "இந்த உரிமையைப் பயன்படுத்துவதற்கு வனத்துறையால் விதிக்கப்பட்டுள்ள சட்டப்பூர்வ நிபந்தனைகள் மற்றும் கட்டுப்பாடுகள்: {TITLE_CONDITIONS}.\n"
                "சமூக உரிமைகள் பயன்படுத்தப்படும் வனப்பகுதியின் சட்டப்பூர்வ கசரா அல்லது அளவீட்டு எண் {KHASRA_COMPARTMENT_NUMBER} எனப் பதிவு செய்யப்பட்டுள்ளது.\n"
                "நிலத்தின் எல்லைகளானது மலைகள், நீரோடைகள் போன்ற இயற்கை அடையாளங்களைக் கொண்டு {BOUNDARY_DESCRIPTION} என ஆவணப்படுத்தப்பட்டுள்ளது.\n"
                "மேலும், பல தலைமுறைகளாகச் சமூகத்தால் அங்கீகரிக்கப்பட்ட மரபு வழி எல்லையான {CUSTOMARY_BOUNDARY} சட்டப்பூர்வமாக உறுதி செய்யப்படுகிறது.\n\n"

                "சமூகத்தின் சட்டப்பூர்வக் கடமைகள், கட்டுப்பாடுகள் மற்றும் அரசின் இறுதி ஒப்புதல்.\n"
                "இந்த உரிமைச் சான்றிதழானது, சமூகத் தேவைகளுக்காக மட்டுமே தவிர, எவ்வித வணிக ரீதியான சுரண்டலுக்கும் பயன்படுத்தப்படக் கூடாது.\n"
                "பல்லுயிர் பெருக்கத்தைப் பாதுகாக்கவும், வன விலங்குகளுக்கு எவ்வித அச்சுறுத்தலும் இன்றி வளங்களைப் பயன்படுத்தவும் சமூகம் கடமைப்பட்டுள்ளது.\n"
                "சட்டவிரோத மரவெட்டல் அல்லது அரசுக்கு எதிரான நடவடிக்கைகளில் ஈடுபட்டால் இந்த உரிமை உடனடியாக ரத்து செய்யப்படும்.\n"
                "பழங்குடியினர் நலத்துறை மற்றும் வனத்துறை ஆகிய இரு அரசுத் துறைகளின் முழுமையான ஒருங்கிணைப்போடு இந்த ஆவணம் நிர்வகிக்கப்படும்.\n"
                "மாவட்ட ஆட்சியர் மற்றும் சம்பந்தப்பட்ட அதிகாரிகளின் அதிகாரப்பூர்வ முத்திரை மற்றும் கையொப்பத்துடன் இப்பட்டா அரசிதழில் பதிவு செய்யப்படுகிறது."
            )
        ],

        DOC_TITLE_COMMUNITY_FOREST_RESOURCES: [
            # Variation 1: Bureaucratic / Form Style
            (
                "அனுபந்தம் - IV [விதி 8(i) பார்க்க]\n"
                "சமூக வன வளங்களுக்கான (CFR) பட்டா மற்றும் உரிமையளிப்பு ஆவணம்.\n"
                "இந்த அதிகாரப்பூர்வ ஆவணம் {STATE} மாநிலம், {DISTRICT} மாவட்டம், {TEHSIL_TALUKA} தாலுகாவிற்கு உட்பட்ட பகுதிக்கு வழங்கப்படுகிறது.\n"
                "இதன்படி, {VILLAGE} கிராமம், {GRAM_PANCHAYAT} கிராம பஞ்சாயத்து மற்றும் {GRAM_SABHA} கிராம சபைக்குச் சமூக வன வள உரிமை அளிக்கப்படுகிறது.\n"
                "இந்த உரிமை {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} அல்லது {COMMUNITY_TYPE_BOTH} சமூகங்களைச் சேர்ந்த மக்களுக்கானதாகும்.\n\n"

                "இந்தச் சமூக வன வள உரிமைக்கு உட்பட்ட பகுதியின் கசரா/கம்பார்ட்மென்ட் எண்கள் {KHASRA_COMPARTMENT_NUMBER} ஆகும்.\n"
                "இந்தப் பகுதியின் புவியியல் அமைவிடம் மற்றும் எல்லைகள் {BOUNDARY_DESCRIPTION} என்று மிகத் தெளிவாக ஆவணப்படுத்தப்பட்டுள்ளன.\n"
                "மேலும், காலம் காலமாக இருந்து வரும் மரபு வழி எல்லையான {CUSTOMARY_BOUNDARY} சட்டப்பூர்வமாக அங்கீகரிக்கப்படுகிறது.\n"
                "குறிப்பிட்ட பகுதிக்குள் உள்ள அனைத்து சிறு வனப் பொருட்களையும் நிர்வகிக்கும் அதிகாரம் கிராம சபைக்கு வழங்கப்பட்டுள்ளது.\n"
                "வனத்துறையின் வழிகாட்டுதல்களின்படி, இந்த வளங்களைச் சமூகத்தினர் பாதுகாத்து, நிலையான முறையில் பயன்படுத்த வேண்டும்.\n\n"

                "இந்த உரிமையானது பழங்குடியினர் மற்றும் பிற பாரம்பரிய வனவாசிகளின் வாழ்வாதாரத்தை மேம்படுத்தும் நோக்கில் வழங்கப்படுகிறது.\n"
                "காட்டு வளங்களை நிர்வகிப்பதற்கான குழுக்களை அமைக்கும் அதிகாரம் கிராம சபைக்கு முழுமையாக அளிக்கப்பட்டுள்ளது.\n"
                "இந்த வளங்களைச் சேதப்படுத்தும் எந்தவொரு செயலும் சட்டப்படி குற்றமாகக் கருதப்பட்டு உரிமைகள் ரத்து செய்யப்படும்.\n"
                "இதற்கு மாநில அரசின் உரிய அதிகாரிகளான மாவட்ட ஆட்சியர் மற்றும் வன அலுவலர் முறைப்படி ஒப்புதல் அளித்துள்ளனர்.\n"
                "இந்த ஆவணம் சமூக வன வளங்களின் பாதுகாப்பிற்கான ஒரு முக்கிய மைல்கல்லாகப் பதிவு செய்யப்படுகிறது."
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "சமூக வன வளங்களுக்கான சட்டப்பூர்வ உரிமை ஆவணம் மற்றும் கிராம சபையின் அதிகாரப் பகிர்வு.\n"
                "அரசு, {STATE} மாநிலத்தின் {DISTRICT} மாவட்டத்தில் உள்ள {TEHSIL_TALUKA} தாலுகாவில் வசிக்கும் மக்களின் கோரிக்கையை ஏற்றுள்ளது.\n"
                "இதன் அடிப்படையில், {VILLAGE} கிராமம், {GRAM_PANCHAYAT} பஞ்சாயத்து மற்றும் {GRAM_SABHA} கிராம சபைக்கு CFR பட்டா வழங்கப்படுகிறது.\n"
                "இந்த உரிமை அங்கீகாரம் {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} அல்லது {COMMUNITY_TYPE_BOTH} சமூகங்களுக்குப் பொருந்தும்.\n"
                "இச்சமூகங்கள் காட்டைத் தெய்வமாக மதித்து, அதைப் பாதுகாக்கும் பாரம்பரியத்தைக் கொண்டவர்கள் ஆவர்.\n\n"

                "சமூக வன வளப் பகுதிக்குரிய கசரா/கம்பார்ட்மென்ட் எண்கள் {KHASRA_COMPARTMENT_NUMBER} என நில அளவை ஆவணங்களில் குறிப்பிடப்பட்டுள்ளன.\n"
                "இந்தப் பகுதியின் எல்லைகள், மலைகள் மற்றும் நீரோடைகளை அடையாளமாகக் கொண்டு {BOUNDARY_DESCRIPTION} என வரையறுக்கப்பட்டுள்ளன.\n"
                "இதற்கு அப்பால் உள்ள எங்களின் மரபு வழி எல்லை {CUSTOMARY_BOUNDARY} என்பதும் அரசாங்கத்தால் ஏற்றுக்கொள்ளப்பட்டுள்ளது.\n"
                "இந்த எல்லைக்குள் கிடைக்கும் விறகு, தேன், மற்றும் மூலிகைகளைத் தடையின்றிப் பயன்படுத்தும் உரிமை கிராம சபைக்கு உள்ளது.\n"
                "மேலும், வனக் கொள்ளையர்களிடமிருந்து காட்டைப் பாதுகாக்கும் முழுப் பொறுப்பும் இச்சமூகத்திடம் ஒப்படைக்கப்பட்டுள்ளது.\n\n"

                "சமூக வன வள உரிமைச் சட்டம் பழங்குடி மக்களின் சுயநிர்ணய உரிமையை உறுதி செய்கிறது.\n"
                "பல்லுயிர் அமைப்பைப் பேணுவதற்கான தகுந்த மேலாண்மைத் திட்டத்தைக் கிராம சபை வகுக்க வேண்டும்.\n"
                "அரசு மற்றும் வனத்துறையானது, கிராம சபையின் மேலாண்மைத் திட்டங்களுக்குத் தொழில்நுட்ப உதவிகளை மட்டுமே வழங்கும்.\n"
                "இந்த ஆவணம், சமூகத்தின் பொருளாதார வளர்ச்சியையும் காட்டின் நிலைத்தன்மையையும் ஒருங்கே உறுதி செய்யும்.\n"
                "சம்பந்தப்பட்ட அதிகாரிகளின் முறையான கையொப்பத்துடன் இப்பட்டா இன்று முதல் அமலுக்கு வருகிறது."
            ),
            # Variation 3: Formal Letter Style
            (
                "தலைப்பு: சமூக வன வளங்கள் (CFR) மீதான உரிமை மற்றும் பட்டா சான்றிதழ்.\n"
                "பயனாளி அமைப்பு: {GRAM_SABHA} கிராம சபை, {VILLAGE} கிராமம், {GRAM_PANCHAYAT} பஞ்சாயத்து.\n"
                "அமைவிடம்: தாலுகா {TEHSIL_TALUKA}, மாவட்டம் {DISTRICT}, மாநிலம் {STATE}.\n"
                "சமூக வகைப்பாடு: {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} அல்லது {COMMUNITY_TYPE_BOTH}.\n"
                "பொருள்: மேற்குறிப்பிட்ட கிராம சபைக்குச் சமூக வன வளங்களை நிர்வகிக்கும் அதிகாரப்பூர்வ உரிமை வழங்குதல்.\n\n"

                "வன உரிமைச் சட்டம் 2006-ன் பிரிவுகளின் அடிப்படையில் இந்த வரலாற்றுச் சிறப்புமிக்க உரிமை வழங்கப்படுகிறது.\n"
                "உரிமை பெற்ற வனப்பகுதியின் கசரா அல்லது அளவீட்டு எண் {KHASRA_COMPARTMENT_NUMBER} எனத் தெளிவாகப் பதிவு செய்யப்பட்டுள்ளது.\n"
                "அப்பகுதியின் எல்லையானது {BOUNDARY_DESCRIPTION} என்ற விவரங்கள் மூலம் நிலவியல் ரீதியாக வரையறுக்கப்பட்டுள்ளது.\n"
                "பாரம்பரியமாக இச்சமூகத்தால் பேணப்படும் மரபு வழி எல்லை {CUSTOMARY_BOUNDARY} என்பதும் இதில் அடங்கும்.\n"
                "இந்த எல்லைக்குள் உள்ள அனைத்து இயற்கை வளங்களையும் பாதுகாத்து, பயன்படுத்தும் அதிகாரம் கிராம சபைக்குச் சொந்தமானது.\n\n"

                "இந்த உரிமை எந்த வகையிலும் தனிநபருக்குச் சொந்தமானதல்ல, இது ஒட்டுமொத்த சமூகத்திற்குமான பொதுச் சொத்தாகும்.\n"
                "வன வளங்களின் நிலையான மேலாண்மைக்காகக் கிராம சபை ஒரு வன உரிமைக் குழுவை அமைத்துச் செயல்பட வேண்டும்.\n"
                "காட்டுத்தீ போன்ற இயற்கை பேரிடர்களில் இருந்து காட்டைப் பாதுகாப்பது சமூகத்தின் தலையாய கடமையாகும்.\n"
                "இந்த அதிகாரம், மாநில அளவிலான குழுவால் மதிப்பாய்வு செய்யப்பட்டு, இறுதி ஒப்புதலுக்குப் பின் வழங்கப்படுகிறது.\n"
                "இந்தச் சான்றிதழானது சம்பந்தப்பட்ட மாவட்ட அதிகாரிகளின் முத்திரையோடு அதிகாரப்பூர்வமாக வெளியிடப்படுகிறது."
            ),
            #variation 4
            (
                "சமூக வன வளங்களுக்கான (Community Forest Resources) சட்டப்பூர்வப் பட்டா மற்றும் அரசின் அதிகாரப் பகிர்வு ஆவணம்.\n"
                "பிரிவு 3(1)(i)-ன் கீழ், {STATE} மாநிலம், {DISTRICT} மாவட்டம், {TEHSIL_TALUKA} தாலுகாவிற்கு உட்பட்ட அதிகார வரம்பில் இந்த ஆவணம் சட்டப்பூர்வமாக வழங்கப்படுகிறது.\n"
                "இதன்படி, {VILLAGE} கிராமம், {GRAM_PANCHAYAT} கிராம பஞ்சாயத்து மற்றும் {GRAM_SABHA} கிராம சபைக்குச் சமூக வன வளங்களை நிர்வகிக்கும் முழு அதிகாரம் அளிக்கப்படுகிறது.\n"
                "இந்த ஆவணமானது, {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} அல்லது {COMMUNITY_TYPE_BOTH} சமூகங்களைச் சேர்ந்த மக்களின் வாழ்வாதாரத்தைப் பாதுகாக்கும் சட்ட ஆவணமாகும்.\n"
                "மாவட்ட அளவிலான நிலைக்குழுவின் (DLC) இறுதிக்கட்ட சட்டப்பூர்வ ஒப்புதலுக்குப் பிறகே இந்த உரிமைச் சான்றிதழ் அதிகாரப்பூர்வமாக வெளியிடப்படுகிறது.\n"
                "இதன் மூலம், அரசுக்குச் சொந்தமான வன வளங்களைப் பாதுகாக்கும் மற்றும் நிர்வகிக்கும் உரிமை கிராம சபைக்குச் சட்டப்பூர்வமாக மாற்றப்படுகிறது.\n\n"

                "வன வளப் பகுதியின் சட்டப்பூர்வ நில அளவை எண்கள், எல்லைகள் மற்றும் மரபுவழிப் பிரகடனம்.\n"
                "சமூக நிர்வாகத்திற்கு உட்பட்ட வன வளப் பகுதியின் கசரா (Khasra) அல்லது கம்பார்ட்மென்ட் எண்கள் {KHASRA_COMPARTMENT_NUMBER} என நில அளவை ஆவணங்களில் தெளிவாகப் பதிவு செய்யப்பட்டுள்ளது.\n"
                "இந்தப் பகுதியின் புவியியல் மற்றும் நிலவியல் எல்லைகள் {BOUNDARY_DESCRIPTION} என்று வரைபடங்கள் மூலம் அரசாங்கத்தால் உறுதி செய்யப்பட்டுள்ளன.\n"
                "அண்டை கிராமங்கள் மற்றும் வனத்துறையுடன் எல்லையைப் பகிர்ந்து கொள்ளும் மரபு வழி எல்லையான {CUSTOMARY_BOUNDARY} அதிகாரப்பூர்வமாகச் சான்றளிக்கப்படுகிறது.\n"
                "இந்த எல்லைகளுக்குள் உள்ள குறுங்காட்டுப் பொருட்கள், நீராதாரங்கள் மற்றும் தாவர வகைகளைப் பயன்படுத்தும் முழுமையான உரிமை கிராம சபைக்கு வழங்கப்பட்டுள்ளது.\n"
                "எல்லை குறித்த எவ்வித சர்ச்சைகளும் எழாத வண்ணம் நில அளவைத் துறை மூலம் முறையான கல்வெட்டுகள் மற்றும் குறியீடுகள் நிறுவப்பட்டுள்ளன.\n\n"

                "கிராம சபையின் சட்டப்பூர்வப் பொறுப்புகள், வனப் பாதுகாப்பு மற்றும் அதிகாரிகளின் இறுதிச் சான்றளிப்பு.\n"
                "அச்சட்டத்தின் விதிகளைத் தவிர்த்து, இந்த உரிமையின் மீது வேறு எவ்விதப் புதிய கட்டுப்பாடுகளும் அல்லது நிபந்தனைகளும் மாநில அரசால் விதிக்கப்படவில்லை.\n"
                "இருப்பினும், காட்டின் சூழலியல் சமநிலையைப் பேணுவதும், காட்டுத்தீ போன்ற பேரிடர்களைத் தடுப்பதும் கிராம சபையின் முழுமையான சட்டப்பூர்வக் கடமையாகும்.\n"
                "இதற்காகக் கிராம சபை சார்பாக 'வன வளப் பாதுகாப்புக் குழு' ஒன்று அமைக்கப்பட்டு, அதன் அறிக்கை ஆண்டுதோறும் அரசுக்குச் சமர்ப்பிக்கப்பட வேண்டும்.\n"
                "சட்டத்திற்குப் புறம்பான வகையில் வன வளங்கள் அழிக்கப்பட்டால், குற்றவியல் நடைமுறைச் சட்டத்தின் கீழ் கிராம சபை பொறுப்பேற்க நேரிடும்.\n"
                "மாநில அரசின் உயர்மட்ட அதிகாரிகளான மாவட்ட ஆட்சியர், மாவட்ட வன அலுவலர் மற்றும் பழங்குடியினர் நல அதிகாரி ஆகியோரின் சான்றொப்பத்துடன் இப்பட்டா அதிகாரப்பூர்வமாக அமலுக்கு வருகிறது."
            )
        ]
    },
    # Telugu

    "te": {
        DOC_CLAIM_FOREST_LAND: [
            # Variation 1: Bureaucratic / Form Style (Simulating Form A filled application)
            (
                "ఫారం - ఎ [నిబంధన 11(1)(a) చూడండి]\n"
                "అటవీ భూమిపై హక్కుల కోసం దావా దరఖాస్తు ఫారం మరియు దరఖాస్తుదారు ప్రాథమిక వివరాలు.\n"
                "దావాదారుని పూర్తి పేరు: {CLAIMANT_NAME}.\n"
                "తండ్రి లేదా తల్లి పేరు: {FATHER_MOTHER_NAME}. జీవిత భాగస్వామి పేరు: {SPOUSE_NAME}.\n"
                "దరఖాస్తుదారుని పూర్తి నివాస చిరునామా: {ADDRESS_FULL} గా నమోదు చేయబడింది.\n"
                "ఈ అటవీ భూమి {STATE} రాష్ట్రం, {DISTRICT} జిల్లా మరియు {TEHSIL_TALUKA} తాలూకా పరిధిలో ఉంది.\n"
                "అలాగే, ఇది {VILLAGE} గ్రామం, {GRAM_PANCHAYAT} గ్రామ పంచాయతీ మరియు {GRAM_SABHA} గ్రామ సభ పరిపాలనా పరిధిలోకి వస్తుంది.\n\n"

                "దావాదారుని కుటుంబ వివరాలు మరియు అటవీ భూమి ఆక్రమణ స్థితి:\n"
                "నా కుటుంబ సభ్యుడు {FAMILY_MEMBER_NAME} (వయస్సు: {FAMILY_MEMBER_AGE} సంవత్సరాలు) మరియు నాపై ఆధారపడిన వ్యక్తి {DEPENDENT_NAME} నాతోనే నివసిస్తున్నారు.\n"
                "మేము {CATEGORY_SCHEDULED_TRIBE} లేదా {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} వర్గానికి చెందినవారమని ధృవీకరిస్తున్నాము.\n"
                "నివాసం కోసం మా ఆధీనంలో ఉన్న అటవీ భూమి విస్తీర్ణం {LAND_EXTENT_HABITATION} గా నిర్ణయించబడింది.\n"
                "స్వయం సాగు (వ్యవసాయం) కోసం ఉపయోగిస్తున్న భూమి విస్తీర్ణం {LAND_EXTENT_SELF_CULTIVATION} గా ఉంది.\n"
                "అటవీ గ్రామాల పరిధిలో ఉన్న భూమి విస్తీర్ణం {LAND_EXTENT_FOREST_VILLAGE} గా రెవెన్యూ రికార్డుల్లో నమోదు చేయబడింది.\n\n"

                "భూమికి సంబంధించిన ఇతర దావాలు, వివాదాలు మరియు ఆధారాలు:\n"
                "ఈ భూమిపై ఏదైనా వివాదం ఉన్నట్లయితే, దాని వివరాలు: {DISPUTED_LAND_DESCRIPTION}.\n"
                "గతంలో జారీ చేసిన పట్టాలు, లీజులు లేదా మంజూరు వివరాలు: {EXISTING_PATTAS_LEASES_GRANTS}.\n"
                "పునరావాసం లేదా ప్రత్యామ్నాయ భూమి కోసం దావా వేయబడిన భూమి {REHABILITATION_LAND}.\n"
                "ఎలాంటి పరిహారం లేకుండా నిర్వాసితులైన భూమి వివరాలు: {DISPLACED_FROM_LAND}.\n"
                "మా ఇతర సాంప్రదాయ హక్కులు {OTHER_TRADITIONAL_RIGHT} మరియు అదనపు సమాచారం {OTHER_INFORMATION} జతచేయబడింది.\n"
                "ఈ దావాకు మద్దతుగా సాక్ష్యంగా {EVIDENCE_ITEM} పత్రాలు సమర్పించబడుతున్నాయి."
            ),
            # Variation 2: Narrative / Descriptive Style (Simulating a Gram Sabha resolution narrative)
            (
                "గ్రామ సభ ముందు సమర్పించిన సమగ్ర నివేదిక మరియు అటవీ భూమిపై హక్కుల దావా.\n"
                "నేను, శ్రీ/శ్రీమతి {CLAIMANT_NAME} (తండ్రి/తల్లి: {FATHER_MOTHER_NAME}, జీవిత భాగస్వామి: {SPOUSE_NAME}) ఈ నివేదికను సమర్పిస్తున్నాను.\n"
                "నా శాశ్వత నివాస చిరునామా {ADDRESS_FULL}. నేను {STATE} రాష్ట్రంలోని {DISTRICT} జిల్లా వాసిని.\n"
                "మా ఇల్లు {TEHSIL_TALUKA} తాలూకా పరిధిలోని {VILLAGE} గ్రామంలో ఉంది.\n"
                "ఈ ప్రాంతం నేరుగా {GRAM_PANCHAYAT} గ్రామ పంచాయతీ మరియు {GRAM_SABHA} గ్రామ సభ పరిపాలనా నియంత్రణలో ఉంది.\n\n"

                "మా కుటుంబం తరతరాలుగా అడవులపై ఆధారపడి ఉంది మరియు మేము {CATEGORY_SCHEDULED_TRIBE} లేదా {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} కమ్యూనిటీకి చెందిన సాంప్రదాయ అటవీ నివాసులం.\n"
                "నా కుటుంబంలో సభ్యులు {FAMILY_MEMBER_NAME} (వయస్సు {FAMILY_MEMBER_AGE} సంవత్సరాలు) మరియు నాపై పూర్తిగా ఆధారపడిన {DEPENDENT_NAME} ఉన్నారు.\n"
                "మేము అనేక తరాలుగా నివసిస్తున్న నివాస అటవీ భూమి విస్తీర్ణం {LAND_EXTENT_HABITATION}.\n"
                "మా జీవనాధారం వ్యవసాయం మరియు మేము స్వయంగా సాగు చేస్తున్న భూమి విస్తీర్ణం {LAND_EXTENT_SELF_CULTIVATION}.\n"
                "అదనంగా, అటవీ గ్రామ సరిహద్దుల్లో ఉన్న మా భూమి విస్తీర్ణం {LAND_EXTENT_FOREST_VILLAGE} గా కొలవబడింది.\n\n"

                "ఈ దావాకు సంబంధించి కొన్ని ముఖ్యమైన చట్టపరమైన వాస్తవాలు నమోదు చేయబడుతున్నాయి.\n"
                "భూమికి సంబంధించిన ఏదైనా వివాదం {DISPUTED_LAND_DESCRIPTION} గా వివరించబడింది మరియు పాత పట్టాల వివరాలు {EXISTING_PATTAS_LEASES_GRANTS}.\n"
                "పునరావాసం కోసం మాకు {REHABILITATION_LAND} భూమి అవసరం మరియు గతంలో మేము ఎలాంటి పరిహారం లేకుండా {DISPLACED_FROM_LAND} నుండి తొలగించబడ్డాము.\n"
                "మా పూర్వీకులు అనుభవించిన ఇతర సాంప్రదాయ హక్కులు {OTHER_TRADITIONAL_RIGHT} నేటికీ వర్తిస్తాయి.\n"
                "దావాను నిర్ధారించడానికి బలమైన ఆధారాలు {EVIDENCE_ITEM} సమర్పించబడ్డాయి మరియు ఇతర సంబంధిత సమాచారం {OTHER_INFORMATION} పరిశీలన కోసం జతచేయబడింది."
            ),
            # Variation 3: Formal Letter Style (Simulating a petition to the Sub-Divisional Level Committee)
            (
                "ప్రేషకుడు: {CLAIMANT_NAME}, తండ్రి/తల్లి: {FATHER_MOTHER_NAME}, జీవిత భాగస్వామి: {SPOUSE_NAME}.\n"
                "చిరునామా: {ADDRESS_FULL}, గ్రామం {VILLAGE}, పంచాయతీ {GRAM_PANCHAYAT}, గ్రామ సభ {GRAM_SABHA}.\n"
                "తాలూకా: {TEHSIL_TALUKA}, జిల్లా: {DISTRICT}, రాష్ట్రం: {STATE}.\n"
                "విషయం: అటవీ హక్కుల చట్టం 2006 కింద వ్యక్తిగత అటవీ భూమి హక్కులను మంజూరు చేయుట గురించి దరఖాస్తు.\n"
                "అయ్యా, పై విషయానికి సంబంధించి నేను దీర్ఘకాలంగా అటవీ ప్రాంతంలో నివసిస్తున్నానని వినయపూర్వకంగా తెలియజేస్తున్నాను.\n\n"

                "నేను అర్హత కలిగిన {CATEGORY_SCHEDULED_TRIBE} లేదా {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} వర్గానికి చెందిన సభ్యుడినని ధృవీకరిస్తున్నాను.\n"
                "నా కుటుంబంలో {FAMILY_MEMBER_NAME} (వయస్సు {FAMILY_MEMBER_AGE}) మరియు ఆధారపడిన {DEPENDENT_NAME} ఉన్నారు, వీరు ఈ భూమిపైనే ఆధారపడి జీవిస్తున్నారు.\n"
                "అటవీ ప్రాంతంలో మా ఇల్లు మరియు నివాస ప్రాంగణం మొత్తం విస్తీర్ణం {LAND_EXTENT_HABITATION}.\n"
                "మేము స్వయంగా వ్యవసాయం కోసం ఉపయోగిస్తున్న వ్యవసాయ భూమి విస్తీర్ణం {LAND_EXTENT_SELF_CULTIVATION}.\n"
                "అటవీ గ్రామాలలో మా భూమి విస్తీర్ణం {LAND_EXTENT_FOREST_VILLAGE} గా రెవెన్యూ రికార్డుల్లో నమోదు చేయబడాలి.\n\n"

                "ఈ భూమికి సంబంధించిన వివాదాస్పద పరిస్థితి {DISPUTED_LAND_DESCRIPTION}, దీనిని పరిష్కరించాల్సిన అవసరం ఉంది.\n"
                "గతంలో జారీ చేసిన లీజులు లేదా పట్టాల {EXISTING_PATTAS_LEASES_GRANTS} కాపీలు ధృవీకరణ కోసం జతచేయబడ్డాయి.\n"
                "ప్రత్యామ్నాయ పునరావాస భూమి {REHABILITATION_LAND} మరియు పరిహారం లేకుండా నిర్వాసితులైన భూమి {DISPLACED_FROM_LAND} ను కూడా పరిగణనలోకి తీసుకోవాలి.\n"
                "చట్టం ద్వారా రక్షించబడిన మా ఇతర సాంప్రదాయ హక్కులు {OTHER_TRADITIONAL_RIGHT} మాకు మంజూరు చేయబడాలి.\n"
                "సాక్ష్యంగా {EVIDENCE_ITEM} మరియు అదనపు వివరాలు {OTHER_INFORMATION} దరఖాస్తుతో పాటు జతచేయబడ్డాయి."
            ),
            # Variation 4: Legal / Statutory Declaration Style (Simulating a sworn affidavit)
            (
                "అఫిడవిట్ మరియు చట్టబద్ధమైన హక్కుల ప్రకటన (అటవీ హక్కుల చట్టం 2006 కింద).\n"
                "నేను, {CLAIMANT_NAME} (తండ్రి/తల్లి: {FATHER_MOTHER_NAME}, చట్టబద్ధమైన జీవిత భాగస్వామి: {SPOUSE_NAME}), ఈ క్రింది విషయాలను సత్యనిష్ఠతో ప్రకటిస్తున్నాను.\n"
                "నా చట్టబద్ధమైన మరియు శాశ్వత చిరునామా {ADDRESS_FULL} గా ప్రభుత్వ పత్రాలలో నమోదు చేయబడింది.\n"
                "దావా చేయబడిన భూమి {STATE} రాష్ట్రం, {DISTRICT} జిల్లా మరియు {TEHSIL_TALUKA} తాలూకా అధికార పరిధిలో ఉంది.\n"
                "ఈ భూమి పూర్తిగా {VILLAGE} రెవెన్యూ గ్రామం, {GRAM_PANCHAYAT} గ్రామ పంచాయతీ మరియు {GRAM_SABHA} గ్రామ సభ చట్టబద్ధమైన పరిధిలో ఉంది.\n\n"

                "సెక్షన్ 3(1)(a) కింద భూ ఆక్రమణ మరియు సామాజిక వర్గం యొక్క చట్టబద్ధమైన నిర్ధారణ.\n"
                "నేను చట్టబద్ధమైన {CATEGORY_SCHEDULED_TRIBE} లేదా {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} వర్గానికి చెందినవాడినని ప్రమాణపూర్వకంగా తెలియజేస్తున్నాను.\n"
                "నా చట్టబద్ధమైన వారసులు {FAMILY_MEMBER_NAME} (వయస్సు {FAMILY_MEMBER_AGE}) మరియు ఆధారపడిన {DEPENDENT_NAME} ఈ దావా యొక్క ప్రత్యక్ష లబ్ధిదారులు.\n"
                "చట్టంలోని నిబంధనల ప్రకారం, నివాస ప్రయోజనాల కోసం ఆక్రమించబడిన భూమి కొలత {LAND_EXTENT_HABITATION} గా నిర్ణయించబడింది.\n"
                "వ్యవసాయ ఉపయోగం లేదా స్వయం సాగు కోసం సాగు చేయబడుతున్న భూమి విస్తీర్ణం {LAND_EXTENT_SELF_CULTIVATION} గా కనుగొనబడింది.\n"
                "సెక్షన్ 3(1)(h) ప్రకారం, అటవీ గ్రామాల్లో ఉన్న భూమి పరిమితి {LAND_EXTENT_FOREST_VILLAGE} గా ఉంది.\n\n"

                "పెండింగ్‌లో ఉన్న దావాలు, పట్టాలు మరియు ఇతర చట్టబద్ధమైన హక్కుల బహిర్గతం.\n"
                "సెక్షన్ 3(1)(f) కింద ఈ భూమిపై ఉన్న ఎలాంటి వివాదమైనా {DISPUTED_LAND_DESCRIPTION} గా ప్రకటించబడుతుంది.\n"
                "గత ప్రభుత్వాలు జారీ చేసిన పట్టాలు లేదా మంజూరుల వివరాలు: {EXISTING_PATTAS_LEASES_GRANTS}.\n"
                "సెక్షన్ 3(1)(m) కింద స్వస్థలంలో పునరావాసం పొందిన భూమి {REHABILITATION_LAND} వివరాలు కూడా సమర్పించబడ్డాయి.\n"
                "సెక్షన్ 4(8) ప్రకారం, ఎలాంటి తగిన పరిహారం లేకుండా తొలగించబడిన భూమి వివరాలు {DISPLACED_FROM_LAND}.\n"
                "సెక్షన్ 3(1)(l) కింద ఇతర సాంప్రదాయ హక్కులు {OTHER_TRADITIONAL_RIGHT} మరియు చట్టపరమైన సాక్ష్యం {EVIDENCE_ITEM} తో సహా {OTHER_INFORMATION} ఈ అఫిడవిట్‌లో అంతర్భాగం."
            )
        ],

        DOC_CLAIM_COMMUNITY_RIGHTS: [
            # Variation 1: Bureaucratic / Form Style
            (
                "ఫారం - బి [నిబంధన 11(1)(a) మరియు (4) చూడండి]\n"
                "సమిష్టి అటవీ హక్కుల కోసం అధికారిక దావా ఫారం మరియు గ్రామ సభ తీర్మానం.\n"
                "ఈ ఉమ్మడి దరఖాస్తు {VILLAGE} గ్రామం మరియు {GRAM_PANCHAYAT} గ్రామ పంచాయతీ తరపున సమర్పించబడుతోంది.\n"
                "ఇది {STATE} రాష్ట్రం, {DISTRICT} జిల్లా, మరియు {TEHSIL_TALUKA} తాలూకా పరిధిలోని {GRAM_SABHA} గ్రామ సభచే ఆమోదించబడింది.\n"
                "మేమంతా సాంప్రదాయ అటవీ నివాసులం మరియు {COMMUNITY_TYPE_FDST} లేదా {COMMUNITY_TYPE_OTFD} సమాజానికి ప్రాతినిధ్యం వహిస్తున్నాము.\n\n"

                "సమాజం అనుభవిస్తున్న అటవీ హక్కుల స్వభావం క్రింది విధంగా నమోదు చేయబడింది.\n"
                "సామాజిక ఉపయోగం కోసం నిస్తార్ (Nistar) హక్కులు: {COMMUNITY_RIGHT_NISTAR}.\n"
                "లఘు అటవీ ఉత్పత్తుల (MFP) సేకరణ మరియు యాజమాన్య హక్కు: {RIGHT_MINOR_FOREST_PRODUCE}.\n"
                "చేపలు పట్టడం, జల వనరులు మరియు ఇతర వనరుల వినియోగ హక్కు: {COMMUNITY_RIGHT_RESOURCE_USE}.\n"
                "పశువులను మేపడానికి సంబంధించిన హక్కు: {COMMUNITY_RIGHT_GRAZING}.\n"
                "సంచార మరియు పశువుల కాపరుల సంఘాల కోసం సాంప్రదాయ వనరుల ప్రాప్యత: {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS}.\n\n"

                "ముఖ్యంగా దుర్బల గిరిజన సమూహాలు (PTG) మరియు వ్యవసాయ పూర్వ సంఘాల కోసం నివాస (Habitat) హక్కులు {COMMUNITY_TENURE_HABITAT} నిర్ధారించబడాలి.\n"
                "జీవవైవిధ్యం, మేధో సంపత్తి మరియు సాంప్రదాయ జ్ఞానాన్ని పొందే హక్కు {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} గా పరిగణించబడాలి.\n"
                "చట్టం ద్వారా నిర్వచించబడిన ఇతర సాంప్రదాయ హక్కులు {OTHER_TRADITIONAL_RIGHT} మా జీవనాధారానికి మూలం.\n"
                "ఈ సమిష్టి దావాలను నిరూపించడానికి సమర్పించిన ఆధారాలు: {EVIDENCE_ITEM}.\n"
                "పరిపాలనా సమీక్ష కోసం అవసరమైన అదనపు సమాచారం {OTHER_INFORMATION} ఈ ఫారమ్‌కు జతచేయబడింది."
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "సమిష్టి అటవీ హక్కుల మరియు సాంప్రదాయ హక్కుల రక్షణ కోసం గ్రామ సభ ఉమ్మడి దరఖాస్తు.\n"
                "మా {GRAM_SABHA} గ్రామ సభ, {VILLAGE} గ్రామంలోని నివాసితులందరి తరపున ఈ దావాను సమర్పిస్తోంది.\n"
                "మా ప్రాంతం {STATE} రాష్ట్రంలోని {DISTRICT} జిల్లాలో ఉన్న {TEHSIL_TALUKA} తాలూకా మరియు {GRAM_PANCHAYAT} పంచాయతీ పరిధిలోకి వస్తుంది.\n"
                "మా కమ్యూనిటీ ప్రభుత్వ వర్గీకరణ ప్రకారం {COMMUNITY_TYPE_FDST} లేదా {COMMUNITY_TYPE_OTFD} గా గుర్తించబడింది.\n"
                "మేము తరతరాలుగా అడవులతో సహజీవన జీవనశైలిని అనుసరిస్తున్నాము.\n\n"

                "రోజువారీ జీవితం మరియు జీవనోపాధి కోసం మేము ప్రధానంగా ఈ క్రింది సమిష్టి హక్కులపై ఆధారపడతాము.\n"
                "మా నిస్తార్ హక్కులు స్పష్టంగా {COMMUNITY_RIGHT_NISTAR} గా స్థాపించబడ్డాయి.\n"
                "తేనె, మూలికలు వంటి లఘు అటవీ ఉత్పత్తులను పొందే హక్కు {RIGHT_MINOR_FOREST_PRODUCE}.\n"
                "స్థానిక జల వనరుల వినియోగం మరియు చేపలు పట్టే హక్కు {COMMUNITY_RIGHT_RESOURCE_USE}.\n"
                "పశువుల పచ్చికబయళ్ళు మరియు మేత హక్కు {COMMUNITY_RIGHT_GRAZING} కింద రక్షించబడింది.\n"
                "కాలానుగుణంగా వలస వెళ్ళే సంచార సంఘాల వనరుల హక్కులు {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS} గా అందించబడ్డాయి.\n\n"

                "ఆదిమ జాతుల ప్రాచీన నివాసాలను (Habitat) రక్షించే హక్కు {COMMUNITY_TENURE_HABITAT} చాలా ముఖ్యమైనది.\n"
                "సాంప్రదాయ జ్ఞానం మరియు స్థానిక జీవవైవిధ్యంపై మా హక్కు {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} గా దావా చేయబడింది.\n"
                "మా పూర్వీకులు ఉపయోగించిన ఇతర సాంప్రదాయ హక్కులు {OTHER_TRADITIONAL_RIGHT} నేటికీ కొనసాగుతున్నాయి.\n"
                "ఈ హక్కుల ప్రామాణికత కోసం {EVIDENCE_ITEM} వంటి చారిత్రక పత్రాలు సమర్పించబడ్డాయి.\n"
                "వివరణాత్మక పరిశీలన కోసం {OTHER_INFORMATION} తో సహా ఇతర వాస్తవాలు కూడా అందించబడ్డాయి."
            ),
            # Variation 3: Formal Letter Style
            (
                "విషయం: అటవీ హక్కుల చట్టం 2006 కింద సమిష్టి అటవీ హక్కుల గుర్తింపు కోసం ఉమ్మడి వినతిపత్రం.\n"
                "మేము {STATE} రాష్ట్రం, {DISTRICT} జిల్లా మరియు {TEHSIL_TALUKA} తాలూకా వాసులం.\n"
                "మా నివాసం {VILLAGE} గ్రామం మరియు {GRAM_PANCHAYAT} పంచాయతీ పరిధిలోకి వస్తుంది.\n"
                "ఈ లేఖ {GRAM_SABHA} గ్రామ సభ ఏకాభిప్రాయం మరియు పూర్తి సమ్మతితో రాయబడింది.\n"
                "మేము {COMMUNITY_TYPE_FDST} మరియు {COMMUNITY_TYPE_OTFD} వర్గానికి చెందిన గిరిజనులు మరియు సాంప్రదాయ అటవీ నివాసులం.\n\n"

                "చట్టంలోని నిబంధనలకు అనుగుణంగా, మేము ఈ క్రింది సమిష్టి హక్కులను కోరుతున్నాము:\n"
                "నిస్తార్ మరియు ఉమ్మడి వినియోగ హక్కులు: {COMMUNITY_RIGHT_NISTAR}. లఘు అటవీ ఉత్పత్తుల హక్కు: {RIGHT_MINOR_FOREST_PRODUCE}.\n"
                "చెరువులు మరియు జల వనరులను ఉపయోగించుకునే హక్కు: {COMMUNITY_RIGHT_RESOURCE_USE}.\n"
                "పశువులను మేపే సమిష్టి హక్కు: {COMMUNITY_RIGHT_GRAZING}.\n"
                "సంచార సంఘాలకు పచ్చికబయళ్ల ప్రాప్యత హక్కు: {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS}.\n\n"

                "మా సాంప్రదాయ నివాసాల పట్టా {COMMUNITY_TENURE_HABITAT} రూపంలో మాకు అప్పగించాలి.\n"
                "మా జ్ఞానం మరియు జీవవైవిధ్యంపై మేధో హక్కు {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} నిర్ధారించబడాలి.\n"
                "మా జీవితాలకు సంబంధించిన ఇతర సాంప్రదాయ హక్కులన్నీ {OTHER_TRADITIONAL_RIGHT} కూడా చెల్లుబాటు కావాలి.\n"
                "ఈ దావాకు మద్దతుగా పటిష్టమైన సాక్ష్యంగా {EVIDENCE_ITEM} జతచేయబడ్డాయి.\n"
                "అదనపు సమాచారం {OTHER_INFORMATION} పరిపాలనా యంత్రాంగం దృష్టికి తీసుకురాబడుతోంది."
            ),
            # Variation 4: Legal / Statutory Declaration Style
            (
                "కమ్యూనిటీ అటవీ హక్కుల (Community Forest Rights) చట్టబద్ధమైన దావా మరియు ప్రకటన పత్రం.\n"
                "ఈ ప్రకటన {STATE} రాష్ట్రం, {DISTRICT} జిల్లా మరియు {TEHSIL_TALUKA} తాలూకా సంబంధిత అధికారుల ముందు సమర్పించబడుతోంది.\n"
                "ఈ దావా {VILLAGE} గ్రామస్తుల తరపున, {GRAM_PANCHAYAT} గ్రామ పంచాయతీ మరియు {GRAM_SABHA} గ్రామ సభ చట్టబద్ధమైన తీర్మానం ద్వారా ఆమోదించబడింది.\n"
                "అటవీ హక్కుల చట్టం 2006 కింద ఈ కమ్యూనిటీకి {COMMUNITY_TYPE_FDST} లేదా {COMMUNITY_TYPE_OTFD} గా చట్టపరమైన గుర్తింపు ఉంది.\n"
                "ఈ సంఘం యొక్క సమిష్టి హక్కులను చట్టబద్ధంగా పునరుద్ధరించడానికి ఈ పత్రం తయారు చేయబడింది.\n\n"

                "సెక్షన్ 3 కింద నిర్వచించబడిన సామాజిక వినియోగం మరియు వనరులపై హక్కుల జాబితా.\n"
                "సెక్షన్ 3(1)(b) కింద నిస్తార్ (Nistar) యొక్క చట్టబద్ధమైన హక్కులు {COMMUNITY_RIGHT_NISTAR} గా ప్రకటించబడ్డాయి.\n"
                "సెక్షన్ 3(1)(c) కింద లఘు అటవీ ఉత్పత్తులపై (MFP) యాజమాన్య హక్కు {RIGHT_MINOR_FOREST_PRODUCE} గా చెల్లుబాటు అవుతుంది.\n"
                "నీటి వనరులు మరియు మత్స్య సంపదను ఉపయోగించుకునే చట్టపరమైన హక్కు {COMMUNITY_RIGHT_RESOURCE_USE} గా నిర్ణయించబడింది.\n"
                "సాంప్రదాయ మేత హక్కులు {COMMUNITY_RIGHT_GRAZING} గా అధికారికంగా నమోదు చేయబడ్డాయి.\n"
                "సంచార సంఘాలకు వనరుల చట్టబద్ధమైన ప్రాప్యత {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS} నిర్ధారించబడింది.\n\n"

                "గిరిజన నివాస హక్కులు, మేధో సంపత్తి మరియు సమర్పించిన చట్టబద్ధమైన సాక్ష్యం.\n"
                "పిటిజి (PTG) మరియు వ్యవసాయ పూర్వ సంఘాలకు నివాస (Habitat) చట్టపరమైన హక్కు {COMMUNITY_TENURE_HABITAT} గా దావా వేయబడింది.\n"
                "సెక్షన్ 3(1)(k) ప్రకారం జీవవైవిధ్యం మరియు సాంప్రదాయ జ్ఞానాన్ని పొందే హక్కు {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} గా నమోదు చేయబడింది.\n"
                "చట్టం ద్వారా అందించబడిన అన్ని ఇతర ఆచార హక్కులు {OTHER_TRADITIONAL_RIGHT} మా సమిష్టి వారసత్వం.\n"
                "పై చట్టబద్ధమైన దావాలను నిరూపించడానికి డాక్యుమెంటరీ సాక్ష్యం {EVIDENCE_ITEM} జతచేయబడింది.\n"
                "చట్టపరమైన పరిశోధన ప్రయోజనాల కోసం ఇతర డేటా {OTHER_INFORMATION} అధికారికంగా సమర్పించబడుతుంది."
            )
        ],

        DOC_CLAIM_COMMUNITY_FOREST_RESOURCE: [
            # Variation 1: Bureaucratic / Form Style
            (
                "ఫారం - సి [చట్టంలోని సెక్షన్ 3(1)(i) మరియు నిబంధన 11(1) చూడండి]\n"
                "సామాజిక అటవీ వనరుల (CFR) హక్కుల కోసం దావా ఫారం.\n"
                "ఈ దావా {STATE} రాష్ట్రం, {DISTRICT} జిల్లా, మరియు {TEHSIL_TALUKA} తాలూకా పరిధిలోకి వస్తుంది.\n"
                "ఇది {GRAM_PANCHAYAT} గ్రామ పంచాయతీ పరిధిలోని {VILLAGE} గ్రామస్తుల తరపున సమర్పించబడుతోంది.\n"
                "ఈ ప్రతిపాదన {GRAM_SABHA} గ్రామ సభ సమావేశంలో ఏకగ్రీవంగా ఆమోదించబడింది.\n\n"

                "ఈ దావాను సమర్పిస్తున్న గ్రామ సభ ముఖ్య సభ్యులు {GRAM_SABHA_MEMBER_NAME}.\n"
                "ఈ సభ్యులు చట్టబద్ధంగా {CATEGORY_SCHEDULED_TRIBE} లేదా {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} వర్గానికి చెందినవారు.\n"
                "మేము దావా చేస్తున్న అటవీ వనరుల ప్రాంతం యొక్క ఖస్రా/కంపార్ట్‌మెంట్ నంబర్ {KHASRA_COMPARTMENT_NUMBER}.\n"
                "మా అటవీ ప్రాంతం సరిహద్దులో ఉన్న గ్రామాలు {BORDERING_VILLAGE}.\n"
                "ఈ ప్రాంతం యొక్క భౌగోళిక సరిహద్దులు {BOUNDARY_DESCRIPTION} గా స్పష్టంగా నిర్వచించబడ్డాయి.\n\n"

                "మా సమాజం తరతరాలుగా ఈ ప్రాంతాన్ని రక్షిస్తూ మరియు నిర్వహిస్తోంది.\n"
                "దీని కోసం, సామాజిక అటవీ వనరుల సాక్ష్యాల జాబితా {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} జతచేయబడింది.\n"
                "మా సాంప్రదాయ వినియోగాన్ని నిరూపించే ఇతర సాక్ష్యాలు {EVIDENCE_ITEM} గా సమర్పించబడ్డాయి.\n"
                "ఈ అటవీ వనరును స్థిరంగా ఉపయోగించుకునే హక్కు గ్రామ సభకు ఉందని మేము నిర్ధారిస్తున్నాము.\n"
                "సమర్థ అధికారి దీనిని పరిశీలించి సామాజిక అటవీ వనరుల హక్కును గుర్తించాలని అభ్యర్థిస్తున్నాము."
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "సామాజిక అటవీ వనరుల నిర్వహణ మరియు పరిరక్షణ కోసం గ్రామ సభ ఉమ్మడి ప్రకటన.\n"
                "మేము, {STATE} రాష్ట్రం {DISTRICT} జిల్లాలోని {TEHSIL_TALUKA} తాలూకా వాసులం.\n"
                "మా {VILLAGE} గ్రామం, {GRAM_PANCHAYAT} గ్రామ పంచాయతీ పరిపాలనా పరిధిలోకి వస్తుంది.\n"
                "ఈ రోజు {GRAM_SABHA} గ్రామ సభలో సమావేశమై, మా సాంప్రదాయ అటవీ వనరుల హక్కులను ప్రకటిస్తున్నాము.\n"
                "ఈ సభకు నాయకత్వం వహించే ముఖ్య సభ్యులు {GRAM_SABHA_MEMBER_NAME}.\n\n"

                "మేమంతా {CATEGORY_SCHEDULED_TRIBE} లేదా {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} వర్గానికి చెందిన సాంప్రదాయ అటవీ నివాసులం.\n"
                "మేము నిర్వహించే అటవీ ప్రాంతం యొక్క ఖస్రా/కంపార్ట్‌మెంట్ నంబర్ {KHASRA_COMPARTMENT_NUMBER} గా భూమి రికార్డులలో నమోదు చేయబడింది.\n"
                "మా అటవీ ప్రాంతం చుట్టూ ఉన్న పొరుగు గ్రామాలు {BORDERING_VILLAGE} గా పిలువబడతాయి.\n"
                "ఉత్తరాన నది మరియు దక్షిణాన కొండ వరకు విస్తరించి ఉన్న మా సరిహద్దుల వివరణ {BOUNDARY_DESCRIPTION}.\n"
                "ఈ సరిహద్దులో అందుబాటులో ఉన్న అన్ని వనరులను సంరక్షించే పూర్తి హక్కు మాకు ఉంది.\n\n"

                "జీవవైవిధ్యాన్ని కాపాడేందుకు, అడవుల నరికివేతను అడ్డుకునేందుకు కృతనిశ్చయంతో ఉన్నాం.\n"
                "మా వాదనను బలోపేతం చేయడానికి మేము సాక్ష్యాల జాబితాను {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} సిద్ధం చేసాము.\n"
                "మౌఖిక చరిత్ర మరియు చారిత్రక పత్రాలు {EVIDENCE_ITEM} గా సమర్పించబడ్డాయి.\n"
                "ఈ సాక్ష్యాల ఆధారంగా, సామాజిక అటవీ వనరుల హక్కు (CFR) మాకు వెంటనే మంజూరు చేయబడాలి.\n"
                "ప్రభుత్వ అధికారులు దీనిపై సత్వరమే విచారణ జరిపి ఆదేశాలు జారీ చేయాలని కోరుతున్నాం."
            ),
            # Variation 3: Formal Letter Style
            (
                "విషయం: సెక్షన్ 3(1)(i) కింద సామాజిక అటవీ వనరుల (CFR) పై హక్కు దావా.\n"
                "ప్రాంతం వివరాలు: తాలూకా {TEHSIL_TALUKA}, జిల్లా {DISTRICT}, రాష్ట్రం {STATE}.\n"
                "గ్రామం: {VILLAGE}, పంచాయతీ: {GRAM_PANCHAYAT}, గ్రామ సభ: {GRAM_SABHA}.\n"
                "ఈ దావా గ్రామ సభ సభ్యుడు {GRAM_SABHA_MEMBER_NAME} నేతృత్వంలో పరిపాలన యంత్రాంగం ముందు సమర్పించబడుతోంది.\n"
                "దరఖాస్తుదారులు ప్రధానంగా {CATEGORY_SCHEDULED_TRIBE} మరియు {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} వర్గానికి చెందినవారు.\n\n"

                "మేము రక్షిత అటవీ ప్రాంతం యొక్క ఖస్రా లేదా కంపార్ట్‌మెంట్ నంబర్ {KHASRA_COMPARTMENT_NUMBER}.\n"
                "మా సరిహద్దుకు ఆనుకొని ఉన్న సరిహద్దు గ్రామాలు {BORDERING_VILLAGE} ఈ అడవిని పంచుకోవు.\n"
                "మా సామాజిక అటవీ వనరుల భౌగోళిక సరిహద్దులు {BOUNDARY_DESCRIPTION} ప్రకారం మ్యాప్‌లో గుర్తించబడ్డాయి.\n"
                "ఈ ప్రాంతం యొక్క పర్యావరణ సమతుల్యతను కాపాడటం మా కమ్యూనిటీ యొక్క ప్రాథమిక విధి.\n"
                "అందువల్ల, ఈ అటవీ వనరులను నిర్వహించే పూర్తి హక్కు మా గ్రామ సభకు ఇవ్వాలి.\n\n"

                "ఈ భూమితో మా సాంప్రదాయ సంబంధాన్ని ధృవీకరించడానికి ఆధారాలు సంకలనం చేయబడ్డాయి.\n"
                "ముఖ్యమైన పత్రాల జాబితా {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} అధికారికంగా సమర్పించబడుతోంది.\n"
                "ఇతర బలమైన సాక్ష్యంగా {EVIDENCE_ITEM} పత్రాలు కూడా ఈ అప్లికేషన్‌తో జోడించబడ్డాయి.\n"
                "ఈ సాక్ష్యాలన్నీ మా దావా యొక్క ప్రామాణికత మరియు న్యాయబద్ధతను పూర్తిగా రుజువు చేస్తాయి.\n"
                "దీని ఆధారంగా, మా గ్రామ సభ యొక్క సామాజిక అటవీ వనరుల హక్కు ప్రభుత్వ గుర్తింపు పొందాలి."
            ),
            # Variation 4: Legal / Statutory Declaration Style
            (
                "సామాజిక అటవీ వనరుల (Community Forest Resource) దావాల చట్టబద్ధమైన ప్రకటన పత్రం.\n"
                "అటవీ హక్కుల చట్టం 2006, సెక్షన్ 3(1)(i) కింద, {STATE} రాష్ట్రం, {DISTRICT} జిల్లా, {TEHSIL_TALUKA} తాలూకా అధికారులకు సమర్పించిన చట్టబద్ధమైన దావా.\n"
                "ఈ అధికారిక డిమాండ్ {VILLAGE} గ్రామస్తుల తరపున, {GRAM_PANCHAYAT} గ్రామ పంచాయతీ మరియు {GRAM_SABHA} గ్రామ సభ ద్వారా సమర్పించబడుతుంది.\n"
                "గ్రామ సభ యొక్క అధీకృత చట్టపరమైన ప్రతినిధి {GRAM_SABHA_MEMBER_NAME} ఈ పత్రంపై సంతకం చేశారు.\n"
                "ఈ దావాలో పాలుపంచుకున్న సభ్యులు {CATEGORY_SCHEDULED_TRIBE} లేదా {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} అనే చట్టపరమైన వర్గం ద్వారా రక్షించబడతారు.\n\n"

                "క్లెయిమ్ చేయబడిన అటవీ వనరుల భౌగోళిక, భూమి కొలత మరియు సరిహద్దుల చట్టబద్ధమైన నమోదులు.\n"
                "దావా వేయబడిన అటవీ ప్రాంతం యొక్క చట్టబద్ధమైన ఖస్రా (Khasra) లేదా అటవీ శాఖ కంపార్ట్‌మెంట్ నంబర్ {KHASRA_COMPARTMENT_NUMBER} రెవెన్యూ రికార్డులలో నమోదు చేయబడింది.\n"
                "రెవెన్యూ మ్యాప్ ప్రకారం, ఈ ప్రాంతంతో సరిహద్దులను పంచుకునే పొరుగు గ్రామాలు {BORDERING_VILLAGE}.\n"
                "మొత్తం క్లెయిమ్ చేయబడిన అటవీ వనరుల భౌగోళిక మరియు స్థలాకృతి సరిహద్దులు {BOUNDARY_DESCRIPTION} గా చాలా స్పష్టంగా నిర్వచించబడ్డాయి.\n"
                "ఈ సరిహద్దులలో ఉన్న అటవీ వనరులను నిరంతరం ఉపయోగించుకోవడానికి మరియు నిర్వహించడానికి ఈ సంఘానికి చట్టబద్ధమైన హక్కు ఉంది.\n"
                "ఈ ప్రాంతంలో అటవీ సంపద పునరుత్పత్తి బాధ్యత మరియు హక్కు చట్టబద్ధంగా గ్రామ సభకు అప్పగించాలి.\n\n"

                "ప్రామాణికమైన సాక్ష్యాల సమర్పణ మరియు చట్టపరమైన దావాల నిర్ధారణ.\n"
                "ఈ కమ్యూనిటీ యొక్క సాంప్రదాయ కనెక్షన్‌ను ధృవీకరించడానికి, సాక్ష్యాల అధికారిక జాబితా {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} జోడించబడింది.\n"
                "అదే సమయంలో, గ్రామ రికార్డులు మరియు చారిత్రక పత్రాల వంటి అదనపు నిర్ధారణ సాక్ష్యం {EVIDENCE_ITEM} గా సమర్పించబడింది.\n"
                "ఈ పత్రాలన్నీ చట్టంలోని రూల్ 13 కింద చట్టపరమైన సాక్ష్యంగా ఆమోదయోగ్యమైనవి మరియు చెల్లుబాటు అయ్యేవి.\n"
                "ఈ సాక్ష్యాల ఆధారంగా, మొత్తం ప్రాంతం యొక్క పరిరక్షణ మరియు అభివృద్ధికి చట్టబద్ధమైన హక్కును గ్రామ సభకు అందించడం తప్పనిసరి.\n"
                "చట్టపరమైన నిబంధనల ప్రకారం, ఈ దావాను త్వరగా సమీక్షించాలని మరియు గెజిటెడ్ ఆర్డర్ జారీ చేయాలని అభ్యర్థించబడింది."
            )
        ],

        DOC_TITLE_UNDER_OCCUPATION: [
            # Variation 1: Bureaucratic / Form Style
            (
                "అనుబంధం - II [నిబంధన 8(h) చూడండి]\n"
                "ఆక్రమణలో ఉన్న అటవీ భూమికి అధికారిక హక్కు పత్రం / పట్టా.\n"
                "అటవీ భూమి యొక్క ఈ హక్కు పత్రం రాష్ట్ర ప్రభుత్వం ద్వారా {TITLE_HOLDER_NAME} కి మంజూరు చేయబడింది.\n"
                "పట్టాదారు తండ్రి/తల్లి పేరు {FATHER_MOTHER_NAME} మరియు జీవిత భాగస్వామి పేరు {SPOUSE_NAME}.\n"
                "వీరిపై ఆధారపడిన వ్యక్తులు {DEPENDENT_NAME} కూడా ఈ అధికార పత్రం రక్షణ పరిధిలోకి వస్తారు.\n\n"

                "పట్టాదారు పూర్తి నమోదిత చిరునామా {TITLE_ADDRESS_FULL}.\n"
                "ఈ అటవీ భూమి {VILLAGE} గ్రామం మరియు {GRAM_PANCHAYAT} గ్రామ పంచాయతీ భౌగోళిక ప్రాంతంలో ఉంది.\n"
                "ఇది {GRAM_SABHA} గ్రామ సభ పరిధిలో, {TEHSIL_TALUKA} తాలూకా కింద వస్తుంది.\n"
                "ఇది జిల్లా {DISTRICT} మరియు రాష్ట్రం {STATE} యొక్క పరిపాలనా నియంత్రణలో ఉంది.\n"
                "పట్టాదారు {CATEGORY_SCHEDULED_TRIBE} లేదా {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} వర్గానికి చెందిన అర్హతగల సభ్యుడని ధృవీకరించబడింది.\n\n"

                "ఈ పత్రం ద్వారా హక్కు కల్పించబడిన అటవీ భూమి మొత్తం విస్తీర్ణం {TITLE_LAND_AREA_MEASURE}.\n"
                "భూ రికార్డులలో ఈ భూమి యొక్క ఖస్రా లేదా కంపార్ట్‌మెంట్ నంబర్ {KHASRA_COMPARTMENT_NUMBER} గా నమోదు చేయబడింది.\n"
                "భూమికి నాలుగు దిక్కులా ఉన్న సరిహద్దులు సహజ గుర్తుల ద్వారా {BOUNDARY_DESCRIPTION} గా వివరించబడ్డాయి.\n"
                "ఈ హక్కు వారసత్వంగా వస్తుంది, కానీ దీనిని విక్రయించడం లేదా బదిలీ చేయడం సాధ్యపడదు.\n"
                "జిల్లా కలెక్టర్ మరియు డివిజనల్ ఫారెస్ట్ ఆఫీసర్ సంతకాలతో ఇది అధికారికంగా జారీ చేయబడింది."
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "గిరిజన వ్యవహారాల మంత్రిత్వ శాఖ జారీ చేసిన వ్యక్తిగత అటవీ భూమి హక్కు పత్రం (పట్టా).\n"
                "శ్రీ/శ్రీమతి {TITLE_HOLDER_NAME} (తండ్రి/తల్లి: {FATHER_MOTHER_NAME}, భర్త/భార్య: {SPOUSE_NAME}) కు ఈ పట్టా అందించబడుతోంది.\n"
                "వారితో పాటు ఆధారపడిన {DEPENDENT_NAME} వంటి ఇతర కుటుంబ సభ్యుల హక్కు కూడా ఈ భూమిపై సురక్షితంగా ఉంటుంది.\n"
                "వీరి నివాస చిరునామా ప్రభుత్వ రికార్డులలో {TITLE_ADDRESS_FULL} గా సక్రమంగా నమోదు చేయబడింది.\n"
                "ఈ ప్రాంతం {STATE} రాష్ట్రం, {DISTRICT} జిల్లాలోని {TEHSIL_TALUKA} తాలూకా కింద వస్తుంది.\n\n"

                "ఈ ప్లాట్ {VILLAGE} గ్రామంలో, {GRAM_PANCHAYAT} పంచాయతీ కింద, {GRAM_SABHA} గ్రామ సభ నియంత్రణలో ఉంది.\n"
                "లబ్ధిదారుడు గిరిజన వర్గం {CATEGORY_SCHEDULED_TRIBE} లేదా సాంప్రదాయ అటవీ నివాసి {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} గా గుర్తించబడ్డాడు.\n"
                "వ్యవసాయం మరియు నివాస ప్రయోజనాల కోసం ప్రభుత్వం వీరికి {TITLE_LAND_AREA_MEASURE} విస్తీర్ణం గల భూమిని కేటాయించింది.\n"
                "రెవెన్యూ రికార్డులలో ఆ భూమి యొక్క ఖస్రా (Khasra) లేదా కొలత సంఖ్య {KHASRA_COMPARTMENT_NUMBER} స్పష్టంగా గుర్తించబడింది.\n"
                "స్థలం యొక్క ఖచ్చితమైన స్థానం మరియు చుట్టుకొలత {BOUNDARY_DESCRIPTION} డీలిమిటేషన్ వివరాల ద్వారా డాక్యుమెంట్ చేయబడింది.\n\n"

                "ఈ అటవీ భూమి పట్టా అటవీ హక్కుల చట్టం 2006 లోని అన్ని నిబంధనలకు లోబడి ఉంటుంది.\n"
                "ఈ భూమిని సాగు చేసుకునేందుకు, తరతరాలుగా అనుభవించే హక్కు మాత్రమే పట్టాదారునికి ఉంటుంది.\n"
                "ఎట్టి పరిస్థితుల్లోనూ ఈ అటవీ భూమిని ఇతరులకు విక్రయించకూడదు లేదా కౌలుకు ఇవ్వకూడదు.\n"
                "ఇది సంబంధిత శాఖాధికారులచే రాష్ట్ర ప్రభుత్వ అధికారిక ముద్రతో ధృవీకరించబడింది.\n"
                "ఈ పత్రం పట్టాదారుడి జీవనోపాధిని రక్షించే చట్టపరమైన కవచంగా పనిచేస్తుంది."
            ),
            # Variation 3: Formal Letter Style
            (
                "అటవీ భూమి హక్కు ఉత్తర్వు మరియు పట్టా ధృవీకరణ పత్రం.\n"
                "హక్కుదారు పేరు: {TITLE_HOLDER_NAME}. తల్లిదండ్రుల పేరు: {FATHER_MOTHER_NAME}. జీవిత భాగస్వామి: {SPOUSE_NAME}.\n"
                "ఆధారపడిన సభ్యులు: {DEPENDENT_NAME}. హక్కుదారు వర్గం: {CATEGORY_SCHEDULED_TRIBE} / {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER}.\n"
                "చిరునామా: {TITLE_ADDRESS_FULL}, గ్రామం: {VILLAGE}, పంచాయతీ: {GRAM_PANCHAYAT}, గ్రామ సభ: {GRAM_SABHA}.\n"
                "తాలూకా: {TEHSIL_TALUKA}, జిల్లా: {DISTRICT}, రాష్ట్రం: {STATE}.\n\n"

                "అటవీ హక్కుల చట్టం 2006 లోని సెక్షన్ 4 కింద ఈ భూమి హక్కు అధికారికంగా గుర్తించబడింది.\n"
                "పై లబ్ధిదారుడి ఆధీనంలో ఉన్న {TITLE_LAND_AREA_MEASURE} విస్తీర్ణంలో ఉన్న భూమికి పట్టా ఇవ్వబడుతోంది.\n"
                "రెవెన్యూ శాఖ రికార్డుల ప్రకారం ఈ భూమి ఖస్రా నంబర్ {KHASRA_COMPARTMENT_NUMBER}.\n"
                "భూమి సరిహద్దులు {BOUNDARY_DESCRIPTION} మార్కులతో ఖచ్చితంగా నిర్వచించబడ్డాయి.\n"
                "అన్ని విచారణలు మరియు ధృవీకరణల తర్వాత, జిల్లా స్థాయి కమిటీ (DLC) ఈ భూమి కేటాయింపుకు ఆమోదం తెలిపింది.\n\n"

                "ఈ భూమి హక్కు వారసత్వ హక్కుగా కొనసాగుతుంది, అయితే భూమి బదిలీ చేయబడదు (non-transferable).\n"
                "ఎప్పటికప్పుడు ప్రభుత్వం అమలు చేసే అటవీ సంరక్షణ నియమాలకు లబ్ధిదారుడు కట్టుబడి ఉండాలి.\n"
                "దీని ద్వారా అటవీవాసుల ఆర్థిక, సామాజిక భద్రతను ప్రభుత్వం కల్పిస్తోంది.\n"
                "ఈ ధృవీకరణ పత్రం రాష్ట్ర ప్రభుత్వ అధీకృత అధికారులచే సంతకం చేయబడి, ముద్ర వేయబడింది.\n"
                "ఈ పత్రం జారీ చేసిన తేదీ నుండి చట్టబద్ధంగా అమలులోకి వస్తుంది."
            ),
            # Variation 4: Legal / Statutory Document Style
            (
                "అటవీ భూమి హక్కుల చట్టం 2006 కింద చట్టబద్ధమైన పట్టా దస్తావేజు (Statutory Title Deed).\n"
                "రాష్ట్ర ప్రభుత్వ చట్టపరమైన అధికారాలకు లోబడి, ఈ హక్కు పత్రం {TITLE_HOLDER_NAME} అనే లబ్ధిదారుని అనుకూలంగా చట్టబద్ధంగా నమోదు చేయబడుతుంది.\n"
                "రికార్డుల ప్రకారం లబ్ధిదారుని తండ్రి/తల్లి పేరు {FATHER_MOTHER_NAME} మరియు చట్టపరమైన జీవిత భాగస్వామి పేరు {SPOUSE_NAME} ధృవీకరించబడింది.\n"
                "లబ్ధిదారునిపై పూర్తిగా ఆధారపడిన చట్టబద్ధమైన వారసుల పేర్లు {DEPENDENT_NAME} కూడా ఈ డీడ్‌లో చేర్చబడ్డాయి.\n"
                "లబ్ధిదారుని అధికారిక మరియు చట్టబద్ధమైన నివాస చిరునామా {TITLE_ADDRESS_FULL} గా రెవెన్యూ మరియు అటవీ రికార్డులలో నమోదు చేయబడింది.\n"
                "ఈ ప్లాట్ {STATE} రాష్ట్రం, {DISTRICT} జిల్లా, {TEHSIL_TALUKA} తాలూకా పరిధిలోని {VILLAGE} గ్రామం, {GRAM_PANCHAYAT} గ్రామ పంచాయతీ మరియు {GRAM_SABHA} గ్రామ సభ చట్టబద్ధమైన అధికార పరిధిలో ఉంది.\n\n"

                "లబ్ధిదారుల చట్టపరమైన వర్గీకరణ, భూ కొలత మరియు భౌగోళిక సరిహద్దుల ధృవీకరణ.\n"
                "చట్టంలోని చట్టపరమైన నిబంధనల కింద లబ్ధిదారుడు {CATEGORY_SCHEDULED_TRIBE} లేదా {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} వర్గానికి చెందిన అర్హతగల సభ్యుడిగా పరిగణించబడ్డాడు.\n"
                "ప్రభుత్వం ద్వారా సక్రమంగా కొలవబడిన తర్వాత కేటాయించబడిన అటవీ భూమి మొత్తం విస్తీర్ణం {TITLE_LAND_AREA_MEASURE} గా ప్రకటించబడింది.\n"
                "రెవెన్యూ మరియు అటవీ రికార్డులలో ఈ భూమి యొక్క నిర్దిష్ట ఖస్రా (Khasra) లేదా కంపార్ట్‌మెంట్ నంబర్ {KHASRA_COMPARTMENT_NUMBER} నమోదు చేయబడింది.\n"
                "ఈ ప్లాట్ యొక్క నాలుగు దిశల భౌగోళిక మరియు సహజ సరిహద్దులు {BOUNDARY_DESCRIPTION} గా చాలా స్పష్టంగా గుర్తించబడ్డాయి.\n"
                "రెవెన్యూ ఇన్‌స్పెక్టర్ మరియు అటవీ శాఖ సర్వేయర్లచే ప్రత్యక్ష భౌతిక ధృవీకరణ తర్వాత ఈ కొలత చేయబడింది.\n\n"

                "హక్కు యొక్క చట్టపరమైన స్వభావం, పరిమితులు మరియు అధికారుల ధృవీకరణ.\n"
                "సెక్షన్ 4(4) నిబంధనల ప్రకారం, ఈ భూమి హక్కు పూర్తిగా వంశపారంపర్యమైనది, అయితే దానిని ఏ పరిస్థితుల్లోనూ విక్రయించకూడదు, బదిలీ చేయకూడదు లేదా కుదువ పెట్టకూడదు (non-alienable).\n"
                "అటవీ పరిరక్షణ చట్టాలు మరియు పర్యావరణ పరిరక్షణ నియమాలకు అనుగుణంగా లబ్ధిదారుడు చట్టబద్ధంగా కట్టుబడి ఉంటాడు.\n"
                "నిబంధనల ఉల్లంఘన జరిగినట్లు తేలితే, ముందస్తు నోటీసు లేకుండా ఈ హక్కును రద్దు చేసే పూర్తి అధికారం రాష్ట్ర ప్రభుత్వానికి ఉంది.\n"
                "ఈ చట్టబద్ధమైన పట్టా సబ్-డివిజనల్ (SDLC) మరియు జిల్లా స్థాయి (DLC) కమిటీల సక్రమ ఆమోదం తర్వాత మాత్రమే జారీ చేయబడింది.\n"
                "దాని చట్టబద్ధమైన నిర్ధారణ కోసం, జిల్లా కలెక్టర్ మరియు డివిజనల్ ఫారెస్ట్ ఆఫీసర్ (DFO) ఈ పట్టాపై అధికారిక సంతకాలు మరియు ముద్రలు వేశారు."
            )
        ],

        DOC_TITLE_COMMUNITY_FOREST_RIGHTS: [
            # Variation 1: Bureaucratic / Form Style
            (
                "అనుబంధం - III [నిబంధన 8(h) చూడండి]\n"
                "సామాజిక అటవీ హక్కుల కోసం పట్టా మరియు అధికారిక హక్కు పత్రం.\n"
                "ఈ సామాజిక అటవీ హక్కు {COMMUNITY_RIGHT_HOLDER_NAME} అనే కమ్యూనిటీ సంస్థకు మంజూరు చేయబడింది.\n"
                "ఈ ప్రాంతం {STATE} రాష్ట్రం, {DISTRICT} జిల్లా మరియు {TEHSIL_TALUKA} తాలూకా పరిధిలోకి వస్తుంది.\n"
                "ఈ పట్టా {VILLAGE} గ్రామం, {GRAM_PANCHAYAT} గ్రామ పంచాయతీ మరియు {GRAM_SABHA} గ్రామ సభ సమిష్టి ఆస్తి.\n\n"

                "ఈ హక్కు పొందిన సంఘం {CATEGORY_SCHEDULED_TRIBE} లేదా {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} గా గుర్తించబడింది.\n"
                "సంఘానికి మంజూరు చేయబడిన హక్కు స్వభావం {COMMUNITY_RIGHT_NATURE} గా స్పష్టంగా నిర్వచించబడింది.\n"
                "ఈ హక్కు వినియోగానికి సంబంధించిన కొన్ని షరతులు ఉన్నాయి, అవి: {TITLE_CONDITIONS}.\n"
                "ఈ హక్కు పరిధిలోకి వచ్చే అటవీ ప్రాంతం ఖస్రా/కంపార్ట్‌మెంట్ నంబర్ {KHASRA_COMPARTMENT_NUMBER}.\n"
                "భూమి సరిహద్దులు భౌగోళిక సూచనల ద్వారా {BOUNDARY_DESCRIPTION} గా సూచించబడతాయి.\n\n"

                "అదనంగా, ఈ ప్రాంతం యొక్క సాంప్రదాయ కస్టమరీ సరిహద్దు (Customary Boundary) {CUSTOMARY_BOUNDARY} కూడా సాంప్రదాయకంగా గుర్తించబడింది.\n"
                "ఈ పత్రం కమ్యూనిటీ ఉపయోగం కోసం అటవీ వనరుల ప్రాప్యతకు చట్టపరమైన గుర్తింపును అందిస్తుంది.\n"
                "అయితే, అటవీ జీవవైవిధ్యానికి ఎలాంటి నష్టం వాటిల్లని విధంగా వనరులను వినియోగించుకోవాలి.\n"
                "నిబంధనలను ఉల్లంఘిస్తే, ఈ హక్కును పునఃపరిశీలించే అధికారం ప్రభుత్వానికి ఉంది.\n"
                "ఈ పట్టా జిల్లా స్థాయి అధికారులచే ఆమోదించబడి జారీ చేయబడింది."
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "సమిష్టి అటవీ హక్కు పట్టా మరియు గ్రామ సభకు చట్టబద్ధమైన అధికారాన్ని అప్పగించే పత్రం.\n"
                "ప్రభుత్వ ఆమోదంతో, ఈ హక్కు {COMMUNITY_RIGHT_HOLDER_NAME} సంస్థ/కమ్యూనిటీకి ఇవ్వబడింది.\n"
                "ఈ కమ్యూనిటీ చాలా కాలంగా {STATE} రాష్ట్రం {DISTRICT} జిల్లాలో ఉన్న {TEHSIL_TALUKA} తాలూకాలో నివసిస్తోంది.\n"
                "వీరి నివాస ప్రాంతం {VILLAGE} గ్రామం, {GRAM_PANCHAYAT} పంచాయతీ మరియు {GRAM_SABHA} గ్రామ సభలో కవర్ చేయబడింది.\n"
                "అధికారిక రికార్డులలో వీరు {CATEGORY_SCHEDULED_TRIBE} మరియు {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} వర్గంగా నమోదు చేయబడ్డారు.\n\n"

                "వీరికి మంజూరు చేయబడిన సమిష్టి హక్కు యొక్క ఖచ్చితమైన స్వభావం {COMMUNITY_RIGHT_NATURE} గా వివరించబడింది.\n"
                "ఈ కమ్యూనిటీ హక్కు వినియోగానికి నిర్దేశించిన నియమాలు మరియు షరతులు {TITLE_CONDITIONS}.\n"
                "అటవీ శాఖ రికార్డుల ప్రకారం, ఈ ప్రాంతం యొక్క ఖస్రా నంబర్ {KHASRA_COMPARTMENT_NUMBER} గా గుర్తించబడింది.\n"
                "ఈ ప్రాంతం యొక్క సరిహద్దులు సహజ గుర్తులను ఉపయోగించి {BOUNDARY_DESCRIPTION} గా వివరించబడ్డాయి.\n"
                "అలాగే, తరతరాలుగా అనుసరిస్తున్న సాంప్రదాయ సరిహద్దు {CUSTOMARY_BOUNDARY} గా నిర్ధారించబడింది.\n\n"

                "ఈ పత్రం ద్వారా సంఘం పచ్చికబయళ్ళు మరియు లఘు అటవీ ఉత్పత్తుల సేకరణ హక్కులను రక్షిస్తుంది.\n"
                "పర్యావరణాన్ని, అటవీ ప్రాంతాన్ని పరిరక్షించే బాధ్యత ఇదే సంఘానికి అప్పగిస్తున్నారు.\n"
                "అక్రమ చెట్లు నరకడం, వేట వంటి చట్ట వ్యతిరేక కార్యకలాపాలు పూర్తిగా నిషేధించబడ్డాయి.\n"
                "రాష్ట్ర ప్రభుత్వ గిరిజన సంక్షేమ శాఖ మరియు రెవెన్యూ శాఖల సమ్మతితో ఇది జారీ చేయబడింది.\n"
                "గ్రామ సభ ఈ పత్రాన్ని భద్రపరచాలి మరియు దాని నిబంధనలను సక్రమంగా అమలు చేయాలి."
            ),
            # Variation 3: Formal Letter Style
            (
                "కమ్యూనిటీ అటవీ హక్కులను గుర్తించే అధికారిక సర్టిఫికేట్ (Title Certificate).\n"
                "లబ్ధిదారు: {COMMUNITY_RIGHT_HOLDER_NAME}.\n"
                "ప్రాంతం: {VILLAGE} గ్రామం, {GRAM_PANCHAYAT} పంచాయతీ, {GRAM_SABHA} గ్రామ సభ.\n"
                "పరిపాలనా సరిహద్దులు: తాలూకా {TEHSIL_TALUKA}, జిల్లా {DISTRICT}, రాష్ట్రం {STATE}.\n"
                "లబ్ధిదారుని వర్గం: {CATEGORY_SCHEDULED_TRIBE} లేదా {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER}.\n\n"

                "పై సంఘానికి రాష్ట్ర ప్రభుత్వం ద్వారా {COMMUNITY_RIGHT_NATURE} స్వభావం గల అటవీ హక్కులు మంజూరు చేయబడ్డాయి.\n"
                "ఈ హక్కు {TITLE_CONDITIONS} లో పేర్కొన్న పరిమితులు మరియు షరతులకు లోబడి ఉంటుంది.\n"
                "కేటాయించబడిన అటవీ భూమి యొక్క ఖస్రా లేదా కొలత సంఖ్య {KHASRA_COMPARTMENT_NUMBER} గా నిర్ణయించబడింది.\n"
                "పత్రాలలో పేర్కొన్న భూమి సరిహద్దులు {BOUNDARY_DESCRIPTION} మార్కుల ద్వారా నిర్ణయించబడతాయి.\n"
                "సంఘంచే సాంప్రదాయకంగా గుర్తించబడిన ఆచార సరిహద్దు {CUSTOMARY_BOUNDARY} కూడా ధృవీకరించబడింది.\n\n"

                "ఈ హక్కు గ్రామ సభ సమిష్టి నిర్వహణలో మాత్రమే వినియోగించబడాలి.\n"
                "అటవీ వనరులను వాణిజ్య ప్రయోజనాల కోసం కాకుండా సామాజిక అవసరాల కోసం మాత్రమే ఉపయోగించాలి.\n"
                "ప్రభుత్వ ఆడిట్‌లు మరియు తనిఖీలలో గ్రామ సభ పూర్తి సహకారం అందించడం తప్పనిసరి.\n"
                "ఈ పత్రం జిల్లా కలెక్టర్ మరియు డివిజనల్ ఫారెస్ట్ ఆఫీసర్ ముద్రతో జారీ చేయబడింది.\n"
                "జారీ చేసిన తేదీ నుండి, సంఘం యొక్క అటవీ ఆధారిత ఆర్థిక స్వాతంత్ర్యం నిర్ధారించబడుతుంది."
            ),
            # Variation 4: Legal / Statutory Document Style
            (
                "సమిష్టి అటవీ హక్కుల (CFR) చట్టబద్ధమైన దస్తావేజు మరియు పట్టా.\n"
                "ఈ అధికారిక దస్తావేజు ద్వారా, {COMMUNITY_RIGHT_HOLDER_NAME} అనే కమ్యూనిటీ సంస్థకు అటవీ భూమిపై చట్టపరమైన హక్కులు మంజూరు చేయబడ్డాయి.\n"
                "ఈ హక్కు {STATE} రాష్ట్రం, {DISTRICT} జిల్లా మరియు {TEHSIL_TALUKA} తాలూకా భౌగోళిక అధికార పరిధిలో మంజూరు చేయబడింది.\n"
                "చట్టపరంగా ఈ ప్రాంతం {VILLAGE} గ్రామం, {GRAM_PANCHAYAT} గ్రామ పంచాయతీ మరియు {GRAM_SABHA} గ్రామ సభ పరిపాలనా నియంత్రణలో వస్తుంది.\n"
                "హక్కు పొందే ఈ కమ్యూనిటీ, ప్రభుత్వ రికార్డుల ప్రకారం {CATEGORY_SCHEDULED_TRIBE} లేదా {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} చట్టపరమైన వర్గం కింద రక్షించబడింది.\n"
                "గ్రామ సభ సమిష్టి తీర్మానం మరియు జిల్లా స్థాయి కమిటీ (DLC) ఆమోదం ఆధారంగా ఈ పత్రం చట్టబద్ధంగా జారీ చేయబడుతుంది.\n\n"

                "ఆమోదించబడిన సామాజిక హక్కు యొక్క స్వభావం, షరతులు మరియు భౌగోళిక డాక్యుమెంటేషన్.\n"
                "ప్రభుత్వం ద్వారా ఈ కమ్యూనిటీకి అధికారికంగా మంజూరు చేయబడిన హక్కు స్వభావం స్పష్టంగా {COMMUNITY_RIGHT_NATURE} గా నిర్వచించబడింది.\n"
                "ఈ హక్కు వినియోగానికి అటవీ శాఖ విధించిన చట్టపరమైన షరతులు మరియు ఆంక్షలు ఈ క్రింది విధంగా ఉన్నాయి: {TITLE_CONDITIONS}.\n"
                "కమ్యూనిటీ హక్కుల పరిధిలోకి వచ్చే అటవీ ప్రాంతం యొక్క చట్టబద్ధమైన ఖస్రా లేదా కొలత సంఖ్య {KHASRA_COMPARTMENT_NUMBER} గా నమోదు చేయబడింది.\n"
                "భూమి సరిహద్దులు పర్వతాలు, నదుల వంటి సహజ గుర్తులను సూచిస్తూ {BOUNDARY_DESCRIPTION} గా పత్రబద్ధం చేయబడ్డాయి.\n"
                "అదే సమయంలో, అనేక తరాలుగా కమ్యూనిటీచే గుర్తించబడిన కస్టమరీ సరిహద్దు (Customary Boundary) {CUSTOMARY_BOUNDARY} చట్టబద్ధంగా ధృవీకరించబడింది.\n\n"

                "సంఘం యొక్క చట్టపరమైన బాధ్యతలు, పరిమితులు మరియు ప్రభుత్వం యొక్క తుది ఆమోదం.\n"
                "ఈ హక్కు ధృవీకరణ పత్రం పూర్తిగా కమ్యూనిటీ ఉపయోగం కోసం ఉద్దేశించబడింది; ఏ రకమైన వాణిజ్యపరమైన దోపిడీ (Commercial exploitation) అనుమతించబడదు.\n"
                "పశువులు మేపడం మరియు అటవీ ఫలసాయం సేకరించడంతో పాటు, అటవీ జీవవైవిధ్యానికి ఎలాంటి నష్టం వాటిల్లకుండా చూసుకోవడం సంఘం యొక్క చట్టపరమైన బాధ్యత.\n"
                "చట్టవిరుద్ధంగా చెట్లు నరకడం లేదా రాజ్య వ్యతిరేక కార్యకలాపాలకు పాల్పడినట్లయితే, ఈ హక్కు తక్షణమే రద్దు చేయబడుతుంది.\n"
                "ఈ పత్రం గిరిజన సంక్షేమ శాఖ మరియు అటవీ శాఖ రెండింటి పూర్తి సమన్వయంతో నిర్వహించబడుతుంది.\n"
                "జిల్లా కలెక్టర్ (DM) మరియు సంబంధిత అటవీ అధికారుల అధికారిక ముద్ర మరియు సంతకంతో ఈ పట్టా గెజిట్‌లో నమోదు చేయబడింది."
            )
        ],

        DOC_TITLE_COMMUNITY_FOREST_RESOURCES: [
            # Variation 1: Bureaucratic / Form Style
            (
                "అనుబంధం - IV [నిబంధన 8(i) చూడండి]\n"
                "సామాజిక అటవీ వనరుల (CFR) కోసం పట్టా మరియు హక్కు పత్రం.\n"
                "ఈ అధికారిక పత్రం {STATE} రాష్ట్రం, {DISTRICT} జిల్లా, {TEHSIL_TALUKA} తాలూకా పరిధిలోని ప్రాంతానికి మంజూరు చేయబడింది.\n"
                "దీని ప్రకారం, {VILLAGE} గ్రామం, {GRAM_PANCHAYAT} గ్రామ పంచాయతీ మరియు {GRAM_SABHA} గ్రామ సభకు సామాజిక అటవీ వనరుల హక్కు ఇవ్వబడింది.\n"
                "ఈ హక్కు {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} లేదా {COMMUNITY_TYPE_BOTH} సంఘాలకు చెందిన ప్రజల కోసం ఉద్దేశించబడింది.\n\n"

                "ఈ సామాజిక అటవీ వనరుల హక్కు పరిధిలోకి వచ్చే ప్రాంతం యొక్క ఖస్రా/కంపార్ట్‌మెంట్ నంబర్లు {KHASRA_COMPARTMENT_NUMBER}.\n"
                "ఈ ప్రాంతం యొక్క భౌగోళిక స్థానం మరియు సరిహద్దులు {BOUNDARY_DESCRIPTION} గా చాలా స్పష్టంగా పత్రబద్ధం చేయబడ్డాయి.\n"
                "అదే సమయంలో, శతాబ్దాలుగా ఉన్న సాంప్రదాయ కస్టమరీ సరిహద్దు {CUSTOMARY_BOUNDARY} చట్టబద్ధంగా గుర్తించబడింది.\n"
                "నిర్దేశిత ప్రాంతంలోని అన్ని లఘు అటవీ ఉత్పత్తులను నిర్వహించే అధికారం గ్రామ సభకు అప్పగించబడింది.\n"
                "అటవీ శాఖ మార్గదర్శకాల ప్రకారం, సంఘం ఈ వనరులను సంరక్షించాలి మరియు స్థిరంగా ఉపయోగించాలి.\n\n"

                "గిరిజనులు మరియు ఇతర సాంప్రదాయ అటవీ నివాసుల జీవనోపాధిని మెరుగుపరిచే ఉద్దేశ్యంతో ఈ హక్కు మంజూరు చేయబడింది.\n"
                "అటవీ వనరుల నిర్వహణ కోసం కమిటీలను ఏర్పాటు చేసే పూర్తి అధికారం గ్రామ సభకు ఇవ్వబడింది.\n"
                "ఈ వనరులను దెబ్బతీసే ఏదైనా చర్య చట్టపరమైన నేరంగా పరిగణించబడుతుంది మరియు హక్కులు రద్దు చేయబడతాయి.\n"
                "జిల్లా కలెక్టర్ మరియు అటవీ అధికారి వంటి రాష్ట్ర ప్రభుత్వ సమర్థ అధికారులు దీన్ని సక్రమంగా ఆమోదించారు.\n"
                "సామాజిక అటవీ వనరుల పరిరక్షణలో ఒక ముఖ్యమైన మైలురాయిగా ఈ పత్రం నమోదు చేయబడుతోంది."
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "సమిష్టి అటవీ వనరుల కోసం చట్టబద్ధమైన హక్కు దస్తావేజు మరియు గ్రామ సభకు అధికార బదిలీ.\n"
                "ప్రభుత్వం {STATE} రాష్ట్రం {DISTRICT} జిల్లాలోని {TEHSIL_TALUKA} తాలూకాలో నివసిస్తున్న ప్రజల డిమాండ్‌ను అంగీకరించింది.\n"
                "దీని ఆధారంగా {VILLAGE} గ్రామం, {GRAM_PANCHAYAT} పంచాయతీ మరియు {GRAM_SABHA} గ్రామ సభకు CFR పట్టా మంజూరు చేయబడింది.\n"
                "ఈ హక్కు గుర్తింపు {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} లేదా {COMMUNITY_TYPE_BOTH} వర్గాలకు వర్తిస్తుంది.\n"
                "అడవిని దేవుడిగా భావించి రక్షించే సంప్రదాయం ఉన్న కమ్యూనిటీలు ఇవి.\n\n"

                "సామాజిక అటవీ వనరుల ప్రాంతం కోసం ఖస్రా/కంపార్ట్‌మెంట్ నంబర్ {KHASRA_COMPARTMENT_NUMBER} భూ కొలత రికార్డులలో పేర్కొనబడింది.\n"
                "ఈ ప్రాంతం యొక్క సరిహద్దులు పర్వతాలు మరియు నదులను సూచిస్తూ {BOUNDARY_DESCRIPTION} గా నిర్వచించబడ్డాయి.\n"
                "దీనికి మించి మా సాంప్రదాయ ఆచార సరిహద్దు {CUSTOMARY_BOUNDARY} ని కూడా ప్రభుత్వం ఆమోదించింది.\n"
                "ఈ పరిమితిలో లభించే వంటచెరకు, తేనె మరియు మూలికలను స్వేచ్ఛగా వినియోగించుకునే హక్కు గ్రామ సభకు ఉంది.\n"
                "అంతేకాకుండా, అటవీ మాఫియా నుండి అడవిని రక్షించే పూర్తి బాధ్యత ఇదే సంఘానికి అప్పగించబడింది.\n\n"

                "సామాజిక అటవీ వనరుల హక్కుల చట్టం ఆదివాసీ ప్రజల స్వయం నిర్ణయాధికారాన్ని నిర్ధారిస్తుంది.\n"
                "జీవవైవిధ్యాన్ని కాపాడేందుకు గ్రామ సభ సరైన నిర్వహణ ప్రణాళికను సిద్ధం చేయాలి.\n"
                "ప్రభుత్వం మరియు అటవీ శాఖ గ్రామ సభ నిర్వహణ ప్రణాళికలకు సాంకేతిక సహాయాన్ని మాత్రమే అందిస్తాయి.\n"
                "ఈ పత్రం కమ్యూనిటీ ఆర్థిక అభివృద్ధి మరియు అటవీ స్థిరత్వం రెండింటినీ ఏకకాలంలో నిర్ధారిస్తుంది.\n"
                "సంబంధిత అధికారుల సక్రమ సంతకాలతో ఈ పట్టా ఈ రోజు నుండి అమలులోకి వచ్చింది."
            ),
            # Variation 3: Formal Letter Style
            (
                "శీర్షిక: సమిష్టి అటవీ వనరుల (CFR) పై హక్కు మరియు పట్టా సర్టిఫికేట్.\n"
                "లబ్ధిదారు సంస్థ: {GRAM_SABHA} గ్రామ సభ, {VILLAGE} గ్రామం, {GRAM_PANCHAYAT} పంచాయతీ.\n"
                "స్థానం: తాలూకా {TEHSIL_TALUKA}, జిల్లా {DISTRICT}, రాష్ట్రం {STATE}.\n"
                "కమ్యూనిటీ వర్గీకరణ: {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} లేదా {COMMUNITY_TYPE_BOTH}.\n"
                "విషయం: సామాజిక అటవీ వనరులను నిర్వహించే అధికారిక హక్కును పై గ్రామ సభకు మంజూరు చేయడం.\n\n"

                "అటవీ హక్కుల చట్టం 2006 లోని నిబంధనల ఆధారంగా ఈ చారిత్రక హక్కు మంజూరు చేయబడుతోంది.\n"
                "హక్కు పొందిన అటవీ ప్రాంతం యొక్క ఖస్రా లేదా కొలత సంఖ్య {KHASRA_COMPARTMENT_NUMBER} స్పష్టంగా నమోదు చేయబడింది.\n"
                "ఆ ప్రాంతం యొక్క సరిహద్దు భౌగోళికంగా {BOUNDARY_DESCRIPTION} వివరణ ద్వారా నిర్వచించబడింది.\n"
                "సమాజం సాంప్రదాయకంగా నిర్వహించే ఆచార సరిహద్దు {CUSTOMARY_BOUNDARY} కూడా ఇందులో చేర్చబడింది.\n"
                "ఈ సరిహద్దులోని ప్రకృతి వనరులన్నింటినీ రక్షించే మరియు వినియోగించుకునే హక్కు గ్రామ సభకు చెందినది.\n\n"

                "ఈ హక్కు ఏ విధంగానూ వ్యక్తులకు సంబంధించినది కాదు, ఇది మొత్తం సమాజం యొక్క ఉమ్మడి ఆస్తి.\n"
                "అటవీ వనరుల స్థిరమైన నిర్వహణ కోసం గ్రామ సభ అటవీ హక్కుల కమిటీని ఏర్పాటు చేసి పని చేయాలి.\n"
                "అడవి మంటల వంటి ప్రకృతి వైపరీత్యాల నుంచి అడవిని రక్షించడం సంఘం ప్రాథమిక విధి.\n"
                "రాష్ట్ర స్థాయి కమిటీ సమీక్ష మరియు తుది ఆమోదం తర్వాత ఈ హక్కు మంజూరు చేయబడుతుంది.\n"
                "సంబంధిత జిల్లా అధికారుల ముద్రతో ఈ ధృవీకరణ పత్రం అధికారికంగా జారీ చేయబడుతుంది."
            ),
            # Variation 4: Legal / Statutory Document Style
            (
                "కమ్యూనిటీ ఫారెస్ట్ రిసోర్సెస్ (Community Forest Resources) చట్టబద్ధమైన పట్టా మరియు ప్రభుత్వ అధికార బదిలీ దస్తావేజు.\n"
                "సెక్షన్ 3(1)(i) నిబంధనల ప్రకారం, {STATE} రాష్ట్రం, {DISTRICT} జిల్లా, {TEHSIL_TALUKA} తాలూకా అధికార పరిధిలో ఈ దస్తావేజు చట్టబద్ధంగా అమలు చేయబడింది.\n"
                "దీని ప్రకారం, {VILLAGE} గ్రామం, {GRAM_PANCHAYAT} గ్రామ పంచాయతీ మరియు {GRAM_SABHA} గ్రామ సభలకు సమిష్టి అటవీ వనరులను నిర్వహించే పూర్తి చట్టపరమైన అధికారం ఇవ్వబడింది.\n"
                "ఈ పత్రం, {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} లేదా {COMMUNITY_TYPE_BOTH} వర్గాలకు చెందిన నివాసితుల జీవనోపాధిని రక్షించే చట్టపరమైన రూపం.\n"
                "జిల్లా స్థాయి కమిటీ (DLC) తుది చట్టపరమైన ఆమోదం తర్వాత మాత్రమే ఈ హక్కు ధృవీకరణ పత్రం అధికారికంగా ప్రచురించబడుతోంది.\n"
                "దీని ద్వారా, రాష్ట్ర యాజమాన్యంలోని అటవీ వనరులను రక్షించే మరియు నిర్వహించే హక్కు చట్టబద్ధంగా గ్రామ సభకు బదిలీ చేయబడుతుంది.\n\n"

                "అటవీ వనరుల ప్రాంతం యొక్క చట్టపరమైన భూ-సర్వే సంఖ్య, సరిహద్దులు మరియు సాంప్రదాయ ప్రకటన.\n"
                "కమ్యూనిటీ నిర్వహణలో ఉన్న అటవీ వనరుల ప్రాంతం యొక్క ఖస్రా (Khasra) లేదా కంపార్ట్‌మెంట్ నంబర్ {KHASRA_COMPARTMENT_NUMBER} భూమి సర్వే రికార్డులలో స్పష్టంగా నమోదు చేయబడింది.\n"
                "ఈ ప్రాంతం యొక్క భౌగోళిక మరియు స్థలాకృతి సరిహద్దులు మ్యాప్‌ల ద్వారా {BOUNDARY_DESCRIPTION} గా చట్టబద్ధంగా ధృవీకరించబడ్డాయి.\n"
                "పొరుగు గ్రామాలు మరియు అటవీ శాఖతో సరిహద్దులను పంచుకునే సాంప్రదాయ కస్టమరీ సరిహద్దు (Customary Boundary) {CUSTOMARY_BOUNDARY} అధికారికంగా ధృవీకరించబడింది.\n"
                "ఈ సరిహద్దుల్లో ఉన్న మైనర్ ఫారెస్ట్ ప్రొడ్యూస్, నీటి వనరులు మరియు వృక్షజాలాన్ని ఉపయోగించుకునే పూర్తి హక్కు గ్రామ సభకు ఇవ్వబడింది.\n"
                "ఎలాంటి సరిహద్దు వివాదాలను నివారించడానికి భూమి సర్వే విభాగం ద్వారా తగిన సరిహద్దు స్తంభాలు మరియు చట్టపరమైన గుర్తులు ఏర్పాటు చేయబడ్డాయి.\n\n"

                "గ్రామ సభ చట్టబద్ధమైన బాధ్యతలు, అటవీ సంరక్షణ మరియు అధికారుల తుది ధృవీకరణ.\n"
                "చట్టంలోని ప్రాథమిక నిబంధనలు మినహా, ఈ హక్కుపై రాష్ట్ర ప్రభుత్వం మరే ఇతర కొత్త పరిమితులు లేదా షరతులు విధించలేదు.\n"
                "అయినప్పటికీ, అటవీ పర్యావరణ సమతుల్యతను కాపాడుకోవడం మరియు దావాగ్ని (Forest Fire) వంటి విపత్తులను నివారించడం గ్రామ సభ యొక్క పూర్తి చట్టపరమైన బాధ్యత.\n"
                "ఈ ప్రయోజనం కోసం, గ్రామ సభ తరపున 'అటవీ వనరుల సంరక్షణ కమిటీ' ఏర్పాటు చేయడం తప్పనిసరి, దీని నివేదికను ఏటా ప్రభుత్వానికి సమర్పించాలి.\n"
                "చట్టవిరుద్ధంగా అటవీ వనరులు ధ్వంసమైతే, క్రిమినల్ ప్రొసీజర్ కోడ్ కింద గ్రామ సభ బాధ్యత వహిస్తుంది.\n"
                "ఈ పట్టా రాష్ట్ర ప్రభుత్వ ఉన్నతాధికారులైన జిల్లా కలెక్టర్, డివిజనల్ ఫారెస్ట్ ఆఫీసర్ (DFO) మరియు గిరిజన సంక్షేమ అధికారి సంతకాలతో చట్టబద్ధంగా అమలులోకి వస్తుంది."
            )
        ]
    },
    # Bengali
    "bn": {
        DOC_CLAIM_FOREST_LAND: [
            # Variation 1: Bureaucratic / Form Style (Simulating Form A filled application)
            (
                "ফর্ম - ক [নিয়ম ১১(১)(ক) দ্রষ্টব্য]\n"
                "বনভূমির ওপর অধিকারের জন্য দাবিপত্র এবং আবেদনকারীর প্রাথমিক বিবরণ।\n"
                "দাবিদারের সম্পূর্ণ নাম: {CLAIMANT_NAME}।\n"
                "পিতা অথবা মাতার নাম: {FATHER_MOTHER_NAME}। স্বামী বা স্ত্রীর নাম: {SPOUSE_NAME}।\n"
                "আবেদনকারীর সম্পূর্ণ আবাসিক ঠিকানা: {ADDRESS_FULL} হিসেবে নথিবদ্ধ করা হলো।\n"
                "এই জমিটি {STATE} রাজ্যের অন্তর্গত {DISTRICT} জেলার {TEHSIL_TALUKA} তহসিলের সীমানায় অবস্থিত।\n"
                "একইসঙ্গে, এটি {VILLAGE} গ্রাম, {GRAM_PANCHAYAT} গ্রাম পঞ্চায়েত এবং {GRAM_SABHA} গ্রাম সভার প্রশাসনিক এক্তিয়ারে পড়ে।\n\n"

                "দাবিদারের পরিবারের বিবরণ এবং বনভূমিতে দখলের বর্তমান স্থিতি:\n"
                "আমার পরিবারের সদস্য {FAMILY_MEMBER_NAME} (বয়স: {FAMILY_MEMBER_AGE} বছর) এবং আমার ওপর নির্ভরশীল {DEPENDENT_NAME} আমার সাথে বসবাস করেন।\n"
                "আমরা এতদ্বারা প্রত্যয়ন করছি যে আমরা {CATEGORY_SCHEDULED_TRIBE} অথবা {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} শ্রেণিভুক্ত।\n"
                "বসবাসের উদ্দেশ্যে আমাদের দখলে থাকা বনভূমির পরিমাণ হলো {LAND_EXTENT_HABITATION}।\n"
                "স্ব-চাষাবাদ বা কৃষি কাজের জন্য ব্যবহৃত জমির পরিমাণ হলো {LAND_EXTENT_SELF_CULTIVATION}।\n"
                "বনগ্রাম বা ফরেস্ট ভিলেজগুলোতে অবস্থিত জমির পরিমাণ {LAND_EXTENT_FOREST_VILLAGE} হিসেবে রাজস্ব রেকর্ডে নিবন্ধিত।\n\n"

                "জমি সম্পর্কিত অন্যান্য দাবি, বিতর্ক এবং সংযুক্ত প্রমাণাদি:\n"
                "যদি এই জমির ওপর কোনো বিরোধ বা বিতর্ক থাকে, তবে তার বিবরণ: {DISPUTED_LAND_DESCRIPTION}।\n"
                "পূর্বে প্রদান করা পাট্টা বা লিজের বিবরণ: {EXISTING_PATTAS_LEASES_GRANTS}।\n"
                "পুনর্বাসন বা বিকল্প জমির জন্য দাবি করা হয়েছে এমন জমি হলো {REHABILITATION_LAND}।\n"
                "বিনা ক্ষতিপূরণে যে জমি থেকে আমাদের উৎখাত করা হয়েছিল, তার বিবরণ: {DISPLACED_FROM_LAND}।\n"
                "আমাদের অন্যান্য প্রথাগত অধিকার হলো {OTHER_TRADITIONAL_RIGHT} এবং অতিরিক্ত তথ্য {OTHER_INFORMATION} সংযুক্ত করা হয়েছে।\n"
                "এই দাবির সমর্থনে প্রামাণ্য দলিল হিসেবে {EVIDENCE_ITEM} উপস্থাপন করা হলো।"
            ),
            # Variation 2: Narrative / Descriptive Style (Simulating a Gram Sabha resolution narrative)
            (
                "গ্রাম সভার সামনে উপস্থাপিত বিস্তৃত বিবরণ এবং বনভূমির ওপর অধিকারের দাবি।\n"
                "আমি, শ্রী/শ্রীমতী {CLAIMANT_NAME} (পিতা/মাতা: {FATHER_MOTHER_NAME}, স্বামী/স্ত্রী: {SPOUSE_NAME}) এই বিবরণ পেশ করছি।\n"
                "আমার স্থায়ী বাসস্থানের সম্পূর্ণ ঠিকানা হলো {ADDRESS_FULL}। আমি {STATE} রাজ্যের {DISTRICT} জেলার একজন স্থায়ী বাসিন্দা।\n"
                "আমার বসতবাড়িটি {TEHSIL_TALUKA} তহসিলের অন্তর্গত {VILLAGE} গ্রামে অবস্থিত।\n"
                "এই অঞ্চলটি সরাসরি {GRAM_PANCHAYAT} গ্রাম পঞ্চায়েত এবং {GRAM_SABHA} গ্রাম সভার প্রশাসনিক নিয়ন্ত্রণের অধীনে আসে।\n\n"

                "আমাদের পরিবার বংশানুক্রমিকভাবে জঙ্গলের ওপর নির্ভরশীল এবং আমরা {CATEGORY_SCHEDULED_TRIBE} বা {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} সম্প্রদায়ের প্রথাগত বনবাসী।\n"
                "আমার পরিবারে সদস্য {FAMILY_MEMBER_NAME} (বয়স {FAMILY_MEMBER_AGE} বছর) এবং সম্পূর্ণ নির্ভরশীল {DEPENDENT_NAME} অন্তর্ভুক্ত রয়েছেন।\n"
                "আমরা বহু প্রজন্ম ধরে যে স্থানে বসবাস করছি, সেই আবাসিক বনভূমির পরিমাণ হলো {LAND_EXTENT_HABITATION}।\n"
                "আমাদের জীবনযাত্রার প্রধান উপায় কৃষি এবং আমাদের নিজস্ব চাষের জমির পরিমাণ হলো {LAND_EXTENT_SELF_CULTIVATION}।\n"
                "এছাড়া, বনগ্রামের সীমানায় আমাদের দখলি জমির পরিমাণ {LAND_EXTENT_FOREST_VILLAGE} মাপা হয়েছে।\n\n"

                "এই দাবির প্রসঙ্গে কিছু গুরুত্বপূর্ণ আইনি তথ্য এখানে লিপিবদ্ধ করা হচ্ছে।\n"
                "জমি সম্পর্কিত কোনো বিরোধের স্থিতি {DISPUTED_LAND_DESCRIPTION} হিসেবে স্পষ্ট করা হয়েছে এবং পুরনো পাট্টার বিবরণ {EXISTING_PATTAS_LEASES_GRANTS}।\n"
                "আমাদের পুনর্বাসনের জন্য {REHABILITATION_LAND} জমির প্রয়োজন এবং অতীতে আমাদের ক্ষতিপূরণ ছাড়াই {DISPLACED_FROM_LAND} থেকে সরানো হয়েছিল।\n"
                "আমাদের পূর্বপুরুষদের দ্বারা ব্যবহৃত অন্যান্য প্রথাগত অধিকার {OTHER_TRADITIONAL_RIGHT} আজও প্রাসঙ্গিক।\n"
                "দাবি প্রমাণের জন্য মজবুত প্রমাণ {EVIDENCE_ITEM} প্রস্তুত আছে এবং অন্যান্য সম্পর্কিত তথ্য {OTHER_INFORMATION} বিবেচনার জন্য সংযুক্ত করা হলো।"
            ),
            # Variation 3: Formal Letter Style (Simulating a petition to the Sub-Divisional Level Committee)
            (
                "প্রেরক: {CLAIMANT_NAME}, পিতা/মাতা: {FATHER_MOTHER_NAME}, জীবনসঙ্গী: {SPOUSE_NAME}।\n"
                "ঠিকানা: {ADDRESS_FULL}, গ্রাম: {VILLAGE}, পঞ্চায়েত: {GRAM_PANCHAYAT}, গ্রাম সভা: {GRAM_SABHA}।\n"
                "তহসিল: {TEHSIL_TALUKA}, জেলা: {DISTRICT}, রাজ্য: {STATE}।\n"
                "বিষয়: বন অধিকার আইন ২০০৬-এর অধীনে ব্যক্তিগত বনভূমির অধিকার প্রদানের জন্য আবেদন।\n"
                "মহাশয়, উপর্যুক্ত বিষয়ে সবিনয় নিবেদন এই যে, আমি দীর্ঘকাল ধরে বনাঞ্চলে বসবাস করছি।\n\n"

                "আমি প্রত্যয়ন করছি যে আমি {CATEGORY_SCHEDULED_TRIBE} অথবা {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} শ্রেণির একজন যোগ্য সদস্য।\n"
                "আমার পরিবারে {FAMILY_MEMBER_NAME} (বয়স {FAMILY_MEMBER_AGE}) এবং নির্ভরশীল {DEPENDENT_NAME} রয়েছেন, যাদের ভরণপোষণ এই জমি থেকেই হয়।\n"
                "বনাঞ্চলের ভেতরে আমাদের বসতবাড়ি ও আবাসিক চত্বরের মোট পরিমাণ হলো {LAND_EXTENT_HABITATION}।\n"
                "আমাদের দ্বারা নিজস্ব কৃষি কাজের জন্য ব্যবহৃত জমির পরিমাণ হলো {LAND_EXTENT_SELF_CULTIVATION}।\n"
                "বনগ্রামগুলিতে আমাদের জমির পরিমাণ {LAND_EXTENT_FOREST_VILLAGE} হিসেবে রাজস্ব রেকর্ডে অন্তর্ভুক্ত হওয়া উচিত।\n\n"

                "এই জমি সম্পর্কিত বিরোধপূর্ণ পরিস্থিতিটি হলো {DISPUTED_LAND_DESCRIPTION}, যার সমাধান হওয়া অত্যন্ত আবশ্যক।\n"
                "পূর্বে প্রদান করা লিজ বা পাট্টার {EXISTING_PATTAS_LEASES_GRANTS} অনুলিপি যাচাইয়ের জন্য সংযুক্ত করা হয়েছে।\n"
                "বিকল্প পুনর্বাসন জমি {REHABILITATION_LAND} এবং ক্ষতিপূরণ ছাড়া উচ্ছেদ হওয়া জমি {DISPLACED_FROM_LAND} সম্পর্কেও মনোযোগ আকর্ষণ করছি।\n"
                "আইন দ্বারা সুরক্ষিত আমাদের অন্যান্য প্রথাগত অধিকারগুলি {OTHER_TRADITIONAL_RIGHT} আমাদের প্রদান করা হোক।\n"
                "প্রমাণস্বরূপ {EVIDENCE_ITEM} এবং অতিরিক্ত বিবরণ {OTHER_INFORMATION} আবেদনের সাথে নথিবদ্ধ করা হলো।"
            ),
            # Variation 4: Legal / Statutory Declaration Style (Simulating a sworn affidavit)
            (
                "হলফনামা এবং বিধিবদ্ধ দাবির ঘোষণাপত্র (বন অধিকার আইন ২০০৬-এর অধীনে)।\n"
                "আমি, {CLAIMANT_NAME} (পিতা/মাতা: {FATHER_MOTHER_NAME}, বৈধ স্বামী/স্ত্রী: {SPOUSE_NAME}), সত্যনিষ্ঠার সাথে নিম্নলিখিত ঘোষণা করছি।\n"
                "আমার আইনি ও স্থায়ী ঠিকানা {ADDRESS_FULL} হিসেবে সরকারি নথিপত্রে নিবন্ধিত হয়েছে।\n"
                "দাবিকৃত জমিটি {STATE} রাজ্য, {DISTRICT} জেলা এবং {TEHSIL_TALUKA} তহসিলের এক্তিয়ারে অবস্থিত।\n"
                "এই জমিটি সম্পূর্ণরূপে {VILLAGE} রাজস্ব গ্রাম, {GRAM_PANCHAYAT} গ্রাম পঞ্চায়েত এবং {GRAM_SABHA} গ্রাম সভার বিধিবদ্ধ সীমার অধীনে পড়ে।\n\n"

                "ধারা ৩(১)(ক) অনুসারে জমি দখল এবং সামাজিক শ্রেণির আইনি নিশ্চিতকরণ।\n"
                "আমি শপথপূর্বক জানাচ্ছি যে আমি {CATEGORY_SCHEDULED_TRIBE} বা {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER}-এর বিধিবদ্ধ শ্রেণির অন্তর্গত।\n"
                "আমার আইনি উত্তরাধিকারী {FAMILY_MEMBER_NAME} (বয়স {FAMILY_MEMBER_AGE}) এবং নির্ভরশীল {DEPENDENT_NAME} এই দাবির প্রত্যক্ষ সুবিধাভোগী।\n"
                "আইনের বিধান অনুসারে, বাসস্থানের উদ্দেশ্যে দখলে থাকা জমির পরিমাপ {LAND_EXTENT_HABITATION} নির্ধারণ করা হয়েছে।\n"
                "কৃষিকাজ বা নিজস্ব চাষের জন্য ব্যবহৃত জমির পরিমাণ {LAND_EXTENT_SELF_CULTIVATION} হিসেবে পাওয়া গেছে।\n"
                "ধারা ৩(১)(জ) অনুসারে বনগ্রামগুলিতে অবস্থিত জমির পরিমাণ হলো {LAND_EXTENT_FOREST_VILLAGE}।\n\n"

                "মুলতুবি থাকা মামলা, পাট্টা এবং অন্যান্য বিধিবদ্ধ অধিকারের প্রকাশ।\n"
                "ধারা ৩(১)(চ)-এর অধীনে এই জমির ওপর যেকোনো ধরনের বিবাদকে {DISPUTED_LAND_DESCRIPTION} হিসেবে ঘোষণা করা হচ্ছে।\n"
                "পূর্ববর্তী সরকার কর্তৃক প্রদত্ত পাট্টা বা অনুদানের বিবরণ: {EXISTING_PATTAS_LEASES_GRANTS}।\n"
                "ধারা ৩(১)(ড) অনুযায়ী স্বস্থানে পুনর্বাসিত জমি {REHABILITATION_LAND}-এর বিবরণও উপস্থাপন করা হয়েছে।\n"
                "ধারা ৪(৮) অনুসারে কোনো ন্যায্য ক্ষতিপূরণ ছাড়াই উচ্ছেদ করা জমির বিবরণ হলো {DISPLACED_FROM_LAND}।\n"
                "ধারা ৩(১)(ঠ)-এর অধীনে অন্যান্য প্রথাগত অধিকার {OTHER_TRADITIONAL_RIGHT} এবং আইনি প্রমাণ {EVIDENCE_ITEM} সহ {OTHER_INFORMATION} এই হলফনামার অবিচ্ছেদ্য অংশ।"
            )
        ],

        DOC_CLAIM_COMMUNITY_RIGHTS: [
            # Variation 1: Bureaucratic / Form Style
            (
                "ফর্ম - খ [নিয়ম ১১(১)(ক) এবং (৪) দ্রষ্টব্য]\n"
                "গোষ্ঠীগত বন অধিকারের জন্য যথাযথ দাবি ফর্ম এবং গ্রাম সভার প্রস্তাব।\n"
                "এই যৌথ আবেদনটি {VILLAGE} গ্রাম এবং {GRAM_PANCHAYAT} গ্রাম পঞ্চায়েতের পক্ষ থেকে উপস্থাপন করা হচ্ছে।\n"
                "এটি {STATE} রাজ্য, {DISTRICT} জেলা, এবং {TEHSIL_TALUKA} তহসিলের অন্তর্গত {GRAM_SABHA} গ্রাম সভা দ্বারা যথাযথভাবে গৃহীত হয়েছে।\n"
                "আমরা সকলেই ঐতিহ্যগত বনবাসী এবং {COMMUNITY_TYPE_FDST} অথবা {COMMUNITY_TYPE_OTFD} সম্প্রদায়ের প্রতিনিধিত্ব করছি।\n\n"

                "সম্প্রদায় কর্তৃক উপভোগ করা বন অধিকারের প্রকৃতি নিম্নলিখিতভাবে নথিবদ্ধ করা হয়েছে।\n"
                "যৌথ ব্যবহারের জন্য নিস্তার (Nistar) অধিকার: {COMMUNITY_RIGHT_NISTAR}।\n"
                "গৌণ বনজ সম্পদ (MFP) সংগ্রহ এবং মালিকানার অধিকার: {RIGHT_MINOR_FOREST_PRODUCE}।\n"
                "মাছ ধরা, জলাশয় এবং অন্যান্য সম্পদ ব্যবহারের অধিকার: {COMMUNITY_RIGHT_RESOURCE_USE}।\n"
                "পশু চারণ বা গোচারণ সম্পর্কিত অধিকার: {COMMUNITY_RIGHT_GRAZING}।\n"
                "যাযাবর ও পশুপালক সম্প্রদায়ের জন্য প্রথাগত সম্পদে প্রবেশাধিকার: {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS}।\n\n"

                "বিশেষভাবে দুর্বল উপজাতীয় গোষ্ঠী (PTG) এবং প্রাক-কৃষি সম্প্রদায়গুলির জন্য বাসস্থানের (Habitat) অধিকার {COMMUNITY_TENURE_HABITAT} নিশ্চিত করা হোক।\n"
                "জীববৈচিত্র্য, বৌদ্ধিক সম্পত্তি এবং প্রথাগত জ্ঞানের অধিকার {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} হিসেবে স্বীকৃত হোক।\n"
                "আইন দ্বারা সংজ্ঞায়িত অন্যান্য প্রথাগত অধিকারগুলি {OTHER_TRADITIONAL_RIGHT} আমাদের জীবিকার মূল ভিত্তি।\n"
                "এই যৌথ দাবিগুলি প্রমাণ করার জন্য উপস্থাপিত প্রমাণাদি: {EVIDENCE_ITEM}।\n"
                "প্রশাসনিক পর্যালোচনার জন্য প্রয়োজনীয় অতিরিক্ত তথ্য {OTHER_INFORMATION} এই ফর্মের সাথে সংযুক্ত করা হলো।"
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "যৌথ বনায়ন এবং প্রথাগত অধিকার সংরক্ষণের জন্য গ্রাম সভার যৌথ আবেদন।\n"
                "আমাদের {GRAM_SABHA} গ্রাম সভা, {VILLAGE} গ্রামের সমস্ত বাসিন্দাদের পক্ষে এই দাবি পেশ করছে।\n"
                "আমাদের এলাকাটি {STATE} রাজ্যের {DISTRICT} জেলায় অবস্থিত {TEHSIL_TALUKA} তহসিল এবং {GRAM_PANCHAYAT} পঞ্চায়েতের অন্তর্গত।\n"
                "আমাদের সম্প্রদায়টি সরকারি শ্রেণিবিন্যাস অনুযায়ী {COMMUNITY_TYPE_FDST} বা {COMMUNITY_TYPE_OTFD} হিসেবে স্বীকৃত।\n"
                "আমরা বংশানুক্রমিকভাবে জঙ্গলের সাথে সহাবস্থানের জীবনধারা অনুসরণ করে আসছি।\n\n"

                "দৈনন্দিন জীবন ও জীবিকার জন্য আমরা মূলত নিম্নলিখিত গোষ্ঠীগত অধিকারগুলির ওপর নির্ভরশীল।\n"
                "আমাদের নিস্তার অধিকারগুলি স্পষ্টভাবে {COMMUNITY_RIGHT_NISTAR} হিসেবে প্রতিষ্ঠিত হয়েছে।\n"
                "মধু, ভেষজ উদ্ভিদের মতো গৌণ বনজ সম্পদ সংগ্রহের অধিকার হলো {RIGHT_MINOR_FOREST_PRODUCE}।\n"
                "স্থানীয় জলাশয় ব্যবহার এবং মাছ ধরার অধিকার হলো {COMMUNITY_RIGHT_RESOURCE_USE}।\n"
                "গৃহপালিত পশুদের জন্য চারণভূমি ও গোচারণের অধিকার {COMMUNITY_RIGHT_GRAZING}-এর অধীনে সুরক্ষিত রয়েছে।\n"
                "ঋতুভিত্তিক পরিযায়ী যাযাবর সম্প্রদায়ের সম্পদের অধিকার {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS} হিসেবে প্রদত্ত হয়েছে।\n\n"

                "আদিম উপজাতিদের প্রাচীন বাসস্থান (Habitat) সংরক্ষণ করার অধিকার {COMMUNITY_TENURE_HABITAT} অত্যন্ত তাৎপর্যপূর্ণ।\n"
                "প্রথাগত জ্ঞান এবং স্থানীয় জীববৈচিত্র্যের ওপর আমাদের অধিকার {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} হিসেবে দাবি করা হয়েছে।\n"
                "আমাদের পূর্বপুরুষদের দ্বারা ব্যবহৃত অন্যান্য প্রথাগত অধিকার {OTHER_TRADITIONAL_RIGHT} আজও অব্যাহত আছে।\n"
                "এই অধিকারগুলির সত্যতা প্রমাণের জন্য {EVIDENCE_ITEM}-এর মতো ঐতিহাসিক দলিলপত্র উপস্থাপন করা হয়েছে।\n"
                "বিস্তারিত পর্যালোচনার জন্য {OTHER_INFORMATION} সহ অন্যান্য তথ্যও সাথে দেওয়া হয়েছে।"
            ),
            # Variation 3: Formal Letter Style
            (
                "বিষয়: বন অধিকার আইন ২০০৬-এর অধীনে গোষ্ঠীগত বন অধিকারের স্বীকৃতির জন্য যৌথ স্মারকলিপি।\n"
                "আমরা {STATE} রাজ্য, {DISTRICT} জেলা এবং {TEHSIL_TALUKA} তহসিলের স্থায়ী বাসিন্দা।\n"
                "আমাদের বাসস্থান {VILLAGE} গ্রাম এবং {GRAM_PANCHAYAT} পঞ্চায়েতের এক্তিয়ারে অবস্থিত।\n"
                "এই পত্রটি {GRAM_SABHA} গ্রাম সভার সর্বসম্মতি এবং পূর্ণ সম্মতির সাথে লেখা হচ্ছে।\n"
                "আমরা আদিবাসী এবং ঐতিহ্যগত বনবাসী, যারা {COMMUNITY_TYPE_FDST} এবং {COMMUNITY_TYPE_OTFD} সম্প্রদায়ের সাথে যুক্ত।\n\n"

                "আইনের বিধান অনুসারে, আমরা নিম্নলিখিত গোষ্ঠীগত অধিকারগুলির দাবি জানাচ্ছি:\n"
                "নিস্তার এবং সাধারণ ব্যবহারের অধিকার: {COMMUNITY_RIGHT_NISTAR}। গৌণ বনজ সম্পদের অধিকার: {RIGHT_MINOR_FOREST_PRODUCE}।\n"
                "পুকুর এবং জলজ সম্পদ ব্যবহার করার অধিকার: {COMMUNITY_RIGHT_RESOURCE_USE}।\n"
                "পশু চারণের যৌথ অধিকার: {COMMUNITY_RIGHT_GRAZING}।\n"
                "যাযাবর সম্প্রদায়ের জন্য চারণভূমিতে প্রবেশের অধিকার: {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS}।\n\n"

                "আমাদের প্রথাগত বাসস্থানের পাট্টা {COMMUNITY_TENURE_HABITAT} হিসেবে আমাদের কাছে হস্তান্তর করা উচিত।\n"
                "আমাদের জ্ঞান এবং জীববৈচিত্র্যের ওপর বৌদ্ধিক অধিকার {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} সুনিশ্চিত করা হোক।\n"
                "আমাদের জীবনের সাথে জড়িত অন্যান্য সমস্ত প্রথাগত অধিকার {OTHER_TRADITIONAL_RIGHT} বৈধ হিসেবে মান্যতা পাক।\n"
                "এই দাবির সমর্থনে জোরালো প্রমাণ হিসেবে {EVIDENCE_ITEM} সংযুক্ত করা হয়েছে।\n"
                "অতিরিক্ত তথ্য {OTHER_INFORMATION} প্রশাসনের গোচরে আনা হলো।"
            ),
            # Variation 4: Legal / Statutory Declaration Style
            (
                "গোষ্ঠীগত বন অধিকারের (Community Forest Rights) বিধিবদ্ধ দাবি এবং ঘোষণাপত্র।\n"
                "এই ঘোষণাটি {STATE} রাজ্য, {DISTRICT} জেলা, এবং {TEHSIL_TALUKA} তহসিলের সংশ্লিষ্ট কর্তৃপক্ষের সামনে পেশ করা হচ্ছে।\n"
                "এই দাবিটি {VILLAGE} গ্রামবাসীদের পক্ষে, {GRAM_PANCHAYAT} গ্রাম পঞ্চায়েত এবং {GRAM_SABHA} গ্রাম সভার আইনি প্রস্তাব দ্বারা পাস হয়েছে।\n"
                "বন অধিকার আইন ২০০৬-এর অধীনে এই সম্প্রদায়কে {COMMUNITY_TYPE_FDST} অথবা {COMMUNITY_TYPE_OTFD} হিসেবে আইনি স্বীকৃতি দেওয়া হয়েছে।\n"
                "এই সম্প্রদায়ের যৌথ অধিকার আইনগতভাবে পুনরুদ্ধার করার উদ্দেশ্যে এই দলিলটি প্রস্তুত করা হয়েছে।\n\n"

                "ধারা ৩-এর অধীনে সংজ্ঞায়িত গোষ্ঠীগত ব্যবহার এবং সম্পদের ওপর অধিকারের তালিকা।\n"
                "ধারা ৩(১)(খ)-এর অধীনে নিস্তারের (Nistar) বিধিবদ্ধ অধিকারগুলি {COMMUNITY_RIGHT_NISTAR} হিসেবে ঘোষণা করা হলো।\n"
                "ধারা ৩(১)(গ)-এর অধীনে গৌণ বনজ সম্পদের (MFP) ওপর মালিকানার অধিকার {RIGHT_MINOR_FOREST_PRODUCE} হিসেবে বৈধ।\n"
                "জলাশয় ও মৎস্য সম্পদ ব্যবহার করার আইনি অধিকার {COMMUNITY_RIGHT_RESOURCE_USE} নির্ধারিত আছে।\n"
                "প্রথাগত পশু চারণের অধিকার {COMMUNITY_RIGHT_GRAZING} হিসেবে আনুষ্ঠানিকভাবে নথিবদ্ধ রয়েছে।\n"
                "যাযাবর সম্প্রদায়ের সম্পদের আইনি প্রবেশাধিকার {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS} সুনিশ্চিত করা হয়েছে।\n\n"

                "উপজাতীয় বাসস্থানের অধিকার, বৌদ্ধিক সম্পত্তি এবং উপস্থাপিত বিধিবদ্ধ প্রমাণ।\n"
                "পিটিজি (PTG) এবং প্রাক-কৃষি সম্প্রদায়ের জন্য বাসস্থানের (Habitat) আইনি অধিকার {COMMUNITY_TENURE_HABITAT} দাবি করা হয়েছে।\n"
                "ধারা ৩(১)(ট) অনুযায়ী জীববৈচিত্র্য এবং প্রথাগত জ্ঞানে প্রবেশাধিকার {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} নিবন্ধিত আছে।\n"
                "আইন দ্বারা প্রদত্ত অন্যান্য সমস্ত প্রথাগত অধিকার {OTHER_TRADITIONAL_RIGHT} আমাদের যৌথ ঐতিহ্য।\n"
                "উল্লিখিত বিধিবদ্ধ দাবিগুলি প্রমাণ করার জন্য নথিপত্র এবং প্রমাণ {EVIDENCE_ITEM} সংযুক্ত করা হয়েছে।\n"
                "আইনি যাচাইয়ের উদ্দেশ্যে অন্যান্য তথ্য {OTHER_INFORMATION} আনুষ্ঠানিকভাবে উপস্থাপন করা হলো।"
            )
        ],

        DOC_CLAIM_COMMUNITY_FOREST_RESOURCE: [
            # Variation 1: Bureaucratic / Form Style
            (
                "ফর্ম - গ [আইনের ধারা ৩(১)(ঝ) এবং নিয়ম ১১(১) দ্রষ্টব্য]\n"
                "গোষ্ঠীগত বনজ সম্পদ (CFR) অধিকারের জন্য দাবিপত্র।\n"
                "এই দাবিটি {STATE} রাজ্য, {DISTRICT} জেলা, এবং {TEHSIL_TALUKA} তহসিলের এক্তিয়ারের অধীনে আসে।\n"
                "এটি {GRAM_PANCHAYAT} গ্রাম পঞ্চায়েতের অধীনস্থ {VILLAGE} গ্রামবাসীদের পক্ষ থেকে উপস্থাপন করা হচ্ছে।\n"
                "এই প্রস্তাবটি {GRAM_SABHA} গ্রাম সভার যথাযথ বৈঠকে সর্বসম্মতিক্রমে পাস হয়েছে।\n\n"

                "এই দাবি উপস্থাপনকারী গ্রাম সভার প্রধান সদস্য হলেন {GRAM_SABHA_MEMBER_NAME}।\n"
                "এই সদস্যরা আইনত {CATEGORY_SCHEDULED_TRIBE} বা {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} সম্প্রদায়ের সাথে যুক্ত।\n"
                "আমরা যে বনজ সম্পদ এলাকার ওপর দাবি জানাচ্ছি তার খতিয়ান/কম্পার্টমেন্ট নম্বর হলো {KHASRA_COMPARTMENT_NUMBER}।\n"
                "আমাদের বনাঞ্চলের সীমানা সংলগ্ন গ্রামগুলি হলো {BORDERING_VILLAGE}।\n"
                "এই এলাকার ভৌগোলিক সীমানা {BOUNDARY_DESCRIPTION} হিসেবে স্পষ্টভাবে সংজ্ঞায়িত করা হয়েছে।\n\n"

                "এই ভূখণ্ডটি আমাদের সম্প্রদায় বংশানুক্রমিকভাবে সংরক্ষণ ও পরিচালনা করে আসছে।\n"
                "এর জন্য গোষ্ঠীগত বনজ সম্পদের প্রমাণের যথাযথ তালিকা {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} সংযুক্ত করা হয়েছে।\n"
                "আমাদের প্রথাগত ব্যবহার প্রমাণ করে এমন অন্যান্য প্রমাণাদি {EVIDENCE_ITEM} হিসেবে উপস্থাপন করা হয়েছে।\n"
                "আমরা নিশ্চিত করছি যে এই বনজ সম্পদের টেকসই ব্যবহারের অধিকার গ্রাম সভার হাতে ন্যস্ত আছে।\n"
                "সক্ষম কর্তৃপক্ষের কাছে অনুরোধ করা হচ্ছে যে তারা এর তদন্ত করে গোষ্ঠীগত বনজ সম্পদ অধিকারকে স্বীকৃতি প্রদান করুক।"
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "গোষ্ঠীগত বনজ সম্পদের পরিচালনা এবং সংরক্ষণের জন্য গ্রাম সভার যৌথ ঘোষণাপত্র।\n"
                "আমরা, {STATE} রাজ্যের {DISTRICT} জেলায় অবস্থিত {TEHSIL_TALUKA} তহসিলের বাসিন্দা।\n"
                "আমাদের {VILLAGE} গ্রামটি {GRAM_PANCHAYAT} গ্রাম পঞ্চায়েতের প্রশাসনিক কাঠামোর অন্তর্গত।\n"
                "আজ {GRAM_SABHA} গ্রাম সভায় একত্রিত হয়ে, আমরা আমাদের ঐতিহ্যগত বনজ সম্পদ অধিকার ঘোষণা করছি।\n"
                "এই সভার নেতৃত্ব দিচ্ছেন প্রধান সদস্য {GRAM_SABHA_MEMBER_NAME}।\n\n"

                "আমরা সকলেই ঐতিহ্যগত বনবাসী যারা {CATEGORY_SCHEDULED_TRIBE} অথবা {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} সম্প্রদায়ের অন্তর্গত।\n"
                "আমরা যে বনভূমির পরিচর্যা করি, তার খতিয়ান/কম্পার্টমেন্ট নম্বর {KHASRA_COMPARTMENT_NUMBER} ভূমি রেকর্ডে লিপিবদ্ধ রয়েছে।\n"
                "আমাদের বনাঞ্চলের চারপাশের প্রতিবেশী গ্রামগুলি {BORDERING_VILLAGE} নামে পরিচিত।\n"
                "উত্তরে নদী এবং দক্ষিণে পাহাড় পর্যন্ত বিস্তৃত আমাদের সীমানার বিবরণ হলো {BOUNDARY_DESCRIPTION}।\n"
                "এই সীমানার মধ্যে উপলব্ধ সমস্ত সম্পদ সংরক্ষণের সম্পূর্ণ অধিকার আমাদের রয়েছে।\n\n"

                "জীববৈচিত্র্য বজায় রাখতে এবং জঙ্গল ধ্বংসের হাত থেকে বাঁচাতে আমরা দৃঢ়প্রতিজ্ঞ।\n"
                "নিজেদের দাবি মজবুত করতে আমরা প্রমাণের একটি তালিকা {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} প্রস্তুত করেছি।\n"
                "মৌখিক ইতিহাস এবং ঐতিহাসিক দলিলগুলিকে {EVIDENCE_ITEM} হিসেবে উপস্থাপন করা হয়েছে।\n"
                "এই প্রমাণের ভিত্তিতে, গোষ্ঠীগত বনজ সম্পদ অধিকার (CFR) আমাদের অবিলম্বে প্রদান করা উচিত।\n"
                "আমরা সরকারি আধিকারিকদের অনুরোধ করছি তারা যেন দ্রুত বিবেচনা করে আদেশ জারি করেন।"
            ),
            # Variation 3: Formal Letter Style
            (
                "বিষয়: ধারা ৩(১)(ঝ)-এর অধীনে গোষ্ঠীগত বনজ সম্পদের (CFR) ওপর অধিকারের দাবি।\n"
                "এলাকার বিবরণ: তহসিল {TEHSIL_TALUKA}, জেলা {DISTRICT}, রাজ্য {STATE}।\n"
                "গ্রাম: {VILLAGE}, পঞ্চায়েত: {GRAM_PANCHAYAT}, গ্রাম সভা: {GRAM_SABHA}।\n"
                "এই দাবিটি গ্রাম সভার সদস্য {GRAM_SABHA_MEMBER_NAME}-এর নেতৃত্বে প্রশাসনের কাছে পেশ করা হচ্ছে।\n"
                "আবেদনকারীরা মূলত {CATEGORY_SCHEDULED_TRIBE} এবং {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} বর্গের সাথে যুক্ত।\n\n"

                "আমাদের দ্বারা সংরক্ষিত বনাঞ্চলের খতিয়ান বা কম্পার্টমেন্ট নম্বর হলো {KHASRA_COMPARTMENT_NUMBER}।\n"
                "আমাদের সীমানার সাথে যুক্ত সীমান্ত গ্রামগুলি, যেমন {BORDERING_VILLAGE}, এই বনটি ভাগ করে না।\n"
                "আমাদের গোষ্ঠীগত বনজ সম্পদের ভৌগোলিক সীমানা {BOUNDARY_DESCRIPTION} অনুযায়ী মানচিত্রে চিহ্নিত করা হয়েছে।\n"
                "এই অঞ্চলের পরিবেশগত ভারসাম্য বজায় রাখা আমাদের সম্প্রদায়ের প্রাথমিক কর্তব্য।\n"
                "অতএব, এই বনজ সম্পদগুলি পরিচালনার সম্পূর্ণ অধিকার আমাদের গ্রাম সভাকে দেওয়া উচিত।\n\n"

                "এই জমির সাথে আমাদের প্রথাগত সম্পর্ক প্রমাণ করার জন্য প্রমাণাদি সংকলন করা হয়েছে।\n"
                "গুরুত্বপূর্ণ নথিপত্রের তালিকা {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} আনুষ্ঠানিকভাবে জমা দেওয়া হচ্ছে।\n"
                "অন্যান্য জোরালো প্রমাণ হিসেবে {EVIDENCE_ITEM} নথিপত্রও এই আবেদনের সাথে যুক্ত করা হয়েছে।\n"
                "এই সমস্ত প্রমাণ আমাদের দাবির বৈধতা এবং ন্যায্যতা সম্পূর্ণরূপে প্রমাণ করে।\n"
                "এর ভিত্তিতে আমাদের গ্রাম সভার গোষ্ঠীগত বনজ সম্পদ অধিকার সরকারি স্বীকৃতি পাওয়া উচিত।"
            ),
            # Variation 4: Legal / Statutory Declaration Style
            (
                "গোষ্ঠীগত বনজ সম্পদ (Community Forest Resource) দাবির বিধিবদ্ধ প্রামাণ্য দলিল।\n"
                "বন অধিকার আইন ২০০৬, ধারা ৩(১)(ঝ)-এর অধীনে, {STATE} রাজ্য, {DISTRICT} জেলা, {TEHSIL_TALUKA} তহসিলের কর্তৃপক্ষের কাছে উপস্থাপিত আইনি দাবি।\n"
                "এই আনুষ্ঠানিক দাবিটি {VILLAGE} গ্রামবাসীদের পক্ষে, {GRAM_PANCHAYAT} গ্রাম পঞ্চায়েত এবং {GRAM_SABHA} গ্রাম সভার মাধ্যমে পেশ করা হচ্ছে।\n"
                "গ্রাম সভার অনুমোদিত আইনি প্রতিনিধি {GRAM_SABHA_MEMBER_NAME} এই দলিলে স্বাক্ষর করছেন।\n"
                "এই দাবিতে অন্তর্ভুক্ত সদস্যরা {CATEGORY_SCHEDULED_TRIBE} বা {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} নামক আইনি শ্রেণির দ্বারা সুরক্ষিত।\n\n"

                "দাবিকৃত বনজ সম্পদ এলাকার ভৌগোলিক অবস্থান, জমির পরিমাপ এবং সীমানা সম্পর্কিত বিধিবদ্ধ ভুক্তি।\n"
                "দাবির অধীনে থাকা বনাঞ্চলের আইনি খতিয়ান (Khasra) বা বন বিভাগের কম্পার্টমেন্ট নম্বর {KHASRA_COMPARTMENT_NUMBER} রাজস্ব রেকর্ডে লিপিবদ্ধ আছে।\n"
                "রাজস্ব মানচিত্র অনুসারে, এই এলাকার সাথে সীমানা ভাগ করে নেওয়া পার্শ্ববর্তী গ্রামগুলি হলো {BORDERING_VILLAGE}।\n"
                "সমগ্র দাবিকৃত বনজ সম্পদ এলাকার ভৌগোলিক এবং ভূ-প্রাকৃতিক সীমানা {BOUNDARY_DESCRIPTION} হিসেবে অত্যন্ত স্পষ্টভাবে সংজ্ঞায়িত করা হয়েছে।\n"
                "এই সীমানার মধ্যে অবস্থিত বনজ সম্পদের টেকসই ব্যবহার এবং পরিচালনার প্রথাগত আইনি অধিকার এই সম্প্রদায়ের রয়েছে।\n"
                "এই এলাকায় বন সম্পদের পুনরুৎপাদনের দায়িত্ব এবং অধিকার আইনগতভাবে গ্রাম সভাকে দেওয়া উচিত।\n\n"

                "প্রামাণ্য দলিলের উপস্থাপন এবং আইনি দাবির নিশ্চয়তা।\n"
                "এই সম্প্রদায়ের প্রথাগত সম্পর্ক প্রমাণ করার জন্য, প্রমাণের আনুষ্ঠানিক তালিকা {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} সংযুক্ত করা হয়েছে।\n"
                "সাথে, গ্রাম্য রেকর্ড এবং ঐতিহাসিক দলিলের মতো অতিরিক্ত প্রমাণ {EVIDENCE_ITEM} হিসেবে উপস্থাপন করা হয়েছে।\n"
                "এই সমস্ত দলিল আইনের নিয়ম ১৩-এর অধীনে আইনি প্রমাণ হিসেবে গ্রহণযোগ্য এবং বৈধ।\n"
                "এই প্রমাণের ভিত্তিতে, সম্পূর্ণ এলাকার সংরক্ষণ এবং উন্নয়নের বিধিবদ্ধ অধিকার গ্রাম সভাকে প্রদান করা অনিবার্য।\n"
                "আইনি বিধান অনুযায়ী এই দাবির ওপর দ্রুত পর্যালোচনা করে গেজেট আদেশ জারি করার অনুরোধ করা হচ্ছে।"
            )
        ],

        DOC_TITLE_UNDER_OCCUPATION: [
            # Variation 1: Bureaucratic / Form Style
            (
                "পরিশিষ্ট - II [নিয়ম ৮(জ) দ্রষ্টব্য]\n"
                "দখলের অধীনে থাকা বনভূমির জন্য আনুষ্ঠানিক অধিকারপত্র / পাট্টা।\n"
                "বনভূমির এই অধিকারপত্রটি রাজ্য সরকার কর্তৃক {TITLE_HOLDER_NAME}-কে প্রদান করা হচ্ছে।\n"
                "পাট্টা প্রাপকের পিতা/মাতার নাম {FATHER_MOTHER_NAME} এবং স্বামী/স্ত্রীর নাম {SPOUSE_NAME}।\n"
                "এঁদের ওপর নির্ভরশীল ব্যক্তি {DEPENDENT_NAME}-ও এই অধিকারপত্রের সুরক্ষার আওতায় আসেন।\n\n"

                "পাট্টা প্রাপকের সম্পূর্ণ নিবন্ধিত ঠিকানা হলো {TITLE_ADDRESS_FULL}।\n"
                "এই বনভূমিটি {VILLAGE} গ্রাম এবং {GRAM_PANCHAYAT} গ্রাম পঞ্চায়েতের ভৌগোলিক এলাকায় অবস্থিত।\n"
                "এটি {GRAM_SABHA} গ্রাম সভার এক্তিয়ারে, {TEHSIL_TALUKA} তহসিলের অধীনে পড়ে।\n"
                "এটি জেলা {DISTRICT} এবং রাজ্য {STATE}-এর প্রশাসনিক নিয়ন্ত্রণের অধীনে রয়েছে।\n"
                "এতদ্বারা প্রত্যয়ন করা যাইতেছে যে ধারক {CATEGORY_SCHEDULED_TRIBE} বা {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} শ্রেণির একজন যোগ্য সদস্য।\n\n"

                "এই দলিল দ্বারা অধিকারে দেওয়া বনভূমির মোট ক্ষেত্রফল হলো {TITLE_LAND_AREA_MEASURE}।\n"
                "ভূমির রেকর্ডে এই জমির খতিয়ান বা কম্পার্টমেন্ট নম্বর {KHASRA_COMPARTMENT_NUMBER} হিসেবে নথিবদ্ধ আছে।\n"
                "জমির চারদিকের সীমানা প্রাকৃতিক চিহ্ন দ্বারা {BOUNDARY_DESCRIPTION} হিসেবে বর্ণনা করা হয়েছে।\n"
                "এই অধিকারটি বংশানুক্রমিক, তবে এটি বিক্রি বা হস্তান্তর করা যাবে না।\n"
                "জেলাশাসক এবং বিভাগীয় বন আধিকারিকের স্বাক্ষরের মাধ্যমে এটি আনুষ্ঠানিকভাবে জারি করা হয়েছে।"
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "উপজাতীয় বিষয়ক মন্ত্রক কর্তৃক জারি করা ব্যক্তিগত বনভূমির অধিকারপত্র (পাট্টা)।\n"
                "শ্রী/শ্রীমতী {TITLE_HOLDER_NAME} (পিতা/মাতা: {FATHER_MOTHER_NAME}, স্বামী/স্ত্রী: {SPOUSE_NAME})-কে এই পাট্টা প্রদান করা হচ্ছে।\n"
                "তাঁর ওপর নির্ভরশীল {DEPENDENT_NAME}-এর মতো পরিবারের অন্যান্য সদস্যদেরও এই জমির ওপর অধিকার সুরক্ষিত থাকবে।\n"
                "এঁদের আবাসিক ঠিকানা {TITLE_ADDRESS_FULL} হিসেবে সরকারি রেকর্ডে যথাযথভাবে লিপিবদ্ধ হয়েছে।\n"
                "এই এলাকাটি {STATE} রাজ্যের {DISTRICT} জেলায় অবস্থিত {TEHSIL_TALUKA} তহসিলের অন্তর্গত।\n\n"

                "এই জমিটি {VILLAGE} গ্রামে, {GRAM_PANCHAYAT} পঞ্চায়েতের অধীনে, {GRAM_SABHA} গ্রাম সভার নিয়ন্ত্রণে রয়েছে।\n"
                "সুবিধাভোগী উপজাতি শ্রেণি {CATEGORY_SCHEDULED_TRIBE} বা প্রথাগত বনবাসী {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} হিসেবে স্বীকৃতি পেয়েছেন।\n"
                "সরকার কৃষি এবং আবাসনের উদ্দেশ্যে এঁদের {TITLE_LAND_AREA_MEASURE} আয়তনের জমি বরাদ্দ করেছে।\n"
                "রাজস্ব রেকর্ডে সেই জমির খতিয়ান বা পরিমাপ সংখ্যা {KHASRA_COMPARTMENT_NUMBER} স্পষ্টভাবে চিহ্নিত আছে।\n"
                "স্থানটির সঠিক অবস্থান এবং পরিধি {BOUNDARY_DESCRIPTION}-এর সীমানা নির্ধারণের বিবরণের মাধ্যমে প্রামাণ্য করা হয়েছে।\n\n"

                "এই বনভূমির পাট্টা বন অধিকার আইন ২০০৬-এর সমস্ত নিয়মের অধীন।\n"
                "ধারকের কেবলমাত্র এই জমিতে চাষাবাদ করার এবং বংশপরম্পরায় এটি উপভোগ করার অধিকার রয়েছে।\n"
                "কোনো অবস্থাতেই এই বনভূমি অন্য কোনো ব্যক্তিকে বিক্রি বা লিজ দেওয়া যাবে না।\n"
                "সংশ্লিষ্ট দপ্তরের আধিকারিকদের দ্বারা রাজ্য সরকারের আনুষ্ঠানিক মোহরের সাথে এটি যাচাই করা হয়েছে।\n"
                "এই দলিলটি পাট্টা প্রাপকের জীবিকা রক্ষাকারী আইনি ঢাল হিসেবে কাজ করবে।"
            ),
            # Variation 3: Formal Letter Style
            (
                "বনভূমির অধিকারের আদেশ এবং পাট্টার শংসাপত্র।\n"
                "অধিকার ধারকের নাম: {TITLE_HOLDER_NAME}। পিতামাতার নাম: {FATHER_MOTHER_NAME}। স্বামী/স্ত্রী: {SPOUSE_NAME}।\n"
                "নির্ভরশীল সদস্য: {DEPENDENT_NAME}। ধারকের শ্রেণি: {CATEGORY_SCHEDULED_TRIBE} / {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER}।\n"
                "ঠিকানা: {TITLE_ADDRESS_FULL}, গ্রাম: {VILLAGE}, পঞ্চায়েত: {GRAM_PANCHAYAT}, গ্রাম সভা: {GRAM_SABHA}।\n"
                "তহসিল: {TEHSIL_TALUKA}, জেলা: {DISTRICT}, রাজ্য: {STATE}।\n\n"

                "বন অধিকার আইন ২০০৬-এর ধারা ৪-এর অধীনে এই জমির অধিকার আনুষ্ঠানিকভাবে স্বীকৃতি পাচ্ছে।\n"
                "উপর্যুক্ত সুবিধাভোগীর দখলে থাকা {TITLE_LAND_AREA_MEASURE} আয়তনের জমির জন্য পাট্টা প্রদান করা হচ্ছে।\n"
                "রাজস্ব বিভাগের রেকর্ড অনুযায়ী, এই জমির খতিয়ান নম্বর হলো {KHASRA_COMPARTMENT_NUMBER}।\n"
                "জমির সীমানা {BOUNDARY_DESCRIPTION}-এর চিহ্নগুলি দিয়ে নিখুঁতভাবে সংজ্ঞায়িত করা হয়েছে।\n"
                "সমস্ত যাচাই এবং পরিদর্শনের পর, জেলা স্তরের কমিটি (DLC) এই জমি বরাদ্দের অনুমোদন দিয়েছে।\n\n"

                "এই জমির অধিকার একটি বংশানুক্রমিক অধিকার হিসেবে অব্যাহত থাকবে, তবে জমি অহস্তান্তরযোগ্য (non-transferable)।\n"
                "সুবিধাভোগীকে সরকার কর্তৃক সময়ে সময়ে বলবৎ হওয়া বন সংরক্ষণ আইন মেনে চলা বাধ্যতামূলক হবে।\n"
                "এর মাধ্যমে সরকার বনবাসীদের অর্থনৈতিক ও সামাজিক নিরাপত্তা নিশ্চিত করছে।\n"
                "এই শংসাপত্রটি রাজ্য সরকারের অনুমোদিত আধিকারিকদের দ্বারা স্বাক্ষরিত এবং মোহরযুক্ত।\n"
                "এই দলিলটি জারি হওয়ার তারিখ থেকে আইনগতভাবে কার্যকর হবে।"
            ),
            # Variation 4: Legal / Statutory Document Style
            (
                "বনভূমি অধিকার আইন ২০০৬-এর অধীনে বিধিবদ্ধ পাট্টা দলিল (Statutory Title Deed)।\n"
                "রাজ্য সরকারের আইনি ক্ষমতার অধীনে, এই অধিকারপত্রটি {TITLE_HOLDER_NAME} নামক সুবিধাভোগীর অনুকূলে বিধিবদ্ধভাবে নিবন্ধিত করা হচ্ছে।\n"
                "রেকর্ড অনুযায়ী সুবিধাভোগীর পিতা/মাতার নাম {FATHER_MOTHER_NAME} এবং আইনি স্বামী/স্ত্রীর নাম {SPOUSE_NAME} যাচাই করা হয়েছে।\n"
                "সুবিধাভোগীর ওপর সম্পূর্ণ নির্ভরশীল আইনি উত্তরাধিকারীদের নাম {DEPENDENT_NAME}-ও এই দলিলে অন্তর্ভুক্ত করা হয়েছে।\n"
                "সুবিধাভোগীর আনুষ্ঠানিক এবং আইনি আবাসিক ঠিকানা {TITLE_ADDRESS_FULL} হিসেবে রাজস্ব ও বন বিভাগের নথিতে নিবন্ধিত।\n"
                "এই ভূখণ্ডটি {STATE} রাজ্য, {DISTRICT} জেলা, {TEHSIL_TALUKA} তহসিলের অন্তর্গত {VILLAGE} গ্রাম, {GRAM_PANCHAYAT} গ্রাম পঞ্চায়েত এবং {GRAM_SABHA} গ্রাম সভার আইনি এক্তিয়ারে অবস্থিত।\n\n"

                "সুবিধাভোগীর আইনি শ্রেণিবিন্যাস, জমির পরিমাপ এবং ভৌগোলিক সীমানার শংসাপত্র।\n"
                "সুবিধাভোগীকে আইনের আইনি বিধানের অধীনে {CATEGORY_SCHEDULED_TRIBE} বা {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} শ্রেণির যোগ্য সদস্য হিসেবে বিবেচনা করা হয়েছে।\n"
                "সরকার দ্বারা যথাযথ পরিমাপের পর বরাদ্দকৃত বনভূমির মোট ক্ষেত্রফল {TITLE_LAND_AREA_MEASURE} হিসেবে ঘোষণা করা হয়েছে।\n"
                "রাজস্ব এবং বন বিভাগের রেকর্ডে এই জমির নির্দিষ্ট খতিয়ান (Khasra) বা কম্পার্টমেন্ট নম্বর {KHASRA_COMPARTMENT_NUMBER} উল্লেখ করা হয়েছে।\n"
                "এই ভূখণ্ডের চারদিকের ভৌগোলিক এবং প্রাকৃতিক সীমানা {BOUNDARY_DESCRIPTION} হিসেবে অত্যন্ত স্পষ্টভাবে চিহ্নিত করা হয়েছে।\n"
                "এই পরিমাপ রাজস্ব পরিদর্শক এবং বন বিভাগের সার্ভেয়ারদের সরাসরি শারীরিক যাচাইয়ের পর করা হয়েছে।\n\n"

                "অধিকারের আইনি প্রকৃতি, বিধিনিষেধ এবং কর্তৃপক্ষের অনুমোদন।\n"
                "ধারা ৪(৪)-এর বিধানের অধীনে, এই জমির অধিকার সম্পূর্ণ বংশানুক্রমিক, তবে কোনো অবস্থাতেই এটি বিক্রি, হস্তান্তর বা বন্ধক রাখা যাবে না (non-alienable)।\n"
                "সুবিধাভোগী বন সংরক্ষণ আইন এবং পরিবেশ সুরক্ষা বিধিমালা মেনে চলতে আইনত বাধ্য থাকবেন।\n"
                "যদি কোনো নিয়ম লঙ্ঘন করা হয়, তবে কোনো পূর্ব নোটিশ ছাড়াই রাজ্য সরকার এই অধিকার বাতিল করার পূর্ণ ক্ষমতা রাখে।\n"
                "এই বিধিবদ্ধ পাট্টা মহকুমা (SDLC) এবং জেলা স্তরের (DLC) কমিটির যথাযথ অনুমোদনের পরেই জারি করা হয়েছে।\n"
                "এর আইনি প্রমাণের জন্য, জেলাশাসক (District Collector) এবং বিভাগীয় বন আধিকারিক (DFO) এই পাট্টায় আনুষ্ঠানিক স্বাক্ষর এবং মোহর দিয়েছেন।"
            )
        ],

        DOC_TITLE_COMMUNITY_FOREST_RIGHTS: [
            # Variation 1: Bureaucratic / Form Style
            (
                "পরিশিষ্ট - III [নিয়ম ৮(জ) দ্রষ্টব্য]\n"
                "গোষ্ঠীগত বন অধিকারের পাট্টা এবং আনুষ্ঠানিক অধিকারের দলিল।\n"
                "এই গোষ্ঠীগত বন অধিকারটি {COMMUNITY_RIGHT_HOLDER_NAME} নামক একটি যৌথ সত্তাকে প্রদান করা হচ্ছে।\n"
                "এই অঞ্চলটি {STATE} রাজ্য, {DISTRICT} জেলা এবং {TEHSIL_TALUKA} তহসিলের অধীনে আসে।\n"
                "এই পাট্টাটি {VILLAGE} গ্রাম, {GRAM_PANCHAYAT} গ্রাম পঞ্চায়েত এবং {GRAM_SABHA} গ্রাম সভার যৌথ সম্পত্তি।\n\n"

                "এই অধিকার প্রাপ্ত সম্প্রদায়টি {CATEGORY_SCHEDULED_TRIBE} বা {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} হিসেবে স্বীকৃত।\n"
                "সম্প্রদায়কে দেওয়া অধিকারের প্রকৃতি {COMMUNITY_RIGHT_NATURE} হিসেবে স্পষ্টভাবে সংজ্ঞায়িত করা হয়েছে।\n"
                "এই অধিকার ব্যবহারের সাথে যুক্ত কিছু শর্ত রয়েছে, যা হলো: {TITLE_CONDITIONS}।\n"
                "এই অধিকারের অধীনে থাকা বনাঞ্চলের খতিয়ান/কম্পার্টমেন্ট নম্বর হলো {KHASRA_COMPARTMENT_NUMBER}।\n"
                "জমির সীমানাগুলি {BOUNDARY_DESCRIPTION} এর মতো ভৌগোলিক নির্দেশের দ্বারা নির্দেশিত হয়েছে।\n\n"

                "এছাড়া, এই এলাকার প্রথাগত ঐতিহ্যবাহী সীমানা (Customary Boundary) {CUSTOMARY_BOUNDARY}-কেও প্রথাগতভাবে স্বীকৃতি দেওয়া হয়েছে।\n"
                "এই দলিলটি যৌথ ব্যবহারের জন্য বনজ সম্পদের প্রবেশাধিকারকে আইনি স্বীকৃতি প্রদান করে।\n"
                "তবে, সম্পদের ব্যবহার এমনভাবে করা উচিত যাতে বনের জীববৈচিত্র্যের কোনো ক্ষতি না হয়।\n"
                "নিয়ম লঙ্ঘন করা হলে সরকারের এই অধিকার পুনর্বিবেচনা করার ক্ষমতা সংরক্ষিত রয়েছে।\n"
                "এই পাট্টাটি জেলা পর্যায়ের কর্তৃপক্ষের দ্বারা অনুমোদিত এবং জারি করা হয়েছে।"
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "গোষ্ঠীগত বন অধিকারের পাট্টা এবং গ্রাম সভাকে আইনি অধিকার হস্তান্তরের দলিল।\n"
                "সরকারের যথাযথ অনুমোদনের সাথে, এই অধিকার {COMMUNITY_RIGHT_HOLDER_NAME} সংস্থা/সম্প্রদায়কে দেওয়া হচ্ছে।\n"
                "এই সম্প্রদায়টি দীর্ঘদিন ধরে {STATE} রাজ্যের {DISTRICT} জেলায় অবস্থিত {TEHSIL_TALUKA} তহসিলে বসবাস করছে।\n"
                "তাঁদের বাসস্থানের এলাকা {VILLAGE} গ্রাম, {GRAM_PANCHAYAT} পঞ্চায়েত এবং {GRAM_SABHA} গ্রাম সভার মধ্যে অন্তর্ভুক্ত।\n"
                "তাঁদের সরকারি নথিতে {CATEGORY_SCHEDULED_TRIBE} এবং {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} শ্রেণি হিসেবে অন্তর্ভুক্ত করা হয়েছে।\n\n"

                "তাঁদের দেওয়া যৌথ অধিকারের সুনির্দিষ্ট প্রকৃতির বর্ণনা হলো {COMMUNITY_RIGHT_NATURE}।\n"
                "এই যৌথ অধিকার প্রয়োগের জন্য নির্ধারিত নিয়ম ও শর্তাবলী হলো {TITLE_CONDITIONS}।\n"
                "বন দপ্তরের রেকর্ড অনুসারে, এই এলাকার খতিয়ান নম্বর {KHASRA_COMPARTMENT_NUMBER} চিহ্নিত আছে।\n"
                "এই এলাকার সীমানা প্রাকৃতিক ল্যান্ডমার্ক ব্যবহার করে {BOUNDARY_DESCRIPTION} হিসেবে বর্ণনা করা হয়েছে।\n"
                "একই সাথে, বংশপরম্পরায় চলে আসা প্রথাগত সীমানা {CUSTOMARY_BOUNDARY} হিসেবে নিশ্চিত করা হয়েছে।\n\n"

                "এই দলিলের মাধ্যমে গোচারণ এবং গৌণ বনজ সম্পদ সংগ্রহের যৌথ অধিকার সুরক্ষিত করা হয়েছে।\n"
                "পরিবেশ ও বনাঞ্চল রক্ষার দায়িত্ব এই সম্প্রদায়ের হাতে তুলে দেওয়া হচ্ছে।\n"
                "বেআইনি গাছ কাটা এবং শিকারের মতো অবৈধ কার্যকলাপ সম্পূর্ণভাবে নিষিদ্ধ।\n"
                "এটি রাজ্য সরকারের উপজাতি কল্যাণ দপ্তর এবং রাজস্ব দপ্তরের সম্মতিতে জারি করা হয়েছে।\n"
                "গ্রাম সভাকে এই দলিলটি সুরক্ষিত রাখতে হবে এবং এর বিধানগুলি সঠিকভাবে প্রয়োগ করতে হবে।"
            ),
            # Variation 3: Formal Letter Style
            (
                "গোষ্ঠীগত বন অধিকারকে স্বীকৃতি প্রদানকারী আনুষ্ঠানিক অধিকারের শংসাপত্র।\n"
                "অধিকার প্রাপক: {COMMUNITY_RIGHT_HOLDER_NAME}।\n"
                "এলাকা: {VILLAGE} গ্রাম, {GRAM_PANCHAYAT} পঞ্চায়েত, {GRAM_SABHA} গ্রাম সভা।\n"
                "প্রশাসনিক সীমানা: তহসিল {TEHSIL_TALUKA}, জেলা {DISTRICT}, রাজ্য {STATE}।\n"
                "সুবিধাভোগী শ্রেণি: {CATEGORY_SCHEDULED_TRIBE} অথবা {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER}।\n\n"

                "রাজ্য সরকার কর্তৃক উপর্যুক্ত সম্প্রদায়কে {COMMUNITY_RIGHT_NATURE} প্রকৃতির বন অধিকার প্রদান করা হচ্ছে।\n"
                "এই অধিকারটি {TITLE_CONDITIONS}-এ উল্লিখিত সীমাবদ্ধতা এবং শর্তাবলীর অধীন থাকবে।\n"
                "বরাদ্দকৃত বনভূমির খতিয়ান বা পরিমাপ সংখ্যা {KHASRA_COMPARTMENT_NUMBER} নির্ধারণ করা হয়েছে।\n"
                "দলিলে নির্দিষ্ট করা জমির সীমানা {BOUNDARY_DESCRIPTION} চিহ্নের মাধ্যমে স্থির করা হয়েছে।\n"
                "সম্প্রদায় দ্বারা ঐতিহ্যগতভাবে স্বীকৃত প্রথাগত সীমানাও {CUSTOMARY_BOUNDARY} প্রত্যয়িত হচ্ছে।\n\n"

                "এই অধিকারের প্রয়োগ শুধুমাত্র গ্রাম সভার যৌথ পরিচালনার অধীনেই করা উচিত।\n"
                "বনজ সম্পদের ব্যবহার বাণিজ্যিক উদ্দেশ্যে নয়, শুধুমাত্র যৌথ প্রয়োজনের জন্য করা উচিত।\n"
                "সরকারি অডিট এবং পরিদর্শনে গ্রাম সভার পূর্ণ সহযোগিতা প্রদান বাধ্যতামূলক।\n"
                "এই দলিলটি জেলাশাসক এবং বিভাগীয় বন আধিকারিকের মোহর সহ জারি করা হচ্ছে।\n"
                "এটি জারি হওয়ার তারিখ থেকে, সম্প্রদায়ের বন-ভিত্তিক অর্থনৈতিক স্বাধীনতা নিশ্চিত করা হলো।"
            ),
            # Variation 4: Legal / Statutory Document Style
            (
                "গোষ্ঠীগত বন অধিকারের (CFR) গেজেট বিজ্ঞাপিত আইনি দলিল (Statutory Deed) এবং পাট্টা।\n"
                "এই আনুষ্ঠানিক দলিলের মাধ্যমে, {COMMUNITY_RIGHT_HOLDER_NAME} নামক একটি যৌথ সংস্থাকে বনভূমির ওপর আইনি অধিকার প্রদান করা হচ্ছে।\n"
                "এই অধিকারটি {STATE} রাজ্য, {DISTRICT} জেলা এবং {TEHSIL_TALUKA} তহসিলের ভৌগোলিক এক্তিয়ারের মধ্যে প্রদান করা হচ্ছে।\n"
                "আইনগতভাবে এই এলাকাটি {VILLAGE} গ্রাম, {GRAM_PANCHAYAT} গ্রাম পঞ্চায়েত এবং {GRAM_SABHA} গ্রাম সভার প্রশাসনিক নিয়ন্ত্রণের অধীনে আসে।\n"
                "অধিকার প্রাপ্ত এই সম্প্রদায়, সরকারি রেকর্ড অনুযায়ী {CATEGORY_SCHEDULED_TRIBE} বা {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} আইনি শ্রেণির অধীনে সুরক্ষিত।\n"
                "গ্রাম সভার যৌথ প্রস্তাব এবং জেলা স্তরের কমিটির (DLC) অনুমোদনের ভিত্তিতে এই দলিলটি আইনগতভাবে জারি করা হচ্ছে।\n\n"

                "স্বীকৃত যৌথ অধিকারের প্রকৃতি, শর্তাবলী এবং ভৌগোলিক প্রামাণ্যকরণ।\n"
                "সরকার কর্তৃক এই সম্প্রদায়কে আনুষ্ঠানিকভাবে প্রদত্ত অধিকারের প্রকৃতি {COMMUNITY_RIGHT_NATURE} হিসেবে সুনির্দিষ্টভাবে সংজ্ঞায়িত করা হয়েছে।\n"
                "এই অধিকার ব্যবহার করার জন্য বন দপ্তর কর্তৃক আরোপিত আইনি শর্ত এবং বিধিনিষেধ এই রূপ: {TITLE_CONDITIONS}।\n"
                "যৌথ অধিকারের অধীনে থাকা বনাঞ্চলের আইনি খতিয়ান বা পরিমাপ সংখ্যা {KHASRA_COMPARTMENT_NUMBER} হিসেবে নিবন্ধিত আছে।\n"
                "জমির সীমানাগুলি পাহাড়, নদীর মতো প্রাকৃতিক চিহ্নের উল্লেখ করে {BOUNDARY_DESCRIPTION} হিসেবে নথিবদ্ধ করা হয়েছে।\n"
                "এছাড়া, বহু প্রজন্ম ধরে সম্প্রদায় কর্তৃক স্বীকৃত প্রথাগত সীমানা (Customary Boundary) {CUSTOMARY_BOUNDARY} আইনিভাবে নিশ্চিত করা হয়েছে।\n\n"

                "সম্প্রদায়ের আইনি দায়িত্ব, বিধিনিষেধ এবং সরকারের চূড়ান্ত অনুমোদন।\n"
                "এই অধিকারের প্রমাণপত্রটি সম্পূর্ণরূপে যৌথ ব্যবহারের উদ্দেশ্যে; এর যেকোনো প্রকার বাণিজ্যিক (Commercial) শোষণ নিষিদ্ধ।\n"
                "পশু চারণ এবং বনজ সম্পদ সংগ্রহের পাশাপাশি বনের জীববৈচিত্র্যের কোনো ক্ষতি না হয় তা নিশ্চিত করা সম্প্রদায়ের আইনি দায়িত্ব।\n"
                "যদি বেআইনি গাছ কাটা বা রাষ্ট্রবিরোধী কার্যকলাপে জড়িত থাকার প্রমাণ পাওয়া যায়, তবে অবিলম্বে এই অধিকার বাতিল করা হবে।\n"
                "উপজাতি কল্যাণ দপ্তর এবং বন দপ্তরের পূর্ণ সমন্বয়ে এই দলিলটি পরিচালিত হবে।\n"
                "জেলাশাসক (DM) এবং সংশ্লিষ্ট বন আধিকারিকের আনুষ্ঠানিক মোহর ও স্বাক্ষরের সাথে এই পাট্টা গেজেটে নিবন্ধিত হলো।"
            )
        ],

        DOC_TITLE_COMMUNITY_FOREST_RESOURCES: [
            # Variation 1: Bureaucratic / Form Style
            (
                "পরিশিষ্ট - IV [নিয়ম ৮(ঝ) দ্রষ্টব্য]\n"
                "গোষ্ঠীগত বনজ সম্পদের (CFR) জন্য পাট্টা এবং অধিকারপত্র।\n"
                "এই আনুষ্ঠানিক দলিলটি {STATE} রাজ্য, {DISTRICT} জেলা, {TEHSIL_TALUKA} তহসিলের আওতাধীন এলাকাকে প্রদান করা হচ্ছে।\n"
                "এর অধীনে, {VILLAGE} গ্রাম, {GRAM_PANCHAYAT} গ্রাম পঞ্চায়েত এবং {GRAM_SABHA} গ্রাম সভাকে গোষ্ঠীগত বনজ সম্পদের অধিকার দেওয়া হচ্ছে।\n"
                "এই অধিকারটি {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} অথবা {COMMUNITY_TYPE_BOTH} সম্প্রদায়ের অন্তর্ভুক্ত মানুষের জন্য প্রযোজ্য।\n\n"

                "এই গোষ্ঠীগত বনজ সম্পদ অধিকারের অধীন এলাকার খতিয়ান/কম্পার্টমেন্ট নম্বর হলো {KHASRA_COMPARTMENT_NUMBER}।\n"
                "এই এলাকার ভৌগোলিক অবস্থান এবং সীমানাগুলি {BOUNDARY_DESCRIPTION} হিসেবে অত্যন্ত স্পষ্টভাবে নথিবদ্ধ করা হয়েছে।\n"
                "একই সাথে, শতাব্দী প্রাচীন প্রথাগত সীমানা {CUSTOMARY_BOUNDARY} আইনি স্বীকৃতি পেয়েছে।\n"
                "নির্দিষ্ট এলাকার মধ্যে থাকা সমস্ত গৌণ বনজ সম্পদ পরিচালনার অধিকার গ্রাম সভাকে অর্পণ করা হয়েছে।\n"
                "বন দপ্তরের নির্দেশিকা অনুযায়ী সম্প্রদায়কে এই সম্পদগুলি সংরক্ষণ করতে হবে এবং স্থিতিশীলভাবে ব্যবহার করতে হবে।\n\n"

                "এই অধিকারটি আদিবাসী এবং অন্যান্য ঐতিহ্যগত বনবাসীদের জীবনযাত্রার মান উন্নত করার উদ্দেশ্যে দেওয়া হচ্ছে।\n"
                "বনজ সম্পদ পরিচালনার জন্য কমিটি গঠন করার পূর্ণ অধিকার গ্রাম সভাকে দেওয়া হয়েছে।\n"
                "এই সম্পদের ক্ষতি সাধনকারী যেকোনো কাজকে আইনি অপরাধ হিসেবে গণ্য করা হবে এবং অধিকার বাতিল করা হবে।\n"
                "রাজ্য সরকারের যোগ্য আধিকারিক, যেমন জেলাশাসক এবং বন আধিকারিক যথাযথভাবে এর অনুমোদন করেছেন।\n"
                "এই দলিলটি গোষ্ঠীগত বনজ সম্পদ সংরক্ষণে একটি গুরুত্বপূর্ণ মাইলফলক হিসেবে রেকর্ড করা হচ্ছে।"
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "গোষ্ঠীগত বনজ সম্পদের আইনি অধিকারের দলিল এবং গ্রাম সভার কাছে ক্ষমতা হস্তান্তর।\n"
                "সরকার {STATE} রাজ্যের {DISTRICT} জেলায় অবস্থিত {TEHSIL_TALUKA} তহসিলের বাসিন্দাদের দাবি মেনে নিয়েছে।\n"
                "এই ভিত্তিতে {VILLAGE} গ্রাম, {GRAM_PANCHAYAT} পঞ্চায়েত এবং {GRAM_SABHA} গ্রাম সভাকে CFR পাট্টা প্রদান করা হচ্ছে।\n"
                "এই অধিকারের স্বীকৃতি {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} অথবা {COMMUNITY_TYPE_BOTH} সম্প্রদায়ের ওপর প্রযোজ্য।\n"
                "এই সম্প্রদায়গুলি জঙ্গলকে দেবতা হিসেবে মানে এবং তা সংরক্ষণ করার ঐতিহ্য বজায় রাখে।\n\n"

                "গোষ্ঠীগত বনজ সম্পদ এলাকার জন্য খতিয়ান/কম্পার্টমেন্ট নম্বর {KHASRA_COMPARTMENT_NUMBER} ভূমি সমীক্ষা রেকর্ডে উল্লেখ করা আছে।\n"
                "এই এলাকার সীমানাগুলি পাহাড় এবং নদী চিহ্নিত করে {BOUNDARY_DESCRIPTION} হিসেবে সংজ্ঞায়িত করা হয়েছে।\n"
                "এর বাইরে আমাদের প্রথাগত সীমানা {CUSTOMARY_BOUNDARY}-ও সরকারের দ্বারা গৃহীত হয়েছে।\n"
                "এই সীমানার মধ্যে উপলব্ধ জ্বালানি কাঠ, মধু এবং ভেষজ উদ্ভিদ স্বাধীনভাবে ব্যবহার করার অধিকার গ্রাম সভার আছে।\n"
                "এছাড়া, বন মাফিয়াদের হাত থেকে জঙ্গল রক্ষার সম্পূর্ণ দায়িত্ব এই সম্প্রদায়ের হাতে তুলে দেওয়া হয়েছে।\n\n"

                "গোষ্ঠীগত বনজ সম্পদ অধিকার আইন আদিবাসীদের আত্মনিয়ন্ত্রণের অধিকার নিশ্চিত করে।\n"
                "জীববৈচিত্র্য বজায় রাখতে গ্রাম সভাকে একটি উপযুক্ত পরিচালনার পরিকল্পনা প্রস্তুত করতে হবে।\n"
                "সরকার এবং বন দপ্তর গ্রাম সভার পরিচালনা পরিকল্পনার জন্য শুধুমাত্র প্রযুক্তিগত সহায়তা প্রদান করবে।\n"
                "এই দলিলটি সম্প্রদায়ের অর্থনৈতিক উন্নয়ন এবং জঙ্গলের স্থায়িত্ব উভয়ই একসাথে সুনিশ্চিত করবে।\n"
                "সংশ্লিষ্ট আধিকারিকদের যথাযথ স্বাক্ষরের সাথে এই পাট্টা আজ থেকে কার্যকর হলো।"
            ),
            # Variation 3: Formal Letter Style
            (
                "শিরোনাম: গোষ্ঠীগত বনজ সম্পদের (CFR) ওপর অধিকার এবং পাট্টার শংসাপত্র।\n"
                "সুবিধাভোগী সংস্থা: {GRAM_SABHA} গ্রাম সভা, {VILLAGE} গ্রাম, {GRAM_PANCHAYAT} পঞ্চায়েত।\n"
                "অবস্থান: তহসিল {TEHSIL_TALUKA}, জেলা {DISTRICT}, রাজ্য {STATE}।\n"
                "সম্প্রদায়ের শ্রেণিবিন্যাস: {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} অথবা {COMMUNITY_TYPE_BOTH}।\n"
                "বিষয়: উপর্যুক্ত গ্রাম সভাকে গোষ্ঠীগত বনজ সম্পদ পরিচালনার আনুষ্ঠানিক অধিকার প্রদান করা।\n\n"

                "বন অধিকার আইন ২০০৬-এর বিধানের ভিত্তিতে এই ঐতিহাসিক অধিকার প্রদান করা হচ্ছে।\n"
                "অধিকার প্রাপ্ত বনভূমির খতিয়ান বা পরিমাপ সংখ্যা {KHASRA_COMPARTMENT_NUMBER} স্পষ্টভাবে নথিবদ্ধ করা হয়েছে।\n"
                "সেই এলাকার সীমানা {BOUNDARY_DESCRIPTION} বিবরণের মাধ্যমে ভৌগোলিকভাবে সংজ্ঞায়িত করা হয়েছে।\n"
                "সম্প্রদায় কর্তৃক প্রথাগতভাবে রক্ষিত প্রথাগত সীমানাও {CUSTOMARY_BOUNDARY} এর অন্তর্ভুক্ত।\n"
                "এই সীমানার মধ্যে থাকা সমস্ত প্রাকৃতিক সম্পদ রক্ষা এবং ব্যবহার করার অধিকার গ্রাম সভার।\n\n"

                "এই অধিকার কোনোভাবেই ব্যক্তিগত নয়, এটি সমগ্র সম্প্রদায়ের সাধারণ সম্পত্তি।\n"
                "বনজ সম্পদের দীর্ঘস্থায়ী পরিচালনার জন্য গ্রাম সভাকে একটি বন অধিকার কমিটি গঠন করে কাজ করতে হবে।\n"
                "দাবানলের মতো প্রাকৃতিক দুর্যোগ থেকে জঙ্গলকে রক্ষা করা সম্প্রদায়ের প্রাথমিক কর্তব্য।\n"
                "এই অধিকার রাজ্য স্তরের কমিটির দ্বারা পর্যালোচনা এবং চূড়ান্ত অনুমোদনের পর প্রদান করা হচ্ছে।\n"
                "এই শংসাপত্রটি সংশ্লিষ্ট জেলা আধিকারিকদের মোহর সহ আনুষ্ঠানিকভাবে জারি করা হচ্ছে।"
            ),
            # Variation 4: Legal / Statutory Document Style
            (
                "গোষ্ঠীগত বনজ সম্পদের (Community Forest Resources) বিধিবদ্ধ পাট্টা এবং সরকারের ক্ষমতা হস্তান্তরের দলিল।\n"
                "ধারা ৩(১)(ঝ)-এর বিধানের অধীনে, {STATE} রাজ্য, {DISTRICT} জেলা, {TEHSIL_TALUKA} তহসিলের এক্তিয়ারে এই দলিলটি আইনগতভাবে সম্পাদিত করা হচ্ছে।\n"
                "তদনুসারে, {VILLAGE} গ্রাম, {GRAM_PANCHAYAT} গ্রাম পঞ্চায়েত এবং {GRAM_SABHA} গ্রাম সভাকে গোষ্ঠীগত বনজ সম্পদ পরিচালনার সম্পূর্ণ আইনি অধিকার অর্পণ করা হচ্ছে।\n"
                "এই দলিলটি, {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} বা {COMMUNITY_TYPE_BOTH} সম্প্রদায়ের সাথে যুক্ত বাসিন্দাদের জীবিকা সুরক্ষিত করার একটি আইনি ফর্ম।\n"
                "জেলা স্তরের কমিটির (DLC) চূড়ান্ত আইনি অনুমোদনের পরেই এই অধিকারের শংসাপত্রটি আনুষ্ঠানিকভাবে প্রকাশ করা হচ্ছে।\n"
                "এর দ্বারা, রাষ্ট্রের মালিকানাধীন বনজ সম্পদ রক্ষা ও পরিচালনার অধিকার আইনগতভাবে গ্রাম সভার কাছে হস্তান্তর করা হচ্ছে।\n\n"

                "বনজ সম্পদ এলাকার বিধিবদ্ধ ভূমি-সমীক্ষা নম্বর, সীমানা এবং প্রথাগত প্রকাশ।\n"
                "যৌথ পরিচালনার অধীনে থাকা বনজ সম্পদ এলাকার খতিয়ান (Khasra) বা কম্পার্টমেন্ট নম্বর {KHASRA_COMPARTMENT_NUMBER} ভূমি সমীক্ষা রেকর্ডে স্পষ্টভাবে নিবন্ধিত রয়েছে।\n"
                "এই এলাকার ভৌগোলিক এবং ভূ-প্রাকৃতিক সীমানা {BOUNDARY_DESCRIPTION} হিসেবে মানচিত্রের মাধ্যমে সরকার দ্বারা আইনগতভাবে নিশ্চিত করা হয়েছে।\n"
                "প্রতিবেশী গ্রাম এবং বন দপ্তরের সাথে সীমানা ভাগ করে নেওয়া প্রথাগত সীমানা (Customary Boundary) {CUSTOMARY_BOUNDARY} আনুষ্ঠানিকভাবে প্রত্যয়িত হচ্ছে।\n"
                "এই সীমানার মধ্যে থাকা গৌণ বনজ সম্পদ, জলজ সম্পদ এবং গাছপালা ব্যবহার করার সম্পূর্ণ অধিকার গ্রাম সভাকে দেওয়া হয়েছে।\n"
                "সীমানা সংক্রান্ত কোনো বিবাদ এড়াতে ভূমি সমীক্ষা দপ্তরের মাধ্যমে উপযুক্ত সীমানা-স্তম্ভ এবং আইনি চিহ্ন স্থাপন করা হয়েছে।\n\n"

                "গ্রাম সভার আইনি দায়িত্ব, বন সংরক্ষণ এবং আধিকারিকদের চূড়ান্ত প্রত্যয়ন।\n"
                "আইনের মূল নিয়মগুলি ছাড়া, রাজ্য সরকার কর্তৃক এই অধিকারের ওপর অন্য কোনো নতুন বিধিনিষেধ বা শর্ত আরোপ করা হয়নি।\n"
                "তা সত্ত্বেও, বনের পরিবেশগত ভারসাম্য বজায় রাখা এবং দাবানল (Forest Fire)-এর মতো বিপর্যয় প্রতিরোধ করা গ্রাম সভার সম্পূর্ণ আইনি দায়িত্ব হবে।\n"
                "এই উদ্দেশ্যে গ্রাম সভার তরফ থেকে 'বনজ সম্পদ সংরক্ষণ কমিটি' গঠন করা বাধ্যতামূলক, যার রিপোর্ট প্রতি বছর সরকারকে জমা দিতে হবে।\n"
                "আইনবহির্ভূতভাবে বনজ সম্পদ ধ্বংস করা হলে, ফৌজদারি দণ্ডবিধির অধীনে গ্রাম সভাকে জবাবদিহি করতে হবে।\n"
                "রাজ্য সরকারের শীর্ষ আধিকারিক—জেলাশাসক, বিভাগীয় বন আধিকারিক (DFO) এবং উপজাতি কল্যাণ আধিকারিকের স্বাক্ষরের মাধ্যমে এই পাট্টা আইনগতভাবে কার্যকর হচ্ছে।"
            )
        ]
    },
 #odia
 
    "or": {
        DOC_CLAIM_FOREST_LAND: [
            # Variation 1: Bureaucratic / Form Style (Simulating Form A filled application)
            (
                "ଫର୍ମ - କ [ନିୟମ ୧୧(୧)(କ) ଦେଖନ୍ତୁ]\n"
                "ଜଙ୍ଗଲ ଜମି ଉପରେ ଅଧିକାର ପାଇଁ ଦାବି ଫର୍ମ ଏବଂ ଆବେଦନକାରୀଙ୍କ ପ୍ରାଥମିକ ବିବରଣୀ।\n"
                "ଦାବିଦାରଙ୍କ ସମ୍ପୂର୍ଣ୍ଣ ନାମ: {CLAIMANT_NAME}।\n"
                "ପିତା ଅଥବା ମାତାଙ୍କ ନାମ: {FATHER_MOTHER_NAME}। ସ୍ୱାମୀ/ସ୍ତ୍ରୀଙ୍କ ନାମ: {SPOUSE_NAME}।\n"
                "ଆବେଦନକାରୀଙ୍କ ସମ୍ପୂର୍ଣ୍ଣ ବାସସ୍ଥାନ ଠିକଣା: {ADDRESS_FULL} ଭାବେ ଲିପିବଦ୍ଧ ଅଛି।\n"
                "ଏହି ଜମି {STATE} ରାଜ୍ୟର ଅନ୍ତର୍ଗତ {DISTRICT} ଜିଲ୍ଲା ଏବଂ {TEHSIL_TALUKA} ତହସିଲ ସୀମାରେ ଅବସ୍ଥିତ।\n"
                "ସାଥିରେ, ଏହା {VILLAGE} ଗ୍ରାମ, {GRAM_PANCHAYAT} ଗ୍ରାମ ପଞ୍ଚାୟତ ତଥା {GRAM_SABHA} ଗ୍ରାମ ସଭାର ଅଧିକାର କ୍ଷେତ୍ରରେ ଆସୁଛି।\n\n"

                "ଦାବିଦାରଙ୍କ ପରିବାରର ବିବରଣୀ ଏବଂ ଜଙ୍ଗଲ ଜମି ଉପରେ ଦଖଲ ସ୍ଥିତି:\n"
                "ମୋ ପରିବାରର ସଦସ୍ୟ {FAMILY_MEMBER_NAME} (ବୟସ: {FAMILY_MEMBER_AGE} ବର୍ଷ) ଏବଂ ଆଶ୍ରିତ {DEPENDENT_NAME} ମୋ ସହିତ ବସବାସ କରୁଛନ୍ତି।\n"
                "ଆମେ ପ୍ରମାଣିତ କରୁଛୁ ଯେ ଆମେ {CATEGORY_SCHEDULED_TRIBE} ଅଥବା {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} ଶ୍ରେଣୀଭୁକ୍ତ ଅଟୁ।\n"
                "ବାସସ୍ଥାନ ଉଦ୍ଦେଶ୍ୟରେ ଆମ ଦଖଲରେ ଥିବା ଜଙ୍ଗଲ ଜମିର ପରିମାଣ {LAND_EXTENT_HABITATION} ନିର୍ଦ୍ଧାରିତ ହୋଇଛି।\n"
                "ସ୍ୱୟଂ ଚାଷ (କୃଷି) ପାଇଁ ବ୍ୟବହାର ହେଉଥିବା ଜମିର ପରିମାଣ {LAND_EXTENT_SELF_CULTIVATION} ଅଟେ।\n"
                "ଜଙ୍ଗଲ ଗ୍ରାମ (ଫରେଷ୍ଟ ଭିଲେଜ) ଗୁଡ଼ିକରେ ଅବସ୍ଥିତ ଜମିର ପରିମାଣ {LAND_EXTENT_FOREST_VILLAGE} ଭାବେ ରେକର୍ଡ ହୋଇଛି।\n\n"

                "ଜମି ସମ୍ବନ୍ଧୀୟ ଅନ୍ୟାନ୍ୟ ଦାବି, ବିବାଦ ଏବଂ ସଂଲଗ୍ନ ପ୍ରମାଣ:\n"
                "ଯଦି ଏହି ଜମି ଉପରେ କୌଣସି ବିବାଦ ଅଛି, ତେବେ ତାର ବିବରଣୀ: {DISPUTED_LAND_DESCRIPTION}।\n"
                "ପୂର୍ବରୁ ପ୍ରଦାନ କରାଯାଇଥିବା ପଟ୍ଟା କିମ୍ବା ଲିଜ୍ ର ବିବରଣୀ: {EXISTING_PATTAS_LEASES_GRANTS}।\n"
                "ପୁନର୍ବାସ ବା ବିକଳ୍ପ ଜମି ନିମନ୍ତେ ଦାବି କରାଯାଇଥିବା ଜମି {REHABILITATION_LAND} ଅଟେ।\n"
                "ବିନା କୌଣସି କ୍ଷତିପୂରଣରେ ଯେଉଁ ଜମିରୁ ବିସ୍ଥାପିତ କରାଯାଇଥିଲା, ତାର ବିବରଣୀ: {DISPLACED_FROM_LAND}।\n"
                "ଆମର ଅନ୍ୟାନ୍ୟ ପାରମ୍ପରିକ ଅଧିକାର {OTHER_TRADITIONAL_RIGHT} ଅଟେ ଏବଂ ଅତିରିକ୍ତ ସୂଚନା {OTHER_INFORMATION} ସଂଲଗ୍ନ କରାଯାଇଛି।\n"
                "ଏହି ଦାବିର ସମର୍ଥନରେ ପ୍ରମାଣ ସ୍ୱରୂପ {EVIDENCE_ITEM} ଉପସ୍ଥାପନ କରାଯାଉଛି।"
            ),
            # Variation 2: Narrative / Descriptive Style (Simulating a Gram Sabha resolution narrative)
            (
                "ଗ୍ରାମ ସଭା ସମ୍ମୁଖରେ ଉପସ୍ଥାପିତ ବିସ୍ତୃତ ବିବରଣୀ ଏବଂ ଜଙ୍ଗଲ ଜମି ଉପରେ ଅଧିକାର ଦାବି।\n"
                "ମୁଁ, ଶ୍ରୀ/ଶ୍ରୀମତୀ {CLAIMANT_NAME} (ପିତା/ମାତା: {FATHER_MOTHER_NAME}, ସ୍ୱାମୀ/ସ୍ତ୍ରୀ: {SPOUSE_NAME}) ଏହି ବିବରଣୀ ଉପସ୍ଥାପନ କରୁଛି।\n"
                "ମୋର ସ୍ଥାୟୀ ବାସସ୍ଥାନର ସମ୍ପୂର୍ଣ୍ଣ ଠିକଣା ହେଉଛି {ADDRESS_FULL}। ମୁଁ {STATE} ରାଜ୍ୟର {DISTRICT} ଜିଲ୍ଲାର ନିବାସୀ ଅଟେ।\n"
                "ମୋର ଘର {TEHSIL_TALUKA} ତହସିଲ ଅନ୍ତର୍ଗତ {VILLAGE} ଗ୍ରାମରେ ଅବସ୍ଥିତ।\n"
                "ଏହି କ୍ଷେତ୍ର ସିଧାସଳଖ ଭାବରେ {GRAM_PANCHAYAT} ଗ୍ରାମ ପଞ୍ଚାୟତ ଏବଂ {GRAM_SABHA} ଗ୍ରାମ ସଭାର ପ୍ରଶାସନିକ ନିୟନ୍ତ୍ରଣରେ ଆସୁଛି।\n\n"

                "ଆମ ପରିବାର ପିଢ଼ି ପିଢ଼ି ଧରି ଜଙ୍ଗଲ ଉପରେ ନିର୍ଭରଶୀଳ ଏବଂ ଆମେ {CATEGORY_SCHEDULED_TRIBE} ଅଥବା {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} ସମ୍ପ୍ରଦାୟର ପାରମ୍ପରିକ ବନବାସୀ ଅଟୁ।\n"
                "ମୋ ପରିବାରରେ ସଦସ୍ୟ {FAMILY_MEMBER_NAME} (ବୟସ {FAMILY_MEMBER_AGE} ବର୍ଷ) ଏବଂ ମୋ ଉପରେ ସମ୍ପୂର୍ଣ୍ଣ ଆଶ୍ରିତ ଥିବା {DEPENDENT_NAME} ସାମିଲ ଅଛନ୍ତି।\n"
                "ଆମେ ବହୁ ପିଢ଼ି ଧରି ଯେଉଁ ସ୍ଥାନରେ ବସବାସ କରୁଛୁ, ସେହି ବାସସ୍ଥାନ ଜମିର ପରିମାଣ {LAND_EXTENT_HABITATION} ଅଟେ।\n"
                "ଆମ ଜୀବିକାର ମୁଖ୍ୟ ମାଧ୍ୟମ କୃଷି ଅଟେ ଏବଂ ଆମର ନିଜସ୍ୱ ଚାଷ ଜମିର ପରିମାଣ {LAND_EXTENT_SELF_CULTIVATION} ଅଟେ।\n"
                "ଏହା ବ୍ୟତୀତ, ଜଙ୍ଗଲ ଗ୍ରାମ ସୀମା ଭିତରେ ଆମର ଜମିର ପରିମାଣ {LAND_EXTENT_FOREST_VILLAGE} ମପାଯାଇଛି।\n\n"

                "ଏହି ଦାବି ସମ୍ବନ୍ଧରେ କିଛି ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ଆଇନଗତ ତଥ୍ୟ ଲିପିବଦ୍ଧ କରାଯାଉଛି।\n"
                "ଜମି ସହ ଜଡିତ କୌଣସି ବିବାଦର ସ୍ଥିତିକୁ {DISPUTED_LAND_DESCRIPTION} ରୂପେ ସ୍ପଷ୍ଟ କରାଯାଇଛି ଏବଂ ପୁରୁଣା ପଟ୍ଟାର ବିବରଣୀ {EXISTING_PATTAS_LEASES_GRANTS} ଅଟେ।\n"
                "ଆମକୁ ପୁନର୍ବାସ ପାଇଁ {REHABILITATION_LAND} ଜମିର ଆବଶ୍ୟକତା ଅଛି ଏବଂ ଅତୀତରେ ଆମକୁ ବିନା କ୍ଷତିପୂରଣରେ {DISPLACED_FROM_LAND} ରୁ ହଟାଯାଇଥିଲା।\n"
                "ଆମ ପୂର୍ବଜଙ୍କ ଦ୍ୱାରା ଉପଯୋଗ କରାଯାଉଥିବା ଅନ୍ୟାନ୍ୟ ପାରମ୍ପରିକ ଅଧିକାର {OTHER_TRADITIONAL_RIGHT} ଆଜି ମଧ୍ୟ ପ୍ରାସଙ୍ଗିକ।\n"
                "ଦାବିର ପ୍ରମାଣ ପାଇଁ ମଜବୁତ ସାକ୍ଷ୍ୟ {EVIDENCE_ITEM} ପ୍ରସ୍ତୁତ ଅଛି ଏବଂ ଅନ୍ୟାନ୍ୟ ସମ୍ବନ୍ଧିତ ତଥ୍ୟ {OTHER_INFORMATION} ବିଚାର ପାଇଁ ସଂଲଗ୍ନ କରାଯାଇଛି।"
            ),
            # Variation 3: Formal Letter Style (Simulating a petition to the Sub-Divisional Level Committee)
            (
                "ପ୍ରେରକ: {CLAIMANT_NAME}, ପିତା/ମାତା: {FATHER_MOTHER_NAME}, ସ୍ୱାମୀ/ସ୍ତ୍ରୀ: {SPOUSE_NAME}।\n"
                "ଠିକଣା: {ADDRESS_FULL}, ଗ୍ରାମ {VILLAGE}, ପଞ୍ଚାୟତ {GRAM_PANCHAYAT}, ଗ୍ରାମ ସଭା {GRAM_SABHA}।\n"
                "ତହସିଲ: {TEHSIL_TALUKA}, ଜିଲ୍ଲା: {DISTRICT}, ରାଜ୍ୟ: {STATE}।\n"
                "ବିଷୟ: ଜଙ୍ଗଲ ଅଧିକାର ଅଧିନିୟମ ୨୦୦୬ ଅନ୍ତର୍ଗତ ବ୍ୟକ୍ତିଗତ ଜଙ୍ଗଲ ଜମି ଅଧିକାର ପ୍ରଦାନ ନିମନ୍ତେ ଆବେଦନ।\n"
                "ମହାଶୟ, ଉପରୋକ୍ତ ବିଷୟରେ ସବିନୟ ନିବେଦନ ଏହିକି ଯେ, ମୁଁ ଦୀର୍ଘ ଦିନ ଧରି ଜଙ୍ଗଲ ଅଞ୍ଚଳରେ ବସବାସ କରୁଅଛି।\n\n"

                "ମୁଁ ପ୍ରମାଣିତ କରୁଛି ଯେ ମୁଁ {CATEGORY_SCHEDULED_TRIBE} କିମ୍ବା {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} ଶ୍ରେଣୀର ଯୋଗ୍ୟ ସଦସ୍ୟ ଅଟେ।\n"
                "ମୋ ପରିବାରରେ {FAMILY_MEMBER_NAME} (ବୟସ {FAMILY_MEMBER_AGE}) ଏବଂ ଆଶ୍ରିତ {DEPENDENT_NAME} ସାମିଲ ଅଛନ୍ତି, ଯେଉଁମାନଙ୍କର ଭରଣପୋଷଣ ଏହି ଜମିରୁ ହୋଇଥାଏ।\n"
                "ଜଙ୍ଗଲ କ୍ଷେତ୍ର ଭିତରେ ଆମ ଘର ଏବଂ ବାସସ୍ଥାନର ସମୁଦାୟ ପରିମାଣ {LAND_EXTENT_HABITATION} ଅଟେ।\n"
                "ଆମ ଦ୍ୱାରା ନିଜସ୍ୱ କୃଷି କାର୍ଯ୍ୟ ପାଇଁ ଉପଯୋଗ କରାଯାଉଥିବା ଜମିର ପରିମାଣ {LAND_EXTENT_SELF_CULTIVATION} ଅଟେ।\n"
                "ଜଙ୍ଗଲ ଗ୍ରାମଗୁଡ଼ିକରେ ଆମର ଜମିର ପରିମାଣ {LAND_EXTENT_FOREST_VILLAGE} ଭାବେ ରାଜସ୍ୱ ରେକର୍ଡରେ ଲିପିବଦ୍ଧ ହେବା ଉଚିତ।\n\n"

                "ଏହି ଜମି ସମ୍ବନ୍ଧରେ ବିବାଦୀୟ ସ୍ଥିତି ହେଉଛି {DISPUTED_LAND_DESCRIPTION}, ଯାହାର ସମାଧାନ ହେବା ଆବଶ୍ୟକ।\n"
                "ପୂର୍ବରୁ ପ୍ରଦାନ କରାଯାଇଥିବା ଲିଜ୍ ବା ପଟ୍ଟା {EXISTING_PATTAS_LEASES_GRANTS} ର ନକଲ ଯାଞ୍ଚ ପାଇଁ ସଂଲଗ୍ନ ଅଛି।\n"
                "ବିକଳ୍ପ ପୁନର୍ବାସ ଜମି {REHABILITATION_LAND} ଏବଂ କ୍ଷତିପୂରଣ ବିନା ବିସ୍ଥାପନ ଜମି {DISPLACED_FROM_LAND} ବିଷୟରେ ମଧ୍ୟ ଧ୍ୟାନ ଦିଆଯାଉ।\n"
                "ଆଇନ ଦ୍ୱାରା ସୁରକ୍ଷିତ ଆମର ଅନ୍ୟାନ୍ୟ ପାରମ୍ପରିକ ଅଧିକାର {OTHER_TRADITIONAL_RIGHT} ଆମକୁ ପ୍ରଦାନ କରାଯାଉ।\n"
                "ସାକ୍ଷ୍ୟ ସ୍ୱରୂପ {EVIDENCE_ITEM} ଏବଂ ଅତିରିକ୍ତ ବିବରଣୀ {OTHER_INFORMATION} ଆବେଦନ ସହିତ ସଂଲଗ୍ନ କରାଯାଇଛି।"
            ),
            # Variation 4: Legal / Statutory Declaration Style (Simulating a sworn affidavit)
            (
                "ଶପଥ ପତ୍ର ଏବଂ ବୈଧାନିକ ଦାବି ଘୋଷଣା (ଜଙ୍ଗଲ ଅଧିକାର ଅଧିନିୟମ ୨୦୦୬ ଅଧୀନରେ)।\n"
                "ମୁଁ, {CLAIMANT_NAME} (ପିତା/ମାତା: {FATHER_MOTHER_NAME}, ବୈଧ ସ୍ୱାମୀ/ସ୍ତ୍ରୀ: {SPOUSE_NAME}), ସତ୍ୟନିଷ୍ଠାର ସହ ନିମ୍ନଲିଖିତ ଘୋଷଣା କରୁଛି।\n"
                "ମୋର ଆଇନଗତ ଏବଂ ସ୍ଥାୟୀ ଠିକଣା {ADDRESS_FULL} ଭାବେ ସରକାରୀ ନଥିପତ୍ରରେ ପଞ୍ଜିକୃତ ହୋଇଛି।\n"
                "ଦାବିକୃତ ଜମି {STATE} ରାଜ୍ୟ, {DISTRICT} ଜିଲ୍ଲା ଏବଂ {TEHSIL_TALUKA} ତହସିଲର ଅଧିକାର କ୍ଷେତ୍ରରେ ଅବସ୍ଥିତ।\n"
                "ଏହି ଜମି ସମ୍ପୂର୍ଣ୍ଣ ଭାବେ {VILLAGE} ରାଜସ୍ୱ ଗ୍ରାମ, {GRAM_PANCHAYAT} ଗ୍ରାମ ପଞ୍ଚାୟତ ତଥା {GRAM_SABHA} ଗ୍ରାମ ସଭାର ବୈଧାନିକ ସୀମା ଅଧୀନରେ ଅଛି।\n\n"

                "ଧାରା ୩(୧)(କ) ଅନୁଯାୟୀ ଜମି ଦଖଲ ଏବଂ ସାମାଜିକ ଶ୍ରେଣୀର ବୈଧାନିକ ନିଶ୍ଚିତକରଣ।\n"
                "ମୁଁ ଶପଥ ପୂର୍ବକ କହୁଛି ଯେ ମୁଁ {CATEGORY_SCHEDULED_TRIBE} ଅଥବା {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} ର ବୈଧ ଶ୍ରେଣୀ ଅନ୍ତର୍ଭୁକ୍ତ ଅଟେ।\n"
                "ମୋର ଆଇନଗତ ଉତ୍ତରାଧିକାରୀ {FAMILY_MEMBER_NAME} (ବୟସ {FAMILY_MEMBER_AGE}) ଏବଂ ଆଶ୍ରିତ {DEPENDENT_NAME} ଏହି ଦାବିର ପ୍ରତ୍ୟକ୍ଷ ହିତାଧିକାରୀ ଅଟନ୍ତି।\n"
                "ଅଧିନିୟମର ପ୍ରାବଧାନ ଅନୁଯାୟୀ, ବାସସ୍ଥାନ ଉଦ୍ଦେଶ୍ୟରେ ଦଖଲ ଥିବା ଜମିର ମାପ {LAND_EXTENT_HABITATION} ନିର୍ଦ୍ଧାରଣ କରାଯାଇଛି।\n"
                "କୃଷି ଉପଯୋଗ ଅଥବା ସ୍ୱୟଂ ଚାଷ ପାଇଁ ଚାଷ କରାଯାଉଥିବା ଜମିର ପରିମାଣ {LAND_EXTENT_SELF_CULTIVATION} ମିଳିଅଛି।\n"
                "ଧାରା ୩(୧)(ଜ) ଅନୁସାରେ ଜଙ୍ଗଲ ଗ୍ରାମଗୁଡ଼ିକରେ ଅବସ୍ଥିତ ଜମିର ସୀମା ହେଉଛି {LAND_EXTENT_FOREST_VILLAGE}।\n\n"

                "ପ୍ରଲମ୍ବିତ ମାମଲା, ପଟ୍ଟା ଏବଂ ଅନ୍ୟାନ୍ୟ ବୈଧାନିକ ଅଧିକାରର ପ୍ରକଟିକରଣ।\n"
                "ଧାରା ୩(୧)(ଚ) ଅନ୍ତର୍ଗତ ଏହି ଜମି ଉପରେ ଯେକୌଣସି ପ୍ରକାରର ବିବାଦକୁ {DISPUTED_LAND_DESCRIPTION} ରୂପେ ଘୋଷଣା କରାଯାଉଛି।\n"
                "ବିଗତ ସରକାରଙ୍କ ଦ୍ୱାରା ଜାରି କରାଯାଇଥିବା ପଟ୍ଟା କିମ୍ବା ଅନୁଦାନର ବିବରଣୀ: {EXISTING_PATTAS_LEASES_GRANTS}।\n"
                "ଧାରା ୩(୧)(ଡ) ଅନୁଯାୟୀ ସ୍ୱସ୍ଥାନେ ପୁନର୍ବାସିତ ଜମି {REHABILITATION_LAND} ର ବିବରଣୀ ମଧ୍ୟ ଉପସ୍ଥାପିତ କରାଯାଇଛି।\n"
                "ଧାରା ୪(୮) ଅନୁଯାୟୀ ବିନା କୌଣସି ଉଚିତ କ୍ଷତିପୂରଣରେ ବେଦଖଲ କରାଯାଇଥିବା ଜମିର ବିବରଣୀ ହେଉଛି {DISPLACED_FROM_LAND}।\n"
                "ଧାରା ୩(୧)(ଠ) ଅନ୍ତର୍ଗତ ଅନ୍ୟାନ୍ୟ ପାରମ୍ପରିକ ଅଧିକାର {OTHER_TRADITIONAL_RIGHT} ଏବଂ ଆଇନଗତ ସାକ୍ଷ୍ୟ {EVIDENCE_ITEM} ସହିତ {OTHER_INFORMATION} ଏହି ସତ୍ୟପାଠର ଅବିଚ୍ଛେଦ୍ୟ ଅଙ୍ଗ ଅଟେ।"
            )
        ],

        DOC_CLAIM_COMMUNITY_RIGHTS: [
            # Variation 1: Bureaucratic / Form Style
            (
                "ଫର୍ମ - ଖ [ନିୟମ ୧୧(୧)(କ) ଏବଂ (୪) ଦେଖନ୍ତୁ]\n"
                "ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ଅଧିକାର ନିମନ୍ତେ ଯଥାବିଧି ଦାବି ଫର୍ମ ଏବଂ ଗ୍ରାମ ସଭାର ପ୍ରସ୍ତାବ।\n"
                "ଏହି ସାମୂହିକ ଆବେଦନ {VILLAGE} ଗ୍ରାମ ଏବଂ {GRAM_PANCHAYAT} ଗ୍ରାମ ପଞ୍ଚାୟତ ତରଫରୁ ଉପସ୍ଥାପନ କରାଯାଉଛି।\n"
                "ଏହା {STATE} ରାଜ୍ୟ, {DISTRICT} ଜିଲ୍ଲା, ଏବଂ {TEHSIL_TALUKA} ତହସିଲ ଅନ୍ତର୍ଗତ {GRAM_SABHA} ଗ୍ରାମ ସଭା ଦ୍ୱାରା ଯଥାବିଧି ଗୃହୀତ ହୋଇଛି।\n"
                "ଆମେ ସମସ୍ତେ ପାରମ୍ପରିକ ବନବାସୀ ଅଟୁ ଏବଂ {COMMUNITY_TYPE_FDST} କିମ୍ବା {COMMUNITY_TYPE_OTFD} ସମ୍ପ୍ରଦାୟର ପ୍ରତିନିଧିତ୍ୱ କରୁଛୁ।\n\n"

                "ସମ୍ପ୍ରଦାୟ ଦ୍ୱାରା ଉପଭୋଗ କରାଯାଉଥିବା ଜଙ୍ଗଲ ଅଧିକାରର ପ୍ରକୃତି ନିମ୍ନମତେ ଲିପିବଦ୍ଧ ଅଛି।\n"
                "ସାମୂହିକ ବ୍ୟବହାର ପାଇଁ ନିସ୍ତାର (Nistar) ଅଧିକାର: {COMMUNITY_RIGHT_NISTAR}।\n"
                "ଲଘୁ ବନଜାତ ଦ୍ରବ୍ୟ (MFP) ସଂଗ୍ରହ ଏବଂ ମାଲିକାନା ଅଧିକାର: {RIGHT_MINOR_FOREST_PRODUCE}।\n"
                "ମାଛ ଧରିବା, ଜଳ ଉତ୍ସ ଏବଂ ଅନ୍ୟାନ୍ୟ ସମ୍ପଦ ବ୍ୟବହାର କରିବାର ଅଧିକାର: {COMMUNITY_RIGHT_RESOURCE_USE}।\n"
                "ପଶୁ ଚରାଇବା ସମ୍ବନ୍ଧୀୟ ଗୋଚର ଅଧିକାର: {COMMUNITY_RIGHT_GRAZING}।\n"
                "ଯାଯାବର ଏବଂ ପଶୁପାଳକ ସମ୍ପ୍ରଦାୟ ପାଇଁ ପାରମ୍ପରିକ ସମ୍ପଦ ପ୍ରବେଶ ଅଧିକାର: {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS}।\n\n"

                "ବିଶେଷ ଭାବେ ଦୁର୍ବଳ ଜନଜାତି ଗୋଷ୍ଠୀ (PTG) ଏବଂ ପ୍ରାକ୍-କୃଷି ସମ୍ପ୍ରଦାୟଗୁଡ଼ିକ ପାଇଁ ବାସସ୍ଥାନ (Habitat) ଅଧିକାର {COMMUNITY_TENURE_HABITAT} ସୁନିଶ୍ଚିତ କରାଯାଉ।\n"
                "ଜୈବ ବିବିଧତା, ବୌଦ୍ଧିକ ସମ୍ପତ୍ତି ଏବଂ ପାରମ୍ପରିକ ଜ୍ଞାନର ଅଧିକାର {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} ଭାବରେ ସ୍ୱୀକୃତ ହେଉ।\n"
                "ଆଇନ ଦ୍ୱାରା ବ୍ୟାଖ୍ୟା କରାଯାଇଥିବା ଅନ୍ୟାନ୍ୟ ପାରମ୍ପରିକ ଅଧିକାର {OTHER_TRADITIONAL_RIGHT} ଆମ ଜୀବିକାର ମୂଳ ଆଧାର ଅଟେ।\n"
                "ଏହି ସାମୂହିକ ଦାବିଗୁଡ଼ିକୁ ପ୍ରମାଣିତ କରିବା ପାଇଁ ଉପସ୍ଥାପିତ ସାକ୍ଷ୍ୟ: {EVIDENCE_ITEM}।\n"
                "ପ୍ରଶାସନିକ ସମୀକ୍ଷା ନିମନ୍ତେ ଆବଶ୍ୟକ ଅତିରିକ୍ତ ସୂଚନା {OTHER_INFORMATION} ଏହି ଫର୍ମ ସହିତ ସଂଲଗ୍ନ କରାଯାଇଛି।"
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "ସାମୂହିକ ବନୀକରଣ ଏବଂ ପାରମ୍ପରିକ ଅଧିକାରର ସୁରକ୍ଷା ନିମନ୍ତେ ଗ୍ରାମ ସଭାର ସାମୂହିକ ଆବେଦନ।\n"
                "ଆମର {GRAM_SABHA} ଗ୍ରାମ ସଭା, {VILLAGE} ଗ୍ରାମର ସମସ୍ତ ବାସିନ୍ଦାଙ୍କ ପକ୍ଷରୁ ଏହି ଦାବି ଉପସ୍ଥାପନ କରୁଛି।\n"
                "ଆମର କ୍ଷେତ୍ର {STATE} ରାଜ୍ୟର {DISTRICT} ଜିଲ୍ଲାରେ ଅବସ୍ଥିତ {TEHSIL_TALUKA} ତହସିଲ ଏବଂ {GRAM_PANCHAYAT} ପଞ୍ଚାୟତ ଅନ୍ତର୍ଗତ।\n"
                "ଆମର ସମ୍ପ୍ରଦାୟ ସରକାରୀ ବର୍ଗୀକରଣ ଅନୁଯାୟୀ {COMMUNITY_TYPE_FDST} ଅଥବା {COMMUNITY_TYPE_OTFD} ଭାବରେ ସ୍ୱୀକୃତି ପ୍ରାପ୍ତ ଅଟେ।\n"
                "ଆମେ ପିଢ଼ି ପିଢ଼ି ଧରି ଜଙ୍ଗଲ ସହିତ ସହବସ୍ଥାନର ଜୀବନଶୈଳୀ ଅନୁସରଣ କରି ଆସୁଛୁ।\n\n"

                "ଦୈନନ୍ଦିନ ଜୀବନ ଏବଂ ଜୀବିକା ପାଇଁ ଆମେ ମୁଖ୍ୟତଃ ନିମ୍ନଲିଖିତ ଗୋଷ୍ଠୀ ଅଧିକାର ଉପରେ ନିର୍ଭର କରିଥାଉ।\n"
                "ଆମର ନିସ୍ତାର ଅଧିକାର ସ୍ପଷ୍ଟ ଭାବରେ {COMMUNITY_RIGHT_NISTAR} ରୂପେ ପ୍ରତିଷ୍ଠିତ ହୋଇଛି।\n"
                "ମହୁ, ଚେରମୂଳି ଭଳି ଲଘୁ ବନଜାତ ଦ୍ରବ୍ୟ ହାସଲ କରିବାର ଅଧିକାର ହେଉଛି {RIGHT_MINOR_FOREST_PRODUCE}।\n"
                "ସ୍ଥାନୀୟ ଜଳାଶୟର ବ୍ୟବହାର ଏବଂ ମାଛ ଧରିବାର ଅଧିକାର ହେଉଛି {COMMUNITY_RIGHT_RESOURCE_USE}।\n"
                "ଗୃହପାଳିତ ପଶୁମାନଙ୍କ ପାଇଁ ଚାରଣଭୂମି ଏବଂ ଗୋଚର ଅଧିକାର {COMMUNITY_RIGHT_GRAZING} ଅଧୀନରେ ସୁରକ୍ଷିତ ଅଛି।\n"
                "ଋତୁକାଳୀନ ପ୍ରବାସ କରୁଥିବା ଯାଯାବର ସମ୍ପ୍ରଦାୟର ସମ୍ପଦ ଅଧିକାର {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS} ଭାବରେ ପ୍ରଦାନ କରାଯାଇଛି।\n\n"

                "ଆଦିମ ଜନଜାତିଙ୍କ ପ୍ରାଚୀନ ବାସସ୍ଥାନ (Habitat) ସଂରକ୍ଷଣ କରିବାର ଅଧିକାର {COMMUNITY_TENURE_HABITAT} ଅତ୍ୟନ୍ତ ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ଅଟେ।\n"
                "ପାରମ୍ପରିକ ଜ୍ଞାନ ଏବଂ ସ୍ଥାନୀୟ ଜୈବ ବିବିଧତା ଉପରେ ଆମର ଅଧିକାର {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} ରୂପେ ଦାବି କରାଯାଇଛି।\n"
                "ଆମ ପୂର୍ବଜଙ୍କ ଦ୍ୱାରା ବ୍ୟବହୃତ ଅନ୍ୟାନ୍ୟ ପାରମ୍ପରିକ ଅଧିକାର {OTHER_TRADITIONAL_RIGHT} ଆଜି ମଧ୍ୟ ଜାରି ରହିଛି।\n"
                "ଏହି ଅଧିକାରଗୁଡ଼ିକର ପ୍ରାମାଣିକତା ପାଇଁ {EVIDENCE_ITEM} ଭଳି ଐତିହାସିକ ଦଲିଲ୍ ଉପସ୍ଥାପନ କରାଯାଇଛି।\n"
                "ବିସ୍ତୃତ ଆଲୋଚନା ନିମନ୍ତେ {OTHER_INFORMATION} ସମେତ ଅନ୍ୟାନ୍ୟ ତଥ୍ୟ ମଧ୍ୟ ସାଥିରେ ଦିଆଯାଇଛି।"
            ),
            # Variation 3: Formal Letter Style
            (
                "ବିଷୟ: ଜଙ୍ଗଲ ଅଧିକାର ଅଧିନିୟମ ୨୦୦୬ ଅନ୍ତର୍ଗତ ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ଅଧିକାରର ସ୍ୱୀକୃତି ନିମନ୍ତେ ସାମୂହିକ ସ୍ମାରକପତ୍ର।\n"
                "ଆମେ {STATE} ରାଜ୍ୟ, {DISTRICT} ଜିଲ୍ଲା ଏବଂ {TEHSIL_TALUKA} ତହସିଲର ଅଧିବାସୀ ଅଟୁ।\n"
                "ଆମର ବାସସ୍ଥାନ {VILLAGE} ଗ୍ରାମ ଏବଂ {GRAM_PANCHAYAT} ପଞ୍ଚାୟତର ଅଧିକାର କ୍ଷେତ୍ରରେ ଆସୁଛି।\n"
                "ଏହି ପତ୍ର {GRAM_SABHA} ଗ୍ରାମ ସଭାର ସର୍ବସମ୍ମତି ଏବଂ ପୂର୍ଣ୍ଣ ସହମତି ସହିତ ଲେଖାଯାଉଛି।\n"
                "ଆମେ ଆଦିବାସୀ ଏବଂ ପାରମ୍ପରିକ ବନବାସୀ ଅଟୁ ଯେଉଁମାନେ {COMMUNITY_TYPE_FDST} ଏବଂ {COMMUNITY_TYPE_OTFD} ସମ୍ପ୍ରଦାୟ ସହ ଜଡିତ ଅଛୁ।\n\n"

                "ଅଧିନିୟମର ବ୍ୟବସ୍ଥା ଅନୁଯାୟୀ, ଆମେ ନିମ୍ନଲିଖିତ ଗୋଷ୍ଠୀ ଅଧିକାର ଦାବି କରୁଛୁ:\n"
                "ନିସ୍ତାର ଏବଂ ସାଧାରଣ ବ୍ୟବହାରର ଅଧିକାର: {COMMUNITY_RIGHT_NISTAR}। ଲଘୁ ବନଜାତ ଦ୍ରବ୍ୟର ଅଧିକାର: {RIGHT_MINOR_FOREST_PRODUCE}।\n"
                "ପୋଖରୀ ଏବଂ ଜଳ ସମ୍ପଦ ବ୍ୟବହାର କରିବାର ଅଧିକାର: {COMMUNITY_RIGHT_RESOURCE_USE}।\n"
                "ପଶୁ ଚରାଇବାର ସାମୂହିକ ଅଧିକାର: {COMMUNITY_RIGHT_GRAZING}।\n"
                "ଯାଯାବର ସମ୍ପ୍ରଦାୟ ପାଇଁ ଚାରଣଭୂମିରେ ପ୍ରବେଶ ଅଧିକାର: {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS}।\n\n"

                "ଆମର ପାରମ୍ପରିକ ବାସସ୍ଥାନର ପଟ୍ଟା {COMMUNITY_TENURE_HABITAT} ରୂପେ ଆମକୁ ହସ୍ତାନ୍ତର କରାଯିବା ଉଚିତ।\n"
                "ଆମର ଜ୍ଞାନ ଏବଂ ଜୈବ ବିବିଧତା ଉପରେ ବୌଦ୍ଧିକ ଅଧିକାର {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} ସୁନିଶ୍ଚିତ କରାଯାଉ।\n"
                "ଅନ୍ୟ ସମସ୍ତ ପାରମ୍ପରିକ ଅଧିକାର {OTHER_TRADITIONAL_RIGHT} ଯାହା ଆମ ଜୀବନ ସହ ଜଡ଼ିତ, ତାହା ମଧ୍ୟ ବୈଧ ହେଉ।\n"
                "ଏହି ଦାବିର ସମର୍ଥନରେ ଦୃଢ଼ ସାକ୍ଷ୍ୟ ସ୍ୱରୂପ {EVIDENCE_ITEM} ସଂଲଗ୍ନ କରାଯାଇଛି।\n"
                "ଅତିରିକ୍ତ ସୂଚନା {OTHER_INFORMATION} ପ୍ରଶାସନର ଦୃଷ୍ଟିଗୋଚର କରାଯାଉଛି।"
            ),
            # Variation 4: Legal / Statutory Declaration Style
            (
                "ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ଅଧିକାର (Community Forest Rights) ର ବୈଧାନିକ ଦାବି ଏବଂ ଘୋଷଣାପତ୍ର।\n"
                "ଏହି ଘୋଷଣା {STATE} ରାଜ୍ୟ, {DISTRICT} ଜିଲ୍ଲା ଏବଂ {TEHSIL_TALUKA} ତହସିଲର ସମ୍ପୃକ୍ତ ଅଧିକାରୀଙ୍କ ସମ୍ମୁଖରେ ଉପସ୍ଥାପନ କରାଯାଉଛି।\n"
                "ଏହି ଦାବି {VILLAGE} ଗ୍ରାମବାସୀଙ୍କ ତରଫରୁ, {GRAM_PANCHAYAT} ଗ୍ରାମ ପଞ୍ଚାୟତ ଏବଂ {GRAM_SABHA} ଗ୍ରାମ ସଭାର ବୈଧାନିକ ପ୍ରସ୍ତାବ ଦ୍ୱାରା ପାରିତ ହୋଇଛି।\n"
                "ଜଙ୍ଗଲ ଅଧିକାର ଅଧିନିୟମ ୨୦୦୬ ଅଧୀନରେ ଏହି ସମ୍ପ୍ରଦାୟକୁ {COMMUNITY_TYPE_FDST} କିମ୍ବା {COMMUNITY_TYPE_OTFD} ରୂପେ ଆଇନଗତ ସ୍ୱୀକୃତି ମିଳିଛି।\n"
                "ଏହି ସମ୍ପ୍ରଦାୟର ସାମୂହିକ ଅଧିକାରକୁ ଆଇନଗତ ଭାବେ ପୁନଃସ୍ଥାପନ କରିବା ପାଇଁ ଏହି ଦଲିଲ ପ୍ରସ୍ତୁତ କରାଯାଇଛି।\n\n"

                "ଧାରା ୩ ଅଧୀନରେ ପରିଭାଷିତ ସାମୂହିକ ବ୍ୟବହାର ଏବଂ ସମ୍ପଦ ଉପରେ ଅଧିକାରର ତାଲିକା।\n"
                "ଧାରା ୩(୧)(ଖ) ଅନ୍ତର୍ଗତ ନିସ୍ତାର (Nistar) ର ବୈଧାନିକ ଅଧିକାର {COMMUNITY_RIGHT_NISTAR} ଭାବେ ଘୋଷଣା କରାଯାଇଛି।\n"
                "ଧାରା ୩(୧)(ଗ) ଅନ୍ତର୍ଗତ ଲଘୁ ବନଜାତ ଦ୍ରବ୍ୟ (MFP) ଉପରେ ମାଲିକାନା ଅଧିକାର {RIGHT_MINOR_FOREST_PRODUCE} ରୂପେ ବୈଧ ଅଟେ।\n"
                "ଜଳାଶୟ ଏବଂ ମତ୍ସ୍ୟ ପାଳନର ବ୍ୟବହାର କରିବାର ଆଇନଗତ ଅଧିକାର {COMMUNITY_RIGHT_RESOURCE_USE} ନିର୍ଦ୍ଧାରିତ ଅଛି।\n"
                "ପାରମ୍ପରିକ ଗୋଚର ଅଧିକାର {COMMUNITY_RIGHT_GRAZING} ରୂପେ ଆନୁଷ୍ଠାନିକ ଭାବରେ ଲିପିବଦ୍ଧ ଅଛି।\n"
                "ଯାଯାବର ସମ୍ପ୍ରଦାୟର ସମ୍ପଦ ପ୍ରତି ବୈଧାନିକ ପ୍ରବେଶ ଅଧିକାର {COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS} ସୁନିଶ୍ଚିତ କରାଯାଇଛି।\n\n"

                "ଜନଜାତି ବାସସ୍ଥାନ ଅଧିକାର, ବୌଦ୍ଧିକ ସମ୍ପତ୍ତି ଏବଂ ଉପସ୍ଥାପିତ ବୈଧାନିକ ସାକ୍ଷ୍ୟ।\n"
                "ପିଟିଜି (PTG) ଏବଂ ପ୍ରାକ୍-କୃଷି ସମ୍ପ୍ରଦାୟ ପାଇଁ ବାସସ୍ଥାନ (Habitat) ର ଆଇନଗତ ଅଧିକାର {COMMUNITY_TENURE_HABITAT} ଦାବି କରାଯାଉଛି।\n"
                "ଧାରା ୩(୧)(ଟ) ଅନୁଯାୟୀ ଜୈବ ବିବିଧତା ଏବଂ ପାରମ୍ପରିକ ଜ୍ଞାନ ପାଇଁ ପ୍ରବେଶ ଅଧିକାର {COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK} ପଞ୍ଜିକୃତ ଅଛି।\n"
                "ଆଇନ ଦ୍ୱାରା ପ୍ରଦତ୍ତ ଅନ୍ୟ ସମସ୍ତ ପାରମ୍ପରିକ ଅଧିକାର {OTHER_TRADITIONAL_RIGHT} ଆମର ସାମୂହିକ ଐତିହ୍ୟ ଅଟେ।\n"
                "ଉପରୋକ୍ତ ବୈଧାନିକ ଦାବିଗୁଡ଼ିକୁ ପ୍ରମାଣିତ କରିବା ପାଇଁ ଦସ୍ତାବେଜୀୟ ସାକ୍ଷ୍ୟ {EVIDENCE_ITEM} ସଂଲଗ୍ନ କରାଯାଇଛି।\n"
                "ବିଧିଗତ ଯାଞ୍ଚ ଉଦ୍ଦେଶ୍ୟରେ ଅନ୍ୟାନ୍ୟ ତଥ୍ୟ {OTHER_INFORMATION} ଆନୁଷ୍ଠାନିକ ଭାବରେ ଉପସ୍ଥାପନ କରାଯାଉଛି।"
            )
        ],

        DOC_CLAIM_COMMUNITY_FOREST_RESOURCE: [
            # Variation 1: Bureaucratic / Form Style
            (
                "ଫର୍ମ - ଗ [ଅଧିନିୟମର ଧାରା ୩(୧)(ଝ) ଏବଂ ନିୟମ ୧୧(୧) ଦେଖନ୍ତୁ]\n"
                "ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦ (CFR) ଅଧିକାର ନିମନ୍ତେ ଦାବି ଫର୍ମ।\n"
                "ଏହି ଦାବି {STATE} ରାଜ୍ୟ, {DISTRICT} ଜିଲ୍ଲା, ଏବଂ {TEHSIL_TALUKA} ତହସିଲର କ୍ଷେତ୍ରାଧିକାର ଅନ୍ତର୍ଗତ ଅଟେ।\n"
                "ଏହା {GRAM_PANCHAYAT} ଗ୍ରାମ ପଞ୍ଚାୟତ ଅଧୀନସ୍ଥ {VILLAGE} ଗ୍ରାମବାସୀଙ୍କ ପକ୍ଷରୁ ଉପସ୍ଥାପନ କରାଯାଉଛି।\n"
                "ଏହି ପ୍ରସ୍ତାବ {GRAM_SABHA} ଗ୍ରାମ ସଭାର ଯଥାବିଧି ବୈଠକରେ ସର୍ବସମ୍ମତି କ୍ରମେ ପାରିତ ହୋଇଛି।\n\n"

                "ଏହି ଦାବିକୁ ଉପସ୍ଥାପନ କରୁଥିବା ଗ୍ରାମ ସଭାର ପ୍ରମୁଖ ସଦସ୍ୟ ହେଉଛନ୍ତି {GRAM_SABHA_MEMBER_NAME}।\n"
                "ଏହି ସଦସ୍ୟମାନେ ବୈଧାନିକ ରୂପେ {CATEGORY_SCHEDULED_TRIBE} କିମ୍ବା {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} ସମ୍ପ୍ରଦାୟ ସହ ଜଡିତ ଅଟନ୍ତି।\n"
                "ଆମେ ଯେଉଁ ଜଙ୍ଗଲ ସମ୍ପଦ ଅଞ୍ଚଳ ଉପରେ ଦାବି କରୁଛୁ ତାହାର ଖସଡା/କମ୍ପାର୍ଟମେଣ୍ଟ ନମ୍ବର ହେଉଛି {KHASRA_COMPARTMENT_NUMBER}।\n"
                "ଆମ ଜଙ୍ଗଲ ସୀମାକୁ ଲାଗି ରହିଥିବା ସୀମାବର୍ତ୍ତୀ ଗ୍ରାମଗୁଡ଼ିକ ହେଉଛି {BORDERING_VILLAGE}।\n"
                "ଏହି କ୍ଷେତ୍ରର ଭୌଗୋଳିକ ସୀମା {BOUNDARY_DESCRIPTION} ରୂପେ ସ୍ପଷ୍ଟ ଭାବରେ ବ୍ୟାଖ୍ୟା କରାଯାଇଛି।\n\n"

                "ଏହି ଭୂଭାଗକୁ ଆମ ସମ୍ପ୍ରଦାୟ ପିଢ଼ି ପିଢ଼ି ଧରି ସଂରକ୍ଷଣ ଏବଂ ପରିଚାଳନା କରିଆସୁଛି।\n"
                "ଏଥିପାଇଁ ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦ ସାକ୍ଷ୍ୟର ଯଥାବିଧି ତାଲିକା {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} ସଂଲଗ୍ନ କରାଯାଇଛି।\n"
                "ଆମର ପାରମ୍ପରିକ ଉପଯୋଗକୁ ପ୍ରମାଣିତ କରୁଥିବା ଅନ୍ୟାନ୍ୟ ସାକ୍ଷ୍ୟ {EVIDENCE_ITEM} ରୂପେ ଉପସ୍ଥାପିତ କରାଯାଇଛି।\n"
                "ଆମେ ନିଶ୍ଚିତ କରୁଛୁ ଯେ ଏହି ଜଙ୍ଗଲ ସମ୍ପଦର ସ୍ଥାୟୀ ବ୍ୟବହାର କରିବାର ଅଧିକାର ଗ୍ରାମ ସଭାରେ ନିହିତ ଅଛି।\n"
                "ସକ୍ଷମ ପ୍ରାଧିକାରୀଙ୍କୁ ଅନୁରୋଧ ଯେ ସେମାନେ ଏହାର ତଦନ୍ତ କରି ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦ ଅଧିକାରକୁ ସ୍ୱୀକୃତି ପ୍ରଦାନ କରନ୍ତୁ।"
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦର ପରିଚାଳନା ଏବଂ ସଂରକ୍ଷଣ ନିମନ୍ତେ ଗ୍ରାମ ସଭାର ସାମୂହିକ ଘୋଷଣାପତ୍ର।\n"
                "ଆମେ, {STATE} ରାଜ୍ୟର {DISTRICT} ଜିଲ୍ଲାରେ ଅବସ୍ଥିତ {TEHSIL_TALUKA} ତହସିଲର ଅଧିବାସୀ ଅଟୁ।\n"
                "ଆମର {VILLAGE} ଗ୍ରାମ, {GRAM_PANCHAYAT} ଗ୍ରାମ ପଞ୍ଚାୟତର ପ୍ରଶାସନିକ ଢାଞ୍ଚା ଅନ୍ତର୍ଗତ ଅଟେ।\n"
                "ଆଜି {GRAM_SABHA} ଗ୍ରାମ ସଭାରେ ଏକତ୍ରିତ ହୋଇ, ଆମେ ଆମର ପାରମ୍ପରିକ ଜଙ୍ଗଲ ସମ୍ପଦ ଅଧିକାରର ଘୋଷଣା କରୁଛୁ।\n"
                "ଏହି ସଭାର ନେତୃତ୍ୱ ନେଉଥିବା ପ୍ରମୁଖ ସଦସ୍ୟ ହେଉଛନ୍ତି {GRAM_SABHA_MEMBER_NAME}।\n\n"

                "ଆମେ ସମସ୍ତେ ପାରମ୍ପରିକ ବନବାସୀ ଅଟୁ ଯେଉଁମାନେ {CATEGORY_SCHEDULED_TRIBE} କିମ୍ବା {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} ସମ୍ପ୍ରଦାୟରୁ ଆସିଛୁ।\n"
                "ଆମେ ଯେଉଁ ଜଙ୍ଗଲ ଅଞ୍ଚଳର ପରିଚାଳନା କରୁଛୁ, ତାର ଖସଡା/କମ୍ପାର୍ଟମେଣ୍ଟ ନମ୍ବର {KHASRA_COMPARTMENT_NUMBER} ଭୂ-ଅଭିଲେଖରେ ଲିପିବଦ୍ଧ ଅଛି।\n"
                "ଆମ ଜଙ୍ଗଲ କ୍ଷେତ୍ରର ଚାରିପଟେ ଥିବା ପଡୋଶୀ ଗ୍ରାମଗୁଡ଼ିକ {BORDERING_VILLAGE} ଭାବରେ ଜଣାଶୁଣା।\n"
                "ଉତ୍ତରରେ ନଦୀ ଏବଂ ଦକ୍ଷିଣରେ ପାହାଡ଼ ପର୍ଯ୍ୟନ୍ତ ବିସ୍ତୃତ ଆମ ସୀମାର ବିବରଣୀ ହେଉଛି {BOUNDARY_DESCRIPTION}।\n"
                "ଏହି ସୀମା ଭିତରେ ଉପଲବ୍ଧ ସମସ୍ତ ସମ୍ପଦର ସଂରକ୍ଷଣ କରିବାର ସମ୍ପୂର୍ଣ୍ଣ ଅଧିକାର ଆମ ପାଖରେ ଅଛି।\n\n"

                "ଜୈବ ବିବିଧତା ବଜାୟ ରଖିବା ପାଇଁ ଏବଂ ଜଙ୍ଗଲକୁ କଟାଯିବାରୁ ରକ୍ଷା କରିବା ପାଇଁ ଆମେ ଦୃଢ଼ ସଂକଳ୍ପବଦ୍ଧ ଅଟୁ।\n"
                "ନିଜ ଦାବିକୁ ମଜବୁତ କରିବା ପାଇଁ ଆମେ ସାକ୍ଷ୍ୟଗୁଡ଼ିକର ଏକ ତାଲିକା {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} ପ୍ରସ୍ତୁତ କରିଛୁ।\n"
                "ମୌଖିକ ଇତିହାସ ଏବଂ ଐତିହାସିକ ଦଲିଲଗୁଡ଼ିକୁ {EVIDENCE_ITEM} ଭାବରେ ଉପସ୍ଥାପନ କରାଯାଇଛି।\n"
                "ଏହି ପ୍ରମାଣଗୁଡ଼ିକ ଆଧାରରେ, ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦ ଅଧିକାର (CFR) ଆମକୁ ତୁରନ୍ତ ପ୍ରଦାନ କରାଯିବା ଉଚିତ।\n"
                "ଆମେ ସରକାରୀ ଅଧିକାରୀମାନଙ୍କୁ ଅନୁରୋଧ କରୁଛୁ ଯେ ସେମାନେ ଏହା ଉପରେ ଶୀଘ୍ର ବିଚାର କରି ଆଦେଶ ଜାରି କରନ୍ତୁ।"
            ),
            # Variation 3: Formal Letter Style
            (
                "ବିଷୟ: ଧାରା ୩(୧)(ଝ) ଅନ୍ତର୍ଗତ ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦ (CFR) ଉପରେ ଅଧିକାରର ଦାବି।\n"
                "କ୍ଷେତ୍ରର ବିବରଣୀ: ତହସିଲ {TEHSIL_TALUKA}, ଜିଲ୍ଲା {DISTRICT}, ରାଜ୍ୟ {STATE}।\n"
                "ଗ୍ରାମ: {VILLAGE}, ପଞ୍ଚାୟତ: {GRAM_PANCHAYAT}, ଗ୍ରାମ ସଭା: {GRAM_SABHA}।\n"
                "ଏହି ଦାବି ଗ୍ରାମ ସଭା ସଦସ୍ୟ {GRAM_SABHA_MEMBER_NAME} ଙ୍କ ନେତୃତ୍ୱରେ ପ୍ରଶାସନ ସମ୍ମୁଖରେ ଉପସ୍ଥାପନ କରାଯାଉଛି।\n"
                "ଆବେଦନକାରୀମାନେ ମୁଖ୍ୟତଃ {CATEGORY_SCHEDULED_TRIBE} ଏବଂ {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} ବର୍ଗ ସହ ଜଡିତ ଅଟନ୍ତି।\n\n"

                "ଆମ ଦ୍ୱାରା ସଂରକ୍ଷିତ ଜଙ୍ଗଲ ଅଞ୍ଚଳର ଖସଡା କିମ୍ବା କମ୍ପାର୍ଟମେଣ୍ଟ ନମ୍ବର ହେଉଛି {KHASRA_COMPARTMENT_NUMBER}।\n"
                "ଆମ ସୀମାକୁ ଲାଗି ରହିଥିବା ସୀମାବର୍ତ୍ତୀ ଗ୍ରାମ ଯେପରିକି {BORDERING_VILLAGE} ଏହି ଜଙ୍ଗଲକୁ ଭାଗ କରନ୍ତି ନାହିଁ।\n"
                "ଆମ ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦର ଭୌଗୋଳିକ ସୀମା {BOUNDARY_DESCRIPTION} ଅନୁଯାୟୀ ମାନଚିତ୍ରରେ ଚିହ୍ନିତ ହୋଇଛି।\n"
                "ଏହି କ୍ଷେତ୍ରର ପାରିସ୍ଥିତିକ ସନ୍ତୁଳନ ବଜାୟ ରଖିବା ଆମ ସମ୍ପ୍ରଦାୟର ପ୍ରାଥମିକ କର୍ତ୍ତବ୍ୟ ରହିଆସିଛି।\n"
                "ଅତଏବ, ଏହି ଜଙ୍ଗଲ ସମ୍ପଦଗୁଡ଼ିକର ପରିଚାଳନାର ସମ୍ପୂର୍ଣ୍ଣ ଅଧିକାର ଆମ ଗ୍ରାମ ସଭାକୁ ଦିଆଯିବା ଉଚିତ।\n\n"

                "ଏହି ଜମି ସହିତ ଆମର ପାରମ୍ପରିକ ସମ୍ପର୍କକୁ ପ୍ରମାଣିତ କରୁଥିବା ସାକ୍ଷ୍ୟ ସଂକଳନ କରାଯାଇଛି।\n"
                "ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ଦଲିଲଗୁଡ଼ିକର ତାଲିକା {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} ଆନୁଷ୍ଠାନିକ ଭାବରେ ଜମା କରାଯାଉଛି।\n"
                "ଅନ୍ୟାନ୍ୟ ଦୃଢ଼ ପ୍ରମାଣ ସ୍ୱରୂପ {EVIDENCE_ITEM} ଦଲିଲ ମଧ୍ୟ ଏହି ଆବେଦନ ସହିତ ଯୋଡାଯାଇଛି।\n"
                "ଏହି ସମସ୍ତ ସାକ୍ଷ୍ୟ ଆମ ଦାବିର ବୈଧତା ଏବଂ ନ୍ୟାୟସଙ୍ଗତତାକୁ ସମ୍ପୂର୍ଣ୍ଣ ରୂପେ ପ୍ରମାଣିତ କରୁଛି।\n"
                "ଏହା ଆଧାରରେ ଆମ ଗ୍ରାମ ସଭାର ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦ ଅଧିକାରକୁ ସରକାରୀ ସ୍ୱୀକୃତି ମିଳିବା ଉଚିତ।"
            ),
            # Variation 4: Legal / Statutory Declaration Style
            (
                "ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦ (Community Forest Resource) ଦାବିଗୁଡ଼ିକର ବୈଧାନିକ ପ୍ରକଟିକରଣ ଦଲିଲ।\n"
                "ଜଙ୍ଗଲ ଅଧିକାର ଅଧିନିୟମ ୨୦୦୬, ଧାରା ୩(୧)(ଝ) ଅନ୍ତର୍ଗତ, {STATE} ରାଜ୍ୟ, {DISTRICT} ଜିଲ୍ଲା, {TEHSIL_TALUKA} ତହସିଲର ପ୍ରାଧିକାରୀମାନଙ୍କୁ ଉପସ୍ଥାପିତ ବୈଧାନିକ ଦାବି।\n"
                "ଏହି ଆନୁଷ୍ଠାନିକ ଦାବି {VILLAGE} ଗ୍ରାମବାସୀଙ୍କ ପକ୍ଷରୁ, {GRAM_PANCHAYAT} ଗ୍ରାମ ପଞ୍ଚାୟତ ଏବଂ {GRAM_SABHA} ଗ୍ରାମ ସଭା ମାଧ୍ୟମରେ ଉପସ୍ଥାପିତ କରାଯାଉଛି।\n"
                "ଗ୍ରାମ ସଭାର ଅଧିକୃତ ଆଇନଗତ ପ୍ରତିନିଧି {GRAM_SABHA_MEMBER_NAME} ଏହି ଦଲିଲରେ ସ୍ୱାକ୍ଷର କରୁଛନ୍ତି।\n"
                "ଏହି ଦାବିରେ ସାମିଲ ଥିବା ସଦସ୍ୟମାନେ {CATEGORY_SCHEDULED_TRIBE} କିମ୍ବା {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} ନାମକ ବିଧିକ ଶ୍ରେଣୀ ଦ୍ୱାରା ସୁରକ୍ଷିତ ଅଟନ୍ତି।\n\n"

                "ଦାବିକୃତ ଜଙ୍ଗଲ ସମ୍ପଦ କ୍ଷେତ୍ରର ଭୌଗୋଳିକ, ଜମି ମାପ ଏବଂ ସୀମା ସମ୍ବନ୍ଧୀୟ ବୈଧାନିକ ପ୍ରବିଷ୍ଟି।\n"
                "ଦାବି ଅଧୀନସ୍ଥ ଜଙ୍ଗଲ ଅଞ୍ଚଳର ବୈଧାନିକ ଖସଡା (Khasra) କିମ୍ବା ଜଙ୍ଗଲ ବିଭାଗ କମ୍ପାର୍ଟମେଣ୍ଟ ନମ୍ବର {KHASRA_COMPARTMENT_NUMBER} ରାଜସ୍ୱ ଅଭିଲେଖରେ ଲିପିବଦ୍ଧ ଅଛି।\n"
                "ରାଜସ୍ୱ ମାନଚିତ୍ର ଅନୁଯାୟୀ, ଏହି କ୍ଷେତ୍ର ସହିତ ସୀମା ଭାଗ କରୁଥିବା ପଡୋଶୀ ଗ୍ରାମଗୁଡ଼ିକ ହେଉଛି {BORDERING_VILLAGE}।\n"
                "ସମ୍ପୂର୍ଣ୍ଣ ଦାବିକୃତ ଜଙ୍ଗଲ ସମ୍ପଦ ଅଞ୍ଚଳର ଭୌଗୋଳିକ ଏବଂ ସ୍ଥଳାକୃତିକ ସୀମାଗୁଡ଼ିକ {BOUNDARY_DESCRIPTION} ରୂପେ ଅତ୍ୟନ୍ତ ସ୍ପଷ୍ଟ ଭାବରେ ପରିଭାଷିତ କରାଯାଇଛି।\n"
                "ଏହି ସୀମାଗୁଡ଼ିକ ଭିତରେ ଥିବା ଜଙ୍ଗଲ ସମ୍ପଦର ସ୍ଥାୟୀ ଉପଯୋଗ ଏବଂ ପରିଚାଳନା କରିବାର ପାରମ୍ପରିକ ବୈଧାନିକ ଅଧିକାର ଏହି ସମ୍ପ୍ରଦାୟ ପାଖରେ ଅଛି।\n"
                "ଏହି କ୍ଷେତ୍ରରେ ବନ ସମ୍ପଦର ପୁନରୁତ୍ପାଦନର ଦାୟିତ୍ୱ ଏବଂ ଅଧିକାର ଆଇନଗତ ଭାବେ ଗ୍ରାମ ସଭାକୁ ଦିଆଯିବା ଉଚିତ।\n\n"

                "ପ୍ରାମାଣିକ ସାକ୍ଷ୍ୟଗୁଡ଼ିକର ଉପସ୍ଥାପନ ଏବଂ ବିଧିକ ଦାବିଗୁଡ଼ିକର ପୁଷ୍ଟି।\n"
                "ଏହି ସମ୍ପ୍ରଦାୟର ପାରମ୍ପରିକ ସମ୍ପର୍କକୁ ପ୍ରମାଣିତ କରିବା ପାଇଁ, ସାକ୍ଷ୍ୟଗୁଡ଼ିକର ଆନୁଷ୍ଠାନିକ ତାଲିକା {COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST} ସଂଲଗ୍ନ କରାଯାଇଛି।\n"
                "ସାଥିରେ, ଗ୍ରାମ୍ୟ ରେକର୍ଡ ଏବଂ ଐତିହାସିକ ଦଲିଲ ଭଳି ଅତିରିକ୍ତ ପ୍ରମାଣିତ ସାକ୍ଷ୍ୟ {EVIDENCE_ITEM} ରୂପେ ଉପସ୍ଥାପନ କରାଯାଇଛି।\n"
                "ଏହି ସମସ୍ତ ଦଲିଲ ଅଧିନିୟମର ନିୟମ ୧୩ ଅନ୍ତର୍ଗତ ବିଧିକ ସାକ୍ଷ୍ୟ ଭାବରେ ଗ୍ରହଣଯୋଗ୍ୟ ଏବଂ ମାନ୍ୟ ଅଟେ।\n"
                "ଏହି ପ୍ରମାଣଗୁଡ଼ିକ ଆଧାରରେ, ସମ୍ପୂର୍ଣ୍ଣ କ୍ଷେତ୍ରର ସଂରକ୍ଷଣ ଏବଂ ବିକାଶର ବୈଧାନିକ ଅଧିକାର ଗ୍ରାମ ସଭାକୁ ପ୍ରଦାନ କରାଯିବା ଅନିବାର୍ଯ୍ୟ ଅଟେ।\n"
                "ଆଇନଗତ ବ୍ୟବସ୍ଥା ଅନୁଯାୟୀ ଏହି ଦାବି ଉପରେ ଶୀଘ୍ର ସମୀକ୍ଷା କରି ଗେଜେଟ୍ ଆଦେଶ ଜାରି କରିବାକୁ ଅନୁରୋଧ କରାଯାଉଛି।"
            )
        ],

        DOC_TITLE_UNDER_OCCUPATION: [
            # Variation 1: Bureaucratic / Form Style
            (
                "ପରିଶିଷ୍ଟ - II [ନିୟମ ୮(ଜ) ଦେଖନ୍ତୁ]\n"
                "ଦଖଲ ଅଧୀନରେ ଥିବା ଜଙ୍ଗଲ ଜମି ପାଇଁ ଆନୁଷ୍ଠାନିକ ଅଧିକାର ପତ୍ର / ପଟ୍ଟା।\n"
                "ଜଙ୍ଗଲ ଜମିର ଏହି ଅଧିକାର ପତ୍ର {TITLE_HOLDER_NAME} ଙ୍କୁ ରାଜ୍ୟ ସରକାରଙ୍କ ଦ୍ୱାରା ପ୍ରଦାନ କରାଯାଉଛି।\n"
                "ପଟ୍ଟାଧାରୀଙ୍କ ପିତା/ମାତାଙ୍କ ନାମ {FATHER_MOTHER_NAME} ତଥା ସ୍ୱାମୀ/ସ୍ତ୍ରୀଙ୍କ ନାମ {SPOUSE_NAME} ଅଟେ।\n"
                "ଏମାନଙ୍କ ଉପରେ ଆଶ୍ରିତ ବ୍ୟକ୍ତି {DEPENDENT_NAME} ମଧ୍ୟ ଏହି ଅଧିକାର ପତ୍ରର ସଂରକ୍ଷଣ ଅନ୍ତର୍ଗତ ଆସୁଛନ୍ତି।\n\n"

                "ପଟ୍ଟାଧାରୀଙ୍କ ସମ୍ପୂର୍ଣ୍ଣ ପଞ୍ଜିକୃତ ଠିକଣା ହେଉଛି {TITLE_ADDRESS_FULL}।\n"
                "ଏହି ଜଙ୍ଗଲ ଜମି {VILLAGE} ଗ୍ରାମ ଏବଂ {GRAM_PANCHAYAT} ଗ୍ରାମ ପଞ୍ଚାୟତର ଭୌଗୋଳିକ କ୍ଷେତ୍ରରେ ଅବସ୍ଥିତ।\n"
                "ଏହା {GRAM_SABHA} ଗ୍ରାମ ସଭାର କ୍ଷେତ୍ରାଧିକାରରେ, {TEHSIL_TALUKA} ତହସିଲ ଅନ୍ତର୍ଗତ ଆସୁଛି।\n"
                "ଏହା ଜିଲ୍ଲା {DISTRICT} ଏବଂ ରାଜ୍ୟ {STATE} ର ପ୍ରଶାସନିକ ନିୟନ୍ତ୍ରଣ ଅଧୀନରେ ଅଛି।\n"
                "ପ୍ରମାଣିତ କରାଯାଉଛି ଯେ ଧାରକ {CATEGORY_SCHEDULED_TRIBE} କିମ୍ବା {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} ବର୍ଗର ଯୋଗ୍ୟ ସଦସ୍ୟ ଅଟନ୍ତି।\n\n"

                "ଏହି ଦଲିଲ ଦ୍ୱାରା ଅଧିକାରରେ ଦିଆଯାଇଥିବା ଜଙ୍ଗଲ ଜମିର ସମୁଦାୟ କ୍ଷେତ୍ରଫଳ {TITLE_LAND_AREA_MEASURE} ଅଟେ।\n"
                "ଭୂମି ରେକର୍ଡରେ ଏହି ଜମିର ଖସଡା କିମ୍ବା କମ୍ପାର୍ଟମେଣ୍ଟ ନମ୍ବର {KHASRA_COMPARTMENT_NUMBER} ରୂପେ ଦର୍ଜ ଅଛି।\n"
                "ଜମିର ଚାରି ଦିଗର ସୀମା ପ୍ରାକୃତିକ ଚିହ୍ନଗୁଡ଼ିକ ଦ୍ୱାରା {BOUNDARY_DESCRIPTION} ରୂପେ ବର୍ଣ୍ଣନା କରାଯାଇଛି।\n"
                "ଏହି ଅଧିକାର ବଂଶାନୁକ୍ରମିକ ଅଟେ, କିନ୍ତୁ ଏହାକୁ ବିକ୍ରି ବା ହସ୍ତାନ୍ତର କରାଯାଇପାରିବ ନାହିଁ।\n"
                "ଜିଲ୍ଲାପାଳ ଏବଂ ଖଣ୍ଡୀୟ ଜଙ୍ଗଲ ଅଧିକାରୀଙ୍କ ସ୍ୱାକ୍ଷର ସହିତ ଏହାକୁ ଆନୁଷ୍ଠାନିକ ଭାବେ ଜାରି କରାଯାଇଛି।"
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "ଜନଜାତି ବ୍ୟାପାର ମନ୍ତ୍ରଣାଳୟ ଦ୍ୱାରା ଜାରି କରାଯାଇଥିବା ବ୍ୟକ୍ତିଗତ ଜଙ୍ଗଲ ଜମି ଅଧିକାର ପତ୍ର (ପଟ୍ଟା)।\n"
                "ଶ୍ରୀ/ଶ୍ରୀମତୀ {TITLE_HOLDER_NAME} (ପିତା/ମାତା: {FATHER_MOTHER_NAME}, ସ୍ୱାମୀ/ସ୍ତ୍ରୀ: {SPOUSE_NAME}) ଙ୍କୁ ଏହି ପଟ୍ଟା ପ୍ରଦାନ କରାଯାଉଛି।\n"
                "ତାଙ୍କ ଉପରେ ଆଶ୍ରିତ ଥିବା {DEPENDENT_NAME} ଭଳି ପରିବାରର ଅନ୍ୟ ସଦସ୍ୟମାନଙ୍କର ମଧ୍ୟ ଏହି ଜମି ଉପରେ ଅଧିକାର ସୁରକ୍ଷିତ ରହିବ।\n"
                "ଏମାନଙ୍କ ବାସସ୍ଥାନ ଠିକଣା {TITLE_ADDRESS_FULL} ଭାବରେ ସରକାରୀ ରେକର୍ଡରେ ଯଥାବିଧି ଲିପିବଦ୍ଧ ହୋଇଛି।\n"
                "ଏହି କ୍ଷେତ୍ର {STATE} ରାଜ୍ୟର {DISTRICT} ଜିଲ୍ଲାରେ ଅବସ୍ଥିତ {TEHSIL_TALUKA} ତହସିଲ ଅନ୍ତର୍ଗତ ଆସୁଛି।\n\n"

                "ଏହି ଜମିଖଣ୍ଡ {VILLAGE} ଗ୍ରାମରେ, {GRAM_PANCHAYAT} ପଞ୍ଚାୟତ ଅଧୀନରେ, {GRAM_SABHA} ଗ୍ରାମ ସଭାର ନିୟନ୍ତ୍ରଣରେ ଅଛି।\n"
                "ହିତାଧିକାରୀଙ୍କୁ ଆଦିବାସୀ ଶ୍ରେଣୀ {CATEGORY_SCHEDULED_TRIBE} କିମ୍ବା ପାରମ୍ପରିକ ବନବାସୀ {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} ଭାବରେ ସ୍ୱୀକୃତି ପ୍ରାପ୍ତ ହୋଇଛି।\n"
                "ସରକାର କୃଷି ଏବଂ ଆବାସ ଉଦ୍ଦେଶ୍ୟରେ ଏମାନଙ୍କୁ {TITLE_LAND_AREA_MEASURE} କ୍ଷେତ୍ରଫଳର ଜମି ଆବଣ୍ଟିତ କରିଛନ୍ତି।\n"
                "ରାଜସ୍ୱ ରେକର୍ଡରେ ସେହି ଜମିର ଖସଡା (Khasra) କିମ୍ବା ମାପ ସଂଖ୍ୟା {KHASRA_COMPARTMENT_NUMBER} ସ୍ପଷ୍ଟ ଭାବେ ଅଙ୍କିତ ଅଛି।\n"
                "ସ୍ଥାନର ସଠିକ୍ ଅବସ୍ଥିତି ଏବଂ ପରିଧିକୁ {BOUNDARY_DESCRIPTION} ର ସୀମା ନିର୍ଦ୍ଧାରଣ ବିବରଣୀ ମାଧ୍ୟମରେ ପ୍ରାମାଣିକୃତ କରାଯାଇଛି।\n\n"

                "ଏହି ଜଙ୍ଗଲ ଜମି ପଟ୍ଟା ଜଙ୍ଗଲ ଅଧିକାର ଅଧିନିୟମ ୨୦୦୬ ର ସମସ୍ତ ନିୟମ ଅଧୀନରେ ଅଟେ।\n"
                "ଧାରକଙ୍କୁ କେବଳ ଏହି ଜମିରେ ଚାଷ କରିବାକୁ ଏବଂ ପିଢ଼ି ପରେ ପିଢ଼ି ଏହାର ଉପଭୋଗ କରିବାର ଅଧିକାର ଅଛି।\n"
                "କୌଣସି ବି ପରିସ୍ଥିତିରେ ଏହି ଜଙ୍ଗଲ ଜମିକୁ କୌଣସି ଅନ୍ୟ ବ୍ୟକ୍ତିଙ୍କୁ ବିକ୍ରି କିମ୍ବା ଲିଜ୍ ରେ ଦିଆଯାଇପାରିବ ନାହିଁ।\n"
                "ସମ୍ପୃକ୍ତ ବିଭାଗର ଅଧିକାରୀମାନଙ୍କ ଦ୍ୱାରା ରାଜ୍ୟ ସରକାରଙ୍କ ଆନୁଷ୍ଠାନିକ ମୋହର ସହିତ ଏହାକୁ ପ୍ରମାଣିତ କରାଯାଇଛି।\n"
                "ଏହି ଦଲିଲ ପଟ୍ଟାଧାରୀଙ୍କ ଜୀବିକା ରକ୍ଷା କରୁଥିବା ଆଇନଗତ କବଚ ଭାବରେ କାର୍ଯ୍ୟ କରିବ।"
            ),
            # Variation 3: Formal Letter Style
            (
                "ଜଙ୍ଗଲ ଜମି ଅଧିକାର ଆଦେଶ ଏବଂ ପଟ୍ଟା ପ୍ରମାଣପତ୍ର।\n"
                "ଅଧିକାର ଧାରକଙ୍କ ନାମ: {TITLE_HOLDER_NAME}। ପିତା-ମାତାଙ୍କ ନାମ: {FATHER_MOTHER_NAME}। ସ୍ୱାମୀ/ସ୍ତ୍ରୀ: {SPOUSE_NAME}।\n"
                "ଆଶ୍ରିତ ସଦସ୍ୟ: {DEPENDENT_NAME}। ଧାରକଙ୍କ ଶ୍ରେଣୀ: {CATEGORY_SCHEDULED_TRIBE} / {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER}।\n"
                "ଠିକଣା: {TITLE_ADDRESS_FULL}, ଗ୍ରାମ: {VILLAGE}, ପଞ୍ଚାୟତ: {GRAM_PANCHAYAT}, ଗ୍ରାମ ସଭା: {GRAM_SABHA}।\n"
                "ତହସିଲ: {TEHSIL_TALUKA}, ଜିଲ୍ଲା: {DISTRICT}, ରାଜ୍ୟ: {STATE}।\n\n"

                "ଜଙ୍ଗଲ ଅଧିକାର ଅଧିନିୟମ ୨୦୦୬ ର ଧାରା ୪ ଅନ୍ତର୍ଗତ ଏହି ଜମି ଅଧିକାରକୁ ଆନୁଷ୍ଠାନିକ ଭାବେ ମାନ୍ୟତା ଦିଆଯାଉଛି।\n"
                "ଉପରୋକ୍ତ ହିତାଧିକାରୀଙ୍କ ଦଖଲରେ ଥିବା {TITLE_LAND_AREA_MEASURE} କ୍ଷେତ୍ରଫଳର ଜମି ପାଇଁ ପଟ୍ଟା ପ୍ରଦାନ କରାଯାଉଛି।\n"
                "ରାଜସ୍ୱ ବିଭାଗର ଅଭିଲେଖ ଅନୁଯାୟୀ, ଏହି ଜମିର ଖସଡା ନମ୍ବର {KHASRA_COMPARTMENT_NUMBER} ଅଟେ।\n"
                "ଜମିର ସୀମାଗୁଡ଼ିକ {BOUNDARY_DESCRIPTION} ର ଚିହ୍ନଗୁଡ଼ିକ ସହିତ ସଠିକତା ସହ ପରିଭାଷିତ କରାଯାଇଛି।\n"
                "ସମସ୍ତ ଯାଞ୍ଚ ଏବଂ ପ୍ରମାଣୀକରଣ ପରେ, ଜିଲ୍ଲା ସ୍ତରୀୟ କମିଟି (DLC) ଏହି ଜମି ଆବଣ୍ଟନକୁ ନିଜର ସ୍ୱୀକୃତି ଦେଇଛି।\n\n"

                "ଏହି ଜମି ଅଧିକାର ଏକ ବଂଶାନୁକ୍ରମିକ ଅଧିକାର ଭାବରେ ଜାରି ରହିବ, କିନ୍ତୁ ଜମି ଅହସ୍ତାନ୍ତରଣୀୟ (non-transferable) ଅଟେ।\n"
                "ହିତାଧିକାରୀଙ୍କ ପାଇଁ ସରକାରଙ୍କ ଦ୍ୱାରା ସମୟ ସମୟରେ ଲାଗୁ ହେଉଥିବା ଜଙ୍ଗଲ ସଂରକ୍ଷଣ ନିୟମ ପାଳନ କରିବା ବାଧ୍ୟତାମୂଳକ ହେବ।\n"
                "ଏହା ମାଧ୍ୟମରେ, ସରକାରଙ୍କ ଦ୍ୱାରା ବନବାସୀମାନଙ୍କର ଅର୍ଥନୈତିକ ଏବଂ ସାମାଜିକ ସୁରକ୍ଷା ସୁନିଶ୍ଚିତ କରାଯାଉଛି।\n"
                "ଏହି ପ୍ରମାଣପତ୍ର ରାଜ୍ୟ ସରକାରଙ୍କ ଅଧିକୃତ ଅଧିକାରୀମାନଙ୍କ ଦ୍ୱାରା ସ୍ୱାକ୍ଷରିତ ଏବଂ ମୋହରଯୁକ୍ତ ଅଟେ।\n"
                "ଏହି ଦଲିଲ ଜାରି ହେବା ତାରିଖରୁ ହିଁ ବିଧିକ ରୂପରେ ପ୍ରଭାବଶାଳୀ ହେବ।"
            ),
            # Variation 4: Legal / Statutory Document Style
            (
                "ଜଙ୍ଗଲ ଜମି ଅଧିକାର ଅଧିନିୟମ ୨୦୦୬ ଅନ୍ତର୍ଗତ ବୈଧାନିକ ପଟ୍ଟା ଦଲିଲ (Statutory Title Deed)।\n"
                "ରାଜ୍ୟ ସରକାରଙ୍କ ବିଧିକ କ୍ଷମତା ଅଧୀନରେ, ଏହି ଅଧିକାର ପତ୍ର {TITLE_HOLDER_NAME} ନାମକ ହିତାଧିକାରୀଙ୍କ ସପକ୍ଷରେ ବୈଧାନିକ ରୂପେ ପଞ୍ଜିକୃତ କରାଯାଉଛି।\n"
                "ଅଭିଲେଖ ଅନୁଯାୟୀ ହିତାଧିକାରୀଙ୍କ ପିତା/ମାତାଙ୍କ ନାମ {FATHER_MOTHER_NAME} ଏବଂ ବିଧିକ ସ୍ୱାମୀ/ସ୍ତ୍ରୀଙ୍କ ନାମ {SPOUSE_NAME} ସତ୍ୟାପିତ କରାଯାଇଛି।\n"
                "ହିତାଧିକାରୀଙ୍କ ଉପରେ ପୂର୍ଣ୍ଣତଃ ଆଶ୍ରିତ ବିଧିକ ଉତ୍ତରାଧିକାରୀମାନଙ୍କର {DEPENDENT_NAME} ନାମ ମଧ୍ୟ ଏହି ଦଲିଲରେ ଅନ୍ତର୍ଭୁକ୍ତ କରାଯାଇଛି।\n"
                "ହିତାଧିକାରୀଙ୍କ ଆଧିକାରିକ ଏବଂ ବୈଧାନିକ ବାସସ୍ଥାନ ଠିକଣା {TITLE_ADDRESS_FULL} ଭାବେ ରାଜସ୍ୱ ତଥା ଜଙ୍ଗଲ ଅଭିଲେଖରେ ଦର୍ଜ ଅଛି।\n"
                "ଏହି ଭୂଖଣ୍ଡ {STATE} ରାଜ୍ୟ, {DISTRICT} ଜିଲ୍ଲା, {TEHSIL_TALUKA} ତହସିଲ ଅନ୍ତର୍ଗତ {VILLAGE} ଗ୍ରାମ, {GRAM_PANCHAYAT} ଗ୍ରାମ ପଞ୍ଚାୟତ ଏବଂ {GRAM_SABHA} ଗ୍ରାମ ସଭାର ବୈଧାନିକ କ୍ଷେତ୍ରାଧିକାରରେ ଅବସ୍ଥିତ।\n\n"

                "ହିତାଧିକାରୀଙ୍କ ବିଧିକ ବର୍ଗୀକରଣ, ଜମିର ମାପ ଏବଂ ଭୌଗୋଳିକ ସୀମାଗୁଡ଼ିକର ପ୍ରମାଣୀକରଣ।\n"
                "ହିତାଧିକାରୀଙ୍କୁ ଅଧିନିୟମର ବିଧିକ ପ୍ରାବଧାନ ଅଧୀନରେ {CATEGORY_SCHEDULED_TRIBE} ଅଥବା {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} ଶ୍ରେଣୀର ଯୋଗ୍ୟ ପାତ୍ର ବିବେଚନା କରାଯାଇଛି।\n"
                "ସରକାରଙ୍କ ଦ୍ୱାରା ଯଥାବିଧି ମାପ ପରେ ଆବଣ୍ଟିତ ଜଙ୍ଗଲ ଜମିର ସମୁଦାୟ କ୍ଷେତ୍ରଫଳ {TITLE_LAND_AREA_MEASURE} ଘୋଷଣା କରାଯାଇଛି।\n"
                "ରାଜସ୍ୱ ଏବଂ ଜଙ୍ଗଲ ଅଭିଲେଖରେ ଏହି ଜମିର ବିଶିଷ୍ଟ ଖସଡା (Khasra) କିମ୍ବା କମ୍ପାର୍ଟମେଣ୍ଟ ନମ୍ବର {KHASRA_COMPARTMENT_NUMBER} ଦର୍ଜ କରାଯାଇଛି।\n"
                "ଏହି ଭୂଖଣ୍ଡର ଚାରି ଦିଗର ଭୌଗୋଳିକ ଏବଂ ପ୍ରାକୃତିକ ସୀମାଗୁଡ଼ିକ {BOUNDARY_DESCRIPTION} ରୂପେ ଅତ୍ୟନ୍ତ ସ୍ପଷ୍ଟତାର ସହ ସୀମାଙ୍କିତ କରାଯାଇଛି।\n"
                "ଏହି ମାପ ରାଜସ୍ୱ ନିରୀକ୍ଷକ ଏବଂ ଜଙ୍ଗଲ ବିଭାଗର ସର୍ଭେକ୍ଷକମାନଙ୍କ ଦ୍ୱାରା ପ୍ରତ୍ୟକ୍ଷ ଭୌତିକ ସତ୍ୟାପନ ପରେ କରାଯାଇଛି।\n\n"

                "ଅଧିକାରର ବୈଧାନିକ ପ୍ରକୃତି, ପ୍ରତିବନ୍ଧକ ଏବଂ ପ୍ରାଧିକାରୀମାନଙ୍କର ପ୍ରମାଣୀକରଣ।\n"
                "ଧାରା ୪(୪) ର ପ୍ରାବଧାନ ଅନ୍ତର୍ଗତ, ଏହି ଜମି ଅଧିକାର ପୂର୍ଣ୍ଣତଃ ବଂଶାନୁକ୍ରମିକ ଅଟେ, ପରନ୍ତୁ କୌଣସି ଦଶାରେ ଏହାକୁ ବିକ୍ରି, ହସ୍ତାନ୍ତର କିମ୍ବା ବନ୍ଧକ ରଖାଯାଇପାରିବ ନାହିଁ (non-alienable)।\n"
                "ହିତାଧିକାରୀ ଜଙ୍ଗଲ ସଂରକ୍ଷଣ ଅଧିନିୟମ ଏବଂ ପରିବେଶ ସୁରକ୍ଷା ନିୟମର ଅନୁପାଳନ ପାଇଁ ବିଧିକ ରୂପେ ବାଧ୍ୟ ହେବେ।\n"
                "ଯଦି ନିୟମଗୁଡ଼ିକର ଉଲ୍ଲଂଘନ ହୋଇଥିବା ଜଣାପଡେ, ତେବେ ବିନା କୌଣସି ପୂର୍ବ ସୂଚନାରେ ରାଜ୍ୟ ସରକାର ଏହି ଅଧିକାରକୁ ବାତିଲ କରିବାର ପୂର୍ଣ୍ଣ କ୍ଷମତା ରଖନ୍ତି।\n"
                "ଏହି ବୈଧାନିକ ପଟ୍ଟା ଉପ-ଖଣ୍ଡୀୟ (SDLC) ତଥା ଜିଲ୍ଲା ସ୍ତରୀୟ (DLC) କମିଟିଗୁଡ଼ିକର ଯଥାବିଧି ଅନୁମୋଦନ ପରେ ହିଁ ନିର୍ଗତ କରାଯାଇଛି।\n"
                "ଏହାର ବୈଧାନିକ ପୁଷ୍ଟି ନିମନ୍ତେ, ଜିଲ୍ଲାପାଳ (District Collector) ତଥା ଖଣ୍ଡୀୟ ଜଙ୍ଗଲ ଅଧିକାରୀ (DFO) ଏହି ପଟ୍ଟା ଉପରେ ଆଧିକାରିକ ସ୍ୱାକ୍ଷର ଏବଂ ମୋହର ଅଙ୍କିତ କରିଛନ୍ତି।"
            )
        ],

        DOC_TITLE_COMMUNITY_FOREST_RIGHTS: [
            # Variation 1: Bureaucratic / Form Style
            (
                "ପରିଶିଷ୍ଟ - III [ନିୟମ ୮(ଜ) ଦେଖନ୍ତୁ]\n"
                "ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ଅଧିକାର ପାଇଁ ପଟ୍ଟା ଏବଂ ଆଧିକାରିକ ଅଧିକାର ଦଲିଲ।\n"
                "ଏହି ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ଅଧିକାର {COMMUNITY_RIGHT_HOLDER_NAME} ନାମକ ସାମୂହିକ ଇକାଇକୁ ପ୍ରଦାନ କରାଯାଉଛି।\n"
                "ଏହି କ୍ଷେତ୍ର {STATE} ରାଜ୍ୟ, {DISTRICT} ଜିଲ୍ଲା ଏବଂ {TEHSIL_TALUKA} ତହସିଲ ଅନ୍ତର୍ଗତ ଆସୁଛି।\n"
                "ଏହି ପଟ୍ଟା {VILLAGE} ଗ୍ରାମ, {GRAM_PANCHAYAT} ଗ୍ରାମ ପଞ୍ଚାୟତ ଏବଂ {GRAM_SABHA} ଗ୍ରାମ ସଭାର ସାମୂହିକ ସମ୍ପତ୍ତି ଅଟେ।\n\n"

                "ଏହି ଅଧିକାର ପ୍ରାପ୍ତ କରୁଥିବା ସମ୍ପ୍ରଦାୟ {CATEGORY_SCHEDULED_TRIBE} କିମ୍ବା {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} ଭାବରେ ସ୍ୱୀକୃତିପ୍ରାପ୍ତ ଅଟେ।\n"
                "ସମ୍ପ୍ରଦାୟକୁ ପ୍ରଦାନ କରାଯାଇଥିବା ଅଧିକାରର ପ୍ରକୃତି {COMMUNITY_RIGHT_NATURE} ରୂପେ ସ୍ପଷ୍ଟ ଭାବରେ ପରିଭାଷିତ କରାଯାଇଛି।\n"
                "ଏହି ଅଧିକାରର ବ୍ୟବହାର କରିବା ସହ ଜଡିତ କିଛି ସର୍ତ୍ତ ଅଛି, ଯାହା ଏହିପରି: {TITLE_CONDITIONS}।\n"
                "ଏହି ଅଧିକାର ଅଧୀନରେ ଆସୁଥିବା ଜଙ୍ଗଲ କ୍ଷେତ୍ରର ଖସଡା/କମ୍ପାର୍ଟମେଣ୍ଟ ନମ୍ବର {KHASRA_COMPARTMENT_NUMBER} ଅଟେ।\n"
                "ଜମିର ସୀମାଗୁଡ଼ିକ {BOUNDARY_DESCRIPTION} ଭଳି ଭୌଗୋଳିକ ସନ୍ଦର୍ଭଗୁଡ଼ିକ ଦ୍ୱାରା ଦର୍ଶାଯାଇଛି।\n\n"

                "ଏହା ଅତିରିକ୍ତ, ଏହି କ୍ଷେତ୍ରର ପାରମ୍ପରିକ ରୀତିନୀତି ସୀମା {CUSTOMARY_BOUNDARY} କୁ ମଧ୍ୟ ପାରମ୍ପରିକ ଭାବରେ ସ୍ୱୀକୃତି ପ୍ରାପ୍ତ ଅଛି।\n"
                "ଏହି ଦଲିଲ ସାମୂହିକ ଉପଯୋଗ ପାଇଁ ଜଙ୍ଗଲ ସମ୍ପଦକୁ ପ୍ରବେଶକୁ ବୈଧାନିକ ମାନ୍ୟତା ପ୍ରଦାନ କରେ।\n"
                "ପରନ୍ତୁ, ସମ୍ପଦର ଉପଯୋଗ ଏପରି କରାଯିବା ଉଚିତ ଯେପରି ଜଙ୍ଗଲର ଜୈବ ବିବିଧତାକୁ କୌଣସି କ୍ଷତି ନ ପହଞ୍ଚେ।\n"
                "ନିୟମଗୁଡ଼ିକର ଉଲ୍ଲଂଘନ ହେଲେ ସରକାରଙ୍କ ପାଖରେ ଏହି ଅଧିକାର ଉପରେ ପୁନର୍ବିଚାର କରିବାର କ୍ଷମତା ସୁରକ୍ଷିତ ଅଛି।\n"
                "ଏହି ପଟ୍ଟା ଜିଲ୍ଲା ସ୍ତରୀୟ ପ୍ରାଧିକାରୀମାନଙ୍କ ଦ୍ୱାରା ଅନୁମୋଦିତ ଏବଂ ଜାରି କରାଯାଇଛି।"
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ଅଧିକାର ପଟ୍ଟା ଏବଂ ଗ୍ରାମ ସଭାକୁ ବୈଧାନିକ ଅଧିକାର ହସ୍ତାନ୍ତରର ଦଲିଲ।\n"
                "ସରକାରଙ୍କ ଯଥାବିଧି ମଞ୍ଜୁରୀ ସହିତ, ଏହି ଅଧିକାର {COMMUNITY_RIGHT_HOLDER_NAME} ସଂସ୍ଥା/ସମ୍ପ୍ରଦାୟକୁ ଦିଆଯାଉଛି।\n"
                "ଏହି ସମ୍ପ୍ରଦାୟ {STATE} ରାଜ୍ୟର {DISTRICT} ଜିଲ୍ଲାରେ ଅବସ୍ଥିତ {TEHSIL_TALUKA} ତହସିଲରେ ଦୀର୍ଘ ଦିନ ଧରି ବସବାସ କରୁଛି।\n"
                "ଏମାନଙ୍କ ବାସସ୍ଥାନ କ୍ଷେତ୍ର {VILLAGE} ଗ୍ରାମ, {GRAM_PANCHAYAT} ପଞ୍ଚାୟତ ଏବଂ {GRAM_SABHA} ଗ୍ରାମ ସଭା ଅନ୍ତର୍ଗତ ସମାହିତ ଅଟେ।\n"
                "ଏମାନଙ୍କୁ ଆଧିକାରିକ ରେକର୍ଡରେ {CATEGORY_SCHEDULED_TRIBE} ଏବଂ {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} ଶ୍ରେଣୀ ଭାବରେ ଦର୍ଜ କରାଯାଇଛି।\n\n"

                "ଏମାନଙ୍କୁ ପ୍ରଦାନ କରାଯାଇଥିବା ସାମୂହିକ ଅଧିକାରର ସଠିକ୍ ପ୍ରକୃତିର ବିବରଣୀ {COMMUNITY_RIGHT_NATURE} ଅଟେ।\n"
                "ଏହି ସାମୂହିକ ଅଧିକାରର ପ୍ରୟୋଗ ନିମନ୍ତେ ନିର୍ଦ୍ଧାରିତ ନିୟମ ଏବଂ ସର୍ତ୍ତଗୁଡ଼ିକ {TITLE_CONDITIONS} ଅଟେ।\n"
                "ଜଙ୍ଗଲ ବିଭାଗର ଅଭିଲେଖ ଅନୁଯାୟୀ, ଏହି କ୍ଷେତ୍ରର ଖସଡା ନମ୍ବର {KHASRA_COMPARTMENT_NUMBER} ଅଙ୍କିତ ଅଛି।\n"
                "ଏହି କ୍ଷେତ୍ରର ସୀମାଗୁଡ଼ିକ ପ୍ରାକୃତିକ ଚିହ୍ନଗୁଡ଼ିକର ଉପଯୋଗ କରୁଥିବା ବେଳେ {BOUNDARY_DESCRIPTION} ରୂପେ ବର୍ଣ୍ଣିତ କରାଯାଇଛି।\n"
                "ସାଥିରେ, ପିଢ଼ି ପିଢ଼ି ଧରି ଚାଲି ଆସୁଥିବା ରୀତିନୀତି ସୀମା (Customary Boundary) {CUSTOMARY_BOUNDARY} ରୂପେ ପୁଷ୍ଟ କରାଯାଇଛି।\n\n"

                "ଏହି ଦଲିଲ ମାଧ୍ୟମରେ ଗୋଚର ଏବଂ ଲଘୁ ବନଜାତ ଦ୍ରବ୍ୟ ସଂଗ୍ରହର ସାମୂହିକ ଅଧିକାର ସୁରକ୍ଷିତ କରାଯାଉଛି।\n"
                "ପରିବେଶ ଏବଂ ଜଙ୍ଗଲ କ୍ଷେତ୍ରର ରକ୍ଷା କରିବାର ଉତ୍ତରଦାୟିତ୍ୱ ଏହି ସମ୍ପ୍ରଦାୟକୁ ହସ୍ତାନ୍ତର କରାଯାଉଛି।\n"
                "ଅବୈଧ ଗଛ କଟା ଏବଂ ଶିକାର ଭଳି ବେଆଇନ କାର୍ଯ୍ୟକଳାପ ସମ୍ପୂର୍ଣ୍ଣ ରୂପେ ନିଷିଦ୍ଧ ଅଟେ।\n"
                "ଏହା ରାଜ୍ୟ ସରକାରଙ୍କ ଜନଜାତି କଲ୍ୟାଣ ବିଭାଗ ଏବଂ ରାଜସ୍ୱ ବିଭାଗର ସହମତିରେ ଜାରି କରାଯାଉଛି।\n"
                "ଗ୍ରାମ ସଭାକୁ ଏହି ଦଲିଲକୁ ସୁରକ୍ଷିତ ରଖିବା ଉଚିତ ଏବଂ ଏହାର ପ୍ରାବଧାନଗୁଡ଼ିକୁ ଠିକ୍ ଭାବେ ଲାଗୁ କରିବା ଉଚିତ।"
            ),
            # Variation 3: Formal Letter Style
            (
                "ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ଅଧିକାରକୁ ମାନ୍ୟତା ଦେଉଥିବା ଆଧିକାରିକ ଅଧିକାର ପ୍ରମାଣପତ୍ର।\n"
                "ଅଧିକାର ପ୍ରାପ୍ତକର୍ତ୍ତା: {COMMUNITY_RIGHT_HOLDER_NAME}।\n"
                "କ୍ଷେତ୍ର: {VILLAGE} ଗ୍ରାମ, {GRAM_PANCHAYAT} ପଞ୍ଚାୟତ, {GRAM_SABHA} ଗ୍ରାମ ସଭା।\n"
                "ପ୍ରଶାସନିକ ସୀମା: ତହସିଲ {TEHSIL_TALUKA}, ଜିଲ୍ଲା {DISTRICT}, ରାଜ୍ୟ {STATE}।\n"
                "ହିତାଧିକାରୀ ଶ୍ରେଣୀ: {CATEGORY_SCHEDULED_TRIBE} ଅଥବା {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER}।\n\n"

                "ରାଜ୍ୟ ସରକାରଙ୍କ ଦ୍ୱାରା ଉପରୋକ୍ତ ସମ୍ପ୍ରଦାୟକୁ {COMMUNITY_RIGHT_NATURE} ପ୍ରକୃତି ବିଶିଷ୍ଟ ଜଙ୍ଗଲ ଅଧିକାର ପ୍ରଦାନ କରାଯାଉଛି।\n"
                "ଏହି ଅଧିକାର {TITLE_CONDITIONS} ରେ ଉଲ୍ଲିଖିତ ପ୍ରତିବନ୍ଧକ ଏବଂ ସର୍ତ୍ତଗୁଡ଼ିକ ଅଧୀନରେ ରହିବ।\n"
                "ଆବଣ୍ଟିତ ଜଙ୍ଗଲ ଜମିର ଖସଡା କିମ୍ବା ମାପ ସଂଖ୍ୟା {KHASRA_COMPARTMENT_NUMBER} ନିର୍ଦ୍ଧାରିତ ହୋଇଛି।\n"
                "ଦଲିଲଗୁଡ଼ିକରେ ନିର୍ଦ୍ଦିଷ୍ଟ ଜମିର ସୀମାଗୁଡ଼ିକ {BOUNDARY_DESCRIPTION} ଚିହ୍ନଗୁଡ଼ିକ ଦ୍ୱାରା ସ୍ଥିର କରାଯାଇଛି।\n"
                "ସମ୍ପ୍ରଦାୟ ଦ୍ୱାରା ପାରମ୍ପରିକ ଭାବେ ମାନ୍ୟ ପ୍ରାପ୍ତ ରୀତିନୀତି ସୀମା {CUSTOMARY_BOUNDARY} ମଧ୍ୟ ପ୍ରମାଣିତ କରାଯାଉଛି।\n\n"

                "ଏହି ଅଧିକାରର ପ୍ରୟୋଗ କେବଳ ଗ୍ରାମ ସଭାର ସାମୂହିକ ପରିଚାଳନା ଅଧୀନରେ ହିଁ କରାଯିବା ଉଚିତ।\n"
                "ଜଙ୍ଗଲ ସମ୍ପଦର ଉପଯୋଗ ବାଣିଜ୍ୟିକ ଉଦ୍ଦେଶ୍ୟ ପାଇଁ ନୁହେଁ, ବରଂ କେବଳ ସାମୂହିକ ଆବଶ୍ୟକତା ପାଇଁ କରାଯିବା ଉଚିତ।\n"
                "ଗ୍ରାମ ସଭାକୁ ସରକାରୀ ଅଡିଟ୍ ଏବଂ ନିରୀକ୍ଷଣରେ ପୂର୍ଣ୍ଣ ସହଯୋଗ ଦେବା ବାଧ୍ୟତାମୂଳକ ଅଟେ।\n"
                "ଏହି ଦଲିଲ ଜିଲ୍ଲାପାଳ ଏବଂ ଖଣ୍ଡୀୟ ଜଙ୍ଗଲ ଅଧିକାରୀଙ୍କ ମୋହର ସହିତ ଜାରି କରାଯାଉଛି।\n"
                "ଏହାର ଜାରି ହେବା ତାରିଖରୁ, ସମ୍ପ୍ରଦାୟର ଜଙ୍ଗଲ-ଆଧାରିତ ଅର୍ଥନୈତିକ ସ୍ୱାଧୀନତା ସୁନିଶ୍ଚିତ ହେଉଛି।"
            ),
            # Variation 4: Legal / Statutory Document Style
            (
                "ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ଅଧିକାର (CFR) ର ଗେଜେଟ୍ ପ୍ରକାଶିତ ବୈଧାନିକ ବିଲେଖ (Statutory Deed) ଏବଂ ପଟ୍ଟା।\n"
                "ଏହି ଆଧିକାରିକ ବିଲେଖ ମାଧ୍ୟମରେ, {COMMUNITY_RIGHT_HOLDER_NAME} ନାମକ ସାମୂହିକ ଇକାଇକୁ ଜଙ୍ଗଲ ଜମି ଉପରେ ବୈଧାନିକ ଅଧିକାର ପ୍ରଦାନ କରାଯାଉଛି।\n"
                "ଏହି ଅଧିକାର {STATE} ରାଜ୍ୟ, {DISTRICT} ଜିଲ୍ଲା ଏବଂ {TEHSIL_TALUKA} ତହସିଲର ଭୌଗୋଳିକ କ୍ଷେତ୍ରାଧିକାର ଭିତରେ ପ୍ରଦାନ କରାଯାଉଛି।\n"
                "ବୈଧାନିକ ରୂପେ ଏହି କ୍ଷେତ୍ର {VILLAGE} ଗ୍ରାମ, {GRAM_PANCHAYAT} ଗ୍ରାମ ପଞ୍ଚାୟତ ତଥା {GRAM_SABHA} ଗ୍ରାମ ସଭାର ପ୍ରଶାସନିକ ନିୟନ୍ତ୍ରଣରେ ଆସୁଛି।\n"
                "ଅଧିକାର ପ୍ରାପ୍ତ କରୁଥିବା ଏହି ସମ୍ପ୍ରଦାୟ, ସରକାରୀ ଅଭିଲେଖ ଅନୁଯାୟୀ {CATEGORY_SCHEDULED_TRIBE} ଅଥବା {CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER} ବୈଧାନିକ ଶ୍ରେଣୀ ଅଧୀନରେ ସୁରକ୍ଷିତ ଅଟେ।\n"
                "ଗ୍ରାମ ସଭାର ସାମୂହିକ ପ୍ରସ୍ତାବ ତଥା ଜିଲ୍ଲା ସ୍ତରୀୟ କମିଟି (DLC) ର ଅନୁମୋଦନ ଆଧାରରେ ଏହି ଦଲିଲ ବୈଧାନିକ ରୂପେ ନିର୍ଗତ କରାଯାଉଛି।\n\n"

                "ସ୍ୱୀକୃତ ଗୋଷ୍ଠୀ ଅଧିକାରର ପ୍ରକୃତି, ସର୍ତ୍ତ ଏବଂ ଭୌଗୋଳିକ ପ୍ରଲେଖୀକରଣ।\n"
                "ସରକାରଙ୍କ ଦ୍ୱାରା ଏହି ସମ୍ପ୍ରଦାୟକୁ ଆଧିକାରିକ ଭାବରେ ପ୍ରଦାନ କରାଯାଇଥିବା ଅଧିକାରର ପ୍ରକୃତି {COMMUNITY_RIGHT_NATURE} ରୂପେ ସୁସ୍ପଷ୍ଟ ପରିଭାଷିତ ଅଟେ।\n"
                "ଏହି ଅଧିକାରର ଉପଯୋଗ କରିବା ପାଇଁ ଜଙ୍ଗଲ ବିଭାଗ ଦ୍ୱାରା ଲାଗୁ କରାଯାଇଥିବା ବୈଧାନିକ ସର୍ତ୍ତ ଏବଂ ପ୍ରତିବନ୍ଧକ ଏହି ପ୍ରକାରର: {TITLE_CONDITIONS}।\n"
                "ଗୋଷ୍ଠୀ ଅଧିକାରର ଅଧୀନରେ ଆସୁଥିବା ଜଙ୍ଗଲ କ୍ଷେତ୍ରର ବୈଧାନିକ ଖସଡା କିମ୍ବା ମାପ ସଂଖ୍ୟା {KHASRA_COMPARTMENT_NUMBER} ରୂପେ ପଞ୍ଜିକୃତ ଅଟେ।\n"
                "ଜମିର ସୀମାଗୁଡ଼ିକ, ପାହାଡ଼, ନଦୀ ଭଳି ପ୍ରାକୃତିକ ଚିହ୍ନଗୁଡ଼ିକର ସନ୍ଦର୍ଭ ଦେଇ {BOUNDARY_DESCRIPTION} ରୂପେ ପ୍ରଲେଖିତ କରାଯାଇଛି।\n"
                "ସାଥିରେ, ଅନେକ ପିଢ଼ିରୁ ସମ୍ପ୍ରଦାୟ ଦ୍ୱାରା ମାନ୍ୟ ରୀତିନୀତି ସୀମା (Customary Boundary) {CUSTOMARY_BOUNDARY} ବୈଧାନିକ ରୂପେ ପୁଷ୍ଟ କରାଯାଉଛି।\n\n"

                "ସମ୍ପ୍ରଦାୟର ବୈଧାନିକ ଦାୟିତ୍ୱ, ପ୍ରତିବନ୍ଧକ ଏବଂ ସରକାରଙ୍କ ଚୂଡାନ୍ତ ଅନୁମୋଦନ।\n"
                "ଏହି ଅଧିକାର ପ୍ରମାଣ ପତ୍ର ପୂର୍ଣ୍ଣତଃ ସାମୂହିକ ଉପଯୋଗ ନିମନ୍ତେ ଅଟେ; ଏହାର କୌଣସି ବି ପ୍ରକାରର ବାଣିଜ୍ୟିକ (Commercial) ଶୋଷଣ ବର୍ଜିତ ଅଟେ।\n"
                "ପଶୁମାନଙ୍କ ଚାରଣ ଏବଂ ବନଜାତ ଦ୍ରବ୍ୟ ସଂଗ୍ରହ ସହିତ, ଜଙ୍ଗଲର ଜୈବ ବିବିଧତାକୁ କୌଣସି କ୍ଷତି ନ ପହଞ୍ଚିବ, ଏହା ସୁନିଶ୍ଚିତ କରିବା ସମ୍ପ୍ରଦାୟର ବୈଧାନିକ ଦାୟିତ୍ୱ ଅଟେ।\n"
                "ଯଦି ଅବୈଧ କଟା କିମ୍ବା ରାଜ୍ୟ ବିରୋଧୀ କାର୍ଯ୍ୟକଳାପରେ ସମ୍ପୃକ୍ତି ଜଣାପଡେ, ତେବେ ଏହି ଅଧିକାର ତତ୍କାଳ ପ୍ରଭାବ ସହିତ ରଦ୍ଦ କରିଦିଆଯିବ।\n"
                "ଜନଜାତି କଲ୍ୟାଣ ବିଭାଗ ଏବଂ ଜଙ୍ଗଲ ବିଭାଗ ଉଭୟଙ୍କ ପୂର୍ଣ୍ଣ ସମନ୍ୱୟ ସହିତ ଏହି ପ୍ରଲେଖକୁ ପ୍ରଶାସିତ କରାଯିବ।\n"
                "ଜିଲ୍ଲାପାଳ (DM) ଏବଂ ସମ୍ପୃକ୍ତ ଜଙ୍ଗଲ ଅଧିକାରୀଙ୍କ ଆଧିକାରିକ ମୋହର ଏବଂ ସ୍ୱାକ୍ଷର ସହିତ ଏହି ପଟ୍ଟା ଗେଜେଟ୍ ରେ ପଞ୍ଜିକୃତ କରାଯାଉଛି।"
            )
        ],

        DOC_TITLE_COMMUNITY_FOREST_RESOURCES: [
            # Variation 1: Bureaucratic / Form Style
            (
                "ପରିଶିଷ୍ଟ - IV [ନିୟମ ୮(ଝ) ଦେଖନ୍ତୁ]\n"
                "ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦ (CFR) ପାଇଁ ପଟ୍ଟା ଏବଂ ଅଧିକାର ପତ୍ର।\n"
                "ଏହି ଆଧିକାରିକ ଦଲିଲ {STATE} ରାଜ୍ୟ, {DISTRICT} ଜିଲ୍ଲା, {TEHSIL_TALUKA} ତହସିଲ ଅନ୍ତର୍ଗତ ଆସୁଥିବା କ୍ଷେତ୍ରକୁ ପ୍ରଦାନ କରାଯାଉଛି।\n"
                "ଏହା ଅନୁଯାୟୀ, {VILLAGE} ଗ୍ରାମ, {GRAM_PANCHAYAT} ଗ୍ରାମ ପଞ୍ଚାୟତ ଏବଂ {GRAM_SABHA} ଗ୍ରାମ ସଭାକୁ ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦ ଅଧିକାର ଦିଆଯାଉଛି।\n"
                "ଏହି ଅଧିକାର {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} କିମ୍ବା {COMMUNITY_TYPE_BOTH} ସମ୍ପ୍ରଦାୟ ସହିତ ଜଡିତ ଲୋକଙ୍କ ପାଇଁ ଅଟେ।\n\n"

                "ଏହି ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦ ଅଧିକାର ଅଧୀନରେ ଥିବା କ୍ଷେତ୍ରର ଖସଡା/କମ୍ପାର୍ଟମେଣ୍ଟ ନମ୍ବର {KHASRA_COMPARTMENT_NUMBER} ଅଟେ।\n"
                "ଏହି କ୍ଷେତ୍ରର ଭୌଗୋଳିକ ସ୍ଥିତି ଏବଂ ସୀମାଗୁଡ଼ିକ {BOUNDARY_DESCRIPTION} ରୂପେ ଅତ୍ୟନ୍ତ ସ୍ପଷ୍ଟ ଭାବରେ ପ୍ରଲେଖିତ କରାଯାଇଛି।\n"
                "ସାଥିରେ, ଶତାବ୍ଦୀ ଶତାବ୍ଦୀ ଧରି ଚାଲି ଆସୁଥିବା ପାରମ୍ପରିକ ରୀତିନୀତି ସୀମା {CUSTOMARY_BOUNDARY} କୁ ଆଇନଗତ ରୂପେ ସ୍ୱୀକୃତି ମିଳିଛି।\n"
                "ନିର୍ଦ୍ଦିଷ୍ଟ କ୍ଷେତ୍ର ଭିତରେ ଥିବା ସମସ୍ତ ଲଘୁ ବନଜାତ ଦ୍ରବ୍ୟର ପରିଚାଳନାର ଅଧିକାର ଗ୍ରାମ ସଭାକୁ ସମର୍ପିତ କରାଯାଇଛି।\n"
                "ଜଙ୍ଗଲ ବିଭାଗର ମାର୍ଗଦର୍ଶିକା ଅନୁଯାୟୀ, ସମ୍ପ୍ରଦାୟକୁ ଏହି ସମ୍ପଦର ସଂରକ୍ଷଣ ଏବଂ ସ୍ଥାୟୀ ଉପଯୋଗ କରିବାକୁ ହେବ।\n\n"

                "ଏହି ଅଧିକାର ଆଦିବାସୀ ଏବଂ ଅନ୍ୟ ପାରମ୍ପରିକ ବନବାସୀଙ୍କ ଜୀବିକାକୁ ଉନ୍ନତ କରିବା ଉଦ୍ଦେଶ୍ୟରେ ଦିଆଯାଉଛି।\n"
                "ଜଙ୍ଗଲ ସମ୍ପଦର ପରିଚାଳନା ପାଇଁ ସମିତି ଗଠନ କରିବାର ପୂର୍ଣ୍ଣ ଅଧିକାର ଗ୍ରାମ ସଭାକୁ ଦିଆଯାଇଛି।\n"
                "ଏହି ସମ୍ପଦକୁ କ୍ଷତି ପହଞ୍ଚାଉଥିବା କୌଣସି କାର୍ଯ୍ୟକୁ ଆଇନଗତ ଅପରାଧ ମାନି ନିଆଯିବ ଏବଂ ଅଧିକାର ରଦ୍ଦ କରାଯିବ।\n"
                "ରାଜ୍ୟ ସରକାରଙ୍କ ସକ୍ଷମ ଅଧିକାରୀ, ଯେପରିକି ଜିଲ୍ଲାପାଳ ଏବଂ ଜଙ୍ଗଲ ଅଧିକାରୀ ଏହାକୁ ଯଥାବିଧି ଅନୁମୋଦିତ କରିଛନ୍ତି।\n"
                "ଏହି ଦଲିଲ ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦର ସଂରକ୍ଷଣରେ ଏକ ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ମାଇଲଖୁଣ୍ଟ ଭାବରେ ଦର୍ଜ କରାଯାଉଛି।"
            ),
            # Variation 2: Narrative / Descriptive Style
            (
                "ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦ ପାଇଁ ବୈଧାନିକ ଅଧିକାର ପ୍ରଲେଖ ଏବଂ ଗ୍ରାମ ସଭାକୁ କ୍ଷମତା ହସ୍ତାନ୍ତର।\n"
                "ସରକାର {STATE} ରାଜ୍ୟର {DISTRICT} ଜିଲ୍ଲାରେ ଅବସ୍ଥିତ {TEHSIL_TALUKA} ତହସିଲରେ ରହୁଥିବା ଲୋକଙ୍କ ଦାବିକୁ ଗ୍ରହଣ କରିଛନ୍ତି।\n"
                "ଏହି ଆଧାରରେ {VILLAGE} ଗ୍ରାମ, {GRAM_PANCHAYAT} ପଞ୍ଚାୟତ ଏବଂ {GRAM_SABHA} ଗ୍ରାମ ସଭାକୁ CFR ପଟ୍ଟା ପ୍ରଦାନ କରାଯାଉଛି।\n"
                "ଏହି ଅଧିକାର ମାନ୍ୟତା {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} ଅଥବା {COMMUNITY_TYPE_BOTH} ସମ୍ପ୍ରଦାୟ ଉପରେ ଲାଗୁ ହେଉଛି।\n"
                "ଏହି ସମ୍ପ୍ରଦାୟଗୁଡ଼ିକ ଜଙ୍ଗଲକୁ ଦେବତା ମାନନ୍ତି ଏବଂ ତାକୁ ସଂରକ୍ଷିତ କରିବାର ପରମ୍ପରା ରଖନ୍ତି।\n\n"

                "ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦ କ୍ଷେତ୍ର ପାଇଁ ଖସଡା/କମ୍ପାର୍ଟମେଣ୍ଟ ନମ୍ବର {KHASRA_COMPARTMENT_NUMBER} ଭୂମି ସର୍ବେକ୍ଷଣ ରେକର୍ଡରେ ଉଲ୍ଲିଖିତ ଅଛି।\n"
                "ଏହି କ୍ଷେତ୍ରର ସୀମାଗୁଡ଼ିକ, ପାହାଡ଼ ଏବଂ ନଦୀଗୁଡ଼ିକୁ ଚିହ୍ନିତ କରୁଥିବା {BOUNDARY_DESCRIPTION} ରୂପେ ପରିଭାଷିତ କରାଯାଇଛି।\n"
                "ଏହା ବାହାରେ ଆମର ପାରମ୍ପରିକ ରୀତିନୀତି ସୀମା {CUSTOMARY_BOUNDARY} କୁ ମଧ୍ୟ ସରକାରଙ୍କ ଦ୍ୱାରା ସ୍ୱୀକାର କରି ନିଆଯାଇଛି।\n"
                "ଏହି ସୀମା ଭିତରେ ଉପଲବ୍ଧ ଜାଳେଣି କାଠ, ମହୁ ଏବଂ ଚେରମୂଳିର ସ୍ୱାଧୀନ ରୂପେ ଉପଯୋଗ କରିବାର ଅଧିକାର ଗ୍ରାମ ସଭାର ଅଛି।\n"
                "ଏହା ବ୍ୟତୀତ, ଜଙ୍ଗଲ ମାଫିଆମାନଙ୍କଠାରୁ ଜଙ୍ଗଲର ରକ୍ଷା କରିବାର ପୂର୍ଣ୍ଣ ଦାୟିତ୍ୱ ଏହି ସମ୍ପ୍ରଦାୟକୁ ସମର୍ପିତ କରାଯାଇଛି।\n\n"

                "ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦ ଅଧିକାର ଆଇନ ଆଦିବାସୀ ଲୋକଙ୍କ ଆତ୍ମନିର୍ଣ୍ଣୟର ଅଧିକାରକୁ ସୁନିଶ୍ଚିତ କରେ।\n"
                "ଜୈବ ବିବିଧତାକୁ ବଜାୟ ରଖିବା ପାଇଁ ଗ୍ରାମ ସଭାକୁ ଏକ ଉଚିତ ପରିଚାଳନା ଯୋଜନା ପ୍ରସ୍ତୁତ କରିବାକୁ ହେବ।\n"
                "ସରକାର ଏବଂ ଜଙ୍ଗଲ ବିଭାଗ ଗ୍ରାମ ସଭାର ପରିଚାଳନା ଯୋଜନାଗୁଡ଼ିକ ପାଇଁ କେବଳ ବୈଷୟିକ ସହାୟତା ପ୍ରଦାନ କରିବେ।\n"
                "ଏହି ଦଲିଲ ସମ୍ପ୍ରଦାୟର ଅର୍ଥନୈତିକ ବିକାଶ ଏବଂ ଜଙ୍ଗଲର ସ୍ଥିରତା ଉଭୟକୁ ଏକାସାଥିରେ ସୁନିଶ୍ଚିତ କରିବ।\n"
                "ସମ୍ପୃକ୍ତ ଅଧିକାରୀମାନଙ୍କ ଯଥାବିଧି ସ୍ୱାକ୍ଷର ସହିତ ଏହି ପଟ୍ଟା ଆଜିଠାରୁ ପ୍ରଭାବୀ ହୋଇଛି।"
            ),
            # Variation 3: Formal Letter Style
            (
                "ଶୀର୍ଷକ: ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦ (CFR) ଉପରେ ଅଧିକାର ଏବଂ ପଟ୍ଟା ପ୍ରମାଣପତ୍ର।\n"
                "ହିତାଧିକାରୀ ନିକାୟ: {GRAM_SABHA} ଗ୍ରାମ ସଭା, {VILLAGE} ଗ୍ରାମ, {GRAM_PANCHAYAT} ପଞ୍ଚାୟତ।\n"
                "ସ୍ଥାନ: ତହସିଲ {TEHSIL_TALUKA}, ଜିଲ୍ଲା {DISTRICT}, ରାଜ୍ୟ {STATE}।\n"
                "ସମ୍ପ୍ରଦାୟର ବର୍ଗୀକରଣ: {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} ଅଥବା {COMMUNITY_TYPE_BOTH}।\n"
                "ବିଷୟ: ଉପରୋକ୍ତ ଗ୍ରାମ ସଭାକୁ ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦର ପରିଚାଳନାର ଆଧିକାରିକ ଅଧିକାର ପ୍ରଦାନ କରିବା।\n\n"

                "ଜଙ୍ଗଲ ଅଧିକାର ଅଧିନିୟମ ୨୦୦୬ ର ପ୍ରାବଧାନଗୁଡ଼ିକ ଆଧାରରେ ଏହି ଐତିହାସିକ ଅଧିକାର ପ୍ରଦାନ କରାଯାଉଛି।\n"
                "ଅଧିକାର ପ୍ରାପ୍ତ ଜଙ୍ଗଲ କ୍ଷେତ୍ରର ଖସଡା କିମ୍ବା ମାପ ସଂଖ୍ୟା {KHASRA_COMPARTMENT_NUMBER} ସ୍ପଷ୍ଟ ରୂପେ ଦର୍ଜ କରାଯାଇଛି।\n"
                "ସେହି କ୍ଷେତ୍ରର ସୀମାକୁ {BOUNDARY_DESCRIPTION} ବିବରଣୀ ମାଧ୍ୟମରେ ଭୌଗୋଳିକ ରୂପେ ପରିଭାଷିତ କରାଯାଇଛି।\n"
                "ସମ୍ପ୍ରଦାୟ ଦ୍ୱାରା ପାରମ୍ପରିକ ଭାବରେ ଅନୁରକ୍ଷିତ ରୀତିନୀତି ସୀମା {CUSTOMARY_BOUNDARY} ମଧ୍ୟ ଏଥିରେ ସାମିଲ ଅଛି।\n"
                "ଏହି ସୀମା ଭିତରେ ସମସ୍ତ ପ୍ରାକୃତିକ ସମ୍ପଦର ରକ୍ଷା ଏବଂ ଉପଯୋଗ କରିବାର ଅଧିକାର ଗ୍ରାମ ସଭାର ଅଟେ।\n\n"

                "ଏହି ଅଧିକାର କୌଣସି ବି ପ୍ରକାରରେ ବ୍ୟକ୍ତି ବିଶେଷଙ୍କର ନୁହେଁ, ଏହା ସମଗ୍ର ସମ୍ପ୍ରଦାୟର ସାଧାରଣ ସମ୍ପତ୍ତି ଅଟେ।\n"
                "ଜଙ୍ଗଲ ସମ୍ପଦର ସ୍ଥାୟୀ ପରିଚାଳନା ପାଇଁ ଗ୍ରାମ ସଭାକୁ ଏକ ଜଙ୍ଗଲ ଅଧିକାର ସମିତି ଗଠନ କରି କାର୍ଯ୍ୟ କରିବା ଉଚିତ।\n"
                "ଜଙ୍ଗଲ ନିଆଁ (ଦାବାନଳ) ଭଳି ପ୍ରାକୃତିକ ବିପର୍ଯ୍ୟୟରୁ ଜଙ୍ଗଲକୁ ବଞ୍ଚାଇବା ସମ୍ପ୍ରଦାୟର ପ୍ରାଥମିକ କର୍ତ୍ତବ୍ୟ ଅଟେ।\n"
                "ଏହି ଅଧିକାର ରାଜ୍ୟ ସ୍ତରୀୟ କମିଟି ଦ୍ୱାରା ସମୀକ୍ଷା ଏବଂ ଚୂଡାନ୍ତ ସ୍ୱୀକୃତି ପରେ ପ୍ରଦାନ କରାଯାଉଛି।\n"
                "ଏହି ପ୍ରମାଣପତ୍ର ସମ୍ପୃକ୍ତ ଜିଲ୍ଲା ଅଧିକାରୀମାନଙ୍କ ମୋହର ସହିତ ଆଧିକାରିକ ତତ୍ତ୍ୱରେ ଜାରି କରାଯାଉଛି।"
            ),
            # Variation 4: Legal / Statutory Document Style
            (
                "ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦ (Community Forest Resources) ର ବୈଧାନିକ ପଟ୍ଟା ଏବଂ ସରକାରଙ୍କ ଅଧିକାର ହସ୍ତାନ୍ତର ପ୍ରଲେଖ।\n"
                "ଧାରା ୩(୧)(ଝ) ର ପ୍ରାବଧାନ ଅନ୍ତର୍ଗତ, {STATE} ରାଜ୍ୟ, {DISTRICT} ଜିଲ୍ଲା, {TEHSIL_TALUKA} ତହସିଲର କ୍ଷେତ୍ରାଧିକାରରେ ଏହି ବିଲେଖ ବୈଧାନିକ ରୂପେ ନିଷ୍ପାଦିତ କରାଯାଉଛି।\n"
                "ତଦନୁଯାୟୀ, {VILLAGE} ଗ୍ରାମ, {GRAM_PANCHAYAT} ଗ୍ରାମ ପଞ୍ଚାୟତ ତଥା {GRAM_SABHA} ଗ୍ରାମ ସଭାକୁ ଗୋଷ୍ଠୀ ଜଙ୍ଗଲ ସମ୍ପଦର ପରିଚାଳନାର ପୂର୍ଣ୍ଣ ବୈଧାନିକ ଅଧିକାର ସମର୍ପିତ କରାଯାଉଛି।\n"
                "ଏହି ପ୍ରଲେଖ, {COMMUNITY_TYPE_SCHEDULED_TRIBE}, {COMMUNITY_TYPE_OTHER_TFD} ଅଥବା {COMMUNITY_TYPE_BOTH} ସମ୍ପ୍ରଦାୟଗୁଡ଼ିକ ସହ ଜଡିତ ନିବାସୀମାନଙ୍କ ଜୀବିକାକୁ ସୁରକ୍ଷିତ କରୁଥିବା ଏକ ବିଧିକ ପ୍ରପତ୍ର ଅଟେ।\n"
                "ଜିଲ୍ଲା ସ୍ତରୀୟ କମିଟି (DLC) ର ଚୂଡାନ୍ତ ବିଧିକ ଅନୁମୋଦନ ପରେ ହିଁ ଏହି ଅଧିକାର ପ୍ରମାଣପତ୍ରକୁ ଆଧିକାରିକ ରୂପେ ପ୍ରକାଶିତ କରାଯାଉଛି।\n"
                "ଏହା ଦ୍ୱାରା, ରାଜ୍ୟର ସ୍ୱାମିତ୍ୱରେ ଥିବା ଜଙ୍ଗଲ ସମ୍ପଦର ସୁରକ୍ଷା ଏବଂ ପରିଚାଳନାର ଅଧିକାର ବୈଧାନିକ ରୂପେ ଗ୍ରାମ ସଭାକୁ ହସ୍ତାନ୍ତରିତ କରାଯାଉଛି।\n\n"

                "ଜଙ୍ଗଲ ସମ୍ପଦ କ୍ଷେତ୍ରର ବୈଧାନିକ ଭୂ-ସର୍ବେକ୍ଷଣ କ୍ରମାଙ୍କ, ସୀମାଗୁଡ଼ିକ ଏବଂ ରୀତିନୀତି ପ୍ରକଟିକରଣ।\n"
                "ସାମୂହିକ ପରିଚାଳନା ଅଧୀନରେ ଥିବା ଜଙ୍ଗଲ ସମ୍ପଦ କ୍ଷେତ୍ରର ଖସଡା (Khasra) କିମ୍ବା କମ୍ପାର୍ଟମେଣ୍ଟ ନମ୍ବର {KHASRA_COMPARTMENT_NUMBER} ଭୂ-ସର୍ବେକ୍ଷଣ ଅଭିଲେଖରେ ସ୍ପଷ୍ଟ ରୂପେ ଦର୍ଜ କରାଯାଇଛି।\n"
                "ଏହି କ୍ଷେତ୍ରର ଭୌଗୋଳିକ ଏବଂ ସ୍ଥଳାକୃତିକ ସୀମାଗୁଡ଼ିକ {BOUNDARY_DESCRIPTION} ରୂପେ ମାନଚିତ୍ର ଦ୍ୱାରା ସରକାରଙ୍କ ଦ୍ୱାରା ବିଧିକ ରୂପେ ପୁଷ୍ଟ କରାଯାଇଛି।\n"
                "ପଡୋଶୀ ଗ୍ରାମ ଏବଂ ଜଙ୍ଗଲ ବିଭାଗ ସହିତ ସୀମା ଭାଗ କରୁଥିବା ପାରମ୍ପରିକ ରୀତିନୀତି ସୀମା (Customary Boundary) {CUSTOMARY_BOUNDARY} ଆଧିକାରିକ ରୂପେ ପ୍ରମାଣିତ କରାଯାଉଛି।\n"
                "ଏହି ସୀମାଗୁଡ଼ିକ ଭିତରେ ଥିବା ଲଘୁ ବନଜାତ ଦ୍ରବ୍ୟ, ଜଳ ସମ୍ପଦ ଏବଂ ବନସ୍ପତିର ଉପଯୋଗ କରିବାର ପୂର୍ଣ୍ଣ ଅଧିକାର ଗ୍ରାମ ସଭାକୁ ପ୍ରଦାନ କରାଯାଇଛି।\n"
                "ସୀମା ସମ୍ବନ୍ଧୀୟ କୌଣସି ବି ବିବାଦରୁ ବଞ୍ଚିବା ପାଇଁ ଭୂମି ସର୍ବେକ୍ଷଣ ବିଭାଗ ମାଧ୍ୟମରେ ଉଚିତ ସୀମା-ସ୍ତମ୍ଭ ଏବଂ ବିଧିକ ଚିହ୍ନ ସ୍ଥାପିତ କରାଯାଇଛି।\n\n"

                "ଗ୍ରାମ ସଭାର ବୈଧାନିକ ଦାୟିତ୍ୱ, ଜଙ୍ଗଲ ସଂରକ୍ଷଣ ଏବଂ ଅଧିକାରୀମାନଙ୍କର ଚୂଡାନ୍ତ ପ୍ରମାଣୀକରଣ।\n"
                "ଅଧିନିୟମର ମୂଳ ନିୟମଗୁଡ଼ିକୁ ଛାଡି, ରାଜ୍ୟ ସରକାରଙ୍କ ଦ୍ୱାରା ଏହି ଅଧିକାର ଉପରେ କୌଣସି ଅନ୍ୟ ନୂତନ ପ୍ରତିବନ୍ଧକ କିମ୍ବା ସର୍ତ୍ତ ଲଗାଯାଇ ନାହିଁ।\n"
                "ତଥାପି, ଜଙ୍ଗଲର ପାରିସ୍ଥିତିକ ସନ୍ତୁଳନକୁ ବଜାୟ ରଖିବା ଏବଂ ଦାବାନଳ (Forest Fire) ଭଳି ବିପର୍ଯ୍ୟୟକୁ ରୋକିବା ଗ୍ରାମ ସଭାର ପୂର୍ଣ୍ଣ ବୈଧାନିକ ଦାୟିତ୍ୱ ହେବ।\n"
                "ଏହି ଉଦ୍ଦେଶ୍ୟ ପାଇଁ ଗ୍ରାମ ସଭା ପକ୍ଷରୁ 'ଜଙ୍ଗଲ ସମ୍ପଦ ସଂରକ୍ଷଣ ସମିତି' ର ଗଠନ କରାଯିବା ଅନିବାର୍ଯ୍ୟ ଅଟେ, ଯାହାର ରିପୋର୍ଟ ପ୍ରତିବର୍ଷ ସରକାରଙ୍କୁ ଉପସ୍ଥାପନ କରାଯିବ।\n"
                "ବିଧିକ ରୂପେ ଅବୈଧ ଉପାୟରେ ଜଙ୍ଗଲ ସମ୍ପଦର ବିନାଶ କରାଗଲେ, ଅପରାଧିକ ପ୍ରକ୍ରିୟା ସଂହିତା ଅନ୍ତର୍ଗତ ଗ୍ରାମ ସଭାକୁ ଜବାବଦେହୀ କରାଯିବ।\n"
                "ରାଜ୍ୟ ସରକାରଙ୍କ ଶୀର୍ଷ ଅଧିକାରୀ—ଜିଲ୍ଲାପାଳ, ଖଣ୍ଡୀୟ ଜଙ୍ଗଲ ଅଧିକାରୀ (DFO) ତଥା ଜନଜାତି କଲ୍ୟାଣ ଅଧିକାରୀଙ୍କ ସ୍ୱାକ୍ଷର ସହିତ ଏହି ପଟ୍ଟା ବୈଧାନିକ ରୂପେ ପ୍ରଭାବଶାଳୀ ହେଉଛି।"
            )
        ]
    }
}


PLACEHOLDER_RE = re.compile(r"\{([A-Z0-9_]+)\}")


def validate_templates_against_schema() -> None:
    """Ensure all placeholders used in templates have a SLOT2LABEL mapping.

    This keeps the label/schema code in sync with the templates when they change.
    """
    all_slots = set()
    for lang_templates in TEMPLATES.values():
        for templates in lang_templates.values():
            for tmpl in templates:
                for m in PLACEHOLDER_RE.finditer(tmpl):
                    all_slots.add(m.group(1))

    undefined = sorted(slot for slot in all_slots if slot not in SLOT2LABEL)
    if undefined:
        raise ValueError(f"Undefined template placeholders (no SLOT2LABEL mapping): {undefined}")


@dataclass
class EntitySpan:
    start: int
    end: int
    base_label: str


def sample_slot_value(lang: str, slot: str) -> str:
    # Map slot name to concrete value generators
    if slot in {"CLAIMANT_NAME", "SPOUSE_NAME", "FAMILY_MEMBER_NAME", "DEPENDENT_NAME",
                "TITLE_HOLDER_NAME", "COMMUNITY_RIGHT_HOLDER_NAME", "GRAM_SABHA_MEMBER_NAME"}:
        return sample_name(lang)
    if slot == "FAMILY_MEMBER_AGE":
        return sample_age()
    if slot == "VILLAGE":
        return sample_village(lang)
    if slot == "DISTRICT":
        return sample_district(lang)
    if slot == "STATE":
        return sample_state(lang)
    if slot == "TEHSIL_TALUKA":
        return sample_tehsil(lang)
    if slot == "GRAM_PANCHAYAT":
        # Use a village name as the panchayat name
        return sample_village(lang)
    if slot == "GRAM_SABHA":
        # Use a village name as the sabha name
        return sample_village(lang)
    if slot in {"LAND_EXTENT_HABITATION", "LAND_EXTENT_SELF_CULTIVATION",
                "LAND_EXTENT_FOREST_VILLAGE", "LAND_AREA_MEASURE", "TITLE_LAND_AREA_MEASURE"}:
        return sample_land_area(lang)
    if slot == "RIGHT_MINOR_FOREST_PRODUCE":
        return sample_minor_forest_produce(lang)
    if slot in {"BOUNDARY_DESCRIPTION", "CUSTOMARY_BOUNDARY"}:
        return sample_boundary_description(lang)
    if slot == "KHASRA_COMPARTMENT_NUMBER":
        return sample_khasra(lang)
    if slot == "COMMUNITY_TYPE_FDST":
        return sample_community_type_fdst(lang)
    if slot == "COMMUNITY_TYPE_OTFD":
        return sample_community_type_otfd(lang)
    if slot == "CATEGORY_SCHEDULED_TRIBE":
        # Use localized ST label from caste/category pools
        return CASTE_CATEGORIES[lang][0]
    if slot == "CATEGORY_OTHER_TRADITIONAL_FOREST_DWELLER":
        # Use localized OTFD label from caste/category pools
        return CASTE_CATEGORIES[lang][1]
    if slot == "COMMUNITY_TYPE_SCHEDULED_TRIBE":
        # Reuse localized ST community description
        return CASTE_CATEGORIES[lang][0]
    if slot == "COMMUNITY_TYPE_OTHER_TFD":
        # Reuse localized OTFD community description
        return CASTE_CATEGORIES[lang][1]
    if slot == "COMMUNITY_TYPE_BOTH":
        if lang == "hi":
            return "अनुसूचित जनजाति (ST) और अन्य पारंपरिक वनवासी (OTFD) दोनों समुदाय"
        if lang == "ta":
            return "ST மற்றும் OTFD இரு சமூகங்கள்"
        if lang == "te":
            return "ST మరియు OTFD రెండు సమూహాలు"
        if lang == "bn":
            return "ST এবং OTFD উভয় সম্প্রদায়"
        if lang == "or":
            return "ST ଏବଂ OTFD ଉଭୟ ସମ୍ପ୍ରଦାୟ"
        return "ST and OTFD communities"
    if slot in {"COMMUNITY_RIGHT_NISTAR", "COMMUNITY_RIGHT_RESOURCE_USE",
                "COMMUNITY_RIGHT_GRAZING", "COMMUNITY_RIGHT_NOMADIC_PASTORALIST_ACCESS",
                "COMMUNITY_TENURE_HABITAT", "COMMUNITY_RIGHT_BIODIVERSITY_IPR_TK",
                "COMMUNITY_RIGHT_NATURE", "DISPUTED_LAND_DESCRIPTION",
                "EXISTING_PATTAS_LEASES_GRANTS", "REHABILITATION_LAND",
                "DISPLACED_FROM_LAND", "OTHER_TRADITIONAL_RIGHT",
                "OTHER_INFORMATION", "TITLE_CONDITIONS"}:
        # Generic descriptive text, can be refined per language
        if lang == "hi":
            return "प्रचलित प्रथागत अधिकार"
        if lang == "ta":
            return "பழமையான வழக்குரிமை"
        if lang == "te":
            return "పారంపర్య హక్కు"
        if lang == "bn":
            return "প্রচলিত প্রথাগত অধিকার"
        if lang == "or":
            return "ପାରମ୍ପରିକ ଅଧିକାର"
    if slot == "EVIDENCE_ITEM":
        return RNG.choice(EVIDENCE_POOLS[lang])
    if slot == "COMMUNITY_FOREST_RESOURCE_EVIDENCE_LIST":
        # Join a couple of evidence items to simulate a list
        items = RNG.sample(EVIDENCE_POOLS[lang], k=min(2, len(EVIDENCE_POOLS[lang])))
        return ", ".join(items)
    if slot in {"TITLE_ADDRESS_FULL", "ADDRESS_FULL"}:
        return sample_address(lang)
    if slot == "BORDERING_VILLAGE":
        return sample_village(lang)
    # Fallback: slot name itself (should rarely happen)
    return slot


def fill_template(lang: str, template: str) -> Tuple[str, List[EntitySpan]]:
    """Replace placeholders in template with values and track char spans."""
    result_parts: List[str] = []
    entities: List[EntitySpan] = []
    last_index = 0
    for m in PLACEHOLDER_RE.finditer(template):
        result_parts.append(template[last_index:m.start()])
        slot = m.group(1)
        base_label = SLOT2LABEL.get(slot)
        value = sample_slot_value(lang, slot)
        start_char = sum(len(p) for p in result_parts)
        result_parts.append(value)
        end_char = start_char + len(value)
        if base_label is not None:
            entities.append(EntitySpan(start=start_char, end=end_char, base_label=base_label))
        last_index = m.end()
    result_parts.append(template[last_index:])
    text = "".join(result_parts)
    return text, entities


def tokenize_simple(text: str) -> List[str]:
    """Very simple whitespace tokenizer. Works reasonably for Indic scripts with spaces."""
    return text.split()


def align_spans_to_tokens(text: str, entities: List[EntitySpan], words: List[str]) -> List[int]:
    """Convert character-level entity spans to BIO label IDs per word.

    We align by checking overlap between word char range and entity span.
    """
    # Build word char ranges
    word_spans: List[Tuple[int, int]] = []
    offset = 0
    for w in words:
        # Skip leading whitespace
        while offset < len(text) and text[offset].isspace():
            offset += 1
        start = offset
        end = start + len(w)
        word_spans.append((start, end))
        offset = end

    ner_ids = [LABEL2ID["O"]] * len(words)

    for ent in entities:
        b_id, i_id = bio_ids(ent.base_label)
        first_token = True
        for idx, (w_start, w_end) in enumerate(word_spans):
            if w_end <= ent.start or w_start >= ent.end:
                continue
            if first_token:
                ner_ids[idx] = b_id
                first_token = False
            else:
                ner_ids[idx] = i_id

    return ner_ids


def generate_examples_for_doc_type(
    lang: str,
    doc_type: str,
    num_per_variation: int,
) -> List[Dict]:
    """Generate num_per_variation examples for each template variation of a doc_type.

    If there are 4 variations and num_per_variation=50, this yields 200 examples
    for that (language, doc_type) pair.
    """
    examples: List[Dict] = []
    templates = TEMPLATES[lang][doc_type]
    for template in templates:
        for _ in range(num_per_variation):
            text, spans = fill_template(lang, template)
            words = tokenize_simple(text)
            ner = align_spans_to_tokens(text, spans, words)
            examples.append(
                {
                    "language": lang,
                    "doc_type": doc_type,
                    "text": text,
                    "words": words,
                    "ner": ner,
                }
            )
    return examples


def generate_dataset_per_language(
    lang: str,
    num_per_variation: int = 50,
) -> List[Dict]:
    all_examples: List[Dict] = []
    for doc_type in [
        DOC_CLAIM_FOREST_LAND,
        DOC_CLAIM_COMMUNITY_RIGHTS,
        DOC_CLAIM_COMMUNITY_FOREST_RESOURCE,
        DOC_TITLE_UNDER_OCCUPATION,
        DOC_TITLE_COMMUNITY_FOREST_RIGHTS,
        DOC_TITLE_COMMUNITY_FOREST_RESOURCES,
    ]:
        if doc_type in TEMPLATES[lang]:
            all_examples.extend(
                generate_examples_for_doc_type(lang, doc_type, num_per_variation)
            )
    return all_examples


def save_jsonl(path: Path, records: List[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def main() -> None:
    # Sanity-check that template placeholders match SLOT2LABEL/schema
    validate_templates_against_schema()

    output_dir = Path("data_synthetic-3")
    output_dir.mkdir(exist_ok=True)

    # Save label list for reference
    labels_path = output_dir / "labels.json"
    with labels_path.open("w", encoding="utf-8") as f:
        json.dump({"labels": LABEL_LIST}, f, ensure_ascii=False, indent=2)

    # Generate datasets for each language.
    # Each language has 6 doc types; each doc type has 4 variations; we
    # generate 50 examples per variation => 6 * 4 * 50 = 1200 per language.
    for lang in ["hi", "ta", "te", "bn", "or"]:
        examples = generate_dataset_per_language(lang, num_per_variation=50)
        out_path = output_dir / f"synthetic_{lang}.jsonl"
        save_jsonl(out_path, examples)
        print(f"Saved {len(examples)} examples to {out_path}")


if __name__ == "__main__":
    main()
